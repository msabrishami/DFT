# -*- coding: utf-8 -*-

from seaborn.categorical import _PointPlotter
import utils
import experiments as exp
import config
import argparse
import math
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
import pandas as pd
from circuit import Circuit
from pfs import PFS
import observation as obsv
import pdb

import sys

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

def node_info(node):

    node_parameters = {}
    node_parameters["C0"] = node.C0
    node_parameters["C1"] = node.C1
    node_parameters["S"] = node.S
    node_parameters["B0"] = node.B0
    node_parameters["B1"] = node.B1
    node_parameters["CB0"] = node.CB0
    node_parameters["CB1"] = node.CB1
    node_parameters["B"] = node.B

    return node_parameters

def tpfc_stafan(circuit, times=1, tp=100, tp_load=100):
    """
    Fault coverage estimation
    Choose tp_count, factor and the limit according to the size of PI
    """
    for i in range(times):
        path = f"{config.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"{path}/{circuit.c_name}-TP{tp_load}-{i}.stafan"
        if not os.path.exists(fname):
            circuit.STAFAN(tp_load)
            circuit.save_TMs(tp=tp_load, fname=fname)
        else:
            circuit.load_TMs(fname)

        fc_sequence = [0]
        tp_sequence = [0]
        for tpc in range(tp):
            try:
                fc_sequence.append(circuit.STAFAN_FC(tpc)*100)
                tp_sequence.append(tpc)
            except:
                continue

        plot = sns.lineplot(x=tp_sequence, y=fc_sequence,
                            color="green", alpha=0.5)

    plot.set_ylabel(f"Fault Coverage (FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"Dependency of fault coverage on random test patterns\n\
                for circuit {circuit.c_name}", fontsize=13)

    path = f"{config.FIG_DIR}/{circuit.c_name}/fc-estimation/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"{tp}-fc-estimation.png"
    plt.tight_layout()
    plt.savefig(fname)
    print(f"Figure saved in {fname}")
    return plt

def diff_tp_stafan(circuit):
    """
    Fault simulation estimation with different sizes of tp_load using STAFAN data
    """
    tps = [100,200,500,1000,2000,5000,10_000,20_000,50_000,100_000,200_000,500_000,1_000_000,10_000_000]
    set = 0
    tp_size = [f"{tp}-{set}" for tp in tps]+["1000000", "10000000"]
    for i in tp_size:
        path = f"{config.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"{path}/{circuit.c_name}-TP{i}.stafan"
        if not os.path.exists(fname):
            tpc = re.findall(r"\d+", i)[0]
            circuit.STAFAN(int(tpc))
            circuit.save_TMs(tp=tp_size, fname=fname)
        else:
            circuit.load_TMs(fname)

        fc_sequence = [0]
        tp_sequence = [0]
        for tps in tp_size:
            tp = re.findall(r"\d+", i)[0]
            try:
                fc_sequence.append(circuit.STAFAN_FC(tps)*100)
                tp_sequence.append(tps)
            except:
                continue

        plot = sns.lineplot(x=tp_sequence, y=fc_sequence,
                            color="green", alpha=0.5)

    plot.set_ylabel(f"Fault Coverage (FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"Dependency of fault coverage on random test patterns\nfor circuit {circuit.c_name}", fontsize=13)

    path = f"{config.FIG_DIR}/{circuit.c_name}/estimation-diff-tploads/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"{tp}-fc-estimation.pdf"
    plt.tight_layout()
    plt.savefig(fname)

def tpfc_ppsf(circuit, args):  # Not completed
    """
    Fault simulation estimation with different sizes of tp_load using STAFAN data
    """
    path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
        circuit.c_name, args.ci, args.cpu))
    p_init = utils.load_pd_ppsf_conf(fname)
    tps = np.arange(0, args.tp, 10)
    fcs = []
    for tp in tps:
        # fc is estimated based on constant count of tps for ppsf
        fcs.append(utils.estimate_FC(p_init, tp=tp))
    plt.plot(tps, fcs)
    plt.ylabel(f"Fault Coverage (FC%)", fontsize=13)
    plt.xlabel("Test Pattern Count #TP", fontsize=13)
    plt.title(
            f"fault coverage for random test patterns\n\
                    circuit: {circuit.c_name}", fontsize=13)

    # path = f"{config.FIG_DIR}/{circuit.c_name}/estimation-diff-tploads/"
    fname = f"./results/figures/{circuit.c_name}-tpfc-ppsf-ci{args.ci}-cpu{args.cpu}.png"
    print(f"Figure saved in {fname}")
    # if not os.path.exists(path):
    #     os.makedirs(path)
    # fname = path+f"{tps[0]}-fc-estimation-ppsf.pdf"
    plt.tight_layout()
    plt.savefig(fname)
    return plt 


def tpfc_pfs(circuit, tp, times):
    """ running and plotting the TPFC figure by doing real fault simulation (PFS) 
        if times > 1, then the fault simulation is done several times with different sets of 
        random test patterns. The figure will show the range and the mean of FC value 
        through all simulations. 

        Parameters:
        -----------
        tp : int , number of patterns used for fault simulation 
        times : int , number of times fault simulation is done
    """

    df = pd.DataFrame(columns=["tp", "fc", "batch"])

    for batch in range(times):
        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        fc = pfs.tpfc(tp, fault_drop=1)
        arr = [list(range(1,tp+1)), fc, [batch]*tp]
        df = df.append(pd.DataFrame(np.array(arr).T, columns = ["tp", "fc", "batch"]),
                ignore_index=True)
    plt.xlim(50,tp)
    plt.ylim(min(df[df["tp"]==50]["fc"].tolist()), max(df["fc"].tolist()) )
    # print(min(df[df["tp"]==50]["fc"].tolist()))
    # df["nfc"] = 100.00001 - df["fc"]
    plot = sns.lineplot(data = df, x='tp', y='fc', alpha=0.8, color="b", linewidth=1, ci=99.99)
    # plt.yticks(df["nfc"], df["fc"])
    plot.set_ylabel(f"Fault Coverage", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(f"Dependency of fault coverage on\n \
            random test patterns for {circuit.c_name}",
                   fontsize=13)

    # plot.set_xticks(df['batch'])
    # plot.set_xticklabels(plot.get_xticks()[::2])
    # plt.xticks(df["batch"])

    path = f"results/figures/"
    if not os.path.exists(path):
        os.makedirs(path)
    fname = path + f"tpfc-pfs-{circuit.c_name}.png"
    print(f"Figure saved in {fname}")
    plt.tight_layout()
    plt.savefig(fname)
    return plt

def compare_stafan_ppsf_pfs(circuit, args): # plt3 is not completed
    """
    FC estimation using STAFAN vs. PFS vs. PPSF
    """
    plt1 = tpfc_stafan(circuit, times=args.times,
            tp_load=args.tpLoad, tp=args.tp)
    plt2 = tpfc_pfs(circuit, times=args.times, tp=args.tp)
    plt3 = tpfc_ppsf(circuit, args)

    path = f"{config.FIG_DIR}/{circuit.c_name}/compare/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"tpfc-compare.pdf"
    # plt.legend(handles=[plt1, plt2, plt3], labels=[
    #            "fc estimation with stafan", "pfs", "ppsf"])
    plt.tight_layout()
    plt.savefig(fname)


def stafan_scoap(circuit):
    """STAFAN and scoap values"""
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()

    tp_no = 10
    step = 2
    limit = 20_000
    node_num = 12
    mode = "*"  # + or *

    parameters = ["C0", "C1", "S", "B0", "B1", "CB0", "CB1", "B"]

    result_dict = {}
    for node in circuit.nodes_lev:
        for p in parameters:
            result_dict[(node, p)] = []

    tp_no_seq = []
    while tp_no < limit:
        # print(f"{tp_no = }") # TODO: why there is an error here?! 
        fname = config.STAFAN_DIR + "/" + circuit.c_name + "/"
        if not os.path.exists(fname):
            os.makedirs(fname)
        fname += f"{circuit.c_name}-TP{tp_no}-0.stafan"
        if not os.path.exists(fname):
            circuit.STAFAN(tp_no, 8)
            circuit.save_TMs(fname)
        else:
            circuit.load_TMs(fname)

        tp_no_seq.append(tp_no)
        for node in circuit.nodes_lev:
            for p in parameters:
                result_dict[(node, p)].append(node_info(node)[p])
        if mode == "*":
            tp_no *= step
        elif mode == "+":
            tp_no += step
        else:
            raise "Operation is not valid"

    for param in parameters:
        test_array = result_dict[(circuit.nodes_lev[node_num], param)]
        sns.scatterplot(x=tp_no_seq, y=test_array)
        t = sns.lineplot(x=tp_no_seq, y=test_array, label=param)
    ax = plt.gca()
    ax.grid(True, which="both")

    t.set_ylabel("value")
    t.set_xlabel("No. of tests")
    t.set_title(
        f"SCOAP measures of node {node_num} in circuit {circuit.c_name}")
    # t.set_yscale("log")
    # t.set_xscale("log")

    path = f"{config.FIG_DIR}/{circuit.c_name}/stafan/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"{limit}-stafan.pdf"
    plt.tight_layout()
    plt.savefig(fname)


def ppsf_ci(circuit, tpLoad, _cis):
    colors = ["b", "r", "g"]
    i = 0
    for ci in _cis:
        path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
        fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
            circuit.c_name, ci, 50))
        res_ppsf = utils.load_ppsf_parallel_step(fname)
        print(res_ppsf)
        ppsf_pd = [x for x in res_ppsf.values()]
        bins = np.logspace(np.floor(np.log10(min(ppsf_pd))),
                           np.log10(max(ppsf_pd)), 20)
        sns.histplot(ppsf_pd, bins=bins, alpha=0.2,
                     color=colors[i], label=f"PPSF_{ci}=") # Some issue here
        i += 1

    # plt.xscale("log")
    # plt.yscale("log")
    plt.legend()
    plt.title("Detection probability histogram\n{}".format(
        circuit.c_name, tpLoad))
    plt.show()


def euclidean(circuit):  # It seems to be useless!
    tps = [100, 200, 500, 1000, 2000, 5000]
    nd = {}
    sim_seq = []
    dist_seq = []
    for tp in tps:
        fname = "../data/fault-sim-cpu50-ci3/fault-sim-cpu50/c432_synV2-ppsf-steps-ci3-cpu50.ppsf"
        res_ppsf = utils.load_ppsf_parallel_step(fname, tp)
        # ppsf_pd = [x for x in res_ppsf.values()]
        names = []
        for m in circuit.nodes_lev:
            if "@" in m.num:
                nd[m.num[:-2]] = {"ppsf": 0, "stafan": 0}
                names.append(m.num[:-2])
            else:
                nd[m.num] = {"ppsf": 0, "stafan": 0}
                names.append(m.num)
        for k in res_ppsf.items():
            nd[k[0][:-2]]["ppsf"] += k[1]

        # todo: load for different x-0 and compare
        path = f"{config.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"{path}/{circuit.c_name}-TP{tp}-0.stafan"
        if os.path.exists(fname):
            circuit.load_TMs(fname)
        else:
            circuit.STAFAN(tp)
            circuit.save_TMs(tp=tp, fname=fname)

        stafan_pd = []
        for node in circuit.nodes_lev:
            stafan_pd.extend([node.C1*node.B1])  # and D1
            if node.num not in nd.keys():
                nd[node.num] = {}
            nd[node.num]["stafan"] = node.C1*node.B1  # and D1

        ppsf_pd = []
        stafan_pd = []
        for n in names:
            ppsf_pd.append(nd[n]["ppsf"])
            stafan_pd.append(nd[n]["stafan"])

        similarity = np.dot(np.array(ppsf_pd), np.array(
            stafan_pd))/(np.linalg.norm(np.array(ppsf_pd))*np.linalg.norm(np.array(stafan_pd)))
        distance = np.linalg.norm(np.array(ppsf_pd)-np.array(stafan_pd))

        sim_seq.append(similarity)
        dist_seq.append(distance)
        # print(f"{similarity = },{distance = }")

    plt.xlabel("#test patterns")
    plt.ylabel("similarity")
    sns.lineplot(y=sim_seq, x=tps, label="Cosine similarity", color="r")
    plt.show()

    sns.lineplot(y=dist_seq, x=tps, label="Euclidean distance", color="g")
    plt.show()


def ppsf_corr_ci(circuit, args, _cis, heatmap=False):
    df = pd.DataFrame(columns=["fault"].extend(["ci"+str(x) for x in _cis]))
    cis = []
    for c in _cis:
        path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
        fname = os.path.join(
            path, f"{circuit.c_name}-ppsf-steps-ci{c}-cpu{args.cpu}.ppsf")
        cis.append(utils.load_pd_ppsf_conf(fname))
    fault_list = [i for i in cis[0].keys()]
    for f in fault_list:
        row = {"fault": f}
        for idx, c in enumerate(_cis):
            row["ci" + str(c)] = cis[idx][f]
        try:
            df = df.append(row, ignore_index=True)
        except:
            pass
    max_ci = max(_cis)
    _cis.remove(max_ci)
    colors = ["orange", "red", "blue", "green", "brown", "black"]
    max_ci_col = "ci" + str(max_ci)

    subs = math.ceil(math.sqrt(len(_cis)))
    subs2 = subs
    if subs*(subs-1) == len(_cis):
        subs2 -= 1
    fig, ax = plt.subplots(subs2, subs, figsize=(4*subs, 4*subs2))

    for idx, c in enumerate(_cis):
        i = idx//subs
        j = idx % subs
        ax[i, j].set_yscale("log")
        ax[i, j].set_xscale("log")
        ax[i, j].set_aspect(1)
        col = "ci" + str(c)
        sns.scatterplot(x=df[max_ci_col], y=df[col],
                        color=colors[idx], alpha=0.3, s=6, ax=ax[i, j])
        ax[i, j].set_ylabel(f"PD (CI={c})")
        ax[i, j].set_xlabel(f"PD (CI={max_ci})")

    if heatmap:
        sns.heatmap(df.corr(), annot=True, fmt="f", cmap="YlGnBu")

    fig.suptitle(
        "Mean of detection probability which are\n \
                in the given confidence interval.", fontsize=16)
    fig.tight_layout()
    fname = f"results/figures/{circuit.c_name}-ppsf-cis-max{max_ci}-cpu{args.cpu}.png" 
    plt.savefig(fname)
    print(f"Figure saved in {fname}")
    plt.show()
    # fig.show()


def ppsf_error_ci(circuit, hist_scatter, args, _cis):
    df = pd.DataFrame(columns=["fault"].extend(["ci"+str(x) for x in _cis]))
    cis = []
    for c in _cis:
        path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
        fname = os.path.join(
            path, f"{circuit.c_name}-ppsf-steps-ci{c}-cpu{args.cpu}.ppsf")
        cis.append(utils.load_pd_ppsf_conf(fname))
    fault_list = [i for i in cis[0].keys()]
    for f in fault_list:
        row = {"fault": f}
        for idx, c in enumerate(_cis):
            row["ci" + str(c)] = cis[idx][f]
        try:
            df = df.append(row, ignore_index=True)
        except:
            pass
    max_ci = max(_cis)
    _cis.remove(max_ci)
    max_ci_col = "ci" + str(max_ci)
    colors = ["orange", "red", "blue", "green", "brown", "black"]
    min_val = max(
        min((df["ci" + str(min(_cis))]-df[max_ci_col]) / df[max_ci_col]), -0.2)
    max_val = min(
        max((df["ci" + str(min(_cis))]-df[max_ci_col]) / df[max_ci_col]), 0.2)
    bins = np.linspace(min_val, max_val, 40)
    temp = []
    plt.rcParams["patch.force_edgecolor"] = False
    plt.figure(figsize=(12, 6), dpi=300)

    for idx, c in enumerate(_cis):
        col = "ci" + str(c)
        df[col+"_error"] = (df[col]-df[max_ci_col])/df[max_ci_col]
        temp.append(col+"_error")
        if hist_scatter == "hist":
            plt.xlim(min_val, max_val) #TODO: Move me please
            sns.histplot(df[col+"_error"], alpha=0.1, color=colors[idx],
                         linewidth=0.01,
                         # line_kws=dict(edgecolor="white", linewidth=0.01),
                         kde=True,
                         label=col.replace("ci", "CI="), bins=bins)
            plt.legend()

        elif hist_scatter == "scatter":
            sns.scatterplot(x=df[max_ci_col], y=df[col+"_error"],
                            color=colors[idx], alpha=0.2, s=8,
                            label=col.replace("ci", "CI="))
            # sns.scatterplot(x=df[max_ci_col], y=df[col+"_error"], label = col, element="step")

            plt.xscale("log")

    plt.title(f"Comparing error in detection probability (DP) value of faults measured with PPSF \n\
            for different confidence intervals (CIs) \n\
            CI = {max_ci} is used as the reference for error. \n\
            Number of parallel processes for PPSF = {args.cpu} \n\
            Circuit = {circuit.c_name}")
    if hist_scatter == "hist":
        plt.ylabel("Count of faults")
        plt.xlabel(f"Relative error to PPSF with CI={max_ci}")
    else:
        plt.ylabel(f"Relative error to PPSF with CI={max_ci}")
        plt.xlabel("PD using PPSF with CI={max_ci}")
    
    fname = f"results/figures/{circuit.c_name}-ppsf-error-cis-{hist_scatter}-cpu{args.cpu}.png" 
    plt.savefig(fname, bbox_inches="tight")
    print(f"Figure saved in {fname}")
    plt.close()
    # plt.show()

if __name__ == "__main__":
    args = pars_args()

    circuit = read_circuit(args)
    circuit.lev()

    ckt_name = args.ckt + "_" + args.synv if args.synv else args.ckt

    if args.func == "tpfc-stafan":
        tpfc_stafan(circuit=circuit, times=args.times,
                      tp_load=args.tpLoad, tp=args.tp)
    
    elif args.func == "tpfc-pfs":
        tpfc_pfs(circuit=circuit, tp=args.tp, times=args.times)
    
    elif args.func == "tpfc-ppsf":
        tpfc_ppsf(circuit, args)

    elif args.func == "compare-tpfc":
        compare_stafan_ppsf_pfs(circuit, args)

    elif args.func == "diff-tp-stafan":  # estimation with different tp loads
        diff_tp_stafan(circuit)

    elif args.func == "stafan":
        stafan_scoap(circuit)

    elif args.func == "euclidean":
        euclidean(circuit)

    elif args.func == "ppsf":
        ppsf_ci(circuit, args.tpLoad, [2, 3, 4])

    elif args.func == "ppsf-corr":
        ppsf_corr_ci(circuit, _cis=[1, 2, 3, 4, 5, 6, 10], args=args)

    elif args.func == "ppsf-error":
        # ppsf_error_ci(circuit, hist_scatter="scatter", args=args, _cis=[1,2,6,10])
        ppsf_error_ci(circuit, hist_scatter="hist",
                args=args, _cis=[1, 2, 3])
