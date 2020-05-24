# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import pdb
import networkx as nx


all_ckts = ["c17", "c432", "c499", "c880", "c1355", "c5315", "c6288"]
# "c7552", "c2670", "c1908", "c3540",
all_ckts = ["c1355"]
for ckt in all_ckts:
    print("READING CIRCUIT: ", ckt)
    circuit = Circuit(ckt)
    circuit.read_circuit()
    circuit.lev()
    # circuit.STAFAN_B()
    circuit.STAFAN(10000, num_proc=2)
    circuit.get_hist("C1", plot=False)
'''
ckt = "c432"
circuit = Circuit(ckt)
circuit.read_circuit()
circuit.lev()

circuit.SCOAP_CC()
# circuit.observability()
circuit.SCOAP_CO()

# circuit.STAFAN_CS(100)
circuit.co_ob_info()
graph = circuit.gen_graph()
nx.write_graphml(graph, "./g_noon.graphml")
'''
