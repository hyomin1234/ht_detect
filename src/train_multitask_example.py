# train_multitask_example.py
from __future__ import annotations

import torch
from torch.optim import AdamW

from netlist_to_pyg import build_pyg_from_netlist, GATE_VOCAB  # 기존 파일
from auto_features import attach_auto_features
from label_utils import attach_multitask_labels, TYPE_TO_ID
from splits_metrics import stratified_node_split, evaluate_multitask
from hybrid_trojan_multitask import HybridTrojanNetPyGMultiTask, MultiTaskLoss


def _compute_pos_weight(y_bin: torch.Tensor, mask: torch.Tensor, device):
    yt = y_bin[mask]
    pos = int((yt == 1).sum().item())
    neg = int((yt == 0).sum().item())
    val = neg / max(pos, 1)
    return torch.tensor([val], dtype=torch.float32, device=device)


def _compute_type_weights(y_type: torch.Tensor, mask: torch.Tensor, num_types: int, device):
    yt = y_type[mask]
    w = torch.ones(num_types, dtype=torch.float32, device=device)
    for c in range(num_types):
        cnt = int((yt == c).sum().item())
        w[c] = 1.0 / max(cnt, 1)
    w = w / w.mean()
    return w


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # ----------------------------------------------------
    # 1) JSON 없이 netlist 직접 파싱
    # ----------------------------------------------------
    data = build_pyg_from_netlist(
        netlist_path="design_top.v",
        top_module="top",
        scoap=None,          # 외부 파일 없으면 None
        switching=None,      # 외부 파일 없으면 None
        trojan_nodes=None,   # 멀티태스크 라벨 함수에서 처리
    )

    # ----------------------------------------------------
    # 2) SCOAP/activity 자동 채우기
    # ----------------------------------------------------
    data = attach_auto_features(data, gate_vocab=GATE_VOCAB, overwrite=False, pi_prob=0.5)

    # ----------------------------------------------------
    # 3) 멀티태스크 라벨 (예시)
    #    node_name -> type
    # ----------------------------------------------------
    node_to_type = {
        "Trigger_U48": "trigger",
        "Payload_X12": "logic",
        "LeakPath_U3": "leakage",
        "FSMHijack_U7": "control",
        # 정상은 생략하면 normal 처리(assume_unlisted_normal=True)
    }
    data = attach_multitask_labels(data, node_to_type=node_to_type, assume_unlisted_normal=True)

    # ----------------------------------------------------
    # 4) split (stratified)
    # ----------------------------------------------------
    data = stratified_node_split(
        data,
        y_key="y_bin",
        eligible_mask_key="train_mask",   # parser에서 PI 제외 마스크
        train_ratio=0.70,
        val_ratio=0.15,
        seed=42,
    )

    data = data.to(device)

    # ----------------------------------------------------
    # 5) model / loss
    # ----------------------------------------------------
    model = HybridTrojanNetPyGMultiTask(
        num_gate_types=len(GATE_VOCAB),
        num_types=5,
        num_num_feat=data.num_feat.size(1),
        edge_dim=data.edge_attr.size(1) if data.edge_attr.numel() > 0 else 3,
        hidden_dim=128,
        heads=4,
        dropout=0.1,
    ).to(device)

    train_bin_mask = data.split_train_mask & (data.y_bin >= 0)
    train_type_mask = data.split_train_mask & (data.y_type >= 0)

    pos_weight = _compute_pos_weight(data.y_bin, train_bin_mask, device)
    type_weight = _compute_type_weights(data.y_type, train_type_mask, num_types=5, device=device)

    criterion = MultiTaskLoss(
        alpha=0.25,
        gamma=2.0,
        pos_weight=pos_weight,
        type_class_weight=type_weight,
        lambda_type=0.4,
        lambda_cons=0.1,
    )
    optimizer = AdamW(model.parameters(), lr=2e-4, weight_decay=1e-4)

    # ----------------------------------------------------
    # 6) train loop + metric logging
    # ----------------------------------------------------
    best_val_ap = -1.0
    best_state = None

    for epoch in range(1, 201):
        model.train()
        optimizer.zero_grad()

        out = model(data)
        loss, logs = criterion(out, data, train_bin_mask, train_type_mask)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            model.eval()
            with torch.no_grad():
                out_eval = model(data)

            val_bin_mask = data.split_val_mask & (data.y_bin >= 0)
            val_type_mask = data.split_val_mask & (data.y_type >= 0)
            val_metrics = evaluate_multitask(out_eval, data, val_bin_mask, val_type_mask)

            msg = (
                f"[{epoch:03d}] "
                f"loss={logs['loss_total']:.4f} "
                f"bin_f1={val_metrics['bin_f1']:.4f} "
                f"bin_ap={val_metrics['bin_ap']:.4f} "
                f"bin_auc={val_metrics['bin_auroc']:.4f} "
                f"type_macro_f1={val_metrics['type_macro_f1']:.4f}"
            )
            print(msg)

            val_ap = val_metrics["bin_ap"]
            if val_ap == val_ap and val_ap > best_val_ap:  # NaN check
                best_val_ap = val_ap
                best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}

    if best_state is not None:
        model.load_state_dict(best_state)

    # ----------------------------------------------------
    # 7) test metrics
    # ----------------------------------------------------
    model.eval()
    with torch.no_grad():
        out_test = model(data)

    test_bin_mask = data.split_test_mask & (data.y_bin >= 0)
    test_type_mask = data.split_test_mask & (data.y_type >= 0)
    test_metrics = evaluate_multitask(out_test, data, test_bin_mask, test_type_mask)

    print("\n[Test Metrics]")
    for k, v in test_metrics.items():
        if isinstance(v, float):
            print(f"{k:>16s}: {v:.6f}")
        else:
            print(f"{k:>16s}: {v}")

    # ----------------------------------------------------
    # 8) suspicious top-k
    # ----------------------------------------------------
    prob = torch.sigmoid(out_test["bin_logits"]).detach().cpu()
    valid = torch.where(data.train_mask.cpu())[0]
    k = min(30, valid.numel())
    vals, idx = torch.topk(prob[valid], k=k)

    type_pred = out_test["type_logits"].argmax(dim=-1).detach().cpu()
    id_to_type = {v: k for k, v in TYPE_TO_ID.items()}

    print("\n[Top Suspicious Nodes]")
    for rank, (v, j) in enumerate(zip(vals.tolist(), idx.tolist()), start=1):
        nid = int(valid[j].item())
        nname = data.node_names[nid]
        tname = id_to_type.get(int(type_pred[nid].item()), "unknown")
        print(f"{rank:02d}. {nname:40s} prob={v:.4f} type_pred={tname}")


if __name__ == "__main__":
    main()