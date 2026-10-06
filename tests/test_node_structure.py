"""Tests for node construction and the connectivity helpers of Node."""
import pytest

from pycad.circuit.circuit import Circuit
from pycad.node import node
from pycad.node.node import GateType, NodeType

LIB = Circuit.STD_NODE_LIB


def info(n_type, g_type, num="1"):
    return {"n_type": n_type, "g_type": g_type, "num": num}


@pytest.mark.parametrize("g_type", ["XOR", "OR", "NOR", "NOT", "NAND", "AND", "BUFF", "XNOR"])
@pytest.mark.parametrize("n_type", ["GATE", "PO"])
def test_gen_node_builds_gates(n_type, g_type):
    n = node.Node.gen_node(info(n_type, g_type), LIB)
    assert isinstance(n, getattr(node, g_type))
    assert n.gtype == g_type and n.ntype == n_type


def test_gen_node_builds_inputs_and_branches():
    assert isinstance(node.Node.gen_node(info("PI", "IPT"), LIB), node.IPT)
    # a primary input that is also a primary output
    assert isinstance(node.Node.gen_node(info("PO", "IPT"), LIB), node.IPT)
    assert isinstance(node.Node.gen_node(info("FB", "BRCH"), LIB), node.BRCH)


@pytest.mark.parametrize("n_type, g_type", [("GATE", "IPT"), ("PI", "AND"), ("FB", "NAND")])
def test_gen_node_rejects_unsupported_combinations(n_type, g_type):
    with pytest.raises(NotImplementedError, match="Unsupported node"):
        node.Node.gen_node(info(n_type, g_type, "77"), LIB)


def make_gate_with_inputs(count=3):
    gate = node.AND(NodeType.GATE, GateType.AND, "g")
    inputs = [node.IPT(NodeType.PI, GateType.IPT, str(i)) for i in range(count)]
    for i, ipt in enumerate(inputs):
        ipt.value = i % 2
        gate.add_unode(ipt)
        ipt.add_dnode(gate)
    return gate, inputs


def test_get_neighbors_returns_the_other_inputs_of_the_same_gate():
    _, (a, b, c) = make_gate_with_inputs()
    assert a.get_neighbors() == [b, c]
    assert a.get_neighbors(value=True) == [1, 0]


def test_get_neighbors_inclusive_starts_with_the_node_itself():
    _, (a, b, c) = make_gate_with_inputs()
    assert a.get_neighbors(inclusive=True) == [a, b, c]
    assert b.get_neighbors(inclusive=True, value=True) == [1, 0, 0]


def test_get_neighbors_of_a_node_without_fanout():
    gate, _ = make_gate_with_inputs()
    assert gate.get_neighbors() == []
    assert gate.get_neighbors(inclusive=True) == [gate]


def test_str_lists_types_level_and_connections():
    gate, _ = make_gate_with_inputs(2)
    gate.lev = 1
    assert str(gate) == "g, GATE, AND, 1, FIN: [0 1], FOUT: []"
