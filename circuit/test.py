# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import pdb
import networkx as nx

import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
'''
all_ckts = ["c17", "c432", "c499", "c880", "c1355", "c6288"]
all_ckts = ["c3540"]
# "c5315", "c7552", "c2670" "c1908",
# all_ckts = ["c432"]
for ckt in all_ckts:
    print("READING CIRCUIT: ", ckt)
    circuit = Circuit(ckt)
    circuit.read_circuit()
    circuit.lev()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    circuit.STAFAN_CS(100)
    circuit.STAFAN_B()
    # circuit.STAFAN(10)# , num_proc=2)
    # circuit.co_ob_info()
    circuit.get_hist("CC0", plot=False)
'''
ckt = "c432"
circuit = Circuit(ckt)
circuit.read_circuit()
circuit.lev()

'''




circuit.STAFAN_CS(1000)
circuit.STAFAN_B()
graph = circuit.gen_graph()
nx.write_graphml(graph, "./g_noon.graphml")
temp = nx.read_graphml("./g_noon.graphml")
'''
