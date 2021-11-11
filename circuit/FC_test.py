import utils
from convert import Converter
from fault_coverage import FC_fault_simulation, FC_test_pattern
from multiprocessing import Process, Pipe
from fault_sim import FaultList_2
from ppsf_sim import PPSF
from parallel_fs import PFS
import convert
from load_circuit import LoadCircuit
from observation import OPI
import observation
from checker_logicsim import Checker
import config
import argparse
import pdb
import networkx as nx
import math
import time
import os
import numpy as np
import copy

from circuit import Circuit
from modelsim_simulator import Modelsim

from regular_tp_gen import regular_tp_gen


import sys
sys.path.insert(1, "../data/netlist_behavioral")

### These functions are copied from main_personal.py ###


def read_tp_file(fname):
    infile = open(fname)
    lines = infile.readlines()
    tps = []
    for line in lines[1:]:
        tps.append(line.strip().split(","))

    return tps


def gen_tps():
    # Gen tps and all the required folder!
    for ckt in CKTs:
        print(ckt)
        circuit = Circuit(ckt)
        LoadCircuit(circuit, "ckt")
        circuit.lev()
        dfs = DFS(circuit)
        dfs.fs_folder()
        for idx in range(3):
            if len(circuit.PI) < 6:
                test_count = 4
            else:
                test_count = 10
            circuit.gen_tp_file(test_count=test_count,
                                fname="../data/fault_sim/{}/input/{}_test_count-{}_id-{}.tp".format(
                                    ckt, ckt, str(test_count), str(idx)))
            circuit.gen_tp_file(test_count=1,
                                fname="../data/fault_sim/{}/input/{}_test_count-1_id-{}.tp".format(
                                    ckt, ckt, str(idx)))


def golden_fault_sim():
    import glob
    for ckt in CKTs:
        print(ckt)
        circuit = Circuit(ckt)
        LoadCircuit(circuit, "ckt")
        circuit.lev()
        dfs = DFS(circuit)
        files = glob.glob("../data/fault_sim/{}/input/*.tp".format(ckt))
        files.sort()
        for tp_fname in files:
            tps = read_tp_file(tp_fname)
            tps = [[int(x) for x in tp] for tp in tps]
            fs_fname = tp_fname.split("/")[-1][:-2] + "fs"
            print(fs_fname)
            dfs.multiple(pattern_list=tps, fname_log=fs_fname)


def ppsf_thread(conn, ckt_name, tp_count, tp_fname, fault_fname):
    ckt = Circuit(ckt_name)
    ckt.lev()
    tps = circuit.gen_tp_file(tp_count, fname=tp_fname)
    fault_sim = PPSF(circuit)
    fault_sim.fault_list.add_file(fault_fname)
    fault_sim.fs_exe(tp_fname)
    conn.send(fault_sim.fault_list)


def pars_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=False,
                        help="ckt file address")
    parser.add_argument("-v", type=str, required=False,
                        help="verilog file address")
    parser.add_argument("-synv", type=str, required=False, help="syn ver")
    parser.add_argument("-tp", type=int, required=False,
                        help="tp count for random sim")
    parser.add_argument("-fault", type=int, required=False, help="fault count")
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


if __name__ == '__main__':

    args = pars_args()

    config.HTO_TH = args.HTO_th if args.HTO_th else config.HTO_TH
    config.HTC_TH = args.HTC_th if args.HTC_th else config.HTC_TH

    circuit = read_circuit(args)
    ckt_name = args.ckt + "_" + args.synv if args.synv else args.ckt

    print("======================================================")
    print("Run | circuit: {} | Test Count: {}/{} | CPUs: {}".format(
        circuit.c_fname, args.tp, args.tpLoad, args.cpu))

    if args.func == "fctp":
        circuit.lev()
        path = "../data/patterns/{}_TP{}.tp".format(circuit.c_name, args.tp)
        tps = circuit.gen_tp_file(args.tp, path)
        circuit.STAFAN_CS(tp = args.tp) 
        circuit.STAFAN_B() 
        # circuit.STAFAN(args.tp)

        fctp = FC_test_pattern(
            circuit=circuit, fault_mode='full', fault_list=[],tps_count=len(tps))
        fctp.calculate()

    if args.func == "fcfs":
        pass
