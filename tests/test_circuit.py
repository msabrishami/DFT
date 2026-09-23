"""Behavior of Circuit: levelization, backward distances, simulation and file output."""
import os
import warnings

import networkx as nx
import pytest

from pycad import config
from pycad.circuit.circuit import Circuit
from pycad.circuit.circuit_loader import CircuitLoader
from pycad.fault_simulation.fault import Fault
from pycad.node import node

C17 = os.path.join(config.CKT_DIR, "c17.ckt")


def test_levelize_can_be_repeated():
    circuit = Circuit(C17)
    before = [(n.num, n.lev) for n in circuit.nodes_lev]
    circuit.levelize()
    assert [(n.num, n.lev) for n in circuit.nodes_lev] == before


def test_levelize_recomputes_levels_after_a_change():
    circuit = Circuit(C17)
    out = circuit.outputs[0]
    stem = out.unodes[0]
    # put an extra buffer between the output and its first fan-in
    buff = node.BUFF("GATE", "BUFF", "extra")
    CircuitLoader.insert_branch(stem, out, buff)
    circuit.nodes[buff.num] = buff
    circuit.levelize()
    assert buff.lev == stem.lev + 1
    assert out.lev == max(u.lev for u in out.unodes) + 1
    assert out.lev >= buff.lev + 1
    assert [n.lev for n in circuit.nodes_lev] == sorted(n.lev for n in circuit.nodes.values())


def test_levelize_rejects_combinational_loops():
    circuit = Circuit(C17)
    first_gate = next(n for n in circuit.nodes_lev if n.ntype == "GATE")
    last_gate = circuit.outputs[0]
    first_gate.unodes.append(last_gate)  # feedback
    last_gate.dnodes.append(first_gate)
    with pytest.raises(ValueError, match="loop"):
        circuit.levelize()


def test_node_without_fanin_is_reported_and_put_at_level_zero():
    circuit = Circuit(C17)
    gate = next(n for n in circuit.nodes_lev if n.ntype == "GATE")
    for unode in gate.unodes:
        unode.dnodes.remove(gate)
    gate.unodes = []
    with pytest.warns(UserWarning, match="no fan-in"):
        circuit.levelize()
    assert gate.lev == 0


def test_levelize_is_silent_for_a_normal_circuit():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        Circuit(C17)


@pytest.mark.parametrize("name", ["c17", "c432"])
def test_levelize_backward_matches_networkx(name):
    circuit = Circuit(os.path.join(config.CKT_DIR, f"{name}.ckt"))
    dist = circuit.levelize_backward()
    graph = circuit.gen_graph()
    assert set(dist) == set(circuit.nodes.values())
    for n in circuit.nodes.values():
        lengths = [nx.shortest_path_length(graph, n.num, po.num)
                   for po in circuit.outputs if nx.has_path(graph, n.num, po.num)]
        assert dist[n] == min(lengths)


def test_levelize_backward_marks_dangling_logic():
    circuit = Circuit(C17)
    dangling = node.NOT("GATE", "NOT", "dangling")
    stem = circuit.inputs[0]
    dangling.unodes.append(stem)  # driven, but drives nothing
    circuit.nodes[dangling.num] = dangling
    assert circuit.levelize_backward()[dangling] == float("inf")


def test_get_rand_nodes_samples_without_repetition():
    circuit = Circuit(C17)
    picked = circuit.get_rand_nodes(len(circuit.nodes))
    assert sorted(n.num for n in picked) == sorted(circuit.nodes)
    assert len(circuit.get_rand_nodes()) == 1
    with pytest.raises(ValueError):
        circuit.get_rand_nodes(len(circuit.nodes) + 1)


# ----------------------------------------------------------------- simulation
ALL_C17_PATTERNS = [[(p >> i) & 1 for i in range(5)] for p in range(32)]


def test_logic_sim_rejects_wrong_pattern_length_and_x():
    circuit = Circuit(C17)
    with pytest.raises(ValueError, match="5 inputs"):
        circuit.logic_sim([0, 1, 0])
    with pytest.raises(ValueError, match="X"):
        circuit.logic_sim([0, 1, "X", 0, 1])


def test_ternary_sim_agrees_with_binary_sim_on_known_values():
    circuit = Circuit(C17)
    for pattern in ALL_C17_PATTERNS:
        assert circuit.logic_sim_t(pattern) == circuit.logic_sim(pattern)


def test_ternary_sim_propagates_unknowns_only_when_needed():
    circuit = Circuit(C17)
    # input 3 at 0 forces both gates fed by it to 1, so output 22 depends on the others
    outputs = circuit.logic_sim_t([1, 1, "X", 1, 1])
    assert "X" in outputs
    # N10 = NAND(1, 3) and N11 = NAND(3, 6) are unknown, then N16 = NAND(2, 11) too,
    # but with 1=0, N10 = 1 whatever 3 is, and with 2=0, N16 = 1: N22 = NAND(1, 1) = 0
    assert circuit.logic_sim_t([0, 0, "X", "X", "X"])[0] == 0


def test_bitwise_sim_is_64_independent_simulations():
    circuit = Circuit(C17)
    width = circuit.nodes_lev[0].bitlen
    words = [0] * 5
    patterns = [ALL_C17_PATTERNS[k % 32] for k in range(width)]
    for k, pattern in enumerate(patterns):
        for i, bit in enumerate(pattern):
            words[i] |= bit << k
    packed = circuit.logic_sim_bitwise(words)
    for k, pattern in enumerate(patterns):
        expected = circuit.logic_sim(pattern)
        assert [(word >> k) & 1 for word in packed] == expected


@pytest.mark.parametrize("stuck", ["0", "1"])
def test_bitwise_sim_with_a_fault_matches_hand_derived_c17(stuck):
    """Fault on N16 (the stem feeding branches 20 and 21), computed from the c17 equations."""
    circuit = Circuit(C17)
    words = [0] * 5
    for k, pattern in enumerate(ALL_C17_PATTERNS):
        for i, bit in enumerate(pattern):
            words[i] |= bit << k
    faulty = circuit.logic_sim_bitwise(words, Fault("16", stuck))

    def nand(a, b):
        return 1 - (a & b)

    for k, (n1, _n2, n3, n6, n7) in enumerate(ALL_C17_PATTERNS):
        n10, n11 = nand(n1, n3), nand(n3, n6)
        n16 = int(stuck)
        n19 = nand(n11, n7)
        expected = [nand(n10, n16), nand(n16, n19)]
        assert [(word >> k) & 1 for word in faulty] == expected, (k, stuck)


# ---------------------------------------------------------------- file output
def write_patterns(path, patterns):
    with open(path, "w") as f:
        f.write("1,2,3,6,7\n")
        for pattern in patterns:
            f.write(",".join(map(str, pattern)) + "\n")


def test_logic_sim_file_and_golden_check_round_trip(tmp_path):
    circuit = Circuit(C17)
    pattern_file = tmp_path / "tp.csv"
    result_file = tmp_path / "result.txt"
    write_patterns(pattern_file, ALL_C17_PATTERNS)
    circuit.logic_sim_file(pattern_file, result_file)

    lines = result_file.read_text().splitlines()
    assert lines[:2] == ["Inputs: N1,N2,N3,N6,N7", "Outputs: N22,N23"]
    assert lines[2] == "Test # = 1"
    assert len(lines) == 2 + 3 * 32
    assert circuit.check_golden(result_file)


def test_golden_check_detects_a_wrong_response(tmp_path):
    circuit = Circuit(C17)
    pattern_file = tmp_path / "tp.csv"
    result_file = tmp_path / "result.txt"
    write_patterns(pattern_file, ALL_C17_PATTERNS[:4])
    circuit.logic_sim_file(pattern_file, result_file)
    lines = result_file.read_text().splitlines()
    lines[4] = "0,0" if lines[4] != "0,0" else "1,1"
    result_file.write_text("\n".join(lines) + "\n")
    assert not circuit.check_golden(result_file)


def test_golden_check_detects_a_different_input_order(tmp_path):
    circuit = Circuit(C17)
    result_file = tmp_path / "result.txt"
    result_file.write_text("Inputs: N2,N1,N3,N6,N7\nOutputs: N22,N23\n")
    assert not circuit.check_golden(result_file)


def test_write_stil(tmp_path):
    circuit = Circuit(C17)
    pattern_file = tmp_path / "tp.csv"
    stil_file = tmp_path / "out.stil"
    write_patterns(pattern_file, [[1, 1, 1, 1, 1], [0, 0, 0, 0, 0]])
    circuit.write_stil(pattern_file, stil_file)
    text = stil_file.read_text()
    assert text.startswith("PI:1,2,3,6,7\nPO:22,23\n")
    assert '"pattern 0": Call "capture" {' in text
    assert '"_pi"=11111;' in text
    # c17 with all ones: N10=0, N11=0, N16=1, N19=1, N22=1, N23=0
    assert '"_po"=HL;' in text
    assert '"_pi"=00000;' in text


# --------------------------------------------------------------------- helpers
def test_gen_graph_mirrors_the_connections():
    circuit = Circuit(C17)
    graph = circuit.gen_graph()
    assert graph.number_of_nodes() == len(circuit.nodes)
    assert nx.is_directed_acyclic_graph(graph)
    for n in circuit.nodes.values():
        assert set(graph.predecessors(n.num)) == {u.num for u in n.unodes}
        assert graph.nodes[n.num]["lev"] == n.lev
        assert graph.nodes[n.num]["gtype"] == n.gtype


def test_make_num_int_and_get_node_attr_follow_level_order():
    circuit = Circuit(C17)
    numbering = circuit.make_num_int()
    assert sorted(numbering.values()) == list(range(len(circuit.nodes)))
    assert [circuit.nodes_lev[i].num for i in numbering.values()] == list(numbering)
    assert circuit.get_node_attr("lev") == [n.lev for n in circuit.nodes_lev]


def test_read_outputs_and_str():
    circuit = Circuit(C17)
    circuit.logic_sim([1, 1, 1, 1, 1])
    assert circuit.read_outputs() == {"22": 1, "23": 0}
    text = str(circuit)
    assert text.startswith("Circuit name: c17\n#Nodes: 17")
    assert "#PI: 5" in text and "#PO: 2" in text
