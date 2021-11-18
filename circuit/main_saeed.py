# -*- coding: utf-8 -*-

import utils
from convert import Converter
import experiments as exp
from multiprocessing import Process, Pipe
from fault_sim import FaultList_2
from ppsf import PPSF
from pfs import PFS
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
import matplotlib.pyplot as plt
import seaborn as sns
import re

from circuit import Circuit
from modelsim_simulator import Modelsim
from regular_tp_gen import regular_tp_gen

import sys
sys.path.insert(1, "../data/netlist_behavioral")


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
    parser.add_argument("-code", type=str, required=False,
                        help="code for general use")
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
    parser.add_argument("-times", type=int, required=False,
                        help="Repetition count for figures")

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
    circuit.lev()

    ckt_name = args.ckt + "_" + args.synv if args.synv else args.ckt

    print("======================================================")
    print("Run | circuit: {} | Test Count: {}/{} | CPUs: {}".format(
        circuit.c_fname, args.tp, args.tpLoad, args.cpu))

    if args.func == "test0":
        circuit.SCOAP_CC()
        circuit.SCOAP_CO()
        circuit.STAFAN(args.tp, args.cpu)
        circuit.co_ob_info()
        print(circuit)

    elif args.func == "test-tp-gen":
        # testing tp generation methods
        tps = circuit.gen_tp_file_full()
        # print(tps)
        tps = circuit.gen_tp_file(args.tp, mode="b")
        # print(tps)
        tps = circuit.gen_tp_file(args.tp, mode="x")
        # print(tps)
        tps = circuit.load_tp_file('../data/patterns/c2_TP3.tp')
        # print(tps)

    elif args.func == "stafan-save-coded":
        """ Running STAFAN with random TPs and saving TPs into file """

        path = config.STAFAN_DIR + "/" + circuit.c_name
        if not os.path.exists(path):
            os.mkdir(path)
        fname = os.path.join(path, circuit.c_name)
        if not os.path.exists(fname):
            os.mkdir(fname)


        for ite in range(int(args.code)):
            time_s = time.time()
            circuit.STAFAN(args.tp, args.cpu)
            fname = config.STAFAN_DIR+ "/" + circuit.c_name + "/"
            fname += "{}-TP{}-{}.stafan".format(circuit.c_name, args.tp, ite)
            circuit.save_TMs(fname)
            print("Time: \t{:.3}".format(time.time() - time_s))


    elif args.func == "stafan-save":
        """ Running STAFAN with random TPs and saving TPs into file """
        time_s = time.time()
        circuit.STAFAN(args.tp, args.cpu)
        # fname = "../data/stafan-data/{}-TP{}.stafan".format(circuit.c_name, args.tp)
        # circuit.save_TMs(fname)
        circuit.save_TMs(tp=args.tp)
        print("Time: \t{:.3}".format(time.time() - time_s))

    elif args.func == "stafan-load":
        fname = config.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad)
        circuit.load_TMs(fname)
        circuit.co_ob_info()
        print("E[FC] (T={}) = {:.2f} % ".format(
            args.tp, 100*circuit.STAFAN_FC(args.tp)))

    elif args.func == "backward-level":
        circuit.all_shortest_distances_to_PO()

    elif args.func == "pfs":
        tp_fname = "../data/patterns/{}_tp_{}.tp".format(
            circuit.c_name, args.tp)
        tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)
        # tp_fname = "../data/patterns/{}_tp_full.tp".format(circuit.c_name)
        # tps = circuit.gen_tp_file_full()
        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        pfs.fs_exe(tp_fname=tp_fname, fault_drop=1)

    elif args.func == "ppsf":
        tp_fname = "../data/patterns/{}_tp_{}.tp".format(
            circuit.c_name, args.tp)
        tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)
        # tp_fname = "../data/patterns/{}_tp_full.tp".format(circuit.c_name)
        # tps = circuit.gen_tp_file_full()
        ppsf = PPSF(circuit)
        ppsf.fault_list.add_all(circuit)
        ppsf.fs_exe(tp_fname)

    elif args.func == "pfs-vs-ppsf":
        if len(circuit.PI) < 12:
            tp_fname = "../data/patterns/{}_tp_full.tp".format(circuit.c_name)
            tps = circuit.gen_tp_file_full()
        else:
            tp_fname = "../data/patterns/{}_tp_{}.tp".format(
                circuit.c_name, args.tp)
            tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)

        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        pfs.fs_exe(tp_fname=tp_fname)

        ppsf = PPSF(circuit)
        ppsf.fault_list.add_all(circuit)
        ppsf.fs_exe(tp_fname)

        pfs_res = dict()
        for fault in pfs.fault_list.faults:
            pfs_res[str(fault)] = fault.D_count
        error = False
        for fault in ppsf.fault_list.faults:
            if fault.D_count != pfs_res[str(fault)]:
                error = True
                print("Error: Fault={} PFS={} PPSF={}".format(
                    str(fault), pfs_res[str(fault)], fault.D_count))
        if not error:
            print("PFS and PPSF results match!")
    elif args.func == "ppsf_parallel":
        exp.ppsf_parallel(circuit, args)

    elif args.func == "ppsf_parallel_old":
        time_s = time.time()
        circuit.lev()
        tot_fl = FaultList_2()
        tot_fl.add_random(circuit, args.fault)
        fault_fname = "../data/fault_list/{}-random{}.fl".format(
            circuit.c_name, args.fault)
        tot_fl.write_file(fault_fname)

        process_list = []
        for i in range(args.cpu):
            tp_fname = "../data/patterns/{}-ppsf-tp{}-part{}.tp".format(
                circuit.c_name, args.tp, i)
            parent_conn, child_conn = Pipe()
            p = Process(target=ppsf_thread,
                        args=(child_conn, args.ckt, args.tp, tp_fname, fault_fname))
            p.start()
            process_list.append((p, parent_conn))

        fault_lists = []
        for p, conn in process_list:
            tup = conn.recv()
            fault_lists.append(tup)
            p.join()

        for fault in tot_fl.faults:
            fault.D_count = []
        for fl in fault_lists:
            for idx in range(len(fl.faults)):
                tot_fl.faults[idx].D_count.append(fl.faults[idx].D_count)
        out_fname = "../data/fault_list/{}-ppsf-fault{}-tp{}-cpu{}.fl".format(
            circuit.c_name, args.fault, args.tp, args.cpu)
        tot_fl.write_file_extra(out_fname)
        print("Total time: {:.2f}".format(time.time() - time_s))
        with open(out_fname, "a") as outfile:
            outfile.write("Total time: {:.2f}\n".format(time.time() - time_s))

    elif args.func == "tpfc":
        """ Generating random test patterns and running fault simulation, using parallel 
        fault simulation with fault drop equal to 1. 
        Result is the Test pattern count fault coverage (TPFC) values stored in log files. 
        We may want to run this function many times, that is why we have code to avoid 
            overwriting tp files. 
        """
        tp_fname = os.path.join(config.PATTERN_DIR, 
                "{}_tp_{}_{}.tp".format(circuit.c_name, args.tp, args.code))
        tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)
        log_fname = config.FAULT_SIM_DIR + "/" + circuit.c_name + "/pfs/"
        log_fname += "tpfc_tp-" + str(args.tp) + "_" + args.code + ".log"
        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        pfs.fs_exe(tp_fname=tp_fname, log_fname=log_fname, fault_drop=1)

    elif args.func == "tpfc-fig":
        path = config.FAULT_SIM_DIR + "/" + circuit.c_name + "/pfs/"
        path += "tpfc_tp-" + str(args.tp)
        for i in range(1, 20):
            tmp = str(i)
            for i in range(3-len(tmp)):
                tmp = "0" + tmp
            log_fname = "{}_{}.log".format(path, tmp)
            print(log_fname)
            infile = open(log_fname, "r")
            lines = infile.readlines()
            fc = [float(line.split()[-1][:-1]) for line in lines]
            plt.plot(fc[:-1])
        plt.savefig("results-tpfc.pdf")
        plt.close()

    elif args.func == "fc-es-fig":

        exp.fc_estimation_fig(circuit=circuit, times=args.times, tp_load=args.tpLoad,tp=args.tp)

    elif args.func == "ppp":
        exp.compare_ppsf_stafan(circuit, args)

    elif args.func == "qqq":
        fname = config.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
                circuit.c_name, circuit.c_name, args.tpLoad) 
        circuit.load_TMs(fname)
        PDs = []
        for node in circuit.nodes_lev:
            PDs.append(node.C0 * node.B0)
            PDs.append(node.C1 * node.B1)

        PDs_sorted_idx = np.argsort(PDs)
        for idx in PDs_sorted_idx:
            node_idx = int(idx/2)
            node = circuit.nodes_lev[node_idx]
            # print(node)
            deltaP = observation.deltaP_2(circuit, node)
            node_str = "".join([" " for x in range(10-len(node.num))]) + node.num
            print("{}\t{}\t{:.4f}".format(node_str, node.lev, deltaP))
            # print("-------------------------------------------------------")
        
        pdb.set_trace()
    
    elif args.func == "writeOB":
        # circuit.co_ob_info()
        path = "../data/ob_stat/{}_TP{}.obs".format(ckt_name, args.tpLoad)
        print("Saving ob info in {}".format(path))
        circuit.write_ob_info(path)

    elif args.func == "analysisOB":
        TPs = [50, 100, 200, 500, 1000, 2000,
               5000, 10000, 20000, 50000, 100000]
        report_path = "../data/ob_stat/{}_REPORT.obsr".format(ckt_name)
        report = open(report_path, "w")
        data = []
        real_TP = []
        for tp in TPs:
            ob_fname = "../data/ob_stat/{}_TP{}.obs".format(ckt_name, tp)
            print(ob_fname)
            if not os.path.exists(ob_fname):
                print("SKIPPED", ob_fname)
                continue
            real_TP.append(tp)
            infile = open(ob_fname)
            lines = infile.readlines()
            data.append([(x.split()[1]) for x in lines[1:]])

        for idx in range(len(data)):
            report.write(str(real_TP[idx]) + "," + ",".join(data[idx]) + "\n")

        print("Report file generated in {}".format(report_path))

    elif args.func == "histOB":
        """ histogram of OB, reading from .stafan files"""
        mybins = np.logspace(-6, 0, 13)
        arr = []
        for node in circuit.nodes_lev:
            arr.append(node.B)
        min_val = min(arr)
        print(min_val)
        if min_val < 0:
            raise ValueError("min value is zero")
        if min_val == 0:
            print("Min value 0 spotted")
            exit()
        mybins = np.logspace(np.log10(min_val), 0, 11)
        # res = np.histogram(arr, mybins)
        res = np.histogram(arr, bins=mybins, density=False)
        # print(np.sum(res[0]))
        temp = [str(np.round(x, 3)) for x in res[0]]
        log = "," + ",".join(["{:.1e}".format(x) for x in res[1]]) + "\n"
        log += ckt_name + "," + ",".join(temp)
        print(log)

    elif args.func in ["deltaP", "deltaHTO"]:
        conv = Converter(ckt_name, "EPFL")
        # TODO: be cautious about passing args
        ops = OPI(circuit, args.func, count_op=args.opCount, args=args)
        fname = "../data/observations/" + ckt_name + \
            "_" + args.func + "_B-" + str(args.Bth)
        fname += "_Count-" + str(args.opCount) + ".op"

        conv.nodes2tmax_OP(ops, fname)
        print("Stored Synopsys readable results in {}".format(fname))
        print(ops)
        for op in ops:
            print(op + "\t" + conv.n2g(op))

    elif args.func == "gen_stil":
        # Does not generate the test patterns but reads them, and creates stil file
        # generate a test pattern file in 658 format and save it in ../data/patterns/

        # We read the ckt_name circuit, which is the synthesized version
        # But we read the golden TP from ckt circuit, because we don't have ckt.v and only
        # have ckt_synVX.v
        tp_fname = "../data/patterns/" + args.ckt + args.synv + "deltaP_TP" + \
            str(args.tpLoad) + ".tp"
        stil_fname = "../data/patterns/" + \
            args.ckt + "_" + str(args.tp) + ".raw-stil"
        # circuit.gen_tp_file(args.tp, fname=tp_fname)
        circuit.logic_sim_file(tp_fname, stil_fname,
                               out_format="STIL", tp_count=args.tp)
        print("Done stil gen, added in {}".format(stil_fname))

    elif args.func == "Single_OP_FS":
        """ For one circuit, generates OPs, based on args settings (B_th)
        For each OP, generate a new verilog file, with name as cname_OP_<OP-node>.v
        Use a predefined .tp file to simulate your new circuit 
        Store the results for this new verilog in the .STIL format
        """

        conv = Converter(args.ckt, utils.ckt_type(args.ckt))
        ops = OPI(circuit, args.OPIalg, count_op=args.opCount, B_th=args.Bth)
        print("Observation points are: ")
        for op in ops:
            print(op + "\t" + conv.n2g(op))

        tp_fname = os.path.join(
            config.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        OPs_fname = "../data/observations/" + args.ckt + "_" + \
            args.OPIalg + "_B-" + str(args.Bth)
        OPs_fname += "_Count-" + str(args.opCount) + ".op"
        conv.nodes2tmax_OP(ops, OPs_fname)
        print("Stored Synopsys observation file in     \t{}".format(fname))

        for op in ops:

            print("".join(["-"]*100))
            # Step 1: Generate a new verilog file
            print("Generating modified verilog for op: \t\t{}".format(op))
            cname_mod = args.ckt + "_OP_" + op
            path_in = os.path.join(config.VERILOG_DIR, args.ckt + ".v")
            path_out = os.path.join(config.VERILOG_DIR, cname_mod + ".v")
            convert.add_OP_verilog(path_in=path_in,
                                   op=op, path_out=path_out, verilog_version=utils.ckt_type(args.ckt))

            print("New verilog file generated in \t\t\t{}".format(path_out))

            # Step 2: Logic sim and generate STIL file
            ckt_mod = Circuit(cname_mod)
            ckt_mod.lev()
            LoadCircuit(ckt_mod, "v")
            stil_fname = os.path.join(config.PATTERN_DIR,
                                      cname_mod + "_" + str(args.tp) + ".raw-stil")
            ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL")
            print("STIL format file  generated in \t\t\t{}".format(stil_fname))
            # convert.replace_primitive2cell(path_out)

        print("".join(["-"]*100))

    elif args.func == "Multi_OP_FS":
        """ For one circuit, generates OPs, based on args settings (B_th)
        TODO: complete me after testing
        """

        conv = Converter(args.ckt, utils.ckt_type(args.ckt))
        ops = OPI(circuit, args.OPIalg, count_op=args.opCount, B_th=args.Bth)
        print("Observation points are: ")
        for op in ops:
            print(op + "\t" + conv.n2g(op))

        tp_fname = os.path.join(
            config.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        OPs_fname = "../data/observations/" + args.ckt + "_" + \
            args.OPIalg + "_B-" + str(args.Bth)
        OPs_fname += "_Count-" + str(args.opCount) + ".op"
        conv.nodes2tmax_OP(ops, OPs_fname)
        print("Stored Synopsys observation file in     \t{}".format(fname))

        # The path to verilog file changes cumulitavely
        path_in = os.path.join(config.VERILOG_DIR, args.ckt + ".v")
        for idx, op in enumerate(ops):

            print("".join(["-"]*100))

            print("Generating modified verilog for {} ops.".format(idx+1))
            print("Original verilog netlist is: \t\t\t {}".format(path_in))

            # Step 1: Continuously modifying a verilog file
            cname_mod = args.ckt + "_OP_" + args.OPIalg + "_B-" + \
                str(args.Bth) + "_Acc" + str(idx+1)
            path_out = os.path.join(config.VERILOG_DIR, cname_mod + ".v")
            convert.add_OP_verilog(
                path_in=path_in,
                op=op,
                path_out=path_out,
                verilog_version=utils.ckt_type(args.ckt),
                new_buff="MSABUFF" + str(idx),
                new_po="MSAPO" + str(idx))
            print("New verilog file generated in \t\t\t{}".format(path_out))

            # Step 2: Logic sim and generate STIL file
            ckt_mod = Circuit(cname_mod)
            ckt_mod.lev()
            LoadCircuit(ckt_mod, "v")
            stil_fname = os.path.join(config.PATTERN_DIR,
                                      cname_mod + "_" + str(args.tp) + ".raw-stil")
            ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL")
            print("STIL format file  generated in \t\t\t{}".format(stil_fname))
            path_in = path_out
            # convert.replace_primitive2cell(path_out)

        print("".join(["-"]*100))

    elif args.func == "genV_TMAXOP":
        """ input: the address to the TMAX op file 
        output: verilog file with ops as PO to be sent to fault simulation """
        # TODO: what should be the output file name?

        path_in = os.path.join(config.VERILOG_DIR, ckt_name + ".v")
        print("the original circuit is {}".format(path_in))
        v_orig = convert.read_verilog_lines(path_in)

        # op_fname = "../data/observations/{}_TMAX.op".format(ckt_name)
        op_fname = f"../data/observations/{args.op_fname}.op"
        print("reading op file from {}".format(op_fname))

        conv = Converter(ckt_name, utils.ckt_type(args.ckt))
        ops_gate = conv.tmax2nodes_OP(op_fname)
        # ops_gate = []
        print("Observation points are: ")
        ops_node = []
        args.opCount = args.opCount if args.opCount else len(ops_gate)
        for op in ops_gate[:args.opCount]:
            op = op.split("/")[0]
            ops_node.append(conv.g2n(op))
            print(op + "\t" + conv.g2n(op))

        new_pos = ["MSAPO" + op for op in ops_node]

        temp = "," + ", ".join(new_pos) + ");"
        v_orig[0] = v_orig[0].replace(");", temp)

        temp = "," + ", ".join(new_pos) + ";"
        v_orig[2] = v_orig[2].replace(";", temp)

        cname_mod = "{}_deltaP_Bth_{}_OP{}".format(
            ckt_name, args.Bth, args.opCount)
        path_out = "../data/verilog/{}.v".format(cname_mod)
        outfile = open(path_out, "w")
        outfile.write(v_orig[0] + "\n")
        outfile.write(v_orig[1] + "\n")
        outfile.write(v_orig[2] + "\n")
        outfile.write(v_orig[3] + "\n")
        for line in v_orig[4:-1]:
            outfile.write(line + "\n")

        for idx, op in enumerate(ops_node):
            new_buff = "MSABUFF" + op
            new_po = "MSAPO" + op
            outfile.write("BUF_X1 {} ( .I({}) , .Z({}) );\n".format(
                new_buff, op, new_po))

        outfile.write("endmodule\n")
        outfile.close()
        print("New verilog file generated in \t\t\t{}".format(path_out))

        # Step 2: Logic sim and generate STIL file
        tp_fname = os.path.join(
            config.PATTERN_DIR, args.ckt + "_TP" + str(args.tpLoad) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        ckt_mod = Circuit(cname_mod)
        LoadCircuit(ckt_mod, "v")
        ckt_mod.lev()
        stil_fname = os.path.join(config.PATTERN_DIR,
                                  cname_mod + "_" + str(args.tp) + ".raw-stil")
        ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL", args.tp)
        print("STIL format file  generated in \t\t\t{}".format(stil_fname))

        print("".join(["-"]*100))

    else:
        print("Function not found")
