from __future__ import annotations
import random
from pathlib import Path
import numpy as np
import torch

from netlist_to_pyg import build_pyg_from_netlist, GATE_VOCAB
from auto_features import attach_auto_features
from label_utils import attach_multitask_labels
from dataset_utils import find_contest_netlists, load_trojan_labels, get_node_type_map
from hybrid_trojan_multitask import HybridTrojanNetPyGMultiTask

from postprocess_utils import (
    predict_node_risk,
    get_valid_mask,
    get_node_names,
    select_gates_hysteresis,
)

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

def graph_split_indices(data_list, seed=42, train_ratio=0.7, val_ratio=0.15):
    random.seed(seed)
    pos = [i for i, d in enumerate(data_list) if int(d.graph_y.item()) == 1]
    neg = [i for i, d in enumerate(data_list) if int(d.graph_y.item()) == 0]
    random.shuffle(pos); random.shuffle(neg)

    def split(arr):
        n = len(arr)
        n_tr = int(n * train_ratio)
        n_va = int(n * val_ratio)
        tr = arr[:n_tr]
        va = arr[n_tr:n_tr+n_va]
        te = arr[n_tr+n_va:]
        return tr, va, te

    p_tr, p_va, p_te = split(pos)
    n_tr, n_va, n_te = split(neg)
    tr = p_tr + n_tr; va = p_va + n_va; te = p_te + n_te
    random.shuffle(tr); random.shuffle(va); random.shuffle(te)
    return tr, va, te

def risk_stats(risk, valid):
    v = risk[valid]
    if v.numel() == 0:
        return {"q99":0.0, "q995":0.0, "vmax":0.0, "spike":0.0}
    vmax = float(v.max().item())
    q99 = float(torch.quantile(v, 0.99).item()) if v.numel() >= 50 else vmax
    q995 = float(torch.quantile(v, 0.995).item()) if v.numel() >= 50 else vmax
    spike = vmax / (q99 + 1e-6)
    return {"q99":q99, "q995":q995, "vmax":vmax, "spike":spike}

def load_all(data_root, device):
    paths = sorted(find_contest_netlists(data_root), key=lambda p: p.name)
    data_list = []
    for p in paths:
        d = build_pyg_from_netlist(p, top_module=None)
        d = attach_auto_features(d, gate_vocab=GATE_VOCAB)
        tg = load_trojan_labels(p) or []
        d = attach_multitask_labels(d, node_to_type=get_node_type_map(tg), assume_unlisted_normal=True)
        d.graph_y = torch.tensor([1 if len(tg)>0 else 0], dtype=torch.long)
        d.num_nodes = int(d.gate_type_id.numel())
        d.case_name = p.stem
        data_list.append(d)
    return data_list

def build_model(sample, model_path, device):
    model = HybridTrojanNetPyGMultiTask(
        num_gate_types=len(GATE_VOCAB),
        num_types=5,
        num_num_feat=sample.num_feat.size(1),
        edge_dim=sample.edge_attr.size(1) if sample.edge_attr.numel() > 0 else 3,
        hidden_dim=96,
        heads=4,
        dropout=0.15,
    ).to(device)
    state = torch.load(model_path, map_location=device)
    model.load_state_dict(state, strict=True)
    model.eval()
    return model

def main():
    set_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    DATA_ROOT = "C:/HT_detect/00_contest/testcase_release_all/release_all(20250728)"
    MODEL_PATH = "results/model_best.pt"

    TARGET_COUNTS = {
        "design16": 2002,
        "design11": 42,
        "design0": 71,
    }
    EXPECT_CLEAN = {"design23": 0, "design28": 0}

    data_list = load_all(DATA_ROOT, device)
    tr_idx, va_idx, te_idx = graph_split_indices(data_list, seed=42)
    test_data = [data_list[i] for i in te_idx]

    model = build_model(data_list[0], MODEL_PATH, device)

    # test 캐시
    cache = {}
    for d in test_data:
        risk, _, _ = predict_node_risk(model, d, device)
        valid = get_valid_mask(d)
        cache[d.case_name] = {
            "data": d, "risk": risk, "valid": valid, "stats": risk_stats(risk, valid)
        }

    # 그리드 (dense용)
    seed_grid = [0.34, 0.38, 0.42, 0.46]
    grow_grid = [0.06, 0.08, 0.10, 0.12]
    comp_grid = [0.70, 0.80, 0.90, 0.95]
    lq_grid   = [0.10, 0.14, 0.18, 0.22]

    # sparse용 고정
    sparse_cfg = dict(
        seed_thr=0.62, grow_thr=0.26, max_comp_ratio=0.05,
        singleton_seed_thr=0.92, local_quantile=0.86,
        force_one_seed_if_empty=False
    )

    best = None
    rows = []

    for seed_thr in seed_grid:
        for grow_thr in grow_grid:
            for mcr in comp_grid:
                for lq in lq_grid:
                    pred_counts = {}

                    for case, c in cache.items():
                        d, risk, s = c["data"], c["risk"], c["stats"]
                        # dense/sparse 분기
                        dense_alarm = s["q99"] >= 0.20
                        sparse_alarm = (s["vmax"] >= 0.62) and (s["spike"] >= 12.0)

                        if not (dense_alarm or sparse_alarm):
                            gates = []
                        elif dense_alarm:
                            gates = select_gates_hysteresis(
                                data=d, risk=risk,
                                seed_thr=seed_thr, grow_thr=grow_thr,
                                max_comp_ratio=mcr, singleton_seed_thr=0.82,
                                local_quantile=lq, force_one_seed_if_empty=False
                            )
                        else:
                            gates = select_gates_hysteresis(
                                data=d, risk=risk, **sparse_cfg
                            )

                        pred_counts[case] = len(gates)

                    # 목적함수: 목표 count 근접 + clean 0 유지
                    err = 0.0
                    for k, t in TARGET_COUNTS.items():
                        if k in pred_counts:
                            err += abs(pred_counts[k] - t) / max(t, 1)

                    clean_pen = 0.0
                    for k, t in EXPECT_CLEAN.items():
                        if k in pred_counts:
                            clean_pen += max(0, pred_counts[k] - t)

                    obj = err + 0.01 * clean_pen

                    row = {
                        "obj": obj,
                        "seed_thr": seed_thr,
                        "grow_thr": grow_thr,
                        "max_comp_ratio": mcr,
                        "local_quantile": lq,
                        "pred": pred_counts
                    }
                    rows.append(row)

                    if (best is None) or (obj < best["obj"]):
                        best = row

    rows = sorted(rows, key=lambda x: x["obj"])
    print("\n=== Top 10 configs ===")
    for r in rows[:10]:
        print(
            f"obj={r['obj']:.4f} "
            f"seed={r['seed_thr']:.2f} grow={r['grow_thr']:.2f} "
            f"mcr={r['max_comp_ratio']:.2f} lq={r['local_quantile']:.2f} "
            f"pred={r['pred']}"
        )

    print("\n=== Best ===")
    print(best)

if __name__ == "__main__":
    main()  