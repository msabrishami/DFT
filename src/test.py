# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import pdb

ckt = "c17"
circuit = Circuit(ckt)
circuit.read_circuit()
circuit.lev()

circuit.SCOAP_CC()
# circuit.observability()
circuit.SCOAP_CO()

# circuit.STAFAN_CS(100)
# circuit.STAFAN_B()
circuit.STAFAN(1000, num_proc=8)
circuit.co_ob_info()
graph = circuit.gen_graph()
nx.write_graphml(graph, "./g_noon.graphml")
