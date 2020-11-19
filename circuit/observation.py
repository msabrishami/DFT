
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



def deltaHTO(circuit, op, HTO_th=config.HTO_TH, HTC_th=config.HTC_TH):
    """ count the number of nodes that change from HTO to ETO 
    by making node an observation point """ 
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


def circuit_deltaHTO(circuit, B_th=0.1):
    res = {}
    
    for node in circuit.nodes_lev:

        if node.B > B_th:
            continue
        if node.ntype in ["FB", "PI"]:
            continue

        count = deltaHTO(circuit, node)
        res[node.num] = count

    res = {k: v for k,v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
    return res

def make_OP(circuit, op):
    """ adds an observation point, updates STAFAN_B """ 
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()


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


def circuit_deltaP(circuit, B_th=0.1):
    """ measuring the change made in the fan-in cone nodes if made PO 
    Calculates this for all the nodes
    returns a ranked list of nodes based on value of B
    Note: we are not considering branch nodes 
    """
    
    res_arit = {}
    res_geom = {}

    for node in circuit.nodes_lev:

        if node.B > B_th:
            # print(node.num, "SKIPPED")
            continue
        
        if node.ntype == "FB":
            continue
        
        if node.ntype == "PI":
            continue
        # print("\n===============================")
        # print(node.num, round(node.B0, 3), round(node.B1, 3), round(node.B,3))
        a_all, g_all, a_agg, g_agg = deltaP(circuit, node)
        res_arit[node.num] = a_agg
        res_geom[node.num] = g_agg

        # print("Num:{}\Lev:{} is OP! \nArit AGG:\t\t {}\t\tGeom AGG: \t {}".format(
        #     node.num, node.lev, 
        #     [round(x, 3) for x in a_agg], [round(x, 3) for x in g_agg]))

        # printing the impact on all the nodes if node is made OP
        # for idx in range(len(a_all)):
        #     if a_all[idx][2] < 0.001:
        #         continue
        #     print("{} \t{}".format(circuit.nodes_lev[idx].num, 
        #         circuit.nodes_lev[idx].lev), end="")
        #     print("\t\t", [round(x, 3) for x in a_all[idx]], end="\t\t")
        #     print("\t\t", [round(x, 3) for x in g_all[idx]])
    guide = {"B0":0, "B1":1, "B":2, "CB0":3, "CB1":4}
    # print("\n\n=============clean format==============")
    # print("arit: B0,B1,B,CB0,CB1. geom: B0,B1,B,CB0,CB1")
    # for node in circuit.nodes_lev:
    #     if node.num in res_arit:
    #         msg = node.num + ","
    #         msg = msg + ",".join([str(x) for x in res_arit[node.num]]) + "," 
    #         msg = msg + ",".join([str(x) for x in res_geom[node.num]])
    #         print(msg)
    # print("\n\n=============clean format==============\n\n")
    
    _arit = {}
    _geom = {}
    for key in res_arit.keys():
        _arit[key] = res_arit[key][guide["B"]]
        _geom[key] = res_geom[key][guide["B"]]
    arit_ordered = {k: v for k,v in sorted(_arit.items(), key=lambda item: item[1], reverse=True)}
    geom_ordered = {k: v for k,v in sorted(_geom.items(), key=lambda item: item[1], reverse=True)}
    return (arit_ordered, geom_ordered)


def OPI(circuit, alg, count_op=10, B_th=0.2):
    """ runs the observation point insertion, with algorithm alg
    for count_op number of observation points 
    The circuit argument is considered to be fully loaded
    Note: this function modifies the circuit
    returns: a list of OP node numbers"""

    res = [] 
    if alg == "deltaP":
        for x in range(count_op):
            arit, geom = circuit_deltaP(circuit, B_th=B_th)
            if len(arit) == 0:
                print("No more points with B_th={}".format(B_th))
                break
            new_op = circuit.nodes[list(arit)[0]]
            # print(new_op.num, arit[new_op.num])
            res.append(new_op.num)
            make_OP(circuit, new_op)
    elif alg == "deltaHTO":
        for x in range(count_op):
            ops = circuit_deltaHTO(circuit, B_th=B_th)
            if len(ops) == 0:
                print("No more points with B_th={}".format(B_th))
                break
            new_op = circuit.nodes[list(ops)[0]]
            if new_op.num == "N73":
                pdb.set_trace()
            # print(new_op.num, arit[new_op.num])
            res.append(new_op.num)
            make_OP(circuit, new_op)
    else:
        raise NameError("Algorithm not defined")
   
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

