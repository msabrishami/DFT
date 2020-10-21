# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import argparse
import pdb
import networkx as nx
import math
import time
from random import randint

import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim

def print_nodes(ckt):
    for node in ckt.nodes_lev:
        print(node.num, node.value)



def check_gate_netlist(circuit, total_T=1):

    for t in range(total_T):
        PI_dict = dict()
        PI_list = []

        for PI_num in circuit.input_num_list:
            val = randint(0,1)
            PI_dict["in" + str(PI_num)] = val
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
    parser.add_argument("-ckt", type=str, required=True, help="name of the ircuit, e.g. c17, no extension")
    parser.add_argument("-tp", type=int, required=True, help="name of the ircuit, e.g. c17, no extension")
    parser.add_argument("-cpu", type=int, required=True, help="name of the ircuit, e.g. c17, no extension")
    args = parser.parse_args()

    print("\n======================================================")
    print("Run | circuit: {} | Test Count: {} | CPUs: {}".format(args.ckt, args.tp, args.cpu))
    # start_time = time.time()

    # for each benchmark dataset in ["ISCAS85", "ITC", "EPFL", "LGSynth"]
    # Read a verilog/bench original file
    # Simulate this file using Tejasvi's code which runs modelsim, call it golden
    # convert this file to ckt658 [you have two options:
        # 1. Our new ckt658 https://github.com/yydyid/CircuitTranslator
        # 2. Yuhang's code
    # Use logic_sim on the ckt658 circuit using this platform and the generated golden inputs
    # Compare the golden output with the output of logic_sim
    # Results can determine a few things:
        # is Eda's translator working ok?
        # is Yuhang's translator working ok?
        # is logic_sim working ok?

    # ckt1 = Circuit("c17_orig")
    # ckt2 = Circuit("c17_tran")
    circuit = Circuit(args.ckt)
    circuit.read_circuit()
    circuit.lev()
    exit()
    # circuit.golden_test("../data/golden_IO/c499_golden_IO.txt")
    # check_gate_netlist(circuit, 1000)
    exit()
    inputnum = len(circuit.input_num_list)
    limit = [0, pow(2, inputnum)-1]
    for i in range(100):
        b = ('{:0%db}'%inputnum).format(randint(limit[0], limit[1]))
        list_to_logicsim = []
        for j in range(inputnum):
            list_to_logicsim.append(int(b[j]))
        pdb.set_trace()
        print(circuit.input_num_list)
        print(list_to_logicsim)
        circuit.logic_sim(list_to_logicsim)
        print(b)
        # print_nodes(circuit)

    # observability() need to follow controllability()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    # circuit.STAFAN_CS(100)
    # circuit.STAFAN_B()

    circuit.STAFAN(args.tp, num_proc=args.cpu)
    # circuit.co_ob_info()
    graph = circuit.gen_graph()
    suffix = round(math.log10(args.tp))
    fname = ("10e" + str(suffix)) if (suffix%1==0) else str(args.tp)
    fname = "./../data/graph/" + args.ckt + "_" + fname + ".graphml"
    print("Saving graph in ", fname)
    nx.write_graphml(graph, fname)
    print("Saved!")
    print("Total simulation ime: {:.2f} seconds".format(time.time() - start_time))
    print()

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

if __name__ == "__main__":
    main()
