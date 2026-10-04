"""Locations of data and shared constants.

All paths are derived from ``DATA_DIR``. It defaults to the ``data/`` folder of
a source checkout; set the ``PYCAD_DATA_DIR`` environment variable to use a
different location, for example when PyCAD is installed from a wheel.
"""
import os

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.environ.get("PYCAD_DATA_DIR", os.path.join(_REPO_ROOT, "data"))

# Benchmark circuits
CKT_DIR = os.path.join(DATA_DIR, "ckt")
VERILOG_DIR = os.path.join(DATA_DIR, "verilog")

ISCAS85_DIR = os.path.join(VERILOG_DIR, "ISCAS85")
ISCAS89_DIR = os.path.join(VERILOG_DIR, "ISCAS89")
EPFL_DIR = os.path.join(VERILOG_DIR, "EPFL")

ISCAS85_V0_DIR = os.path.join(ISCAS85_DIR, "v0")
ISCAS85_V1_DIR = os.path.join(ISCAS85_DIR, "v1")
ISCAS85_V2_DIR = os.path.join(ISCAS85_DIR, "v2")

EPFL_V0_DIR = os.path.join(EPFL_DIR, "v0")
EPFL_V1_DIR = os.path.join(EPFL_DIR, "v1")
EPFL_V2_DIR = os.path.join(EPFL_DIR, "v2")

ALL_CIRCUIT_DIRS = [CKT_DIR,
                    ISCAS85_V0_DIR, ISCAS85_V1_DIR, ISCAS85_V2_DIR,
                    EPFL_V0_DIR, EPFL_V1_DIR, EPFL_V2_DIR,
                    ISCAS89_DIR]

ALL_ISCAS85 = ["c17", "c432", "c499", "c880", "c1355", "c1908", "c3540", "c5315", "c6288", "c7552"]

# Generated results (not tracked by git)
PATTERN_DIR = os.path.join(DATA_DIR, "patterns")
FAULT_SIM_DIR = os.path.join(DATA_DIR, "fault_sim")
STAFAN_DIR = os.path.join(DATA_DIR, "stafan-data")
SCOAP_DIR = os.path.join(DATA_DIR, "scoap-data")

# Logic value used for an unknown signal in ternary simulation
X_VALUE = "X"

# Standard-cell names recognised for each gate type
CELL_NAMES = {
    "XOR": ["xor", "XOR2", "XOR2_X1"],
    "XNOR": ["xnor", "XNOR2", "XNOR2_X1"],
    "OR": ["or", "OR2", "OR2_X1", "OR", "OR2_X2", "OR3_X1", "OR4_X1"],
    "NOR": ["nor", "NOR2", "NOR2_X1", "NOR2_X2", "NOR3_X1", "NOR4_X1"],
    "AND": ["and", "AND2", "AND2_X1", "AND", "AND2_X2", "AND3_X1", "AND4_X1"],
    "NAND": ["nand", "NAND2", "NAND2_X2", "NAND3_X1", "NAND4_X1", "NAND2_X1"],
    "NOT": ["not", "inv", "NOT", "INV_X1", "INV_X2", "INV_X4"],
    "BUFF": ["buff", "buf",
             "CLKBUF_X12", "CLKBUF_X1", "CLKBUF_X2", "CLKBUF_X4", "CLKBUF_X8", "CLKBUF_X16",
             "BUF_X1", "BUF_X2", "BUF_X4", "BUF_X8"],
}

# Statistical static timing analysis (SSTA): technology and process variations
SSTA_DATA_DIR = os.path.join(DATA_DIR, "cell_ssta")
SAMPLES = 100
PVS = "vth0-N0.03_lg-N0.05_w-N0.05_toxe-N0.10_ndep-N0.05_MC20000"
TECH = "MOSFET_45nm_HP"
