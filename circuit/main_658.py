

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

parser = argparse.ArgumentParser()
parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
parser.add_argument("-tp", type=int, help="test patterns")
args = parser.parse_args()

circuit = Circuit(args.ckt)
# circuit.read_verilog()
circuit.read_ckt()
circuit.lev()
print("DFS starts")
dfs = DFS(circuit)
all_faults = set()
for x in range(args.tp):
    tp = circuit.gen_tp()
    temp = dfs.single(tp)
    all_faults = temp.union(all_faults)

print("{}/{}".format(len(all_faults), len(circuit.nodes_lev)*2))
# generate 10 random test patterns and corresponding results

# for i in range(1, 11):
#     dfs.fs_exe_golden(tp_num=1, t_mode='rand', no=i, r_mode='b')
# 
# dfs.fs_exe(tp_num=args.tp, t_mode='rand', r_mode='b')
# circuit.FD_new_generator()

