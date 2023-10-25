import os
import operator
import numpy as np

from collections import deque
from functools import reduce
import config as cfg

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

mul_list = lambda arr: reduce(operator.mul, arr, 1)

not_gate = lambda a: 1-a

def ckt_type(cname):
    print("FIX ME LATER -- CKT TYPE AUTOMATIC DETECTION")
    return "EPFL"
    if cname in cfg.ALL_ISCAS85:
        return "ISCAS85"
    elif cname in cfg.ALL_EPFL:
        return "EPFL"
    else:
        raise NameError("Circuit is not known")

def bin2int(bin_arr):
    """ Its the other way around ... """ 
    int_val = 0
    print(bin_arr)
    for idx, val in enumerate(bin_arr):
        int_val += (val * (2**idx))
    print(int_val)
    return int_val

def int2binList(val, bitwidth):
    res = [] 
    for k in range(bitwidth):
        res.append(val%2)
        val = int(val/2)
    return res

def comp_Zg_Zf_bin(Zg, Zf, bitwidth):
    """ Compare two output dictionaries if the logic values are 
    binary, like in PPSF fault simulation 
    Zg and Zf are integer values.
    
    Return
    -------
    indices of test patterns that detected a fault
    """ 
    tps = set()
    for k in Zg:
        val_g = bin(Zg[k])[2:][-bitwidth:]
        val_f = bin(Zf[k])[2:][-bitwidth:]
        val_g = "".join(['0']*(bitwidth - len(val_g))) + val_g
        val_f = "".join(['0']*(bitwidth - len(val_f))) + val_f
        for j in range(len(val_g)):
            if val_g[j] != val_f[j]:
                tps.add(j)
    return tps 

def print_out_bin(Z):
    for k in Z:
        print(k + "\t" + "{:064b}".format(Z[k]))

def get_node_gtype_fin(node):
    """ converts a node type from CKT658 to "c<lower-case><#fin>"
    e.g. NAND with 3 inputs --> cnand2 
    can be used for changing CSM cells into DFT cells 
    """
    if node.ntype in ["PI", "FB"]:
        return node.gtype
    if node.gtype == "NOT":
        return "cinv"
    if node.gtype == "BUFF":
        return "cbuff"
    if node.gtype in ["OR", "NOR", "NAND", "AND", "XOR", "XNOR"]:
        return "c" + node.gtype.lower() + str(len(node.unodes))

def get_fanin_rec(circuit, node, res):
    """ Only called within get_fanin mehtod, 
    The recursive method for getting the fanins-code of node in a circuit 
    Using DFS approach 
    """
    if node.num in res:
        return res
    res.add(node.num)
    if node.gtype == "IPT":
        return res
    for unode in node.unodes:
        res.update(get_fanin_rec(circuit, unode, res))
    return res

def get_fanin(circuit, node):
    """ Find the nodes in the fanin-cone of a node in a circuit 
    Using semi-DFS approach 
    Returns a set of node numbers
    Note: not really DFS, as we are considering levels, and not depth. 
    """
    if isinstance(node, str):
        node = circuit.nodes[node]
    res = set() 
    get_fanin_rec(circuit, node, res)
    return res


def get_fanin_depth(circuit, node, lev_depth):
    """ Finds the nodes in the fanin-cone of a node in a circuit
    within a specific depth from the source node
    The distance is based on hop-based min distance, and not circuit level
    The algorithm is based on BFS running backward in circuit graph
    node.flagA is used to record the backward level value
    """
    res = []
    q = deque()
    q.append(node)
    node.flagA = 0 
    
    while(len(q) != 0):
        current_node = q.popleft()
        res.append(current_node)
        if current_node.flagA == lev_depth:
            continue
        for unode in current_node.unodes:
            if unode.flagA != None: # we have already seen it! 
                continue
            unode.flagA = current_node.flagA + 1 
            q.append(unode)

    for n in res:
        n.flagA = None
    
    return res


def get_fanin_BFS(circuit, node, lev_depth=False):
    """ Finds the nodes in the fanin-cone of a node in a circuit
    returns an ordered list of nodes 
    Using BFS approach, based on level of nodes, and not hop-based
    lev_depth : int 
        depth of search based on level 
    Note: not really BFS, as we are considering levels, and not hop-based depth
    Note: node.flagA is used within this method 
    """
    if lev_depth:
        return get_fanin_depth(circuit, node, lev_depth)

    res = []
    q = deque()
    q.append(node)
    node.flagA = True
    
    while(len(q) != 0):
        current_node = q.popleft()
        res.append(current_node)
        for unode in current_node.unodes:
            if unode.flagA != None:
                continue
            unode.flagA = True
            q.append(unode)
    
    for n in res:
        n.flagA = None
    
    return res

def estimate_FC(probs, tp): 
    #TODO 4 Ghazal : documentation 
    # probs is a dictionary, keys are faults strings, and values are ppsf probs
    """ estimating the fault coverage of a circuit based on all the faults """
    nfc = 0
    for key in probs:
        nfc += np.exp(-probs[key] * tp)

    return 1 - nfc/len(probs)

def fix_size(number, k):

    while len(number) > k:
        number = number[1:]

    while len(number) < k:
        number = '0'+number

    return number    


def path_ppsf():
    pass


def path_ppsf_ci(c_name, ci, cpu):
    path = os.path.join(cfg.FAULT_SIM_DIR, c_name)
    path = os.path.join(path, "ppsf")
    if not os.path.exists(path):
        os.makedirs(path)
    fname = f"{c_name}_ppsf_ci{ci}_proc{cpu}.ppsf"
    fname = os.path.join(path, fname)
    return fname

def path_ppsf_ci_try(c_name, ci, cpu, max_idx=20):
    path = os.path.join(cfg.FAULT_SIM_DIR, c_name)
    path = os.path.join(path, "ppsf")

    for i in range(max_idx):
        fname = f"{c_name}-ppsf-ci{ci}-proc{cpu}-try{i}.log"
        fname = os.path.join(path, fname)
        if not os.path.exists(fname):
            break
    return fname

def path_stafan(c_name, tp):
    path = os.path.join(cfg.STAFAN_DIR, c_name)
    fname = os.path.join(path, f"{c_name}_tp{tp}.stafan")
    return fname

def path_graph_v0(c_name, tp, ci, cpu):
    if not os.path.exists(cfg.GRAPH_DIR):
        os.mkdir(cfg.GRAPH_DIR)
    fname = f"{c_name}-stafan{tp}-ci{ci}-proc{cpu}"
    fname = os.path.join(cfg.GRAPH_DIR, fname + ".gml")
    return fname 

def path_stafan_code(c_name, tp, code=None):
    path = os.path.join(cfg.STAFAN_DIR, c_name)
    if not os.path.exists(path):
        os.makedirs(path)
    if code is None:
        fname = os.path.join(path, f"{c_name}-tp{tp}.stafan")
    else:
        fname = os.path.join(path, f"{c_name}-tp{tp}-{code}.stafan")
    return fname 

def path_tpfc_pfs(c_name, tp, idx):
    path = os.path.join(cfg.FAULT_SIM_DIR, c_name)
    if not os.path.exists(path):
        os.makedirs(path)
    fname = os.path.join(path, f"tpfc-pfs-{c_name}-tp{tp}-part{idx}.csv")
    return fname

def path_tpfc_ppsf_fig(c_name, tp, ci, cpu):
    fname = f"tpfc-ppsf-{c_name}-tp{tp}-ci{ci}-proc{cpu}.png"
    fname = os.path.join(cfg.FIG_DIR, fname)
    return fname

def path_tpfc_pfs_fig(c_name, tp, times):
    fname = f"tpfc-pfs-{c_name}-tp{tp}-times{times}.png"
    fname = os.path.join(cfg.FIG_DIR, fname)
    return fname

def path_tpfc_compare(c_name, tp, tpLoad, ci, cpu, k_stafan, k_pfs):
    fname = f"tpfc-compare-{c_name}-tp{tp}-ci{ci}"
    fname += f"-tpLoad{tpLoad}-proc{cpu}-Kpfs{k_pfs}-Kstafan{k_stafan}.png"
    fname = os.path.join(cfg.FIG_DIR, fname)
    return fname



