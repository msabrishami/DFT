"""The D-algorithm.

Unlike PODEM it assigns values to any node, not only to inputs. The good and the
faulty circuit are two three-valued assignments (a node that differs between the
two carries D or D-bar). A decision either pushes the fault effect through a gate
of the D-frontier or justifies the value of an unjustified gate; every decision is
followed by forward and backward implication until nothing changes.
"""
from pycad.atpg.base import ABORTED, DETECTED, REDUNDANT, Atpg, AtpgResult
from pycad.config import X_VALUE
from pycad.node.node import GateType

X = X_VALUE
GOOD, FAULTY = 0, 1
_CONTROLLED = (GateType.AND, GateType.NAND, GateType.OR, GateType.NOR)
_PARITY = (GateType.XOR, GateType.XNOR)


def imply_gate(node, ins, out):
    """Forward and backward implication of one gate.

    Returns ``(ins, out)`` with every value that follows from the given ones, or
    ``None`` if they contradict each other.
    """
    ins = list(ins)
    gtype = node.gtype
    if gtype in (GateType.BUFF, GateType.BRCH, GateType.NOT):
        flip = 1 if gtype == GateType.NOT else 0
        if ins[0] != X:
            expected = ins[0] ^ flip
            if out == X:
                out = expected
            elif out != expected:
                return None
        elif out != X:
            ins[0] = out ^ flip
        return ins, out

    if gtype in _PARITY:
        unknown = [k for k, v in enumerate(ins) if v == X]
        known = sum(v for v in ins if v != X)
        if not unknown:
            expected = (known + node.INVERT) % 2
            if out == X:
                out = expected
            elif out != expected:
                return None
        elif len(unknown) == 1 and out != X:
            ins[unknown[0]] = (out ^ node.INVERT ^ known) & 1
        return ins, out

    control, non_control = node.CONTROL, 1 - node.CONTROL
    out_controlled = control ^ node.INVERT
    out_free = 1 - out_controlled
    if control in ins:
        expected = out_controlled
    elif X not in ins:
        expected = out_free
    else:
        expected = None
    if expected is not None:
        if out == X:
            out = expected
        elif out != expected:
            return None
    if out == out_free:
        if control in ins:
            return None
        ins = [non_control] * len(ins)
    elif out == out_controlled and control not in ins:
        unknown = [k for k, v in enumerate(ins) if v == X]
        if not unknown:
            return None
        if len(unknown) == 1:
            ins[unknown[0]] = control
    return ins, out


class DAlgorithm(Atpg):
    """D-algorithm test generator, see :class:`~pycad.atpg.base.Atpg`."""

    # A state is [good values, faulty values] (lists indexed like ``self.nodes``).

    def _cone(self, target):
        cone, todo = {target}, [target]
        while todo:
            for j in self.fanout[todo.pop()]:
                if j not in cone:
                    cone.add(j)
                    todo.append(j)
        return cone

    def _set(self, state, i, comp, value, cone, queue):
        """Assign ``value`` to a node; False on conflict. Nodes outside the cone are shared."""
        comps = (comp,) if i in cone else (GOOD, FAULTY)
        for k in comps:
            if state[k][i] == value:
                continue
            if state[k][i] != X:
                return False
            state[k][i] = value
            queue.append(i)
            queue.extend(self.fanout[i])
        return True

    def _imply(self, state, target, cone, queue):
        """Propagate implications until the queue is empty; False on conflict."""
        while queue:
            i = queue.pop()
            node = self.nodes[i]
            if node.gtype == GateType.IPT:
                continue
            for comp in (GOOD, FAULTY):
                if i not in cone and comp == FAULTY:
                    continue
                if i == target and comp == FAULTY:
                    continue
                values = state[comp]
                fanin = self.fanin[i]
                result = imply_gate(node, [values[j] for j in fanin], values[i])
                if result is None:
                    return False
                ins, out = result
                for j, value in zip(fanin, ins, strict=True):
                    if value != X and not self._set(state, j, comp, value, cone, queue):
                        return False
                if out != X and not self._set(state, i, comp, out, cone, queue):
                    return False
        return True

    def _differs(self, state, i):
        g, f = state[GOOD][i], state[FAULTY][i]
        return g != X and f != X and g != f

    def _d_frontier(self, state, cone):
        frontier = []
        for i in sorted(cone):
            node = self.nodes[i]
            if node.gtype == GateType.IPT:
                continue
            if X not in (state[GOOD][i], state[FAULTY][i]):
                continue
            if any(self._differs(state, j) for j in self.fanin[i]):
                frontier.append(i)
        return frontier

    def _unjustified(self, state, target, cone):
        """The (gate, component) pairs whose output is not yet explained by their inputs."""
        for i, node in enumerate(self.nodes):
            if node.gtype not in _CONTROLLED and node.gtype not in _PARITY:
                continue
            for comp in (GOOD, FAULTY):
                if comp == FAULTY and (i not in cone or i == target):
                    continue
                values = state[comp]
                out = values[i]
                ins = [values[j] for j in self.fanin[i]]
                if out == X or X not in ins:
                    continue
                if node.gtype in _PARITY:
                    return i, comp
                if out == node.CONTROL ^ node.INVERT and node.CONTROL not in ins:
                    return i, comp
        return None

    @staticmethod
    def _copy(state):
        return [state[GOOD][:], state[FAULTY][:]]

    def _propagate_choices(self, state, frontier, target, cone):
        """Child states that bring the fault effect nearer to the output of a frontier gate.

        For AND-like gates all unspecified inputs go to the non-controlling value. For
        XOR-like gates the choice matters (inputs may carry the effect themselves), so
        the first unspecified input is tried at both values.
        """
        for i in frontier:
            node = self.nodes[i]
            if node.gtype in _PARITY:
                j = next(j for j in self.fanin[i] if X in (state[GOOD][j], state[FAULTY][j]))
                for value in (0, 1):
                    child, queue, ok = self._copy(state), [], True
                    for comp in (GOOD, FAULTY):
                        if child[comp][j] == X:
                            ok = ok and self._set(child, j, comp, value, cone, queue)
                    if ok:
                        yield child, queue
                continue
            child, queue, ok = self._copy(state), [], True
            for j in self.fanin[i]:
                for comp in (GOOD, FAULTY):
                    if child[comp][j] == X:
                        ok = ok and self._set(child, j, comp, 1 - node.CONTROL, cone, queue)
            if ok:
                yield child, queue

    def _justify_choices(self, state, gate, comp, cone):
        """Child states: each unspecified input of an unjustified gate set in turn."""
        node = self.nodes[gate]
        for j in self.fanin[gate]:
            if state[comp][j] != X:
                continue
            values = (0, 1) if node.gtype in _PARITY else (node.CONTROL,)
            for value in values:
                child, queue = self._copy(state), []
                if self._set(child, j, comp, value, cone, queue):
                    yield child, queue

    def generate(self, fault):
        target, stuck = self._site(fault)
        cone = self._cone(target)
        size = len(self.nodes)
        root = [[X] * size, [X] * size]
        queue = []
        self._set(root, target, GOOD, 1 - stuck, cone, queue)
        self._set(root, target, FAULTY, stuck, cone, queue)

        backtracks = 0
        stack = [iter([(root, queue)])]
        while stack:
            try:
                state, queue = next(stack[-1])
            except StopIteration:
                stack.pop()
                backtracks += 1
                if backtracks > self.backtrack_limit:
                    return AtpgResult(ABORTED, None, backtracks)
                continue
            if not self._imply(state, target, cone, queue):
                continue
            if any(self._differs(state, i) for i in self.output_pos):
                pending = self._unjustified(state, target, cone)
                if pending is None:
                    pattern = [state[GOOD][i] for i in self.input_pos]
                    return AtpgResult(DETECTED, pattern, backtracks)
                stack.append(self._justify_choices(state, *pending, cone))
            else:
                frontier = self._d_frontier(state, cone)
                stack.append(self._propagate_choices(state, frontier, target, cone))
        return AtpgResult(REDUNDANT, None, backtracks)
