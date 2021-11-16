from ppsf import PPSF
from pfs import PFS
from load_circuit import LoadCircuit
from fault_coverage import Fault_coverage_estimation
import config
import argparse
import os
import re
import seaborn as sns
import matplotlib.pyplot as plt


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
    parser.add_argument("-fault_count", type=int, required=False, default=None,
                        help="Number of faults")
    # parser.add_argument("-op_fname", type=str, required=False,
    #                     default=None, help="OP file name")
    parser.add_argument("-code", type=str, required=False,
                        help="code for general use")

    args = parser.parse_args()

    return args

def read_circuit(args):
    circuit = None
    if args.ckt:
        circuit = Circuit(args.ckt)

    elif args.v:
        circuit = Circuit(args.v)
    return circuit

def draw_graph(x,y):
    sns.scatterplot(x=x, y=y)
    plot = sns.lineplot(x=x, y=y)

    plot.set_ylabel(f'Fault Coverage Estimation Using STAFAN(FC%)')
    plot.set_xlabel('Test Pattern Count #TP')
    plot.set_title(f'Dependency of fault coverage on random test patterns')

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
        limit = (2<<19) # Choose according to the size of PI

        for i in range(9):
            tps_count = 2 # Choose according to the size of PI
            factor = 16 # Choose according to the size of PI
            fc_sequence = [0]
            tps_sequence = [0]

            while tps_count <= limit:
                circuit.STAFAN_CS(tp = tps_count) 

                try:
                    circuit.STAFAN_B() 
                except:
                    tps_count*=factor
                    continue

                fctp = Fault_coverage_estimation(
                    circuit=circuit, fault_mode='full',tps_count=tps_count)
                
                fc_sequence.append(fctp.calculate())
                tps_sequence.append(tps_count)

                tps_count*=factor

            print(i)
            draw_graph(x = tps_sequence,y = fc_sequence)

        plt.show()

    if args.func == "tpfc-fig":
        circuit.lev()
        op_fname = []
        tests_count = 20
        for i in range(1,tests_count+1):
            t = str(i)
            op_fname.append("0"*(3-len(t))+t)

        for ofn in op_fname:
            tp_fname = os.path.join(config.PATTERN_DIR,
                                    "{}_tp_{}_{}.tp".format(circuit.c_name, args.tp, args.code))
            tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)
            log_fname = config.FAULT_SIM_DIR + "/" + circuit.c_name + "/pfs/"
            log_fname += "tpfc_tp-" + \
                str(args.tp) + "_" + args.code + "_"+ofn+".log"
            pfs = PFS(circuit)
            pfs.fault_list.add_all(circuit)
            pfs.fs_exe(tp_fname=tp_fname, log_fname=log_fname, fault_drop=1)

            path = config.FAULT_SIM_DIR + "/" + circuit.c_name + "/pfs/"
            path += "tpfc_tp-" + str(args.tp) + "_"+args.code
            for i in range(1, 20):

                log_fname = "{}_{}.log".format(path, ofn)
                infile = open(log_fname, "r")
                lines = infile.readlines()
                fc_sequence = []
                for line in lines[:-1]:
                    tp_num, new_fault, total_fault, fc = re.findall(
                        r"\s*(\d+)\s*New:\s*(\d+)\s*Total:\s*(\d+)\s*FC:\s*(\d+\.\d+)%", line)[0]
                    fc_sequence.append(float(fc))
                plot = sns.lineplot(x=range(len(fc_sequence)),y=fc_sequence,linewidth = 0.5)
        
        plot.set_ylabel(f'Fault Coverage Using Fault Simluation(FC%)')
        plot.set_xlabel('Test Pattern Count #TP')
        plot.set_title(f'Dependency of fault coverage on random test patterns')
        plt.show()
