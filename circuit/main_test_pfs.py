# -*- coding: utf-8 -*-


import argparse
import pdb
#import networkx as nx
import math
import time
from random import randint

from circuit import Circuit
from modelsim_simulator import Modelsim

import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
import config
from checker_logicsim import *
from regular_tp_gen import *
from checker_dfs import *
from FaultSim import *
from parallel_fs import *

def check_gate_netlist(circuit, total_T=1):

    for t in range(total_T):
        PI_dict = dict()
        PI_list = []
        
        PI_num = [x.num for x in circuit.PI]
        for pi in PI_num:
            val = randint(0,1)
            PI_dict["in" + str(pi)] = val
            PI_list.append(val)

        res_beh = c432_sim(PI_dict)
        circuit.logic_sim(PI_list)
        res_ckt = circuit.read_PO()
        if res_beh != res_ckt:
            print("Wrong")
            return False
    print("all test patterns passed")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
    parser.add_argument("-tp", type=int, required=False, help="number of tp for random sim")
    parser.add_argument("-cpu", type=int, required=False, help="number of parallel CPUs")
    args = parser.parse_args()

    print("\n======================================================")
    print("Run | circuit: {} | Test Count: {} | CPUs: {}".format(args.ckt, args.tp, args.cpu))
    print("======================================================\n")

    #Ting-Yu
    
    # for c in ['c17','c432','c499','c880','c1355','c1908','c2670','c3540','c5315','c6288','c7552']:
    #     checker = Checker(c, args.tp)
    #     if checker.check_PI_PO() == False:
    #         print('#################################')
    #         continue
    #     checker.modelsim_wrapper()
    #     checker.check_ckt_verilog('verilog')
    #     checker.check_ckt_verilog('ckt')
    #     print('#################################')
    # #exit()
    

    circuit = Circuit(args.ckt)
    circuit.read_verilog()
    #circuit.read_ckt()
    circuit.lev()

    """ Testing DFS """
    print("PFS starts")
    pfs = PFS(circuit)
    pfs.fs_exe(tp_num=args.tp, t_mode='rand', r_mode='b',fault_list_type=1)

    # circuit.FD_new_generator()
    exit()



def parallel_graph():
    netlists = ["c17", "c432", "c499", "c880", "c1355", "c1908", "c2670",
            "c3540", "c5315", "c6288", "c7552"]

if __name__ == "__main__":
    main()
