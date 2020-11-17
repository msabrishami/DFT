# -*- coding: utf-8 -*-


import argparse
import pdb
import networkx as nx
import math
import time
import os

from circuit import Circuit
from modelsim_simulator import Modelsim


import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
import config
from checker_logicsim import Checker
import observation
import experiments 
from load_circuit import LoadCircuit
from convert import Converter 
import convert
import utils 

parser = argparse.ArgumentParser()
parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
parser.add_argument("-tp", type=int, required=False, help="number of tp for random sim")
parser.add_argument("-tpLoad", type=int, required=False, help="number tp used in loading STAFAN")
parser.add_argument("-cpu", type=int, required=False, help="number of parallel CPUs")
parser.add_argument("-func", type=str, required=False, help="What operation you want to run")
parser.add_argument("-OPIalg", type=str, required=False, help="OPI Algorithm")
parser.add_argument("-Bth", type=float, required=False, default=0.1, help="B threshold for OPI")
parser.add_argument("-opCount", type=int, required=False, default=20, help="OP count")
args = parser.parse_args()

print("======================================================")
print("Run | circuit: {} | Test Count: {} | CPUs: {}".format(args.ckt, args.tp, args.cpu))
# print("======================================================\n")

# experiments.exp_check_c432_behavioral(mode="ckt", tp=100)
# experiments.exp_check_c432_behavioral(mode="v", tp=100)
# experiments.exp_check_verilog_modelsim()

if args.func not in ["saveStat", "gen_Stil"]:
    fname = "../data/stafan-data/" + args.ckt + "-stafan-" + str(args.tpLoad) + ".log"
    print("Loading circuit with STAFAN values in " + fname)
    circuit = Circuit(args.ckt)
    LoadCircuit(circuit, "v")
    circuit.lev()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    circuit.load_circuit(fname)


if args.func == "saveStat":
    config.STAFAN_C_MIN = 1.0/args.tp
    time_start = time.time()
    circuit = Circuit(args.ckt)
    LoadCircuit(circuit, "v")
    circuit.lev()
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    circuit.STAFAN_CS(args.tp) 
    circuit.STAFAN_B() 
    print("Zeros: \t{}".format(circuit.c_zero_count))
    print("{:.3}".format(time.time() - time_start))
    fname = "../data/stafan-data/" + args.ckt + "-stafan-" + str(args.tp) + ".log"
    print("Saving circuit with STAFAN values in " + fname)
    circuit.save_circuit(fname)
    exit()

elif args.func == "writeInfo":
    # circuit.co_ob_info()
    circuit.write_ob_info("./ob_stat/" + args.ckt + "_" + str(args.tpLoad) + "_obInfo.log")
    exit()

elif args.func == "ObConverge":
    print("salam")



elif args.func == "ObHist":
    # Calculate the histogram of B0 for all nodes in log scale
    import numpy as np
    # for ckt in config.ALL_EPFL_EZ:
    for ckt in config.ALL_ISCAS85:
        args.ckt = ckt # + "_syn" 
        fname = "temp_results/" + args.ckt + "-stafan-" + str(args.tp) + ".log"
        # print("Loading circuit with STAFAN values in " + fname)
        circuit = Circuit(args.ckt)
        LoadCircuit(circuit, "v")
        circuit.lev()
        circuit.SCOAP_CC()
        circuit.SCOAP_CO()
        circuit.load_circuit(fname)
        arr = []
        for node in circuit.nodes_lev:
            arr.append(node.B0)
        mybins = np.logspace(-6, 0, 13)
        res = np.histogram(arr, mybins)
        print(ckt, "\t", res[0])

elif args.func in  ["deltaP", "deltaHTO"]:
    conv = Converter(args.ckt, "ISCAS85") 
    ops = observation.OPI(circuit, args.func, count_op=args.opCount, B_th=args.Bth)
    fname = "../data/observations/" + args.ckt + "_" + args.func + "_B-" + str(args.Bth) 
    fname += "_Count-" + str(args.opCount) + ".op"
    print(ops)
    conv.nodes2tmax_OP_file(ops, fname)
    print("Stored Synopsys readable results in {}".format(fname))
    for op in ops:
        print(op + "\t" + conv.n2g(op)) 


elif args.func == "gen_stil":
    # generate a test pattern file in 658 format and save it in ../data/patterns/
    # then logicsim on this and save it as stil format in ../data/patterns/
    circuit = Circuit(args.ckt)
    LoadCircuit(circuit, "v")
    circuit.lev()
    tp_fname = "../data/patterns/" + args.ckt + "_" + str(args.tp) + ".tp"
    stil_fname = "../data/patterns/" + args.ckt + "_" + str(args.tp) + ".raw-stil"
    circuit.gen_tp_file(args.tp, fname=tp_fname)
    circuit.logic_sim_file(tp_fname, stil_fname, out_format="STIL")
    print("Done stil gen, added in {}".format(stil_fname))


elif args.func == "Single_OP_FS":
    """ For one circuit, generates OPs, based on args settings (B_th)
    For each OP, generate a new verilog file, with name as cname_OP_<OP-node>.v
    Use a predefined .tp file to simulate your new circuit 
    Store the results for this new verilog in the .STIL format
    """

    conv = Converter(args.ckt, utils.ckt_type(args.ckt)) 
    ops = observation.OPI(circuit, args.OPIalg, count_op=args.opCount, B_th=args.Bth)
    print("Observation points are: ")
    for op in ops:
        print(op + "\t" + conv.n2g(op)) 

    tp_fname = os.path.join(config.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
    print("Reading test patterns from \t\t\t{}".format(tp_fname))

    OPs_fname = "../data/observations/" + args.ckt + "_" + args.OPIalg + "_B-" + str(args.Bth) 
    OPs_fname += "_Count-" + str(args.opCount) + ".op"
    conv.nodes2tmax_OP_file(ops, OPs_fname)
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
    ops = observation.OPI(circuit, args.OPIalg, count_op=args.opCount, B_th=args.Bth)
    print("Observation points are: ")
    for op in ops:
        print(op + "\t" + conv.n2g(op)) 

    tp_fname = os.path.join(config.PATTERN_DIR, args.ckt + "_" + str(args.tp) + ".tp")
    print("Reading test patterns from \t\t\t{}".format(tp_fname))

    OPs_fname = "../data/observations/" + args.ckt + "_" + args.OPIalg + "_B-" + str(args.Bth) 
    OPs_fname += "_Count-" + str(args.opCount) + ".op"
    conv.nodes2tmax_OP_file(ops, OPs_fname)
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


else:
    exit()
# observation.stat_HTO(circuit, config.HTO_TH, config.HTC_TH)
# graph = circuit.gen_graph()


# Testing saving and loading graphs
""" 
suffix = round(math.log10(args.tp))
fname = ("10e" + str(suffix)) if (suffix%1==0) else str(args.tp)
# fname = "./../data/graph/" + args.ckt + "_" + fname + ".graphml"
fname = "./../data/graph/" + args.ckt + "_" + fname + "_HTC-" + str(config.HTC_TH) + \
        "_HTO-" + str(config.HTO_TH) + ".graphml"
# fname = "../data/graph/temp_graph.graphml"
print("Saving graph in ", fname)
nx.write_graphml(graph, fname)
temp = nx.read_graphml(fname)
print("loaded")
"""



