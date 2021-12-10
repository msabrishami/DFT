
import numpy as np
import config
import matplotlib.pyplot as plt
import pdb
import sys
import math
from multiprocessing import Process, Pipe
from collections import deque

def ckt_type(cname):
    print("FIX ME LATER -- CKT TYPE AUTOMATIC DETECTION")
    return "EPFL"
    if cname in config.ALL_ISCAS85:
        return "ISCAS85"
    elif cname in config.ALL_EPFL:
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
    Zg and Zf are integer values """ 
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
    Using DFS approach 
    Returns a set of node numbers
    TODO: is this really DFS, because we are considering levels, and not depth 
    """
    if isinstance(node, str):
        node = circuit.nodes[node]
    res = set() 
    get_fanin_rec(circuit, node, res)
    return res
    
def get_fanin_BFS(circuit, node, lev_depth=None):
    """ Finds the nodes in the fanin-cone of a node in a circuit
    returns an ordered list of nodes
    Using BFS approach 
    lev_depth : int 
        depth of search based on level 
    TODO: is this really BFS, because we are considering levels, and not depth
    """
    q = deque()
    res = []
    visited = set()
    lev_depth = len(circuit.nodes) if lev_depth==None else lev_depth
    lev_max = node.lev - lev_depth
    q.append(node)
    visited.add(node.num)
    
    while(len(q) != 0):
        current_node = q.popleft()
        # print(current_node)
        res.append(current_node)
        for unode in current_node.unodes:
            if (unode.num in visited) or (unode.lev < lev_max) :
                continue
            visited.add(unode.num)
            q.append(unode)
    
    return res
    
   
def load_ppsf_parallel(fname):
    """ loads a ppsf_parallel simulated log file 
    the last line is time """ 
    lines = open(fname, "r").readlines()
    res = {}
    for line in lines[:-1]:
        words = line.strip().split(",")
        res[words[0]] = [int(x) for x in words[1:]]
    return res

def load_ppsf_parallel_step(fname):
    #TODO: ppsf-step is based on accumulated TPs now, wrong load 
    """ loads a ppsf_parallel_step simulated log file 
    """ 
    lines = open(fname, "r").readlines()
    res = {}
    current_tp = 0
    for line in lines:
        if line.startswith("#TP="):
            current_tp += float(line.split("=")[-1])
            print(current_tp)
            continue
        if line.startswith("#TP: (remaining"):
            if lines[-1] == line:
                break
            # TODO: check this out, we are not returning any info about remaining faults
            print("Fault simulation was not completed for some nodes!")
            break
        words = line.split()
        res[words[0]] = float(words[1])/current_tp

    return res

def load_ppsf_parallel_step_D(circuit, args, confidence):
    path = os.path.join(cfg.FAULT_SIM_DIR, circuit.c_name)
    fname = os.path.join(path, "{}-ppsf-steps-ci{}-cpu{}.ppsf".format(
            circuit.c_name, confidence, args.cpu))
    print("Loading ppsf results file from {} into node.D values".format(fname))
    res_ppsf = utils.load_ppsf_parallel_step(fname)
    for fault, prob in res_ppsf.items():
        if fault[-1] == "1":
            circuit.nodes[fault[:-2]].D1 = prob
        else:
            circuit.nodes[fault[:-2]].D0 = prob

