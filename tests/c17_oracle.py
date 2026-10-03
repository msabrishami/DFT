"""The ISCAS c17 circuit written out by hand, shared by the tests as an independent oracle.

Nothing here uses the library's gates or simulators. Patterns list the inputs in the
order of the netlist: 1, 2, 3, 6, 7.
"""
import itertools
import os

from pycad import config

C17 = os.path.join(config.CKT_DIR, "c17.ckt")
PATTERNS = [list(p) for p in itertools.product([0, 1], repeat=5)]  # all 32, counting order


def nand(a, b):
    return 1 - (a & b)


def c17_node_values(pattern, forced=None):
    """Values of all 17 nodes of c17; ``forced = (node, value)`` overrides one node's value."""
    values = {}

    def put(node, value):
        values[node] = forced[1] if forced and forced[0] == node else value

    for node, value in zip(["1", "2", "3", "6", "7"], pattern, strict=True):
        put(node, value)
    put("8", values["3"])
    put("9", values["3"])
    put("10", nand(values["1"], values["8"]))
    put("11", nand(values["9"], values["6"]))
    put("14", values["11"])
    put("15", values["11"])
    put("16", nand(values["2"], values["14"]))
    put("20", values["16"])
    put("21", values["16"])
    put("19", nand(values["15"], values["7"]))
    put("22", nand(values["10"], values["20"]))
    put("23", nand(values["21"], values["19"]))
    return values


def c17_outputs(pattern, forced=None):
    """The outputs [22, 23] of c17."""
    values = c17_node_values(pattern, forced)
    return [values["22"], values["23"]]
