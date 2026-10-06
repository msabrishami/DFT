"""Per-gate SCOAP, STAFAN, PFS and sensitization rules of the DFT nodes.

Expected values are written out by hand from the definitions of the measures.
"""
import itertools
import random
import warnings

import pytest

from pycad.node import dft_node
from pycad.node.node import GateType, NodeType


def make_gate(name, inputs):
    """A DFT gate of type ``name`` fed by new input nodes with the given attributes."""
    gate = getattr(dft_node, f"DFT{name}")(NodeType.GATE, GateType(name), "g")
    for i, attrs in enumerate(inputs):
        ipt = dft_node.DFTIPT(NodeType.PI, GateType.IPT, str(i))
        for key, value in attrs.items():
            setattr(ipt, key, value)
        ipt.dnodes = [gate]
        gate.unodes.append(ipt)
    return gate


def cc(c0, c1):
    return {"CC0": c0, "CC1": c1}


# --------------------------------------------------------------------- SCOAP
A, B = cc(2, 3), cc(4, 1)  # two inputs: (CC0, CC1)


@pytest.mark.parametrize("name, cc0, cc1, co_a, co_b", [
    # AND: 1 needs every input at 1, 0 needs the easiest input at 0
    ("AND", 1 + 2, 1 + 3 + 1, 10 + 1 + 1, 10 + 1 + 3),
    ("NAND", 1 + 3 + 1, 1 + 2, 10 + 1 + 1, 10 + 1 + 3),
    # OR: 0 needs every input at 0, 1 needs the easiest input at 1
    ("OR", 1 + 2 + 4, 1 + 1, 10 + 1 + 4, 10 + 1 + 2),
    ("NOR", 1 + 1, 1 + 2 + 4, 10 + 1 + 4, 10 + 1 + 2),
])
def test_two_input_gate_scoap(name, cc0, cc1, co_a, co_b):
    gate = make_gate(name, [A, B])
    gate.CO = 10
    gate.eval_cc()
    gate.eval_co()
    assert (gate.CC0, gate.CC1) == (cc0, cc1)
    assert (gate.unodes[0].CO, gate.unodes[1].CO) == (co_a, co_b)


@pytest.mark.parametrize("name, cc0, cc1", [("XOR", 5, 4), ("XNOR", 4, 5)])
def test_parity_gate_scoap(name, cc0, cc1):
    gate = make_gate(name, [A, B])
    gate.CO = 10
    gate.eval_cc()
    gate.eval_co()
    # inputs differ: min(a1+b0, a0+b1) = min(7, 3), plus 1  -> 4
    # inputs equal:  min(a0+b0, a1+b1) = min(6, 4), plus 1  -> 5
    assert (gate.CC0, gate.CC1) == (cc0, cc1)
    assert gate.unodes[0].CO == min(4, 1) + 10 + 1
    assert gate.unodes[1].CO == min(2, 3) + 10 + 1


def test_parity_gate_scoap_needs_two_inputs():
    gate = make_gate("XOR", [A, B, A])
    with pytest.raises(NotImplementedError, match="3 inputs"):
        gate.eval_cc()


@pytest.mark.parametrize("name, cc0, cc1", [
    ("AND", 1 + 1, 1 + 1 + 2 + 3),         # 0: easiest input at 0; 1: all inputs at 1
    ("NOR", 1 + 1, 1 + 1 + 2 + 3),         # 1 needs all at 0; 0 needs the easiest at 1
])
def test_three_input_gate_scoap(name, cc0, cc1):
    # every input has CC0 == CC1, so AND and NOR give the same numbers
    gate = make_gate(name, [cc(1, 1), cc(2, 2), cc(3, 3)])
    gate.CO = 0
    gate.eval_cc()
    gate.eval_co()
    assert (gate.CC0, gate.CC1) == (cc0, cc1)
    # observing an input needs every other input non-controlling
    assert [u.CO for u in gate.unodes] == [2 + 3 + 1, 1 + 3 + 1, 1 + 2 + 1]


def test_single_input_gates_scoap():
    buff = make_gate("BUFF", [A])
    buff.CO = 10
    buff.eval_cc()
    buff.eval_co()
    assert (buff.CC0, buff.CC1, buff.unodes[0].CO) == (3, 4, 11)

    inv = make_gate("NOT", [A])
    inv.CO = 10
    inv.eval_cc()
    inv.eval_co()
    assert (inv.CC0, inv.CC1, inv.unodes[0].CO) == (4, 3, 11)

    ipt = dft_node.DFTIPT(NodeType.PI, GateType.IPT, "x")
    ipt.eval_cc()
    assert (ipt.CC0, ipt.CC1) == (1, 1)


def test_branch_scoap_copies_controllability_and_stem_takes_best_branch():
    stem = dft_node.DFTNOT(NodeType.GATE, GateType.NOT, "stem")
    stem.CC0, stem.CC1 = 6, 7
    branches = []
    for i, co in enumerate([9, 4, 12]):
        brch = dft_node.DFTBRCH(NodeType.FB, GateType.BRCH, f"b{i}")
        brch.unodes = [stem]
        brch.CO = co
        stem.dnodes.append(brch)
        branches.append(brch)
    for brch in branches:
        brch.eval_cc()
        assert (brch.CC0, brch.CC1) == (6, 7)
    branches[0].eval_co()
    assert stem.CO == 4


# -------------------------------------------------------------------- STAFAN
def stafan_inputs():
    return [{"S": 0.6, "C0": 0.5, "C1": 0.5}, {"S": 0.6, "C0": 0.5, "C1": 0.5}]


@pytest.mark.parametrize("name, out_c, out_b, expected_b0, expected_b1", [
    # AND: B1(u) = B1o*C1o/C1u, B0(u) = B0o*(S - C1o)/C0u
    ("AND", {"C1": 0.25}, {"B1": 0.5, "B0": 0.4}, 0.4 * (0.6 - 0.25) / 0.5, 0.5 * 0.25 / 0.5),
    # NAND: B1(u) = B0o*C0o/C1u, B0(u) = B1o*(S - C0o)/C0u
    ("NAND", {"C0": 0.25}, {"B1": 0.5, "B0": 0.4}, 0.5 * (0.6 - 0.25) / 0.5, 0.4 * 0.25 / 0.5),
    # OR: B0(u) = B0o*C0o/C0u, B1(u) = B1o*(S - C0o)/C1u
    ("OR", {"C0": 0.25}, {"B1": 0.5, "B0": 0.4}, 0.4 * 0.25 / 0.5, 0.5 * (0.6 - 0.25) / 0.5),
    # NOR: B0(u) = B1o*C1o/C0u, B1(u) = B0o*(S - C1o)/C1u
    ("NOR", {"C1": 0.25}, {"B1": 0.5, "B0": 0.4}, 0.5 * 0.25 / 0.5, 0.4 * (0.6 - 0.25) / 0.5),
])
def test_controlled_gate_stafan_b(name, out_c, out_b, expected_b0, expected_b1):
    gate = make_gate(name, stafan_inputs())
    for key, value in {**out_c, **out_b}.items():
        setattr(gate, key, value)
    gate.stafan_b()
    for unode in gate.unodes:
        assert unode.B0 == pytest.approx(expected_b0)
        assert unode.B1 == pytest.approx(expected_b1)


@pytest.mark.parametrize("name", ["XOR", "XNOR", "NOT"])
def test_inverting_and_parity_gates_swap_b0_and_b1(name):
    gate = make_gate(name, [{}])
    gate.B0, gate.B1 = 0.3, 0.8
    gate.stafan_b()
    assert (gate.unodes[0].B0, gate.unodes[0].B1) == (0.8, 0.3)


def test_buffer_copies_b():
    gate = make_gate("BUFF", [{}])
    gate.B0, gate.B1 = 0.3, 0.8
    gate.stafan_b()
    assert (gate.unodes[0].B0, gate.unodes[0].B1) == (0.3, 0.8)


def test_branch_stafan_b_combines_the_branches():
    stem = dft_node.DFTNOT(NodeType.GATE, GateType.NOT, "stem")
    for i, (b0, b1) in enumerate([(0.5, 0.2), (0.5, 0.5)]):
        brch = dft_node.DFTBRCH(NodeType.FB, GateType.BRCH, f"b{i}")
        brch.unodes = [stem]
        brch.B0, brch.B1 = b0, b1
        stem.dnodes.append(brch)
    stem.dnodes[0].stafan_b()
    assert stem.B0 == pytest.approx(1 - 0.5 * 0.5)
    assert stem.B1 == pytest.approx(1 - 0.8 * 0.5)


def test_zero_controllability_gives_an_approximation_and_a_warning():
    # AND: C1 of input 0 is zero, so B1 cannot divide by it
    inputs = [{"S": 0.1, "C0": 1.0, "C1": 0.0}, {"S": 0.1, "C0": 0.5, "C1": 0.5}]
    gate = make_gate("AND", inputs)
    gate.C1, gate.B1, gate.B0 = 0.0, 0.5, 0.4
    with pytest.warns(RuntimeWarning, match="Controllability of node 0"):
        gate.stafan_b()
    # replaced by B1o times the C1 of the other input
    assert gate.unodes[0].B1 == pytest.approx(0.5 * 0.5)


def test_zero_controllability_everywhere_is_an_error():
    inputs = [{"S": 0.1, "C0": 1.0, "C1": 0.0}, {"S": 0.1, "C0": 1.0, "C1": 0.0}]
    gate = make_gate("AND", inputs)
    gate.C1, gate.B1, gate.B0 = 0.0, 0.5, 0.4
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with pytest.raises(ValueError, match="undefined"):
            gate.stafan_b()


# ---------------------------------------------------------------- sensitization
def sensitization(name, other_value):
    gate = make_gate(name, [{"value": 0}, {"value": other_value}])
    return gate.unodes[0].is_sensible()


@pytest.mark.parametrize("name, blocking, passing", [
    ("AND", 0, 1), ("NAND", 0, 1), ("OR", 1, 0), ("NOR", 1, 0)])
def test_controlling_value_on_a_neighbor_blocks_sensitization(name, blocking, passing):
    assert sensitization(name, blocking) is False
    assert sensitization(name, passing) is True


@pytest.mark.parametrize("name", ["XOR", "XNOR"])
def test_parity_gates_always_propagate(name):
    assert sensitization(name, 0) and sensitization(name, 1)


def test_other_cases_of_sensitization():
    assert make_gate("NOT", [{}]).unodes[0].is_sensible()
    assert make_gate("BUFF", [{}]).unodes[0].is_sensible()
    po = dft_node.DFTNOT(NodeType.PO, GateType.NOT, "po")
    assert po.is_sensible()
    dangling = dft_node.DFTNOT(NodeType.GATE, GateType.NOT, "d")
    assert dangling.is_sensible() is False


# ----------------------------------------------------------------------- PFS
def per_bit(name, words, width):
    """Reference: apply the gate to every bit position separately."""
    ref = {"AND": all, "NAND": lambda v: not all(v), "OR": any, "NOR": lambda v: not any(v),
           "XOR": lambda v: sum(v) % 2 == 1, "XNOR": lambda v: sum(v) % 2 == 0}[name]
    result = 0
    for k in range(width):
        result |= int(bool(ref([(w >> k) & 1 for w in words]))) << k
    return result


@pytest.mark.parametrize("name", ["AND", "NAND", "OR", "NOR", "XOR", "XNOR"])
@pytest.mark.parametrize("fanin", [1, 2, 3, 4])
def test_imply_p_is_bit_parallel_logic(name, fanin):
    rng = random.Random(11)
    for _ in range(20):
        words = [rng.getrandbits(64) for _ in range(fanin)]
        gate = make_gate(name, [{"pfs_V": w} for w in words])
        gate.imply_p(gate.bitwise_not)
        assert gate.pfs_V == per_bit(name, words, 64)


def test_imply_p_of_single_input_gates():
    word = random.Random(2).getrandbits(64)
    for name, expected in [("BUFF", word), ("NOT", word ^ (2**64 - 1))]:
        gate = make_gate(name, [{"pfs_V": word}])
        gate.imply_p(gate.bitwise_not)
        assert gate.pfs_V == expected
    brch = dft_node.DFTBRCH(NodeType.FB, GateType.BRCH, "b")
    brch.unodes = [dft_node.DFTIPT(NodeType.PI, GateType.IPT, "s")]
    brch.unodes[0].pfs_V = word
    brch.imply_p(brch.bitwise_not)
    assert brch.pfs_V == word


def test_input_nodes_replicate_the_value_over_all_bits():
    ipt = dft_node.DFTIPT(NodeType.PI, GateType.IPT, "x")
    ipt.imply_p(2**64 - 1, 1)
    assert ipt.pfs_V == 2**64 - 1
    ipt.imply_p(2**64 - 1, 0)
    assert ipt.pfs_V == 0


def test_insert_fault_forces_the_masked_bits():
    gate = make_gate("AND", [{}])
    full = gate.bitwise_not
    gate.pfs_V = 0b1100
    gate.pfs_I = 0b1010          # bits 1 and 3 carry a fault
    gate.insert_f(full, 0b0010)  # stuck values: bit 1 -> 1, bit 3 -> 0
    assert gate.pfs_V == 0b0110


def test_dft_nodes_are_gates_too():
    """A DFT node still evaluates its logic like the plain gate."""
    for name in ["AND", "NAND", "OR", "NOR", "XOR", "XNOR"]:
        for vals in itertools.product([0, 1], repeat=3):
            gate = make_gate(name, [{"value": v} for v in vals])
            gate.imply()
            assert gate.value == int(per_bit(name, list(vals), 1))
