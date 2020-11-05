

from circuit import Circuit
from observation import *
import pdb
from random import randint

from c432_logic_sim import c432_sim

def check_c432_logicsim(circuit, total_T=1, mode="ckt"):
    """ ckt and verilog files in all ISCAS valid circuits differ by "N"
    if mode is selected ckt: node numbers are simple integers, no issue
    else if mode is verilog, one "N" will be added to node.num
    """

    for t in range(total_T):
        PI_dict = dict()
        PI_list = []
        
        PI_num = [x.num for x in circuit.PI]
        PI_num = [x[1:] for x in PI_num] if mode=="verilog" else PI_num 
        for pi in PI_num:
            val = randint(0,1)
            PI_dict[pi] = val
            PI_list.append(val)

        res_beh = c432_sim(PI_dict)
        circuit.logic_sim(PI_list)
        res_ckt = circuit.read_PO()
        res_ckt_2 = {}
        if mode == "verilog":
            for k in res_ckt:
                res_ckt_2[k[1:]] = res_ckt[k]
            res_ckt = res_ckt_2
        if res_beh != res_ckt:
            print("Wrong")
            return False
    print("Logicsim matches behavioral simulation for {}, with {} test patterns ".format(
        circuit.c_name, total_T))
    return True


def exp_check_ckt(mode="ckt"):
    circuit = Circuit("c432")
    circuit.read_ckt()
    circuit.lev()
    check_c432_logicsim(circuit, 1000)

def exp_check_verilog():
    circuit = Circuit("c432")
    circuit.read_verilog()
    circuit.lev()
    check_c432_logicsim(circuit, 1000, mode="verilog")



def exp_read_v2():
    circuit = Circuit("adder_syn")
    circuit.read_verilog()
    circuit.lev()
    return 


def exp_1(args):
    
    # circuit = Circuit(args.ckt)
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
