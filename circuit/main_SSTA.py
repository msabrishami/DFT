
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

circuit = Circuit(args.ckt)
LoadCircuit(circuit, "ckt")
circuit.lev()
# circuit.load_mchist("MOSFET_16nm_HP")
# circuit.ssta_pmf()
circuit.SSTA(mode=args.mode, samples=args.samples)
fname = "ssta-{}-{}-SK.png".format(args.ckt, args.mode)
circuit.ssta_plot(fname=fname)
# temp = circuit.load_mchist("MOSFET_16nm_HP")


