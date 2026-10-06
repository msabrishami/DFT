"""Loading netlists: every bundled circuit loads and is structurally consistent."""
import glob
import os

import pytest
from c17_oracle import PATTERNS, c17_outputs

from pycad import config
from pycad.circuit.circuit import Circuit

CKT_FILES = sorted(glob.glob(os.path.join(config.CKT_DIR, "*.ckt")))
VERILOG_FILES = [
    os.path.join(config.ISCAS85_DIR, version, f"c17_syn{version.upper()}.v")
    for version in ("v0", "v1", "v2")
]

# (PI count, PO count) of well-known circuits
KNOWN_IO = {"c17": (5, 2), "c432": (36, 7), "c499": (41, 32), "c880": (60, 26),
            "c1355": (41, 32), "c1908": (33, 25), "c3540": (50, 22),
            "c5315": (178, 123), "c6288": (32, 32)}


def check_structure(circuit):
    """Invariants every loaded circuit must satisfy."""
    for node in circuit.nodes.values():
        # connections are symmetric
        for unode in node.unodes:
            assert node in unode.dnodes, (node.num, unode.num)
        for dnode in node.dnodes:
            assert node in dnode.unodes, (node.num, dnode.num)
        # levels: inputs are 0, every other node is one above its highest fan-in
        assert node.lev is not None
        if node.unodes:
            assert node.lev == max(u.lev for u in node.unodes) + 1
        else:
            assert node.lev == 0
        # a node driving several different gates always drives branches only
        # (a gate may list the same input twice, e.g. AND(x, x))
        if len(set(node.dnodes)) > 1:
            assert all(d.ntype == "FB" for d in node.dnodes), node.num
        # an input has no fan-in, a branch has exactly one
        if node.gtype == "IPT":
            assert not node.unodes
        if node.gtype == "BRCH":
            assert len(node.unodes) == 1
    # lists are consistent with the node types
    assert [n.num for n in circuit.inputs] == [
        n.num for n in circuit.nodes.values() if n.gtype == "IPT"]
    assert all(n.ntype == "PO" for n in circuit.outputs)
    assert len(circuit.outputs) == sum(n.ntype == "PO" for n in circuit.nodes.values())
    # nodes_lev is sorted by level and holds every node once
    levels = [n.lev for n in circuit.nodes_lev]
    assert levels == sorted(levels)
    assert sorted(n.num for n in circuit.nodes_lev) == sorted(circuit.nodes)


@pytest.mark.parametrize("fname", CKT_FILES, ids=os.path.basename)
def test_ckt_files_load(fname):
    circuit = Circuit(fname)
    check_structure(circuit)
    expected = KNOWN_IO.get(circuit.c_name)
    if expected:
        assert (len(circuit.inputs), len(circuit.outputs)) == expected


@pytest.mark.parametrize("fname", VERILOG_FILES, ids=os.path.basename)
def test_verilog_files_load(fname):
    circuit = Circuit(fname)
    check_structure(circuit)
    assert (len(circuit.inputs), len(circuit.outputs)) == KNOWN_IO["c17"]


def test_c17_has_the_textbook_structure():
    circuit = Circuit(os.path.join(config.CKT_DIR, "c17.ckt"))
    gates = [n for n in circuit.nodes.values() if n.ntype in ("GATE", "PO")]
    assert len(gates) == 6
    assert all(n.gtype == "NAND" for n in gates)
    assert sum(n.ntype == "FB" for n in circuit.nodes.values()) == 6
    assert max(n.lev for n in circuit.nodes.values()) == 6


def test_c17_logic_function():
    circuit = Circuit(os.path.join(config.CKT_DIR, "c17.ckt"))
    assert [n.num for n in circuit.inputs] == ["1", "2", "3", "6", "7"]
    for pattern in PATTERNS:
        assert circuit.logic_sim(pattern) == c17_outputs(pattern), pattern


def test_unsupported_format_is_rejected():
    with pytest.raises(NotImplementedError):
        Circuit("somewhere/c17.xyz")


@pytest.mark.parametrize("name", ["c2670", "c7552"])
def test_input_that_is_also_an_output(name):
    """Some ISCAS netlists declare a primary input as an output as well."""
    circuit = Circuit(os.path.join(config.CKT_DIR, "others", f"{name}.ckt"))
    check_structure(circuit)
    both = [n for n in circuit.outputs if n.gtype == "IPT"]
    assert both and all(n in circuit.inputs for n in both)
    # such a node simply reflects the value applied to it
    pattern = [i % 2 for i in range(len(circuit.inputs))]
    values = circuit.logic_sim(pattern)
    for node in both:
        assert values[circuit.outputs.index(node)] == pattern[circuit.inputs.index(node)]


def test_verilog_outputs_follow_the_declaration_order(tmp_path):
    netlist = tmp_path / "order.v"
    netlist.write_text("module t (a, b, z1, z2);\n"
                       "  input a, b;\n"
                       "  output z1, z2;\n"
                       "  or g2 (z2, a, b);\n"     # the gate of z2 comes first
                       "  and g1 (z1, a, b);\n"
                       "endmodule\n")
    circuit = Circuit(str(netlist))
    assert [n.num for n in circuit.outputs] == ["z1", "z2"]
    assert circuit.logic_sim([1, 0]) == [0, 1]
