
import os 
import numpy as np
from bisect import bisect 
from multiprocessing import Process, Pipe
import time
import pandas as pd
import matplotlib.pyplot as plt

from circuit import Circuit
import observation as obsv
from random import randint
from load_circuit import LoadCircuit
from pfs import PFS
from ppsf import PPSF 
from fault_sim import FaultList
import config as cfg
import utils

import pdb

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
        LoadCircuit(circuit, "v")
        circuit.lev()
        path = "../data/modelsim/golden_IO_from_verilog/golden_" + ckt + "_10_b.txt"
        circuit.golden_test(path)

def exp_check_c432_behavioral(mode="ckt", tp=100, ):
    if mode not in ["ckt", "v"]:
        raise NameError("mode {} is not accepted".format(mode))
    print("Checking c432 behavioral golden with c432 in {} format".format(mode))
    circuit = Circuit("c432")
    LoadCircuit(circuit, mode)
    circuit.lev()
    check_c432_logicsim(circuit, tp, mode)

def ppsf_thread_old(conn, ckt_name, tp_count, tp_fname, fl_fname):
    ckt = Circuit(ckt_name) 
    ckt.lev()
    tps = ckt.gen_multiple_tp(tp_count)
    fault_sim = PPSF(ckt)
    fault_sim.fault_list.add_file(fl_fname)
    fault_sim.fs_exe(tps)
    conn.send(fault_sim.fault_list)

def ppsf_thread(conn, ckt, tp_count, fault_list):
    tps = ckt.gen_multiple_tp(tp_count)
    fault_sim = PPSF(ckt)
    fault_sim.fault_list = fault_list
    fault_sim.fs_exe(tps)
    conn.send(fault_sim.fault_list)

def pd_ppsf_step(circuit, fl_curr, tp, cpu, log_fname=None, count_cont=False):
    """ Run ppsf in parallel for one step given tp count and fault list, \
    counts the number of times faults in fault list are detected. 
    The tps are generated in each process separately, but are not stored by default. \

    Parameters
    ----------
    circuit : Circuit
    fl_curr : FaultList
        Initially is total faults
    tp : int
        The number of test patterns for each process  
    cpu : int
        Count of parallel processes
    log_fname : str
        File name for the final log fil. If None, does not log results (default is None)
    count_cont: int
        #TODO: define this (default is False)

    Returns
    ------
    list
        A fault list with D_count with length equal to given count of CPUs
    """

    time_s = time.time()
    process_list = []
    for _ in range(cpu):
        parent_conn, child_conn = Pipe()
        p = Process(target=ppsf_thread,
                    args=(child_conn, circuit, tp, fl_curr))
        p.start()
        process_list.append((p, parent_conn))

    fault_lists = []
    for p, conn in process_list:
        tup = conn.recv()
        fault_lists.append(tup)
        p.join()

    for fault in fl_curr.faults:
        fault.D_count = []

    for fl in fault_lists:
        for idx in range(len(fl_curr.faults)):
            fl_curr.faults[idx].D_count.append(fl.faults[idx].D_count)
    
    if log_fname:
        tot_fl.write_file_extra(log_fname) #TODO: tot_fl not defined in this scope
        with open(log_fname, "a") as outfile:
            outfile.write("Total time: {:.2f}\n".format(time.time() - time_s))
    
    return fl_curr 

def pd_ppsf_basic(circuit, tp, cpu, fault_count=None):
    """ Basic parallel PPSF fault simulation
    If fault_count is given, randomly selects faults, o.w. it generates a fault list \
    with all the faults in the circuit. 
    Logs the results in a file with a default name. 
    The result is a fault list, and D_count attribute of each fault is a list of \
    the number of times the fault is detected in each process. 

    Parameters
    ----------
    circuit : Circuit 
    tp : int
        The number of test patterns for each process  
    cpu : int
        count of parallel processes
    fault_count : int
        Number of random faults, if None, all faults are considered 

    Returns
    ------
    list
        A fault list with D_count with length equal to given count of CPUs
    """
    
    tot_fl = FaultList()
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    if fault_count:
        tot_fl.add_random(circuit, fault_count)
        log_fname = os.path.join(path, "{}-ppsf-fpb{}-tp{}-cpu{}.ppsf".format(
            circuit.c_name, fault_count, tp, cpu))
    else:
        tot_fl.add_all(circuit)
        log_fname = os.path.join(path, "{}-ppsf-all-tp{}-cpu{}.ppsf".format(
            circuit.c_name, tp, cpu))
    
    return pd_ppsf_step(circuit, tot_fl, tp, cpu, log_fname)

def pd_ppsf_conf(circuit, args, tp_steps, op=None, verbose=False, log=True):
    """ Run ppsf with count of test patterns in stp_steps list over the given number of CPUs.\
    If the times of probability detection is in the confidential interval, the \
    fault is dropped. Finally, for each fault the mean of detection times and the standard \
    deviation is stored in the log file.

    Parameters
    ----------
    circuit : Circuit 
    args : args
        Command-line arguments
    tp_steps : list
        Lengths of tps in each run
    op : Node
        Node used for observation point insertion (default is None)
    verbose : boolean
        If True, print results (default is False)
    log : boolean
        If True, save logs in log file (default is True).
        Logs are list of faults and the mean of times they were detected over cp times of \
        process. Logs are separated by the line '#TP=tp_counts' in each step.
        
    Returns
    ------
    dict : str to float
        A dictionary of faults to the mean of their detection times \
        over args.cpu times of process with cumulative count of test patterns.
    """

    fl_cont = FaultList()
    fl_curr = FaultList()
    if op is None:
        fl_cont.add_all(circuit)
        fl_curr.add_all(circuit)
    else:
        fanin_nodes = utils.get_fanin_BFS(circuit, op)
        for node in fanin_nodes:
            fl_cont.add(node.num, "1")
            fl_cont.add(node.num, "0")
            fl_curr.add(node.num, "1")
            fl_curr.add(node.num, "0")
    fault_idx = {}
    for idx, fault in enumerate(fl_cont.faults):
        fault_idx[str(fault)] = idx
        fault.D_count = np.zeros(args.cpu) 

    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    if log==False:
        log_fname = None
    elif op==None:
        log_fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
                circuit.c_name, args.ci, args.cpu))
    else:
        log_fname = os.path.join(path, "{}-{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
                circuit.c_name, node.num, args.ci, args.cpu))

    if log and verbose:
        print("Log for step based PPSF is being stored in {}".format(log_fname))
    if log:
        outfile = open(log_fname, "w")

    tp_tot = 0 
    res_final = {}
    for tp in tp_steps:
        tp_tot += tp
        time_s = time.time()
        fl_temp = FaultList()
        fl_curr = pd_ppsf_step(circuit, fl_curr, tp, args.cpu, log_fname=None, 
                count_cont=True)
        if log: 
            outfile.write("#TP={}\n".format(tp))

        for fault in fl_curr.faults:
            fault_cont = fl_cont.faults[fault_idx[str(fault)]]
            fault_cont.D_count += np.array(fault.D_count)
            mu = np.mean(fault_cont.D_count) 
            std = np.std(fault_cont.D_count)
            if mu==0 and std==0:
                fl_temp.add_str(str(fault))
            elif mu/std > args.ci:
                if log:
                    outfile.write("{}\t{:.2f}\t{:.2f}\n".format(fault, mu, std))
                res_final[str(fault)] = mu/tp_tot 
            else:
                fl_temp.add_str(str(fault))

        if verbose:
            print("TP={} #FL={} -> #FL={}\ttime={:.2f}".format(
                tp, len(fl_curr.faults), len(fl_temp.faults), time.time()-time_s))
        fl_curr = fl_temp 
        if len(fl_curr.faults) == 0:
            break
    
    # Writing down the remaining faults 
    if log:
        outfile.write("#TP: (remaining faults)\n")
    for fault in fl_curr.faults:
        mu = np.mean(fault.D_count) 
        std = np.std(fault.D_count)
        if log:
            outfile.write("{}\t{:.2f}\t{:.2f}\n".format(fault, mu, std))
        res_final[str(fault)] = mu/tp_tot 
    if log:
        outfile.close()
    return res_final 

def pd_ppsf(circuit, args, steps=None, op=None, verbose=False, log=True):
    """ Parallel Fault Simulation
    If steps is given, the ppsfs will be run for all tp counts over the \
    given count of processes in the args and the mean and std will be save into log file. Else, \
    the simple parallel patterns with the given count of test patterns will be run.

    Parameters
    ----------
    circuit : Circuit 
    args : args
        Command-line arguments
    steps : list
        A list of tp counts for each run
        (default is None)
    op : None
        Node used for observation point insertion (default is None)
    verbose : boolean
        If True, print results (default is False)
    log : boolean
        If save logs in log file (default is True)
        Logs are list of faults and the mean of times they were detected over cp times of \
            process. Logs are separated by the line '#TP=tp_counts' in each step
    
    Returns
    ------
    dict or list
        According to the steps, it will be determined. If steps is given, returns \
        a dictionary of faults to means, otherwise, A fault list with D_count  \
        with length equal to cpu is returned
    """
    if steps:
        res = pd_ppsf_conf(circuit, args, steps, op, verbose=verbose, log=log)
    else:
        res = pd_ppsf_basic(circuit, args.tp, args.cpu, args.fault_per_bin)
    return res

def ppsf_analysis(circuit, args):
    # TODO: let's get rid of this or at least change the name 
    fname = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(fname, "{}-ppsf-all-tp{}-cpu{}.ppsf".format(
        circuit.c_name, args.tp, args.cpu))
    print("Reading PPSF parallel simulation results from {}".format(fname))
    res = utils.load_ppsf_parallel(fname)
    for k, v in res.items():
        res[k] = np.mean(v), np.std(v)

    return res

def compare_ppsf_stafan(circuit, args, mode="hist"):
    # TODO : let's get rid of this soon ... 
    
    # STEP 1: load stafan data into the circuit nodes
    fname = cfg.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad)
    circuit.load_TMs(fname)

    # Step 2: load ppsf parallel step based values
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
            circuit.c_name, args.ci, args.cpu))
    res_ppsf = utils.load_pd_ppsf_conf(fname)
    
    stafan_pd = []
    ppsf_pd = [x for x in res_ppsf.values()]
    for node in circuit.nodes_lev:
        # stafan_pd.extend([node.D0, node.D1]) # D0 & D1 are not used for STAFAN anymore
        stafan_pd.extend([node.C1*node.B1, node.C0*node.B0])
    
    if mode=="hist":
        # Figure 1: histogram of STAFAN and PPSF probabilities 
        bins = np.logspace(np.floor(np.log10(min(ppsf_pd))), np.log10(max(ppsf_pd)), 20)
        plt.figure(figsize=(10, 8), dpi=300)
        plt.xscale("log")
        plt.yscale("log")
        plt.hist(stafan_pd, bins=bins, color="r", alpha=0.2, label="STAFAN")
        plt.hist(ppsf_pd,  bins=bins, color="b", alpha=0.2, label="PPSF")
        plt.title("Detection probability histogram\n{}-tp={}".format(
            circuit.c_name, args.tpLoad))
        plt.legend()
        fname = "./results/figures/stafan-vs-ppsf-hist-{}-tpLoad{}-ci{}-cpu{}.png".format(
                circuit.c_name, args.tpLoad, args.ci, args.cpu)
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        print("Figure saved in {}".format(fname))
    
    elif mode=="rel-err":
        # Figure 2: relative error based on the PPSF value
        X = []
        Y = []
        for fault, prob in res_ppsf.items():

            node = circuit.nodes[fault[:-2]]
            if fault[-1] == 1:
                D = node.C0 * node.B0
            else:
                D = node.C1 * node.B1 
            if D==prob:
                continue
            X.append(prob)
            Y.append( abs(D-prob)/prob ) 
        
        plt.xscale("log")
        plt.yscale("log")
        plt.scatter(X, Y, s=2)
        plt.ylim(max(min(Y), 0.001), max(Y)*1.1)
        # plt.xlim(0,0.2)
        plt.title("Relative error in detection probability STAFAN vs PPSF\n\
                CI={}\tCPU={}\nCircuit={}".format(
                    args.ci, args.cpu, circuit.c_name))
        plt.xlabel("Detection Probability (PPSF)")
        plt.ylabel("(D_STAFAN - D_PPSF)/D_PPSF")
        fname = "./results/figures/stafan-vs-ppsf-error-{}-tpLoad{}-ci{}-cpu{}.png".format(
                circuit.c_name, args.tpLoad, args.ci, args.cpu)
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        print("Figure saved in {}".format(fname))

    elif mode=="scatter":
        # Figure 2: relative error based on the PPSF value
        X = []
        Y = []
        for fault, prob in res_ppsf.items():
            node = circuit.nodes[fault[:-2]]
            if fault[-1] == 1:
                Y.append(node.C0 * node.B0)
            else:
                Y.append(node.C1 * node.B1)
            X.append(prob)
        
        plt.xscale("log")
        plt.yscale("log")
        plt.scatter(X, Y, s=2)
        plt.ylim(max(min(Y), 0.001), max(Y)*1.1)
        # plt.xlim(0,0.2)
        plt.title("Relative error in detection probability STAFAN vs PPSF\n\
                CI={}, CPU={}\nCircuit={}".format(
                    args.ci, args.cpu, circuit.c_name))
        plt.xlabel("PPSF")
        plt.ylabel("STAFAN")
        fname = "./results/figures/stafan-vs-ppsf-scatter-{}-tpLoad{}-ci{}-cpu{}.png".format(
                circuit.c_name, args.tpLoad, args.ci, args.cpu)
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        print("Figure saved in {}".format(fname))


def fanin_analysis(circuit, args):
    args.opCount = int(max(200, len(circuit.nodes)/4 ))
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
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
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
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
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
        res_stafan  = obsv.deltaFC(circuit, node, TPs) #cut_BFS=None
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
    fname =  "results/deltaFC/OPI-deltaFC-{}-ci{}-op{}-{}.csv".format(
            circuit.c_name, args.ci, args.opCount,i)
    while os.path.exists(fname):
        i+=1
        fname =  "OPI-report-{}-ci{}-op{}i-{}.csv".format(circuit.c_name, args.ci, args.opCount,i)
    print("Dataframe of OPI analysis results is stored in {}".format(fname))
    df.to_csv(fname, float_format='%.5e')
    return df
