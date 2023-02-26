import os
import argparse
import pandas as pd
import time
import sys
import pdb


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import utils
import config as cfg
import experiments.experiments as exp
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
from circuit.circuit import Circuit

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
    parser.add_argument("-fault_per_bin", type=int, required=False, help="faults per bin")
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
    parser.add_argument("-depth", type=int, required=False,
                        help="depth of search")

    # TODO: args.ci is now an integer because the way we saved current files
    parser.add_argument("-ci", type=int, required=False,
                        help="Confidence value (mu/std)")

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

    # cfg.HTO_TH = args.HTO_th if args.HTO_th else cfg.HTO_TH
    # cfg.HTC_TH = args.HTC_th if args.HTC_th else cfg.HTC_TH

    circuit = read_circuit(args)
    circuit.lev()

    ckt_name = args.ckt + "_" + args.synv if args.synv else args.ckt

    print("\n-----------------------------------------------")
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
        # TODO: update test generation calling
        tps = circuit.gen_full_tp_file()
        # print(tps)
        tps = circuit.gen_tp_file(args.tp, mode="b")
        # print(tps)
        tps = circuit.gen_tp_file(args.tp, mode="x")
        # print(tps)
        tps = circuit.load_tp_file('../data/patterns/c2_TP3.tp')
        # print(tps)

    elif args.func == "stafan-save":
        """ Running STAFAN with random TPs and saving TMs into file """
        time_s = time.time()
        circuit.STAFAN(args.tp, args.cpu)
        circuit.save_TMs(fname)
        print("Time: \t{:.3}".format(time.time() - time_s))


    elif args.func == "stafan-save-coded":
        """ Running STAFAN with random TPs, for args.code times 
            and saving TMs into file """
        for ite in range(int(args.code)):
            time_s = time.time()
            circuit.STAFAN(args.tp, args.cpu)
            fname = cfg.STAFAN_DIR+ "/" + circuit.c_name + "/"
            fname += "{}-TP{}-{}.stafan".format(circuit.c_name, args.tp, ite)
            circuit.save_TMs(fname)
            print("Time: \t{:.3}".format(time.time() - time_s))


    elif args.func == "lev-backward":
        #TODO: needs review
        circuit.levelize_backward()

    elif args.func == "pfs":
        tp_fname = "../data/patterns/{}_tp_{}.tp".format(
            circuit.c_name, args.tp)
        tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)
        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        pfs.run(tps=tp_fname, fault_drop=1, verbose=True)


    elif args.func == "ppsf":
        ppsf = PPSF(circuit)
        ppsf.fault_list.add_all(circuit)
        ppsf.run(tp_fname, args.tp, fault_drop=1)


    elif args.func == "pfs-vs-ppsf":
        exp.check_pfs_vs_ppsf(circuit, args)
        
    
    elif args.func == "pd-ppsf":
        # TODO full review and documentation  
        time_s = time.time()
        exp.pd_ppsf(circuit, args, steps=cfg.PPSF_STEPS, verbose=True)
        print("Total time = {:.2f}".format(time.time() - time_s))
    

    elif args.func == "ppsf-vs-stafan":
        exp.compare_ppsf_stafan(circuit, args, mode="hist")


    elif args.func == "ppsf_analysis":
        mu = {}
        std = {}
        TPs = [10, 20, 30, 40, 50, 100, 200, 500, 1000]
        for tp in TPs: 
            args.tp = tp
            res = exp.ppsf_analysis(circuit, args)
            faults = list(res.keys())
            # mu = [100*x[0]/args.tp for x in res.values() if (x[0]/args.tp < float(args.code))]
            # std = [x[1] for x in res.values()]
            # print("Removed {}/{} elements, PD>{}".format(
            #     len(res)-len(mu), len(mu), args.code))
            # plt.figure(figsize=(10, 8), dpi=300)
            # plt.hist(mu, bins=40)
            # plt.savefig("ppsf-hist-{}-tp{}.png".format(circuit.c_name, args.tp))
            # plt.close()
            mu[tp] = [x[0]/args.tp for x in res.values()]
            std[tp] = [x[1]/args.tp for x in res.values()]
        ind_sorted = np.argsort(mu[TPs[-1]])
        res = ""
        # for idx in ind_sorted:
        #     if idx%20 != 0:
        #         continue
        #     res = ["{:.2f}/{:.2f}> {:.1f}".format(
        #         mu[tp][idx]*100, std[tp][idx]*100, mu[tp][idx]/std[tp][idx]) for tp in TPs]
        #     print("{}: \t{}".format(faults[idx], "\t".join(res)))
        print("\t0.7(75%)\t0.9(80%)\t1.0(84%)\t1.3(90%)\t1.5(93%)\t2.0(97%)\t2.1(98%)\t2.3(99%)")
        for tp in TPs:
            print("TP={}\t".format(tp), end="")
            for r in [0.7, 0.9, 1.0, 1.3, 1.5, 2.0, 2.1, 2.3]: 
                drops = [(mu[tp][idx]/std[tp][idx] > r) for idx in range(len(std[tp]))]
                ratio = sum(drops)/len(drops)
                print("{:.1f}%".format(ratio*100), end="\t\t")
            print()
            # print("TP={}\t (mu/std > 2.0) = {:.1f}% \t{:.1f}".format(
            #     tp, 100*ratio, 1/(1-ratio)))
    
    elif args.func == "tpfc":
        """ Generating random test patterns and running fault simulation, using parallel 
        fault simulation with fault drop equal to 1. 
        Result is the Test pattern count fault coverage (TPFC) values stored in log files. 
        We may want to run this function many times, that is why we have code to avoid 
            overwriting tp files. 
        """
        tp_fname = os.path.join(cfg.PATTERN_DIR, 
                "{}_tp_{}_{}.tp".format(circuit.c_name, args.tp, args.code))
        tps = circuit.gen_tp_file(args.tp, tp_fname=tp_fname)
        log_fname = cfg.FAULT_SIM_DIR + "/" + circuit.c_name + "/pfs/"
        log_fname += "tpfc_tp-" + str(args.tp) + "_" + args.code + ".log"
        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        pfs.run(tps=tp_fname, fault_drop=1)
    

    elif args.func == "tpfc-fig":
        path = cfg.FAULT_SIM_DIR + "/" + circuit.c_name + "/pfs/"
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

    elif args.func == "fc-sta-fs":
        TPs = [x*100 for x in range(1,21)]
        exp.FCTP_analysis(circuit, args)

    elif args.func == "BFS-DFS":
        #TODO: review is required
        node = circuit.get_rand_nodes()
        print(node)

        # testing backward BFS: 
        res = utils.get_fanin_lvl(circuit, node, 2)
        for n in res:
            print(n, n.flagA)
        
        res_DFS = utils.get_fanin(circuit, node)
        print(len(res_DFS))
        res_BFS = utils.get_fanin_BFS(circuit, node)
        print(len(res_BFS))
        # TODO: check if the results of BFS and DFS are the same 

    elif args.func == "fanin-analysis":
        # exp.fanin_analysis(circuit, args)
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'brown',
          'purple', 'turquoise', 'salmon', 'skyblue']
        plt.rcParams["patch.force_edgecolor"] = False
        plt.rcParams['patch.linewidth'] = 0
        plt.rcParams['patch.edgecolor'] = 'none'
        for idx, depth in enumerate([5, 8, 10, 15, 20]):
            res = exp.fanin_depth_analysis(circuit, depth)
            plot = sns.distplot(res, 
                # bins=bins, 
                # log_scale=(False, True),
                label=f"depth={depth}",
                hist=False,
                kde=True, 
                color=colors[idx])
        res.sort()
        plt.xlim(0, res[int(len(res)*0.95)])
        plt.legend()
        plt.savefig(f"fanin-depth-{circuit.c_name}.png")
        plt.close()
        
    
    elif args.func == "deltaFCP":
        """ calculating deltaFC and deltaP of random OPs 
        based on STAFAN and PPSF results """ 
        time_s = time.time()
        df = exp.OP_impact(circuit, args)
        print("Total time = {:.2f}".format(time.time() - time_s))

    elif args.func == "deltaFCP-alt": 
        fname = "./results/csv/OPI-report-{}-ci{}-op{}.csv".format(
                circuit.c_name, args.ci, args.opCount)
        df = pd.read_csv(fname)
        df2 = pd.DataFrame()
        # df2["Node"] = df["Node"]
        cols = df.columns.values.tolist()[1:]
        for col in cols:
            if col not in ["Node", "deltaP", 
                    "FC-FS-tp0600", "FC-FS-tp0700", "FC-FS-tp0800", 
                    "FC-ST-tp0600", "FC-ST-tp0700", "FC-ST-tp0800"]:
                df2[col] = df[col].rank(ascending=1)
                print(col)
        cols = df2.columns.values.tolist()
        print("\t", end="")
        for col in cols:
            print("\t{}".format(col), end="")
        print()
        for i in range(len(cols)):
            print("{:15}".format(cols[i]), end="")
            for j in range(len(cols)):
                print("{:.2f}".format(df2[cols[i]].corr(df2[cols[j]])), end="\t")
            print()
        TPs = [x*100 for x in range(1,11)]
        for tp in TPs:
            col1 = "FC-ST-tp{:04d}".format(tp)
            col2 = "FC-FS-tp{:04d}".format(tp)
            plt.scatter(df[col1], df[col2])
            plt.title("Compare deltaFC based on STAFAN vs. PPSF for nodes\n{}".format(
                circuit.c_name))
            plt.xlabel("deltaFC based on STAFAN")
            plt.ylabel("deltaFC based on Fault Simulation")
            fname = "./results/figures/{}-deltaFC-STAFAN-PPSF-samples{}-tp{}.png".format(
                    circuit.c_name, args.opCount, tp)
            print("figure plotted in {}".format(fname))
            plt.savefig(fname)
            plt.close()

    else:
        print("Function not found")
