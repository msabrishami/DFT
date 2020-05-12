# -*- coding: utf-8 -*-
from circuit import Circuit
import argparse
import multiprocessing
from multiprocessing import Process, Pipe
"""
Multiprocessing calculate STAFAN controllability for each node.
"""

def control_thread(conn, c_name, thread_cnt, idx):
    circuit = Circuit(c_name)
    circuit.read_circuit()
    circuit.lev()
    one_count_list, zero_count_list, sen_count_list = circuit.STAFAN_multithreading(thread_cnt, idx)
    conn.send((one_count_list, zero_count_list, sen_count_list))
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("c_name", type = str, help = "Please enter the name of circuit, i.e., c17, c880, no extensions required")
    args = parser.parse_args()
    c_name = args.c_name
    circuit = Circuit(c_name)
    circuit.read_circuit()
    circuit.lev()
    nodes_cnt = circuit.nodes_cnt
    total_pattern = pow(2, circuit.input_cnt)
    thread_cnt = multiprocessing.cpu_count()
    process_list = []
    for i in range(thread_cnt):
    # for idx in process_list:
        parent_conn, child_conn = Pipe()
        p = Process(target = control_thread, args =(child_conn, c_name, thread_cnt, i, ))
        p.start()
        process_list.append((p, parent_conn))
    
    one_count_list = [0] * nodes_cnt
    zero_count_list = [0] * nodes_cnt
    sen_count_list = [0] * nodes_cnt
    for p, conn in process_list:
        tup = conn.recv()
        for i in range(len(tup[0])):
            one_count_list[i] += tup[0][i]
            zero_count_list[i] += tup[1][i]
            sen_count_list[i] += tup[2][i]
        p.join()
    for i in range(len(circuit.nodes_lev)):
        circuit.nodes_lev[i].one_control = one_count_list[i] / total_pattern
        circuit.nodes_lev[i].zero_control = zero_count_list[i] / total_pattern
        circuit.nodes_lev[i].sen_p = sen_count_list[i] / total_pattern
        # print (circuit.nodes_lev[i].one_control, circuit.nodes_lev[i].zero_control,circuit.nodes_lev[i].sen_p)
    circuit.STAFAN_observability()



