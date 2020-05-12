# -*- coding: utf-8 -*-

from circuit import Circuit
from atpg_v0 import ATPG
import argparse
import pdb

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, help="name of the ircuit, i.e., c17, c880, no extension")
    args = parser.parse_args()
    circuit = Circuit(args.ckt)
    circuit.read_circuit()
    circuit.lev()
    
    
    pdb.set_trace()

    #observability() need to follow controllability()
    circuit.controllability()
    circuit.observability()    
    # circuit.gen_graph()
    circuit.STAFAN(1000)  


    # circuit.get_full_fault_list()
    # # circuit.gen_fault_dic()
    # # circuit.get_reduced_fault_list()
    # # pattern = circuit.get_random_input_pattern()
    # # pfs_list = circuit.pfs(pattern)
    # # print (pfs_list)
    # # pfs_fault_list = circuit.pfs(pattern)
    # # circuit.get_d_correctness()

    # circuit.get_d_coverage()
    
    # # circuit.get_podem_correctness()
    # circuit.get_podem_coverage()
    # circuit.time_for_podem()
    
    
    #-------------------ATPG part-----------------
    # atpg = ATPG(c_name)
    # atpg.class_main()


if __name__ == "__main__":
    main()
