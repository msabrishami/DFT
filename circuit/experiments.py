
import os 
import numpy as np
from bisect import bisect 
from multiprocessing import Process, Pipe
import time

from circuit import Circuit
from observation import *
from random import randint
from load_circuit import LoadCircuit
from pfs import PFS
from ppsf import PPSF 
from fault_sim import FaultList
import config as cfg

import seaborn as sns
import matplotlib.pyplot as plt

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


def fc_estimation_fig(circuit,tp_count=2,factor=2,limit=200,times = 1,tp=100,tp_load=100):
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


def ppsf_parallel_step(circuit, tot_fl, tp, cpu, log_fname=None):
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
                    args=(child_conn, circuit, tp, tot_fl))

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
    
    if log_fname:
        tot_fl.write_file_extra(log_fname)
        with open(log_fname, "a") as outfile:
            outfile.write("Total time: {:.2f}\n".format(time.time() - time_s))
    
    print("Total time: {:.2f}".format(time.time() - time_s))
    return tot_fl

def ppsf_parallel_basic(circuit, tp, cpu, fault_count=None):
    
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


def ppsf_parallel_confidence(circuit, args, tp_steps, confidence):
    tot_fl = FaultList()
    tot_fl.add_all(circuit)
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    log_fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
            circuit.c_name, confidence, args.cpu))
    print("Log for step based PPSF is being stored in {}".format(log_fname))
    outfile = open(log_fname, "w")
    for tp in tp_steps:
        time_s = time.time()
        temp_fl = FaultList()
        fl_fname = os.path.join(path, "{}-steps-temp.fl".format(circuit.c_name))
        tot_fl.write_file(fl_fname)
        tot_fl = ppsf_parallel_step(circuit, tot_fl, tp, args.cpu, log_fname=None)
        fault_completed = []
        outfile.write("#TP={}\n".format(tp))
        for fault in tot_fl.faults:
            mu = np.mean(fault.D_count) 
            std = np.std(fault.D_count)
            if mu==0 and std==0:
                temp_fl.add_str(str(fault))
            elif mu/std > confidence:
                outfile.write("{}\t{:.2f}\t{:.2f}\n".format(fault, mu, std))
            else:
                #TODO: we maybe need to extend D_count, not just overwrite it! 
                # temp_fl.add_fault(fault)
                temp_fl.add_str(str(fault))

        print("TP={} #FL={} -> #FL={}\ttime={:.2f}".format(
            tp, len(tot_fl.faults), len(temp_fl.faults), time.time()-time_s))
        tot_fl = temp_fl
        if len(tot_fl.faults) == 0:
            break

def ppsf_parallel(circuit, args, steps=None, confidence=None):
    if steps == None:
        ppsf_parallel_basic(circuit, args.tp, args.cpu, args.fault_per_bin)
    else:
        ppsf_parallel_confidence(circuit, args, steps, confidence)

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





