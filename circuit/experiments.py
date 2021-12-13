
import os 
import numpy as np
from bisect import bisect 
from multiprocessing import Process, Pipe
import time
import pandas as pd
import seaborn as sns
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


def fc_estimation_fig(circuit, tp_count=2, factor=2, limit=200, times=1, tp=100, tp_load=100):
    """
    Fault coverage estimation
    Choose tp_count, factor and the limit according to the size of PI
    """
    for i in range(times):
        tpc = tp_count
        path = f"{cfg.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.mkdir(path)
        fname = f"{path}/{circuit.c_name}-TP{tp_load}-{i}.stafan"
        if not os.path.exists(fname):
            circuit.STAFAN(tp_load)
            circuit.save_TMs(tp=tp_load,fname = fname)
        else:
            circuit.load_TMs(fname)

        limit = min(limit, (2<<len(circuit.PI)))

        fc_sequence = [0]
        tp_sequence = [0]
        for tpc in range(tp):
            try:
                fc_sequence.append(circuit.STAFAN_FC(tpc)*100)
                tp_sequence.append(tpc)
                tpc*=factor

            except:
                continue

        plot = sns.lineplot(x=tp_sequence, y=fc_sequence,color = 'green', alpha = 0.5)

    plot.set_ylabel(f'Fault Coverage (FC%)',fontsize=13)
    plot.set_xlabel('Test Pattern Count #TP',fontsize=13)
    plot.set_title(f'Dependency of fault coverage on random test patterns\nfor circuit {circuit.c_name}',fontsize=13)
    plt.subplots_adjust(top=0.835,bottom=0.25,left=0.125,right=0.9,hspace=0.195,wspace=0.2)
    plt.figtext(0.5, 0.04, f"The experiment is carried out {times} times.", wrap=True, horizontalalignment='center', fontsize=12)

    path = f"{cfg.FIG_DIR}/{circuit.c_name}/"
    if not os.path.exists(path):
        os.mkdir(path)

    fname = path+f"{limit}-fc-estimation.pdf"

    plt.savefig(fname)  
    plt.show()

def tpfc    ():
    """
    Fault coverage using fault simulation
    """
    pass

def compare_fc_tp_estimation():
    pass


def ppsf_parallel_step(circuit, fl_curr, tp, cpu, log_fname=None, count_cont=False):
    """ Running ppsf in parallel for one step given test patterns and fault list, 
        counts the number of times faults are detected. The test patterns are 
        generated in each process separately, but are not stored by default.
    Parameters
    ----------
    circuit : Circuit 
    fl : FaultList 
    tp : number of test patterns for each process  
    cpu : count of parallel processes
    log_fname : fname for the final log file 

    Return
    ------
    The final fault list 
    """
    time_s = time.time()
    process_list = []
    for i in range(cpu):
        tp_fname = os.path.join(cfg.PATTERN_DIR, "{}-ppsf-tp{}-part{}.tp".format(
            circuit.c_name, tp, i))
        parent_conn, child_conn = Pipe()
        # p = Process(target=ppsf_thread,
        #             args=(child_conn, circuit.c_fname, tp, tp_fname, fl_fname))
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
        tot_fl.write_file_extra(log_fname)
        with open(log_fname, "a") as outfile:
            outfile.write("Total time: {:.2f}\n".format(time.time() - time_s))
    
    # print("Total time: {:.2f}".format(time.time() - time_s))
    return fl_curr 

def ppsf_parallel_basic(circuit, tp, cpu, op=None, fault_count=None):
    
    tot_fl = FaultList()
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    if fault_count:
        tot_fl.add_random(circuit, args.fault)
        fl_fname = os.path.join(path, "{}-rand{}.fl".format(
            circuit.c_name, fault_count))
        log_fname = os.path.join(path, "{}-ppsf-fpb{}-tp{}-cpu{}.ppsf".format(
            circuit.c_name, fault_count, tp, cpu))
    else:
        tot_fl.add_all(circuit)
        fl_fname = os.path.join(path, "{}-all.fl".format(circuit.c_name))
        log_fname = os.path.join(path, "{}-ppsf-all-tp{}-cpu{}.ppsf".format(
            circuit.c_name, tp, cpu))

    tot_fl.write_file(fl_fname)
    return ppsf_parallel_step(circuit, tot_fl, tp, cpu, log_fname)


def ppsf_parallel_confidence(circuit, args, tp_steps, op=None, log=True, verbose=False):
    #TODO: documentation AND -- FLAG FOR WRITING INTO FILE OR NOT WRITING 
    fl_cont = FaultList()
    fl_curr = FaultList()
    if op == None:
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
        fl_curr = ppsf_parallel_step(circuit, fl_curr, tp, args.cpu, log_fname=None, 
                count_cont=True)
        fault_completed = []
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


def ppsf_parallel(circuit, args, op=None, steps=None, log=True):
    if steps == None:
        res = ppsf_parallel_basic(circuit, args.tp, args.cpu, op, args.fault_per_bin)
    else:
        res = ppsf_parallel_confidence(circuit, args, steps, op, verbose=False, log=log)
    return res

    # This is for log fname 
    # out_fname = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name) 
    # if args.fault:
    #     out_fname = os.path.join(out_fname, "{}-ppsf-fault{}-tp{}-cpu{}.ppsf".format(
    #         circuit.c_name, args.fault, args.tp, args.cpu))
    # else:
    #     out_fname = os.path.join(out_fname, "{}-ppsf-all-tp{}-cpu{}.ppsf".format(
    #         circuit.c_name, args.tp, args.cpu))
    
def ppsf_analysis(circuit, args):
    fname = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(fname, "{}-ppsf-all-tp{}-cpu{}.ppsf".format(
        circuit.c_name, args.tp, args.cpu))
    print("Reading PPSF parallel simulation results from {}".format(fname))
    res = utils.load_ppsf_parallel(fname)
    for k, v in res.items():
        res[k] = np.mean(v), np.std(v)

    return res

def compare_ppsf_step_stafan_hist(circuit, args):
    # STEP 1: load stafan data into the circuit nodes
    fname = cfg.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad)
    circuit.load_TMs(fname)

    # Step 2: load ppsf parallel step based values
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
            circuit.c_name, args.ci, args.cpu))
    res_ppsf = utils.load_ppsf_parallel_step(fname)
    
    stafan_pd = []
    ppsf_pd = [x for x in res_ppsf.values()]
    for node in circuit.nodes_lev:
        # stafan_pd.extend([node.D0, node.D1]) # D0 & D1 are not used for STAFAN anymore
        stafan_pd.extend([node.C1*node.B1, node.C0*node.B0])
    
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
    plt.savefig("ppsf-vs-stafan-{}-tp{}.png".format(circuit.c_name, args.tpLoad))
    plt.close()
    
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
        # Y.append(D)
    
    plt.xscale("log")
    plt.yscale('log')
    plt.scatter(X, Y, s=2)
    plt.ylim(max(min(Y), 0.001), max(Y)*1.1)
    # plt.xlim(0,0.2)
    plt.title("Error in detection probability (D) STAFAN vs PPSF\n{}".format(circuit.c_name))
    plt.xlabel("Detection Probability (PPSF)")
    plt.ylabel("(D_STAFAN - D_PPSF)/D_PPSF")
    plt.savefig("./results/STAFAN-Error-{}.png".format(circuit.c_name))
    plt.close()




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
    # Loading STAFAN data
    fname = cfg.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad) 
    circuit.load_TMs(fname)
    
    # Loading PPSF data
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
        circuit.c_name, args.ci, args.cpu))
    p_init = utils.load_ppsf_parallel_step_D(circuit, args)

    FC_stafan = []
    FC_ppsf = []
    TPs_base = [x*50 for x in range(1, 200)]
    TPs = []
    for tp in TPs_base:
        FC_stafan.append(100*circuit.STAFAN_FC(tp))
        FC_ppsf.append(100*utils.estimate_FC(circuit, tp))
        print("TP = {:04d}\tFC-STAFAN={:.2f}%\tFC-PPSF={:.2f}%".format(
            tp, FC_stafan[-1], FC_ppsf[-1]))
        TPs.append(tp)
        if len(FC_stafan) > 5:
            if (FC_stafan[-1]-FC_stafan[-5] < 0.05 ) and (FC_ppsf[-1]-FC_ppsf[-5] < 0.05):
                break
    plt.plot(TPs, FC_stafan, color='b', label="STAFAN")
    plt.plot(TPs, FC_ppsf, color='r', label="Fault Simulation (PPSF)")
    plt.title("FC estimation based on fault detection probabilities\n{}".format(
        circuit.c_name))
    plt.xlabel("Test Pattern Count")
    plt.ylabel("Fault Coverage (%)")
    plt.legend()
    plt.savefig("./results/figures/FCTP-STA-FS-{}.png".format(circuit.c_name))
    plt.close()


def OP_impact(circuit, args):

    samples = args.opCount 
    nodes = circuit.get_rand_nodes(samples)
    df = pd.DataFrame(columns=["Node", "B1", "B0", "C0", "C1"])
    TPs_based = [x*100 for x in range(1, 50)]# [100, 200, 300, 400, 500, 1000]
    steps = cfg.PPSF_STEPS 
    
    # Reading and loading characterized STAFAN prob. values 
    fname = cfg.STAFAN_DIR + "/{}/{}-TP{}.stafan".format(
            circuit.c_name, circuit.c_name, args.tpLoad) 
    circuit.load_TMs(fname)
    
    # Reading and loading characterized PPSF prob. values 
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
        circuit.c_name, args.ci, args.cpu))
    p_init = utils.load_ppsf_parallel_step_D(circuit, args)
    
    # Finding the range of the TP counts to generate results 
    FC_stafan = []
    FC_ppsf = []
    TPs = []
    for tp in TPs_based:
        FC_stafan.append(100*circuit.STAFAN_FC(tp))
        FC_ppsf.append(100*utils.estimate_FC(circuit, tp))
        TPs.append(tp)
        if len(FC_stafan) > 5:
            if (FC_stafan[-1]-FC_stafan[-5] < 0.05 ) and (FC_ppsf[-1]-FC_ppsf[-5] < 0.05):
                break
    print(TPs) 

    # Finding the impact of each of the random nodes
    for count, node in enumerate(nodes):
        row = {"Node": node.num, "B1":node.B1, "B0":node.B0, "C1":node.C1, "C0":node.C0}
        #TODO: later we can check if the result file already exists! 
        res_stafan  = obsv.deltaFC(circuit, node, TPs) #cut_BFS=None
        res_ppsf = obsv.deltaFC_PPSF(circuit, node, p_init, TPs, args, steps) 
        row["P-FS"] = res_ppsf["deltaP"]
        row["P-ST"] = sum(obsv.deltaP(circuit, node)) #cut_BFS=None

        for idx, tp in enumerate(TPs):
            row["FC-ST-tp{:04d}".format(tp)] = res_stafan[idx]
            row["FC-FS-tp{:04d}".format(tp)] = res_ppsf["deltaFC"][idx]
        
        print("{:5}\tOPI for node {} completed".format(count, node.num))
        df = df.append(row, ignore_index=True)
    
    # Storing the datafram into a csv file 
    fname =  "OPI-report-{}-ci{}-op{}.csv".format(circuit.c_name, args.ci, args.opCount)
    print("Dataframe of OPI analysis results is stored in {}".format(fname))
    df.to_csv(fname)
    return df

