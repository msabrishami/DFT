"""PODEM: path-oriented decision making.

The search only assigns primary inputs. Each step picks an objective (excite the
fault, or push the fault effect through a gate of the D-frontier), traces it back
to an input, assigns that input and simulates the good and the faulty circuit
with three-valued logic. If the objective cannot be reached, the last input
assignment is flipped.
"""
from pycad.atpg.base import (
    ABORTED,
    DETECTED,
    MULTI_INPUT,
    PARITY,
    REDUNDANT,
    Atpg,
    AtpgResult,
    differs,
)
from pycad.config import X_VALUE as X
from pycad.node.node import GateType


class Podem(Atpg):
    """PODEM test generator, see :class:`~pycad.atpg.base.Atpg`."""

    def _simulate(self, assigned, target, stuck, cone):
        """Good and faulty values; the faulty circuit only differs inside ``cone``."""
        good = [X] * len(self.nodes)
        for i, node in enumerate(self.nodes):
            if node.gtype == GateType.IPT:
                good[i] = assigned.get(i, X)
            else:
                good[i] = node.eval_t([good[j] for j in self.fanin[i]])
        faulty = good[:]
        for i in cone:
            node = self.nodes[i]
            if i == target:
                faulty[i] = stuck
            elif node.gtype != GateType.IPT:
                faulty[i] = node.eval_t([faulty[j] for j in self.fanin[i]])
        return good, faulty

    def _objective(self, good, faulty, target, stuck, cone):
        """The next (node, value) to achieve; ``None`` if the fault cannot be detected any more."""
        if good[target] == stuck:
            return None
        if good[target] == X:
            return target, 1 - stuck
        for i in cone:  # the D-frontier lies inside the cone
            if X not in (good[i], faulty[i]):
                continue
            if not any(differs(good[j], faulty[j]) for j in self.fanin[i]):
                continue
            for j in self.fanin[i]:
                if good[j] == X:
                    node = self.nodes[i]
                    return j, 0 if node.gtype in PARITY else 1 - node.CONTROL
        return None

    def _backtrace(self, good, i, value):
        """Follow unspecified inputs from node ``i`` back to a primary input."""
        while self.nodes[i].gtype != GateType.IPT:
            node = self.nodes[i]
            fanin = self.fanin[i]
            if node.gtype not in MULTI_INPUT:  # NOT, BUFF, BRCH
                if node.gtype == GateType.NOT:
                    value ^= 1
                i = fanin[0]
                continue
            if node.gtype in PARITY:
                known = sum(good[k] for k in fanin if good[k] != X)
                value = (value ^ node.INVERT ^ known) & 1
            else:
                value ^= node.INVERT
            i = next(j for j in fanin if good[j] == X)
        return i, int(value)

    def generate(self, fault):
        target, stuck = self._site(fault)
        cone = self._cone(target)
        in_cone = set(cone)
        cone_outputs = [i for i in self.output_pos if i in in_cone]
        assigned = {}
        stack = []  # [input, value, other value already tried]
        backtracks = 0
        while True:
            good, faulty = self._simulate(assigned, target, stuck, cone)
            if any(differs(good[i], faulty[i]) for i in cone_outputs):
                pattern = [assigned.get(i, X) for i in self.input_pos]
                return AtpgResult(DETECTED, pattern, backtracks)
            objective = self._objective(good, faulty, target, stuck, cone)
            if objective is not None:
                pi, value = self._backtrace(good, *objective)
                assigned[pi] = value
                stack.append([pi, value, False])
                continue
            while stack and stack[-1][2]:
                del assigned[stack.pop()[0]]
            if not stack:
                return AtpgResult(REDUNDANT, None, backtracks)
            backtracks += 1
            if backtracks > self.backtrack_limit:
                return AtpgResult(ABORTED, None, backtracks)
            top = stack[-1]
            top[1] ^= 1
            top[2] = True
            assigned[top[0]] = top[1]
