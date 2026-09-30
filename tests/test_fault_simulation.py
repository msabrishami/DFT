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
from pycad.fault_simulation.deductive_fs import DFS
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
    fc, detected = PFS(circuit).run(PATTERNS, faults=faults, log_dir=None)
    assert faults.get_D_count() == oracle_detection_counts(PATTERNS)
    assert fc[-1] == 1.0
    assert sorted(str(f) for f in detected) == sorted(f"{n}@{s}" for n, s in ALL_FAULTS)


def test_pfs_fault_coverage_curve_is_the_oracle_curve():
    circuit = DFTCircuit(C17)
    random.seed(6)
    tps = [PATTERNS[i] for i in random.sample(range(32), 12)]
    fc, _ = PFS(circuit).run(tps, faults="all", log_dir=None)
    seen = set()
    expected = []
    for p in tps:
        seen |= {(n, s) for n, s in ALL_FAULTS if oracle_detects(p, n, s)}
        expected.append(len(seen) / len(ALL_FAULTS))
    assert fc == pytest.approx(expected)


def test_pfs_fault_dropping_does_not_change_the_coverage_curve():
    circuit = DFTCircuit(C17)
    tps = PATTERNS[:20]
    plain, _ = PFS(circuit).run(tps, faults="all", log_dir=None)
    dropped, _ = PFS(circuit).run(tps, faults="all", fault_drop=1, log_dir=None)
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
    PFS(circuit).run(tps, faults=pfs_faults, log_dir=None)
    ppsf_faults = FaultList(circuit, fault_count="all")
    PPSF(circuit).run(tps, faults=ppsf_faults)
    assert pfs_faults.get_D_count() == ppsf_faults.get_D_count()


# --------------------------------------------------- behavior around the simulators
def test_constructing_a_simulator_creates_no_directories(tmp_path):
    circuit = DFTCircuit(C17)
    PFS(circuit)
    PPSF(circuit)
    assert not (tmp_path / "fault_sim").exists()


def test_running_without_log_dir_writes_nothing(tmp_path):
    circuit = DFTCircuit(C17)
    PFS(circuit).run(PATTERNS, faults="all")
    PPSF(circuit).run(PATTERNS, faults="all")
    assert not (tmp_path / "fault_sim").exists()


def test_pfs_logs_are_written_to_the_given_directory(tmp_path):
    circuit = DFTCircuit(C17)
    log_dir = tmp_path / "logs"
    PFS(circuit).run(PATTERNS[:4], faults="all", log_dir=str(log_dir))
    names = sorted(p.name for p in log_dir.iterdir())
    assert names == ["c17-pfs-tp4-f34.log", "c17-pfs-tpfc-tp4-f34.log"]
    text = (log_dir / names[0]).read_text()
    assert "Detected" in text and text.rstrip().endswith("%")


def test_ppsf_log(tmp_path):
    circuit = DFTCircuit(C17)
    PPSF(circuit).run(PATTERNS, faults="all", log_dir=str(tmp_path))
    lines = (tmp_path / "c17_PPSF_f34_tp32.ppsf").read_text().splitlines()
    assert lines[0] == "#TP=32"
    assert len(lines) == 1 + 34 + 1
    assert lines[-1] == "Fault Coverage = 100.0000%"


def test_faults_can_be_given_in_every_supported_form(tmp_path):
    circuit = DFTCircuit(C17)
    sim = PFS(circuit)
    assert len(sim.resolve_faults("all")) == 34
    assert len(sim.resolve_faults(7)) == 7
    assert [str(f) for f in sim.resolve_faults(["3@1", "22@0"])] == ["3@1", "22@0"]
    fault_file = tmp_path / "faults.txt"
    fault_file.write_text("10@0\n11@1\n")
    assert [str(f) for f in sim.resolve_faults(str(fault_file))] == ["10@0", "11@1"]
    own = FaultList(circuit, fault_count=3)
    assert sim.resolve_faults(own) is own
    with pytest.raises(TypeError):
        sim.resolve_faults(2.5)


def test_without_faults_the_simulator_uses_its_list_or_all_faults():
    circuit = DFTCircuit(C17)
    sim = PFS(circuit)
    assert len(sim.resolve_faults(None)) == 34
    sim.fault_list = FaultList(circuit, fault_count=5)
    assert sim.resolve_faults(None) is sim.fault_list
    assert len(PFS(circuit, faults=4).fault_list) == 4


def test_run_resets_detection_counts():
    circuit = DFTCircuit(C17)
    faults = FaultList(circuit, fault_count="all")
    sim = PFS(circuit)
    sim.run(PATTERNS, faults=faults)
    first = faults.get_D_count()
    sim.run(PATTERNS, faults=faults)
    assert faults.get_D_count() == first


def test_fault_dropping_limits_the_detection_count():
    circuit = DFTCircuit(C17)
    faults = FaultList(circuit, fault_count="all")
    PFS(circuit).run(PATTERNS, faults=faults, fault_drop=2)
    assert max(faults.get_D_count().values()) == 2


@pytest.mark.parametrize("sim_class", [PFS, PPSF])
def test_patterns_are_validated(sim_class):
    circuit = DFTCircuit(C17)
    with pytest.raises(ValueError, match="5 inputs"):
        sim_class(circuit).run([[0, 1]], faults="all")
    with pytest.raises(ValueError, match="binary"):
        sim_class(circuit).run([[0, 1, "X", 0, 1]], faults="all")
    with pytest.raises(TypeError):
        sim_class(circuit).run(1.5, faults="all")


def test_ppsf_without_faults_is_an_error():
    circuit = DFTCircuit(C17)
    with pytest.raises(ValueError, match="No fault"):
        PPSF(circuit).run(PATTERNS, faults=FaultList(circuit))


def test_ppsf_single_pass_returns_pattern_indices():
    circuit = DFTCircuit(C17)
    tps = PATTERNS[:10]
    fault = FaultList(circuit, nodes=[circuit.nodes["16"]]).faults[0]
    expected = {j for j, p in enumerate(tps) if oracle_detects(p, fault.node_num, int(fault.stuck_val))}
    assert PPSF(circuit)._one_fault_run(tps, fault) == expected
    with pytest.raises(ValueError, match="64"):
        PPSF(circuit)._one_fault_run(PATTERNS * 3, fault)


def test_random_pattern_count_and_pattern_file_inputs(tmp_path):
    circuit = DFTCircuit(C17)
    pattern_file = tmp_path / "tps.tp"
    pattern_file.write_text("1,2,3,6,7\n" + "\n".join(",".join(map(str, p)) for p in PATTERNS))
    fc_file, _ = PFS(circuit).run(str(pattern_file), faults="all")
    fc_list, _ = PFS(circuit).run(PATTERNS, faults="all")
    assert fc_file == fc_list
    random.seed(3)
    fc_random, _ = PFS(circuit).run(40, faults="all")
    assert len(fc_random) == 40 and fc_random == sorted(fc_random)


# ------------------------------------------------------------ confidence intervals
def test_run_ci_estimates_the_true_detection_probabilities():
    circuit = DFTCircuit(C17)
    exact = {k: v / 32 for k, v in oracle_detection_counts(PATTERNS).items()}
    random.seed(2)
    estimates = PPSF(circuit).run_ci([2000, 2000, 4000], faults="all", num_proc=4, ci=5)
    assert set(estimates) == set(exact)
    for fault, est in estimates.items():
        assert est.mu == pytest.approx(exact[fault], abs=0.04), fault
        assert est.converged and est.tp_count in (2000, 4000, 8000)
        assert sum(est.counts) / (est.tp_count * 4) == pytest.approx(est.mu)


def test_run_ci_is_reproducible_with_the_seed():
    circuit = DFTCircuit(C17)

    def run():
        random.seed(5)
        return PPSF(circuit).run_ci([200, 200], faults="all", num_proc=2)

    assert run() == run()


def test_run_ci_processes_use_different_patterns():
    circuit = DFTCircuit(C17)
    random.seed(1)
    estimates = PPSF(circuit).run_ci([300], faults="all", num_proc=3, ci=1000)
    assert any(len(set(est.counts)) > 1 for est in estimates.values())


def test_run_ci_never_detected_faults_stay_unconverged():
    circuit = DFTCircuit(C17)
    for seed in range(100):  # find a seed whose single pattern misses the fault
        random.seed(seed)
        est = PPSF(circuit).run_ci([1], faults=["22@0"], num_proc=1, ci=1000)["22@0"]
        if est.mu == 0:
            break
    assert est.mu == 0, "no seed gave a pattern that misses 22@0"
    assert not est.converged and est.e_rel == float("inf")
    assert est.counts == (0,) and est.tp_count == 1


def test_run_ci_advanced_mode_needs_a_small_relative_error():
    circuit = DFTCircuit(C17)
    random.seed(3)
    loose = PPSF(circuit).run_ci([500, 500], faults=["10@0"], num_proc=2, ci=1, mode="advanced",
                                 moe=10)
    random.seed(3)
    tight = PPSF(circuit).run_ci([500, 500], faults=["10@0"], num_proc=2, ci=1, mode="advanced",
                                 moe=1e-9)
    assert loose["10@0"].converged and not tight["10@0"].converged
    with pytest.raises(ValueError, match="mode"):
        PPSF(circuit).run_ci([10], faults="all", mode="fancy")


def test_run_ci_log_round_trips_into_the_nodes(tmp_path):
    circuit = DFTCircuit(C17)
    random.seed(7)
    log = str(tmp_path / "ci.ppsf")
    estimates = PPSF(circuit).run_ci([400, 400], faults="all", num_proc=2, ci=2, log_fname=log)
    text = open(log).read()
    assert text.startswith("#TP=400\n") and "### RUNTIME LOG ###" in text

    fresh = DFTCircuit(C17)
    probabilities = PPSF(fresh).load_detection_probabilities(log)
    assert set(probabilities) == set(estimates)
    for fault, est in estimates.items():
        assert probabilities[fault] == pytest.approx(est.mu, rel=1e-3)
    assert fresh.nodes["10"].stat["DP0"] == pytest.approx(probabilities["10@0"])
    assert fresh.nodes["10"].stat["DP1"] == pytest.approx(probabilities["10@1"])


def test_run_ci_for_the_faults_in_the_fan_in_cone_of_a_node():
    from pycad import utils
    circuit = DFTCircuit(C17)
    cone = utils.get_fanin_BFS(circuit, circuit.nodes["22"], 1)
    faults = FaultList(nodes=cone)
    random.seed(1)
    estimates = PPSF(circuit).run_ci([300], faults=faults, num_proc=2)
    assert {k.split("@")[0] for k in estimates} == {n.num for n in cone}


# ------------------------------------------------------------------------ DFS
def test_dfs_detects_exactly_the_oracle_faults_for_every_pattern():
    circuit = Circuit(C17)  # a plain circuit is enough
    dfs = DFS(circuit)
    for pattern in PATTERNS:
        expected = {f"{n}@{s}" for n, s in ALL_FAULTS if oracle_detects(pattern, n, s)}
        assert dfs.single(pattern) == expected, pattern


def test_dfs_run_matches_the_oracle_counts():
    circuit = Circuit(C17)
    faults = FaultList(circuit, fault_count="all")
    fc, detected = DFS(circuit).run(PATTERNS, faults=faults)
    assert faults.get_D_count() == oracle_detection_counts(PATTERNS)
    assert fc[-1] == 1.0 and len(detected) == 34


@pytest.mark.parametrize("name", ["c17", "add2", "FA", "FA_NAND", "cmini", "x3mult", "c432", "c499"])
def test_dfs_agrees_with_pfs(name):
    """Two different algorithms, same detected faults (the circuits include XOR gates)."""
    circuit = DFTCircuit(os.path.join(config.CKT_DIR, f"{name}.ckt"))
    rng = random.Random(31)
    tps = [[rng.randint(0, 1) for _ in circuit.inputs] for _ in range(25)]
    pfs_faults = FaultList(circuit, fault_count="all")
    dfs_faults = FaultList(circuit, fault_count="all")
    pfs_fc, _ = PFS(circuit).run(tps, faults=pfs_faults)
    dfs_fc, _ = DFS(circuit).run(tps, faults=dfs_faults)
    assert dfs_faults.get_D_count() == pfs_faults.get_D_count()
    assert dfs_fc == pytest.approx(pfs_fc)


def test_dfs_reports_only_the_requested_faults():
    circuit = Circuit(C17)
    fc, detected = DFS(circuit).run(PATTERNS, faults=["10@0", "22@1"])
    assert sorted(str(f) for f in detected) == ["10@0", "22@1"]
    assert fc[-1] == 1.0


def test_dfs_log(tmp_path):
    circuit = Circuit(C17)
    DFS(circuit).run(PATTERNS[:3], faults="all", log_dir=str(tmp_path))
    lines = (tmp_path / "c17-dfs-tp3-f34.log").read_text().splitlines()
    assert len(lines) == 3 and lines[0].startswith("    0 \t FC=")


def test_dfs_rejects_bad_patterns():
    with pytest.raises(ValueError):
        DFS(Circuit(C17)).single([1, 0])
