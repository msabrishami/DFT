"""PODEM: path-oriented decision making.

The search only assigns primary inputs. Each step picks an objective (excite the
fault, or push the fault effect through a gate of the D-frontier), traces it back
to an input, assigns that input and simulates the good and the faulty circuit
with three-valued logic. If the objective cannot be reached, the last input
assignment is flipped.
"""
from pycad.atpg.base import ABORTED, DETECTED, REDUNDANT, Atpg, AtpgResult, eval_gate
from pycad.config import X_VALUE
from pycad.node.node import GateType

X = X_VALUE
_CONTROLLED = (GateType.AND, GateType.NAND, GateType.OR, GateType.NOR)
_PARITY = (GateType.XOR, GateType.XNOR)


class Podem(Atpg):
    """PODEM test generator, see :class:`~pycad.atpg.base.Atpg`."""

    def _simulate(self, assigned, target, stuck):
        good = [X] * len(self.nodes)
        faulty = [X] * len(self.nodes)
        for i, node in enumerate(self.nodes):
            if node.gtype == GateType.IPT:
                good[i] = faulty[i] = assigned.get(i, X)
            else:
                good[i] = eval_gate(node, [good[j] for j in self.fanin[i]])
                faulty[i] = eval_gate(node, [faulty[j] for j in self.fanin[i]])
            if i == target:
                faulty[i] = stuck
        return good, faulty

    @staticmethod
    def _differs(good, faulty, i):
        return good[i] != X and faulty[i] != X and good[i] != faulty[i]

    def _objective(self, good, faulty, target, stuck):
        """The next (node, value) to achieve; ``None`` if the fault cannot be detected any more."""
        if good[target] == stuck:
            return None
        if good[target] == X:
            return target, 1 - stuck
        for i, node in enumerate(self.nodes):
            if X not in (good[i], faulty[i]):
                continue
            if not any(self._differs(good, faulty, j) for j in self.fanin[i]):
                continue
            for j in self.fanin[i]:
                if good[j] == X:
                    value = 0 if node.gtype in _PARITY else 1 - node.CONTROL
                    return j, value
        return None

    def _backtrace(self, good, i, value):
        """Follow unspecified inputs from node ``i`` back to a primary input."""
        while self.nodes[i].gtype != GateType.IPT:
            node = self.nodes[i]
            fanin = self.fanin[i]
            if node.gtype == GateType.NOT:
                value ^= 1
                i = fanin[0]
                continue
            if node.gtype not in _CONTROLLED and node.gtype not in _PARITY:
                i = fanin[0]
                continue
            j = next(j for j in fanin if good[j] == X)
            if node.gtype in _PARITY:
                known = sum(good[k] for k in fanin if good[k] != X)
                value = (value ^ node.INVERT ^ known) & 1
            else:
                value ^= node.INVERT
            i = j
        return i, value

    def generate(self, fault):
        target, stuck = self._site(fault)
        assigned = {}
        stack = []  # [input, value, other value already tried]
        backtracks = 0
        while True:
            good, faulty = self._simulate(assigned, target, stuck)
            if any(self._differs(good, faulty, i) for i in self.output_pos):
                pattern = [assigned.get(i, X) for i in self.input_pos]
                return AtpgResult(DETECTED, pattern, backtracks)
            objective = self._objective(good, faulty, target, stuck)
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
