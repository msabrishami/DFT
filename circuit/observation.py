
import config
import pdb
import os
import numpy as np
import pandas as pd

import utils
import experiments as exp

from FaultSimulation.pfs import PFS
from FaultSimulation.fault import FaultList

def fault_stat(circuit, HTO_th, HTC_th):
    """ categorizes all the nodes in the circuit based on obs and ctrl
    this is a simple division of nodes, 
    the element C*B can also be used. 
    """
    for node in circuit.nodes_lev:
        if (node.B0 >= HTO_th) and (node.C0 >= HTC_th):
            node.stat["SS@1"] = "ETD"
        elif (node.B0 >= HTO_th) and (node.C0 < HTC_th):
            node.stat["SS@1"] = "HTC"
        elif (node.B0 < HTO_th) and (node.C0 >= HTC_th):
            node.stat["SS@1"] = "HTO"
        else: 
            node.stat["SS@1"] = "HTD"

        if (node.B1 >= HTO_th) and (node.C1 >= HTC_th):
            node.stat["SS@0"] = "ETD"
        elif (node.B1 >= HTO_th) and (node.C1 < HTC_th):
            node.stat["SS@0"] = "HTC"
        elif (node.B1 < HTO_th) and (node.C1 >= HTC_th):
            node.stat["SS@0"] = "HTO"
        else:
            node.stat["SS@0"] = "HTD"

def stat_HTO(circuit, HTO_th, HTC_th):
    fault_stat(circuit, HTO_th, HTC_th)
    for node in circuit.nodes_lev:
        node.eval_HTO()

    count = 0 
    for node in circuit.nodes_lev:
        if node.HTO:
            count += 1
    print("Number of HTO nodes are {}".format(count))
    return count

def make_OP_deprecated(circuit, op):
    """ adds an observation point, updates STAFAN_B """ 
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()

def deltaHTO(circuit, op, HTO_th, HTC_th):
    """ count the number of nodes that change from HTO to ETO 
    by making node an observation point """ 
    #TODO: does not look at the fan-in cone, but all the circuit

    circuit.STAFAN_B()
    fault_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    HTO_old = set()
    for node in circuit.nodes_lev: 
        if (node.stat["SS@0"] == "HTO") or (node.stat["SS@1"] == "HTO"):
            HTO_old.add(node.num)
    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()
    fault_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    HTO_new = set()
    count = 0
    for node in circuit.nodes_lev:
        if node.num in HTO_old:
            if (node.stat["SS@0"] != "HTO") and (node.stat["SS@1"] != "HTO"):
                # print("\t{} was HTO, but now became ETO".format(node.num))
                count = count + 1
    op.ntype = orig_ntype
    circuit.PO = circuit.PO[:-1]
    return count

def circuit_deltaHTO(circuit, B_th, ops, args):
    res = {}
    
    for op in ops:
        node = circuit.nodes[op]

        if (node.B > B_th) or (node.ntype in ["FB", "PI"]):
            continue

        count = deltaHTO(circuit, node, args.HTO_th, args.HTC_th)
        res[node.num] = count

    res = {k: v for k,v in sorted(res.items(), key=lambda item: item[1], reverse=True)}

    return res

def deltaP_2(circuit, op, verbose=False):
    """ 
    TODO: what was this one again?! 
    returns:
    aggregated amount of change op's fan-in cone, arithmetic and geometeric
    all amounts of change in the op's fan-in cone
    """
    circuit.STAFAN_B()
    
    p_pre = []
    p_post = []
    for node in circuit.nodes_lev: 
        p_pre.append([node.B0 * node.C0, node.B1 * node.C1])
    
    # Make op as observation point, add it to circuit outputs, run STAFAN again
    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()

    if verbose: print("node\tlevel\td-CB0\td-CB1")
    for idx, node in enumerate(circuit.nodes_lev):
        p_post.append([node.C0 * node.B0, node.C1 * node.B1])
        if verbose:
            if (p_post[idx][0] != p_pre[idx][0] or p_post[idx][1] != p_pre[idx][1]):
                print("{}\t{}\t{:.4f}\t{:.4f}".format(node.num, node.lev,
                    p_post[idx][0] - p_pre[idx][0], p_post[idx][1] - p_pre[idx][1]))
    
    deltaP_tot= 0 
    for idx in range(len(p_post)):
        deltaP_tot += (p_post[idx][0]-p_pre[idx][0])
        deltaP_tot += (p_post[idx][1]-p_pre[idx][1])

    op.ntype = orig_ntype
    circuit.PO = circuit.PO[:-1]
    circuit.STAFAN_B()

    return deltaP_tot

def deltaFC(circuit, op, tps, depth=False, verbose=False): 
    """ Calculating the changes in the FC estimation of the nodes
    in the circuit when node OP is used as an observation point. 
    Detection probability is estimated using STAFAN values.
    FC estimation formula is Sum_FL( exp(-D_pre*tp) - exp(-D_post*tp) ). 

    Parameters
    ----------
    circuit : Circuit before adding op
    op : Node
        Node used for observation point insertion 
    tps : int 
        The number of test patterns, it can be a list of tps
    verbose : boolean
        (default is False)
    cur_bfs : int
        Set limit for BFS depth (default is None)

    Returns
    -------
    float
        The change in fault coverage
    """
    
    circuit.STAFAN_B()
    fanin_cone = utils.get_fanin_BFS(circuit, op, depth)
    
    PDs_init = []
    for node in fanin_cone:
        PDs_init.append(node.C0 * node.B0)
        PDs_init.append(node.C1 * node.B1)

    # temporary adding op as a primary output and redoing STAFAN_B
    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()
    PDs_new = []

    for node in fanin_cone:
        PDs_new.append(node.C0 * node.B0)
        PDs_new.append(node.C1 * node.B1)

    if isinstance(tps, int):
        deltaFC = 0
        for idx in range(len(PDs_new)):
            deltaFC += (np.exp(-PDs_init[idx]*tps) - np.exp(-PDs_new[idx]*tps))
    
    elif isinstance(tps, list):
        deltaFCs = []
        for tp in tps:
            deltaFC = 0
            for idx in range(len(PDs_new)):
                deltaFC += (np.exp(-PDs_init[idx]*tp) - np.exp(-PDs_new[idx]*tp))
            deltaFCs.append(deltaFC)
        deltaFC = deltaFCs

    op.ntype = orig_ntype
    circuit.PO = circuit.PO[:-1]
    return deltaFC

def deltaFC_PPSF(circuit, op, p_init, TPs, args, steps, log=True):
    """ Add op node to the primary output list and run ppsf for the \
    fan-in cone nodes. The op is removed from primary output list at the end.

    Parameters
    ----------
    circuit : Circuit before adding op
    op : Node 
        Primary output node
    TPs : list
        A list of test pattern counts
    args : args
        Command-line arguments
    steps : list
        Lengths of tps in each ppsf run
    log : boolean
        If True, saves the log of ppsf

    Returns
    -------
    dict
        A dictionary in the following format: {"deltaP": float, "deltaFC": float}
    """
    orig_ntype = op.ntype
    if op:
        circuit.PO.append(op)
        op.ntype = "PO"
    p_op = exp.pd_ppsf(circuit, args, op=op, 
            steps=steps, log=log)
    _deltaFC = [0] * len(TPs)
    _deltaP = 0 
    for key in p_op.keys():
        _deltaP += p_op[key] - p_init[key]
        for idx, tp in enumerate(TPs):
            _deltaFC[idx] +=  ( np.exp(-p_init[key]*tp) - np.exp(-p_op[key]*tp) ) 
    
    if op:
        op.ntype = orig_ntype
        circuit.PO = circuit.PO[:-1]

    return {"deltaP":_deltaP, "deltaFC":_deltaFC}


def deltaFC_PFS(circuit, op, tp_count, times, depth=None, log=True):
    """ Add op node to the primary output list and run PFS for the \
    fan-in cone nodes. The op is removed from primary output list at the end.
    This procedure is executed several times (times) with different test patterns.

    Parameters
    ----------
    circuit : Circuit before adding op
    op : Node 
        Primary output node
    tp_count : int 
        test pattern counts
    times : int 
        the number of times to run PFS
    depth : int
        the depth of search for doing PFS
    args : args
        Command-line arguments
    log : boolean
        If True, saves the log of ppsf

    Returns
    ------
    list 
        DataFrame with columns [time, tp, delta_FC]
    """
    if op is None:
        raise ValueError("OP is None")
    fanin_nodes = utils.get_fanin_BFS(circuit, op, depth)
    delta_fcs = pd.DataFrame(columns=["time","tp","delta_FC","OP_Node"])

    for time in range(times):
        tps = circuit.gen_multiple_tp(tp_count)
        for tp in tps:
            init_pfs = PFS(circuit)
            init_pfs.fault_list.add_nodes(fanin_nodes)
        init_fc = init_pfs.tpfc(tps, fault_drop=1, verbose=False)

        circuit.PO.append(op)
        orig_ntype = op.ntype
        op.ntype = "PO"

        op_pfs = PFS(circuit)
        op_pfs.fault_list.add_nodes(fanin_nodes)
        op_fc = op_pfs.tpfc(tps, fault_drop=1, verbose=False)
        for t in range(tp):
            row = {"time":time, "tp":t, "delta_FC":op_fc[t]-init_fc[t], "OP_Node":op.num}
            delta_fcs = delta_fcs.append(row, ignore_index=True)

        op.ntype = orig_ntype
        circuit.PO = circuit.PO[:-1]     
        
    delta_fcs["time"] = delta_fcs["time"].astype(int)
    delta_fcs["tp"] = delta_fcs["tp"].astype(int)

    return delta_fcs


def deltaP(circuit, op, verbose=False, cut_bfs=None): 
    """ Calculating the changes in the sum of detection probability of the nodes
    in the circuit when node OP is used as an observation point 

    Parameters
    ----------
    circuit : Circuit 
        The circuit before adding op
    op : Node 
        Node used for observation point insertion 
    verbose : boolean
        (default is False)
    cur_bfs : int
        Set limit for BFS depth (default is None)
    
    Returns
    -------
    float     
    """
    circuit.STAFAN_B()
    fanin_cone = utils.get_fanin_BFS(circuit, op)
    if cut_bfs:
        fanin_cone = fanin_cone[:cut_bfs]
    PDs_init = []
    # PDs_init = {} 
    for node in fanin_cone:
        PDs_init.append(node.C0 * node.B0)
        PDs_init.append(node.C1 * node.B1)
    
    # temporary adding op as a primary output and redoing STAFAN_B
    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()
    PDs_new = []
    for node in fanin_cone:
        PDs_new.append(node.C0 * node.B0)
        PDs_new.append(node.C1 * node.B1)

    delta_PDs = [PDs_new[i] - PDs_init[i] for i in range(len(PDs_new))] 
    
    op.ntype = orig_ntype
    circuit.PO = circuit.PO[:-1]
    return delta_PDs

def OPI_old(circuit, alg, count_op, args):
    """ runs the observation point insertion, with algorithm alg
    for count_op number of observation points 
    The circuit argument is considered to be fully loaded
    Note: this function modifies the circuit
    returns: a list of OP node numbers"""

    assert alg in ["deltaHTO", "deltaP"], "Algorithm not defined"
 
    res = []
    ops = list(circuit.nodes.keys())

    for x in range(count_op):
        print("Candidates: {}".format(len(ops)))

        if alg == "deltaP":
            ops = circuit_deltaP(circuit, B_th=args.Bth, ops=ops)
        elif alg == "deltaHTO":
            ops = circuit_deltaHTO(circuit, B_th=args.Bth, ops=ops, args=args)

        if len(ops) == 0:
            print("Reached B_th={} limit".format(args.Bth))
            break
        new_op = circuit.nodes[list(ops)[0]]
        res.append(new_op.num)
        make_OP(circuit, new_op)
  
    return res