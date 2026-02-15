# splits_metrics.py
from __future__ import annotations
from typing import Dict, Tuple
import math
import numpy as np
import torch

try:
    from sklearn.metrics import (
        roc_auc_score, average_precision_score,
        f1_score, precision_score, recall_score
    )
    _HAS_SK = True
except Exception:
    _HAS_SK = False


def stratified_node_split(
    data,
    y_key: str = "y_bin",
    eligible_mask_key: str = "train_mask",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    seed: int = 42,
):
    """
    결과:
      data.split_train_mask, data.split_val_mask, data.split_test_mask
    """
    y = getattr(data, y_key).long()
    n = int(y.numel())

    if hasattr(data, eligible_mask_key):
        eligible = getattr(data, eligible_mask_key).bool()
    else:
        eligible = torch.ones(n, dtype=torch.bool)

    eligible = eligible & (y >= 0)
    idx = torch.where(eligible)[0]
    yv = y[idx]

    pos = idx[yv == 1]
    neg = idx[yv == 0]

    g = torch.Generator()
    g.manual_seed(seed)

    pos = pos[torch.randperm(pos.numel(), generator=g)]
    neg = neg[torch.randperm(neg.numel(), generator=g)]

    def _split(arr: torch.Tensor):
        n_ = arr.numel()
        n_tr = int(n_ * train_ratio)
        n_va = int(n_ * val_ratio)
        n_te = n_ - n_tr - n_va
        if n_ >= 3 and n_te == 0:
            n_te = 1
            if n_va > 1:
                n_va -= 1
            elif n_tr > 1:
                n_tr -= 1
        tr = arr[:n_tr]
        va = arr[n_tr:n_tr + n_va]
        te = arr[n_tr + n_va:]
        return tr, va, te

    p_tr, p_va, p_te = _split(pos)
    n_tr, n_va, n_te = _split(neg)

    tr_idx = torch.cat([p_tr, n_tr], dim=0)
    va_idx = torch.cat([p_va, n_va], dim=0)
    te_idx = torch.cat([p_te, n_te], dim=0)

    tr_mask = torch.zeros(n, dtype=torch.bool)
    va_mask = torch.zeros(n, dtype=torch.bool)
    te_mask = torch.zeros(n, dtype=torch.bool)

    tr_mask[tr_idx] = True
    va_mask[va_idx] = True
    te_mask[te_idx] = True

    data.split_train_mask = tr_mask
    data.split_val_mask = va_mask
    data.split_test_mask = te_mask
    return data


def _safe_div(a: float, b: float, eps: float = 1e-12) -> float:
    return a / (b + eps)


def binary_metrics_from_logits(
    logits: torch.Tensor,
    y_true: torch.Tensor,
    mask: torch.Tensor,
    threshold: float = 0.5,
) -> Dict[str, float]:
    logits = logits.detach().cpu()
    y_true = y_true.detach().cpu().long()
    mask = mask.detach().cpu().bool()

    logits = logits[mask]
    y = y_true[mask]
    if y.numel() == 0:
        return {"auroc": math.nan, "ap": math.nan, "f1": math.nan, "precision": math.nan, "recall": math.nan}

    p = torch.sigmoid(logits).numpy()
    yt = y.numpy().astype(np.int64)
    pred = (p >= threshold).astype(np.int64)

    tp = int(((pred == 1) & (yt == 1)).sum())
    fp = int(((pred == 1) & (yt == 0)).sum())
    fn = int(((pred == 0) & (yt == 1)).sum())

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2.0 * precision * recall, precision + recall)

    if _HAS_SK and len(np.unique(yt)) >= 2:
        auroc = float(roc_auc_score(yt, p))
        ap = float(average_precision_score(yt, p))
        precision = float(precision_score(yt, pred, zero_division=0))
        recall = float(recall_score(yt, pred, zero_division=0))
        f1 = float(f1_score(yt, pred, zero_division=0))
    else:
        auroc = math.nan
        ap = math.nan

    return {
        "auroc": auroc,
        "ap": ap,
        "f1": float(f1),
        "precision": float(precision),
        "recall": float(recall),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "n": int(y.numel()),
    }


def multiclass_macro_f1(
    type_logits: torch.Tensor,
    y_type: torch.Tensor,
    mask: torch.Tensor,
    ignore_index: int = -1,
) -> Dict[str, float]:
    type_logits = type_logits.detach().cpu()
    y_type = y_type.detach().cpu().long()
    mask = mask.detach().cpu().bool()

    valid = mask & (y_type != ignore_index)
    if valid.sum() == 0:
        return {"macro_f1": math.nan}

    pred = type_logits[valid].argmax(dim=-1).numpy().astype(np.int64)
    yt = y_type[valid].numpy().astype(np.int64)

    if _HAS_SK:
        from sklearn.metrics import f1_score
        macro = float(f1_score(yt, pred, average="macro", zero_division=0))
        return {"macro_f1": macro}

    classes = sorted(set(yt.tolist()))
    f1s = []
    for c in classes:
        tp = int(((pred == c) & (yt == c)).sum())
        fp = int(((pred == c) & (yt != c)).sum())
        fn = int(((pred != c) & (yt == c)).sum())
        p = _safe_div(tp, tp + fp)
        r = _safe_div(tp, tp + fn)
        f1 = _safe_div(2 * p * r, p + r)
        f1s.append(f1)
    return {"macro_f1": float(np.mean(f1s)) if f1s else math.nan}


def evaluate_multitask(
    out: Dict[str, torch.Tensor],
    data,
    mask_bin: torch.Tensor,
    mask_type: torch.Tensor,
    threshold: float = 0.5,
):
    m_bin = binary_metrics_from_logits(out["bin_logits"], data.y_bin, mask_bin, threshold)
    m_type = multiclass_macro_f1(out["type_logits"], data.y_type, mask_type)
    merged = {}
    merged.update({f"bin_{k}": v for k, v in m_bin.items()})
    merged.update({f"type_{k}": v for k, v in m_type.items()})
    return merged  