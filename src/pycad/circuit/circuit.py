import math
import os
import random
import warnings
from collections import deque

import networkx as nx

from pycad.circuit.circuit_loader import CircuitLoader
from pycad.config import X_VALUE
from pycad.node.node import AND, BRCH, BUFF, IPT, NAND, NOR, NOT, OR, XNOR, XOR


class Circuit:
    """A gate-level combinational circuit that can be logic simulated.

    The circuit is read from a netlist file (``.ckt`` or Verilog) and levelized.
    Every net is a :class:`~pycad.node.node.Node`; every connection from a stem
    to one of several gates goes through a fan-out branch node.

    Attributes
    ----------
    STD_NODE_LIB : dict
        Gate type name -> node class used when reading a netlist.
    c_fname : str
        Netlist file name, with path and format.
    c_name : str
        Circuit name: the file name without path and format.
    nodes : dict
        Node number (str) -> node object.
    nodes_lev : list
        All nodes ordered by level, i.e. in an order that is ready for simulation.
    inputs : list
        Primary input nodes, in netlist order.
    outputs : list
        Primary output nodes, in netlist order.
    """

    STD_NODE_LIB = {'AND':AND, 
                    'XOR':XOR,
                    'OR': OR, 
                    'XNOR':XNOR,
                    'BUFF':BUFF,
                    'BRCH':BRCH,
                    'NOR':NOR,
                    'NOT':NOT,
                    'NAND':NAND,
                    'IPT':IPT}


    def __init__(self, c_fname, std_node_lib=STD_NODE_LIB):
        self.c_fname = c_fname
        self.c_name = os.path.basename(c_fname).split('.')[0]
        self.nodes = {}
        self.nodes_lev = []
        self.inputs = []
        self.outputs = []

        self._load(c_fname, std_node_lib)
        self.levelize()

    def _load(self, netlist_fname, std_node_lib):
        CircuitLoader(self, netlist_fname, std_node_lib)

    def levelize(self):
        """Assign a level to every node and order ``nodes_lev`` by level.

        Inputs are at level 0 and every other node is one level above its
        highest fan-in. Fan-out branches count as gates: the level of a branch
        is the level of its stem plus one. Levels of all nodes are recomputed,
        so this can be called again after the circuit was modified.

        Raises
        ------
        ValueError
            If the circuit has a combinational loop.
        """
        pending = {}  # node -> number of fan-ins whose level is still unknown
        ready = deque()
        for node in self.nodes.values():
            node.lev = None
            pending[node] = len(node.unodes)
            if not node.unodes:
                if node.gtype != "IPT":
                    warnings.warn(
                        f"Node {node.num} has no fan-in, its level is set to zero", stacklevel=2)
                node.lev = 0
                ready.append(node)

        while ready:
            node = ready.popleft()
            for dnode in node.dnodes:
                pending[dnode] -= 1
                if pending[dnode] == 0:
                    dnode.lev = max(unode.lev for unode in dnode.unodes) + 1
                    ready.append(dnode)

        unleveled = [node.num for node in self.nodes.values() if node.lev is None]
        if unleveled:
            raise ValueError(f"The circuit has a combinational loop through nodes {unleveled[:5]}")

        self.nodes_lev = sorted(self.nodes.values(), key=lambda x: x.lev)

    def levelize_backward(self):
        """Distance of every node to the nearest primary output.

        Returns
        -------
        dict
            Node -> minimum number of connections to a primary output. Nodes
            that do not reach an output (dangling logic) map to ``math.inf``.
        """
        dist = {node: math.inf for node in self.nodes.values()}
        queue = deque()
        for po in self.outputs:
            dist[po] = 0
            queue.append(po)

        while queue:
            node = queue.popleft()
            for unode in node.unodes:
                if dist[unode] == math.inf:
                    dist[unode] = dist[node] + 1
                    queue.append(unode)

        return dist

    def __str__(self):
        res = ["Circuit name: " + self.c_name]
        res.append("#Nodes: " + str(len(self.nodes)))
        res.append("#PI: " + str(len(self.inputs)) + " >> ") 
        res.append("\t" + str([x.num for x in self.inputs]))
        res.append("#PO: " + str(len(self.outputs)) + " >> ")
        res.append("\t" + str([x.num for x in self.outputs]))

        for node in self.nodes_lev:
            res.append(str(node))
        return "\n".join(res)

    def get_rand_nodes(self, count=1):
        """Return ``count`` different nodes of the circuit, chosen at random."""
        if count > len(self.nodes):
            raise ValueError(
                f"Cannot choose {count} nodes from a circuit with {len(self.nodes)} nodes")
        return random.sample(self.nodes_lev, k=count)

    def _simulate(self, tp, imply, fault=None):
        """Apply ``tp`` to the inputs and evaluate all nodes in level order.

        ``imply`` is the name of the node method to use (``imply``, ``imply_t``
        or ``imply_b``). With a ``fault``, the value of the faulty node is
        overwritten right after it is computed (bit-parallel values only).
        """
        if len(tp) != len(self.inputs):
            raise ValueError(
                f"The pattern has {len(tp)} values but the circuit has {len(self.inputs)} inputs")
        applied = {pi.num: value for pi, value in zip(self.inputs, tp, strict=True)}

        for node in self.nodes_lev:
            if node.gtype == "IPT":
                getattr(node, imply)(applied[node.num])
            else:
                getattr(node, imply)()
            if fault is not None and node.num == fault.node_num:
                node.value = 0 if fault.stuck_val == '0' else node.bitwise_not

        return [po.value for po in self.outputs]

    def logic_sim(self, tp):
        """Two-valued logic simulation of one pattern.

        Parameters
        ----------
        tp : list
            0/1 values, in the order of ``self.inputs``.

        Returns
        -------
        list
            Values of the outputs, in the order of ``self.outputs``.
        """
        if X_VALUE in tp:
            raise ValueError("The pattern contains X, use logic_sim_t() instead")
        return self._simulate(tp, "imply")

    def logic_sim_t(self, tp):
        """Three-valued logic simulation of one pattern (0, 1 or ``X_VALUE``).

        Parameters and result are as in ``logic_sim``.
        """
        return self._simulate(tp, "imply_t")

    def logic_sim_bitwise(self, tp, fault=None):
        """Bit-parallel logic simulation: every bit of a value is a separate pattern.

        Parameters
        ----------
        tp : list of int
            One integer per input, in the order of ``self.inputs``.
        fault : Fault, optional
            A single stuck-at fault to inject, e.g. node ``43`` stuck at ``'0'``.

        Returns
        -------
        list of int
            Values of the outputs, in the order of ``self.outputs``.
        """
        return self._simulate(tp, "imply_b", fault)

    def logic_sim_file(self, in_fname, out_fname):
        """Simulate the patterns of a file and write patterns with responses.

        The input file has a header line followed by one comma-separated
        pattern per line (see ``TPGenerator``). The output file lists the input
        and output node names and then, for every pattern, a ``Test # = k`` line,
        the pattern and the response. ``check_golden`` reads this format.
        """
        with open(in_fname) as fr, open(out_fname, 'w') as fw:
            fw.write('Inputs: ' + ",".join('N' + str(node.num) for node in self.inputs) + "\n")
            fw.write('Outputs: ' + ",".join('N' + str(node.num) for node in self.outputs) + "\n")
            next(fr)  # header
            for i, line in enumerate(fr, start=1):
                line = line.rstrip('\n')
                response = self.logic_sim([int(x) for x in line.split(',')])
                fw.write(f'Test # = {i}\n')
                fw.write(line + '\n')
                fw.write(",".join(str(value) for value in response) + "\n")

    def write_stil(self, in_fname, out_fname):
        """Simulate the patterns of a file and write them as STIL capture vectors.

        The input file is as for ``logic_sim_file``.
        """
        with open(in_fname) as fr, open(out_fname, 'w') as fw:
            fw.write("PI:" + ",".join(node.num for node in self.inputs) + "\n")
            fw.write("PO:" + ",".join(node.num for node in self.outputs) + "\n")
            next(fr)  # header
            for idx, line in enumerate(fr):
                tp = line.strip().split(",")
                response = self.logic_sim([int(x) for x in tp])
                fw.write(f'"pattern {idx}": Call "capture" {{\n')
                fw.write('"_pi"=' + "".join(tp) + ";\n")
                fw.write('      "_po"=' + "".join("H" if v == 1 else "L" for v in response))
                fw.write("; } \n")

    def check_golden(self, golden_io_filename):
        """Compare the logic simulation of this circuit with a golden file.

        The golden file has the format written by ``logic_sim_file``, e.g. from
        a reference simulator.

        Returns
        -------
        bool
            True if the input order matches and all responses are the same.
        """
        with open(golden_io_filename) as infile:
            lines = [line.strip() for line in infile]
        golden_inputs = [x[1:] for x in lines[0][8:].split(',')]
        golden_outputs = [x[1:] for x in lines[1][9:].split(',')]
        if golden_inputs != [node.num for node in self.inputs]:
            return False
        if golden_outputs != [node.num for node in self.outputs]:
            return False

        for t in range((len(lines) - 2) // 3):
            test_in = [int(x) for x in lines[3 * t + 3].split(',')]
            test_out = [int(x) for x in lines[3 * t + 4].split(',')]
            if self.logic_sim(test_in) != test_out:
                return False
        return True

    def make_num_int(self):
        """Map every node number to its index in ``nodes_lev``."""
        return {node.num: idx for idx, node in enumerate(self.nodes_lev)}

    def gen_graph(self):
        """Directed graph of the circuit, with an edge from every fan-in to its node.

        Graph nodes are the node numbers and carry the attributes ``lev``,
        ``gtype`` and ``ntype``.
        """
        graph = nx.DiGraph()
        for node in self.nodes_lev:
            graph.add_node(node.num, lev=node.lev, gtype=node.gtype, ntype=node.ntype)
            for unode in node.unodes:
                graph.add_edge(unode.num, node.num)
        return graph

    def get_node_attr(self, node_attr):
        """List of the attribute ``node_attr`` of every node, in level order."""
        return [getattr(node, node_attr) for node in self.nodes_lev]

    def read_outputs(self):
        """Values of the outputs after a simulation: node number (str) -> value."""
        return {str(node.num): node.value for node in self.outputs}
