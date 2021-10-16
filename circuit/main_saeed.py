# -*- coding: utf-8 -*-


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
import config
from checker_logicsim import Checker
import observation
from observation import OPI
import experiments 
from load_circuit import LoadCircuit
from convert import Converter 
import convert
import utils 
from parallel_fs import PFS
from ppsf_sim import PPSF

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
            circuit.gen_tp_file(test_count = test_count, 
                    fname="../data/fault_sim/{}/input/{}_test_count-{}_id-{}.tp".format(
                        ckt, ckt, str(test_count), str(idx)))
            circuit.gen_tp_file(test_count = 1, 
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
            dfs.multiple(pattern_list = tps, fname_log=fs_fname)

def pars_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=False, help="ckt file address")
    parser.add_argument("-v", type=str, required=False, help="verilog file address")
    parser.add_argument("-synv", type=str, required=False , help="syn ver")
    parser.add_argument("-tp", type=int, required=False, help="tp count for random sim")
    parser.add_argument("-tpLoad", type=int, required=False, help="tp count for loading STAFAN")
    parser.add_argument("-cpu", type=int, required=False, help="number of parallel CPUs")
    parser.add_argument("-func", type=str, required=False, help="What operation you want to run")
    parser.add_argument("-OPIalg", type=str, required=False, help="OPI Algorithm")
    parser.add_argument("-Bth", type=float, required=False, default=0.1, 
            help="Obsv. threshold for OPI candidate selection")
    parser.add_argument("-HTO_th", type=float, required=False, default=None, 
            help="Obsv. threshold for OPI candidate selection")
    parser.add_argument("-HTC_th", type=float, required=False, default=None, 
            help="Ctrl. threshold for OPI candidate selection")
    parser.add_argument("-opCount", type=int, required=False, default=None, help="OP count")
    parser.add_argument("-op_fname", type=str, required=False, default=None, help="OP file name")
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

    if args.func == "test0":
        circuit.lev()
        circuit.STAFAN(300000, 8)
        circuit.co_ob_info()

    elif args.func == "test1":
        circuit.lev()
        print(circuit)


    elif args.func == "test2": 
        circuit.lev()
        
        # testing single test pattern generation 
        temp = circuit.gen_tp()
    
        # testing generating a file of test patterns
        path = "../data/patterns/{}_TP{}.tp".format(circuit.c_name, args.tp)
        circuit.gen_tp_file(args.tp, path)

    elif args.func == "test3": 
        circuit.lev()
        circuit.SCOAP_CC()
        circuit.SCOAP_CO()
        circuit.STAFAN(args.tp, 10) 


    elif args.func == "test4":
        time_start = time.time()
        circuit.lev()
        circuit.SCOAP_CC()
        circuit.SCOAP_CO()
        path = "../data/patterns/{}_TP{}.tp".format(circuit.c_name, args.tp)
        circuit.gen_tp_file(args.tp, path)
        circuit.STAFAN_CS(args.tp, path) 
        circuit.STAFAN_B() 
        
        fname = "../data/stafan-data/" + circuit.c_name + "-TP" + str(args.tp) + ".stafan"
        circuit.save_TMs(fname)
        print("Time: \t{:.3}".format(time.time() - time_start))

    elif args.func == "backward-level":
        circuit.all_shortest_distances_to_PO()

    elif args.func == "pfsp":
        circuit.lev()
        pfs = PFS(circuit)
        # pfs.add_fault("full",None)
        # print(pfs.single([1,1,1,1,0]))
        pfs.fs_exe(tp_num=args.tp, t_mode='rand', 
                r_mode='b', fault_list_type="full", fname = None)


    elif args.func == "ppsf":

        utils.bin2int([1, 1, 0, 0])
        utils.bin2int([1, 0, 1, 0])
        utils.bin2int([0, 0, 0, 1])

        circuit.lev()
        tps = []
        for _ in range(64):
            tps.append(circuit.gen_tp())
        fault_sim = PPSF(circuit)
        print("PPFS loaded")
        fault_sim.single(tps)
        Z = fault_sim.circuit.read_PO()
        print(Z)


    elif args.func == "saveStatTP":
        ## For now, we are only generating the random input vector files, 
        # Later we need to add read from file 
        """ generate stafan stat file based on reading TPs from file
        The version must be added to the name of .stat file"""
        
        circuit = Circuit(args.ckt)
        circuit.lev()
        circuit.SCOAP_CC()
        circuit.SCOAP_CO()

        tp_path = "../data/patterns/{}_TP{}.tp".format(circuit.c_name, args.tpLoad)
        if not os.path.exists(tp_path):
            raise NameError("no file found in {}".format(tp_path))
        config.STAFAN_C_MIN = 1.0/(10*args.tp)
        time_start = time.time()
        # circuit.STAFAN_CS(args.tp, tp_path) 
        circuit.STAFAN_CS(args.tp) 
        circuit.STAFAN_B() 
        # print("Zeros: \t{}".format(circuit.c_zero_count))
        fname = "../data/stafan-data/" + circuit.c_name + "-TP" + str(args.tp) + ".stafan"
        circuit.save_TMs(fname)
        print("Time: \t{:.3}".format(time.time() - time_start))


    # Double check later 
    elif args.func == "saveEntropyTP":
        """ generate stafan stat file based on orig-TPs, and given tp 
        The version must be added to the name of .stat file"""

        tp_path = "../data/patterns/{}_TP{}.tp".format(args.ckt, args.tpLoad)
        tpi_num = args.TPI_num
        if not os.path.exists(tp_path):
            raise NameError("no file found in {}".format(tp_path))
        config.STAFAN_C_MIN = 1.0/(10*args.tp)
        time_start = time.time()
        circuit = read_circuit(args)
        circuit.lev()
        circuit.SCOAP_CC()
        circuit.SCOAP_CO()
        circuit.STAFAN_CS(args.tp, tp_fname=tp_path) 
        circuit.STAFAN_B()
        circuit.CALC_ENTROPY()
        # print("Zeros: \t{}".format(circuit.c_zero_count))
        print("Time: \t{:.3}".format(time.time() - time_start))
        fname = "../data/stafan-data/" + circuit.c_name + "-TP" + str(args.tp) + ".ent"
        print("Saving circuit with Entropy values in " + fname)
        circuit.CALC_TPI(tpi_num, fname + "TP")  
        circuit.save_circuit_entropy(fname)

    
    elif args.func == "writeOB":
        # circuit.co_ob_info()
        path = "../data/ob_stat/{}_TP{}.obs".format(ckt_name, args.tpLoad)
        print("Saving ob info in {}".format(path))
        circuit.write_ob_info(path)


    elif args.func == "analysisOB":
        TPs = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
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
        log += ckt_name +  "," + ",".join(temp)
        print(log)




    elif args.func in  ["deltaP", "deltaHTO"]:
        conv = Converter(ckt_name, "EPFL") 
        # TODO: be cautious about passing args
        ops = OPI(circuit, args.func, count_op=args.opCount, args=args)
        fname = "../data/observations/" + ckt_name + "_" + args.func + "_B-" + str(args.Bth) 
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
        circuit = Circuit(ckt_name)
        circuit.lev()
        tp_fname = "../data/patterns/" + args.ckt + args.synv + "deltaP_TP" + str(args.tpLoad) + ".tp"
        stil_fname = "../data/patterns/" + args.ckt + "_" + str(args.tp) + ".raw-stil"
        # circuit.gen_tp_file(args.tp, fname=tp_fname)
        circuit.logic_sim_file(tp_fname, stil_fname, out_format="STIL", tp_count = args.tp)
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

        tp_fname = os.path.join(config.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        OPs_fname = "../data/observations/" + args.ckt + "_" + args.OPIalg + "_B-" + str(args.Bth) 
        OPs_fname += "_Count-" + str(args.opCount) + ".op"
        conv.nodes2tmax_OP(ops, OPs_fname)
        print("Stored Synopsys observation file in     \t{}".format(fname))
    
        for op in ops:

            print("".join(["-"]*100))
            ### Step 1: Generate a new verilog file
            print("Generating modified verilog for op: \t\t{}".format(op))
            cname_mod = args.ckt + "_OP_" + op 
            path_in = os.path.join(config.VERILOG_DIR, args.ckt + ".v")
            path_out = os.path.join(config.VERILOG_DIR, cname_mod + ".v")
            convert.add_OP_verilog(path_in=path_in,
                    op=op, path_out=path_out, verilog_version=utils.ckt_type(args.ckt))

            print("New verilog file generated in \t\t\t{}".format(path_out))

            ### Step 2: Logic sim and generate STIL file
            ckt_mod = Circuit(cname_mod)
            ckt_mod.lev()
            LoadCircuit(ckt_mod,"v") 
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

        tp_fname = os.path.join(config.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        OPs_fname = "../data/observations/" + args.ckt + "_" + args.OPIalg + "_B-" + str(args.Bth) 
        OPs_fname += "_Count-" + str(args.opCount) + ".op"
        conv.nodes2tmax_OP(ops, OPs_fname)
        print("Stored Synopsys observation file in     \t{}".format(fname))
        
        # The path to verilog file changes cumulitavely 
        path_in = os.path.join(config.VERILOG_DIR, args.ckt + ".v")
        for idx, op in enumerate(ops):
            
            print("".join(["-"]*100))

            print("Generating modified verilog for {} ops.".format(idx+1))
            print("Original verilog netlist is: \t\t\t {}".format(path_in))
            
            ### Step 1: Continuously modifying a verilog file
            cname_mod = args.ckt + "_OP_" + args.OPIalg + "_B-" + str(args.Bth) + "_Acc" + str(idx+1)
            path_out = os.path.join(config.VERILOG_DIR, cname_mod + ".v")
            convert.add_OP_verilog(
                    path_in=path_in,
                    op=op, 
                    path_out=path_out, 
                    verilog_version=utils.ckt_type(args.ckt),
                    new_buff="MSABUFF" + str(idx), 
                    new_po="MSAPO" + str(idx))
            print("New verilog file generated in \t\t\t{}".format(path_out))

            ### Step 2: Logic sim and generate STIL file
            ckt_mod = Circuit(cname_mod)
            ckt_mod.lev()
            LoadCircuit(ckt_mod,"v") 
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
        args.opCount =  args.opCount if args.opCount else len(ops_gate)
        for op in ops_gate[:args.opCount]:
            op = op.split("/")[0]
            ops_node.append(conv.g2n(op))
            print(op + "\t" + conv.g2n(op)) 
        
        new_pos = ["MSAPO" + op for op in ops_node]

        temp = "," + ", ".join(new_pos) + ");"
        v_orig[0] = v_orig[0].replace(");", temp)

        temp = "," + ", ".join(new_pos) + ";"
        v_orig[2] = v_orig[2].replace(";", temp) 

        cname_mod ="{}_deltaP_Bth_{}_OP{}".format(ckt_name, args.Bth ,args.opCount)
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
            outfile.write("BUF_X1 {} ( .I({}) , .Z({}) );\n".format(new_buff, op, new_po))
        
        outfile.write("endmodule\n")
        outfile.close()
        print("New verilog file generated in \t\t\t{}".format(path_out))
        
        
        ### Step 2: Logic sim and generate STIL file
        tp_fname = os.path.join(config.PATTERN_DIR, args.ckt + "_TP" + str(args.tpLoad) + ".tp")
        print("Reading test patterns from \t\t\t{}".format(tp_fname))

        ckt_mod = Circuit(cname_mod)
        LoadCircuit(ckt_mod,"v") 
        ckt_mod.lev()
        stil_fname = os.path.join(config.PATTERN_DIR, 
                cname_mod + "_" + str(args.tp) + ".raw-stil")
        ckt_mod.logic_sim_file(tp_fname, stil_fname, "STIL", args.tp) 
        print("STIL format file  generated in \t\t\t{}".format(stil_fname))
        
        print("".join(["-"]*100))

    else:
        print("Function not found")


