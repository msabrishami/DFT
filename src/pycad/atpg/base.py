"""Shared parts of the test pattern generators."""
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from pycad.config import X_VALUE
from pycad.fault_simulation.fault import Fault, FaultList
from pycad.node.node import GateType

DETECTED, REDUNDANT, ABORTED = "detected", "redundant", "aborted"
CONTROLLED = (GateType.AND, GateType.NAND, GateType.OR, GateType.NOR)
PARITY = (GateType.XOR, GateType.XNOR)
MULTI_INPUT = CONTROLLED + PARITY


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
class PatternSet:
    """Result of ``Atpg.generate_test_set``."""

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


def differs(good, faulty):
    """True if a node carries D or D-bar: both values known and different."""
    return good != X_VALUE and faulty != X_VALUE and good != faulty


def as_fault(fault):
    """A ``Fault`` from a Fault or a ``"<node>@<value>"`` string."""
    return fault if isinstance(fault, Fault) else Fault.from_str(fault)


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

    def _cone(self, target):
        """Sorted indices of the nodes in the fan-out cone of ``target`` (itself included)."""
        cone, todo = {target}, [target]
        while todo:
            for j in self.fanout[todo.pop()]:
                if j not in cone:
                    cone.add(j)
                    todo.append(j)
        return sorted(cone)

    def _site(self, fault):
        fault = as_fault(fault)
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
            faulty = self.circuit.logic_sim_bitwise(words, as_fault(fault))
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
        PatternSet
        """
        if faults is None:
            faults = FaultList(self.circuit, fault_count="all")
        pending = [as_fault(f) for f in faults]
        result = PatternSet()
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
