# -*- coding: utf-8 -*-


import argparse
import pdb
# import networkx as nx
import math
import time
from random import randint

from circuit import Circuit
from modelsim_simulator import Modelsim


import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
import config
from checker_logicsim import Checker
from observation import *

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

    circuit = Circuit(args.ckt)
    circuit.read_verilog()
    # circuit.read_ckt()
    circuit.lev()

    """ Testing Read Verilog """ 
    # tp_in_fname  = circuit.c_name + "-tp-input-"  + str(args.tp) + ".log"
    # tp_out_fname = circuit.c_name + "-tp-output-" + str(args.tp) + ".log"
    # tp_stil_fname = circuit.c_name + "-tp-" + str(args.tp) + "-stil.log"
    # circuit.gen_tp_file(args.tp, fname=tp_in_fname)
    # circuit.logic_sim_file(in_fname=tp_in_fname, out_fname=tp_stil_fname, stil=True)
    # Test Circuit LogicSim
    # check_gate_netlist(circuit, 3000) # c432
    
    """ Testing with Modelsim Results """ 
    # for c in ["c17", "c432", "c499"]:
    #     checker = Checker()
    #     checker.run(c, args.tp)
    #     checker.run_check(args.tp)
    # sim = Modelsim()
    # sim.project(circuit)
    # tp_fname = sim.gen_rand_tp(tp_count=args.tp, tp_fname="tp-input-" + str(args.tp) + ".log")
    # sim.gen_tb(tp_fname)
    # sim.simulation()


    """ Testing PFS """
    # circuit.get_full_fault_list()
    # circuit.pfs_multiple(fname="c17_full_tp_b.txt", mode="b")

    """ Testing DFS for single pattern """
    # test1 = circuit.gen_tp()
    # print(test1)
    # temp = circuit.dfs_single(test1)
    # print("------------------------")
    # print(temp) 

    """ Testing DFS for all faults with all patterns """ 
    # Here we need a helper function to create a pattern for full test of a circuit
    # tp_fname = circuit.c_name + "-tp-" + str(args.tp) + ".log"
    # report_fname = circuit.c_name + "-tp-" + str(args.tp) + "-fault-sim.log"

    # circuit.gen_tp_file(
    #         args.tp, 
    #         fname=tp_fname,
    #         mode = "b")
    # circuit.dfs_multiple_separate(
    #         # fname_tp="../data/modelsim/c17/input/c17_full_tp_b.txt",
    #         fname_tp = tp_fname,
    #         # fname_log="./c17_all_dfs.log",
    #         fname_log=report_fname,
    #         mode='b')
    # circuit.FD_new_generator()
    # exit()

    """ Observation Point Insertion """  
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    circuit.STAFAN_CS(args.tp)
    circuit.STAFAN_B()
    circuit.co_ob_info() 
    exp1_res_arit = {}
    exp1_res_geom = {}
    for node in circuit.nodes_lev:
        if node.lev < 5:
            continue

        print("================================")

        if node.B > 0.2:
            print(node.num, "SKIPPED")
            continue

        print(node.num, node.B)
        a_all, g_all, a_tot, g_tot = approach_1(circuit, node)
        # stat_arithmetic = [round(x, 2) for x in stat_arithmetic]
        # stat_geometric = [round(x, 2) for x in stat_geometric]
        print("Node num: {}\tNode Lev: {}\nArithmetic:\t {}\t\tGeometric: \t {}".format(
            node.num, node.lev, 
            [round(x, 3) for x in a_tot], [round(x, 3) for x in g_tot]))
        for idx in range(len(a_all)):
            if a_all[idx][2] < 0.001:
                continue
            print("{} {}".format(circuit.nodes_lev[idx].num, circuit.nodes_lev[idx].lev), end="")
            print("\t\t", [round(x, 3) for x in a_all[idx]], end="\t\t")
            print("\t\t", [round(x, 3) for x in g_all[idx]])
    TPI_stat(circuit, HTO_th=config.HTO_TH, HTC_th=config.HTC_TH)

    nodes_HTO = []
    for node in circuit.nodes_lev:
        if (node.stat["SS@1"]=="HTO") or (node.stat["SS@1"]=="HTO"):
            nodes_HTO.append(node)
    print("Initial HTO count: {}".format(len(nodes_HTO)))

    for target in nodes_HTO: 
        print("Target: {}\tB1={:.2f} B2={:.2f} \tdelta={}".format(
            target.num, target.B1, target.B0, 
            NVIDIA_count(circuit, target, 0.05, 0.05))
            )
      
    exit()

    # circuit.STAFAN(args.tp, num_proc=args.cpu)

    graph = circuit.gen_graph()
    suffix = round(math.log10(args.tp))
    fname = ("10e" + str(suffix)) if (suffix%1==0) else str(args.tp)
    fname = "./../data/graph/NEW_" + args.ckt + "_" + fname + ".graphml"
    print("Saving graph in ", fname)
    nx.write_graphml(graph, fname)
    print("Saved!")
    # print("Total simulation ime: {:.2f} seconds".format(time.time() - start_time))
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
