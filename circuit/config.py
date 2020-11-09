

MODELSIM_DIR = "../data/modelsim"
MODELSIM_INPUT_DIR = "input" 
MODELSIM_GOLD_DIR = "gold" 
MODELSIM_OUTPUT_DIR = "output" 
VERILOG_DIR = "../data/verilog"
# VERILOG_DIR = "../data/EPFL"
PATTERN_DIR ="../data/pattern"
# in each modelsim prj directory where inputs will be stored
## TODO for Ting-Yu: read a good description for these constants

FAULT_DICT_DIR = "../data/fault_dict_new"
FAULT_SIM_DIR = "../data/fault_sim"
CKT_DIR = "../data/ckt"
# TEST POINT INSERTION PROBLEM:
HTO_TH = 0.02
HTC_TH = 0.05
STAFAN_B_MIN = 0.0001
STAFAN_C_MIN = 0.001


# LOGIC LIBRARY RELATED:
CELL_NAMES = {
        "XOR": ["xor", "XOR2"],
        "XNOR": ["xnor", "XNOR2"],
        "OR": ["or", "OR2", "OR2_X1", "OR"],
        "NOR": ["nor", "NOR2", "NOR2_X1"],
        "AND": ["and", "AND2", "AND2_X1", "AND"],
        "NAND": ["nand", "NAND2"],
        "NOT": ["not", "inv", "NOT", "INV_X1", "INV_X2"],
        "BUFF": ["buff", "buf"]
        }
