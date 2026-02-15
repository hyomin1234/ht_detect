# hybrid_trojan_pyg.py
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GINConv, GATv2Conv, GPSConv


class DirGATv2Block(nn.Module):
    """
    edge_index 정방향 + 역방향 attention 융합
    """
    def __init__(self, dim: int, edge_dim: int = 3, heads: int = 4, dropout: float = 0.1, alpha: float = 0.5):
        super().__init__()
        assert dim % heads == 0
        od = dim // heads

        self.gat_fwd = GATv2Conv(
            in_channels=dim,
            out_channels=od,
            heads=heads,
            concat=True,
            edge_dim=edge_dim,
            dropout=dropout,
        )
        self.gat_rev = GATv2Conv(
            in_channels=dim,
            out_channels=od,
            heads=heads,
            concat=True,
            edge_dim=edge_dim,
            dropout=dropout,
        )
        self.alpha = alpha
        self.norm = nn.LayerNorm(dim)
        self.drop = nn.Dropout(dropout)

    def forward(self, x, edge_index, edge_attr):
        x_f = self.gat_fwd(x, edge_index, edge_attr=edge_attr)
        x_r = self.gat_rev(x, edge_index.flip(0), edge_attr=edge_attr)
        out = self.alpha * x_f + (1.0 - self.alpha) * x_r
        out = self.norm(x + self.drop(out))
        return out


class HybridTrojanNetPyG(nn.Module):
    """
    Inputs:
      data.gate_type_id [N]
      data.num_feat     [N, 5] -> [CC0,CC1,CO,SW,depth]
      data.edge_index   [2, E]
      data.edge_attr    [E, 3] -> [delta_depth,seq_edge,rare_dst]
    Output:
      logits [N]
    """
    def __init__(
        self,
        num_gate_types: int,
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

        # rare/trigger 강조 게이트 (SCOAP + SW 활용)
        self.risk_gate = nn.Sequential(
            nn.Linear(num_num_feat, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )

        # (A) Local: GIN
        gin_mlp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.local_gin = GINConv(gin_mlp, train_eps=True)

        # (B) Directional: GATv2
        self.dir_attn = DirGATv2Block(
            dim=hidden_dim,
            edge_dim=edge_dim,
            heads=heads,
            dropout=dropout,
            alpha=0.5,
        )

        # (C) Global: GPS (global attention)
        self.global_gps = GPSConv(
            channels=hidden_dim,
            conv=None,           # global-only branch로 사용
            heads=heads,
            dropout=dropout,
            attn_type="multihead",
        )

        self.fuse = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.cls = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, data):
        gate_id = data.gate_type_id.long()
        num_feat = data.num_feat.float()
        edge_index = data.edge_index
        edge_attr = data.edge_attr.float()

        h_gate = self.gate_emb(gate_id)
        h_num = self.num_proj(num_feat)
        x = self.in_proj(torch.cat([h_gate, h_num], dim=-1))

        risk = self.risk_gate(num_feat)          # [N,1]
        x = x * (1.0 + risk)

        x_local = self.local_gin(x, edge_index)
        x_dir = self.dir_attn(x_local, edge_index, edge_attr=edge_attr)

        batch = getattr(data, "batch", None)
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        x_global = self.global_gps(x_dir, edge_index=edge_index, batch=batch)

        x_fused = self.fuse(torch.cat([x_local, x_dir, x_global], dim=-1))
        logits = self.cls(x_fused).squeeze(-1)
        return logits


class FocalBCEWithLogits(nn.Module):
    def __init__(self, alpha: float = 0.25, gamma: float = 2.0, pos_weight: torch.Tensor | None = None):
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
            logits,
            target,
            reduction="none",
            pos_weight=self.pos_weight
        )
        p = torch.sigmoid(logits)
        pt = p * target + (1.0 - p) * (1.0 - target)
        focal = (1.0 - pt).pow(self.gamma)
        alpha_t = self.alpha * target + (1.0 - self.alpha) * (1.0 - target)
        return (alpha_t * focal * bce).mean()