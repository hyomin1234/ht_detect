# run_train_example.py
from __future__ import annotations

import torch
from torch.optim import AdamW

from netlist_to_pyg import build_pyg_from_netlist, load_scoap_csv, load_switching_csv, GATE_VOCAB
from hybrid_trojan_pyg import HybridTrojanNetPyG, FocalBCEWithLogits


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # (선택) 외부 피처
    scoap = load_scoap_csv("scoap.csv") if False else {}
    sw = load_switching_csv("switching.csv") if False else {}

    # (선택) 라벨: 트로이 게이트 인스턴스 이름 집합
    trojan_nodes = {"Trigger_U48", "Payload_X12"}  # 예시

    data = build_pyg_from_netlist(
        netlist_path="design_top.v",
        top_module="top",
        scoap=scoap,
        switching=sw,
        trojan_nodes=trojan_nodes,
    ).to(device)

    model = HybridTrojanNetPyG(
        num_gate_types=len(GATE_VOCAB),
        num_num_feat=data.num_feat.size(1),
        edge_dim=data.edge_attr.size(1) if data.edge_attr.numel() else 3,
        hidden_dim=128,
        heads=4,
        dropout=0.1,
    ).to(device)

    # pos_weight for imbalance
    mask = data.train_mask & (data.y >= 0)
    y_train = data.y[mask]
    pos = int((y_train == 1).sum().item())
    neg = int((y_train == 0).sum().item())
    pw = torch.tensor([neg / max(pos, 1)], device=device)

    criterion = FocalBCEWithLogits(alpha=0.25, gamma=2.0, pos_weight=pw)
    opt = AdamW(model.parameters(), lr=2e-4, weight_decay=1e-4)

    for epoch in range(1, 201):
        model.train()
        opt.zero_grad()

        logits = model(data)
        loss = criterion(logits[mask], data.y[mask].float())

        # DSP 정상 구조 오탐 억제용 regularization 예시(선택)
        # if hasattr(data, "dsp_anchor_mask"):
        #     prob = torch.sigmoid(logits[data.dsp_anchor_mask])
        #     loss = loss + 0.05 * prob.mean()

        loss.backward()
        opt.step()

        if epoch % 20 == 0:
            model.eval()
            with torch.no_grad():
                p = torch.sigmoid(logits)
                pred = (p > 0.5).long()
                acc = (pred[mask] == data.y[mask]).float().mean().item()
            print(f"[{epoch:03d}] loss={loss.item():.4f} acc={acc:.4f}")

    # Inference: suspicious top-k
    model.eval()
    with torch.no_grad():
        prob = torch.sigmoid(model(data))
    valid_idx = torch.where(data.train_mask)[0]
    vals, ord_idx = torch.topk(prob[valid_idx], k=min(30, valid_idx.numel()))
    top_nodes = [data.node_names[valid_idx[i].item()] for i in ord_idx]
    print("Top suspicious nodes:")
    for n, v in zip(top_nodes, vals.tolist()):
        print(f"{n:40s}  {v:.4f}")


if __name__ == "__main__":
    main()