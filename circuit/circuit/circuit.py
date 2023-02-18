# -*- coding: utf-8 -*-

import math
import re
import os 
import random
import time
import sys
import pdb

from enum import Enum
from multiprocessing import Process, Pipe

import utils
import config
from circuit.circuit_loader import CircuitLoader
from node import node

#TODO: one issue with ckt (2670 as example) is that some nodes are both PI and PO
#TODO: we need a flag to make sure no new nodes are added to the circuit, 
#   ... for example, if we find all cell types in one method, later we should 
#   ... read this flag to make sure what this method found is valid now, 
#   ... and no new cell added that is not tracked. 
#TODO: in DFT package gates are logical, NAND can have several inputs, but 
#   ... for SSTA we have cell SSTA delay for NAND2 and NAND3, fix this!
# distributions added to the repo temporarily 
# sys.path.insert(1, "/home/msabrishami/workspace/StatisticsSTA/")



"""
# Tasks for the DFT team:
- Don't change my alreay written methods, if u need to change it let me know. 
- What is the data structure of Node
- Understand the flow of this current code, how we read ckt, 
- How are doing the logic-simulation 
- Adding a new py file, for testbench generation class (maybe call it ModelSim_Simulator
- Add the read_verilog file
- ADd the methods you have for creating a random test pattern file 
- Check if we read a circuit using read_verilog, the current logicsim works fine
"""


class Circuit():
    """ Representing a digital logic circuit, capable of doing logic simulation, 
        test related operations such as fault simulation, ATPG, OPI, testability 
        measurements, SSTA, etc. 

        Attributes
        ---------
        STD_NODE_LIB : dict
            dictionary of node type to related node class
        c_fname : str
            circuit name, full with path and format
        c_name : str
            circuit name, without path or format
        nodes : list
            list of nodes objects
        input_num_list : list
            list of PI node numbers
        nodes_cnt : 
            total number of nodes in the circuit
        nodes_lev : 
            circuit information after levelization,
            each node has level info, previous nodelist_order
        fault_name : 
            full fault list in string format
        fault_node_num : 
            node numbers in full fault list
        """
    
    STD_NODE_LIB = {'AND':node.AND, 
                    'XOR':node.XOR,
                    'OR': node.OR, 
                    'XNOR':node.XNOR,
                    'BUFF':node.BUFF,
                    'BRCH':node.BRCH,
                    'NOR':node.NOR,
                    'NOT':node.NOT,
                    'NAND':node.NAND,
                    'IPT':node.IPT}

    def __init__(self, netlist_fname, std_node_lib=STD_NODE_LIB):
        """ 
        Parameters
        ----------
        c_fname : str
            the name of the circuit with path and format
        c_name : str
            the full name of the circuit without path and format 
        """

        self.c_fname = netlist_fname 
        self.c_name = netlist_fname.split('/')[-1].split('.')[0]
        self.nodes = {}     # dict of all nodes, key is now string node-num
        self.nodes_lev = [] # list of all nodes, ordered by level
        self.PI = [] # this should repalce input_num_list
        self.PO = [] # this should be created to have a list of outputs
        self._load(netlist_fname, std_node_lib)
    
    def _load(self, netlist_fname, std_node_lib):
        CircuitLoader(self, netlist_fname, std_node_lib)

    def lev(self): # --> levelize(self) / if it must be call all the times, put it in the __init__
        """
        Levelization, assigns a level to each node
        Branches are also considered as gates: lev(branch) = lev(stem) + 1 
        Algorithm is not efficient at all, don't care now
        """
        for ptr in self.PI:
            ptr.lev = 0

        flag_change = True
        while flag_change: 
            flag_change = False
            for num, node in self.nodes.items():
                if node.lev == None: # not levelized yet
                    lev_u = [x.lev for x in node.unodes]
                    if None in lev_u:
                        continue
                    elif lev_u == []:
                        print(f"Warning! Node {node.num} has zero fanins")
                        print(node)
                        print("level of this node is set to zero")
                        node.lev = 0
                    else:
                        node.lev = max(lev_u) + 1
                        flag_change = True
    
        self.nodes_lev = sorted(list(self.nodes.values()), key=lambda x:x.lev)

    def lev_backward(self):
        """ Calculate shortest distace from node to POs for all nodes
            using Dijktra algorithm """
        dist = {} 
        MAX_WEIGHT = 10**9
        nodes = list(self.nodes.values()) + self.PO + self.PI

        for node in nodes:
            dist[node] = MAX_WEIGHT
            
        unvisited_nodes = []
        for po in self.PO:
            dist[po] = min(0,dist[po])
            unvisited_nodes.append(po)
            
        while unvisited_nodes:
            for node in unvisited_nodes:
                for unode in node.unodes:
                    dist[unode] = min(1+dist[node],dist[unode])
                    unvisited_nodes.append(unode)
                unvisited_nodes.remove(node)

    def __str__(self):
        res = ["Circuit name: " + self.c_name]
        res.append("#Nodes: " + str(len(self.nodes)))
        res.append("#PI: " + str(len(self.PI)) + " >> ") 
        res.append("\t" + str([x.num for x in self.PI]))
        res.append("#PO: " + str(len(self.PO)) + " >> ")
        res.append("\t" + str([x.num for x in self.PO]))

        for node in self.nodes_lev:
            res.append(str(node))
        return "\n".join(res)

    def get_rand_nodes(self, count=1):
        if count > len(self.nodes):
            print("Error: count should be less than count of total nodes")
            return None
        res = set() 
        while len(res) < count:
            idx = random.randint(0, len(self.nodes)-1)
            res.add(self.nodes_lev[idx])
        return list(res)[0] if count==1 else res  # better to return a list all the time
    
    def print_fanin(self, target_node, depth):
        # TODO: needs to be checked and tested -- maybe using utils.get_fanin?
        from collections import deque
        queue = deque()
        queue.append(target_node)
        min_level = max(0, target_node.lev - depth) 
        self.print_fanin_rec(queue, min_level)

    def print_fanin_rec(self, queue, min_level):
        # TODO: needs to be checked and tested -- maybe using utils.get_fanin?
        """ prints the nodes in the fanin cone 
        first time it is called, queue should be a list with target node as its only element
        this is a simple BFS in the opposite direction of lines
        
        Arguments:
        ----------
        queue : list
            a list of nodes, representing our queue for BFS
        depth : int 
            search depth for BFS, final node to be printed has depth=zero
        """
        print("queue is: " + ",".join([node.num for node in queue]))
        if len(queue) == 0:
            return 
        
        target_node = queue.popleft()
        print(target_node)
        
        if target_node.lev == min_level:
            return 
        
        for node in target_node.unodes:
            print(f"added node {node.num} to the queue")
            queue.append(node)
            
        self.print_fanin_rec(queue, min_level)

    def gen_single_tp(self, mode="b"):
        """ Generate a random input pattern.
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a single input pattern
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")

        bits = ["0","1","X"]
        if mode == "b":
            tp = [int(bits[random.randint(0,1)]) for _ in range(len(self.PI))]
        elif mode == "x":
            tp = [bits[random.randint(0,2)] for _ in range(len(self.PI))]
        
        return tp 
    
    def gen_multiple_tp(self, tp_count, mode="b"):
        """ Generate multiple random input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a list of random test patterns
        does not store the generated tps in file 
        """

        tps = [self.gen_single_tp(mode) for _ in range(int(tp_count))]

        return tps

    def gen_tp_file(self, tp_count, tp_fname=None, mode="b", verbose=False):
        """ Create single file with multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a list of random test patterns
        mention the sequence of inputs and tps
        """ 
        fn = os.path.join(config.PATTERN_DIR, 
                self.c_name + "_" + str(tp_count) + "_tp_" + mode + ".tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.PI]) + "\n")
        tps = self.gen_multiple_tp(tp_count=tp_count,mode=mode)
        for tp in tps:
            tp_str = [str(val) for val in tp]
            outfile.write(",".join(tp_str) + "\n")
        
        outfile.close()
        if verbose:
            print(f"Generated {tp_count} test patterns and saved in {tp_fname}")

        return tps # better to return the file name

    def gen_full_tp(self):
        """
        Return all possible test patterns
        #TODO: should we implement all with mode = x?
        """ 
        tps = []
        for t in range(2**len(self.PI)):
            tp = list(map(int, bin(t)[2:].zfill(len(self.PI))))
            tps.append(tp)
        
        return tps

    def gen_tp_file_full(self, tp_fname=None):
        """Create a single file including all possible test patterns""" 
        if len(self.PI) > 12:
            print("Error: cannot generate full tp file for circuits with PI > 12")
            return []
        fn = os.path.join(config.PATTERN_DIR, self.c_name + "_tp_full.tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.PI]) + "\n")
        tps = self.gen_full_tp()
        for t in tps:
            outfile.write(",".join(str(t)) + "\n")
        outfile.close()
        print(f"Generated full test patterns and saved in {tp_fname}")
        
        return tps # better to return the file name
    
    def load_tp_file(self, fname, tp_count = 0):
        """ Load single file with multiple test pattern vectors. 
            Does not warn if the size of input nodes is less than each test pattern""" 
        # do we need to check the order of the inputs in the file?  
        # this can be done using "yield" or "generate" -- check online 

        if not os.path.exists(fname):
            raise 'Test file does not exist. Use gen_tp_file() or gen_full_tp_file() instead'
            # return self.gen_tp_file(tp_count=tp_count,tp_fname=fname)
        
        infile = open(fname, 'r')
        tps = []
        lines = infile.readlines()

        for line in lines[1:]:
            words = line.rstrip().split(',')
            words = [int(word) if word == '1' or word == '0' else 'X' for word in words]
            # Not the best practice to have a list with multiple types of elements
            tps.append(words)
        infile.close()
        return tps

    def read_PO(self):
        """ Read the values of POs in a dictionary.
        The key to the dictionary is the PO node and value is the value of node
        """ 
        #TODO: remove out from the output 
        res = {}
        for node in self.PO:
            res["out" + str(node.num)] = node.value
        return res

    def logic_sim(self, tp):
        """
        Logic simulation:
        Read a given pattern and perform the logic simulation
        Currently just works with binary logic
        tp is a list of values (currently int) in the ... 
            ... same order as in self.PI
        """
        node_dict = dict(zip([x.num for x in self.PI], tp))

        for node in self.nodes_lev:
            if node.gtype == "IPT":
                node.imply(node_dict[node.num])
            else:
                node.imply()

    def logic_sim_bitwise(self, tp, fault=None):
        """
        Logic simulation bitwise mode:
        Reads a given pattern and perform the logic simulation bitwise

        Arguments
        ---------
        tp : list of int 
            input pattern in the same order as in self.PI
        fault : str
            node.num@fault --> example: N43@0 means node N43 single stuck at zero 

        fault
        """
        node_dict = dict(zip([x.num for x in self.PI], tp))
        # TODO: get rid of this! Why did we not implement this within constructor?
        n = sys.maxsize
        bitlen = math.log2(n)+1

        bitwise_not = 2**bitlen-1
        
        if fault:
            for node in self.nodes_lev:
                if node.gtype == "IPT":
                    node.imply_b(node_dict[node.num])
                else:
                    node.imply_b()
                if node.num == fault.node_num:
                    if fault.stuck_val == '0':
                        node.value = 0
                    else:
                        node.value = node.bitwise_not

        else:
            for node in self.nodes_lev:
                if node.gtype == "IPT":
                    node.imply_b(node_dict[node.num])
                else:
                    node.imply_b()

    def logic_sim_file(self, in_fname, out_fname, stil=False): 
        """
        logic simulation with given input vectors from a file
        - generate an output folder in ../data/modelsim/circuit_name/ directory
        - read an input file in the input folder
        - generate a output file in output folder by using logic_sim() function
        """
        # Saeed needs to rewrite this method using 'yield' in load_tp_file     
        fr = open(in_fname, mode='r')
        fw = open(out_fname, mode='w')
        fw.write('Inputs: ')
        fw.write(",".join(['N'+str(node.num) for node in self.PI]) + "\n")
        fw.write('Outputs: ')
        fw.write(",".join(['N'+str(node.num) for node in self.PO]) + "\n")
        temp = fr.readline()
        i=1
        for line in fr.readlines():
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            self.logic_sim(line_split)
            fw.write('Test # = '+str(i)+'\n')
            fw.write(line+'\n')
            fw.write(",".join([str(node.value) for node in self.PO]) + "\n")
            i+=1
        fw.close()
        fr.close()
        
        if stil:
            infile = open(in_fname, "r")
            lines = infile.readlines()
            outfile = open(out_fname, "w")
            outfile.write("PI:")
            outfile.write(",".join([node.num for node in self.PI]) + "\n")
            outfile.write("PO:")
            outfile.write(",".join([node.num for node in self.PO]) + "\n")
            for idx, line in enumerate(lines[1:]):
                tp=line.rstrip('\n').split(",")
                # for x in range(len(line_split)):
                #    line_split[x]=int(line_split[x])
                # self.logic_sim(line_split)
                self.logic_sim(tp)
                outfile.write("\"pattern " + str(idx) + "\": Call \"capture\" {\n")
                outfile.write("\"_pi\"=")
                outfile.write("".join(line.strip().split(",")))
                outfile.write(";\n")
                outfile.write("      \"_po\"=")
                for node in self.PO:
                    val = "H" if node.value==1 else "L"
                    outfile.write(val)
                outfile.write("; } \n")
            outfile.close()

    def golden_test(self, golden_io_filename):
        # compares the results of logic-sim of this circuit, 
        #  ... provided a golden input/output file
        # Saeed: this needs to be tested by myself later
        infile = open(golden_io_filename, "r")
        lines = infile.readlines()
        PI_t_order  = [x[1:] for x in lines[0][8:].strip().split(',')]
        PO_t_order = [x[1:] for x in lines[1][8:].strip().split(',')]
        print(PI_t_order)
        PI_num = [x.num for x in self.PI]
        print(PI_num)
        print(f"Logic-Sim validation with {int((len(lines)-2)/3)} patterns")
        if PI_t_order != PI_num:
            print("Error: PI node order does not match! ")
            return False
        for t in range(int((len(lines)-2)/3)):
            test_in  = [int(x) for x in lines[(t+1)*3].strip().split(',')]
            test_out = [int(x) for x in lines[(t+1)*3+1].strip().split(',')]
            self.logic_sim(test_in)
            logic_out = self.read_PO()
            for i in range(len(PO_t_order)):
                out_node = PO_t_order[i]
                out_node_golden = test_out[i]
                if out_node_golden != logic_out["out"+str(out_node)]:
                    print("Error: PO node order does not match! ")
                    return False
        print("Validation completed successfully - all correct")
        return True
    
    def CALC_ENTROPY(self):
        for node in self.nodes_lev:
            node.Entropy = -((node.C1*math.log(node.C1, 2.0)) + 
                    (node.C0*math.log(node.C0, 2.0)))

    def co_ob_info(self):
        print("\t".join(self.nodes_lev[0].print_info(get_labels=True)))
        for node in self.nodes_lev:
            node.print_info(print_labels=False)


    def CALC_TPI(self, num_TPI, fname):
        TPI_list = [] #list of node entropy 
        for node in self.nodes_lev:
            node_list = [node.num, node.Entropy]
            if not '-' in node.num:
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

    def TPI_stat(self, HTO_th, HTC_th):
        """ Categorization of nodes based on STAFAN's measurement into 4 groups:
        ETD: easy to detect 
        HTC: hard to control, but easy to observe 
        HTO: hard to observe, but easy to control 
        HTD: hard to control, hard to observe
        """
        for node in self.nodes_lev:
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
    
    def NVIDIA_count(self, op, HTO_th, HTC_th):
        """ count the number of nodes that change from HTO to ETO 
        by making node an observation point """ 
        self.STAFAN_B()
        self.TPI_stat(HTO_th=HTO_th, HTC_th=HTC_th)
        HTO_old = set()
        for node in self.nodes_lev: 
            if (node.stat["SS@0"] == "HTO") or (node.stat["SS@1"] == "HTO"):
                HTO_old.add(node.num)
        orig_ntype = op.ntype
        self.PO.append(op)
        op.ntype = "PO"
        self.STAFAN_B()
        self.TPI_stat(HTO_th=HTO_th, HTC_th=HTC_th)
        HTO_new = set()
        count = 0
        for node in self.nodes_lev:
            if node.num in HTO_old:
                if (node.stat["SS@0"] != "HTO") and (node.stat["SS@1"] != "HTO"):
                    # print("\t{} was HTO, but now became ETO".format(node.num))
                    count = count + 1
        op.ntype = orig_ntype
        self.PO = self.PO[:-1]
        return count
    
    def save_circuit_entropy(self, fname):
        if not os.path.exists('../data/stafan-data'):
            os.makedirs('../data/stafan-data')
        outfile = open(fname, "w")
        for node in self.nodes_lev:
            arr = [node.num,node.Entropy] 
            arr = [str(x) for x in arr]
            ss = ",".join(arr)
            outfile.write(ss + "\n")
        outfile.close()

    def make_num_int(self):
        node2int = dict()
        for idx, node in enumerate(self.nodes_lev):
            node2int[node.num] = idx
        return node2int

    def gen_graph(self):
        """
        Generate directed graph of the circuit, each node has attributes: CC0, CC1, CO, lev
        """
        import networkx as nx
        G = nx.DiGraph()
        for n in self.nodes_lev:
            n_num_normal = n.num
            G.add_node(n_num_normal)
            G.nodes[n_num_normal]['lev'] = n.lev
            G.nodes[n_num_normal]['gtype'] = n.gtype
            G.nodes[n_num_normal]['ntype'] = n.ntype
            G.nodes[n_num_normal]['CC0'] = n.CC0
            G.nodes[n_num_normal]['CC1'] = n.CC1
            G.nodes[n_num_normal]['CO'] = n.CO
            G.nodes[n_num_normal]['C0'] = n.C0
            G.nodes[n_num_normal]['C1'] = n.C1
            G.nodes[n_num_normal]['S'] = n.S
            G.nodes[n_num_normal]['B0'] = n.B0
            G.nodes[n_num_normal]['B1'] = n.B1
            if n.gtype != 'IPT':
                for unode in n.unodes:
                    G.add_edge(unode.num, n_num_normal)
            else:
                pass
        return G

    def get_node_attr(self, node_attr):
        data = []
        for node in self.nodes_lev:
            data.append(getattr(node, node_attr))

        return data
  
    def make_PO(self, target):
        """ connects this target node to a PO using a branch 
        """
        if target.ntype == "PO":
            return 
        # target becomes stem, create new branches:
        new_brch = node.BRCH("PO", "BRCH", target.num+"-IPO") 
        old_brch = node.BRCH("FB", "BRCH", target.num+"-OLD")

        # fixing unodes for new branches
        new_brch.unodes.append(target)
        old_brch.unodes.append(target)
        old_brch.dnodes = target.dnodes
        
        # fixing unodes for target.dnodes
        # if target was stem:
        if len(target.dnodes) > 1:
            for dnode in target.dnodes:
                dnode.unodes = [old_brch]
        # if target was a gate
        else:
            new_unodes = []
            for unode in target.dnodes[0].unodes:
                if unode.num != target.num:
                    new_unodes.append(unode)
            new_unodes.append(old_brch)
            target.dnodes[0].unodes = new_unodes

        self.PO.append(new_brch)    
        self.nodes[new_brch.num] = new_brch