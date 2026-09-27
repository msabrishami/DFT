"""Test point insertion helpers that used to be methods of DFTCircuit.

They are kept for the revival of test point insertion (see ROADMAP). ``circuit``
is a DFTCircuit with STAFAN measures. Not tested; ``calc_tpi`` writes to a
hard-coded relative directory and ``nvidia_count`` modifies the circuit temporarily.
"""
import math
import os


##### Entropy / OR not called anywhere

def calc_entropy(circuit):
    for node in circuit.nodes_lev:
        node.Entropy = -((node.C1*math.log(node.C1, 2.0)) + 
                (node.C0*math.log(node.C0, 2.0)))

def calc_tpi(circuit, num_TPI, fname):
    TPI_list = [] #list of node entropy 
    for node in circuit.nodes_lev:
        node_list = [node.num, node.Entropy]
        if '-' not in node.num:
            TPI_list.append(node_list)
        #print(TPI_list)
    TPI_list.sort(key = lambda x: x[1])
    print(TPI_list)
    TPI_list = TPI_list[:num_TPI]
    print(TPI_list)

    if not os.path.exists('../data/stafan-data'):
        os.makedirs('../data/stafan-data')
    outfile = open(fname, "w")
    for item in TPI_list: 
        outfile.write(item[0] + "\n")
    outfile.close()

def tpi_stat(circuit, HTO_th, HTC_th):
    """ Categorization of nodes based on STAFAN's measurement into 4 groups:
    ETD: easy to detect 
    HTC: hard to control, but easy to observe 
    HTO: hard to observe, but easy to control 
    HTD: hard to control, hard to observe
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

def nvidia_count(circuit, op, HTO_th, HTC_th):
    """ count the number of nodes that change from HTO to ETO 
    by making node an observation point """ 
    circuit.stafan_b()
    tpi_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    HTO_old = set()
    for node in circuit.nodes_lev: 
        if (node.stat["SS@0"] == "HTO") or (node.stat["SS@1"] == "HTO"):
            HTO_old.add(node.num)
    orig_ntype = op.ntype
    circuit.outputs.append(op)
    op.ntype = "PO"
    circuit.stafan_b()
    tpi_stat(circuit, HTO_th=HTO_th, HTC_th=HTC_th)
    HTO_new = set()
    count = 0
    for node in circuit.nodes_lev:
        if node.num in HTO_old:
            if (node.stat["SS@0"] != "HTO") and (node.stat["SS@1"] != "HTO"):
                # print("\t{} was HTO, but now became ETO".format(node.num))
                count = count + 1
    op.ntype = orig_ntype
    circuit.outputs = circuit.outputs[:-1]
    return count

