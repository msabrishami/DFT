"""Common parts of the fault simulators."""
import os
from abc import ABC, abstractmethod

from pycad.fault_simulation.fault import Fault, FaultList
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
        * a list of ``<node>@<value>`` strings or of ``Fault`` objects,
        * ``None``: the simulator's own fault list, or all faults if that is empty.

        Raises
        ------
        ValueError
            If a fault is on a node that is not in the circuit.
        """
        fault_list = self._build_fault_list(faults)
        unknown = [str(f) for f in fault_list.faults if f.node_num not in self.circuit.nodes]
        if unknown:
            raise ValueError(
                f"Faults on nodes that are not in circuit {self.circuit.c_name}: {unknown[:5]}")
        return fault_list

    def _build_fault_list(self, faults):
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
            for fault in faults:
                if isinstance(fault, Fault):
                    fault_list.add_fault(fault)
                else:
                    fault_list.add_str(fault)
            return fault_list
        raise TypeError(f"Cannot make a fault list from {faults!r}")

    def _prepare(self, tps, faults):
        """Patterns and faults of a run, with the detection counts of the faults reset."""
        tps = TPGenerator(self.circuit).resolve(tps)
        self.fault_list = self.resolve_faults(faults)
        for fault in self.fault_list.faults:
            fault.D_count = 0
        return tps

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
    def run(self, tps, faults=None, log_dir=None):
        """Simulate the patterns ``tps`` for the faults and update their ``D_count``.

        The ``D_count`` of the faults counts the patterns that detect them, and
        the faults simulated are ``self.fault_list`` afterwards. What is returned
        differs per simulator.
        """
