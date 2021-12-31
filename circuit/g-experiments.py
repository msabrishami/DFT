# -*- coding: utf-8 -*-

import enum
import utils
import config
import argparse
import math
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
import scipy.stats

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'brown',
          'purple', 'turquoise', 'salmon', 'skyblue']

exp = lambda x: 1.1**(x)
log = lambda x: np.log(x)
yticks = [80,90,95,97.5,99,99.5,99.75,100]

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
    parser.add_argument("-figmode", type=str, required=False, #options are hist, scatter, both
                        help="Draw histogram or scatter plot for function ppsf-error-ci")
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
    # node_parameters["CB0"] = node.CB0
    # node_parameters["CB1"] = node.CB1
    # node_parameters["B"] = node.B

    return node_parameters


def tpfc_stafan(circuit, tp=100, tpLoad=100, times=1,):
    """ Run and plot the TPFC figure usin STAFAN values.
    If times > 1, then  several STAFAN values are calculated using different sets of 
    random test patterns. The figure will show the range and the mean of FC value.

    Parameters
    ---------
    circuit : Circuit
    tpload : int 
        Size of tpLoads for STAFAN to be calculated
    times : int
        Count of different tpLoads which means the times a line is drawn
    tp : int
        The size of tp that is used in FC estimation formula
    """

    df = pd.DataFrame(columns=["tp", "fc", "batch"])
    for i in range(times):
        path = f"{config.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"{path}/{circuit.c_name}-TP{tpLoad}-{i}.stafan"
        if not os.path.exists(fname):
            circuit.STAFAN(tpLoad)
            circuit.save_TMs(tp=tpLoad, fname=fname)
        else:
            circuit.load_TMs(fname)

        for tpc in range(1, tp+1):
            try:
                row = {"tp": tpc, "fc": circuit.STAFAN_FC(tpc)*100, "batch": i}
                df = df.append(row, ignore_index=True)
            except:
                continue

    plot = sns.lineplot(x=df["tp"], y=df["fc"],
                        color="green", ci=99.99, label=f"STAFAN ({tpLoad})")

    
    plot.set_yscale("function", functions=(exp, log))
    plot.set(xlim=(50,tp), ylim=(80,100))
    plot.set_yticks(yticks)
    plot.grid()

    plot.set_ylabel(f"Fault Coverage(FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"Dependency of fault coverage on random test patterns\n\
        for circuit {circuit.c_name}\n \
        method: STAFAN ({tpLoad})", fontsize=13)

    # path = f"{config.FIG_DIR}/{circuit.c_name}/fc-estimation/"
    path = "./results/figures/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"tpfc-stafan-constant-tpLoad-{circuit.c_name}-tpLoad{tpLoad}.png"
    plt.tight_layout()
    plt.savefig(fname)
    print(f"Figure saved in {fname}")


def diff_tp_stafan(circuit, tps): #TODO: Must be changed
    """
    Fault coverage estimation
    STAFAN measures are calculates many times with different tpLoad count of test patterns.
    Then, the fault coverage is calculated using STAFAN values with the correspoing tp count.
    TODO: list of tps should be generated automatically according to ?
    """

    set = 0
    fc_sequence = []
    tp_sequence = []
    for tp in tps:
        f = f"{tp}-{set}"
        path = f"{config.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"{path}/{circuit.c_name}-TP{f}.stafan"
        if not os.path.exists(fname):
            tpc = re.findall(r"\d+", f)[0]
            circuit.STAFAN(int(tpc))
            circuit.save_TMs(tp=tp, fname=fname)
        else:
            circuit.load_TMs(fname)

        try:
            fc_sequence.append(circuit.STAFAN_FC(tp)*100)
            tp_sequence.append(tp)
        except:
            continue

    plot = sns.lineplot(x=tp_sequence, y=fc_sequence,
                        color="green", label = "STAFAN (different tpLoads)")
    plot = sns.scatterplot(x=tp_sequence, y=fc_sequence, color="green") #draw dots
    
    plt.xscale("log")
    plot.set_ylabel(f"Fault Coverage (FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"Dependency of fault coverage on random test patterns\n\
        for circuit {circuit.c_name}\n \
        method: STAFAN (different tpLoads)", fontsize=13)

    # path = f"{config.FIG_DIR}/{circuit.c_name}/estimation-diff-tploads/"
    path = "./results/figures/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"tpfc-stafan-diff-tpLoad-{circuit.c_name}.png"
    print(f"Figure saved in {fname}")
    plt.tight_layout()
    plt.savefig(fname)


def tpfc_pfs(circuit, tp, times):
    """ Run and plot the TPFC figure by doing real fault simulation (PFS).
    If times > 1, then the fault simulation is done several times with different sets of 
    random test patterns. The figure will show the range and the mean of FC value 
    through all simulations. 

    Parameters:
    -----------
    circuit : Circuit
    tp : int 
        The size of tp that is used in FC estimation formula
    times : int 
        Number of times fault simulation is executed
    """

    df = pd.DataFrame(columns=["tp", "fc", "batch"])

    for batch in range(times):
        pfs = PFS(circuit)
        pfs.fault_list.add_all(circuit)
        fc = pfs.tpfc(tp, fault_drop=1)
        arr = [list(range(1, tp+1)), fc, [batch]*tp]
        df = df.append(pd.DataFrame(np.array(arr).T, columns=["tp", "fc", "batch"]),
                       ignore_index=True)

    plot = sns.lineplot(x=df["tp"], y=df["fc"], alpha=0.8,
                        color="b", ci=99.99, label="PFS")

    
    plt.xlim=(50,tp)
    plt.ylim(min(df[df["tp"] == 50]["fc"].tolist()), 100)
    plot.set_yscale("function", functions=(exp, log))
    plot.set_yticks(yticks)
    plot.grid()
    plot.set_ylabel(f"Fault Coverage", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(f"Dependency of fault coverage on\n \
            random test patterns for {circuit.c_name}", fontsize=13)

    path = "results/figures/"
    if not os.path.exists(path):
        os.makedirs(path)
    fname = path + f"tpfc-pfs-{circuit.c_name}-TP{tp}-times{times}.png"
    print(f"Figure saved in {fname}")
    plt.tight_layout()
    plt.savefig(fname)

def tpfc_ppsf(circuit, ci, cpu, tp):
    """ Plot for Fault simulation estimation using PPSF method with different sizes of tpLoads.
    Only the faults that are detected in a given CI percentage are dropped in PPSF algorithm.

    Parameters:
    -----------
    circuit : Circuit
    tp : int
        The size of tp that is used in FC estimation formula.
    ci : int
        Confidence interval used in PPSF algorithm.
    cpu : int
        Count of CPU used to execute PPSF.
    """

    path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
        circuit.c_name, ci, cpu))
    p_init = utils.load_pd_ppsf_conf(fname)
    tps = np.arange(0, tp+1, 10)
    fcs = []
    for tp in tps:
        # fc is estimated based on constant count of tps for ppsf
        fcs.append(utils.estimate_FC(p_init, tp=tp)*100)
    plot = sns.lineplot(x=tps, y=fcs, color="red", label="PPSF")
    
    plot.set_yscale("function", functions=(exp, log))
    plot.set_yticks(yticks)
    plt.xlim=(50,tp)
    plt.ylim(min(80, 100))
    plot.grid()

    plot.set_ylabel(f"Fault Coverage (FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"fault coverage for random test patterns\n\
        for circuit {circuit.c_name} \n \
        method: PPSF", fontsize=13)

    path = "./results/figures"
    # path = f"{config.FIG_DIR}/{circuit.c_name}/fc-estimation/"
    fname = f"{path}/tpfc-ppsf-{circuit.c_name}-TP{tp}-CI{ci}-cpu{cpu}.png"
    print(f"Figure saved in {fname}")
    plt.tight_layout()
    plt.savefig(fname)


def compare_tpfc(circuit, times, tp, tpLoad, ci, cpu):
    """ A plot comparing fault coverage using STAFAN vs. PFS vs. PPSF.
    Be careful that plots are saved cumulative. If you want each plot separately, should \
    directly run the methods.

    Parameters:
    -----------
    circuit : Circuit
    tp : int
        The size of tp that is used in FC estimation formula
    tpLoad : int
        Size of tpLoads for STAFAN to be calculated
    times : int
        Number of times fault simulation is executed
    ci : int
        Confidence interval used in PPSF algorithm.
    cpu : int
        Count of CPU used to execute PPSF.
    """
    
    tpfc_stafan(circuit, tpLoad=tpLoad, tp=tp, times=times)
    tpfc_pfs(circuit, times=times, tp=tp)
    tpfc_ppsf(circuit, ci=ci, cpu=cpu, tp=tp)

    plt.title(f"Dependency of fault coverage on\nrandom test patterns for {circuit.c_name}", 
            fontsize=13)

    # path = f"{config.FIG_DIR}/{circuit.c_name}/compare/"
    path = "./results/figures/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path + f"tpfc-compare-stafan-pfs-ppsf-{circuit.c_name}\
                    -TP{tp}-CI{ci}-tpLoad{tpLoad}-cpu{cpu}.png"
    plt.tight_layout()
    plt.savefig(fname)
    print(f"\nFinal figure saved in {fname}")


def ppsf_ci(circuit, cpu, _cis):
    """ Histogram for probability detection of faults.
    The graph is drawn for the given CIs.

    Parameters:
    -----------
    circuit : Circuit
    cpu : int
        Number of CPUs used to run PPSF.
    _cis : list
        List of CIs used in PPSF algorithm
    """

    copy_cis = _cis.copy()
    for idx, ci in enumerate(copy_cis):
        path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
        fname = os.path.join(
            path, f"{circuit.c_name}-ppsf-steps-ci{ci}-cpu{cpu}.ppsf")
        if not os.path.exists(fname):
            _cis.remove(ci)
            print(f"Data is not available for CI={ci}")
            continue
        res_ppsf = utils.load_pd_ppsf_conf(fname)
        ppsf_pd = [x for x in res_ppsf.values()]
        bins = np.logspace(np.floor(np.log10(min(ppsf_pd))),
                           np.log10(max(ppsf_pd)), 20)
        sns.histplot(ppsf_pd, alpha=0.2, bins=bins,# kde=True,
                     color=colors[idx], label=f"CI={ci}")  # Some issue here

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.rcParams["patch.force_edgecolor"] = False

    plt.xscale("log")
    plt.xlabel("PD using PPSF")
    plt.ylabel("Count of faults")
    plt.title(f"Detection probability histogram with PPSF\n\
        for circuit{circuit.c_name}")
    # path = f"{config.FIG_DIR}/{circuit.c_name}/ppsf/"
    path = f"./results/figures/"
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path+f"ppsf-CI-{circuit.c_name}-maxCI{max(_cis)}.png"
    plt.tight_layout()
    plt.savefig(fname)
    print(f"\nFigure saved in {fname}.")


def ppsf_corr_ci(circuit, cpu, _cis, heatmap=False):
    """ Scatter plot for each CI comparing to the maximum given CI. Drawing heatmap is optional.
    Be careful about subplots. According to the list of CIs, some of them are empty.
    
    Parameters:
    -----------
    circuit : Circuit
    cpu : int
        Number of CPUs used to run PPSF.
    _cis : list
        List of CIs that the PPSF results are reported if the fault convergence is in.
    heatmap : bool
        If draw a heatmap for results with different CIs.
    """

    df = pd.DataFrame(columns=["fault"].extend(["ci"+str(x) for x in _cis]))
    cis = []
    copy_cis = _cis.copy()
    for c in copy_cis:
        path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
        fname = os.path.join(
            path, f"{circuit.c_name}-ppsf-steps-ci{c}-cpu{cpu}.ppsf")
        if not os.path.exists(fname):
            _cis.remove(c)
            print(f"Data is not available for CI={c}")
            continue
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

    subs = math.ceil(math.sqrt(len(_cis)))
    subs2 = subs
    if subs*(subs-1) >= len(_cis):
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

    fig.suptitle("Mean of detection probability which are\n\
    in the given confidence interval.", fontsize=16)
    fig.tight_layout()
    fname = f"results/figures/ppsf-corr-{circuit.c_name}-CIs-max{max_ci}-cpu{cpu}.png"
    plt.savefig(fname)
    print(f"Figure saved in {fname}")


def ppsf_error_ci(circuit, hist_scatter, cpu, _cis):
    """ Histogram or scatter plot for relative error of different PPSF fault coverage results \
    using different CIs with respect to the maximum given CI. In case of histogram, KDE \
    (Kernel Density Estimation) line is also drawn.

    Parameters:
    -----------
    circuit : Circuit
    hist_scatter : str
        Options: hist, scatter
    cpu : int
        Number of CPUs used to run PPSF
    _cis : list
        List of CIs that the PPSF results are reported if the fault convergence is in.
    """

    df = pd.DataFrame(columns=["fault"].extend(["ci"+str(x) for x in _cis]))
    cis = []
    copy_cis = _cis.copy()
    for c in copy_cis:
        path = os.path.join(config.FAULT_SIM_DIR, circuit.c_name)
        fname = os.path.join(
            path, f"{circuit.c_name}-ppsf-steps-ci{c}-cpu{cpu}.ppsf")
        if not os.path.exists(fname):
            _cis.remove(c)
            print(f"Data is not available for CI={c}")
            continue
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
    min_val = max(min((df["ci" + str(min(_cis))]-df[max_ci_col]) / df[max_ci_col]), -0.2)
    max_val = min(max((df["ci" + str(min(_cis))]-df[max_ci_col]) / df[max_ci_col]), 0.2)
    bins = np.linspace(min_val, max_val, 40)
    temp = []
    plt.rcParams["patch.force_edgecolor"] = False
    plt.figure(figsize=(12, 6))
    for idx, c in enumerate(_cis):
        col = "ci" + str(c)
        df[col+"_error"] = (df[col]-df[max_ci_col])/df[max_ci_col]
        temp.append(col+"_error")
        if hist_scatter == "hist":
            plt.xlim(min_val, max_val)
            sns.histplot(df[col+"_error"], alpha=0.1, color=colors[idx],
                         linewidth=0.01,
                         # line_kws=dict(edgecolor="white", linewidth=0.01),
                         kde=True,
                         label=col.replace("ci", "CI="), bins=bins)
            plt.legend()

        if hist_scatter == "scatter":
            sns.scatterplot(x=df[max_ci_col], y=df[col+"_error"],
                            color=colors[idx], alpha=0.5, s=8,
                            label=col.replace("ci", "CI="))

            plt.xscale("log")

    plt.title(f"Comparing error in detection probability (DP) of faults measured with PPSF \n\
    for different confidence intervals (CIs) \n\
    CI = {max_ci} is used as the reference for error. \n\
    Number of parallel processes for PPSF = {cpu} \n\
    Circuit = {circuit.c_name}")
    if hist_scatter == "hist":
        plt.xlabel(f"Relative error with respect to PPSF with CI={max_ci}")
        plt.ylabel("Count of faults")
    else:
        plt.xlabel(f"PD using PPSF with CI={max_ci}")
        plt.ylabel(f"Relative error with respect to PPSF with CI={max_ci}")

    fname = f"results/figures/ppsf-error-{circuit.c_name}-maxCI{max_ci}-{hist_scatter}plot-cpu{cpu}.png"
    plt.savefig(fname, bbox_inches="tight")
    print(f"Figure saved in {fname}")


def stafan(circuit, tps, ci = 5): 
    """
    
    Parameters:
    -----------
    circuit : Circuit
    tps :  list

    """
    df = pd.DataFrame(columns=["Node", "C0", "C1", "B0", "B1", "TP"])
    for tp in tps:
        set = 0
        path = f"{config.STAFAN_DIR}/{circuit.c_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"{path}/{circuit.c_name}-TP{tp}-{set}.stafan"
        if not os.path.exists(fname):
            circuit.STAFAN(tp)
            circuit.save_TMs(tp=tp, fname=fname)
        else:
            circuit.load_TMs(fname)
        for n in circuit.nodes_lev:
            df = df.append({"Node":n.num, "C0": n.C0, "C1": n.C1, "B0": n.B0, "B1": n.B1, "TP":tp}, ignore_index=True)


    max_tp = max(tps)
    tps.remove(max_tp)

    df_max = df[df["TP"]==max_tp]
    df_error = pd.DataFrame(columns=["Node", "C0-error", "C1-error", "B0-error", "B1-error", "TP"])
    for tp in tps:
        for n in circuit.nodes_lev:
            row = {"Node":n.num, "TP":tp}
            dftp = df[df["TP"]==tp]
            for p in ["C0", "C1", "B0", "B1"]:
                a = float(dftp[dftp["Node"]==n.num][p])
                b = float(df_max[df_max["Node"]==n.num][p])
                row[f"{p}-error"] = (a-b)/b
            df_error = df_error.append(row,ignore_index=True)
    del df
    del df_max
    for p in [ "C0", "C1", "B0", "B1"]:
        mean, std = df_error[f"{p}-error"].mean(), df_error[f"{p}-error"].std()
        min_val = mean-ci*std
        max_val = mean+ci*std
        df_ci = df_error[(df_error[f"{p}-error"]>min_val) & (df_error[f"{p}-error"]<max_val)]
        bins_count = 15
        bins = np.linspace(min_val, max_val, bins_count)
        sns.histplot(data=df_ci, x=f"{p}-error", hue = "TP", bins=bins, 
                     alpha=0.4, kde=True, palette=colors[:len(tps)])

        path = "./results/figures/"
        fname = path+f"stafan-{p}-maxTP{max_tp}.png"
        plt.xlabel(f"Relative error")
        plt.ylabel("Node count")
        plt.title(f"Relative error of STAFAN values of {circuit.c_name} using different TPs compared to the maximum TP.\n \
                    Only errors in ci = {ci} are considered.")
        plt.savefig(fname)
        print(f"Figure saved in {fname}")
        plt.show()
        plt.tight_layout()


if __name__ == "__main__":
    args = pars_args()
    plt.rcParams["figure.figsize"]=9,8

    cis = [1, 2, 3, 4, 5, 6, 10]

    circuit = read_circuit(args)
    circuit.lev()

    ckt_name = args.ckt + "_" + args.synv if args.synv else args.ckt


    if args.func == "tpfc-stafan":
        tpfc_stafan(circuit=circuit, times=args.times,
                    tpLoad=args.tpLoad, tp=args.tp)

    elif args.func == "tpfc-pfs":
        tpfc_pfs(circuit=circuit, tp=args.tp, times=args.times)

    elif args.func == "tpfc-ppsf":
        tpfc_ppsf(circuit=circuit, ci=args.ci, cpu=args.cpu, tp=args.tp)

    elif args.func == "compare-tpfc":
        compare_tpfc(circuit, args.times, args.tp, args.tpLoad, args.ci, args.cpu)


    elif args.func == "ppsf-ci":
        ppsf_ci(circuit=circuit, cpu=args.cpu, _cis=cis)

    elif args.func == "ppsf-corr":
        ppsf_corr_ci(circuit=circuit, _cis=cis, cpu=args.cpu)

    elif args.func == "ppsf-error":
        if args.figmode == "both":
            ppsf_error_ci(circuit=circuit, hist_scatter="hist", cpu=args.cpu, _cis=cis)
            ppsf_error_ci(circuit=circuit, hist_scatter="scatter", cpu=args.cpu, _cis=cis)
        else:
            ppsf_error_ci(circuit=circuit, hist_scatter=args.figmode, cpu=args.cpu, _cis=cis)
    
    elif args.func == "stafan":
        stafan(circuit, tps=[50,200,500,1000,2000,5000], ci=1)

    # elif args.func == "stafan":
    #     stafan_scoap(circuit=circuit)

    else:
        raise ValueError(f"Function \"{args.func}\" does not exist.")