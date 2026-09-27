"""Nodes with design-for-test measures.

Every ``DFT*`` class extends a gate class of :mod:`pycad.node.node` with the
backward and forward computations needed by

* SCOAP: combinational controllability ``CC0``/``CC1`` and observability ``CO``
* STAFAN: probabilities ``C0``/``C1`` (controllability), ``S`` (sensitization)
  and ``B0``/``B1`` (observability)
* the parallel fault simulators: ``pfs_V`` (value) and ``pfs_I`` (fault mask)

The attribute names follow the notation of the SCOAP and STAFAN papers.
"""
import math
import warnings
from abc import ABC, abstractmethod
from functools import reduce

from pycad.node import node


class DFTNode(ABC):
    """Measures and methods shared by all DFT nodes (mixin of a gate class).

    Attributes
    ----------
    CC0, CC1, CO : int
        SCOAP controllability to 0 and 1, and observability.
    one_count, zero_count, sen_count : int
        Number of patterns in which the node was 1, was 0, and was sensitized.
    C0, C1, S : float
        STAFAN probabilities, the counts divided by the number of patterns.
    B0, B1 : float
        STAFAN observability of a 0 and of a 1 on the node.
    pfs_V, pfs_I : int
        Bit-parallel value and fault mask used by the PFS fault simulator.
    stat : dict
        Free-form results attached to the node (e.g. detection probabilities).
    """

    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)

        # PFS
        self.pfs_V = None
        self.pfs_I = None

        # SCOAP
        self.CC0 = None
        self.CC1 = None
        self.CO = None

        # STAFAN
        self.one_count = 0
        self.zero_count = 0
        self.sen_count = 0
        self.S = None
        self.C1 = None
        self.C0 = None
        self.B1 = None
        self.B0 = None

        self.stat = {}

    # Value-indexed access: ``cc(0)`` is CC0 and ``cc(1)`` is CC1, and so on.
    def cc(self, value):
        return self.CC1 if value else self.CC0

    def set_cc(self, value, measure):
        if value:
            self.CC1 = measure
        else:
            self.CC0 = measure

    def c_prob(self, value):
        return self.C1 if value else self.C0

    def b_prob(self, value):
        return self.B1 if value else self.B0

    def set_b_prob(self, value, probability):
        if value:
            self.B1 = probability
        else:
            self.B0 = probability

    def insert_f(self, bitwise_not, pfs_S):
        """Force the fault values ``pfs_S`` on the bits of ``pfs_V`` selected by ``pfs_I``."""
        pfs_I_bar = self.pfs_I ^ bitwise_not
        self.pfs_V = (pfs_I_bar & self.pfs_V) | (self.pfs_I & pfs_S)

    def print_info(self, get_labels=False, print_labels=True):
        """Print the node and its measures in one line (labels in the header or inline)."""
        if get_labels:
            return ["N", "LEV", "GATE", "CC0", "CC1", "CO", "C0",
                    "C1", "S", "B0", "B1"]
        if print_labels:
            print(f"N:{str(self.num).zfill(4)}\tLEV:{str(self.lev).zfill(2)}\t"
                  f"GATE:{self.gtype}")
        else:
            print(f"N:{str(self.num).zfill(4)}\t{str(self.lev).zfill(2)}\t{self.gtype}\t"
                  f"{self.CC0}\t{self.CC1}\t{self.CO}\t"
                  f"{self.C0}\t{self.C1}\t{self.S}\t{self.B0}\t{self.B1}")

    @abstractmethod
    def imply_p(self, bitwise_not):
        """Forward bit-parallel value for PFS, from the ``pfs_V`` of the input nodes."""

    @abstractmethod
    def eval_cc(self):
        """Forward SCOAP controllability of this node from its input nodes."""

    @abstractmethod
    def eval_co(self):
        """Backward SCOAP observability of the input nodes from this node's ``CO``."""

    @abstractmethod
    def stafan_b(self):
        """Backward STAFAN observability of the input nodes from this node's ``B0``, ``B1``."""

    def is_sensible(self):
        """True if a change of this node's value changes the output of the gate it feeds.

        Two-valued logic only. A primary output is always sensitized and a
        node that drives nothing never is.
        """
        if self.ntype == 'PO':
            return True
        if not self.dnodes:
            return False

        gate = self.dnodes[0]
        if gate.gtype in ('NOT', 'XOR', 'XNOR', 'BRCH', 'BUFF'):
            return True
        if gate.gtype in ('AND', 'NAND', 'OR', 'NOR'):
            # a controlling value on another input blocks this one
            return gate.CONTROL not in self.get_neighbors(inclusive=False, value=True)
        raise ValueError(f"Node {self.num} feeds a gate of unsupported type {gate.gtype}")


class _DFTPassThrough(DFTNode):
    """BUFF and BRCH: the output copies the input (BRCH: with its own CO rule)."""

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V

    def eval_cc(self):
        self.CC0 = self.unodes[0].CC0
        self.CC1 = self.unodes[0].CC1

    def stafan_b(self):
        self.unodes[0].B1 = self.B1
        self.unodes[0].B0 = self.B0


class DFTBUFF(_DFTPassThrough, node.BUFF):
    def eval_cc(self):
        self.CC0 = 1 + self.unodes[0].CC0
        self.CC1 = 1 + self.unodes[0].CC1

    def eval_co(self):
        self.unodes[0].CO = self.CO + 1


class DFTNOT(DFTNode, node.NOT):
    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V ^ bitwise_not

    def eval_cc(self):
        self.CC0 = 1 + self.unodes[0].CC1
        self.CC1 = 1 + self.unodes[0].CC0

    def eval_co(self):
        self.unodes[0].CO = self.CO + 1

    def stafan_b(self):
        self.unodes[0].B1 = self.B0
        self.unodes[0].B0 = self.B1


class DFTBRCH(_DFTPassThrough, node.BRCH):
    def eval_co(self):
        # The observability of a stem is computed by each of its branches. This
        # repeats the same minimum for every branch, which is harmless.
        self.unodes[0].CO = min(branch.CO for branch in self.unodes[0].dnodes)

    def stafan_b(self):
        # Observability of a stem from its branches: a fault on the stem is seen
        # if it is seen through at least one branch. Very approximate (STAFAN paper).
        branches = self.unodes[0].dnodes
        self.unodes[0].B1 = 1 - math.prod(1 - branch.B1 for branch in branches)
        self.unodes[0].B0 = 1 - math.prod(1 - branch.B0 for branch in branches)


class _DFTControlled(DFTNode):
    """AND, NAND, OR and NOR.

    The measures are written once in terms of the gate's controlling input
    value ``c`` (0 for AND/NAND, 1 for OR/NOR), the non-controlling value
    ``nc = 1 - c`` and the inversion ``INVERT``. All inputs at ``nc`` give the
    output value ``nc ^ INVERT``; any input at ``c`` gives ``c ^ INVERT``.
    """

    def imply_p(self, bitwise_not):
        value = reduce(self._combine, (unode.pfs_V for unode in self.unodes))
        self.pfs_V = value ^ bitwise_not if self.INVERT else value

    def eval_cc(self):
        nc = 1 - self.CONTROL
        # all inputs non-controlling: every input has to be set
        self.set_cc(nc ^ self.INVERT, 1 + sum(unode.cc(nc) for unode in self.unodes))
        # one controlling input is enough: the easiest one
        self.set_cc(self.CONTROL ^ self.INVERT,
                    1 + min(unode.cc(self.CONTROL) for unode in self.unodes))

    def eval_co(self):
        # to observe an input all the others must be non-controlling
        nc = 1 - self.CONTROL
        total = sum(unode.cc(nc) for unode in self.unodes)
        for unode in self.unodes:
            unode.CO = total - unode.cc(nc) + self.CO + 1

    def stafan_b(self):
        # Note: the formulas of the original STAFAN paper contain a typo for NAND.
        nc = 1 - self.CONTROL
        out_nc = nc ^ self.INVERT          # output value when all inputs are non-controlling
        out_c = self.CONTROL ^ self.INVERT  # output value when an input is controlling

        for unode in self.unodes:
            try:
                b_nc = self.b_prob(out_nc) * self.c_prob(out_nc) / unode.c_prob(nc)
            except ZeroDivisionError:
                b_nc = self._b_without_division(unode, out_nc, nc)
            try:
                b_c = (self.b_prob(out_c) * (unode.S - self.c_prob(out_nc))
                       / unode.c_prob(self.CONTROL))
            except ZeroDivisionError:
                b_c = self._b_without_division(unode, out_c, nc)
            unode.set_b_prob(nc, b_nc)
            unode.set_b_prob(self.CONTROL, b_c)

    def _b_without_division(self, unode, out_value, nc):
        """Observability of ``unode`` when its controllability is zero.

        The formula divides by the controllability of ``unode``. The quotient
        is replaced by the product of the other inputs' non-controlling
        probabilities, which is what the quotient stands for.
        """
        others = [x.c_prob(nc) for x in unode.get_neighbors(inclusive=False)]
        if 0 in others:
            raise ValueError(
                f"STAFAN observability of node {unode.num} is undefined: a controllability "
                f"is zero for the node and for another input of gate {self.num}")
        warnings.warn(f"Controllability of node {unode.num} is zero, "
                      f"approximating its observability (gate {self.num})", RuntimeWarning,
                      stacklevel=3)
        b = self.b_prob(out_value)
        for probability in others:
            b *= probability
        return b


class DFTAND(_DFTControlled, node.AND):
    pass


class DFTNAND(_DFTControlled, node.NAND):
    pass


class DFTOR(_DFTControlled, node.OR):
    pass


class DFTNOR(_DFTControlled, node.NOR):
    pass


class _DFTParity(DFTNode):
    """XOR and XNOR. SCOAP is only defined here for gates with two inputs."""

    def _require_two_inputs(self):
        if len(self.unodes) != 2:
            raise NotImplementedError(
                f"SCOAP for {self.gtype} gates with {len(self.unodes)} inputs is not implemented")

    def imply_p(self, bitwise_not):
        value = reduce(lambda a, b: a ^ b, (unode.pfs_V for unode in self.unodes))
        self.pfs_V = value ^ bitwise_not if self.INVERT else value

    def eval_cc(self):
        self._require_two_inputs()
        a, b = self.unodes
        different = 1 + min(a.CC1 + b.CC0, a.CC0 + b.CC1)
        same = 1 + min(a.CC0 + b.CC0, a.CC1 + b.CC1)
        # XOR is 1 when the inputs differ, XNOR when they are the same
        self.CC1, self.CC0 = (same, different) if self.INVERT else (different, same)

    def eval_co(self):
        self._require_two_inputs()
        a, b = self.unodes
        a.CO = min(b.CC0, b.CC1) + self.CO + 1
        b.CO = min(a.CC0, a.CC1) + self.CO + 1

    def stafan_b(self):
        for unode in self.unodes:
            unode.B1 = self.B0
            unode.B0 = self.B1


class DFTXOR(_DFTParity, node.XOR):
    pass


class DFTXNOR(_DFTParity, node.XNOR):
    pass


class DFTIPT(DFTNode, node.IPT):
    def imply_p(self, bitwise_not, pfs_V):
        self.pfs_V = pfs_V * bitwise_not

    def eval_cc(self):
        self.CC0 = 1
        self.CC1 = 1

    def eval_co(self):
        pass

    def stafan_b(self):
        pass
