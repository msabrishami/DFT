

import argparse
import pdb
import math
import time
from random import randint
from circuit import Circuit
from modelsim_simulator import Modelsim
import sys
import config
# from regular_tp_gen import *
# from checker_dfs import *
# from FaultSim import FaultSim
from deductive_fs import DFS
from load_circuit import LoadCircuit
parser = argparse.ArgumentParser()
parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
parser.add_argument("-tp", type=int, help="test patterns")
args = parser.parse_args()


for ckt in ["c1", "c2", "c3", "c4", "c17", "add2", "x3mult", "c432", "c499", "c880", "c1355"]:
    circuit = Circuit(ckt)
    LoadCircuit(circuit, "ckt")
    circuit.lev()
    print(len(circuit.nodes_lev))
    outfile = open("../data/fault_sim/{}_full_fs.txt".format(ckt), "w")
    for node in circuit.nodes_lev:
        outfile.write("{}@0\n".format(node.num))
        outfile.write("{}@1\n".format(node.num))
    outfile.close()

exit()
circuit = Circuit(args.ckt)
# circuit.read_verilog()
circuit.read_ckt()
circuit.lev()
dfs = DFS(circuit)
all_faults = set()
for x in range(args.tp):
    tp = circuit.gen_tp()
    temp = dfs.single(tp)
    all_faults = temp.union(all_faults)
nd_faults = []
for node in circuit.nodes_lev:
    for x in [0,1]:
        fault = (str(node.num), x)
        if fault not in all_faults:
            nd_faults.append("{}@{}".format(node.num, x))
print("Circuit {}, TP {}".format(args.ckt, args.tp))
print("{}/{}".format(len(all_faults), len(circuit.nodes_lev)*2))
print(",".join(nd_faults))
# generate 10 random test patterns and corresponding results

# for i in range(1, 11):
#     dfs.fs_exe_golden(tp_num=1, t_mode='rand', no=i, r_mode='b')
# 
# dfs.fs_exe(tp_num=args.tp, t_mode='rand', r_mode='b')
# circuit.FD_new_generator()

