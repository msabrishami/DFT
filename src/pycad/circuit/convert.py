"""Translate between gate names, node numbers and cell names of a Verilog netlist.

A Verilog netlist names every gate (instance) while PyCAD names every node by
the net the gate drives. Tools such as Synopsys TestMAX speak of gates, so
test points have to be translated between the two views.
"""
import re

from pycad.circuit.circuit_loader import CircuitLoader
from pycad.library import cells

_TMAX_POINT = re.compile(r"(?:(?:[A-Z]+\d*\_\d+)|(?:[A-Z]+\d+))\/[A-Z]+")


class Converter:
    """Maps between gates, nodes and cells of one Verilog netlist.

    Parameters
    ----------
    verilog_fname : str
        Netlist whose gates use named pins, e.g. ``.ZN(n1)``. The output pin
        must be the last one of each gate.
    verilog_format : str
        ``"EPFL"`` (NanGate 15nm cells) or ``"ISCAS85"`` (default cells).

    Attributes
    ----------
    gate2node, node2gate : dict
        Gate (instance) name <-> number of the node the gate drives.
    gate2cell : dict
        Gate name -> cell name, e.g. ``NAND2_X1``.
    """

    def __init__(self, verilog_fname, verilog_format):
        if verilog_format == "EPFL":
            self.cell_pins = cells.NanGate_15nm()
        elif verilog_format == "ISCAS85":
            self.cell_pins = cells.default()
        else:
            raise ValueError(f"The verilog format {verilog_format} is not supported")

        self.gate2node = {}
        self.node2gate = {}
        self.gate2cell = {}
        self._read_gates(verilog_fname)

    def _read_gates(self, verilog_fname):
        for statement in CircuitLoader.read_verilog_statements(verilog_fname):
            x_type, _ = CircuitLoader.read_verilog_syntax(statement)
            if x_type != "GATE":
                continue

            cell, gate, arguments = CircuitLoader.GATE_INSTANCE.match(statement).groups()
            pins = CircuitLoader.named_pins(arguments)
            if not pins:
                raise ValueError(f"Cannot parse pins in line: {statement.strip()}")

            node = pins[-1][1]
            self.gate2node[gate] = node
            self.node2gate[node] = gate
            self.gate2cell[gate] = cell

    def gate_to_node(self, gate):
        """Number of the node driven by ``gate``."""
        return self.gate2node[gate]

    def node_to_gate(self, node):
        """Name of the gate that drives ``node``. Fan-out branches (``12-1``) map to their stem's gate."""
        return self.node2gate[node.split("-")[0]]

    def nodes_to_tmax_op(self, nodes, output_fname):
        """Write observation points as TestMAX ``set_test_point_element`` commands.

        Parameters
        ----------
        nodes : list of str
            Numbers of the nodes to observe. Five points go on each command line.
        output_fname : str
            File to write.
        """
        with open(output_fname, "w") as outfile:
            for start in range(0, len(nodes), 5):
                points = []
                for node in nodes[start:start + 5]:
                    gate = self.node2gate[node]
                    out_pin = self.cell_pins[self.gate2cell[gate]][-1]
                    points.append(f"{gate}/{out_pin}")
                outfile.write("set_test_point_element { " + " ".join(points)
                              + "  } -type observe\n")

    @staticmethod
    def tmax_op_to_nodes(tmax_fname):
        """Read a TestMAX observation point file, returning the ``gate/pin`` names it lists."""
        points = []
        with open(tmax_fname) as infile:
            for line in infile:
                points.extend(_TMAX_POINT.findall(line))
        return points
