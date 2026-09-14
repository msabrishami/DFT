"""Regression test: results must match the output captured from the original code base.

The golden file was produced with a fixed random seed (42) and 20 random test
patterns for each circuit: logic simulation outputs, SCOAP measures, and the
PFS fault coverage with the set of detected faults.
"""
import json
import os
import random

import pytest

from pycad import config
from pycad.circuit.dft_circuit import DFTCircuit
from pycad.fault_simulation.pfs import PFS
from pycad.tp_generator import TPGenerator

GOLDEN = os.path.join(os.path.dirname(__file__), "golden", "baseline.json")
with open(GOLDEN) as f:
    GOLDEN_DATA = json.load(f)


@pytest.mark.parametrize("name", sorted(GOLDEN_DATA))
def test_matches_golden_baseline(name):
    expected = GOLDEN_DATA[name]
    random.seed(42)
    circuit = DFTCircuit(os.path.join(config.CKT_DIR, f"{name}.ckt"))
    tps = TPGenerator(circuit).gen_n_random(20)

    assert len(circuit.nodes_lev) == expected["num_nodes"]
    assert len(circuit.PI) == expected["num_pi"]
    assert len(circuit.PO) == expected["num_po"]

    assert [[int(v) for v in circuit.logic_sim(tp)] for tp in tps] == expected["logic_sim"]

    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    scoap = {str(n.num): [n.CC0, n.CC1, n.CO] for n in circuit.nodes_lev}
    assert scoap == expected["scoap"]

    fc, detected = PFS(circuit).run(tps, faults="all", save_log=False)
    assert float(fc[-1]) == pytest.approx(expected["pfs_fc"])
    assert sorted(str(f) for f in detected) == expected["pfs_detected"]
