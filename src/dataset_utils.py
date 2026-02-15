# dataset_utils.py
from __future__ import annotations
import glob
import os
from pathlib import Path
from typing import List, Tuple, Set, Dict

def find_contest_netlists(root_dir: str | Path) -> List[Path]:
    """
    contest_root 내의 모든 design*.v 파일들을 재귀적으로 찾음 (trojan, trojan_free 폴더 포함)
    """
    root = Path(root_dir)
    # look for design*.v recursively
    pattern = "**/design*.v"
    found = list(root.glob(pattern))
    return sorted(found)

def load_trojan_labels(netlist_path: str | Path) -> Set[str]:
    """
    designX.v -> resultX.txt
    resultX.txt format:
      TROJANED
      TROJAN_GATES
      g123
      g456
      ...
    """
    path = Path(netlist_path)
    name = path.stem  # "design14"
    if not name.startswith("design"):
        return set()
    
    # number extraction
    idx_str = name.replace("design", "")
    if not idx_str.isdigit():
        return set()
        
    result_name = f"result{idx_str}.txt"
    result_path = path.parent / result_name
    
    trojan_gates = set()
    if not result_path.exists():
        # result 파일이 없으면 label 없는 것으로 간주
        return set()
        
    lines = result_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    start_reading = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == "TROJAN_GATES":
            start_reading = True
            continue
        if start_reading:
            trojan_gates.add(line)
            
    return trojan_gates

def get_node_type_map(trojan_gates: Set[str]) -> Dict[str, str]:
    """
    단순 binary 라벨링:
    trojan_gates에 있으면 'trigger' (임시), 없으면 'normal' (생략 가능)
    """
    mapping = {}
    for g in trojan_gates:
        # Multi-task 학습을 위해 일단 'trigger'로 통일 (세부 정보 없으므로)
        mapping[g] = "trigger"
    return mapping
