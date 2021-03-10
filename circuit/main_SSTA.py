
import argparse
import pdb
import math
import time
from random import randint
from circuit import Circuit
import sys
import config
from load_circuit import LoadCircuit
parser = argparse.ArgumentParser()
parser.add_argument("-ckt", type=str, default="c17", help="circuit name, c17, no extension")
args = parser.parse_args()

sys.path.insert(1, "/home/msabrishami/workspace/StatisticsSTA/")
from distributions import Distribution, Normal, SkewNormal, MaxOp, SumOp
import distributions as dist

circuit = Circuit(args.ckt)
LoadCircuit(circuit, "ckt")
circuit.lev()
circuit.load_mchist("MOSFET_16nm_HP")
circuit.ssta_pmf()
circuit.ssta_plot()
temp = circuit.load_mchist("MOSFET_16nm_HP")


