

from circuit import Circuit
from observation import *
import pdb
from random import randint

from c432_logic_sim import c432_sim
from load_circuit import LoadCircuit

def check_c432_logicsim(circuit, tp=1, mode="ckt"):
    """ ckt and verilog files in all ISCAS valid circuits differ by "N"
    if mode is selected ckt: node numbers are simple integers, no issue
    else if mode is verilog, one "N" will be added to node.num
    """

    for t in range(tp):
        PI_dict = dict()
        PI_list = []

        
        PI_num = [x.num for x in circuit.PI]
        PI_num = [x[1:] for x in PI_num] if mode=="v" else PI_num 
        for pi in PI_num:
            val = randint(0,1)
            PI_dict[pi] = val
            PI_list.append(val)

        res_beh = c432_sim(PI_dict)
        circuit.logic_sim(PI_list)
        res_ckt = circuit.read_PO()
        res_ckt_2 = {}
        if mode == "v":
            for k in res_ckt:
                res_ckt_2[k[1:]] = res_ckt[k]
            res_ckt = res_ckt_2
        if res_beh != res_ckt:
            print("Logicsim does NOT match behavioral simulation" +
                    "for {}, with {} test patterns ".format(circuit.c_name, tp))
            return False
    print("Logicsim matches behavioral simulation for {}, with {} test patterns ".format(
        circuit.c_name, tp))
    return True




def exp_check_verilog_modelsim():
    for ckt in ["c17", "c432", "c499", "c880", "c1908"]:
        print("\nCircuit: " + ckt)
        circuit = Circuit(ckt)
        LoadCircuit(circuit, "v")
        circuit.lev()
        path = "../data/modelsim/golden_IO_from_verilog/golden_" + ckt + "_10_b.txt"
        circuit.golden_test(path)


def exp_check_c432_behavioral(mode="ckt", tp=100, ):
    if mode not in ["ckt", "v"]:
        raise NameError("mode {} is not accepted".format(mode))
    print("Checking c432 behavioral golden with c432 in {} format".format(mode))
    circuit = Circuit("c432")
    LoadCircuit(circuit, mode)
    circuit.lev()
    check_c432_logicsim(circuit, tp, mode)


def exp_read_v2():
    circuit = Circuit("adder_syn")
    circuit.read_verilog()
    circuit.lev()
    return 


def exp_1(args):
    """ measuring the change made in the fan-in cone nodes if made PO """
    
    circuit = Circuit(args.ckt)
    LoadCircuit(circuit, "v")
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
        if node.lev < 4:
            continue

        print("================================")

        if node.B > 0.2:
            print(node.num, "SKIPPED")
            continue

        print(node.num, round(node.B,3))
        a_all, g_all, a_agg, g_agg = approach_1(circuit, node)

        exp1_res_arit[node.num] = a_agg
        exp1_res_geom[node.num] = g_agg
        print("Node num:  {}\tNode Lev: {} is now OP! \nArithmetic AGG:\t\t {}\t\tGeometric AGG: \t {}".format(
            node.num, node.lev, 
            [round(x, 3) for x in a_agg], [round(x, 3) for x in g_agg]))

        # exp1_res_arit[node.num] = a_agg[2]
        # exp1_res_geom[node.num] = g_agg[2]
        for idx in range(len(a_all)):
            if a_all[idx][2] < 0.001:
                continue
            print("{} \t{}".format(circuit.nodes_lev[idx].num, 
                circuit.nodes_lev[idx].lev), end="")
            print("\t\t", [round(x, 3) for x in a_all[idx]], end="\t\t")
            print("\t\t", [round(x, 3) for x in g_all[idx]])
    
    print("\n\n=============clean format==============\n\n")
    for node in circuit.nodes_lev:
        if node.num in exp1_res_arit:
            print(node.num, exp1_res_arit[node.num], exp1_res_geom[node.num])
    print("\n\n=============clean format==============\n\n")

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
