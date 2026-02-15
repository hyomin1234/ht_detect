# run_full_pipeline.py
from __future__ import annotations
import os
import random
from pathlib import Path
from typing import List

import numpy as np
import torch
from torch_geometric.loader import DataLoader

from netlist_to_pyg import build_pyg_from_netlist, GATE_VOCAB
from auto_features import attach_auto_features
from label_utils import attach_multitask_labels
from hybrid_trojan_multitask import HybridTrojanNetPyGMultiTask, MultiTaskLoss
from dataset_utils import find_contest_netlists, load_trojan_labels, get_node_type_map
from splits_metrics import binary_metrics_from_logits, multiclass_macro_f1
from postprocess_utils import (
    predict_node_probs,
    predict_node_risk,
    get_valid_mask,
    graph_score_from_probs,
    select_trojan_gates,
    select_gates_hysteresis,
    tune_postprocess_thresholds,
    write_case_output,
)

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def graph_split_indices(data_list, seed=42, train_ratio=0.7, val_ratio=0.15):
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


def safe_trojan_gates(x):
    if x is None:
        return []
    if isinstance(x, (list, tuple, set)):
        return list(x)
    return []


def debug_label_coverage(data, trojan_gates, case_name: str):
    node_set = set(data.node_names)
    gt_set = set(trojan_gates)
    matched = node_set & gt_set

    if len(gt_set) > 0 and len(matched) == 0:
        print(f"[WARN] {case_name}: GT 게이트명과 node_names 매칭 0개")
        print(f"       sample_gt={list(gt_set)[:5]}")
        print(f"       sample_node={list(node_set)[:5]}")


def compute_class_weights(train_data, device):
    yb_all = []
    yt_all = []

    for d in train_data:
        mb = d.train_mask & (d.y_bin >= 0)
        mt = d.train_mask & (d.y_type >= 0)

        if int(mb.sum().item()) > 0:
            yb_all.append(d.y_bin[mb].cpu())
        if int(mt.sum().item()) > 0:
            yt_all.append(d.y_type[mt].cpu())

    if len(yb_all) == 0:
        pos_weight = torch.tensor([1.0], dtype=torch.float32, device=device)
    else:
        yb = torch.cat(yb_all, dim=0)
        n_pos = int((yb == 1).sum().item())
        n_neg = int((yb == 0).sum().item())
        pos_weight = torch.tensor([n_neg / max(n_pos, 1)], dtype=torch.float32, device=device)

    if len(yt_all) == 0:
        type_weight = torch.ones(5, dtype=torch.float32, device=device)
    else:
        yt = torch.cat(yt_all, dim=0)
        cnt = torch.zeros(5, dtype=torch.float32)
        for c in range(5):
            cnt[c] = float((yt == c).sum().item())
        inv = 1.0 / torch.clamp(cnt, min=1.0)
        type_weight = (inv / inv.mean()).to(device)

    return pos_weight, type_weight


@torch.no_grad()
def collect_eval_cache(model, loader, device):
    model.eval()

    logits_bin_all, y_bin_all, mask_bin_all = [], [], []
    logits_type_all, y_type_all, mask_type_all = [], [], []

    for batch in loader:
        batch = batch.to(device)
        out = model(batch)

        mb = batch.train_mask & (batch.y_bin >= 0)
        mt = batch.train_mask & (batch.y_type >= 0)

        logits_bin_all.append(out["bin_logits"].detach().cpu())
        y_bin_all.append(batch.y_bin.detach().cpu())
        mask_bin_all.append(mb.detach().cpu())

        logits_type_all.append(out["type_logits"].detach().cpu())
        y_type_all.append(batch.y_type.detach().cpu())
        mask_type_all.append(mt.detach().cpu())

    if len(logits_bin_all) == 0:
        return None

    return {
        "logits_bin": torch.cat(logits_bin_all, dim=0),
        "y_bin": torch.cat(y_bin_all, dim=0),
        "mask_bin": torch.cat(mask_bin_all, dim=0),
        "logits_type": torch.cat(logits_type_all, dim=0),
        "y_type": torch.cat(y_type_all, dim=0),
        "mask_type": torch.cat(mask_type_all, dim=0),
    }


def metrics_from_cache(cache, threshold=0.5):
    if cache is None:
        return {}

    m_bin = binary_metrics_from_logits(
        cache["logits_bin"], cache["y_bin"], cache["mask_bin"], threshold=threshold
    )
    m_type = multiclass_macro_f1(
        cache["logits_type"], cache["y_type"], cache["mask_type"]
    )

    # confusion counts 정수화
    for k in ["tp", "fp", "fn", "n"]:
        if k in m_bin:
            m_bin[k] = int(m_bin[k])

    return {
        "bin_auroc": m_bin.get("auroc", float("nan")),
        "bin_ap": m_bin.get("ap", float("nan")),
        "bin_f1": m_bin.get("f1", float("nan")),
        "bin_precision": m_bin.get("precision", float("nan")),
        "bin_recall": m_bin.get("recall", float("nan")),
        "bin_tp": m_bin.get("tp", 0),
        "bin_fp": m_bin.get("fp", 0),
        "bin_fn": m_bin.get("fn", 0),
        "bin_n": m_bin.get("n", 0),
        "type_macro_f1": m_type.get("macro_f1", float("nan")),
    }


def tune_threshold(cache):
    best_t = 0.5
    best_f1 = -1.0

    for t in np.linspace(0.05, 0.95, 37):
        m = binary_metrics_from_logits(
            cache["logits_bin"], cache["y_bin"], cache["mask_bin"], threshold=float(t)
        )
        f1 = m.get("f1", float("nan"))
        if f1 == f1 and f1 > best_f1:  # NaN check
            best_f1 = f1
            best_t = float(t)

    return best_t, best_f1


def main():
    set_seed(42)

    # clean / trojan 폴더가 분리되어 있으면 둘 다 추가하세요.
    DATA_ROOTS: List[str] = [
        "C:/HT_detect/00_contest/testcase_release_all/release_all(20250728)",
        # "C:/HT_detect/clean_10cases",
        # "C:/HT_detect/trojan_20cases",
    ]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 여러 루트에서 넷리스트 수집 + 중복 제거
    all_paths = []
    for root in DATA_ROOTS:
        all_paths.extend(find_contest_netlists(root))

    uniq = {}
    for p in all_paths:
        uniq[str(Path(p).resolve())] = Path(p)
    netlists = sorted(list(uniq.values()), key=lambda x: x.name)

    print(f"Found {len(netlists)} netlists.")

    data_list = []
    for path in netlists:
        print(f"Processing {path.name}...")
        try:
            data = build_pyg_from_netlist(netlist_path=path, top_module=None)
            data = attach_auto_features(data, gate_vocab=GATE_VOCAB)

            trojan_gates = safe_trojan_gates(load_trojan_labels(path))
            node_map = get_node_type_map(trojan_gates)
            data = attach_multitask_labels(
                data,
                node_to_type=node_map,
                assume_unlisted_normal=True
            )

            # 그래프 라벨
            data.graph_y = torch.tensor([1 if len(trojan_gates) > 0 else 0], dtype=torch.long)

            # PyG 경고 방지
            data.num_nodes = int(data.gate_type_id.numel())

            data.case_name = path.stem
            debug_label_coverage(data, trojan_gates, path.stem)

            data_list.append(data)

        except Exception as e:
            print(f"Error processing {path.name}: {e}")

    if len(data_list) == 0:
        print("No valid data found. Exiting.")
        return

    n_pos_graph = sum(int(d.graph_y.item()) for d in data_list)
    print(f"Graph label distribution: trojan={n_pos_graph}, clean={len(data_list)-n_pos_graph}")

    tr_idx, va_idx, te_idx = graph_split_indices(data_list, seed=42, train_ratio=0.70, val_ratio=0.15)
    train_data = [data_list[i] for i in tr_idx]
    val_data = [data_list[i] for i in va_idx]
    test_data = [data_list[i] for i in te_idx]

    print(f"Split: Train={len(train_data)}, Val={len(val_data)}, Test={len(test_data)}")

    train_loader = DataLoader(train_data, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=4, shuffle=False)
    test_loader = DataLoader(test_data, batch_size=4, shuffle=False)

    sample = train_data[0]
    model = HybridTrojanNetPyGMultiTask(
        num_gate_types=len(GATE_VOCAB),
        num_types=5,
        num_num_feat=sample.num_feat.size(1),
        edge_dim=sample.edge_attr.size(1) if sample.edge_attr.numel() > 0 else 3,
        hidden_dim=96,
        heads=4,
        dropout=0.15,
    ).to(device)

    pos_weight, _ = compute_class_weights(train_data, device=device)
    # type weight: trigger/control 강조
    type_weight = torch.tensor([1.0, 1.8, 3.8, 2.6, 1.4], device=device)
    print(f"Calc pos_weight: {pos_weight.item():.2f}")

    criterion = MultiTaskLoss(
        pos_weight=pos_weight,            # 기존 계산값 사용
        type_class_weight=type_weight,
        lambda_type=0.30,
        lambda_cons=0.0,
        lambda_count=0.45,                # 추가
        neg_keep_ratio=0.25,              # 추가
        gamma_pos=1.0,
        gamma_neg=3.0,
        w_bce=1.0,
        w_focal=0.8,
        w_dice=0.4,
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=220, eta_min=1e-5)

    epochs = 220
    patience = 25
    best_state = None
    best_val_ap = -1.0
    best_thr = 0.5
    bad = 0

    print("Starting training...")
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        steps = 0

        for batch in train_loader:
            batch = batch.to(device)
            out = model(batch)

            train_mask_bin = batch.train_mask & (batch.y_bin >= 0)
            train_mask_type = batch.train_mask & (batch.y_type >= 0)

            if int(train_mask_bin.sum().item()) == 0:
                continue

            loss, logs = criterion(out, batch, train_mask_bin, train_mask_type)

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()

            total_loss += float(loss.item())
            steps += 1

        avg_loss = total_loss / max(steps, 1)
        scheduler.step()

        if epoch % 5 == 0:
            val_cache = collect_eval_cache(model, val_loader, device)
            if val_cache is None:
                print(f"Epoch {epoch:03d} | Loss: {avg_loss:.4f} | val cache empty")
                continue

            tuned_thr, _ = tune_threshold(val_cache)
            val_metrics = metrics_from_cache(val_cache, threshold=tuned_thr)
            val_ap = val_metrics.get("bin_ap", float("nan"))
            val_f1 = val_metrics.get("bin_f1", float("nan"))

            print(
                f"Epoch {epoch:03d} | Loss: {avg_loss:.4f} | "
                f"Val AP: {val_ap:.4f} | Val F1@{tuned_thr:.2f}: {val_f1:.4f}"
            )

            improved = (val_ap == val_ap) and (val_ap > best_val_ap)
            if improved:
                best_val_ap = val_ap
                best_thr = tuned_thr
                best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
                bad = 0
            else:
                bad += 1
                if bad >= patience:
                    print(f"Early stopping at epoch {epoch}")
                    break

    if best_state is not None:
        model.load_state_dict(best_state)

    print("\nTraining Complete. Final Evaluation on Test Set:")
    test_cache = collect_eval_cache(model, test_loader, device)
    test_metrics = metrics_from_cache(test_cache, threshold=best_thr)

    print(f"[Using tuned threshold from val] thr={best_thr:.3f}")
    for k, v in test_metrics.items():
        print(f"{k}: {v}")

    os.makedirs("results", exist_ok=True)
    torch.save(model.state_dict(), "results/model_best.pt")
    with open("results/metrics.txt", "w", encoding="utf-8") as f:
        f.write(f"best_val_ap: {best_val_ap}\n")
        f.write(f"best_threshold: {best_thr}\n")
        for k, v in test_metrics.items():
            f.write(f"{k}: {v}\n")

    print("\nResults saved to 'results/model_best.pt' and 'results/metrics.txt'")
    
    # ---------------------------------------------------------
    # 8. Post-process threshold tuning on VAL
    # ---------------------------------------------------------
    # 튜닝은 하되, 실제로는 run_postprocess_only.py의 로직(hysteresis)을
    # 그대로 재현하기 위해 best_pp 파라미터를 사용하거나
    # 아니면 간단히 select_gates_hysteresis를 호출
    calib_data = train_data + val_data
    best_pp = tune_postprocess_thresholds(
        model=model,
        val_data=calib_data,
        device=device,
        node_thr_grid=np.linspace(0.40, 0.78, 16),
        graph_thr_grid=np.linspace(0.28, 0.75, 20),
    )
    print(
        f"[PostProc Best] node_thr={best_pp['node_thr']:.3f}, "
        f"graph_thr={best_pp['graph_thr']:.3f}, "
        f"graph_f1={best_pp['graph_f1']:.4f}, gate_f1={best_pp['gate_f1']:.4f}, obj={best_pp['obj']:.4f}"
    )

    # ---------------------------------------------------------
    # 9. Generate case-wise outputs in requested format
    # ---------------------------------------------------------
    out_dir = "results/case_outputs"
    os.makedirs(out_dir, exist_ok=True)

    # run_postprocess_only.py와 동일한 상수로 설정 (간소화)
    # 필요하다면 calibrate_graph_rules 로직을 가져와야 함.
    # 여기서는 안전하게 best_pp 값과 hysteresis 기본값 사용
    
    for d in test_data:
        risk, _, _ = predict_node_risk(model, d, device)
        valid = get_valid_mask(d)
        
        # 간단한 risk stats
        v = risk[valid]
        if v.numel() < 50:
            score = float(v.max().item()) if v.numel() > 0 else 0.0
        else:
            score = float(torch.quantile(v, 0.995).item())

        # Logic from run_postprocess_only (Hardcoded dual mode simplified)
        # Assuming we want to use the robust split logic:
        # For full pipeline, let's use the best_pp['node_thr'] as base
        
        base_seed = max(0.45, float(best_pp["node_thr"]))
        base_grow = max(0.22, base_seed - 0.24)
        
        # Dense vs Sparse Check (Simplified Rule)
        # q99 >= 0.20 -> Dense, else Sparse
        if v.numel() >= 50:
            q99 = float(torch.quantile(v, 0.99).item())
            vmax = float(v.max().item())
            spike = vmax / (q99 + 1e-6)
        else:
            q99 = 0.0
            vmax = 0.0
            spike = 0.0
            
        dense_alarm = (q99 >= 0.20)
        sparse_alarm = (vmax >= 0.62) and (spike >= 12.0)
        
        is_trojan = False
        gates = []

        if dense_alarm:
            gates = select_gates_hysteresis(
                d, risk,
                seed_thr=0.42,
                grow_thr=0.12,
                max_comp_ratio=0.90,
                singleton_seed_thr=0.82,
                local_quantile=0.18,
                force_one_seed_if_empty=False
            )
            # Fallback
            if len(gates) < 20:
                gates = select_gates_hysteresis(
                    d, risk,
                    seed_thr=0.36, 
                    grow_thr=0.08,
                    max_comp_ratio=0.95,
                    singleton_seed_thr=0.80,
                    local_quantile=0.10,
                    force_one_seed_if_empty=False
                )
            is_trojan = (len(gates) >= 15)
            
        elif sparse_alarm:
            gates = select_gates_hysteresis(
                d, risk,
                seed_thr=0.62,
                grow_thr=0.26,
                max_comp_ratio=0.05,
                singleton_seed_thr=0.92,
                local_quantile=0.86,
                force_one_seed_if_empty=False
            )
            is_trojan = (len(gates) >= 1)

        if not is_trojan:
            gates = []

        # 파일명: designX.txt
        case_name = getattr(d, "case_name", "unknown_case")
        out_path = os.path.join(out_dir, f"{case_name}.txt")
        write_case_output(out_path, bool(is_trojan), gates)

    print(f"Case outputs written to: {out_dir}")

if __name__ == "__main__":
    main()
