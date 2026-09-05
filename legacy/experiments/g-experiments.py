import argparse
import math
import os
import pdb

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import IPython

import sys
sys.path.append('../')

from config import FIG_DIR, STAFAN_DIR, FAULT_SIM_DIR, AUTO_TP
from config import PPSF_CI_TP_STEPS

PLOT_MIN_TP = 50
PLOT_MIN_Y = 40
PLOT_MAX_Y = 100

import utils
from circuit.dft_circuit import DFTCircuit
from fault_simulation.pfs import PFS
from fault_simulation.ppsf import PPSF

from tp_generator import TPGenerator

colors = ['r', 'g', 'b', 'brown', 'm', 'y', 'c', 
          'purple', 'turquoise', 'salmon', 'skyblue']

const_base = 1.1
exp = lambda x: (const_base**(x))
log = lambda y: np.log(y) / np.log(const_base)
yticks = [80,90,95,97.5,99,99.5,99.75,100]

def pars_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=False,
                        help="ckt file address")
    # parser.add_argument("-v", type=str, required=False,   # no need. ckt works for both.
    #                     help="verilog file address")
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
    parser.add_argument("-figmode", type=str, required=False, 
            choices=['hist', 'scatter','both'],
            help="Draw histogram or scatter plot for function ppsf-error-ci",)
    args = parser.parse_args()

    return args

def prepare_env():
    if not os.path.exists(FIG_DIR):
        os.makedirs(FIG_DIR)
    if not os.path.exists(STAFAN_DIR):
        os.makedirs(STAFAN_DIR)
    if not os.path.exists(FAULT_SIM_DIR):
        os.makedirs(FAULT_SIM_DIR)
    
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

def tpfc_stafan(circuit: DFTCircuit, tp=100, tpLoad=100, times=1, num_proc=1):
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
        fname = utils.path_stafan_code(circuit.c_name, tpLoad, i)
        if not os.path.exists(fname):
            circuit.STAFAN(tpLoad, num_proc=num_proc, save_log=False, verbose=True)
            circuit.save_STAFAN(fname=fname, verbose=True)
        else:
            circuit.load_STAFAN(fname)
        
        for tpc in range(0, tp+1, 10):
            row = pd.DataFrame({"tp": tpc, "fc": circuit.STAFAN_FC(tpc)*100, 
                "batch": i}, index=[0])
            df = pd.concat([df, row], ignore_index=True)

    plot = sns.lineplot(x=df["tp"], y=df["fc"], color="green", 
            errorbar=('ci', 99.99), label=f"STAFAN ({tpLoad})")

    plot.set_yscale("function", functions=(exp, log))
    plot.set(xlim=(PLOT_MIN_TP,tp), ylim=(PLOT_MIN_Y,PLOT_MAX_Y))
    plot.set_yticks(yticks)
    plot.grid()

    plot.set_ylabel(f"Fault Coverage(FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"Dependency of fault coverage on random test patterns\n\
        for circuit {circuit.c_name}\n \
        method: STAFAN ({tpLoad})", fontsize=13)
    
    path = os.path.join(STAFAN_DIR, circuit.c_name)
    fname = os.path.join(path, f"tpfc-stafan-{circuit.c_name}-tpLoad{tpLoad}-tp{tp}.png")
    plt.tight_layout()
    plt.savefig(fname)
    print(f"Figure saved in {fname}")

def tpfc_pfs(circuit, tp, times, plot_ci=99.99, log_yscale=True):
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
        fc_fname = utils.path_tpfc_pfs(circuit.c_name, tp, batch)

        if os.path.exists(fc_fname):
            print(f"Loading PFS-TPFC from: {fc_fname}")
            fc = [float(x) for x in open(fc_fname, "r").readline().split(",")]
        else:
            print(f"PFS results NOT available, start running and saving into: {fc_fname}")
            pfs = PFS(circuit)
            pfs.fault_list.add_all()
            fc = pfs.tpfc(tp, fault_drop=1, verbose=False)
            with open(fc_fname, "w") as outfile:
                outfile.write(",".join([str(x) for x in fc]))
        arr = [list(range(1, tp+1)), fc, [batch]*tp]
        df = pd.concat([df, pd.DataFrame(np.array(arr).T, 
            columns=["tp", "fc", "batch"])],ignore_index=True)

    plot = sns.lineplot(x=df["tp"], y=df["fc"], alpha=0.8,
                        color="b", errorbar=('ci', plot_ci), label="PFS")
    
    plt.xlim=(PLOT_MIN_TP,tp)
    plt.ylim(min(df[df["tp"] == PLOT_MIN_TP]["fc"].tolist()), 100)

    if log_yscale:
        plot.set_yscale("function", functions=(exp, log))
        plot.set_yticks(yticks)

    plot.grid()
    plot.set_ylabel(f"Fault Coverage", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(f"Dependency of fault coverage on\n \
            random test patterns for {circuit.c_name}", fontsize=13)

    fname = utils.path_tpfc_pfs_fig(circuit.c_name, tp, times) 
    print(f"Figure saved in: {fname}")
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

    fname = utils.path_ppsf_ci(circuit.c_name, ci, cpu)

    if not os.path.exists(fname):
        tp_steps = PPSF_CI_TP_STEPS 
        gen_ppsf(circuit, tp_steps=tp_steps, ci=ci, num_proc=cpu)
    ppsf = PPSF(circuit)
    p_init = ppsf.load_pd_ppsf_conf(fname)    
    tps = np.arange(0, tp+1, 10)
    fcs = []
    for tp in tps:
        fcs.append(utils.estimate_FC(p_init, tp=tp)*100)
    
    plot = sns.lineplot(x=tps, y=fcs, color="red", label="PPSF")
    plot.set_yscale("function", functions=(exp, log))
    plot.set_yticks(yticks)
    plt.xlim=(PLOT_MIN_TP,tp)
    plot.set(xlim=(PLOT_MIN_TP,tp), ylim=(PLOT_MIN_Y,PLOT_MAX_Y))

    plot.grid()

    plot.set_ylabel(f"Fault Coverage (FC%)", fontsize=13)
    plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
    plot.set_title(
        f"fault coverage for random test patterns\n\
        for circuit {circuit.c_name} \n \
        method: PPSF", fontsize=13)

    fname = utils.path_tpfc_ppsf_fig(circuit.c_name, tp, ci, cpu) 
    print(f"Figure saved in: {fname}")
    plt.tight_layout()
    plt.savefig(fname)

def compare_tpfc(circuit, times_stafan, times_pfs, tp, tpLoad, ci, cpu):
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
    
    tpfc_stafan(circuit, tpLoad=tpLoad, tp=tp, times=times_stafan, num_proc=cpu)
    tpfc_pfs(circuit, times=times_pfs, tp=tp)
    tpfc_ppsf(circuit, ci=ci, cpu=cpu, tp=tp)

    plt.title(f"Dependency of fault coverage on\nrandom test patterns for {circuit.c_name}", 
            fontsize=13)

    fname = utils.path_tpfc_compare(circuit.c_name, tp, tpLoad, ci, cpu, 
            times_stafan, times_pfs)
    plt.tight_layout()
    plt.savefig(fname)
    print(f"Final figure saved in: {fname}")

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
        fname = utils.path_ppsf_ci(circuit.c_name, ci, cpu)
        if not os.path.exists(fname):
            _cis.remove(ci)
            print(f"Warning: Data is not available for CI={ci} in {fname}")
            continue
        ppsf = PPSF(circuit)
        res_ppsf = ppsf.load_pd_ppsf_conf(fname)
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

    path = os.path.join(FAULT_SIM_DIR, circuit.c_name + "/ppsf/")
    if not os.path.exists(path):
        os.makedirs(path)
    fname = f"ppsf-ci-{circuit.c_name}-minCI{min(_cis)}-maxCI{max(_cis)}.png"
    fname = os.path.join(path, fname)
    plt.tight_layout()
    plt.savefig(fname)
    print(f"\nFigure saved in {fname}")

def ppsf_corr_ci(circuit, cpu, _cis, heatmap=False):
    """ Scatter plot for each CI comparing to the maximum given CI. 
    Drawing heatmap is optional.
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

        fname = utils.path_ppsf_ci(circuit.c_name, c, cpu, moe=0.1)

        # fname = os.path.join(path, f"{circuit.c_name}_ppsf_ci{c}_proc{cpu}.ppsf")
        if not os.path.exists(fname):
            _cis.remove(c)
            print(f"Data is not available for CI={c} in :{fname}")
            continue
        ppsf = PPSF(circuit)
        cis.append(ppsf.load_pd_ppsf_conf(fname))

    fault_list = [i for i in cis[0].keys()]
    for f in fault_list:
        row = {"fault": f}
        for idx, c in enumerate(_cis):
            row["ci" + str(c)] = cis[idx][f]
            df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)

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

    fig.suptitle("Mean of detection probability\n\
    in the given confidence interval", fontsize=16)
    fig.tight_layout()
    
    path = os.path.join(FAULT_SIM_DIR, circuit.c_name)
    fname = f"{path}/ppsf/ppsf-corr-{circuit.c_name}-maxCI{max_ci}-proc{cpu}.png"
    plt.savefig(fname)
    print(f"Figure saved in {fname}")

def ppsf_error_ci(circuit, hist_scatter, cpu, _cis):
    """ Histogram or scatter plot for relative error of different PPSF fault coverage 
    results using different CIs with respect to the maximum given CI. In case of 
    histogram, KDE (Kernel Density Estimation) line is also drawn.

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
    if hist_scatter not in ['hist', 'scatter']:
        raise Exception('Warning: flag "figmode" is not passed.')
    df = pd.DataFrame(columns=["fault"].extend(["ci"+str(x) for x in _cis]))
    cis = []
    copy_cis = _cis.copy()
    for c in copy_cis:
        fname = utils.path_ppsf_ci(circuit.c_name, c, cpu, moe=0.1)
        path = os.path.join(FAULT_SIM_DIR, circuit.c_name)
        if not os.path.exists(fname):
            copy_cis.remove(c)
            print(f"Data is not available in: {fname}")
            continue
        ppsf = PPSF(circuit)
        cis.append(ppsf.load_pd_ppsf_conf(fname, mode="advanced"))
    
    if len(cis) == 0:
        raise Exception('No data was loaded.')
    
    fault_list = [i for i in cis[0].keys()]
    for f in fault_list:
        row = {"fault": f}
        for idx, c in enumerate(_cis):
            try:
                row["ci" + str(c)] = cis[idx][f]
            except:
                continue

        df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index = True)

    max_ci = max(copy_cis)
    copy_cis.remove(max_ci)
    max_ci_col = "ci" + str(max_ci)
    min_val = max(min((df["ci"+str(min(copy_cis))]-df[max_ci_col]) / df[max_ci_col]), -0.2)
    max_val = min(max((df["ci"+str(min(copy_cis))]-df[max_ci_col]) / df[max_ci_col]), 0.2)
    bins = np.linspace(min_val, max_val, 40)
    temp = []
    plt.rcParams["patch.force_edgecolor"] = False
    plt.figure(figsize=(24, 12))
    for idx, c in enumerate(copy_cis):
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
                            color=colors[idx], alpha=0.5, s=12,
                            label=col.replace("ci", "CI="))

            plt.xscale("log")
    
    min_ci = min(copy_cis)
    plt.title(f"Comparing error in faults detection probability (DP) measured" + \
            f"with PPSF \n\
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

    path = os.path.join(FAULT_SIM_DIR, circuit.c_name)
    fname = f"{path}/ppsf/ppsf-error-{circuit.c_name}-maxCI{max_ci}-minCI{min_ci}-" + \
            f"{hist_scatter}plot-proc{cpu}.png"
    plt.savefig(fname, bbox_inches="tight")
    print(f"Figure saved in {fname}")

def stafan(circuit: DFTCircuit, tps, ci=5, num_proc=5, plot=True): 
    """
    TODO: Description.
    TODO: finalize axis scales
    Parameters:
    -----------
    circuit : Circuit
    tps :  list

    """

    if len(tps)<2:
        raise Exception('Pass a list with at least two elements for tp')
    
    df = pd.DataFrame(columns=["Node", "C0", "C1", "B0", "B1","D0", "D1" ,"TP"])
    for tp in tps:
        fname = utils.path_stafan_code(circuit.c_name, tp)
        if not os.path.exists(fname):
            circuit.STAFAN(tp, num_proc=num_proc)
            circuit.save_STAFAN(fname=fname, verbose=False)
        else:
            circuit.load_STAFAN(fname)
        if plot == False:
            continue
        for n in circuit.nodes_lev:
            row = {"Node":n.num, "C0": n.C0, "C1": n.C1,
                            "B0": n.B0, "B1": n.B1,
                            "D0":n.B1*n.C1 ,"D1":n.B0*n.C0,
                            "TP":tp}
            df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)

    if plot == False:
        return 

    max_tp = max(tps)
    tps.remove(max_tp)

    df_max = df[df["TP"]==max_tp]
    df_error = pd.DataFrame(columns=["Node", "C0-error", "C1-error",
                                     "B0-error", "B1-error",
                                     "D0-error", "D1-error", "TP"])
    for tp in tps:
        for n in circuit.nodes_lev:
            row = {"Node":n.num, "TP":tp}
            dftp = df[df["TP"]==tp]
            for p in ["C0", "C1", "B0", "B1", "D0", "D1"]:
                a = float(dftp[dftp["Node"]==n.num][p])
                b = float(df_max[df_max["Node"]==n.num][p])
                if b!= 0:
                    row[f"{p}-error"] = (a-b)/b
                else:
                    row[f"{p}-error"] = 0

            df_error = pd.concat([df_error, pd.DataFrame(row, index=[0])], ignore_index=True)
    
    df_p = pd.DataFrame(columns=["C", "B", "D", "TP"])
    for p in [ "C", "B", "D"]:
        df_p[p] = pd.concat([df_error[f"{p}0-error"], df_error[f"{p}1-error"]], ignore_index=True)
        df_p["TP"] = pd.concat([df_error["TP"],df_error["TP"]], ignore_index=True)

    for p in ["C", "B", "D"]:
        mean = df_p[df_p["TP"]==min(tps)][p].mean(skipna=True)
        std = df_p[df_p["TP"]==min(tps)][p].std(skipna=True)
        # TODO4Ghazal: this formula requires limiting to min-max, but not that important
        min_val = max(mean-ci*std, min(df_p[df_p["TP"]==min(tps)][p]))
        max_val = min(mean+ci*std, max(df_p[df_p["TP"]==min(tps)][p]))
        bins_count = 20 if len(circuit.nodes_lev) < 500 else 40 
        # bins = np.linspace(min_val, max_val, bins_count)
        data = df_p[(df_p[p]>min_val) & (df_p[p]<max_val)]
        plt.rcParams["patch.force_edgecolor"] = False
        plt.rcParams['patch.linewidth'] = 0
        plt.rcParams['patch.edgecolor'] = 'none'

        sns.histplot(data=data, x=p, hue="TP",
                alpha=0.1, 
                kde=True, 
                palette=colors[:len(tps)])


        plt.rcParams["patch.force_edgecolor"] = False
        plt.rcParams['patch.linewidth'] = 0
        plt.rcParams['patch.edgecolor'] = 'none'

        plt.xlabel(f"Relative error")
        plt.ylabel("Node count")
        v = p.replace("C","controlability").replace("B","observability")
        v = v.replace("D","detectability")
        plt.title(f"Relative error of STAFAN {v} of {circuit.c_name} \n\
                compared to the maximum TP={max_tp}.\n \
                Showing errors distribution with CI={ci}")
        plt.tight_layout()

        path = os.path.join(STAFAN_DIR, circuit.c_name)
        fname = f"{path}/stafan-error-{v}-{circuit.c_name}-maxTP{max_tp}-CI{ci}.png"
        plt.savefig(fname)
        print(f"Figure saved in {fname}")
        plt.close()

    return 


def ppsf_stafan(circuit: DFTCircuit, tp, ci, num_proc): 
    graph = gen_graph(circuit, tp_count=tp, num_proc=num_proc, ci=ci)
    dp_ppsf = []
    dp_stafan = []
    rel_error = []
    for gnode in graph.nodes:
        gnode = graph.nodes[gnode]
        dp_ppsf.append(gnode["DP0"])
        dp_stafan.append(gnode["C1"]*gnode["B1"])
        dp_ppsf.append(gnode["DP1"])
        dp_stafan.append(gnode["C0"]*gnode["B0"])
    mse = 0
    mse_rel = 0
    for idx in range(len(dp_ppsf)):
        rel_error.append(abs(dp_ppsf[idx]-dp_stafan[idx])/dp_ppsf[idx])
        mse +=  (dp_ppsf[idx]-dp_stafan[idx])**2
        mse_rel += (abs(dp_ppsf[idx]-dp_stafan[idx])/dp_ppsf[idx])**2
    mse = mse / len(dp_ppsf)
    mse_rel = mse_rel / len(dp_ppsf) 
    # TODO: Double check this part of the implementation
    # print(f"HERE {circuit.c_name}\t MSE = {mse:.5f}\t MSE_REL = {mse_rel:5f}") 
    sns.scatterplot(x=dp_ppsf, y=rel_error)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Relative error of PPSF and STAFAN based on PPSF for " + circuit.c_name)
    plt.ylabel("Relative Error: abs(stafan-ppsf)/ppsf")
    plt.xlabel(f"PPSF detection probability, ci={ci}")
    fname = f"STAFAN-vs-PPSF-{circuit.c_name}-ci{ci}-proc{num_proc}.png" 
    fname = os.path.join(FIG_DIR, fname)
    plt.savefig(fname)
    print(f"Figure saved in: {fname}")


def dfc_pfs_analysis(circuit:DFTCircuit, tp_count, times, op_count, log=True):
    """ 
    TODOs: 
    - log fname
    - times is not considered
    - saving the generated TPs
    - summarizing the results and preparing the plot, 
    - making sure we are overwriting anything, log file can be unique
    - a few other steps ... review the code!
    """
    print("ERROR: this method is not completed yet")
    if  op_count > len(circuit.nodes_lev):
        nodes = circuit.nodes_lev
        op_count = len(circuit.nodes_lev)
    else:
        nodes = list(circuit.get_rand_nodes(op_count))

    tg = TPGenerator(circuit)
    tps = tg.gen_n_random(tp_count)
    tps_detected_init = []
    
    init_pfs = PFS(circuit)
    init_pfs.fault_list.add_all()
    all_faults = set([str(x) for x in init_pfs.fault_list.faults])

    for tp in tps:
        init_pfs = PFS(circuit)
        init_pfs.fault_list.add_all()
        tps_detected_init.append([str(x) for x in init_pfs._one_tp_run(tp, fault_drop=1)])

    # MSA: the main idea here was to not consider test patterns one after another
    fname_log = "just-test-deltaFC-PFS-{}.log".format(circuit.c_name)
    outfile = open(fname_log, "w")
    outfile.write("This is just a test!\n") # u can also write down the tps

    for op in nodes:
        if op.ntype in ["PO", "PI"]:
            continue
        outfile.write("\nOP={}\n".format(str(op)))
        
        tps_detected_post = []
        fanin_nodes = utils.get_fanin_BFS(circuit, op) # depth is missing
        op_pfs = PFS(circuit)
        op_pfs.fault_list.add_nodes(fanin_nodes)

        for idx, tp in enumerate(tps):
            # remove those faults that are detected by this tp
            new_faults = op_pfs.fault_list.remove_faults(tps_detected_init[idx])
            if len(new_faults) == 0:
                print("Skip!")
                tps_detected_post.append(set())
                continue
            new_pfs = PFS(circuit)
            new_pfs.fault_list.add_str_list(new_faults)
            circuit.PO.append(op)
            orig_ntype = op.ntype
            op.ntype = "PO"
            delta = set([str(x) for x in new_pfs._one_tp_run(tp, fault_drop=1)])
            tps_detected_post.append(delta)
        # Calculate TPFC for this OP:
        detected_init = set() # set(all_faults)
        detected_post = set() # set(all_faults)
        tpfc_init = []
        tpfc_post = []
        for idx, tp in enumerate(tps):
            detected_init = detected_init.union(set(tps_detected_init[idx]))
            detected_post = detected_post.union(set(tps_detected_init[idx]))
            detected_post = detected_post.union(tps_detected_post[idx])
            tpfc_init.append(100*len(detected_init)/len(all_faults))
            tpfc_post.append(100*len(detected_post)/len(all_faults))
            # print("Init={:.2f}%\tPost={:.2f}%".format(tpfc_init[-1], tpfc_post[-1]))
        outfile.write("Init," + ",".join([str(x) for x in tpfc_init]) + "\n")
        outfile.write("Post," + ",".join([str(x) for x in tpfc_post]) + "\n")
    # delta_fcs = pd.DataFrame(columns=["time","tp","delta_FC"])
    # path = f"../data/delta_FC_PFS/{circuit.c_name}/nodes"
    # if not os.path.exists(path):
    #     os.makedirs(path)
    
    # for node in nodes:
    #     delta_fcs = delta_fcs.append(obsv.deltaFC_PFS(circuit, node, tp, times, 5, log))
    #     fname = f"{path}/OP_node-{node.num}-op{op_count}-tp{tp}-times{times}.csv"
    #     delta_fcs.to_csv(fname)
    #     print(f"results saved in {fname}")
    # log_df = pd.DataFrame(columns=["OP_Node","times","TP","mu","std"])
    # for node in nodes:
    #     for t in range(tp):
    #         df_tp = delta_fcs[delta_fcs["tp"]==t]
    #         df_fc = df_tp[df_tp['OP_Node']==node.num]["delta_FC"]
    #         mu = df_fc.mean()
    #         std = df_fc.std()
    #         row = {"OP_Node":node.num,"times":times, "TP":t, "mu":mu, "std":std}
    #         log_df = log_df.append(row,ignore_index=True)

    # fname = f"../data/delta_FC_PFS/{circuit.c_name}/"
    # fname += f"deltaFC-PFS-{circuit.c_name}-op{op_count}-tp{tp}-times{times}.csv"
    # log_df.to_csv(fname)
    # print(f"logs saved in {fname}")

def gen_graph(circuit, tp_count, num_proc=20, ci=3):
    
    # SCOAP
    circuit.SCOAP()

    # STAFAN
    fname = utils.path_stafan(circuit.c_name, tp_count)
    if os.path.exists(fname):
        circuit.load_STAFAN(fname)
    else:
        IPython.embed()
        circuit.STAFAN(tp_count=tp_count, num_proc=num_proc, save_log=True)
    
    # PPSF with CI
    fname = utils.path_ppsf_ci(circuit.c_name, ci, num_proc, moe=0.1)
    ppsf = PPSF(circuit)
    if os.path.exists(fname):
        ppsf_res = ppsf.load_pd_ppsf_conf(fname)
        if len(ppsf_res) != 2*len(circuit.nodes_lev):
            print("\n\nWRONG FILE: " + fname)
            os.system(f"rm {fname}")
            tp_steps=[100,200,500,1000,5e3,1e4,2e4,5e4,1e5,2e5,5e5,1e6,2e6,5e6,1e7]
            gen_ppsf(circuit,tp_steps, ci, num_proc)
    else:
        tp_steps=[100,200,500,1000,5e3,1e4,2e4,5e4,1e5,2e5,5e5,1e6,2e6,5e6,1e7]
        gen_ppsf(circuit,tp_steps, ci, num_proc)  

    ## Graph  
    fname = utils.path_graph_v0(circuit.c_name, tp_count, ci, num_proc) 
    graph = circuit.gen_graph(fname)
    return graph


def gen_ppsf(circuit, tp_steps, ci=3, num_proc=8, moe=0.1, target_fault=None):
    ppsf = PPSF(circuit)
    tg = TPGenerator(circuit)
    fname = utils.path_ppsf_ci(circuit.c_name, ci, num_proc, moe)

    # TODO: Ad hoc method here 
    if target_fault is not None:
        fname = fname.replace(".ppsf", f"-{str(target_fault)}.ppsf")
        print(fname)

    if os.path.exists(fname):
        print(f"Data exists in: {fname}")
    else:
        print(f"Generating data for {fname}")
        _res, fl = ppsf.multiprocess_ci_run(tp_steps=tp_steps,
                target_fault=target_fault,
                log_fname=fname, verbose=True, ci=ci, num_proc=num_proc, 
                fault_count='all', save_log=True, mode="advanced", moe=moe)
        #TODO: maybe integrate this update into ppsf.multiprocess_ci_run
        for fault, dp in _res.items():
            node = fault.split('@')[0]
            stuck = fault.split('@')[1]
            circuit.nodes[node].stat["DP" + stuck] = dp

def profile(circuit, tp, num_proc, run_stafan=False):
    # circuit.STAFAN_C(tp)
    res = "Circuit name: " + circuit.c_name + "\t"
    res += "#Nodes: " + str(len(circuit.nodes)) + "\t"
    res += "#PI: " + str(len(circuit.PI)) + "\t"
    res += "#PO: " + str(len(circuit.PO)) + "\t"
    max_level = max([node.lev for node in circuit.PO])
    res += "Max-Lev: " + str(max_level) + "\t"
    print(res)
    if not run_stafan:
        return None
    circuit.STAFAN_multi_tmp(tp, num_proc)
    C0s = [x.C0 for x in circuit.nodes_lev]
    C1s = [x.C1 for x in circuit.nodes_lev]
    Cs = C0s + C1s
    levs = [node.lev for node in circuit.nodes_lev]


    bad_count = 0
    for c0 in C0s:
        if c0==1 or c0==0:
            bad_count += 1
    res += "#Bad-C: " + str(bad_count)
    print(res)
    return 
    
    _title = f"Gate={len(circuit.nodes)}, PI={len(circuit.PI)}, PO={len(circuit.PO)}"
    
    bins = 20
    if len(circuit.nodes_lev) > 1000:
        bins = 50

    # bins = np.logspace(np.floor(np.log10(min(C0s))), 
    #         np.log10(max(C0s)), 20)
    sns.histplot(C0s, bins=bins, kde=True)
    plt.title(_title + "\nC0 Histogram")
    # plt.xscale("log")
    plt.xlabel("STAFAN C0")
    plt.ylabel("Count")
    plt.savefig(circuit.c_name + "_Cs.png")
    plt.close()

    bins = 20
    if len(circuit.nodes_lev) > 1000:
        bins = 50
    sns.histplot(levs, bins=bins, kde=True)
    plt.title(_title + "\nLevel Histogram")
    plt.savefig(circuit.c_name + "_levs.png")
    plt.close()

if __name__ == "__main__":
    args = pars_args()
    prepare_env()
    plt.rcParams["figure.figsize"]= 9,8

    cis = [1, 2, 3, 4, 5, 6, 10]

    circuit = DFTCircuit(args.ckt)

    if args.func == "tpfc-stafan":
        tpfc_stafan(circuit=circuit, times=args.times,
                    tpLoad=args.tpLoad, tp=args.tp, num_proc=args.cpu)

    elif args.func == "tpfc-pfs":
        #TODO: consider parallel processing for this! 
        if circuit.c_name in AUTO_TP:
            print("TP count is automatically changed from {} to {}".format(
                        args.tp, AUTO_TP[circuit.c_name]))
            # args.tp = AUTO_TP[circuit.c_name] 
            args.tp = AUTO_TP[circuit.c_name]*2
        tpfc_pfs(circuit=circuit, tp=args.tp, times=args.times)

    elif args.func == "tpfc-ppsf":
        if circuit.c_name in AUTO_TP:
            args.tp = AUTO_TP[circuit.c_name] 
        tpfc_ppsf(circuit=circuit, ci=args.ci, cpu=args.cpu, tp=args.tp)
    
    elif args.func == "gen-ppsf":
<<<<<<< HEAD
        tp_steps = [100, 200, 500, 1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6] 
        gen_ppsf(circuit, tp_steps=tp_steps, 
                 ci=args.ci, num_proc=args.cpu,moe=0.1) 
=======
<<<<<<< HEAD
        tp_steps = [100, 200, 500, 1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6] 
        gen_ppsf(circuit, tp_steps=tp_steps, 
                 ci=args.ci, num_proc=args.cpu,moe=0.1) 
=======
        tp_steps = [100, 200, 500, 1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 
                1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7, 2e7, 5e7, 1e8]
        tp_steps = [2000]*200
        tp_steps = [200]*200
        gen_ppsf(circuit, tp_steps=tp_steps, 
                 ci=args.ci, num_proc=args.cpu,moe=0.05,
                 target_fault="n240@0") 
>>>>>>> f7f122f8183c3755e72044d076c98fc14c01e748
>>>>>>> 051a858a0c9dd4c902a7b2a31c743ce030d335b4

    elif args.func == "compare-tpfc":
        args.tp = 2*AUTO_TP[circuit.c_name] 
        compare_tpfc(circuit, times_stafan=1, times_pfs=args.times, 
                tp=args.tp, tpLoad=args.tpLoad, ci=args.ci, cpu=args.cpu)

    elif args.func == "ppsf-ci":
        cis = [2, 5, 10]
        ppsf_ci(circuit=circuit, cpu=args.cpu, _cis=cis)

    elif args.func == "ppsf-corr":
        cis = [1, 2, 3, 4, 5] # , 6, 7, 8, 9, 10]
        ppsf_corr_ci(circuit=circuit, _cis=cis, cpu=args.cpu)

    elif args.func == "ppsf-error":
        cis = [1, 2, 3, 4, 5] # , 6, 7, 8, 9, 10]
        if args.figmode == "both":
            ppsf_error_ci(circuit=circuit, hist_scatter="hist", cpu=args.cpu, _cis=cis)
            ppsf_error_ci(circuit=circuit, hist_scatter="scatter", cpu=args.cpu, _cis=cis)
        else:
            ppsf_error_ci(circuit=circuit, hist_scatter=args.figmode, 
                    cpu=args.cpu, _cis=cis)
    
    elif args.func == "stafan":
        tps = [1000,2000,5000,10**4,10**5,10**6]# , 10**7] #,10**8]
        stafan(circuit, tps=tps, ci=3, num_proc=args.cpu, plot=False)
        #TODO Some of the pandas methods are going to be deprecated 
    
    elif args.func == "gen-graph":
        gen_graph(circuit, tp_count=args.tp, num_proc=args.cpu, ci=args.ci)
    
    elif args.func == "ppsf-stafan":
        ppsf_stafan(circuit, tp=args.tp, ci=args.ci, num_proc=args.cpu)

    elif args.func == "profile":
        profile(circuit, args.tp, args.cpu, run_stafan=False) 

    elif args.func == "tnx":
        fname = utils.path_ppsf_ci(circuit.c_name, args.ci, args.cpu, 0.1)
        print(fname)
        if not os.path.exists(fname):
            print("ERROR: DOES NOT EXIST")
            exit()
        ppsf = PPSF(circuit)
        res = ppsf.load_pd_ppsf_conf(fname)
        PDs = list(res.values())
        bins = np.logspace(np.floor(10*np.log10(min(PDs)))/10,
                           np.log10(max(PDs)), 20)

        sns.histplot(PDs, bins=bins)  
        plt.xscale("log")
        plt.xlabel("PD using PPSF")
        plt.ylabel("Histogram of PDs")
        plt.title(f"Detection probability histogram with PPSF\n" + \
                f"for circuit {circuit.c_name}")

        plt.xlabel("PD using PPSF")
        path = os.path.join(FAULT_SIM_DIR, circuit.c_name + "/ppsf/")
        if not os.path.exists(path):
            os.makedirs(path)
        fname = f"ppsf-PD-hist-{circuit.c_name}-ci{args.ci}-log.png"
        fname = os.path.join(path, fname)
        plt.tight_layout()
        plt.savefig(fname)
        print(f"\nFigure saved in {fname}")





    # ^^ Testd up to here ^^

    #Delta FC
    elif args.func == "dfc-pfs":
        dfc_pfs_analysis(circuit, tp_count=args.tp, times=args.times, 
                op_count=args.opCount)

    elif args.func == "stafan-hist":
        fname = utils.path_stafan_code(circuit.c_name, args.tp)
        print(fname)                                                         
        if not os.path.exists(fname):                                        
            print("ERROR: DOES NOT EXIST")                                   
            exit()                                                           
        circuit.load_STAFAN(fname)
        PDs = []
        for node in circuit.nodes_lev:
            PDs.append(node.C1 * node.B1)
            PDs.append(node.C0 * node.B0)
        #print(min(PDs), max(PDs))
        # bins = np.logspace(np.floor(10*np.log10(min(PDs)))/10, np.log10(max(PDs)), 20)
        sns.histplot(PDs, bins=20)                                         
        plt.xscale("log")                                                    
        plt.xlabel("PD using STAFAN") 
        plt.ylabel("Histogram of PDs")                                       
        plt.title(f"Detection probability histogram with STAFAN\n" + \
                f"for circuit {circuit.c_name}")                             
        plt.xlabel("PD using PPSF")                                          
        # path = os.path.join(STAFAN_DIR, circuit.c_name ")        
        # if not os.path.exists(path):                                         
        #         os.makedirs(path)                                                
        fname = f"ppsf-PD-hist-{circuit.c_name}-ci{args.ci}-log.png"         
        # fname = os.path.join(path, fname)                                    
        plt.tight_layout()                                                   
        plt.savefig(fname)                                                   
        print(f"\nFigure saved in {fname}")                                  
        IPython.embed()

    else:
        raise ValueError(f"Function \"{args.func}\" does not exist.")
    
