"""Common parts of the fault simulators."""
import os
from abc import ABC, abstractmethod

from pycad.fault_simulation.fault import FaultList
from pycad.node.node import Node
from pycad.tp_generator import TPGenerator


class FaultSim(ABC):
    """Base class of the stuck-at fault simulators.

    Parameters
    ----------
    circuit : DFTCircuit
        The circuit to simulate.
    faults : FaultList, int, str or None
        Faults to simulate, see ``resolve_faults``. ``None`` starts with an empty list.

    Attributes
    ----------
    wordlen : int
        Number of bits of the integers used for bit-parallel simulation.
    fault_list : FaultList
        The faults simulated by default.
    """

    wordlen = Node.bitlen
    bitwise_not = Node.bitwise_not

    def __init__(self, circuit, faults=None):
        self.circuit = circuit
        self.fault_list = FaultList(circuit) if faults is None else self.resolve_faults(faults)

    def resolve_faults(self, faults):
        """Turn a description of faults into a FaultList.

        ``faults`` is

        * a ``FaultList``: used as it is,
        * ``'all'``: both stuck-at faults of every node,
        * an ``int``: that many different random faults,
        * a ``str``: the name of a fault file (``<node>@<value>`` per line),
        * a list of ``<node>@<value>`` strings,
        * ``None``: the simulator's own fault list, or all faults if that is empty.
        """
        if isinstance(faults, FaultList):
            return faults
        if faults is None:
            if len(self.fault_list) > 0:
                return self.fault_list
            return FaultList(self.circuit, fault_count="all")
        if faults == 'all' or isinstance(faults, int):
            return FaultList(self.circuit, fault_count=faults)
        if isinstance(faults, str):
            return FaultList(fname=faults)
        if isinstance(faults, list):
            fault_list = FaultList(self.circuit)
            fault_list.add_str_list(faults)
            return fault_list
        raise TypeError(f"Cannot make a fault list from {faults!r}")

    def resolve_patterns(self, tps):
        """Turn a pattern count, a pattern file name or a list of patterns into a list."""
        if isinstance(tps, int):
            return TPGenerator(self.circuit).gen_n_random(tps)
        if isinstance(tps, str):
            return TPGenerator.load_file(tps)
        if isinstance(tps, list):
            return tps
        raise TypeError("tps should be a pattern count, a file name or a list of patterns")

    def check_pattern(self, tp):
        """Raise ValueError unless ``tp`` is a binary pattern with one value per input."""
        if len(tp) != len(self.circuit.inputs):
            raise ValueError(f"The pattern has {len(tp)} values but the circuit has "
                             f"{len(self.circuit.inputs)} inputs")
        if any(value not in (0, 1) for value in tp):
            raise ValueError("Fault simulation needs binary patterns without X")

    def log_path(self, log_dir, name):
        """Path of a log file inside ``log_dir``, creating the directory."""
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, name)

    @abstractmethod
    def run(self, tps, faults=None, **kwargs):
        """Simulate the patterns ``tps`` for the faults and update their ``D_count``."""
