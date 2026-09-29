"""Running methods over worker processes without pickling the object."""
import os

import pytest

from pycad import config, parallel
from pycad.circuit.dft_circuit import DFTCircuit

needs_fork = pytest.mark.skipif(not parallel.fork_available(), reason="needs the fork start method")


class Worker:
    def __init__(self):
        self.offset = 100
        self.unpicklable = lambda: None  # proves the object itself is never pickled

    def work(self, a, b):
        return self.offset + a * b + os.getpid() * 0


def test_serial_run_for_one_process():
    assert parallel.parallel_map(Worker(), "work", [(1, 2), (3, 4)], 1) == [102, 112]


@needs_fork
def test_workers_see_the_object_and_results_keep_the_job_order():
    jobs = [(i, 2) for i in range(7)]
    assert parallel.parallel_map(Worker(), "work", jobs, 3) == [100 + 2 * i for i in range(7)]


@needs_fork
def test_the_shared_object_is_released_afterwards():
    parallel.parallel_map(Worker(), "work", [(1, 1), (2, 2)], 2)
    assert parallel._shared is None


@needs_fork
def test_a_circuit_too_deep_to_pickle_can_be_used():
    circuit = DFTCircuit(os.path.join(config.CKT_DIR, "c6288.ckt"))
    results = parallel.parallel_map(circuit, "_count_random_patterns", [(5, 1), (5, 2)], 2)
    assert len(results) == 2 and all(len(counts) == len(circuit.nodes) for counts in results[0])


def test_missing_fork_falls_back_to_serial(monkeypatch):
    monkeypatch.setattr(parallel, "fork_available", lambda: False)
    with pytest.warns(RuntimeWarning, match="fork"):
        assert parallel.parallel_map(Worker(), "work", [(1, 1), (2, 2)], 2) == [101, 104]
