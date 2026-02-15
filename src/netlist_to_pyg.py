# netlist_to_pyg.py
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import networkx as nx
import torch
from torch_geometric.data import Data
from auto_features import attach_auto_features


# -----------------------------
# 0) Config / Vocab
# -----------------------------
GATE_VOCAB = {
    "PI": 0,
    "AND": 1,
    "NAND": 2,
    "OR": 3,
    "NOR": 4,
    "XOR": 5,
    "XNOR": 6,
    "NOT": 7,
    "BUF": 8,
    "MUX": 9,
    "DFF": 10,
    "OTHER": 11,
}

OUTPUT_PIN_HINTS = {
    "Y", "Z", "ZN", "Q", "QN", "QB", "OUT", "O", "S", "SO", "CO", "COUT", "X", "F"
}
INPUT_LIKE_PINS = {
    "A", "B", "C", "D", "I", "IN", "S", "SEL",
    "CLK", "CK", "G", "GN", "EN", "SE", "SI",
    "RN", "SN", "RST", "RESET", "SET", "TE", "TI", "CI"
}
SEQ_HINTS = ("DFF", "SDFF", "FF", "LATCH", "DLH", "DLP", "DF")


@dataclass
class Instance:
    cell_type: str
    inst_name: str
    pin_map: Dict[str, str]
    out_pins: List[str]
    in_pins: List[str]


# -----------------------------
# 1) Small parsing helpers
# -----------------------------
def _strip_comments(text: str) -> str:
    text = re.sub(r"//.*?$", "", text, flags=re.M)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return text


def _split_top_commas(s: str) -> List[str]:
    out: List[str] = []
    buf: List[str] = []
    depth = 0
    for ch in s:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(depth - 1, 0)

        if ch == "," and depth == 0:
            item = "".join(buf).strip()
            if item:
                out.append(item)
            buf = []
        else:
            buf.append(ch)

    item = "".join(buf).strip()
    if item:
        out.append(item)
    return out


def _expand_decl_names(names: List[str], bus_range: Optional[str]) -> List[str]:
    if not bus_range:
        return names

    m = re.match(r"\[\s*(\d+)\s*:\s*(\d+)\s*\]", bus_range)
    if not m:
        return names

    msb = int(m.group(1))
    lsb = int(m.group(2))
    step = 1 if lsb >= msb else -1

    expanded: List[str] = []
    for n in names:
        n = n.strip()
        if not n:
            continue
        for i in range(msb, lsb + step, step):
            expanded.append(f"{n}[{i}]")
    return expanded


def _extract_module(netlist: str, top_module: Optional[str]) -> Tuple[str, str]:
    """
    Returns (module_name, module_text_including_body)
    """
    modules = list(re.finditer(r"\bmodule\s+([A-Za-z_]\w*)\b.*?endmodule", netlist, flags=re.S))
    if not modules:
        raise ValueError("No module ... endmodule block found.")

    if top_module is None:
        m = modules[0]
        return m.group(1), m.group(0)

    for m in modules:
        if m.group(1) == top_module:
            return top_module, m.group(0)

    raise ValueError(f"top_module '{top_module}' not found.")


def _normalize_gate_type(cell_type: str) -> str:
    t = cell_type.upper()
    if any(k in t for k in SEQ_HINTS):
        return "DFF"
    if "MUX" in t:
        return "MUX"
    if "XNOR" in t:
        return "XNOR"
    if "XOR" in t:
        return "XOR"
    if "NAND" in t:
        return "NAND"
    if "NOR" in t:
        return "NOR"
    if "AND" in t:
        return "AND"
    if "OR" in t:
        return "OR"
    if "INV" in t or "NOT" in t:
        return "NOT"
    if "BUF" in t:
        return "BUF"
    return "OTHER"


def _is_const(tok: str) -> bool:
    tok = tok.strip()
    if tok in {"1'b0", "1'b1", "1'bx", "1'bz", "1", "0", "x", "z"}:
        return True
    if re.match(r"^\d+'[bBdDhHoO][0-9a-fA-F_xXzZ]+$", tok):
        return True
    return False


def _is_simple_net(tok: str) -> bool:
    # e.g., a, n123, bus[3]
    return bool(re.match(r"^[A-Za-z_]\w*(\[\d+\])?$", tok))


def _expand_vector_token(tok: str) -> List[str]:
    # e.g., data[7:0] -> data[7],...,data[0]
    m = re.match(r"^([A-Za-z_]\w*)\[(\d+):(\d+)\]$", tok)
    if not m:
        return [tok]
    base = m.group(1)
    a = int(m.group(2))
    b = int(m.group(3))
    step = 1 if b >= a else -1
    return [f"{base}[{i}]" for i in range(a, b + step, step)]


def _build_alias_map(module_body: str) -> Dict[str, str]:
    """
    Simple assign alias only:
      assign a = b;
      assign bus[3] = n1;
    Complex expressions are ignored.
    """
    alias: Dict[str, str] = {}
    assign_re = re.compile(r"\bassign\s+([^=;]+?)\s*=\s*([^;]+?)\s*;", flags=re.I)
    for lhs, rhs in assign_re.findall(module_body):
        lhs = lhs.strip()
        rhs = rhs.strip()

        # unary invert etc. -> ignore
        if rhs.startswith(("~", "!")):
            continue
        if _is_const(rhs):
            continue
        if _is_simple_net(lhs) and _is_simple_net(rhs):
            alias[lhs] = rhs
    return alias


def _resolve_alias(net: str, alias: Dict[str, str]) -> str:
    seen = set()
    cur = net
    while cur in alias and cur not in seen:
        seen.add(cur)
        cur = alias[cur]
    return cur


def _expr_to_nets(expr: str, alias: Dict[str, str]) -> List[str]:
    """
    Converts expression to list of net tokens.
    Supports:
      - single net: n1, bus[3]
      - vector slice: bus[7:0]
      - concat: {a,b[0],c}
      - unary ~a or !a -> a
    """
    expr = expr.strip()
    if not expr:
        return []

    # concat
    if expr.startswith("{") and expr.endswith("}"):
        inner = expr[1:-1].strip()
        parts = _split_top_commas(inner)
    else:
        parts = [expr]

    nets: List[str] = []
    for p in parts:
        p = p.strip()
        if p.startswith(("~", "!")):
            p = p[1:].strip()

        if _is_const(p):
            continue

        for t in _expand_vector_token(p):
            t = t.strip()
            if _is_const(t):
                continue
            if not _is_simple_net(t):
                # complex expression token -> ignore
                continue
            t = _resolve_alias(t, alias)
            nets.append(t)

    return nets


def _infer_pin_roles(cell_type: str, pin_map: Dict[str, str]) -> Tuple[List[str], List[str]]:
    pins = list(pin_map.keys())
    if not pins:
        return [], []

    # Positional pins
    if pins[0].startswith("__P"):
        g = _normalize_gate_type(cell_type)
        # primitive positional: first arg = output
        if g in {"AND", "NAND", "OR", "NOR", "XOR", "XNOR", "NOT", "BUF", "MUX"}:
            out = [pins[0]]
        elif g == "DFF":
            # library마다 다르지만 fallback으로 __P0를 output 가정
            out = [pins[0]]
        else:
            out = [pins[-1]]
        inn = [p for p in pins if p not in out]
        return out, inn

    # Named pins
    outs = [p for p in pins if p.upper() in OUTPUT_PIN_HINTS or p.upper().startswith(("Q", "Y", "Z", "OUT", "O"))]
    if not outs:
        candidates = [p for p in pins if p.upper() not in INPUT_LIKE_PINS]
        outs = candidates[-1:] if candidates else [pins[-1]]

    inn = [p for p in pins if p not in outs]
    return outs, inn


def _parse_declarations(module_text: str) -> Tuple[Set[str], Set[str]]:
    """
    Extract input/output nets (bit expanded).
    Works with lines like:
      input [7:0] a, b;
      output y;
      input wire clk;
    """
    input_nets: Set[str] = set()
    output_nets: Set[str] = set()

    decl_re = re.compile(
        r"\b(input|output|wire|reg)\b\s*(?:wire|reg|logic|signed|\s)*(\[[^\]]+\])?\s*([^;]+);",
        flags=re.I
    )

    for kind, rng, names_str in decl_re.findall(module_text):
        names = []
        for n in _split_top_commas(names_str):
            n = n.strip()
            if not n:
                continue
            # remove default assignment if exists
            if "=" in n:
                n = n.split("=")[0].strip()
            names.append(n)

        expanded = _expand_decl_names(names, rng)
        if kind.lower() == "input":
            input_nets.update(expanded)
        elif kind.lower() == "output":
            output_nets.update(expanded)

    return input_nets, output_nets


def _parse_instances(module_body: str) -> List[Instance]:
    """
    Parse structural instances:
      CELL U1 ( .A(n1), .B(n2), .Y(n3) );
      and  g1 (n3, a, b);  # positional primitive
    """
    body = re.sub(r"\(\*.*?\*\)", "", module_body, flags=re.S)  # remove attributes

    inst_re = re.compile(
        r"^\s*([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\s*\((.*?)\)\s*;\s*$",
        flags=re.M | re.S
    )
    named_pin_re = re.compile(r"\.(\w+)\s*\(\s*([^()]+?)\s*\)")

    instances: List[Instance] = []
    for m in inst_re.finditer(body):
        cell = m.group(1)
        inst = m.group(2)
        pins_raw = m.group(3).strip()

        if cell.lower() in {"module", "input", "output", "wire", "reg", "assign"}:
            continue

        pin_pairs = named_pin_re.findall(pins_raw)
        pin_map: Dict[str, str] = {}

        if pin_pairs:
            for p, e in pin_pairs:
                pin_map[p.strip()] = e.strip()
        else:
            # positional fallback
            plist = _split_top_commas(pins_raw)
            for i, e in enumerate(plist):
                pin_map[f"__P{i}"] = e.strip()

        out_pins, in_pins = _infer_pin_roles(cell, pin_map)
        instances.append(
            Instance(
                cell_type=cell,
                inst_name=inst,
                pin_map=pin_map,
                out_pins=out_pins,
                in_pins=in_pins,
            )
        )

    return instances


def _compute_depth(
    num_nodes: int,
    edges: List[Tuple[int, int]],
    source_nodes: List[int],
) -> List[float]:
    """
    Cycle-safe depth:
    - SCC condensation DAG에서 longest depth 계산
    """
    if num_nodes == 0:
        return []

    g = nx.DiGraph()
    g.add_nodes_from(range(num_nodes))
    g.add_edges_from(edges)

    dag = nx.condensation(g)  # DAG
    mapping: Dict[int, int] = dag.graph["mapping"]  # original node -> scc id

    NEG = -10**9
    comp_depth = {c: NEG for c in dag.nodes()}

    for s in source_nodes:
        comp_depth[mapping[s]] = max(comp_depth[mapping[s]], 0)

    for c in nx.topological_sort(dag):
        if comp_depth[c] == NEG:
            comp_depth[c] = 0
        for nxt in dag.successors(c):
            comp_depth[nxt] = max(comp_depth[nxt], comp_depth[c] + 1)

    return [float(comp_depth[mapping[i]]) for i in range(num_nodes)]


# -----------------------------
# 2) Public API
# -----------------------------
def build_pyg_from_netlist(
    netlist_path: str | Path,
    top_module: Optional[str] = None,
    scoap: Optional[Dict[str, Tuple[float, float, float]]] = None,   # node -> (CC0, CC1, CO)
    switching: Optional[Dict[str, float]] = None,                    # node -> activity [0,1]
    trojan_nodes: Optional[Set[str]] = None,                         # label positives (instance names)
) -> Data:
    """
    Directly parse .v netlist (no JSON) -> PyG Data.
    """
    scoap = scoap or {}
    switching = switching or {}
    trojan_nodes = trojan_nodes or set()

    text = Path(netlist_path).read_text(encoding="utf-8", errors="ignore")
    text = _strip_comments(text)

    mod_name, module_text = _extract_module(text, top_module=top_module)
    # body part
    start = module_text.find(";")
    end = module_text.rfind("endmodule")
    module_body = module_text[start + 1:end] if start >= 0 else module_text

    input_nets, _output_nets = _parse_declarations(module_text)
    alias = _build_alias_map(module_body)
    instances = _parse_instances(module_body)

    if not instances:
        raise ValueError("No gate instances parsed. Check netlist style or parser assumptions.")

    # Build node list (instance nodes first)
    node_names: List[str] = []
    node_types: List[str] = []
    is_pi_node: List[bool] = []

    for inst in instances:
        node_names.append(inst.inst_name)
        node_types.append(_normalize_gate_type(inst.cell_type))
        is_pi_node.append(False)

    inst2idx = {n: i for i, n in enumerate(node_names)}

    # net -> drivers / sinks (instance index)
    drivers: Dict[str, List[int]] = {}
    sinks: Dict[str, List[int]] = {}

    for inst in instances:
        i = inst2idx[inst.inst_name]

        for p in inst.out_pins:
            expr = inst.pin_map.get(p, "")
            for net in _expr_to_nets(expr, alias):
                drivers.setdefault(net, []).append(i)

        for p in inst.in_pins:
            expr = inst.pin_map.get(p, "")
            for net in _expr_to_nets(expr, alias):
                sinks.setdefault(net, []).append(i)

    # Create PI pseudo-nodes only when needed (un-driven input nets)
    pi_idx_of_net: Dict[str, int] = {}
    for net in sorted(sinks.keys()):
        if net in drivers:
            continue
        if net in input_nets:
            pi_name = f"PI::{net}"
            idx = len(node_names)
            node_names.append(pi_name)
            node_types.append("PI")
            is_pi_node.append(True)
            pi_idx_of_net[net] = idx

    # Build edges
    edge_set: Set[Tuple[int, int]] = set()
    for net, dsts in sinks.items():
        if net in drivers:
            srcs = drivers[net]
            for u in srcs:
                for v in dsts:
                    if u != v:
                        edge_set.add((u, v))
        elif net in pi_idx_of_net:
            u = pi_idx_of_net[net]
            for v in dsts:
                if u != v:
                    edge_set.add((u, v))

    edges = sorted(edge_set)
    num_nodes = len(node_names)

    # Gate type id
    gate_type_id = torch.tensor(
        [GATE_VOCAB.get(t, GATE_VOCAB["OTHER"]) for t in node_types],
        dtype=torch.long
    )

    # Numeric features: [CC0, CC1, CO, SW, depth]
    num_feat = torch.zeros((num_nodes, 5), dtype=torch.float32)

    for i, name in enumerate(node_names):
        if is_pi_node[i]:
            continue
        cc0, cc1, co = scoap.get(name, (0.0, 0.0, 0.0))
        sw = float(switching.get(name, 0.0))
        sw = max(0.0, min(1.0, sw))
        num_feat[i, 0] = float(cc0)
        num_feat[i, 1] = float(cc1)
        num_feat[i, 2] = float(co)
        num_feat[i, 3] = sw

    # Depth (source: PI nodes + DFF nodes)
    src_nodes = [i for i, b in enumerate(is_pi_node) if b] + \
                [i for i, t in enumerate(node_types) if t == "DFF"]

    depths = _compute_depth(num_nodes, edges, src_nodes if src_nodes else list(range(num_nodes)))
    if len(depths) == num_nodes:
        num_feat[:, 4] = torch.tensor(depths, dtype=torch.float32)

    # Edge tensors
    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()  # [2, E]
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    # Edge features: [delta_depth, seq_edge, rare_dst]
    edge_attr_list: List[List[float]] = []
    is_seq = torch.tensor([1 if t == "DFF" else 0 for t in node_types], dtype=torch.float32)

    for (u, v) in edges:
        delta_depth = float(num_feat[v, 4] - num_feat[u, 4])
        seq_edge = float((is_seq[u] > 0) or (is_seq[v] > 0))

        cc0, cc1, co, sw = num_feat[v, 0].item(), num_feat[v, 1].item(), num_feat[v, 2].item(), num_feat[v, 3].item()
        rare_dst = (cc0 + cc1 + co) * (1.0 - sw)

        edge_attr_list.append([delta_depth, seq_edge, rare_dst])

    edge_attr = torch.tensor(edge_attr_list, dtype=torch.float32) if edge_attr_list else torch.empty((0, 3), dtype=torch.float32)

    # Labels
    y = torch.full((num_nodes,), -1, dtype=torch.long)  # unlabeled default
    train_mask = torch.tensor([not b for b in is_pi_node], dtype=torch.bool)

    if trojan_nodes:
        y[:] = 0
        for i, n in enumerate(node_names):
            if n in trojan_nodes:
                y[i] = 1
        # PI node는 supervised에서 제외 권장
        y[~train_mask] = -1

    data = Data(
        edge_index=edge_index,
        edge_attr=edge_attr,
        gate_type_id=gate_type_id,
        num_feat=num_feat,
        y=y,
        train_mask=train_mask,
    )
    data.node_names = node_names
    data.node_types = node_types
    data.top_module = mod_name

    # Auto-calculate SCOAP/Activity if missing
    data = attach_auto_features(data, gate_vocab=GATE_VOCAB, overwrite=False)

    return data


def load_scoap_csv(path: str | Path) -> Dict[str, Tuple[float, float, float]]:
    """
    CSV columns: node,cc0,cc1,co
    """
    out: Dict[str, Tuple[float, float, float]] = {}
    text = Path(path).read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    if not text:
        return out
    hdr = [h.strip().lower() for h in text[0].split(",")]
    idx = {k: i for i, k in enumerate(hdr)}
    for line in text[1:]:
        c = [x.strip() for x in line.split(",")]
        if len(c) < 4:
            continue
        n = c[idx["node"]]
        out[n] = (float(c[idx["cc0"]]), float(c[idx["cc1"]]), float(c[idx["co"]]))
    return out


def load_switching_csv(path: str | Path) -> Dict[str, float]:
    """
    CSV columns: node,sw
    """
    out: Dict[str, float] = {}
    text = Path(path).read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    if not text:
        return out
    hdr = [h.strip().lower() for h in text[0].split(",")]
    idx = {k: i for i, k in enumerate(hdr)}
    for line in text[1:]:
        c = [x.strip() for x in line.split(",")]
        if len(c) < 2:
            continue
        n = c[idx["node"]]
        out[n] = float(c[idx["sw"]])
    return out