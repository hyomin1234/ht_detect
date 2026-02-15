# auto_features.py
from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import networkx as nx
import torch


def _build_adj(edge_index: torch.Tensor, n: int):
    preds = [[] for _ in range(n)]
    succs = [[] for _ in range(n)]
    if edge_index.numel() == 0:
        return preds, succs
    src = edge_index[0].tolist()
    dst = edge_index[1].tolist()
    for u, v in zip(src, dst):
        preds[v].append(u)
        succs[u].append(v)
    return preds, succs


def _id2name_from_vocab(gate_vocab: Dict[str, int]) -> Dict[int, str]:
    return {v: k for k, v in gate_vocab.items()}


def _depth_from_sources(n: int, edge_index: torch.Tensor, source_mask: torch.Tensor) -> torch.Tensor:
    g = nx.DiGraph()
    g.add_nodes_from(range(n))
    if edge_index.numel() > 0:
        g.add_edges_from(zip(edge_index[0].tolist(), edge_index[1].tolist()))

    dag = nx.condensation(g)  # SCC DAG
    mapping = dag.graph["mapping"]  # node -> comp

    NEG = -10**9
    comp_depth = {c: NEG for c in dag.nodes()}
    src_nodes = torch.where(source_mask)[0].tolist()
    if not src_nodes:
        src_nodes = [i for i in range(n) if g.in_degree(i) == 0]
        if not src_nodes:
            src_nodes = list(range(n))

    for s in src_nodes:
        comp_depth[mapping[s]] = max(comp_depth[mapping[s]], 0)

    for c in nx.topological_sort(dag):
        if comp_depth[c] == NEG:
            comp_depth[c] = 0
        for nxt in dag.successors(c):
            comp_depth[nxt] = max(comp_depth[nxt], comp_depth[c] + 1)

    d = torch.zeros(n, dtype=torch.float32)
    for i in range(n):
        d[i] = float(comp_depth[mapping[i]])
    return d


def _xor_cc_pair(cc0a: float, cc1a: float, cc0b: float, cc1b: float) -> Tuple[float, float]:
    cc0 = min(cc0a + cc0b, cc1a + cc1b) + 1.0
    cc1 = min(cc0a + cc1b, cc1a + cc0b) + 1.0
    return cc0, cc1


def _gate_cc(g: str, cc0_ins: List[float], cc1_ins: List[float]) -> Tuple[float, float]:
    if len(cc0_ins) == 0:
        return 1.0, 1.0

    if g == "PI":
        return 1.0, 1.0
    if g in ("BUF",):
        return cc0_ins[0] + 1.0, cc1_ins[0] + 1.0
    if g in ("NOT",):
        return cc1_ins[0] + 1.0, cc0_ins[0] + 1.0
    if g == "DFF":
        # 순차소자 근사: D->Q 전달 기반
        return cc0_ins[0] + 1.0, cc1_ins[0] + 1.0

    if g == "AND":
        cc0 = min(cc0_ins) + 1.0
        cc1 = sum(cc1_ins) + 1.0
        return cc0, cc1
    if g == "NAND":
        a0, a1 = _gate_cc("AND", cc0_ins, cc1_ins)
        return a1, a0
    if g == "OR":
        cc0 = sum(cc0_ins) + 1.0
        cc1 = min(cc1_ins) + 1.0
        return cc0, cc1
    if g == "NOR":
        o0, o1 = _gate_cc("OR", cc0_ins, cc1_ins)
        return o1, o0

    if g == "XOR":
        c0, c1 = cc0_ins[0], cc1_ins[0]
        for i in range(1, len(cc0_ins)):
            c0, c1 = _xor_cc_pair(c0, c1, cc0_ins[i], cc1_ins[i])
        return c0, c1
    if g == "XNOR":
        x0, x1 = _gate_cc("XOR", cc0_ins, cc1_ins)
        return x1, x0

    if g == "MUX":
        # 포트 정보 완전하지 않은 구조파서 가정에서 보수적 근사
        cc0 = min(cc0_ins) + 2.0
        cc1 = min(cc1_ins) + 2.0
        return cc0, cc1

    # OTHER fallback
    return min(cc0_ins) + 1.0, min(cc1_ins) + 1.0


def _gate_co_input_cost(
    g: str,
    input_idx: int,
    cc0_ins: List[float],
    cc1_ins: List[float],
    co_out: float
) -> float:
    n = len(cc0_ins)
    if n == 0:
        return co_out + 1.0

    if g in ("PI",):
        return co_out + 1.0
    if g in ("BUF", "NOT", "DFF"):
        return co_out + 1.0

    if g in ("AND", "NAND"):
        others = [cc1_ins[j] for j in range(n) if j != input_idx]
        return co_out + sum(others) + 1.0

    if g in ("OR", "NOR"):
        others = [cc0_ins[j] for j in range(n) if j != input_idx]
        return co_out + sum(others) + 1.0

    if g in ("XOR", "XNOR"):
        # 다른 입력들을 '구분 가능'하게 만드는 최소 비용 근사
        others = [min(cc0_ins[j], cc1_ins[j]) for j in range(n) if j != input_idx]
        return co_out + sum(others) + 1.0

    if g == "MUX":
        return co_out + 2.0

    return co_out + 1.0


def _gate_p1(g: str, p_ins: List[float]) -> float:
    if len(p_ins) == 0:
        return 0.5

    if g == "PI":
        return p_ins[0] if len(p_ins) > 0 else 0.5
    if g == "BUF":
        return p_ins[0]
    if g == "NOT":
        return 1.0 - p_ins[0]
    if g == "DFF":
        return p_ins[0]

    if g == "AND":
        p = 1.0
        for q in p_ins:
            p *= q
        return p
    if g == "NAND":
        p = 1.0
        for q in p_ins:
            p *= q
        return 1.0 - p
    if g == "OR":
        p0 = 1.0
        for q in p_ins:
            p0 *= (1.0 - q)
        return 1.0 - p0
    if g == "NOR":
        p0 = 1.0
        for q in p_ins:
            p0 *= (1.0 - q)
        return p0
    if g == "XOR":
        p = 0.0
        for q in p_ins:
            p = p * (1.0 - q) + (1.0 - p) * q
        return p
    if g == "XNOR":
        p = 0.0
        for q in p_ins:
            p = p * (1.0 - q) + (1.0 - p) * q
        return 1.0 - p
    if g == "MUX":
        # (d0,d1,s) 근사. 없으면 평균.
        if len(p_ins) >= 3:
            d0, d1, s = p_ins[0], p_ins[1], p_ins[2]
            return (1.0 - s) * d0 + s * d1
        return sum(p_ins) / len(p_ins)

    return sum(p_ins) / len(p_ins)


def compute_scoap_activity(
    data,
    gate_vocab: Dict[str, int],
    pi_prob: float = 0.5,
    cc_iter: int = 4,
    co_iter: int = 4,
    p_iter: int = 4,
):
    """
    returns:
      cc0, cc1, co, activity, depth   (all torch.float [N])
    요구 데이터 필드:
      data.edge_index, data.gate_type_id
    """
    gate_id = data.gate_type_id.long()
    n = int(gate_id.numel())
    edge_index = data.edge_index

    id2name = _id2name_from_vocab(gate_vocab)
    gname = [id2name.get(int(gate_id[i]), "OTHER") for i in range(n)]

    preds, succs = _build_adj(edge_index, n)

    pi_id = gate_vocab.get("PI", -999)
    source_mask = (gate_id == pi_id) | torch.tensor([x == "DFF" for x in gname], dtype=torch.bool)
    depth = _depth_from_sources(n, edge_index, source_mask)

    order = torch.argsort(depth).tolist()
    rev_order = list(reversed(order))

    # ----- CC0 / CC1 -----
    cc0 = torch.full((n,), 5.0, dtype=torch.float32)
    cc1 = torch.full((n,), 5.0, dtype=torch.float32)

    for i in range(n):
        if gname[i] == "PI":
            cc0[i] = 1.0
            cc1[i] = 1.0

    for _ in range(cc_iter):
        for v in order:
            g = gname[v]
            if g == "PI":
                continue
            ins = preds[v]
            if len(ins) == 0:
                cc0[v], cc1[v] = 1.0, 1.0
                continue
            c0_in = [float(cc0[u].item()) for u in ins]
            c1_in = [float(cc1[u].item()) for u in ins]
            c0, c1 = _gate_cc(g, c0_in, c1_in)
            cc0[v] = c0
            cc1[v] = c1

    # ----- CO -----
    INF = 1e9
    co = torch.full((n,), INF, dtype=torch.float32)

    po_nodes = [i for i in range(n) if len(succs[i]) == 0]
    if not po_nodes:
        po_nodes = [order[-1]] if order else [0]
    for i in po_nodes:
        co[i] = 0.0

    for _ in range(co_iter):
        for v in rev_order:
            if co[v] >= INF / 2:
                continue
            ins = preds[v]
            if len(ins) == 0:
                continue
            g = gname[v]
            c0_in = [float(cc0[u].item()) for u in ins]
            c1_in = [float(cc1[u].item()) for u in ins]
            co_out = float(co[v].item())

            for k, u in enumerate(ins):
                cand = _gate_co_input_cost(g, k, c0_in, c1_in, co_out)
                if cand < co[u]:
                    co[u] = cand

    finite = co[co < INF / 2]
    fill_val = float(finite.max().item() + 5.0) if finite.numel() > 0 else 10.0
    co[co >= INF / 2] = fill_val

    # ----- Switching Activity -----
    p1 = torch.full((n,), 0.5, dtype=torch.float32)
    for i in range(n):
        if gname[i] == "PI":
            p1[i] = float(pi_prob)

    for _ in range(p_iter):
        for v in order:
            g = gname[v]
            if g == "PI":
                continue
            ins = preds[v]
            if len(ins) == 0:
                p1[v] = 0.5
                continue
            pin = [float(p1[u].item()) for u in ins]
            pv = _gate_p1(g, pin)
            p1[v] = max(0.0, min(1.0, pv))

    activity = 2.0 * p1 * (1.0 - p1)

    return cc0, cc1, co, activity, depth


def attach_auto_features(
    data,
    gate_vocab: Dict[str, int],
    overwrite: bool = False,
    pi_prob: float = 0.5,
):
    """
    data.num_feat[:, 0:5] = [CC0, CC1, CO, SW, depth]
    """
    cc0, cc1, co, sw, depth = compute_scoap_activity(
        data=data,
        gate_vocab=gate_vocab,
        pi_prob=pi_prob,
    )

    n = cc0.numel()
    if not hasattr(data, "num_feat") or data.num_feat is None or data.num_feat.numel() == 0:
        data.num_feat = torch.zeros((n, 5), dtype=torch.float32)

    if data.num_feat.size(1) < 5:
        pad = torch.zeros((n, 5 - data.num_feat.size(1)), dtype=torch.float32, device=data.num_feat.device)
        data.num_feat = torch.cat([data.num_feat, pad], dim=1)

    if overwrite:
        data.num_feat[:, 0] = cc0
        data.num_feat[:, 1] = cc1
        data.num_feat[:, 2] = co
        data.num_feat[:, 3] = sw
        data.num_feat[:, 4] = depth
    else:
        # 값이 0인 곳만 자동 채움
        for k, t in enumerate([cc0, cc1, co, sw, depth]):
            cur = data.num_feat[:, k]
            fill = (cur == 0)
            cur[fill] = t[fill]
            data.num_feat[:, k] = cur

    # optional cache
    data.cc0 = cc0
    data.cc1 = cc1
    data.co = co
    data.sw = sw
    data.depth = depth
    return data