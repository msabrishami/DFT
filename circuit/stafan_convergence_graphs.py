# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as plt
import config
import argparse

from circuit import Circuit

import sys
sys.path.insert(1, "../data/netlist_behavioral")


def read_tp_file(fname):
    infile = open(fname)
    lines = infile.readlines()
    tps = []
    for line in lines[1:]:
        tps.append(line.strip().split(","))

    return tps


def pars_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=False,
                        help="ckt file address")
    parser.add_argument("-v", type=str, required=False,
                        help="verilog file address")
    parser.add_argument("-synv", type=str, required=False, help="syn ver")
    parser.add_argument("-tp", type=int, required=False,
                        help="tp count for random sim")
    parser.add_argument("-tpLoad", type=int, required=False,
                        help="tp count for loading STAFAN")
    parser.add_argument("-cpu", type=int, required=False,
                        help="number of parallel CPUs")
    parser.add_argument("-func", type=str, required=False,
                        help="What operation you want to run")
    parser.add_argument("-OPIalg", type=str,
                        required=False, help="OPI Algorithm")
    parser.add_argument("-Bth", type=float, required=False, default=0.1,
                        help="Obsv. threshold for OPI candidate selection")
    parser.add_argument("-HTO_th", type=float, required=False, default=None,
                        help="Obsv. threshold for OPI candidate selection")
    parser.add_argument("-HTC_th", type=float, required=False, default=None,
                        help="Ctrl. threshold for OPI candidate selection")
    parser.add_argument("-opCount", type=int, required=False,
                        default=None, help="OP count")
    parser.add_argument("-op_fname", type=str, required=False,
                        default=None, help="OP file name")
    parser.add_argument("-TPI_num", type=int, required=False, default=None,
                        help="Number of TPI candidates specified")
    args = parser.parse_args()

    return args


def read_circuit(args):
    circuit = None
    if args.ckt:
        circuit = Circuit(args.ckt)

    elif args.v:
        circuit = Circuit(args.v)
    return circuit


def node_info(node):

    node_parameters = {}
    node_parameters['C0'] = node.C0
    node_parameters['C1'] = node.C1
    node_parameters['S'] = node.S
    node_parameters['B0'] = node.B0
    node_parameters['B1'] = node.B1
    node_parameters['CB0'] = node.CB0
    node_parameters['CB1'] = node.CB1
    node_parameters['B'] = node.B
    return node_parameters


if __name__ == '__main__':

    args = pars_args()

    config.HTO_TH = args.HTO_th if args.HTO_th else config.HTO_TH
    config.HTC_TH = args.HTC_th if args.HTC_th else config.HTC_TH

    circuit = read_circuit(args)
    ckt_name = args.ckt + "_" + args.synv if args.synv else args.ckt

    print("======================================================")
    print("Run | circuit: {} | Test Count: {}/{} | CPUs: {}".format(
        circuit.c_fname, args.tp, args.tpLoad, args.cpu))

    circuit.lev()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()

    processor_numbers = 8
    tp_no = processor_numbers
    step = 10
    limit = 200_000
    node_num = 12

    parameters = ['C0', 'C1', 'S', 'B0', 'B1', 'CB0', 'CB1', 'B']
    draw_graph_for = 'C0'

    result_dict = {}
    for node in circuit.nodes_lev:
        for p in parameters:
            result_dict[(node, p)] = []

    tp_no_seq = []

    while tp_no < limit:
        circuit.STAFAN(tp_no, 8)
        tp_no_seq.append(tp_no)
        tp_no *= step
        for node in circuit.nodes_lev:
            for p in parameters:
                result_dict[(node, p)].append(node_info(node)[p])

    test_array = result_dict[(circuit.nodes_lev[node_num], draw_graph_for)]
    sns.scatterplot(x=tp_no_seq, y=test_array)
    t = sns.lineplot(x=tp_no_seq, y=test_array)
    ax = plt.gca()
    ax.grid(True, which='both')

    t.set_ylabel(f'{draw_graph_for}')
    t.set_xlabel('No. of tests')
    t.set_title(f'{draw_graph_for} of node {circuit.nodes_lev[node_num]}')
    t.set_yscale('log')
    t.set_xscale('log')

    plt.show()