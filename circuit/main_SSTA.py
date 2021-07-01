
import argparse
import pdb
import math
import time
from random import randint
from circuit import Circuit
import sys
import config
from load_circuit import LoadCircuit

# sys.path.insert(1, "/home/msabrishami/workspace/StatisticsSTA/")
from distributions import Distribution, Normal, SkewNormal, MaxOp, SumOp
import distributions as dist

parser = argparse.ArgumentParser()
parser.add_argument("-ckt", type=str, default="c17", help="circuit name, c17, no extension")
parser.add_argument("-mode", type=str, default="alt", help="circuit name, c17, no extension")
parser.add_argument("-samples", type=int, default=100, help="SSTA samples")
args = parser.parse_args()
config.SAMPLES = args.samples


from distributions import Triangle, Uniform
import matplotlib.pyplot as plt

# d1 = Triangle(0,4,1)
# d2 = Triangle(10,18,11)
# d1 = Uniform(1,2)
# d2 = Uniform(4,6)
# T1,f1 = d1.pmf(100)
# T2,f2 = d2.pmf(100)
# 
# plt.plot(T1, f1, color='r')
# plt.plot(T2, f2, color='b')
# T1,F1 = d1.cmf(100)
# T2,F2 = d2.cmf(100) 
# plt.plot(T1,F1, color='g')
# plt.plot(T2,F2, color='c')
# 
# opsum = SumOp()
# T, f_T = opsum.sum_num(d1, d2, 100).pmf()
# plt.plot(T, f_T, color='black', ls='-')
# plt.savefig("triangle-dist.pdf")

circuit = Circuit(args.ckt)
circuit.lev()
# circuit.load_mchist("MOSFET_16nm_HP")
# circuit.ssta_pmf()
circuit.SSTA(mode=args.mode, samples=args.samples)
fname = "./results/ssta-{}-{}-s{}-SK.png".format(circuit.c_name, args.mode, args.samples)
circuit.ssta_plot(fname=fname)
# temp = circuit.load_mchist("MOSFET_16nm_HP")


