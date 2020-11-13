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

    path_tp = "../data/modelsim/patterns/" + args.ckt + "_98_tp_b.tp"
    path_stil = args.ckt + "_98.stil"

    circuit = Circuit(args.ckt)
    LoadCircuit(circuit, "v")
    circuit.lev()
    circuit.logic_sim_file(in_fname = path_tp, out_fname = path_stil, out_format="STIL")
    # circuit.logic_sim_file(in_fname = path1, out_fname = "c432-658.txt", out_format="658")
    # circuit.gen_tp_file(args.tp)
    exit()

    # graph = circuit.gen_graph()
    # suffix = round(math.log10(args.tp))
    # fname = ("10e" + str(suffix)) if (suffix%1==0) else str(args.tp)
    # fname = "./../data/graph/NEW_" + args.ckt + "_" + fname + ".graphml"
    # print("Saving graph in ", fname)
    # nx.write_graphml(graph, fname)
    # print("Saved!")
    # print()
    # temp = nx.read_graphml("./g_noon.graphml")

def parallel_graph():
    netlists = ["c17", "c432", "c499", "c880", "c1355", "c1908", "c2670",
            "c3540", "c5315", "c6288", "c7552"]

if __name__ == "__main__":
    main()
