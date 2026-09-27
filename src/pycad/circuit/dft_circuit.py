"""A circuit with the testability measures SCOAP and STAFAN."""
import math
import multiprocessing
import os
import random
import warnings

import networkx as nx

from pycad import config, paths
from pycad.circuit.circuit import Circuit
from pycad.node import dft_node
from pycad.tp_generator import TPGenerator


class DFTCircuit(Circuit):
    """A Circuit whose nodes also carry SCOAP and STAFAN measures.

    The circuit supports

    * SCOAP: ``scoap_cc`` (controllability), ``scoap_co`` (observability)
    * STAFAN: ``stafan_c`` / ``stafan_b`` or ``stafan`` for both, ``stafan_fc``
    * the fault simulators ``PFS`` and ``PPSF``

    See :class:`~pycad.node.dft_node.DFTNode` for the measures stored in the nodes.
    """

    STD_NODE_LIB = {'AND': dft_node.DFTAND,
                    'XOR': dft_node.DFTXOR,
                    'OR': dft_node.DFTOR,
                    'XNOR': dft_node.DFTXNOR,
                    'BUFF': dft_node.DFTBUFF,
                    'BRCH': dft_node.DFTBRCH,
                    'NOR': dft_node.DFTNOR,
                    'NAND': dft_node.DFTNAND,
                    'NOT': dft_node.DFTNOT,
                    'IPT': dft_node.DFTIPT}

    def __init__(self, netlist_fname):
        super().__init__(netlist_fname, DFTCircuit.STD_NODE_LIB)
        self._stafan_ready = False   # C, S and B are set (computed or loaded)
        self._stafan_tp_count = None  # number of patterns of the last computation

    # ------------------------------------------------------------------- SCOAP
    def scoap_cc(self):
        """Combinational controllability (CC0, CC1) of all nodes, from inputs to outputs."""
        for node in self.nodes_lev:
            node.eval_cc()

    def scoap_co(self):
        """Combinational observability (CO) of all nodes, from outputs to inputs.

        Needs the controllabilities, see ``scoap_cc``.
        """
        for node in self.outputs:
            node.CO = 0
        for node in reversed(self.nodes_lev):
            node.eval_co()

    def scoap(self):
        """All SCOAP measures."""
        self.scoap_cc()
        self.scoap_co()

    # ------------------------------------------------------------------ STAFAN
    def _count_patterns(self, tps):
        """Simulate patterns and count, per node, ones, zeros and sensitizations.

        Returns three lists in the order of ``nodes_lev``.
        """
        size = len(self.nodes_lev)
        ones, zeros, sensitized = [0] * size, [0] * size, [0] * size
        for tp in tps:
            self.logic_sim(tp)
            for i, node in enumerate(self.nodes_lev):
                if node.value == 1:
                    ones[i] += 1
                elif node.value == 0:
                    zeros[i] += 1
                if node.is_sensible():
                    sensitized[i] += 1
        return ones, zeros, sensitized

    def _count_random_patterns(self, count, seed):
        tps = TPGenerator(self, rng=random.Random(seed)).gen_n_random(count)
        return self._count_patterns(tps)

    def _set_stafan_c(self, ones, zeros, sensitized, tp_count):
        for node, one, zero, sen in zip(self.nodes_lev, ones, zeros, sensitized, strict=True):
            node.one_count, node.zero_count, node.sen_count = one, zero, sen
            node.C1 = one / tp_count
            node.C0 = zero / tp_count
            node.S = sen / tp_count
        self._stafan_tp_count = tp_count

    def stafan_c(self, tp):
        """STAFAN controllability and sensitization probabilities (C0, C1, S) of all nodes.

        Parameters
        ----------
        tp : int, str or list
            A number of random patterns to generate, the name of a pattern file,
            or a list of patterns.
        """
        if isinstance(tp, int):
            tps = TPGenerator(self).gen_n_random(tp)
        elif isinstance(tp, str):
            tps = TPGenerator.load_file(tp)
        elif isinstance(tp, list):
            tps = tp
        else:
            raise TypeError("tp should be a pattern count, a file name or a list of patterns")
        if not tps:
            raise ValueError("STAFAN needs at least one test pattern")

        self._set_stafan_c(*self._count_patterns(tps), len(tps))

    def stafan_b(self):
        """STAFAN observability (B0, B1) of all nodes, from outputs to inputs.

        Needs ``stafan_c`` first.

        Raises
        ------
        ValueError
            If the observability of a node is undefined because controllabilities are zero.
        """
        for node in reversed(self.nodes_lev):
            if node.ntype == "PO":
                node.B0 = 1.0
                node.B1 = 1.0
            node.stafan_b()

    def stafan(self, tp_count, num_proc=1, save_log=False):
        """STAFAN controllability and observability with ``tp_count`` random patterns.

        The patterns are generated here and not stored. With ``num_proc`` > 1 the
        patterns are split over processes (where the ``fork`` start method exists).
        The result depends on the state of the global ``random`` generator, so
        ``random.seed`` makes it reproducible for a fixed ``num_proc``.

        Parameters
        ----------
        tp_count : int
            Total number of patterns, at least ``num_proc``.
        num_proc : int
            Number of worker processes.
        save_log : bool
            Save the measures with ``save_stafan``.
        """
        if tp_count < num_proc:
            raise ValueError("The number of patterns must be at least the number of processes")

        # every worker gets its own seed, otherwise forked workers would repeat patterns
        seeds = [random.getrandbits(64) for _ in range(num_proc)]
        shares = [tp_count // num_proc + (i < tp_count % num_proc) for i in range(num_proc)]
        jobs = list(zip(shares, seeds, strict=True))

        if num_proc == 1 or "fork" not in multiprocessing.get_all_start_methods():
            if num_proc > 1:
                warnings.warn("Parallel STAFAN needs the 'fork' start method, running serially",
                              RuntimeWarning, stacklevel=2)
            results = [self._count_random_patterns(*job) for job in jobs]
        else:
            with multiprocessing.get_context("fork").Pool(num_proc) as pool:
                results = pool.starmap(self._count_random_patterns, jobs)

        ones, zeros, sensitized = (
            [sum(counts) for counts in zip(*lists, strict=True)]
            for lists in zip(*results, strict=True))
        self._set_stafan_c(ones, zeros, sensitized, tp_count)
        self.stafan_b()
        self._stafan_ready = True

        if save_log:
            self.save_stafan()

    def stafan_fc(self, tp):
        """Estimated fault coverage of ``tp`` random patterns, for all stuck-at faults.

        Needs STAFAN measures, from ``stafan`` or ``load_stafan``.
        """
        if not self._stafan_ready or any(
                None in (node.C0, node.C1, node.B0, node.B1) for node in self.nodes_lev):
            raise RuntimeError("STAFAN is not calculated or loaded completely. "
                               "First call stafan() or load_stafan().")
        undetected = 0.0
        for node in self.nodes_lev:
            undetected += math.exp(-node.C1 * node.B1 * tp)
            undetected += math.exp(-node.C0 * node.B0 * tp)
        return 1 - undetected / (2 * len(self.nodes))

    # ----------------------------------------------------------------- file I/O
    def save_stafan(self, fname=None):
        """Write the STAFAN measures of all nodes to a CSV file and return its name.

        By default the file goes to ``config.STAFAN_DIR/<circuit>/`` and is named
        after the number of patterns; a ``fname`` is taken relative to that directory.
        """
        directory = os.path.join(config.STAFAN_DIR, self.c_name)
        if fname is None:
            if self._stafan_tp_count is None:
                raise RuntimeError("STAFAN is not calculated: nothing to save")
            fname = paths.stafan_file(self.c_name, self._stafan_tp_count)
        else:
            fname = os.path.join(directory, fname)
        os.makedirs(os.path.dirname(fname), exist_ok=True)

        with open(fname, 'w') as outfile:
            outfile.write("Node,C0,C1,B0,B1,S\n")
            for node in self.nodes_lev:
                values = [f"{x:e}" for x in (node.C0, node.C1, node.B0, node.B1, node.S)]
                outfile.write(",".join([node.num] + values) + "\n")
        return fname

    def load_stafan(self, fname):
        """Read the measures from a file written by ``save_stafan``."""
        with open(fname) as infile:
            lines = infile.readlines()[1:]
        for line in lines:
            words = line.strip().split(",")
            node = self.nodes[words[0]]
            node.C0, node.C1, node.B0, node.B1, node.S = (float(x) for x in words[1:6])
        self._stafan_ready = True

    def save_scoap(self, fname=None):
        """Write the SCOAP measures of all nodes to a CSV file and return its name.

        By default the file goes to ``config.SCOAP_DIR``.
        """
        if fname is None:
            fname = os.path.join(config.SCOAP_DIR, f"{self.c_name}_scoap.txt")
        os.makedirs(os.path.dirname(os.path.abspath(fname)), exist_ok=True)
        with open(fname, "w") as outfile:
            outfile.write("Node,CC0,CC1,CO\n")
            for node in self.nodes_lev:
                outfile.write(f"{node.num},{node.CC0},{node.CC1},{node.CO}\n")
        return fname

    def print_measures(self):
        """Print a table of the measures of all nodes."""
        print("\t".join(self.nodes_lev[0].print_info(get_labels=True)))
        for node in self.nodes_lev:
            node.print_info(print_labels=False)

    # ------------------------------------------------------------------- graphs
    def gen_graph(self):
        """Directed graph of the circuit with the measures as node attributes.

        Besides the attributes of ``Circuit.gen_graph`` (``lev``, ``gtype``,
        ``ntype``), each node has the SCOAP measures ``CC0``, ``CC1``, ``CO``,
        the STAFAN measures ``C0``, ``C1``, ``S``, ``B0``, ``B1``, and, if known
        from PPSF-CI, the detection probabilities ``DP0`` and ``DP1``.
        """
        graph = super().gen_graph()
        for node in self.nodes_lev:
            attrs = graph.nodes[node.num]
            for name in ("CC0", "CC1", "CO", "C0", "C1", "S", "B0", "B1"):
                attrs[name] = getattr(node, name)
            if "DP0" in node.stat:
                attrs["DP0"] = node.stat["DP0"]
                attrs["DP1"] = node.stat["DP1"]
        return graph

    def write_graph(self, fname):
        """Write ``gen_graph()`` in GML format."""
        nx.write_gml(self.gen_graph(), fname)

    @staticmethod
    def read_graph(fname):
        """Read a graph written by ``write_graph``."""
        return nx.read_gml(fname)
