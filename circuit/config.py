import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

LIB_CELLS_PATH = os.path.join(DATA_DIR, "library")
MODELSIM_DIR = os.path.join(DATA_DIR, "modelsim")

MODELSIM_INPUT_DIR = "input" 
MODELSIM_GOLD_DIR = "gold" 
MODELSIM_OUTPUT_DIR = "output" 

"""Circuits Absolute Directories"""
CKT_DIR = os.path.join(DATA_DIR, "ckt")
VERILOG_DIR = os.path.join(DATA_DIR, 'verilog')

ISAS89_DIR = os.path.join(VERILOG_DIR, 'ISCAS89')
ISCAS85_DIR = os.path.join(VERILOG_DIR, 'ISCAS85')
EPFL_DIR = os.path.join(VERILOG_DIR, 'EPFL')

ISCAS85_V0_DIR = os.path.join(ISCAS85_DIR, 'v0')
ISCAS85_V1_DIR = os.path.join(ISCAS85_DIR, 'v1')
ISCAS85_V2_DIR = os.path.join(ISCAS85_DIR, 'v2')

EPFL_V0_DIR = os.path.join(EPFL_DIR, 'v0')
EPFL_V1_DIR = os.path.join(EPFL_DIR, 'v1')
EPFL_V2_DIR = os.path.join(EPFL_DIR, 'v2')

ISCAS89_DIR = os.path.join(VERILOG_DIR, 'ISCAS89')

ALL_CIRCUIT_DIRS = [CKT_DIR, 
                    ISCAS85_V0_DIR, ISCAS85_V1_DIR, ISCAS85_V2_DIR,
                    EPFL_V0_DIR, EPFL_V1_DIR, EPFL_V2_DIR,
                    ISCAS89_DIR]

"""Others in data/"""
PATTERN_DIR =os.path.join(DATA_DIR, "patterns")
FAULT_DICT_DIR = os.path.join(DATA_DIR, "fault_dict")
FAULT_SIM_DIR = os.path.join(DATA_DIR, "fault_sim")
STAFAN_DIR = os.path.join(DATA_DIR, "stafan-data")
FIG_DIR = os.path.join(DATA_DIR, "figures")

"""Test Point Insertion Poblem"""
HTO_TH = 0.1
HTC_TH = 0.05
STAFAN_B_MIN = 0.0001
STAFAN_C_MIN = 0.001

PPSF_STEPS = [50, 100, 200, 500, 
        1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 
        1e5, 2e5, 5e5, 1e6, 2e6, 5e6]
SAMPLES = 100

V_FORMATS = ["EPFL", "ISCAS85"]

"""Logic Library Related"""
CELL_NAMES = {
        "XOR": ["xor", "XOR2", "XOR2_X1"],
        "XNOR": ["xnor", "XNOR2", "XNOR2_X1"],
        "OR": ["or", "OR2", "OR2_X1", "OR", "OR2_X2", "OR3_X1", "OR4_X1"],
        "NOR": ["nor", "NOR2", "NOR2_X1", "NOR2_X2", "NOR3_X1", "NOR4_X1"],
        "AND": ["and", "AND2", "AND2_X1", "AND", "AND2_X2", "AND3_X1", "AND4_X1"],
        "NAND": ["nand", "NAND2", "NAND2_X2", "NAND3_X1", "NAND4_X1", "NAND2_X1"],
        "NOT": ["not", "inv", "NOT", "INV_X1", "INV_X2", "INV_X4"],
        "BUFF": ["buff", "buf", 
            "CLKBUF_X12", "CLKBUF_X1", "CLKBUF_X2","CLKBUF_X4","CLKBUF_X8","CLKBUF_X16",
            "BUF_X1", "BUF_X2", "BUF_X4", "BUF_X8"]
        }

ALL_ISCAS85=["c17","c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"] 
ALL_EPFL_EZ=["arbiter", "sin", "bar","dec", "int2float", 
        "multiplier", "cavlc", "adder", "max", "priority", "voter"]
ALL_EPFL_HARD = ["hyp", "square", "router", "log2", "div", "sqrt", "mem_ctrl", "i2c", "ctrl"]

SSTA_DATA_DIR = os.path.join(DATA_DIR, "cell_ssta")

PVS = "vth0-N0.03_lg-N0.05_w-N0.05_toxe-N0.10_ndep-N0.05_MC20000"
TECH = "MOSFET_45nm_HP"

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

X_VALUE = 'X'