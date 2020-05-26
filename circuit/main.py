# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import argparse
import pdb
import networkx as nx
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, help="name of the ircuit, e.g. c17, no extension")
    args = parser.parse_args()
    circuit = Circuit(args.ckt)
    circuit.read_circuit()
    circuit.lev()

    #observability() need to follow controllability()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()

    # circuit.STAFAN_CS(100)
    # circuit.STAFAN_B()
    start_time = time.time()
    circuit.STAFAN(10000, num_proc=4)
    circuit.co_ob_info()
    graph = circuit.gen_graph()
    nx.write_graphml(graph, "./../data/graph/" + args.ckt + "10e4.graphml")
    print("Graph Saved")
    # temp = nx.read_graphml("./g_noon.graphml")
    # print(time.time() - start_time)

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

if __name__ == "__main__":
    main()
