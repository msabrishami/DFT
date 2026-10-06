"""Truth-table tests for every gate in the three simulation modes.

The expected values come from small reference functions written independently
of the gate classes: two-valued logic, Kleene three-valued logic and, for the
bit-parallel mode, the two-valued reference applied to each bit separately.
"""
import itertools
import random

import pytest

from pycad.config import X_VALUE
from pycad.node import node
from pycad.node.node import GateType, NodeType

BITS = node.Node.bitlen  # width of the bit-parallel values


# ---------------------------------------------------------------- references
def ref_and(vals):
    return int(all(vals))


def ref_or(vals):
    return int(any(vals))


def ref_xor(vals):
    return sum(vals) % 2


def neg(f):
    return lambda vals: 1 - f(vals)


REFERENCE = {
    "AND": ref_and,
    "NAND": neg(ref_and),
    "OR": ref_or,
    "NOR": neg(ref_or),
    "XOR": ref_xor,
    "XNOR": neg(ref_xor),
}


def ref_ternary(name, vals):
    """Kleene three-valued logic. An unknown input only matters when no known input decides."""
    f = REFERENCE[name]
    unknown = [i for i, v in enumerate(vals) if v == X_VALUE]
    if not unknown:
        return f(vals)
    # The output is known only if every assignment of the unknown inputs agrees.
    outs = set()
    for fill in itertools.product([0, 1], repeat=len(unknown)):
        trial = list(vals)
        for i, bit in zip(unknown, fill, strict=True):
            trial[i] = bit
        outs.add(f(trial))
    return outs.pop() if len(outs) == 1 else X_VALUE


MULTI_INPUT = ["AND", "NAND", "OR", "NOR", "XOR", "XNOR"]


# ------------------------------------------------------------------- helpers
def build(name, values):
    """A gate of type ``name`` whose input nodes hold ``values``."""
    inputs = []
    for i, v in enumerate(values):
        ipt = node.IPT(NodeType.PI, GateType.IPT, str(i))
        ipt.value = v
        inputs.append(ipt)
    gate = getattr(node, name)(NodeType.GATE, GateType(name), "g")
    gate.unodes = inputs
    return gate


# --------------------------------------------------------------------- tests
@pytest.mark.parametrize("name", MULTI_INPUT)
@pytest.mark.parametrize("fanin", [1, 2, 3, 4])
def test_binary_truth_table(name, fanin):
    for vals in itertools.product([0, 1], repeat=fanin):
        gate = build(name, vals)
        gate.imply()
        assert gate.value == REFERENCE[name](vals), (name, vals)


@pytest.mark.parametrize("name", MULTI_INPUT)
@pytest.mark.parametrize("fanin", [1, 2, 3, 4])
def test_ternary_truth_table(name, fanin):
    for vals in itertools.product([0, 1, X_VALUE], repeat=fanin):
        gate = build(name, vals)
        gate.imply_t()
        assert gate.value == ref_ternary(name, vals), (name, vals)


@pytest.mark.parametrize("name", MULTI_INPUT)
@pytest.mark.parametrize("fanin", [1, 2, 3, 4])
def test_bit_parallel_matches_per_bit_reference(name, fanin):
    rng = random.Random(1234)
    for _ in range(50):
        words = [rng.getrandbits(BITS) for _ in range(fanin)]
        gate = build(name, words)
        gate.imply_b()
        expected = 0
        for k in range(BITS):
            bit_vals = [(w >> k) & 1 for w in words]
            expected |= REFERENCE[name](bit_vals) << k
        assert gate.value == expected, (name, words)


@pytest.mark.parametrize("name", ["BUFF", "BRCH"])
def test_pass_through_gates(name):
    for v in [0, 1, X_VALUE]:
        gate = build(name, [v])
        gate.imply_t()
        assert gate.value == v
    for v in [0, 1]:
        gate = build(name, [v])
        gate.imply()
        assert gate.value == v
    word = random.Random(7).getrandbits(BITS)
    gate = build(name, [word])
    gate.imply_b()
    assert gate.value == word


def test_not_gate_all_modes():
    for v, expected in [(0, 1), (1, 0)]:
        gate = build("NOT", [v])
        gate.imply()
        assert gate.value == expected
        gate.imply_t()
        assert gate.value == expected
    gate = build("NOT", [X_VALUE])
    gate.imply_t()
    assert gate.value == X_VALUE

    word = random.Random(7).getrandbits(BITS)
    gate = build("NOT", [word])
    gate.imply_b()
    assert gate.value == word ^ (2**BITS - 1)


def test_ipt_stores_the_applied_value_in_every_mode():
    ipt = node.IPT(NodeType.PI, GateType.IPT, "1")
    for method, v in [("imply", 1), ("imply_t", X_VALUE), ("imply_b", 0b1010)]:
        getattr(ipt, method)(v)
        assert ipt.value == v


def test_string_valued_inputs_are_converted_for_binary_logic():
    """Netlist-style '0'/'1' strings are accepted as input values."""
    gate = build("AND", ["1", "1"])
    gate.imply()
    assert gate.value == 1
    gate = build("OR", ["0", "0"])
    gate.imply()
    assert gate.value == 0


# ---------------------------------------------------------------- node types
def test_types_compare_equal_to_plain_strings():
    assert GateType.NAND == "NAND"
    assert NodeType.PI == "PI"
    assert str(GateType.XOR) == "XOR"


def test_nodes_convert_string_types_to_enum_members():
    n = node.AND("GATE", "AND", "5")
    assert n.gtype is GateType.AND
    assert n.ntype is NodeType.GATE


def test_unknown_types_are_rejected():
    with pytest.raises(ValueError):
        node.AND("GATE", "NOTAGATE", "5")
    with pytest.raises(ValueError):
        node.AND("NOTANODE", "AND", "5")


def test_ckt_file_codes():
    assert [GateType.from_ckt_code(i) for i in range(10)] == [
        "IPT", "BRCH", "XOR", "OR", "NOR", "NOT", "NAND", "AND", "XNOR", "BUFF"]
    assert [NodeType.from_ckt_code(i) for i in range(4)] == ["GATE", "PI", "FB", "PO"]
