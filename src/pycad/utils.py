"""Small helpers for working with nodes: cell names and fan-in cones."""
from collections import deque

import numpy as np


def get_node_gtype_fin(node):
    """Convert a node into the cell name ``c<lower-case type><fan-in>``.

    For example, a NAND with two inputs becomes ``cnand2``. Used for changing
    CSM cells into DFT cells. Primary inputs and fan-out branches keep their type.
    """
    if node.ntype in ["PI", "FB"]:
        return node.gtype
    if node.gtype == "NOT":
        return "cinv"
    if node.gtype == "BUFF":
        return "cbuff"
    if node.gtype in ["OR", "NOR", "NAND", "AND", "XOR", "XNOR"]:
        return "c" + node.gtype.lower() + str(len(node.unodes))


def _get_fanin_rec(node, res):
    """Depth-first collection of the node numbers in the fan-in cone of ``node``."""
    if node.num in res:
        return res
    res.add(node.num)
    if node.gtype == "IPT":
        return res
    for unode in node.unodes:
        _get_fanin_rec(unode, res)
    return res


def get_fanin(circuit, node):
    """Return the set of node numbers in the fan-in cone of ``node``.

    ``node`` is a Node, or the number (str) of a node in ``circuit``.
    """
    if isinstance(node, str):
        node = circuit.nodes[node]
    return _get_fanin_rec(node, set())


def get_fanin_depth(circuit, node, lev_depth):
    """Return the nodes in the fan-in cone of ``node`` within ``lev_depth`` hops.

    The distance is the minimum number of hops, not the circuit level. This is a
    breadth-first search running backward in the circuit graph. ``node.flagA``
    records the backward level and is reset to None afterwards.
    """
    res = []
    q = deque()
    q.append(node)
    node.flagA = 0

    while q:
        current_node = q.popleft()
        res.append(current_node)
        if current_node.flagA == lev_depth:
            continue
        for unode in current_node.unodes:
            if unode.flagA is not None:  # already visited
                continue
            unode.flagA = current_node.flagA + 1
            q.append(unode)

    for n in res:
        n.flagA = None

    return res


def get_fanin_BFS(circuit, node, lev_depth=False):
    """Return the nodes in the fan-in cone of ``node`` as a list, in BFS order.

    If ``lev_depth`` is given, the search is limited to that many hops (see
    ``get_fanin_depth``). ``node.flagA`` is used internally and reset afterwards.
    """
    if lev_depth:
        return get_fanin_depth(circuit, node, lev_depth)

    res = []
    q = deque()
    q.append(node)
    node.flagA = True

    while q:
        current_node = q.popleft()
        res.append(current_node)
        for unode in current_node.unodes:
            if unode.flagA is not None:
                continue
            unode.flagA = True
            q.append(unode)

    for n in res:
        n.flagA = None

    return res


def estimate_FC(probs, tp):
    """Estimate the fault coverage after ``tp`` random test patterns.

    Parameters
    ----------
    probs : dict
        Fault string -> detection probability of one random pattern.
    tp : int
        Number of test patterns.
    """
    nfc = 0
    for key in probs:
        nfc += np.exp(-probs[key] * tp)

    return 1 - nfc / len(probs)


def fix_size(number, k):
    """Left-pad the digit string ``number`` with zeros, or cut it from the left, to length ``k``."""
    return number[-k:].zfill(k) if k > 0 else ""
