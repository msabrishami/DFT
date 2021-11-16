
import os 
import numpy as np
from bisect import bisect 
from multiprocessing import Process, Pipe
import time

from circuit import Circuit
from observation import *
from random import randint
from c432_logic_sim import c432_sim
from load_circuit import LoadCircuit
from pfs import PFS
from ppsf import PPSF 
from fault_sim import FaultList_2

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

def ppsf_thread(conn, ckt_name, tp_count, tp_fname, fault_fname):
    ckt = Circuit(ckt_name)
    ckt.lev()
    tps = ckt.gen_tp_file(tp_count, tp_fname=tp_fname)
    fault_sim = PPSF(ckt)
    fault_sim.fault_list.add_file(fault_fname)
    fault_sim.fs_exe(tp_fname)
    conn.send(fault_sim.fault_list)


def compare_ppsf_stafan(circuit, args):
    time_s = time.time()
    circuit.lev()
    # Check if the STAFAN results are available 
    fname = config.STAFAN_DIR + "/{}-TP{}.stafan".format(circuit.c_name, args.tpLoad) 
    if not os.path.exists(fname):
        print("STAFAN data for CKT={} with TP={} is not available".format(
            circuit.c_name, args.tpLoad))
        return None
    circuit.load_TMs(fname)
    PDs = []
    for node in circuit.nodes_lev:
        PDs.append(node.C0 * node.B0)
        PDs.append(node.C1 * node.B1)
    bins = np.linspace(min(PDs), max(PDs), 10)
    count = [0]*10
    selected_faults = FaultList_2()
    for node in circuit.nodes_lev:
        idx = bisect(bins, node.C0 * node.B0)-1
        if count[idx] < args.fault:
            selected_faults.add(node.num, 1)
            count[idx] += 1
        idx = bisect(bins, node.C1 * node.B1)-1
        if count[idx] < args.fault:
            selected_faults.add(node.num, 0)
            count[idx] += 1
        if min(count) == args.fault - 1:
            break
    fault_fname = "../data/fault_list/{}-dist-10x{}.fl".format(circuit.c_name, args.fault)
    selected_faults.write_file(fault_fname)
    process_list = []
    for i in range(args.cpu):
        tp_fname = "../data/patterns/{}-ppsf-tp{}-part{}.tp".format(
                circuit.c_name, args.tp, i)
        parent_conn, child_conn = Pipe()
        p = Process(target = ppsf_thread, 
                args = (child_conn, args.ckt, args.tp, tp_fname, fault_fname))
        p.start()
        process_list.append((p, parent_conn))

    fault_lists = []
    for p, conn in process_list:
        tup = conn.recv()
        fault_lists.append(tup)
        p.join()
    
    for fault in selected_faults.faults:
        fault.D_count = []
    for fl in fault_lists:
        for idx in range(len(fl.faults)):
            selected_faults.faults[idx].D_count.append(fl.faults[idx].D_count)
    out_fname = "../data/fault_list/{}-ppsf-fault{}-tp{}-cpu{}.fl".format(
            circuit.c_name, args.fault, args.tp, args.cpu)
    selected_faults.write_file_extra(out_fname)
    print("Total time: {:.2f}".format(time.time() - time_s))
    with open(out_fname, "a") as outfile:
        outfile.write("Total time: {:.2f}\n".format(time.time() - time_s))
    for fl in selected_faults.faults:
        node = circuit.nodes[fl.node_num]
        stafan = node.C0*node.B0 if fl.stuck_val==1 else node.C1*node.B1
        pd = sum(fl.D_count)/(args.tp*args.cpu)
        print("{}\t{:.6f}\t{}\t{}\t{}\t{}\t{}".format(fl, stafan, pd, 
            node.C0, node.C1, node.B0, node.B1))

