
import config
import pdb


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

def make_OP(circuit, op):
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


def deltaP(circuit, op):
    """ count the number of nodes that change from HTO to ETO when op is made observation point 
    returns:
    aggregated amount of change op's fan-in cone, arithmetic and geometeric
    all amounts of change in the op's fan-in cone
    """
    circuit.STAFAN_B()
    # fault_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    stat_arit_all = [] # [[1,1,1]] * len(circuit.nodes_lev)
    stat_geom_all = [] # [[0,0,0]] * len(circuit.nodes_lev)
    stat_arit_agg = [0, 0, 0, 0, 0]
    stat_geom_agg = [0, 0, 0, 0, 0]
    stat_init = []

    for node in circuit.nodes_lev: 
        stat_init.append([node.B0, node.B1, node.B, node.CB0, node.CB1, node.num, node.lev])
        stat_arit_all.append([0, 0, 0, 0, 0])
        stat_geom_all.append([0, 0, 0, 0, 0])
    
    # Make op as observation point, add it to circuit outputs, run STAFAN again
    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()

    for idx, node in enumerate(circuit.nodes_lev):
        changed = [node.B0, node.B1, node.B, node.CB0, node.CB1]
        for x in range(5):
            
            # if no change was made, and still node observation is zero! 
            if stat_init[idx][x] == 0 and changed[x]==0:
                # Both arithmetic and geometric are not changed 
                continue
            # if it changed, but initial value was zero
            elif stat_init[idx][x] == 0:
                stat_init[idx][x] = config.STAFAN_B_MIN

            stat_arit_all[idx][x] = changed[x] - stat_init[idx][x]
            stat_geom_all[idx][x] = (changed[x] / stat_init[idx][x]) - 1
            stat_arit_agg[x] += (changed[x] - stat_init[idx][x])
            stat_geom_agg[x] += ((changed[x] / stat_init[idx][x]) - 1)
        # print("info:\t", idx, node.num, temp, stat_arit_all[idx])

    op.ntype = orig_ntype
    circuit.PO = circuit.PO[:-1]

    return stat_arit_all, stat_geom_all, stat_arit_agg, stat_geom_agg


def circuit_deltaP(circuit, B_th=0.1, ops=None):
    """ measuring the change made in the fan-in cone nodes if made PO 
    Calculates this for all the nodes
    returns a ranked list of nodes based on value of B
    Note: we are not considering branch nodes 
    """
    
    res_arit = {}
    res_geom = {}

    for op in ops:
        node = circuit.nodes[op]

        if (node.B > B_th) or (node.ntype in ["FB", "PI"]):
            continue
        
        a_all, g_all, a_agg, g_agg = deltaP(circuit, node)
        res_arit[node.num] = a_agg
        res_geom[node.num] = g_agg
    
    guide = {"B0":0, "B1":1, "B":2, "CB0":3, "CB1":4}

    _arit = {}
    _geom = {}
    for key in res_arit.keys():
        _arit[key] = res_arit[key][guide["B"]]
        _geom[key] = res_geom[key][guide["B"]]
    arit_sort = {k: v for k,v in sorted(_arit.items(), key=lambda item: item[1], reverse=True)}
    # geom_sort = {k: v for k,v in sorted(_geom.items(), key=lambda item: item[1], reverse=True)}

    return arit_sort


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

