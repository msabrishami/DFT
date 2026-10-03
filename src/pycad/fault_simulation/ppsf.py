"""Parallel-pattern single-fault simulation (PPSF): one fault, many patterns at a time."""
import math
import os
import random
import time
from typing import NamedTuple

import numpy as np

from pycad.fault_simulation.fault import Fault
from pycad.fault_simulation.fault_simulation import FaultSim
from pycad.parallel import parallel_map
from pycad.tp_generator import TPGenerator

CI_MODES = ("basic", "advanced")


class CIEstimate(NamedTuple):
    """Detection probability of one fault estimated by ``PPSF.run_ci``.

    Attributes
    ----------
    mu, std : float
        Mean and standard deviation, over the worker processes, of the fraction of
        patterns that detected the fault.
    se : float
        Standard error of ``mu``.
    e_rel : float
        Relative error ``ci * se / mu`` (infinite if the fault was never detected).
    tp_count : int
        Number of patterns each process had applied when the estimate was made.
    counts : tuple
        Detection counts of the processes.
    converged : bool
        True if the stopping rule was met; False if the patterns ran out first.
    """
    mu: float
    std: float
    se: float
    e_rel: float
    tp_count: int
    counts: tuple
    converged: bool


class PPSF(FaultSim):
    """Parallel Pattern, Single Fault simulation.

    The bits of an integer are different patterns: one pass applies up to
    ``wordlen`` patterns to the fault-free circuit and to the circuit with one fault.
    """

    def _pack(self, tps):
        """One integer per input; bit ``j`` is the value of the input in pattern ``j``."""
        words = [0] * len(self.circuit.inputs)
        for j, tp in enumerate(tps):
            for i, value in enumerate(tp):
                words[i] |= value << j
        return words

    def _detecting_bits(self, words, good, fault):
        """Integer whose set bits are the patterns for which ``fault`` changes an output."""
        faulty = self.circuit.logic_sim_bitwise(words, fault)
        diff = 0
        for g, f in zip(good, faulty, strict=True):
            diff |= g ^ f
        return diff

    def _one_fault_run(self, tps, fault):
        """Simulate at most ``wordlen`` patterns for one fault.

        Returns
        -------
        set of int
            Indices in ``tps`` of the patterns that detect ``fault``.
        """
        if len(tps) > self.wordlen:
            raise ValueError(f"At most {self.wordlen} patterns fit in one pass")
        for tp in tps:
            self.check_pattern(tp)
        words = self._pack(tps)
        good = self.circuit.logic_sim_bitwise(words)
        diff = self._detecting_bits(words, good, fault)
        return {j for j in range(len(tps)) if (diff >> j) & 1}

    def _count_detections(self, tps, faults):
        """Number of patterns in ``tps`` that detect each fault in ``faults`` (a list of counts)."""
        for tp in tps:
            self.check_pattern(tp)
        counts = [0] * len(faults)
        for start in range(0, len(tps), self.wordlen):
            block = tps[start:start + self.wordlen]
            words = self._pack(block)
            mask = (1 << len(block)) - 1
            good = self.circuit.logic_sim_bitwise(words)
            for i, fault in enumerate(faults):
                counts[i] += (self._detecting_bits(words, good, fault) & mask).bit_count()
        return counts

    def run(self, tps, faults=None, log_dir=None):
        """Count how many of the patterns detect each fault.

        The ``D_count`` of the faults is reset and then set to the number of
        detecting patterns.

        Parameters
        ----------
        tps : int, str or list
            A number of random patterns, a pattern file name, or a list of patterns.
        faults : FaultList, int, str, list or None
            The faults to simulate, see ``FaultSim.resolve_faults``. They become
            ``self.fault_list``.
        log_dir : str, optional
            If given, a log of the detection counts is written there.

        Returns
        -------
        dict
            Fault string -> ``D_count``, for the detected faults only.
        """
        tps = self._prepare(tps, faults)
        if len(self.fault_list) == 0:
            raise ValueError("No fault was added to the fault list.")

        counts = self._count_detections(tps, self.fault_list.faults)
        for fault, count in zip(self.fault_list.faults, counts, strict=True):
            fault.D_count = count

        if log_dir is not None:
            self._write_log(log_dir, len(tps))
        return {str(f): f.D_count for f in self.fault_list.faults if f.D_count}

    def _write_log(self, log_dir, tp_count):
        fname = f"{self.circuit.c_name}_PPSF_f{len(self.fault_list)}_tp{tp_count}.ppsf"
        with open(self.log_path(log_dir, fname), "w") as outfile:
            outfile.write(f"#TP={tp_count}\n")
            for fault in self.fault_list.faults:
                outfile.write(f"{fault}\t{fault.D_count}\n")
            outfile.write(f"Fault Coverage = {100 * self.fault_list.calc_fc():.4f}%\n")

    # -------------------------------------------------------- confidence intervals
    def _random_detection_counts(self, tp_count, seed, sites):
        """Worker of ``run_ci``: detections of the faults ``sites`` by random patterns."""
        tps = TPGenerator(self.circuit, rng=random.Random(seed)).gen_n_random(tp_count)
        return self._count_detections(tps, [Fault(num, val) for num, val in sites])

    def run_ci(self, tp_steps, faults=None, num_proc=2, ci=1, mode="basic", moe=0.1,
               log_fname=None):
        """Estimate detection probabilities of faults with random patterns, step by step.

        In every step each of ``num_proc`` processes applies the next number of
        random patterns of ``tp_steps`` (every process with its own patterns) and
        counts the detections of each fault. A fault is *finished* once the
        counts of the processes agree well enough, i.e. when ``mu / std > ci``
        (and, in the ``advanced`` mode, also the relative error is below ``moe``),
        or when every pattern detected the fault. If all processes counted the same
        but not every pattern detected the fault, no spread can be estimated and the
        fault stays unfinished. Finished faults are not simulated in the following steps.

        Parameters
        ----------
        tp_steps : list of int
            Pattern counts added in each step; the totals accumulate.
        faults : FaultList, int, str, list or None
            The faults to estimate, see ``FaultSim.resolve_faults``.
        num_proc : int
            Number of processes, i.e. of independent observations per fault. At
            least 2, because the spread of the counts is part of the stopping rule.
        ci : float
            Confidence factor of the stopping rule.
        mode : {'basic', 'advanced'}
            Stopping rule, see above.
        moe : float
            Largest relative error in the ``advanced`` mode.
        log_fname : str, optional
            File to write a log to. ``pycad.paths.ppsf_ci_file`` builds a conventional name.
            ``load_detection_probabilities`` reads the log.

        Returns
        -------
        dict
            Fault string -> :class:`CIEstimate`, for all faults. Faults that were
            never detected have ``mu == 0``.
        """
        if mode not in CI_MODES:
            raise ValueError(f"mode must be one of {CI_MODES}, not {mode!r}")
        if num_proc < 2:
            raise ValueError("run_ci needs at least 2 processes to estimate a spread")
        fault_list = self.resolve_faults(faults)
        if len(fault_list) == 0:
            raise ValueError("No fault was added to the fault list.")

        counts = {str(f): np.zeros(num_proc) for f in fault_list.faults}
        remaining = list(fault_list.faults)
        estimates = {}
        log = []
        runtime_log = []
        tp_total = 0

        def estimate(fault, converged):
            c = counts[str(fault)]
            mu = float(np.mean(c / tp_total))
            std = float(np.std(c / tp_total))
            se = math.sqrt(mu * (1 - mu) / (tp_total * num_proc))
            e_rel = ci * se / mu if mu > 0 else math.inf
            return CIEstimate(mu, std, se, e_rel, tp_total,
                              tuple(int(x) for x in c), converged)

        def line(tag, fault, est):
            return (f"{tag}\t{fault}\t{est.mu:.4e}\t{est.std:.4e}\t{est.se:.4e}"
                    f"\t{est.e_rel:.4e}\t{','.join(map(str, est.counts))}\n")

        for step in tp_steps:
            step = int(step)
            tp_total += step
            started = time.time()
            sites = [(f.node_num, f.stuck_val) for f in remaining]
            seeds = [random.getrandbits(64) for _ in range(num_proc)]
            jobs = [(step, seed, sites) for seed in seeds]
            results = parallel_map(self, "_random_detection_counts", jobs, num_proc)

            log.append(f"#TP={step}\n")
            unfinished = []
            for k, fault in enumerate(remaining):
                counts[str(fault)] += [result[k] for result in results]
                est = estimate(fault, converged=False)
                if est.mu == 0:
                    unfinished.append(fault)  # not detected yet: nothing to estimate
                    continue
                if est.std == 0:
                    done = est.mu == 1  # detected by every pattern: nothing left to estimate
                else:
                    done = est.mu / est.std > ci and (mode == "basic" or est.e_rel < moe)
                if done:
                    estimates[str(fault)] = est._replace(converged=True)
                else:
                    unfinished.append(fault)
                log.append(line("STOP:" if done else "CONT:", fault, est))

            runtime_log.append(
                f"TP = {step:5}: Simulated faults = #{len(remaining)}\t"
                f"Finalized faults = #{len(remaining) - len(unfinished):4}\t"
                f"Remaining faults = #{len(unfinished):4}\t"
                f"Elapsed time = {time.time() - started:.2f}s\n")
            remaining = unfinished
            if not remaining:
                break

        if tp_total > 0:
            for fault in remaining:
                estimates[str(fault)] = estimate(fault, converged=False)
                log.append(line("REMAINED:", fault, estimates[str(fault)]))

        if log_fname is not None:
            os.makedirs(os.path.dirname(os.path.abspath(log_fname)), exist_ok=True)
            with open(log_fname, "w") as outfile:
                outfile.writelines(log)
                outfile.write("### RUNTIME LOG ###\n")
                outfile.writelines(runtime_log)
        return estimates

    def load_detection_probabilities(self, fname):
        """Read a log written by ``run_ci`` and store the probabilities in the nodes.

        The estimate of fault ``<node>@<value>`` becomes ``node.stat["DP<value>"]``.
        If a fault appears in several steps, the last estimate counts.

        Returns
        -------
        dict
            Fault string -> estimated detection probability.
        """
        probabilities = {}
        with open(fname) as infile:
            for line in infile:
                tag = line.split("\t", 1)[0]
                if tag not in ("STOP:", "CONT:", "REMAINED:"):
                    continue
                _, fault, mu = line.split("\t")[:3]
                num, stuck = fault.split("@")
                self.circuit.nodes[num].stat["DP" + stuck] = float(mu)
                probabilities[fault] = float(mu)
        return probabilities

