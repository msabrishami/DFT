
import os 
import time
import pdb

import numpy as np
from multiprocessing import Process, Pipe
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append('../')

import config as cfg
import utils
import tpi.observation as obsv
from random import randint
from circuit.circuit import Circuit
from circuit.circuit_loader import CircuitLoader
from fault_simulation.pfs import PFS
from fault_simulation.ppsf import PPSF
from fault_simulation.fault import FaultList
from tp_generator import TPGenerator


def check_c432_logicsim(circuit, tp=1, mode="ckt"):
    """ ckt and verilog files in all ISCAS valid circuits differ by "N"
    if mode is selected ckt: node numbers are simple integers, no issue
    else if mode is verilog, one "N" will be added to node.num
    """

    for t in range(tp):
        PI_dict = dict()
        PI_list = []
        
        PI_num = [x.num for x in circuit.PI]
        PI_num = [x[1:] for x in PI_num] if mode=="v" else PI_num 
        for pi in PI_num:
            val = randint(0,1)
            PI_dict[pi] = val
            PI_list.append(val)

        res_beh = c432_sim(PI_dict)
        circuit.logic_sim(PI_list)
        res_ckt = circuit.read_PO()
        res_ckt_2 = {}
        if mode == "v":
            for k in res_ckt:
                res_ckt_2[k[1:]] = res_ckt[k]
            res_ckt = res_ckt_2
        if res_beh != res_ckt:
            print("Logicsim does NOT match behavioral simulation" +
                    "for {}, with {} test patterns ".format(circuit.c_name, tp))
            return False
    print("Logicsim matches behavioral simulation for {}, with {} test patterns ".format(
        circuit.c_name, tp))
    return True

def exp_check_verilog_modelsim():
    for ckt in ["c17", "c432", "c499", "c880", "c1908"]:
        print("\nCircuit: " + ckt)
        circuit = Circuit(ckt)
        CircuitLoader(circuit, "v")
        circuit.lev()
        path = "../../data/modelsim/golden_IO_from_verilog/golden_" + ckt + "_10_b.txt"
        circuit.golden_test(path)

def exp_check_c432_behavioral(mode="ckt", tp=100, ):
    if mode not in ["ckt", "v"]:
        raise NameError("mode {} is not accepted".format(mode))
    print("Checking c432 behavioral golden with c432 in {} format".format(mode))
    circuit = Circuit("c432")
    CircuitLoader(circuit, mode)
    circuit.lev()
    check_c432_logicsim(circuit, tp, mode)

def check_pfs_vs_ppsf(circuit, args):
    """ checking whether the results of PFS and PPSF match 
        if number of PIs in circuit <12, all possible tps are checked,
        o.w. args.tp will be used to generate a tp file """
 

    tg = TPGenerator(circuit)
    if len(circuit.PI) < 12:
        tps = tg.gen_full()
    else:
        tps = tg.gen_n_random(args.tp)

    pfs = PFS(circuit)
    pfs.fault_list.add_all()
    pfs.run(tps=tps,verbose=True, save_log=True)
 
    ppsf = PPSF(circuit)
    ppsf.fault_list.add_all()
    ppsf.run(tps,verbose=True,save_log=True)

    """
    for idx in range(len(pfs.fault_list.faults)):
        fault_pfs = pfs.fault_list.faults[idx]
        fault_ppsf = ppsf.fault_list.faults[idx]
        print(fault_pfs, fault_pfs.D_count, fault_ppsf, fault_ppsf.D_count)
    """

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

def ppsf_analysis(circuit, args):
    # TODO: let's get rid of this or at least change the name
    fname = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(fname, "{}-ppsf-all-tp{}-proc{}.ppsf".format(
        circuit.c_name, args.tp, args.cpu))
    print("Reading PPSF parallel simulation results from {}".format(fname))
    ppsf = PPSF(circuit)

    res = load_ppsf_parallel(fname)
    for k, v in res.items(): 
        res[k] = np.mean(v), np.std(v)

    return res

def fanin_analysis(circuit, args):
    """Histogram of the number of fanin nodes
    """
    if args.opCount > len(circuit.nodes):
        samples = len(circuit.nodes) 
        nodes = circuit.nodes_lev
    else:
        samples = args.opCount
        nodes = circuit.get_rand_nodes(samples)
    fanin_count = []
    for node in nodes:
        fanin_count.append(len(utils.get_fanin_BFS(circuit, node)))
    tt = "Total Nodes={} mean={:.1f} std={:1f}".format(
            len(circuit.nodes), np.mean(fanin_count), np.std(fanin_count))
    print("{}\t{}".format(circuit.c_name, tt))
    plt.title("Histogram of the number of fanin nodes\n{}".format(tt))
    plt.hist(fanin_count)
    plt.savefig("{}-fanin-count.png".format(circuit.c_name))
    plt.close()

def fanin_depth_analysis(circuit, depth):
    res = []
    for node in circuit.nodes_lev:
        res.append(len(utils.get_fanin_depth(circuit, node, depth)))
    return res

def FCTP_analysis(circuit, args):
    """ Draw plot to compare Fault coverage using two methods \
    PFS with detection probability estimation using STAFAN parameters.\
    The plot is saved in ./results/figure/

    Parameters
    ----------
    circuit : Circuit 
    args : args
        command-line arguments
    
    Returns
    ------
    None
    """
    # Loading STAFAN data
    fname = cfg.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad) 
    circuit.load_TMs(fname)
    
    # Loading PPSF data
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-proc{}.ppsf".format(
        circuit.c_name, args.ci, args.cpu))
    p_init = utils.load_pd_ppsf_conf(fname) 

    FC_stafan = []
    FC_ppsf = []
    TPs_base = [x*50 for x in range(1, 200)]
    TPs = []
    for tp in TPs_base:
        FC_stafan.append(100*circuit.STAFAN_FC(tp))
        FC_ppsf.append(100*utils.estimate_FC(p_init, tp))
        print("TP = {:04d}\tFC-STAFAN={:.2f}%\tFC-PPSF={:.2f}%".format(
            tp, FC_stafan[-1], FC_ppsf[-1]))
        TPs.append(tp)
        if len(FC_stafan) > 5:
            if (FC_stafan[-1]-FC_stafan[-5] < 0.05 ) and (FC_ppsf[-1]-FC_ppsf[-5] < 0.05):
                break
    plt.plot(TPs, FC_stafan, color='b', label="STAFAN",linestyle='dashed')
    plt.plot(TPs, FC_ppsf, color='r', label="Fault Simulation (PPSF)", alpha=0.5, linewidth=4)
    plt.title("FC estimation based on fault detection probabilities\n{}".format(
        circuit.c_name))
    plt.xlabel("Test Pattern Count")
    plt.ylabel("Fault Coverage (%)")
    plt.legend()
    path = "./results/figures"

    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig("{}/FCTP-STA-FS-{}.png".format(path,circuit.c_name))
    plt.close()

def OP_impact(circuit, args):
    """ Add args.opCount random nodes to the primary outputs as observation points. \
    Then, calculates the change in the real fault coverage using ppsf and \
    the estimation using STAFAN parameters. Finally saves the diferences in a .csv file. \
    The csv also contains the sum of changes in fault coverage and \
    probability detection in P-FS and P-ST columns.

    Parameters
    ----------
    circuit : Circuit 
    args : args
        Command-line arguments
    args.opCount : number of random nodes to be selected for OP, 
        if larger than total nodes in the circuit, all ndoes will be selected. 
    
    Returns
    ------
    None
    """
    
    samples = args.opCount 
    if  samples > len(circuit.nodes_lev):
        nodes = circuit.nodes_lev
        samples = len(circuit.nodes_lev)
        # the order is kept, gradual increase in simulation time.
    else:
        nodes = circuit.get_rand_nodes(samples)
    df = pd.DataFrame(columns=["Node", "B1", "B0", "C0", "C1"])
    TPs_based = [x*100 for x in range(1, 50)] # [100, 200, 300, 400, 500, 1000]
    steps = cfg.PPSF_STEPS 
    
    # Read and load characterized STAFAN prob. values 
    fname = cfg.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad) 
    circuit.load_TMs(fname)
    
    # Read and load characterized PPSF prob. values 
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-proc{}.ppsf".format(
        circuit.c_name, args.ci, args.cpu))
    p_init = utils.load_pd_ppsf_conf(fname)
    
    # Find the range of the TP counts to generate results 
    FC_stafan = []
    FC_ppsf = []
    TPs = []
    for tp in TPs_based:
        FC_stafan.append(100*circuit.STAFAN_FC(tp))
        FC_ppsf.append(100*utils.estimate_FC(p_init, tp))
        print("tp={}\tFC-PPSF={}\tFC-STAFAN={}".format(tp, FC_ppsf[-1], FC_stafan[-1]))
        TPs.append(tp)
        if len(FC_stafan) > 5:
            if (FC_stafan[-1]-FC_stafan[-5] < 0.05 ) and (FC_ppsf[-1]-FC_ppsf[-5] < 0.05):
                break
    # Find the impact of each of the random nodes
    for count, node in enumerate(nodes):
        row = {"Node": node.num, "B1":node.B1, "B0":node.B0, "C1":node.C1, "C0":node.C0}
        res_stafan  = obsv.deltaFC(circuit, node, TPs, args.depth) #cut_BFS=None
        res_ppsf = obsv.deltaFC_PPSF(circuit, node, p_init, TPs, args, steps) 
        row["P-FS"] = res_ppsf["deltaP"]
        row["P-ST"] = sum(obsv.deltaP(circuit, node)) #cut_BFS=None

        for idx, tp in enumerate(TPs):
            row["FC-ST-tp{:04d}".format(tp)] = res_stafan[idx]
            row["FC-FS-tp{:04d}".format(tp)] = res_ppsf["deltaFC"][idx]
        if count % 50 == 0: 
            print("{:5}\tOPI for node {} completed".format(count, node.num))
        df = df.append(row, ignore_index=True)
    
    # Store the datafram into a csv file
    i = 0
    while True:
        if args.depth:
            fname =  "results/deltaFC/OPI-deltaFC-{}-ci{}-op{}-depth{}-{}.csv".format(
                    circuit.c_name, args.ci, samples, args.depth, i)
        else:
            fname =  "results/deltaFC/OPI-deltaFC-{}-ci{}-op{}-{}.csv".format(
                    circuit.c_name, args.ci, samples, i) 
        if not os.path.exists(fname):
            break
        i+=1
   
    print("Dataframe of OPI analysis results is stored in {}".format(fname))
    df.to_csv(fname, float_format='%.5e')
    return df
