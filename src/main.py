# -*- coding: utf-8 -*-
from circuit import Circuit
import argparse
from atpg_v0 import ATPG

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("c_name", type = str, help = "Please enter the name of circuit, i.e., c17, c880, no extensions required")
    args = parser.parse_args()
    c_name = args.c_name
    circuit = Circuit(c_name)
    circuit.read_circuit()
    circuit.lev()

    #observability() need to follow controllability()
    circuit.controllability()
    circuit.observability()    
    # circuit.STAFAN()  


    


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
main()
