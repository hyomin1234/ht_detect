from __future__ import annotations
import os
import json
import random
from pathlib import Path
from typing import List, Tuple

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
    graph_score_from_probs,
    select_gates_hysteresis,
    tune_postprocess_thresholds,
    write_case_output,
    get_node_names,
)

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def graph_split_indices(data_list, seed=42, train_ratio=0.7, val_ratio=0.15):
    """
    graph-level stratified split (trojan/clean 비율 유지)
    """
    random.seed(seed)
    pos = [i for i, d in enumerate(data_list) if int(d.graph_y.item()) == 1]
    neg = [i for i, d in enumerate(data_list) if int(d.graph_y.item()) == 0]
    random.shuffle(pos)
    random.shuffle(neg)

    def split(arr):
        n = len(arr)
        n_tr = int(n * train_ratio)
        n_va = int(n * val_ratio)
        n_te = n - n_tr - n_va
        if n >= 3 and n_te <= 0:
            n_te = 1
            if n_va > 1:
                n_va -= 1
            elif n_tr > 1:
                n_tr -= 1
        tr = arr[:n_tr]
        va = arr[n_tr:n_tr + n_va]
        te = arr[n_tr + n_va:]
        return tr, va, te

    p_tr, p_va, p_te = split(pos)
    n_tr, n_va, n_te = split(neg)

    tr = p_tr + n_tr
    va = p_va + n_va
    te = p_te + n_te

    random.shuffle(tr)
    random.shuffle(va)
    random.shuffle(te)
    return tr, va, te


def build_dataset(DATA_ROOTS: List[str]):
    all_paths = []
    for root in DATA_ROOTS:
        all_paths.extend(find_contest_netlists(root))

    uniq = {}
    for p in all_paths:
        uniq[str(Path(p).resolve())] = Path(p)
    netlists = sorted(list(uniq.values()), key=lambda x: x.name)

    print(f"Found {len(netlists)} netlists.")

    data_list = []
    bad = 0

    for path in netlists:
        try:
            data = build_pyg_from_netlist(netlist_path=path, top_module=None)
            data = attach_auto_features(data, gate_vocab=GATE_VOCAB)

            trojan_gates = load_trojan_labels(path)
            if trojan_gates is None:
                trojan_gates = []

            node_map = get_node_type_map(trojan_gates)
            data = attach_multitask_labels(
                data,
                node_to_type=node_map,
                assume_unlisted_normal=True
            )

            data.graph_y = torch.tensor([1 if len(trojan_gates) > 0 else 0], dtype=torch.long)
            data.num_nodes = int(data.gate_type_id.numel())
            data.case_name = path.stem

            data_list.append(data)
        except Exception as e:
            bad += 1
            print(f"[WARN] skip {path.name}: {e}")

    if bad > 0:
        print(f"[INFO] skipped {bad} netlists due to parsing/feature errors")

    return netlists, data_list


def make_model_from_sample(sample, device: str):
    model = HybridTrojanNetPyGMultiTask(
        num_gate_types=len(GATE_VOCAB),
        num_types=5,
        num_num_feat=sample.num_feat.size(1),
        edge_dim=sample.edge_attr.size(1) if sample.edge_attr.numel() > 0 else 3,
        hidden_dim=96,
        heads=4,
        dropout=0.15,
    ).to(device)
    return model


def infer_one_case(model, d, device: str, best_pp: dict, rules: dict):
    risk, p_bin, p_non_normal = predict_node_risk(model, d, device)
    valid = get_valid_mask(d)
    s = risk_stats(risk, valid)

    # ---- 분기 기준(보수적으로 하드코딩 floor 적용) ----
    dense_q99_thr = max(0.20, rules.get("dense_q99_thr", 0.20))
    peak_thr = max(0.62, rules.get("peak_thr", 0.62))
    spike_thr = max(12.0, rules.get("spike_thr", 12.0))

    dense_alarm = (s["q99"] >= dense_q99_thr)
    sparse_alarm = (s["vmax"] >= peak_thr) and (s["spike"] >= spike_thr)

    if not (dense_alarm or sparse_alarm):
        return False, [], s, risk, p_bin, p_non_normal

    # ---- dense / sparse 완전 분리 ----
    if dense_alarm:
        # design16/0 같은 대형 군집형 트로이용 (강하게 완화)
        gates = select_gates_hysteresis(
            data=d,
            risk=risk,
            seed_thr=0.42,          # 낮춤
            grow_thr=0.12,          # 많이 낮춤
            max_comp_ratio=0.90,    # 0.06 -> 0.90 (핵심)
            singleton_seed_thr=0.82,
            local_quantile=0.18,    # 0.7대 -> 0.18 (핵심)
            force_one_seed_if_empty=False,
        )

        # 1차가 너무 적으면 fallback 1회 더 완화
        if len(gates) < 20:
            gates = select_gates_hysteresis(
                data=d,
                risk=risk,
                seed_thr=0.36,
                grow_thr=0.08,
                max_comp_ratio=0.95,
                singleton_seed_thr=0.80,
                local_quantile=0.10,
                force_one_seed_if_empty=False,
            )

        # dense는 최소 개수 조건으로 FP 억제
        is_trojan = (len(gates) >= 15)

    else:
        # design11 같은 sparse trigger용 (엄격 유지)
        gates = select_gates_hysteresis(
            data=d,
            risk=risk,
            seed_thr=0.62,
            grow_thr=0.26,
            max_comp_ratio=0.05,
            singleton_seed_thr=0.92,
            local_quantile=0.86,
            force_one_seed_if_empty=False,
        )
        is_trojan = (len(gates) >= 1)

    if not is_trojan:
        gates = []

    return is_trojan, gates, s, risk, p_bin, p_non_normal

def risk_stats(risk: torch.Tensor, valid: torch.Tensor):
    v = risk[valid]
    if v.numel() == 0:
        return {"q995": 0.0, "q99": 0.0, "vmax": 0.0, "spike": 0.0}
    vmax = float(v.max().item())
    if v.numel() >= 50:
        q995 = float(torch.quantile(v, 0.995).item())
        q99 = float(torch.quantile(v, 0.99).item())
    else:
        q995 = vmax
        q99 = float(torch.quantile(v, 0.90).item()) if v.numel() >= 10 else vmax
    spike = vmax / (q99 + 1e-6)
    return {"q995": q995, "q99": q99, "vmax": vmax, "spike": spike}


@torch.no_grad()
def calibrate_graph_rules(model, calib_data, device, best_pp):
    """
    clean 그래프 분포로 graph 판정 규칙 자동 보정
    """
    clean_q995, clean_vmax, clean_spike = [], [], []

    for d in calib_data:
        risk, _, _ = predict_node_risk(model, d, device)
        valid = get_valid_mask(d)
        s = risk_stats(risk, valid)
        gy = int(d.graph_y.item()) if hasattr(d, "graph_y") else 0
        if gy == 0:
            clean_q995.append(s["q995"])
            clean_vmax.append(s["vmax"])
            clean_spike.append(s["spike"])

    # clean 샘플이 너무 적을 때 fallback
    if len(clean_q995) == 0:
        return {
            "mass_thr": max(0.30, float(best_pp["graph_thr"])),
            "peak_thr": 0.65,
            "spike_thr": 6.0,
        }

    mass_thr = max(
        0.30,
        float(best_pp["graph_thr"]),
        float(np.quantile(clean_q995, 0.95) + 0.03),
    )
    peak_thr = max(
        0.60,
        float(np.quantile(clean_vmax, 0.99) + 0.02),
    )
    spike_thr = max(
        5.0,
        float(np.quantile(clean_spike, 0.99) + 0.5),
    )

    return {
        "mass_thr": mass_thr,   # 밀집형 트로이 검출용
        "peak_thr": peak_thr,   # 희소형 최대값 기준
        "spike_thr": spike_thr  # vmax/q99 비율 기준
    }

def graph_decision_from_stats(s: dict, rules: dict):
    # Dense trojan: tail mass가 충분히 높음
    dense_alarm = (s["q99"] >= rules["dense_q99_thr"])
    # Sparse trigger trojan: 높은 peak + 큰 spike ratio
    sparse_alarm = (s["vmax"] >= rules["peak_thr"]) and (s["spike"] >= rules["spike_thr"])
    return dense_alarm, sparse_alarm, (dense_alarm or sparse_alarm)

def robust_graph_score(risk: torch.Tensor, valid: torch.Tensor) -> float:
    v = risk[valid]
    if v.numel() == 0:
        return 0.0
    vmax = float(v.max().item())
    if v.numel() < 50:
        return vmax
    q995 = float(torch.quantile(v, 0.995).item())
    k = max(1, int(0.002 * v.numel()))  # 상위 0.2%
    topk_mean = float(torch.topk(v, k).values.mean().item())
    # 희소 트리거 대응: q995 + peak/topk 혼합
    return max(q995, 0.55 * vmax, 0.90 * topk_mean)

def main():
    set_seed(42)

    # ----------------------------
    # Config
    # ----------------------------
    DATA_ROOTS: List[str] = [
        "C:/HT_detect/00_contest/testcase_release_all/release_all(20250728)",
    ]
    MODEL_PATH = "results/model_best.pt"
    OUT_DIR = "results/case_outputs"
    DEBUG_JSON = "results/postprocess_debug.json"

    # "test" | "val" | "all"
    INFER_SPLIT = "test"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # ----------------------------
    # 1) Data reconstruction
    # ----------------------------
    _, data_list = build_dataset(DATA_ROOTS)
    if len(data_list) == 0:
        print("No valid data. Exit.")
        return

    n_pos = sum(int(d.graph_y.item()) for d in data_list)
    n_neg = len(data_list) - n_pos
    print(f"Graph label distribution: trojan={n_pos}, clean={n_neg}")

    # ----------------------------
    # 2) Split restore
    # ----------------------------
    tr_idx, va_idx, te_idx = graph_split_indices(
        data_list, seed=42, train_ratio=0.7, val_ratio=0.15
    )
    train_data = [data_list[i] for i in tr_idx]
    val_data = [data_list[i] for i in va_idx]
    test_data = [data_list[i] for i in te_idx]
    print(f"Split: Train={len(train_data)}, Val={len(val_data)}, Test={len(test_data)}")

    if len(train_data) == 0:
        print("Train split empty. Exit.")
        return

    # ----------------------------
    # 3) Model load
    # ----------------------------
    model = make_model_from_sample(train_data[0], device)
    state = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state, strict=True)
    model.eval()
    print(f"Loaded model from: {MODEL_PATH}")

    # ----------------------------
    # 4) Tune thresholds on val
    # ----------------------------
    calib_data = train_data + val_data
    best_pp = tune_postprocess_thresholds(
        model=model,
        val_data=calib_data,   # <- 핵심
        device=device,
        node_thr_grid=np.linspace(0.40, 0.78, 16),
        graph_thr_grid=np.linspace(0.28, 0.75, 20),
    )
    rules = calibrate_graph_rules(model, calib_data, device, best_pp)
    print("Graph rules:", rules)
    print(best_pp)

    # 저장
    os.makedirs("results", exist_ok=True)
    with open("results/best_postprocess.json", "w", encoding="utf-8") as f:
        json.dump(best_pp, f, indent=2, ensure_ascii=False)

    # ----------------------------
    # 5) Choose inference set
    # ----------------------------
    if INFER_SPLIT == "test":
        infer_data = test_data
    elif INFER_SPLIT == "val":
        infer_data = val_data
    else:
        infer_data = data_list

    os.makedirs(OUT_DIR, exist_ok=True)

    # ----------------------------
    # 6) Inference & output
    # ----------------------------
    debug_rows = []

    for d in infer_data:
        is_trojan, gates, score, risk, p_bin, p_non_normal, s = infer_one_case(
            model=model,
            d=d,
            device=device,
            best_pp=best_pp,
            rules=rules
        )

        out_path = os.path.join(OUT_DIR, f"{d.case_name}.txt")
        write_case_output(out_path, bool(is_trojan), gates)

        valid = get_valid_mask(d)
        risk_max = float(risk[valid].max().item()) if int(valid.sum()) > 0 else 0.0
        risk_q99 = float(torch.quantile(risk[valid], 0.99).item()) if int(valid.sum()) >= 50 else -1.0

        print(
            f"{d.case_name}: q995={s['q995']:.4f}, vmax={s['vmax']:.4f}, spike={s['spike']:.2f}, "
            f"final_is_trojan={is_trojan}, final_gates={len(gates)}"
        )

        debug_rows.append({
            "case": d.case_name,
            "is_trojan": bool(is_trojan),
            "num_gates": int(len(gates)),
            "score": float(score),
            "risk_max": risk_max,
            "risk_q99": risk_q99,
            "graph_y": int(d.graph_y.item()) if hasattr(d, "graph_y") else None,
        })

    with open(DEBUG_JSON, "w", encoding="utf-8") as f:
        json.dump(debug_rows, f, indent=2, ensure_ascii=False)

    print(f"Done. outputs -> {OUT_DIR}")
    print(f"Saved best postprocess -> results/best_postprocess.json")
    print(f"Saved debug -> {DEBUG_JSON}")


if __name__ == "__main__":
    main()