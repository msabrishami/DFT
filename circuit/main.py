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

    circuit = Circuit(args.ckt)
    LoadCircuit(circuit, "ckt")
    circuit.lev()

if __name__ == "__main__":
    main()
