

from circuit import Circuit
from observation import *
import pdb



def exp_1(args):
    
    circuit = Circuit(args.ckt)
    circuit.read_verilog()
    # circuit.read_ckt()
    circuit.lev()
    
    
    """ Observation Point Insertion """  
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()
    circuit.STAFAN_CS(args.tp)
    circuit.STAFAN_B()
    circuit.co_ob_info() 


    exp1_res_arit = {}
    exp1_res_geom = {}

    for node in circuit.nodes_lev:
        if node.lev < 5:
            continue

        print("================================")

        if node.B > 0.2:
            print(node.num, "SKIPPED")
            continue

        print(node.num, node.B)
        a_all, g_all, a_tot, g_tot = approach_1(circuit, node)
        # stat_arithmetic = [round(x, 2) for x in stat_arithmetic]
        # stat_geometric = [round(x, 2) for x in stat_geometric]
        print("Node num: {}\tNode Lev: {}\nArithmetic:\t {}\t\tGeometric: \t {}".format(
            node.num, node.lev, 
            [round(x, 3) for x in a_tot], [round(x, 3) for x in g_tot]))
        exp1_res_arit[node.num] = a_tot[2]
        exp1_res_geom[node.num] = g_tot[2]
        for idx in range(len(a_all)):
            if a_all[idx][2] < 0.001:
                continue
            print("{} {}".format(circuit.nodes_lev[idx].num, circuit.nodes_lev[idx].lev), end="")
            print("\t\t", [round(x, 3) for x in a_all[idx]], end="\t\t")
            print("\t\t", [round(x, 3) for x in g_all[idx]])
    TPI_stat(circuit, HTO_th=config.HTO_TH, HTC_th=config.HTC_TH)

    nodes_HTO = []
    for node in circuit.nodes_lev:
        if (node.stat["SS@1"]=="HTO") or (node.stat["SS@1"]=="HTO"):
            nodes_HTO.append(node)
    print("Initial HTO count: {}".format(len(nodes_HTO)))

    for target in nodes_HTO: 
        print("Target: {}\tB1={:.2f} B2={:.2f} \tdelta={}".format(
            target.num, target.B1, target.B0, 
            NVIDIA_count(circuit, target, 0.05, 0.05)))
    
    return (exp1_res_arit, exp1_res_geom)
