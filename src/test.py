# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import pdb

ckt = "c17"
circuit = Circuit(ckt)
circuit.read_circuit()
circuit.lev()

#observability() need to follow controllability()
circuit.controllability()
circuit.observability()

# circuit.STAFAN_CS(7000)
# circuit.STAFAN_B()
circuit.STAFAN(10000, num_proc=2)
circuit.co_ob_info()
graph = circuit.gen_graph()


