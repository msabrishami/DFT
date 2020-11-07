# -*- coding: utf-8 -*-


import argparse
import pdb
import networkx as nx
import math
import time


from circuit import Circuit
from modelsim_simulator import Modelsim
from load_circuit import LoadCircuit

import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
import config
from checker_logicsim import Checker
from observation import *
import experiments 



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
    parser.add_argument("-tp", type=int, required=False, help="number of tp for random sim")
    parser.add_argument("-cpu", type=int, required=False, help="number of parallel CPUs")
    args = parser.parse_args()

    print("\n======================================================")
    print("Run | circuit: {} | Test Count: {} | CPUs: {}".format(args.ckt, args.tp, args.cpu))
    print("======================================================\n")

    # experiments.exp_check_c432_behavioral(mode="ckt", tp=100)
    # experiments.exp_check_c432_behavioral(mode="v", tp=100)
    # experiments.exp_check_verilog_modelsim()


    circuit = Circuit(args.ckt)
    circuit.read_verilog()
    circuit.lev()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    circuit.STAFAN_CS(args.tp) 
    circuit.STAFAN_B() 
    graph = circuit.gen_graph()
    pdb.set_trace()



    suffix = round(math.log10(args.tp))
    fname = ("10e" + str(suffix)) if (suffix%1==0) else str(args.tp)
    fname = "./../data/graph/NEW_" + args.ckt + "_" + fname + ".graphml"
    print("Saving graph in ", fname)
    nx.write_graphml(graph, fname)
    print("Saved!")
    print()
    # print(circuit)
    # pdb.set_trace()
    # exit() 
    # temp = nx.read_graphml("./g_noon.graphml")

    # circuit.get_full_fault_list()
    # circuit.gen_fault_dic()
    # circuit.get_reduced_fault_list()
    # pattern = circuit.get_random_input_pattern()
    # pfs_list = circuit.pfs(pattern)
    # print (pfs_list)
    # pfs_fault_list = circuit.pfs(pattern)
    # circuit.get_d_correctness()
    # circuit.get_d_coverage()

    #-------------------ATPG part-----------------
    # atpg = ATPG(c_name)
    # atpg.class_main()


def parallel_graph():
    netlists = ["c17", "c432", "c499", "c880", "c1355", "c1908", "c2670",
            "c3540", "c5315", "c6288", "c7552"]



# circuit = Circuit("c17")
# circuit.read_verilog()
# circuit.lev()
# circuit.SCOAP_CC()
# circuit.SCOAP_CO()
# circuit.STAFAN_CS(100) 
# graph = circuit.gen_graph()
# nx.write_graphml(graph, "test.graphml")

if __name__ == "__main__":
    main()
