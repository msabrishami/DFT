"""Fault and FaultList."""
import os
import random

import pytest

from pycad import config
from pycad.circuit.circuit import Circuit
from pycad.fault_simulation.fault import Fault, FaultList


@pytest.fixture(scope="module")
def c17():
    return Circuit(os.path.join(config.CKT_DIR, "c17.ckt"))


def test_fault_text_form():
    fault = Fault(23, 1)
    assert (fault.node_num, fault.stuck_val) == ("23", "1")
    assert str(fault) == "23@1" == repr(fault)
    parsed = Fault.from_str(" 7@0\n")
    assert (parsed.node_num, parsed.stuck_val) == ("7", "0")
    assert parsed.D_count == 0 and parsed.D_count_list == []


def test_all_faults_of_a_circuit(c17):
    faults = FaultList(c17, fault_count="all")
    assert len(faults) == 2 * len(c17.nodes) == 34
    assert {str(f) for f in faults} == {f"{n}@{v}" for n in c17.nodes for v in (0, 1)}


def test_a_list_from_a_circuit_alone_is_empty(c17):
    assert len(FaultList(c17)) == 0


def test_random_faults_are_different(c17):
    faults = FaultList(c17, fault_count=10)
    assert len(faults) == 10
    assert len({str(f) for f in faults}) == 10
    assert all(f.node_num in c17.nodes and f.stuck_val in "01" for f in faults)


def test_random_faults_can_cover_every_fault_but_not_more(c17):
    assert len({str(f) for f in FaultList(c17, fault_count=34)}) == 34
    with pytest.raises(ValueError, match="34"):
        FaultList(c17, fault_count=35)


def test_random_faults_are_reproducible_with_an_rng(c17):
    def pick(seed):
        faults = FaultList(c17)
        faults.add_n_random(8, rng=random.Random(seed))
        return [str(f) for f in faults]

    assert pick(4) == pick(4)
    assert pick(4) != pick(5)


def test_invalid_fault_count(c17):
    with pytest.raises(ValueError):
        FaultList(c17, fault_count="some")
    with pytest.raises(ValueError, match="circuit"):
        FaultList(fault_count=3)


def test_faults_of_chosen_nodes(c17):
    nodes = [c17.nodes["10"], c17.nodes["22"]]
    assert [str(f) for f in FaultList(nodes=nodes)] == ["10@0", "10@1", "22@0", "22@1"]
    # nodes are honoured together with a circuit too
    assert len(FaultList(c17, nodes=nodes)) == 4


def test_copying_a_list_shares_the_fault_objects(c17):
    original = FaultList(c17, fault_count="all")
    shared = FaultList(fault_list=original)
    assert shared.faults == original.faults
    assert all(a is b for a, b in zip(shared, original, strict=True))


def test_copy_fault_makes_an_independent_fault():
    source = Fault(3, 0)
    source.D_count_list = [1, 2]
    faults = FaultList()
    faults.copy_fault(source)
    copy = faults.faults[0]
    assert copy is not source and str(copy) == "3@0"
    copy.D_count_list.append(3)
    assert source.D_count_list == [1, 2]


def test_string_input():
    faults = FaultList()
    faults.add_str("1@0")
    faults.add_str_list(["2@1", "3@0"])
    assert [str(f) for f in faults] == ["1@0", "2@1", "3@0"]


def test_file_round_trip(c17, tmp_path):
    faults = FaultList(c17, fault_count=12)
    fname = tmp_path / "faults.txt"
    faults.write_file(fname)
    assert [str(f) for f in FaultList(fname=str(fname))] == [str(f) for f in faults]


def test_file_reading_ignores_blank_lines(tmp_path):
    fname = tmp_path / "faults.txt"
    fname.write_text("1@0\n\n2@1\n")
    assert [str(f) for f in FaultList(fname=str(fname))] == ["1@0", "2@1"]


def test_write_file_extra_lists_the_detection_counts(tmp_path):
    faults = FaultList()
    faults.add(1, 0)
    faults.add(2, 1)
    faults.faults[0].D_count_list = [4, 0, 7]
    fname = tmp_path / "extra.txt"
    faults.write_file_extra(fname)
    assert fname.read_text() == "1@0,4,0,7\n2@1\n"


def test_fault_coverage_and_counts():
    faults = FaultList()
    for num in range(4):
        faults.add(num, 0)
    faults.faults[0].D_count = 3
    faults.faults[2].D_count = 1
    assert faults.calc_fc() == 0.5
    assert faults.get_D_count() == {"0@0": 3, "1@0": 0, "2@0": 1, "3@0": 0}
    assert FaultList().calc_fc() == 0.0


def test_faults_excluding_keeps_the_list_order():
    faults = FaultList()
    faults.add_str_list(["5@0", "1@1", "9@0", "2@0"])
    assert faults.faults_excluding(["1@1", Fault(2, 0)]) == ["5@0", "9@0"]
    assert len(faults) == 4  # unchanged
