"""Deductive fault simulation (DFS): all faults, one pattern, in a single pass."""
from functools import reduce

from pycad.fault_simulation.fault_simulation import FaultSim


class DFS(FaultSim):
    """Deductive fault simulation.

    For one pattern, every node gets the set of faults that would change its
    value (written ``<node>@<value>``, stuck at the opposite of the node's good
    value). The sets are deduced from the sets of the input nodes:

    * a pass-through gate (BUFF, BRCH, NOT) keeps the set of its input;
    * for AND, NAND, OR and NOR, if no input has the controlling value the sets
      of all inputs are united; otherwise it is the faults common to all inputs
      with the controlling value, minus those of the other inputs;
    * for XOR and XNOR it is the symmetric difference of the sets of the inputs;
    * a node always adds its own fault stuck at the opposite value.

    The faults at the outputs are the faults detected by the pattern. The circuit
    can be a plain ``Circuit``, the nodes need no DFT measures.
    """

    def single(self, tp):
        """All faults of the circuit detected by pattern ``tp``, as a set of strings."""
        self.check_pattern(tp)
        self.circuit.logic_sim(tp)

        deduced = {}
        for node in self.circuit.nodes_lev:
            if node.gtype == "IPT":
                faults = set()
            else:
                faults = self._propagate(node, [deduced[u.num] for u in node.unodes])
            faults.add(f"{node.num}@{1 - node.value}")  # the node's own fault
            deduced[node.num] = faults

        return set().union(*(deduced[po.num] for po in self.circuit.outputs))

    @staticmethod
    def _propagate(node, input_sets):
        """Faults of the inputs of ``node`` that reach its output, as a new set."""
        if node.gtype in ("BUFF", "BRCH", "NOT"):
            return set(input_sets[0])
        if node.gtype in ("XOR", "XNOR"):
            return reduce(lambda a, b: a ^ b, input_sets, set())

        controlled = [s for s, u in zip(input_sets, node.unodes, strict=True)
                      if u.value == node.CONTROL]
        if not controlled:
            return set().union(*input_sets)
        free = [s for s, u in zip(input_sets, node.unodes, strict=True)
                if u.value != node.CONTROL]
        return reduce(lambda a, b: a & b, controlled) - set().union(*free)

    def run(self, tps, faults=None, log_dir=None):
        """Fault simulate a sequence of patterns, one pattern at a time.

        Gives the same results as ``PFS.run`` (without fault dropping). The
        ``D_count`` of the faults is reset and then counts the detecting patterns.

        Parameters
        ----------
        tps : int, str or list
            A number of random patterns, a pattern file name, or a list of patterns.
        faults : FaultList, int, str, list or None
            The faults to report, see ``FaultSim.resolve_faults``.
        log_dir : str, optional
            If given, a log of the fault coverage is written there.

        Returns
        -------
        tuple
            ``(fc, detected)``: the fault coverage after each pattern (fractions)
            and the list of all faults detected at least once.
        """
        tps = self._prepare(tps, faults)
        by_name = {}
        for fault in self.fault_list.faults:
            by_name.setdefault(str(fault), []).append(fault)

        fault_coverage = []
        detected_all = {}
        for tp in tps:
            for name in self.single(tp) & by_name.keys():
                for fault in by_name[name]:
                    fault.D_count += 1
                    detected_all[fault] = None
            fault_coverage.append(self.fault_list.calc_fc())

        if log_dir is not None:
            fname = f"{self.circuit.c_name}-dfs-tp{len(tps)}-f{len(self.fault_list)}.log"
            with open(self.log_path(log_dir, fname), "w") as outfile:
                for idx, fc in enumerate(fault_coverage):
                    outfile.write(f"{idx:5} \t FC={100 * fc:.4f}%\n")

        return fault_coverage, list(detected_all)
