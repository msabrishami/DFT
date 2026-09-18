"""Experiment-only constants moved out of pycad.config.

Used by the scripts in legacy/experiments; the library itself does not need them.
"""
import os

from pycad.config import DATA_DIR

# ModelSim projects
MODELSIM_DIR = os.path.join(DATA_DIR, "modelsim")
MODELSIM_INPUT_DIR = "input"
MODELSIM_GOLD_DIR = "gold"
MODELSIM_OUTPUT_DIR = "output"

# Experiment output directories
FAULT_DICT_DIR = os.path.join(DATA_DIR, "fault_dict")
FIG_DIR = os.path.join(DATA_DIR, "figures")
GRAPH_DIR = os.path.join(DATA_DIR, "graph-data")

# Test point insertion problem
HTO_TH = 0.1
HTC_TH = 0.05
STAFAN_B_MIN = 0.0001
STAFAN_C_MIN = 0.001

PPSF_STEPS = [50, 100, 200, 500,
              1e3, 2e3, 5e3, 1e4, 2e4, 5e4,
              1e5, 2e5, 5e5, 1e6, 2e6, 5e6]
PPSF_CI_TP_STEPS = [100, 200, 500, 1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]

# Benchmark circuit names
ALL_EPFL_EZ = ["arbiter", "sin", "bar", "dec", "int2float",
               "multiplier", "cavlc", "adder", "max", "priority", "voter"]
ALL_EPFL_HARD = ["hyp", "square", "router", "log2", "div", "sqrt", "mem_ctrl", "i2c", "ctrl"]

# Number of test patterns found by an automatic test pattern generator, per circuit
AUTO_TP = {
        "c432_synV0": 890, 
        "c432_synV1": 1090,
        "c432_synV2": 890,
        "c499_synV0": 1320,
        "c499_synV1": 2050,
        "c499_synV2": 2080,
        "c880_synV0": 4030,
        "c880_synV1": 3020,
        "c880_synV2": 3370,
        "c1355_synV0": 1290,
        "c1355_synV1": 2000,
        "c1355_synV2": 2070,
        "c1908_synV0": 3030,
        "c1908_synV1": 3610,
        "c1908_synV2": 3690,
        "c3540_synV0": 2830,
        "c3540_synV1": 2680,
        "c3540_synV2": 2700,
        "c5315_synV0": 1250,
        "c5315_synV1": 1310,
        "c5315_synV2": 1190,
        "c6288_synV0": 240,
        "c6288_synV1": 270,
        "c6288_synV2": 250}
