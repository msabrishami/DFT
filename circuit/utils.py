
import pdb
import operator
import numpy as np

from collections import deque
from functools import reduce

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
    
def load_ppsf_parallel(fname):
    """ loads a ppsf_parallel simulated log file 
    the last line is time """ 
    lines = open(fname, "r").readlines()
    res = {}
    for line in lines[:-1]:
        words = line.strip().split(",")
        res[words[0]] = [int(x) for x in words[1:]]
    return res

def load_pd_ppsf_conf(fname):
    #TODO 4 Ghazal: documentation 
    """ loads a ppsf with confidence log file 
    """ 
    lines = open(fname, "r").readlines()
    res = {}
    current_tp = 0
    for line in lines:
        if line.startswith("#TP="):
            current_tp += float(line.split("=")[-1])
            continue
        if line.startswith("#TP: (remaining"):
            if lines[-1] == line:
                break
            print("Warning: PPSF was not completed with enough confidence for some faults")
            break
        words = line.split()
        res[words[0]] = float(words[1])/current_tp
    
    return res

def estimate_FC(probs, tp): 
    #TODO 4 Ghazal : documentation 
    # probs is a dictionary, keys are faults strings, and values are ppsf probs
    """ estimating the fault coverage of a circuit based on all the faults """
    nfc = 0
    for key in probs:
        nfc += np.exp(-probs[key] * tp)

    return 1 - nfc/len(probs)
