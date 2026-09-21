"""Behavior of Circuit: levelization, backward distances, simulation and file output."""
import os
import warnings

import networkx as nx
import pytest

from pycad import config
from pycad.circuit.circuit import Circuit
from pycad.circuit.circuit_loader import CircuitLoader
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
