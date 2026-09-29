"""Parallel fault simulation (PFS): one pattern, many faults at a time."""
from pycad.fault_simulation.fault_simulation import FaultSim


class PFS(FaultSim):
    """Parallel Fault, Single Pattern fault simulation.

    The bits of an integer are copies of the circuit: bit ``wordlen - 1`` is the
    fault-free circuit and each of the other bits carries one fault. One pass
    simulates ``wordlen - 1`` faults for one pattern.
    """

    def _one_tp_run(self, tp, fault_drop=None):
        """Simulate one pattern for the faults of ``self.fault_list``.

        Faults whose ``D_count`` is already at least ``fault_drop`` are skipped.
        The ``D_count`` of every fault detected by ``tp`` is increased by one.

        Parameters
        ----------
        tp : list
            One value per input, in the order of ``circuit.inputs``.

        Returns
        -------
        list of Fault
            The faults detected by this pattern, in fault list order.
        """
        self.check_pattern(tp)
        active = self.fault_list.faults
        if fault_drop:
            active = [fault for fault in active if fault.D_count < fault_drop]

        per_pass = self.wordlen - 1
        detected = []
        for start in range(0, len(active), per_pass):
            detected += self._one_pass(tp, active[start:start + per_pass])

        for fault in detected:
            fault.D_count += 1
        return detected

    def _one_pass(self, tp, faults_pass):
        """Simulate ``tp`` once with up to ``wordlen - 1`` faults, one per bit."""
        stuck_values = 0
        masks = {}  # node number -> bits of the faults on that node
        for i, fault in enumerate(faults_pass):
            stuck_values |= int(fault.stuck_val) << i
            masks[fault.node_num] = masks.get(fault.node_num, 0) | (1 << i)

        applied = {pi.num: value for pi, value in zip(self.circuit.inputs, tp, strict=True)}
        for node in self.circuit.nodes_lev:
            node.pfs_I = masks.get(node.num, 0)
            if node.gtype == "IPT":
                node.imply_p(self.bitwise_not, applied[node.num])
            else:
                node.imply_p(self.bitwise_not)
            node.insert_f(self.bitwise_not, stuck_values)

        # a fault is detected if its bit differs from the good bit at some output
        faulty_bits = (1 << (self.wordlen - 1)) - 1
        differs = 0
        for po in self.circuit.outputs:
            good = (po.pfs_V >> (self.wordlen - 1)) & 1
            differs |= (po.pfs_V ^ (faulty_bits * good)) & faulty_bits

        return [fault for i, fault in enumerate(faults_pass) if (differs >> i) & 1]

    def run(self, tps, faults=None, fault_drop=None, log_dir=None):
        """Fault simulate a sequence of patterns, one pattern at a time.

        The ``D_count`` of the faults is reset first and then counts the patterns
        that detect each fault (up to ``fault_drop`` if given).

        Parameters
        ----------
        tps : int, str or list
            A number of random patterns, a pattern file name, or a list of patterns.
        faults : FaultList, int, str, list or None
            The faults to simulate, see ``FaultSim.resolve_faults``. They become
            ``self.fault_list``.
        fault_drop : int, optional
            A fault detected by this many patterns is not simulated any more.
        log_dir : str, optional
            If given, a log of the detected faults and a fault coverage log are
            written there.

        Returns
        -------
        tuple
            ``(fc, detected)``: the fault coverage after each pattern (fractions)
            and the list of all faults detected at least once.
        """
        tps = self.resolve_patterns(tps)
        self.fault_list = self.resolve_faults(faults)
        for fault in self.fault_list.faults:
            fault.D_count = 0

        total = len(self.fault_list)
        fault_coverage, history = [], []
        detected_all = {}  # dict keeps the order of first detection
        for tp in tps:
            detected = self._one_tp_run(tp, fault_drop)
            detected_all.update(dict.fromkeys(detected))
            fault_coverage.append(self.fault_list.calc_fc())
            history.append((tp, detected, len(detected_all)))

        if log_dir is not None:
            self._write_logs(log_dir, history, total, fault_coverage)

        return fault_coverage, list(detected_all)

    def _write_logs(self, log_dir, history, total, fault_coverage):
        name = self.circuit.c_name
        suffix = f"tp{len(history)}-f{total}"
        with open(self.log_path(log_dir, f"{name}-pfs-{suffix}.log"), "w") as outfile:
            for tp, detected, _ in history:
                outfile.write(",".join(map(str, tp)) + "\n")
                outfile.write(f"Detected {len(detected)} faults below:\n")
                outfile.writelines(f"{fault}\n" for fault in detected)
                outfile.write("------------\n")
            outfile.write(f"Fault Coverage = {fault_coverage[-1] * 100:.4f}%\n")

        with open(self.log_path(log_dir, f"{name}-pfs-tpfc-{suffix}.log"), "w") as outfile:
            for idx, (_, detected, cumulative) in enumerate(history):
                outfile.write(f"{idx:5} \t Detected faults: {len(detected):5}"
                              f"  Total detected faults: {cumulative:5}"
                              f"  FC={100 * cumulative / total:.4f}%\n")
            outfile.write(f"Fault Coverage = {fault_coverage[-1] * 100:.4f}%\n")
