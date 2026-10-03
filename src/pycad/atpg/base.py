"""Shared parts of the test pattern generators."""
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from pycad.config import X_VALUE
from pycad.fault_simulation.fault import Fault, FaultList
from pycad.node.node import GateType

DETECTED, REDUNDANT, ABORTED = "detected", "redundant", "aborted"


@dataclass
class AtpgResult:
    """Outcome of generating a test for one fault.

    Attributes
    ----------
    status : str
        ``"detected"`` (``pattern`` detects the fault), ``"redundant"`` (the search
        proved that no pattern detects it) or ``"aborted"`` (backtrack limit reached).
    pattern : list or None
        Values 0, 1 or ``X_VALUE`` in the order of ``circuit.inputs``; the inputs
        marked X may take any value. ``None`` unless the fault was detected.
    backtracks : int
        Number of backtracks of the search.
    """
    status: str
    pattern: list | None = None
    backtracks: int = 0


@dataclass
class TestSet:
    """Result of ``Atpg.generate_test_set``."""
    __test__ = False  # not a pytest class

    patterns: list = field(default_factory=list)
    detected: list = field(default_factory=list)
    redundant: list = field(default_factory=list)
    aborted: list = field(default_factory=list)

    def coverage(self, total):
        return len(self.detected) / total if total else 1.0


def fill_x(pattern, value=None, rng=random):
    """Replace the X values of a pattern: by ``value`` if given, else by random bits."""
    return [(rng.randint(0, 1) if value is None else value) if v == X_VALUE else v
            for v in pattern]


def eval_gate(node, ins):
    """Three-valued output (0, 1 or X) of the gate of ``node`` for input values ``ins``."""
    gtype = node.gtype
    if gtype == GateType.IPT:
        return X_VALUE
    if gtype in (GateType.BUFF, GateType.BRCH):
        return ins[0]
    if gtype == GateType.NOT:
        return X_VALUE if ins[0] == X_VALUE else 1 - ins[0]
    if gtype in (GateType.XOR, GateType.XNOR):
        if X_VALUE in ins:
            return X_VALUE
        return (sum(ins) + node.INVERT) % 2
    if node.CONTROL in ins:
        return node.CONTROL ^ node.INVERT
    if X_VALUE in ins:
        return X_VALUE
    return (1 - node.CONTROL) ^ node.INVERT


class Atpg(ABC):
    """Base class of the test generators for single stuck-at faults.

    Parameters
    ----------
    circuit : Circuit
        The circuit to generate tests for.
    backtrack_limit : int
        A search that needs more backtracks gives up (status ``"aborted"``).
    """

    def __init__(self, circuit, backtrack_limit=1000):
        self.circuit = circuit
        self.backtrack_limit = backtrack_limit
        self.nodes = list(circuit.nodes_lev)
        self.index = {node.num: i for i, node in enumerate(self.nodes)}
        self.fanin = [[self.index[u.num] for u in node.unodes] for node in self.nodes]
        self.fanout = [[self.index[d.num] for d in node.dnodes] for node in self.nodes]
        self.input_pos = [self.index[node.num] for node in circuit.inputs]
        self.output_pos = [self.index[node.num] for node in circuit.outputs]

    def _site(self, fault):
        if not isinstance(fault, Fault):
            fault = Fault.from_str(fault)
        if fault.node_num not in self.index:
            raise ValueError(f"Node {fault.node_num} is not in circuit {self.circuit.c_name}")
        return self.index[fault.node_num], int(fault.stuck_val)

    @abstractmethod
    def generate(self, fault):
        """Search a test for ``fault`` (a ``Fault`` or ``"<node>@<value>"``); an AtpgResult."""

    def detects(self, pattern, fault):
        """True if the fully specified ``pattern`` detects ``fault`` (by simulation).

        Raises
        ------
        ValueError
            If the pattern has unspecified (X) inputs; see ``fill_x``.
        """
        return self._detected_among(pattern, [fault])[0]

    def _detected_among(self, pattern, faults):
        """For each fault, whether ``pattern`` detects it; the good circuit is simulated once."""
        if X_VALUE in pattern:
            raise ValueError("The pattern has unspecified inputs, fill them first (fill_x)")
        words = [int(v) for v in pattern]
        good = self.circuit.logic_sim_bitwise(words)
        detected = []
        for fault in faults:
            if not isinstance(fault, Fault):
                fault = Fault.from_str(fault)
            faulty = self.circuit.logic_sim_bitwise(words, fault)
            detected.append(any((g ^ f) & 1 for g, f in zip(good, faulty, strict=True)))
        return detected

    def generate_test_set(self, faults=None, fill=None, rng=random):
        """Generate tests for a list of faults, dropping faults that earlier tests detect.

        Parameters
        ----------
        faults : FaultList, list or None
            Faults to cover; ``None`` means both stuck-at faults of every node.
        fill : int, optional
            Value for the unspecified inputs of a pattern; random bits by default.
        rng : random.Random
            Source of the random fill.

        Returns
        -------
        TestSet
        """
        if faults is None:
            faults = FaultList(self.circuit, fault_count="all")
        pending = [f if isinstance(f, Fault) else Fault.from_str(f) for f in faults]
        result = TestSet()
        while pending:
            fault = pending.pop(0)
            outcome = self.generate(fault)
            if outcome.status == REDUNDANT:
                result.redundant.append(fault)
            elif outcome.status == ABORTED:
                result.aborted.append(fault)
            else:
                pattern = fill_x(outcome.pattern, fill, rng)
                result.patterns.append(pattern)
                result.detected.append(fault)
                still = []
                for other, hit in zip(pending, self._detected_among(pattern, pending),
                                      strict=True):
                    (result.detected if hit else still).append(other)
                pending = still
        return result
