"""SCOAP and STAFAN on whole circuits, checked against hand-worked and brute-force oracles."""
import math
import multiprocessing
import os
import random

import pytest
from c17_oracle import C17, PATTERNS, c17_node_values

from pycad import config
from pycad.circuit.dft_circuit import DFTCircuit


@pytest.fixture
def c17():
    return DFTCircuit(C17)


# ---------------------------------------------------------------------- SCOAP
# Worked out by hand from the SCOAP rules for the c17 NAND network (see the module test for gates):
#   inputs and their branches: CC0 = CC1 = 1; N10 = NAND(1, 8): CC0 = 1+1+1 = 3, CC1 = 1+1 = 2; ...
C17_SCOAP = {  # node: (CC0, CC1, CO)
    "1": (1, 1, 5), "2": (1, 1, 6), "3": (1, 1, 5), "6": (1, 1, 7), "7": (1, 1, 6),
    "8": (1, 1, 5), "9": (1, 1, 7),
    "10": (3, 2, 3), "11": (3, 2, 5),
    "14": (3, 2, 5), "15": (3, 2, 5),
    "16": (4, 2, 3), "19": (4, 2, 3),
    "20": (4, 2, 3), "21": (4, 2, 3),
    "22": (5, 4, 0), "23": (5, 5, 0),
}


def test_scoap_of_c17_matches_the_hand_computation(c17):
    c17.scoap()
    assert {n.num: (n.CC0, n.CC1, n.CO) for n in c17.nodes_lev} == C17_SCOAP


def test_scoap_steps_can_run_separately(c17):
    c17.scoap_cc()
    assert all(n.CC0 is not None and n.CO is None for n in c17.nodes_lev)
    c17.scoap_co()
    assert all(n.CO is not None for n in c17.nodes_lev)


def test_scoap_is_defined_for_every_bundled_circuit():
    for name in ["add2", "c432", "c880", "cmini", "FA", "x3mult"]:
        try:
            circuit = DFTCircuit(os.path.join(config.CKT_DIR, f"{name}.ckt"))
            circuit.scoap()
        except NotImplementedError:
            continue  # SCOAP of XOR gates with more than two inputs
        assert all(n.CC0 >= 1 and n.CC1 >= 1 and n.CO >= 0 for n in circuit.nodes_lev), name


# --------------------------------------------------------------------- STAFAN
# node -> the other input of the gate it feeds (the node is sensitized when that input is 1);
# stems and outputs are always sensitized
C17_OTHER_INPUT = {"1": "8", "8": "1", "9": "6", "6": "9", "2": "14", "14": "2",
                   "15": "7", "7": "15", "10": "20", "20": "10", "21": "19", "19": "21"}


def test_stafan_controllability_and_sensitization_with_all_patterns(c17):
    c17.stafan_c(PATTERNS)
    values = [c17_node_values(p) for p in PATTERNS]
    for node in c17.nodes_lev:
        ones = sum(v[node.num] for v in values)
        assert node.C1 == pytest.approx(ones / 32), node.num
        assert node.C0 == pytest.approx(1 - ones / 32), node.num
        if node.num in C17_OTHER_INPUT:
            expected = sum(v[C17_OTHER_INPUT[node.num]] for v in values) / 32
        else:
            expected = 1.0
        assert node.S == pytest.approx(expected), node.num


def test_stafan_observability_follows_the_formulas_on_c17(c17):
    c17.stafan_c(PATTERNS)
    c17.stafan_b()
    n = c17.nodes
    for po in ("22", "23"):
        assert (n[po].B0, n[po].B1) == (1.0, 1.0)
    # NAND(10, 20) = 22 with B(22) = 1:  B1(u) = B0o*C0o/C1u,  B0(u) = B1o*(S_u - C0o)/C0u
    for u in ("10", "20"):
        assert n[u].B1 == pytest.approx(n["22"].C0 / n[u].C1)
        assert n[u].B0 == pytest.approx((n[u].S - n["22"].C0) / n[u].C0)
    # a stem is observable through any of its branches
    b1 = 1 - (1 - n["8"].B1) * (1 - n["9"].B1)
    assert n["3"].B1 == pytest.approx(b1)
    for node in c17.nodes_lev:
        assert 0 <= node.B0 <= 1 and 0 <= node.B1 <= 1, node.num


def test_stafan_c_accepts_counts_files_and_lists(c17, tmp_path):
    random.seed(3)
    c17.stafan_c(50)
    assert c17.nodes["22"].one_count + c17.nodes["22"].zero_count == 50

    pattern_file = tmp_path / "tps.tp"
    pattern_file.write_text("1,2,3,6,7\n" + "\n".join(",".join(map(str, p)) for p in PATTERNS))
    c17.stafan_c(str(pattern_file))
    assert c17.nodes["22"].one_count + c17.nodes["22"].zero_count == 32

    with pytest.raises(TypeError):
        c17.stafan_c(1.5)
    with pytest.raises(ValueError):
        c17.stafan_c([])


def test_stafan_is_reproducible_with_the_global_seed():
    def measures():
        random.seed(21)
        circuit = DFTCircuit(os.path.join(config.CKT_DIR, "c432.ckt"))
        circuit.stafan(200)
        return {n.num: (n.C0, n.C1, n.S, n.B0, n.B1) for n in circuit.nodes_lev}

    first = measures()
    assert measures() == first
    assert all(abs(c0 + c1 - 1) < 1e-12 for c0, c1, *_ in first.values())


def test_stafan_probabilities_never_exceed_one(c17):
    """The number of patterns is exactly tp_count, whatever the number of processes."""
    for tp_count in (7, 100):
        c17.stafan(tp_count)
        assert all(n.C0 + n.C1 == pytest.approx(1) and n.S <= 1 for n in c17.nodes_lev)
        assert all(n.one_count + n.zero_count == tp_count for n in c17.nodes_lev)


@pytest.mark.skipif("fork" not in multiprocessing.get_all_start_methods(),
                    reason="parallel STAFAN needs the fork start method")
def test_parallel_stafan_uses_all_patterns_and_is_reproducible(c17):
    def run():
        random.seed(5)
        c17.stafan(101, num_proc=3)
        return {n.num: (n.one_count, n.zero_count, n.sen_count) for n in c17.nodes_lev}

    first = run()
    assert run() == first
    assert all(ones + zeros == 101 for ones, zeros, _ in first.values())


def test_workers_do_not_repeat_each_others_patterns(c17):
    """Two workers with the same patterns would give counts that are all even."""
    random.seed(8)
    c17.stafan(200, num_proc=2)
    assert any(n.one_count % 2 for n in c17.nodes_lev)


def test_stafan_needs_enough_patterns(c17):
    with pytest.raises(ValueError):
        c17.stafan(2, num_proc=3)


def test_stafan_fc_estimate(c17):
    with pytest.raises(RuntimeError, match="stafan"):
        c17.stafan_fc(10)
    c17.stafan_c(PATTERNS)
    with pytest.raises(RuntimeError):  # B is still missing
        c17.stafan_fc(10)

    random.seed(1)
    c17.stafan(500)
    assert c17.stafan_fc(0) == pytest.approx(0.0)
    coverage = [c17.stafan_fc(t) for t in (1, 5, 20, 100)]
    assert coverage == sorted(coverage)
    assert 0 < coverage[0] < coverage[-1] <= 1


# -------------------------------------------------------------------- file I/O
def test_stafan_file_round_trip(c17, tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STAFAN_DIR", str(tmp_path))
    random.seed(2)
    c17.stafan(64)
    fname = c17.save_stafan()
    assert fname == os.path.join(str(tmp_path), "c17", "c17-tp64.stafan")
    assert open(fname).readline() == "Node,C0,C1,B0,B1,S\n"

    other = DFTCircuit(C17)
    other.load_stafan(fname)
    for a, b in zip(c17.nodes_lev, other.nodes_lev, strict=True):
        for name in ("C0", "C1", "B0", "B1", "S"):
            assert getattr(b, name) == pytest.approx(getattr(a, name), rel=1e-6)
    assert other.stafan_fc(50) == pytest.approx(c17.stafan_fc(50), rel=1e-5)


def test_save_stafan_with_a_name_and_before_computing(c17, tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STAFAN_DIR", str(tmp_path))
    with pytest.raises(RuntimeError):
        c17.save_stafan()
    c17.stafan(10)
    assert c17.save_stafan("mine.csv") == os.path.join(str(tmp_path), "c17", "mine.csv")


def test_scoap_file(c17, tmp_path):
    c17.scoap()
    fname = c17.save_scoap(str(tmp_path / "sub" / "scoap.csv"))
    lines = open(fname).read().splitlines()
    assert lines[0] == "Node,CC0,CC1,CO"
    assert len(lines) == 1 + len(c17.nodes)
    assert "22,5,4,0" in lines


def test_graph_with_measures_round_trips_through_gml(c17, tmp_path):
    random.seed(4)
    c17.scoap()
    c17.stafan(50)
    graph = c17.gen_graph()
    assert graph.nodes["22"]["CC0"] == 5 and graph.nodes["22"]["B1"] == 1.0
    assert graph.nodes["10"]["gtype"] == "NAND" and graph.nodes["10"]["lev"] == 2
    assert graph.number_of_edges() == sum(len(n.unodes) for n in c17.nodes.values())

    fname = str(tmp_path / "c17.gml")
    c17.write_graph(fname)
    loaded = DFTCircuit.read_graph(fname)
    assert set(loaded.nodes) == set(c17.nodes)
    assert loaded.nodes["22"]["CC1"] == 4
    assert loaded.nodes["10"]["C1"] == pytest.approx(graph.nodes["10"]["C1"])


def test_print_measures(c17, capsys):
    c17.scoap()
    c17.print_measures()
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].split("\t")[:3] == ["N", "LEV", "GATE"]
    assert len(lines) == 1 + len(c17.nodes)


@pytest.mark.skipif("fork" not in multiprocessing.get_all_start_methods(),
                    reason="parallel STAFAN needs the fork start method")
def test_parallel_stafan_on_a_circuit_too_deep_to_pickle():
    random.seed(1)
    circuit = DFTCircuit(os.path.join(config.CKT_DIR, "c6288.ckt"))
    with pytest.warns(RuntimeWarning, match="approximated"):
        circuit.stafan(60, num_proc=2)
    assert all(n.one_count + n.zero_count == 60 for n in circuit.nodes_lev)


# ------------------------------------------------------ regression tests (review)
DANGLING = """\
1 1 0 1 0
1 2 0 2 0
1 3 0 1 0
2 7 1 2
2 8 1 2
0 5 7 0 2 1 7
3 6 3 0 2 8 3
"""  # AND(1, 7) drives nothing; the only output is OR(8, 3)


def test_logic_that_reaches_no_output_is_unobservable_not_a_crash(tmp_path):
    netlist = tmp_path / "dangling.ckt"
    netlist.write_text(DANGLING)
    circuit = DFTCircuit(str(netlist))
    circuit.scoap()
    assert circuit.nodes["5"].CO == math.inf and circuit.nodes["1"].CO == math.inf
    assert circuit.nodes["2"].CO < math.inf   # observable through its other branch

    random.seed(1)
    circuit.stafan(200)
    assert (circuit.nodes["5"].B0, circuit.nodes["5"].B1) == (0.0, 0.0)
    assert (circuit.nodes["1"].B0, circuit.nodes["1"].B1) == (0.0, 0.0)
    assert circuit.nodes["2"].B1 > 0


def test_a_primary_output_with_fan_out_keeps_observability_zero(tmp_path):
    netlist = tmp_path / "po_fanout.ckt"
    netlist.write_text("1 1 0 1 0\n1 2 0 1 0\n"
                       "3 3 7 2 2 1 2\n"       # AND, a primary output ...
                       "2 4 1 3\n2 5 1 3\n"   # ... that also feeds two branches
                       "3 6 5 0 1 4\n3 7 5 0 1 5\n")
    circuit = DFTCircuit(str(netlist))
    circuit.scoap()
    assert circuit.nodes["3"].CO == 0
    assert circuit.nodes["1"].CO == circuit.nodes["2"].cc(1) + 0 + 1  # AND with CO 0


def test_stafan_b_after_stafan_c_enables_the_fault_coverage_estimate(c17):
    with pytest.raises(RuntimeError, match="stafan_c"):
        c17.stafan_b()
    c17.stafan_c(PATTERNS)
    c17.stafan_b()
    assert 0 < c17.stafan_fc(5) < 1
