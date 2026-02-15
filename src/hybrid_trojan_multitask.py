# hybrid_trojan_multitask.py
from __future__ import annotations
from typing import Optional, Dict

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GINConv, GATv2Conv, GPSConv

class DirGATv2Block(nn.Module):
    def __init__(self, dim: int, edge_dim: int = 3, heads: int = 4, dropout: float = 0.1, alpha: float = 0.5):
        super().__init__()
        assert dim % heads == 0
        out_dim = dim // heads
        self.fwd = GATv2Conv(dim, out_dim, heads=heads, concat=True, edge_dim=edge_dim, dropout=dropout)
        self.rev = GATv2Conv(dim, out_dim, heads=heads, concat=True, edge_dim=edge_dim, dropout=dropout)
        self.alpha = alpha
        self.norm = nn.LayerNorm(dim)
        self.drop = nn.Dropout(dropout)

    def forward(self, x, edge_index, edge_attr):
        xf = self.fwd(x, edge_index, edge_attr=edge_attr)
        xr = self.rev(x, edge_index.flip(0), edge_attr=edge_attr)
        out = self.alpha * xf + (1.0 - self.alpha) * xr
        return self.norm(x + self.drop(out))


class FocalBCEWithLogits(nn.Module):
    def __init__(self, alpha: float = 0.25, gamma: float = 2.0, pos_weight: Optional[torch.Tensor] = None):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        if pos_weight is not None:
            self.register_buffer("pos_weight", pos_weight.float())
        else:
            self.pos_weight = None

    def forward(self, logits: torch.Tensor, target: torch.Tensor):
        target = target.float()
        bce = F.binary_cross_entropy_with_logits(
            logits, target, reduction="none", pos_weight=self.pos_weight
        )
        p = torch.sigmoid(logits)
        pt = p * target + (1.0 - p) * (1.0 - target)
        focal = (1.0 - pt).pow(self.gamma)
        alpha_t = self.alpha * target + (1.0 - self.alpha) * (1.0 - target)
        return (alpha_t * focal * bce).mean()


class HybridTrojanNetPyGMultiTask(nn.Module):
    """
    output:
      {
        "bin_logits": [N],
        "type_logits": [N, num_types],
        "emb": [N, H]
      }
    """
    def __init__(
        self,
        num_gate_types: int,
        num_types: int = 5,            # normal/leakage/trigger/control/logic
        num_num_feat: int = 5,
        edge_dim: int = 3,
        hidden_dim: int = 128,
        gate_emb_dim: int = 32,
        heads: int = 4,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.gate_emb = nn.Embedding(num_gate_types, gate_emb_dim)
        self.num_proj = nn.Sequential(
            nn.Linear(num_num_feat, gate_emb_dim),
            nn.ReLU(),
            nn.Linear(gate_emb_dim, gate_emb_dim),
        )
        self.in_proj = nn.Sequential(
            nn.Linear(gate_emb_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
        )

        # SCOAP/activity 기반 rare 강조
        self.risk_gate = nn.Sequential(
            nn.Linear(num_num_feat, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )

        gin_mlp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.local_gin = GINConv(gin_mlp, train_eps=True)
        self.dir_attn = DirGATv2Block(hidden_dim, edge_dim=edge_dim, heads=heads, dropout=dropout, alpha=0.5)

        self.global_gps = GPSConv(
            channels=hidden_dim,
            conv=None,          # 글로벌 attention branch
            heads=heads,
            dropout=dropout,
            attn_type="multihead",
        )

        self.fuse = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
        )

        self.bin_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1),
        )
        self.type_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, num_types),
        )

    def forward(self, data):
        gate_id = data.gate_type_id.long()
        num_feat = data.num_feat.float()
        edge_index = data.edge_index
        edge_attr = data.edge_attr.float()

        h_gate = self.gate_emb(gate_id)
        h_num = self.num_proj(num_feat)
        x = self.in_proj(torch.cat([h_gate, h_num], dim=-1))

        risk = self.risk_gate(num_feat)
        x = x * (1.0 + risk)

        x_local = self.local_gin(x, edge_index)
        x_dir = self.dir_attn(x_local, edge_index, edge_attr)

        batch = getattr(data, "batch", None)
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        x_global = self.global_gps(x_dir, edge_index=edge_index, batch=batch)

        emb = self.fuse(torch.cat([x_local, x_dir, x_global], dim=-1))
        bin_logits = self.bin_head(emb).squeeze(-1)
        type_logits = self.type_head(emb)
        return {"bin_logits": bin_logits, "type_logits": type_logits, "emb": emb}




class MultiTaskLoss(nn.Module):
    """
    - Binary node loss: OHEM-BCE + Asymmetric Focal + Soft Dice
    - Type loss: weighted CE
    - Graph count loss: per-graph predicted trojan count alignment
    """
    def __init__(
        self,
        pos_weight: torch.Tensor,
        type_class_weight: torch.Tensor | None = None,
        lambda_type: float = 0.25,
        lambda_cons: float = 0.0,
        lambda_count: float = 0.35,
        neg_keep_ratio: float = 0.25,
        gamma_pos: float = 1.0,
        gamma_neg: float = 3.0,
        w_bce: float = 1.0,
        w_focal: float = 0.8,
        w_dice: float = 0.4,
    ):
        super().__init__()
        self.register_buffer("pos_weight", pos_weight.float())
        if type_class_weight is not None:
            self.register_buffer("type_class_weight", type_class_weight.float())
        else:
            self.type_class_weight = None

        self.lambda_type = float(lambda_type)
        self.lambda_cons = float(lambda_cons)
        self.lambda_count = float(lambda_count)
        self.neg_keep_ratio = float(neg_keep_ratio)

        self.gamma_pos = float(gamma_pos)
        self.gamma_neg = float(gamma_neg)

        self.w_bce = float(w_bce)
        self.w_focal = float(w_focal)
        self.w_dice = float(w_dice)

    def _ohem_bce(self, logits, targets):
        # logits, targets: [N]
        per = F.binary_cross_entropy_with_logits(
            logits, targets, reduction="none", pos_weight=self.pos_weight
        )

        pos_mask = targets > 0.5
        neg_mask = ~pos_mask

        pos_loss = per[pos_mask]
        neg_loss = per[neg_mask]

        if neg_loss.numel() > 0:
            k = max(1, int(self.neg_keep_ratio * neg_loss.numel()))
            neg_topk = torch.topk(neg_loss, k=k, largest=True).values
            if pos_loss.numel() > 0:
                return torch.cat([pos_loss, neg_topk], dim=0).mean()
            return neg_topk.mean()

        if pos_loss.numel() > 0:
            return pos_loss.mean()

        return per.mean() * 0.0

    def _asym_focal_with_logits(self, logits, targets):
        p = torch.sigmoid(logits).clamp(1e-6, 1.0 - 1e-6)
        pt = torch.where(targets > 0.5, p, 1.0 - p)
        gamma = torch.where(
            targets > 0.5,
            torch.full_like(pt, self.gamma_pos),
            torch.full_like(pt, self.gamma_neg),
        )
        mod = (1.0 - pt) ** gamma
        ce = -(targets * torch.log(p) + (1.0 - targets) * torch.log(1.0 - p))
        return (mod * ce).mean()

    def _soft_dice_loss_with_logits(self, logits, targets):
        p = torch.sigmoid(logits)
        num = 2.0 * (p * targets).sum() + 1.0
        den = p.sum() + targets.sum() + 1.0
        dice = num / den
        return 1.0 - dice

    def _graph_count_loss(self, logits, targets, valid_mask, batch_idx):
        # logits/targets/valid_mask/batch_idx: [N]
        p = torch.sigmoid(logits)
        uniq = torch.unique(batch_idx)
        losses = []
        for g in uniq:
            gm = (batch_idx == g) & valid_mask
            if gm.sum() == 0:
                continue
            pred_cnt = p[gm].sum()
            true_cnt = targets[gm].sum()

            # sparse graph(트로이 게이트 적음) 가중치 증가
            sparse_w = 2.0 if true_cnt.item() <= 64 else 1.0

            # SmoothL1 with moderate beta
            l = F.smooth_l1_loss(pred_cnt, true_cnt, beta=8.0, reduction="mean")
            losses.append(sparse_w * l)

        if len(losses) == 0:
            return logits.sum() * 0.0
        return torch.stack(losses).mean()

    def forward(self, out, data, mask_bin, mask_type):
        logits_bin = out["bin_logits"].view(-1)
        y_bin_full = data.y_bin.view(-1).float()

        valid_bin = mask_bin & (y_bin_full >= 0)
        if valid_bin.sum() == 0:
            zero = logits_bin.sum() * 0.0
            return zero, {
                "loss_bin": 0.0, "loss_type": 0.0, "loss_count": 0.0, "loss_total": 0.0
            }

        lb = logits_bin[valid_bin]
        yb = y_bin_full[valid_bin]

        loss_bce = self._ohem_bce(lb, yb)
        loss_focal = self._asym_focal_with_logits(lb, yb)
        loss_dice = self._soft_dice_loss_with_logits(lb, yb)
        loss_bin = self.w_bce * loss_bce + self.w_focal * loss_focal + self.w_dice * loss_dice

        # type loss
        loss_type = logits_bin.sum() * 0.0
        if "type_logits" in out and hasattr(data, "y_type"):
            logits_type = out["type_logits"]  # [N, C]
            y_type = data.y_type.view(-1).long()
            valid_type = mask_type & (y_type >= 0)
            if valid_type.sum() > 0:
                loss_type = F.cross_entropy(
                    logits_type[valid_type],
                    y_type[valid_type],
                    weight=self.type_class_weight if hasattr(self, "type_class_weight") else None
                )

        # graph count loss
        if hasattr(data, "batch"):
            batch_idx = data.batch.view(-1)
        else:
            batch_idx = torch.zeros_like(y_bin_full, dtype=torch.long)
        loss_count = self._graph_count_loss(
            logits_bin, y_bin_full, valid_bin, batch_idx
        )

        loss = loss_bin + self.lambda_type * loss_type + self.lambda_count * loss_count

        logs = {
            "loss_bin": float(loss_bin.detach().cpu().item()),
            "loss_type": float(loss_type.detach().cpu().item()),
            "loss_count": float(loss_count.detach().cpu().item()),
            "loss_total": float(loss.detach().cpu().item()),
        }
        return loss, logs