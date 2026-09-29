"""PFS and PPSF against a brute-force oracle written independently of the library.

The oracle is a plain dictionary simulation of c17 from its gate equations in which a
node can be forced to a constant. A fault is detected by a pattern if forcing the node
changes at least one of the outputs.
"""
import itertools
import os
import random

import pytest

from pycad import config
from pycad.circuit.circuit import Circuit
from pycad.circuit.dft_circuit import DFTCircuit
from pycad.fault_simulation.fault import FaultList
from pycad.fault_simulation.pfs import PFS
from pycad.fault_simulation.ppsf import PPSF

C17 = os.path.join(config.CKT_DIR, "c17.ckt")
PATTERNS = [list(p) for p in itertools.product([0, 1], repeat=5)]  # inputs 1, 2, 3, 6, 7
NODES = ["1", "2", "3", "6", "7", "8", "9", "10", "11", "14", "15", "16", "19", "20", "21",
         "22", "23"]


@pytest.fixture(autouse=True)
def fault_sim_in_tmp(tmp_path, monkeypatch):
    """Keep every file the simulators write out of the repository."""
    monkeypatch.setattr(config, "FAULT_SIM_DIR", str(tmp_path / "fault_sim"))


def nand(a, b):
    return 1 - (a & b)


def oracle_outputs(pattern, forced=None):
    """Outputs [22, 23] of c17; ``forced`` = (node, value) overrides that node's value."""
    v = {}

    def put(node, value):
        v[node] = forced[1] if forced and forced[0] == node else value

    for node, value in zip(["1", "2", "3", "6", "7"], pattern, strict=True):
        put(node, value)
    put("8", v["3"])
    put("9", v["3"])
    put("10", nand(v["1"], v["8"]))
    put("11", nand(v["9"], v["6"]))
    put("14", v["11"])
    put("15", v["11"])
    put("16", nand(v["2"], v["14"]))
    put("20", v["16"])
    put("21", v["16"])
    put("19", nand(v["15"], v["7"]))
    put("22", nand(v["10"], v["20"]))
    put("23", nand(v["21"], v["19"]))
    return [v["22"], v["23"]]


def oracle_detects(pattern, node, stuck):
    return oracle_outputs(pattern) != oracle_outputs(pattern, (node, stuck))


ALL_FAULTS = [(n, s) for n in NODES for s in (0, 1)]


def oracle_detection_counts(patterns):
    return {f"{n}@{s}": sum(oracle_detects(p, n, s) for p in patterns) for n, s in ALL_FAULTS}


def test_the_oracle_agrees_with_the_library_logic():
    circuit = Circuit(C17)
    for p in PATTERNS:
        assert circuit.logic_sim(p) == oracle_outputs(p)


def test_every_c17_fault_is_detectable():
    counts = oracle_detection_counts(PATTERNS)
    assert all(count > 0 for count in counts.values())


# ------------------------------------------------------------------------ PFS
def test_pfs_detects_exactly_the_oracle_faults_for_every_pattern():
    circuit = DFTCircuit(C17)
    sim = PFS(circuit)
    sim.fault_list = FaultList(circuit, fault_count="all")
    for pattern in PATTERNS:
        detected = {str(f) for f in sim._one_tp_run(pattern)}
        expected = {f"{n}@{s}" for n, s in ALL_FAULTS if oracle_detects(pattern, n, s)}
        assert detected == expected, pattern


def test_pfs_run_counts_detections_like_the_oracle():
    circuit = DFTCircuit(C17)
    faults = FaultList(circuit, fault_count="all")
    fc, detected = PFS(circuit).run(PATTERNS, faults=faults, save_log=False)
    assert faults.get_D_count() == oracle_detection_counts(PATTERNS)
    assert fc[-1] == 1.0
    assert sorted(str(f) for f in detected) == sorted(f"{n}@{s}" for n, s in ALL_FAULTS)


def test_pfs_fault_coverage_curve_is_the_oracle_curve():
    circuit = DFTCircuit(C17)
    random.seed(6)
    tps = [PATTERNS[i] for i in random.sample(range(32), 12)]
    fc, _ = PFS(circuit).run(tps, faults="all", save_log=False)
    seen = set()
    expected = []
    for p in tps:
        seen |= {(n, s) for n, s in ALL_FAULTS if oracle_detects(p, n, s)}
        expected.append(len(seen) / len(ALL_FAULTS))
    assert fc == pytest.approx(expected)


def test_pfs_fault_dropping_does_not_change_the_coverage_curve():
    circuit = DFTCircuit(C17)
    tps = PATTERNS[:20]
    plain, _ = PFS(circuit).run(tps, faults="all", save_log=False)
    dropped, _ = PFS(circuit).run(tps, faults="all", fault_drop=1, save_log=False)
    assert dropped == pytest.approx(plain)


def test_pfs_with_more_faults_than_fit_in_one_word():
    """c432 has more than 63 faults, so several passes are needed per pattern."""
    circuit = DFTCircuit(os.path.join(config.CKT_DIR, "c432.ckt"))
    sim = PFS(circuit)
    sim.fault_list = FaultList(circuit, fault_count="all")
    assert len(sim.fault_list) > 63 * 5
    pattern = [random.Random(3).randint(0, 1) for _ in circuit.inputs]
    detected = {str(f) for f in sim._one_tp_run(pattern)}
    for fault in random.Random(4).sample(sim.fault_list.faults, 40):
        good = circuit.logic_sim(pattern)
        full = circuit.nodes_lev[0].bitwise_not
        faulty = [value & 1 for value in
                  circuit.logic_sim_bitwise([v * full for v in pattern], fault)]
        assert (good != faulty) == (str(fault) in detected), str(fault)


# ----------------------------------------------------------------------- PPSF
def test_ppsf_counts_detections_like_the_oracle():
    circuit = DFTCircuit(C17)
    faults = FaultList(circuit, fault_count="all")
    result = PPSF(circuit).run(PATTERNS, faults=faults)
    assert faults.get_D_count() == oracle_detection_counts(PATTERNS)
    assert result == {k: v for k, v in oracle_detection_counts(PATTERNS).items() if v}


def test_ppsf_handles_more_patterns_than_one_word():
    circuit = DFTCircuit(C17)
    rng = random.Random(9)
    tps = [PATTERNS[rng.randrange(32)] for _ in range(150)]  # 3 passes of at most 64
    faults = FaultList(circuit, fault_count="all")
    PPSF(circuit).run(tps, faults=faults)
    assert faults.get_D_count() == oracle_detection_counts(tps)


def test_pfs_and_ppsf_agree_on_c432():
    circuit = DFTCircuit(os.path.join(config.CKT_DIR, "c432.ckt"))
    random.seed(12)
    tps = [[random.randint(0, 1) for _ in circuit.inputs] for _ in range(70)]
    pfs_faults = FaultList(circuit, fault_count="all")
    PFS(circuit).run(tps, faults=pfs_faults, save_log=False)
    ppsf_faults = FaultList(circuit, fault_count="all")
    PPSF(circuit).run(tps, faults=ppsf_faults)
    assert pfs_faults.get_D_count() == ppsf_faults.get_D_count()
