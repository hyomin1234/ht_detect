# label_utils.py
from __future__ import annotations
from typing import Dict, Union
import torch

TYPE_TO_ID = {
    "normal": 0,
    "leakage": 1,
    "trigger": 2,
    "control": 3,
    "logic": 4,
}
ID_TO_TYPE = {v: k for k, v in TYPE_TO_ID.items()}


def attach_multitask_labels(
    data,
    node_to_type: Dict[str, Union[int, str]],
    assume_unlisted_normal: bool = True,
):
    """
    data.node_names 필요
    산출:
      data.y_bin  : [N] (0/1, unknown=-1)
      data.y_type : [N] (0~4, unknown=-1)
    """
    if not hasattr(data, "node_names"):
        raise ValueError("data.node_names가 필요합니다.")

    n = len(data.node_names)
    y_bin = torch.full((n,), -1, dtype=torch.long)
    y_type = torch.full((n,), -1, dtype=torch.long)

    if hasattr(data, "train_mask"):
        eligible = data.train_mask.clone().bool()
    else:
        eligible = torch.ones(n, dtype=torch.bool)

    if assume_unlisted_normal:
        y_bin[eligible] = 0
        y_type[eligible] = 0

    for i, name in enumerate(data.node_names):
        if not eligible[i]:
            continue
        if name not in node_to_type:
            continue

        t = node_to_type[name]
        if isinstance(t, str):
            tid = TYPE_TO_ID.get(t.lower(), None)
            if tid is None:
                raise ValueError(f"Unknown type label string: {t}")
        else:
            tid = int(t)
            if tid < 0 or tid > 4:
                raise ValueError(f"Type id must be in [0..4], got {tid}")

        y_type[i] = tid
        y_bin[i] = 0 if tid == 0 else 1

    data.y_bin = y_bin
    data.y_type = y_type
    return data