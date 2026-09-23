"""Gate/node/cell translation of a Verilog netlist (written here, no bundled data needed)."""
import pytest

from pycad.circuit.circuit import Circuit
from pycad.circuit.convert import Converter

NETLIST = """\
module tiny (a, b, c, y);
  input a, b, c;
  output y;
  wire n1, n2;
  NAND2_X1 U1 (.A1(a), .A2(b), .ZN(n1));
  INV_X1 U2 (.A(c), .ZN(n2));
  AND2_X1 U3 (.A1(n1),
              .A2(n2), .Z(y));
endmodule
"""


@pytest.fixture
def netlist(tmp_path):
    path = tmp_path / "tiny.v"
    path.write_text(NETLIST)
    return str(path)


def test_the_test_netlist_is_a_valid_circuit(netlist):
    circuit = Circuit(netlist)
    assert circuit.logic_sim([1, 1, 1]) == [0]  # n1=0 -> y=0
    assert circuit.logic_sim([0, 1, 0]) == [1]  # n1=1, n2=1 -> y=1


def test_gate_node_and_cell_maps(netlist):
    conv = Converter(netlist, "EPFL")
    assert conv.gate2node == {"U1": "n1", "U2": "n2", "U3": "y"}
    assert conv.node2gate == {"n1": "U1", "n2": "U2", "y": "U3"}
    assert conv.gate2cell == {"U1": "NAND2_X1", "U2": "INV_X1", "U3": "AND2_X1"}
    assert conv.gate_to_node("U2") == "n2"
    assert conv.node_to_gate("n2") == "U2"
    assert conv.node_to_gate("n1-2") == "U1"  # a branch belongs to its stem's gate


def test_unknown_format_is_rejected(netlist):
    with pytest.raises(ValueError):
        Converter(netlist, "OTHER")


def test_observation_points_round_trip_through_tmax_format(netlist, tmp_path):
    conv = Converter(netlist, "EPFL")
    out = tmp_path / "ops.tcl"
    conv.nodes_to_tmax_op(["n1", "n2", "y"], out)
    assert out.read_text() == "set_test_point_element { U1/ZN U2/ZN U3/Z  } -type observe\n"
    assert Converter.tmax_op_to_nodes(out) == ["U1/ZN", "U2/ZN", "U3/Z"]


def test_tmax_command_holds_five_points(netlist, tmp_path):
    conv = Converter(netlist, "EPFL")
    out = tmp_path / "ops.tcl"
    conv.nodes_to_tmax_op(["n1", "n2", "y", "n1", "n2", "y"], out)
    lines = out.read_text().splitlines()
    assert len(lines) == 2
    assert lines[1] == "set_test_point_element { U3/Z  } -type observe"
