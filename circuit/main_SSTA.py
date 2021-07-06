
import argparse
import os
import pdb
import math
import time
from random import randint
from circuit import Circuit
import sys
import config
import utils
from load_circuit import LoadCircuit

# sys.path.insert(1, "/home/msabrishami/workspace/StatisticsSTA/")
from distributions import Distribution, Normal, SkewNormal, MaxOp, SumOp, NumDist
import distributions as dist

parser = argparse.ArgumentParser()
parser.add_argument("-ckt", type=str, default="c17", help="circuit name, c17, no extension")
parser.add_argument("-mode", type=str, default="alt", help="circuit name, c17, no extension")
parser.add_argument("-samples", type=int, default=100, help="SSTA samples")
args = parser.parse_args()
config.SAMPLES = args.samples


from distributions import Triangle, Uniform
import matplotlib.pyplot as plt


def test_triangle():
    """ Testing simple sum of simple distributions """ 
    d1 = Triangle(0,4,1)
    d2 = Triangle(10,18,11)
    d1 = Uniform(1,2)
    d2 = Uniform(4,6)
    T1,f1 = d1.pmf(100)
    T2,f2 = d2.pmf(100)
    
    plt.plot(T1, f1, color='r')
    plt.plot(T2, f2, color='b')
    T1,F1 = d1.cmf(100)
    T2,F2 = d2.cmf(100) 
    plt.plot(T1,F1, color='g')
    plt.plot(T2,F2, color='c')
    
    opsum = SumOp()
    T, f_T = opsum.sum_num(d1, d2, 100).pmf()
    plt.plot(T, f_T, color='black', ls='-')
    plt.savefig("triangle-dist.pdf")


def test_sum_chain():
    
    # Basic Distribution 
    # d1 = Uniform(0, 2)
    # d1 = Triangle(0, 20, 10)
    # d1 = Normal(0, 1)
    # d1 = SkewNormal(0,1,1)
    # T, f_T = d1.pmf(512)
    
    # Load from HSPICE Simulation files
    fname = "MOSFET_45nm_LP_cand2_" 
    fname += "vth0-N0.03_lg-N0.05_w-N0.05_toxe-N0.10_ndep-N0.05_MC50000.mcraw"
    fname = os.path.join(config.SSTA_DATA_DIR, "mcraw/"+fname)
    delays = utils.load_mcraw(fname)
    
    # T, f_T = utils.mcraw2mchist(delays, bins=200, pad=3) # , cut=(0.0005, 0.0005)
    T, f_T = utils.mcraw2mchist(delays, bins=200) # , cut=(0.0005, 0.0005)
    f_T = utils.smooth_hist(f_T, window=5) 
    d1 = NumDist(T, f_T)

    plt.plot(T, f_T, label="Initial")
    print("Initial Area: \t{:.6f}".format(Distribution.area_pmf(T, f_T)))
    opsum = SumOp()
    dd = d1
    for i in range(20):
        dd = opsum.sum_num(dd, d1)
        T, f_T = dd.pmf()
        plt.plot(T, f_T, label="Sum {}".format(i))
        print("Level {} | Area: {:.6f}".format(i, dd.area()))
    plt.legend()
    plt.savefig("SumChain-MOSFET.pdf") 
    plt.close()


def test_mchist_plot():

    TECH = "MOSFET_45nm_LP"
    MCs = [10000, 20000, 50000]
    BINs = [100, 200, 400]
    SMs = [0, 3, 5, 11]
    MC = "MC10000"

    for cell in ["cnand2", "cnand3", "cnand4",
            "cnor2", "cnor3", "cnor4",
            "cand2", "cand3", "cand4",
            "cor2", "cor3", "cor4",
            "cbuff", "cinv"]:
        
        fig, ax = plt.subplots(len(BINs), len(SMs), figsize=(40,20))
        fig.suptitle("Cell: {}, {}".format(cell, MC))

        fname = "../data/cell_ssta/mcraw/" + TECH + "_" + cell + "_"
        fname += "vth0-N0.03_lg-N0.05_w-N0.05_toxe-N0.10_ndep-N0.05_" + MC + ".mcraw"
        delays = utils.load_mcraw(fname)
        # fname = "../data/cell_ssta/mchist/" + TECH + "_" + cell + "_" + MC
        # T, f_T = utils.mcraw2mchist(delays, bins, fname=fname + ".mchist", verbose=True)

        for i, bins in enumerate(BINs):
            for j, sm in enumerate(SMs):
                T, f_T = utils.mcraw2mchist(delays, bins)
                if sm != 0:
                    f_T = utils.smooth_hist(f_T, window=sm) 
                # print("Cell: {}\tArea: {:.6f}".format(cell, d.area()))
                ax[i,j].plot(T, f_T, linewidth=2, color='blue', linestyle='-')
                ax[i,j].set_title("Bins: {} Smooth-Window: {}".format(bins, sm))

        for ax in fig.get_axes():
            ax.label_outer()
        fig.savefig(TECH + "_" + cell + "_" + MC + ".pdf")
        plt.close()


# test_sum_chain()
# test_mchist_plot()
circuit = Circuit(args.ckt)
circuit.lev()
# for node in circuit.nodes_lev:
#     print(node.ntype, node.gtype, utils.get_node_gtype_fin(node))
print(args.ckt)
# circuit.set_cell_ssta_delay(src="mcraw")
# circuit.load_mchist("MOSFET_16nm_HP")
# circuit.ssta_pmf()
circuit.ssta_sim(mode=args.mode, src="mcraw", samples=args.samples)
fname = "./results/ssta-{}-{}-s{}-{}.png".format(circuit.c_name, args.mode, args.samples, config.TECH)
circuit.ssta_plot(fname=fname, select="gate")
# temp = circuit.load_mchist("MOSFET_16nm_HP")


