from __future__ import annotations
from typing import List, Set, Dict, Tuple, Optional
import numpy as np
import torch


# -----------------------------
# Basic utilities
# -----------------------------
def gate_prf(pred: Set[str], gt: Set[str]) -> Dict[str, float]:
    tp = len(pred & gt)
    fp = len(pred - gt)
    fn = len(gt - pred)
    p = tp / (tp + fp + 1e-12)
    r = tp / (tp + fn + 1e-12)
    f1 = 2 * p * r / (p + r + 1e-12)
    return {"p": p, "r": r, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


def _to_cpu_bool(x: torch.Tensor) -> torch.Tensor:
    return x.detach().cpu().bool()


def get_valid_mask(data) -> torch.Tensor:
    """
    보통 train_mask를 PIs 제외용 valid mask로 사용.
    없으면 전체 노드 valid.
    """
    n = int(data.num_nodes)
    if hasattr(data, "train_mask"):
        m = data.train_mask
        if torch.is_tensor(m):
            m = _to_cpu_bool(m)
            if m.numel() == n:
                return m
    return torch.ones(n, dtype=torch.bool)


def get_node_names(data) -> List[str]:
    """
    data.node_names를 안전하게 문자열 리스트로 변환.
    """
    n = int(data.num_nodes)
    if not hasattr(data, "node_names"):
        return [f"g{i}" for i in range(n)]

    names = data.node_names
    # 대부분 list[str]일 것
    if isinstance(names, list):
        if len(names) == n:
            return [str(x) for x in names]
        # 길이 불일치 시 fallback
        out = [str(x) for x in names[:n]]
        if len(out) < n:
            out += [f"g{i}" for i in range(len(out), n)]
        return out

    # tensor/ndarray 등 fallback
    try:
        arr = list(names)
        out = [str(x) for x in arr[:n]]
        if len(out) < n:
            out += [f"g{i}" for i in range(len(out), n)]
        return out
    except Exception:
        return [f"g{i}" for i in range(n)]


def graph_score_from_probs(probs: torch.Tensor, valid_mask: torch.Tensor, q: float = 0.995) -> float:
    v = probs[valid_mask]
    if v.numel() == 0:
        return 0.0
    if v.numel() < 50:
        return float(v.max().item())
    return float(torch.quantile(v, q).item())


def build_adj_undirected(num_nodes: int, edge_index: torch.Tensor) -> List[Set[int]]:
    adj = [set() for _ in range(num_nodes)]
    src = edge_index[0].detach().cpu().tolist()
    dst = edge_index[1].detach().cpu().tolist()
    for u, v in zip(src, dst):
        if u == v:
            continue
        adj[u].add(v)
        adj[v].add(u)
    return adj


# -----------------------------
# Model outputs -> probs/risk
# -----------------------------
@torch.no_grad()
def predict_node_probs(model, data, device: str) -> torch.Tensor:
    """
    binary head만 사용한 노드 확률.
    """
    model.eval()
    d = data.to(device)
    out = model(d)

    if isinstance(out, dict):
        if "bin_logits" in out:
            p = torch.sigmoid(out["bin_logits"])
        elif "logits" in out:
            p = torch.sigmoid(out["logits"])
        else:
            raise KeyError("Model output dict must contain 'bin_logits' or 'logits'.")
    else:
        # 모델이 tensor 직접 반환하는 경우
        p = torch.sigmoid(out)

    return p.detach().cpu()


@torch.no_grad()
def predict_node_risk(model, data, device: str) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    risk = sqrt( p_bin * p_non_normal )
    - p_non_normal = 1 - softmax(type_logits)[normal_class=0]
    - type head 없으면 p_non_normal = 1
    """
    model.eval()
    d = data.to(device)
    out = model(d)

    if isinstance(out, dict):
        if "bin_logits" in out:
            p_bin = torch.sigmoid(out["bin_logits"]).detach().cpu()
        elif "logits" in out:
            p_bin = torch.sigmoid(out["logits"]).detach().cpu()
        else:
            raise KeyError("Model output dict must contain 'bin_logits' or 'logits'.")

        if "type_logits" in out:
            p_type = torch.softmax(out["type_logits"], dim=-1).detach().cpu()
            if p_type.size(1) >= 1:
                p_non_normal = 1.0 - p_type[:, 0]
            else:
                p_non_normal = torch.ones_like(p_bin)
        else:
            p_non_normal = torch.ones_like(p_bin)
    else:
        p_bin = torch.sigmoid(out).detach().cpu()
        p_non_normal = torch.ones_like(p_bin)

    risk = torch.sqrt(torch.clamp(p_bin * p_non_normal, min=1e-8, max=1.0))
    return risk, p_bin, p_non_normal


# -----------------------------
# Gate selection (hysteresis)
# -----------------------------
def select_gates_hysteresis(
    data,
    risk: torch.Tensor,
    seed_thr: float = 0.62,
    grow_thr: float = 0.34,
    max_comp_ratio: float = 0.10,
    singleton_seed_thr: float = 0.88,
    local_quantile: float = 0.40,
    force_one_seed_if_empty: bool = True,
) -> List[str]:
    """
    1) seed / grow 이중 임계값으로 후보 생성
    2) undirected connected component 필터링
    3) component 내부 2차 정제로 과다 검출 억제
    """
    n = int(data.num_nodes)
    valid = get_valid_mask(data)
    names = get_node_names(data)
    rv = risk[valid]

    if rv.numel() == 0:
        return []

    # ---- adaptive threshold (중요: 너무 빡빡하게 안 가도록 '완화 가능'하게)
    if rv.numel() >= 50:
        q99 = float(torch.quantile(rv, 0.99).item())
        q95 = float(torch.quantile(rv, 0.95).item())
        seed_eff = float(np.clip(min(seed_thr, q99), 0.35, 0.92))
        grow_eff = float(np.clip(min(grow_thr, q95), 0.20, max(0.20, seed_eff - 0.05)))
    else:
        vmax = float(rv.max().item())
        seed_eff = float(np.clip(min(seed_thr, vmax), 0.30, 0.92))
        grow_eff = float(np.clip(min(grow_thr, seed_eff - 0.05), 0.20, 0.85))

    seed = (risk >= seed_eff) & valid
    cand = (risk >= grow_eff) & valid

    # seed가 없으면 최고 risk 1개로 seed 보강
    if force_one_seed_if_empty and int(seed.sum().item()) == 0 and int(cand.sum().item()) > 0:
        valid_idx = torch.where(valid)[0]
        best_i = int(valid_idx[torch.argmax(risk[valid_idx])].item())
        seed[best_i] = True
        cand[best_i] = True

    if int(cand.sum().item()) == 0:
        return []

    adj = build_adj_undirected(n, data.edge_index)
    cand_np = cand.detach().cpu().numpy().astype(bool)
    seed_set = set(torch.where(seed)[0].detach().cpu().tolist())

    visited = [False] * n
    keep = set()
    max_comp_size = max(12, int(max_comp_ratio * n))

    for i in range(n):
        if not cand_np[i] or visited[i]:
            continue

        st = [i]
        visited[i] = True
        comp = []
        while st:
            u = st.pop()
            comp.append(u)
            for w in adj[u]:
                if cand_np[w] and not visited[w]:
                    visited[w] = True
                    st.append(w)

        csize = len(comp)
        has_seed = any(u in seed_set for u in comp)

        # 단일 노드 component
        if csize == 1:
            u = comp[0]
            if (risk[u].item() >= singleton_seed_thr) or (u in seed_set):
                keep.add(u)
            continue

        # 너무 큰 component 제거 (FP 폭증 방지)
        if csize > max_comp_size:
            continue

        if has_seed:
            keep.update(comp)

    if len(keep) == 0:
        return []

    keep_idx = torch.tensor(sorted(list(keep)), dtype=torch.long)
    local = risk[keep_idx]
    local_thr = max(grow_eff + 0.03, float(torch.quantile(local, local_quantile).item()))
    final_idx = [int(u) for u in keep if risk[u].item() >= local_thr]

    # 그래도 비면 seed 유지
    if len(final_idx) == 0:
        final_idx = [int(u) for u in keep if u in seed_set]

    final_idx = sorted(final_idx, key=lambda u: float(risk[u].item()), reverse=True)
    return [names[u] for u in final_idx]


def select_trojan_gates(
    data,
    probs: torch.Tensor,
    node_thr: float,
    **kwargs,
) -> List[str]:
    """
    호환용 wrapper.
    """
    grow = max(0.20, float(node_thr) - 0.28)
    return select_gates_hysteresis(
        data=data,
        risk=probs,
        seed_thr=float(node_thr),
        grow_thr=grow,
        max_comp_ratio=kwargs.get("max_comp_ratio", 0.10),
        singleton_seed_thr=kwargs.get("singleton_seed_thr", 0.88),
        local_quantile=kwargs.get("local_quantile", 0.40),
        force_one_seed_if_empty=kwargs.get("force_one_seed_if_empty", True),
    )


# -----------------------------
# Threshold tuning
# -----------------------------
@torch.no_grad()
def tune_postprocess_thresholds(
    model,
    val_data: List,
    device: str,
    node_thr_grid=None,   # seed threshold grid
    graph_thr_grid=None,
):
    """
    작은 val 셋에서도 빈예측 붕괴를 줄이도록 objective 구성.
    """
    if val_data is None or len(val_data) == 0:
        return {
            "node_thr": 0.62,
            "graph_thr": 0.30,
            "graph_f1": 0.0,
            "gate_precision": 0.0,
            "gate_recall": 0.0,
            "gate_f1": 0.0,
            "avg_pred_ratio": 0.0,
            "empty_rate": 1.0,
            "obj": -1.0,
        }

    if node_thr_grid is None:
        node_thr_grid = np.linspace(0.35, 0.80, 19)
    if graph_thr_grid is None:
        graph_thr_grid = np.linspace(0.20, 0.85, 27)

    # precompute
    cache = []
    for d in val_data:
        risk, p_bin, p_non_normal = predict_node_risk(model, d, device)
        valid = get_valid_mask(d)
        score = graph_score_from_probs(risk, valid, q=0.995)

        if hasattr(d, "y_bin"):
            yb = d.y_bin.detach().cpu()
            idx = torch.where((yb == 1) & valid)[0].tolist()
            gt_set = set(get_node_names(d)[i] for i in idx)
        else:
            gt_set = set()

        if hasattr(d, "graph_y"):
            true_graph = int(d.graph_y.item())
        else:
            true_graph = 1 if len(gt_set) > 0 else 0

        cache.append({
            "data": d,
            "risk": risk,
            "score": score,
            "gt_set": gt_set,
            "true_graph": true_graph,
            "num_valid": int(valid.sum().item()),
        })

    best = None
    fallback = None

    for nthr in node_thr_grid:
        grow_local = max(0.20, float(nthr) - 0.28)

        pred_gates_all = []
        scores = []
        y_true_graph = []
        pred_ratio_all = []

        for c in cache:
            gates = select_gates_hysteresis(
                data=c["data"],
                risk=c["risk"],
                seed_thr=float(nthr),
                grow_thr=grow_local,
                max_comp_ratio=0.10,
                singleton_seed_thr=0.88,
                local_quantile=0.40,
                force_one_seed_if_empty=True,
            )
            pred_gates_all.append(gates)
            scores.append(c["score"])
            y_true_graph.append(c["true_graph"])
            pred_ratio_all.append(len(gates) / max(c["num_valid"], 1))

        for gthr in graph_thr_grid:
            y_pred_graph = [1 if s >= float(gthr) else 0 for s in scores]

            # graph f1
            tp = sum(1 for t, p in zip(y_true_graph, y_pred_graph) if t == 1 and p == 1)
            fp = sum(1 for t, p in zip(y_true_graph, y_pred_graph) if t == 0 and p == 1)
            fn = sum(1 for t, p in zip(y_true_graph, y_pred_graph) if t == 1 and p == 0)
            gp = tp / (tp + fp + 1e-12)
            gr = tp / (tp + fn + 1e-12)
            graph_f1 = 2 * gp * gr / (gp + gr + 1e-12)

            # gate metrics: trojan graph만 대상으로
            gate_ps, gate_rs, gate_f1s = [], [], []
            empty_on_true_trojan = []

            for i, c in enumerate(cache):
                if c["true_graph"] != 1:
                    continue
                if len(c["gt_set"]) == 0:
                    # GT gate 라벨이 없는 trojan graph는 gate metric에서 제외
                    continue

                pred_set = set(pred_gates_all[i]) if y_pred_graph[i] == 1 else set()
                m = gate_prf(pred_set, c["gt_set"])
                gate_ps.append(m["p"])
                gate_rs.append(m["r"])
                gate_f1s.append(m["f1"])
                empty_on_true_trojan.append(1 if len(pred_set) == 0 else 0)

            mean_gp = float(np.mean(gate_ps)) if gate_ps else 0.0
            mean_gr = float(np.mean(gate_rs)) if gate_rs else 0.0
            mean_gf1 = float(np.mean(gate_f1s)) if gate_f1s else 0.0
            empty_rate = float(np.mean(empty_on_true_trojan)) if empty_on_true_trojan else 1.0
            mean_ratio = float(np.mean(pred_ratio_all)) if pred_ratio_all else 0.0

            # 과다 예측 패널티
            over_pred = max(0.0, mean_ratio - 0.20)

            # objective
            obj = (
                0.55 * mean_gf1
                + 0.20 * mean_gr
                + 0.15 * graph_f1
                + 0.10 * mean_gp
                - 0.30 * empty_rate
                - 0.20 * over_pred
            )

            cand = {
                "node_thr": float(nthr),
                "graph_thr": float(gthr),
                "graph_f1": float(graph_f1),
                "gate_precision": mean_gp,
                "gate_recall": mean_gr,
                "gate_f1": mean_gf1,
                "avg_pred_ratio": mean_ratio,
                "empty_rate": empty_rate,
                "obj": float(obj),
            }

            if (fallback is None) or (cand["obj"] > fallback["obj"]):
                fallback = cand

            # 최소 제약
            if (mean_gr >= 0.03) and (mean_ratio <= 0.25):
                if (best is None) or (cand["obj"] > best["obj"]):
                    best = cand

    return best if best is not None else fallback


# -----------------------------
# Output writer
# -----------------------------
def write_case_output(path: str, is_trojan: bool, gates: List[str]):
    lines = []
    if not is_trojan:
        lines.append("NO_TROJAN")
    else:
        lines.append("TROJANED")
        lines.append("TROJAN_GATES")
        for g in gates:
            lines.append(g)
        lines.append("END_TROJAN_GATES")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")