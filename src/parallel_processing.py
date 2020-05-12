# -*- coding: utf-8 -*-
from circuit import Circuit
import argparse
"""
When MT.cpp passes "circuit_name -1 -1" to this function, it returns the input_cnt of the circuit.
When MT.cpp passes "circuit_name thread_cntm idx" to this function, it generates fault dictionary on one thread of MT.cpp
"""
def parallel_processing():
    parser = argparse.ArgumentParser()
    parser.add_argument("c_name", type = str, help = "Please enter the name of circuit, i.e., c17, c880, no extensions required")
    parser.add_argument("thread_cnt", type = int, help = "-1 if you just want to get the input count, otherwise the number of threads running")
    parser.add_argument("idx", type = int, help = "-1 if you just want to get the input count, otherwise idx of thread")
    args = parser.parse_args()
    idx = args.idx
    c_name = args.c_name
    thread_cnt = args.thread_cnt
    circuit = Circuit(c_name)
    circuit.read_circuit()
    if (thread_cnt == -1):
        print(circuit.input_cnt)
        exit(0)
    else:
        circuit.lev()
        circuit.get_full_fault_list()
        circuit.gen_fault_dic_multithreading(thread_cnt, idx)

parallel_processing()    


