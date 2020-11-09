
import config
import pdb
def TPI_stat(circuit, HTO_th, HTC_th):
    """ this is a simple division of nodes, 
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
    TPI_stat(circuit, HTO_th, HTC_th)
    for node in circuit.nodes_lev:
        node.eval_HTO()

    count = 0 
    for node in circuit.nodes_lev:
        if node.HTO:
            count += 1
    print("Number of HTO nodes are {}".format(count))



def NVIDIA_count(circuit, op, HTO_th, HTC_th):
    """ count the number of nodes that change from HTO to ETO 
    by making node an observation point """ 
    circuit.STAFAN_B()
    TPI_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    HTO_old = set()
    for node in circuit.nodes_lev: 
        if (node.stat["SS@0"] == "HTO") or (node.stat["SS@1"] == "HTO"):
            HTO_old.add(node.num)
    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"
    circuit.STAFAN_B()
    TPI_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
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


def approach_1(circuit, op):
    """ count the number of nodes that change from HTO to ETO 
    by making node an observation point """ 
    circuit.STAFAN_B()
    # TPI_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    stat_arit_all = [] # [[1,1,1]] * len(circuit.nodes_lev)
    stat_geom_all = [] # [[0,0,0]] * len(circuit.nodes_lev)
    stat_arit_agg = [0, 0, 0]
    stat_geom_agg = [0, 0, 0]
    stat_init = []

    for node in circuit.nodes_lev: 
        stat_init.append([node.B0, node.B1, node.B, node.num, node.lev])
        stat_arit_all.append([0, 0, 0])
        stat_geom_all.append([0, 0, 0])
    
    # circuit.co_ob_info()

    orig_ntype = op.ntype
    circuit.PO.append(op)
    op.ntype = "PO"

    circuit.STAFAN_B()

    # circuit.co_ob_info()

    for idx, node in enumerate(circuit.nodes_lev):
        temp = [node.B0, node.B1, node.B]
        for x in range(3):
            # issue of division by 0
            if stat_init[idx][x] == 0 and temp[x]==0:
                continue
            elif stat_init[idx][x] == 0:
                stat_init[idx][x] = config.STAFAN_B_MIN

            stat_arit_all[idx][x] = temp[x]-stat_init[idx][x]
            stat_geom_all[idx][x] = temp[x]/stat_init[idx][x]
            stat_arit_agg[x] += (temp[x] - stat_init[idx][x])
            stat_geom_agg[x] += ((temp[x] / stat_init[idx][x]) - 1)
        # print("info:\t", idx, node.num, temp, stat_arit_all[idx])

    op.ntype = orig_ntype
    circuit.PO = circuit.PO[:-1]

    return stat_arit_all, stat_geom_all, stat_arit_agg, stat_geom_agg


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

