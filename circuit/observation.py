
import config
import pdb
import utils
import numpy as np


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
    # print(res)
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


def deltaFC(circuit, op, tps, ref="STAFAN", verbose=False, cut_bfs=None): 
    """ Calculating the changes in the FC estimation of the nodes
    in the circuit when node OP is used as an observation point. 
    Detection probability is estimated using STAFAN values.
    FC estimation formula is Sum_FL( exp(-D_pre*tp) - exp(-D_post*tp) ). 
    Parameters
    ----------
    circuit : Circuit before adding op
    op : node used for observation point insertion 
    tps : the number of test patterns, it can be a list of tps
    
    Returns
    -------
    float     
    """
    assert ref in ["STAFAN", "PPSF"], "reference should be either STAFAN or PPSF"
    
    circuit.STAFAN_B()
    
    fanin_cone = utils.get_fanin_BFS(circuit, op)
    if cut_bfs:
        fanin_cone = fanin_cone[:cut_bfs]
    
    PDs_init = []
    for node in fanin_cone:
        if ref == "STAFAN":
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



def deltaP(circuit, op, verbose=False, cut_bfs=None): 
    """ Calculating the changes in the sum of detection probability of the nodes
    in the circuit when node OP is used as an observation point 
    Parameters
    ----------
    circuit : Circuit before adding op
    op : Node 
    
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



def OPI(circuit, alg, count_op, args):
    """ runs the observation point insertion, with algorithm alg
    for count_op number of observation points 
    The circuit argument is considered to be fully loaded
    Note: this function modifies the circuit
    returns: a list of OP node numbers"""

    assert alg in ["deltaHTO", "deltaP"],"Algorithm not defined"
 
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


"""
def IMOP_1(circuit, node):
    # Sum of all the observations of the fan-in cone, only if lower than HTO
    # if target becomes OP, how many node pass the threshold
    if node.seen:
        return 0
    delta_B0 = node.B0 / node.stat{"B0_old"}
    delta_B1 = node.B1 / node.stat{"B1_old"}
    elif delta_B0 < 2 and delta_B1 < 2:
        # no significant change
        return 
    for node in circuit.nodes_lev:
        node.seen = False

"""

