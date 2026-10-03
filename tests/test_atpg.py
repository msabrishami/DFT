"""ATPG: every generated test is checked by fault simulation, redundancy by exhaustion."""
import itertools
import os
import random

import pytest

from pycad import config
from pycad.atpg import DAlgorithm, Podem, fill_x
from pycad.atpg.base import eval_gate
from pycad.atpg.dalg import imply_gate
from pycad.circuit.circuit import Circuit
from pycad.config import X_VALUE
from pycad.fault_simulation.fault import Fault, FaultList
from pycad.node import node as node_mod

ALGORITHMS = [Podem, DAlgorithm]


def ckt(name):
    return Circuit(os.path.join(config.CKT_DIR, f"{name}.ckt"))


def detecting_patterns(circuit, fault):
    """Brute force: all input patterns that detect ``fault``."""
    found = []
    for pattern in itertools.product((0, 1), repeat=len(circuit.inputs)):
        good = circuit.logic_sim_bitwise(list(pattern))
        faulty = circuit.logic_sim_bitwise(list(pattern), fault)
        if any((g ^ f) & 1 for g, f in zip(good, faulty, strict=True)):
            found.append(pattern)
    return found


@pytest.fixture(scope="module")
def c17():
    return ckt("c17")


@pytest.fixture
def redundant_circuit(tmp_path):
    # z = a AND (a OR b) = a, so b stuck-at anything cannot be observed
    netlist = tmp_path / "red.v"
    netlist.write_text("module t (a, b, z);\n  input a, b;\n  output z;\n  wire w;\n"
                       "  or g1 (w, a, b);\n  and g2 (z, a, w);\nendmodule\n")
    return Circuit(str(netlist))


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_every_c17_fault_gets_a_test_that_detects_it(c17, algorithm):
    atpg = algorithm(c17)
    for fault in FaultList(c17, fault_count="all"):
        result = atpg.generate(fault)
        assert result.status == "detected", fault
        assert len(result.pattern) == len(c17.inputs)
        # whatever the unspecified inputs are, the fault is detected
        for value in (0, 1):
            assert atpg.detects(fill_x(result.pattern, value), fault), (fault, value)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_redundant_faults_are_proved_redundant(redundant_circuit, algorithm):
    atpg = algorithm(redundant_circuit)
    for fault in ("b@0", "b@1"):
        assert detecting_patterns(redundant_circuit, Fault.from_str(fault)) == []
        assert atpg.generate(fault).status == "redundant"
    assert atpg.generate("a@0").status == "detected"
    assert atpg.generate("z@1").status == "detected"


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_status_agrees_with_exhaustive_search_on_a_small_circuit(redundant_circuit, algorithm):
    atpg = algorithm(redundant_circuit)
    for fault in FaultList(redundant_circuit, fault_count="all"):
        testable = bool(detecting_patterns(redundant_circuit, fault))
        assert (atpg.generate(fault).status == "detected") == testable, fault


@pytest.mark.parametrize("name", ["c432", "c880"])
@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_random_faults_of_larger_circuits(name, algorithm):
    circuit = ckt(name)
    atpg = algorithm(circuit, backtrack_limit=200)
    faults = FaultList(circuit)
    faults.add_n_random(40, rng=random.Random(7))
    seen = set()
    for fault in faults:
        result = atpg.generate(fault)
        seen.add(result.status)
        if result.status == "detected":
            assert atpg.detects(fill_x(result.pattern, 0), fault), fault
    assert "detected" in seen


def test_algorithms_agree_on_testability(c17, redundant_circuit):
    for circuit in (c17, redundant_circuit):
        podem, dalg = Podem(circuit), DAlgorithm(circuit)
        for fault in FaultList(circuit, fault_count="all"):
            assert podem.generate(fault).status == dalg.generate(fault).status, fault


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_backtrack_limit_is_exact(redundant_circuit, algorithm):
    """A search that needs n backtracks succeeds with limit n and aborts with n - 1."""
    needed = algorithm(redundant_circuit, backtrack_limit=1000).generate("b@0")
    assert needed.status == "redundant" and needed.backtracks > 0
    exact = algorithm(redundant_circuit, backtrack_limit=needed.backtracks).generate("b@0")
    assert exact.status == "redundant"
    short = algorithm(redundant_circuit, backtrack_limit=needed.backtracks - 1).generate("b@0")
    assert short.status == "aborted"


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_detects_rejects_unspecified_inputs(c17, algorithm):
    atpg = algorithm(c17)
    pattern = atpg.generate("10@0").pattern
    if X_VALUE in pattern:
        with pytest.raises(ValueError, match="unspecified"):
            atpg.detects(pattern, "10@0")


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_generate_test_set_covers_c17(c17, algorithm):
    atpg = algorithm(c17)
    test_set = atpg.generate_test_set(fill=0)
    assert not test_set.redundant and not test_set.aborted
    assert len(test_set.detected) == 2 * len(c17.nodes)
    assert test_set.coverage(2 * len(c17.nodes)) == 1.0
    assert len(test_set.patterns) < len(test_set.detected)  # fault dropping
    for fault in FaultList(c17, fault_count="all"):
        assert any(atpg.detects(p, fault) for p in test_set.patterns), fault


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_unknown_node_is_rejected(c17, algorithm):
    with pytest.raises(ValueError, match="not in circuit"):
        algorithm(c17).generate("nope@0")


def test_fill_x():
    assert fill_x([0, X_VALUE, 1, X_VALUE], 1) == [0, 1, 1, 1]
    filled = fill_x([X_VALUE] * 20, rng=random.Random(1))
    assert set(filled) == {0, 1}


@pytest.mark.parametrize("gtype", ["AND", "NAND", "OR", "NOR", "XOR", "XNOR", "NOT", "BUFF"])
def test_implication_agrees_with_three_valued_logic(gtype):
    """Every implied value is forced by the given ones; complete inputs give the output."""
    fanin = 1 if gtype in ("NOT", "BUFF") else 3
    circuit_gate = getattr(node_mod, gtype)("GATE", gtype, "g")
    values = (0, 1, X_VALUE)
    for ins in itertools.product(values, repeat=fanin):
        for out in values:
            result = imply_gate(circuit_gate, ins, out)
            completions = [
                c for c in itertools.product((0, 1), repeat=fanin)
                if all(i in (X_VALUE, v) for i, v in zip(ins, c, strict=True))
                and out in (X_VALUE, eval_gate_with(circuit_gate, c))]
            if not completions:
                assert result is None, (ins, out)
                continue
            assert result is not None, (ins, out)
            new_ins, new_out = result
            # complete for what is forced: a value all completions share is implied
            for k in range(fanin):
                shared = {c[k] for c in completions}
                if len(shared) == 1 and fanin == 1:
                    assert new_ins[k] == shared.pop(), (ins, out)
            # sound: every completion agrees with what was implied
            for c in completions:
                assert all(n in (X_VALUE, v) for n, v in zip(new_ins, c, strict=True))
                assert new_out in (X_VALUE, eval_gate_with(circuit_gate, c))


def eval_gate_with(gate, ins):
    return eval_gate(gate, list(ins))


def random_circuit(tmp_path, seed):
    rng = random.Random(seed)
    signals = [f"i{k}" for k in range(5)]
    gates = []
    for g in range(9):
        kind = rng.choice(["and", "nand", "or", "nor", "xor", "xnor", "not"])
        fanin = 1 if kind == "not" else rng.choice([2, 2, 3])
        ins = rng.sample(signals, fanin)
        out = f"n{g}"
        gates.append(f"  {kind} g{g} ({out}, {', '.join(ins)});")
        signals.append(out)
    outputs = ["n7", "n8"]
    text = (f"module t ({', '.join(signals[:5] + outputs)});\n"
            f"  input {', '.join(signals[:5])};\n  output {', '.join(outputs)};\n"
            f"  wire {', '.join(s for s in signals[5:] if s not in outputs)};\n"
            + "\n".join(gates) + "\nendmodule\n")
    path = tmp_path / f"r{seed}.v"
    path.write_text(text)
    return Circuit(str(path))


@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("seed", range(12))
def test_random_circuits_match_exhaustive_search(tmp_path, algorithm, seed):
    circuit = random_circuit(tmp_path, seed)
    atpg = algorithm(circuit, backtrack_limit=10_000)
    for fault in FaultList(circuit, fault_count="all"):
        testable = bool(detecting_patterns(circuit, fault))
        result = atpg.generate(fault)
        assert result.status == ("detected" if testable else "redundant"), (seed, fault)
        if testable:
            assert atpg.detects(fill_x(result.pattern, 0), fault), (seed, fault)
