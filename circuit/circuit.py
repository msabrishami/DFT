# -*- coding: utf-8 -*-

import re
import random
from enum import Enum
import math
import sys
from node import gtype
from node import ntype
from node import *
import collections
# import networkx as nx
import matplotlib.pyplot as plt
from itertools import cycle

from random import randint
import time
import pdb
from multiprocessing import Process, Pipe
#import numpy as np
import os 
import utils
import config
#import xlwt

#TODO: one issue with ckt (2670 as example) is that some nodes are both PI and PO
#TODO: we need a flag to make sure no new nodes are added to the circuit, 
#   ... for example, if we find all cell types in one method, later we should 
#   ... read this flag to make sure what this method found is valid now, 
#   ... and no new cell added that is not tracked. 
#TODO: in DFT package gates are logical, NAND can have several inputs, but 
#   ... for SSTA we have cell SSTA delay for NAND2 and NAND3, fix this!
# distributions added to the repo temporarily 
# sys.path.insert(1, "/home/msabrishami/workspace/StatisticsSTA/")
import load_circuit



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


class Circuit:
    """ Representing a digital logic circuit, capable of doing logic simulation, 
        test related operations such as fault simulation, ATPG, OPI, testability 
        measurements, SSTA, etc. 

        Attributes
        ---------
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

    def __init__(self, netlist_fname):
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

        load_circuit.LoadCircuit(self, netlist_fname)
       
    
    def lev(self):
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
                        print("Warning! Node {} has zero fanins".format(node.num))
                        print(node)
                        print("level of this node is set to zero")
                        node.lev = 0
                    else:
                        node.lev = max(lev_u) + 1
                        flag_change = True
    
        self.nodes_lev = sorted(list(self.nodes.values()), key=lambda x:x.lev)
    
    
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
            idx = randint(0, len(self.nodes))
            res.add(self.nodes_lev[idx])
        return list(res)[0] if count==1 else res
    
    
    def print_fanin(self, target_node, depth):
        # TODO: needs to be checked and tested -- maybe using utils.get_fanin?
        queue = collections.deque()
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
        print()
        print("queue is: " + ",".join([node.num for node in queue]))
        if len(queue) == 0:
            return 
        
        target_node = queue.popleft()
        print(target_node)
        
        if target_node.lev == min_level:
            return 
        
        for node in target_node.unodes:
            print("added node {} to the queue".format(node.num))
            queue.append(node)
            
        self.print_fanin_rec(queue, min_level)

    def gen_single_tp(self, mode="b"):
        """ Randomly generate a single input pattern.
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
        """ Generates multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns the list of geneted test patterns
        does not store the generated tps in file 
        converts tp_count to int, as sometimes we pass fps (e.g. 1e6)
        """
        tps = [self.gen_single_tp(mode) for _ in range(int(tp_count))] 
        return tps

    def gen_tp_file(self, tp_count, tp_fname=None, mode="b", verbose=False):
        """ create single file with multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns the list of geneted test patterns
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
            print("Generated {} test patterns and saved in {}".format(tp_count, tp_fname))
        return tps
    

    def gen_tp_file_full(self, tp_fname=None):
        """ create a single file including all possible tps """ 
        if len(self.PI) > 12:
            print("Error: cannot generate full tp file for circuits with PI > 12")
            return []
        fn = os.path.join(config.PATTERN_DIR, self.c_name + "_tp_full.tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.PI]) + "\n")
        tps = [] 
        for t in range(2**len(self.PI)):
            tp = [str(random.randint(0,1)) for x in range(len(self.PI))]
            tp = "{:{}b}".format(t, len(self.PI)).replace(" ", "0")
            tps.append(tp)
            outfile.write(",".join(list(tp)) + "\n")
        outfile.close()
        print("Generated full test patterns and saved in {}".format(tp_fname))
        return tps

    
    def load_tp_file(self, fname):
        """ Load single file with multiple test pattern vectors. """ 
        # do we need to check the order of the inputs in the file?  
        # this can be done using "yield" or "generate" -- check online 
        infile = open(fname, 'r')
        tps = []
        lines = infile.readlines()

        for line in lines[1:]:
            words = line.rstrip().split(',')
            words = [int(word) if word == '1' or word == '0' else 'X' for word in words]
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
        Reads a given pattern and perform the logic simulation
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
        - generates an output folder in ../data/modelsim/circuit_name/ directory
        - read a input file in input folder
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
        print("Logic-Sim validation with {} patterns".format(int((len(lines)-2)/3)))
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
    
    
    def SCOAP_CC(self):
        """ Calculates combinational controllability based on SCOAP measure """ 
        for node in self.nodes_lev:
            node.eval_CC()
    
    def SCOAP_CO(self):
        """ Calculates combinational observability based on SCOAP measure """ 
        for node in self.PO:
            node.CO = 0

        for node in reversed(self.nodes_lev):
            node.eval_CO()

    def STAFAN_reset_counts(self):
        for node in self.nodes_lev:
            node.one_count = 0
            node.zero_count = 0
            node.sen_count = 0

    def STAFAN_reset_flags(self):
        for node in self.nodes_lev:
            node.sense = False
    
    def STAFAN_C_single(self, tp):
        """ Running STAFAN controllability step for one test pattern 
        The initialization of nodes C1 and C0 are done in the prior method 

        Arguments
        ---------
        tp : a single test pattern vector 
        """
        self.logic_sim(tp)
        self.STAFAN_reset_flags()
            
        for node in self.nodes_lev:
            node.one_count = node.one_count + 1 if node.value == 1 else node.one_count
            node.zero_count = node.zero_count + 1 if node.value ==0 else node.zero_count

            # sensitization
            if node.is_sensible():
                node.sense = True
                node.sen_count += 1

    
    def STAFAN_C(self, tp, limit=None):
        ''' 
        STAFAN controllability 

        Arguments: 
        ----------
        tp : Either the name of a test pattern file (str) or number of test patterns (int).
            If tp is number of test patterns, they will be generated internally within limit
        limit : Limit of test patterns to be generated.
            If limit is not given, all possible tps can be generated. 
            Every test pattern can be assigned a number by putting binary values of 
            primary inputs together in the same sequence as in self.PI, and then converting 
            this value to a decimal one. 
        
        Note: Random input patterns are generated with replacement (not pseudo-random)
        Note: random.choice method is very inefficient
        '''

        if isinstance(tp, str):
            tps = self.load_tp_file(tp)
            num_pattern = len(tps)
            tp_gen = False 

        elif isinstance(tp,int):
            tp_gen = True
            num_pattern = tp

        # We need to reset the circuit
        self.STAFAN_reset_counts()
        if limit == None:
            limit = [0, pow(2, len(self.PI))-1]

        for t in range(num_pattern):
            if tp_gen:
                b = ('{:0%db}'%len(self.PI)).format(randint(limit[0], limit[1]))
                tp = [int(b[j]) for j in range(len(self.PI))]
            else:
                tp = tps[t]

            self.STAFAN_C_single(tp)

        # calculate percentage/prob
        for node in self.nodes_lev:
            node.C1 = node.one_count / num_pattern
            node.C0 = node.zero_count / num_pattern
            node.S = node.sen_count / num_pattern


    def STAFAN_B(self):
        """ calculates the STAFAN observability probabilities for all nodes """

        for node in reversed(self.nodes_lev):
            if node in self.PO:
                node.B0 = 1.0
                node.B1 = 1.0
            node.stafan_b()
            node.CB1 = node.C1 * node.B1
            node.CB0 = node.C0 * node.B0
            node.B = (node.B0*node.C0) + (node.B1*node.C1)

    
    def STAFAN_ctrl_process(self, conn, id_proc, tot_tp_count, tot_proc):
        circuit = Circuit(self.c_fname)
        circuit.lev()
        PI_num = len(circuit.PI)
        tp_count = int(tot_tp_count / tot_proc)
        limit = [int(pow(2, PI_num)/tot_proc) * id_proc, 
                int(pow(2, PI_num)/tot_proc)*(id_proc+1)-1]
        circuit.STAFAN_C(tp_count, limit)

        one_count_list = []
        zero_count_list = []
        sen_count_list = []
        for i in circuit.nodes_lev:
            one_count_list.append(i.one_count)
            zero_count_list.append(i.zero_count)
            sen_count_list.append(i.sen_count)
        conn.send((one_count_list, zero_count_list, sen_count_list))
        conn.close()


    def STAFAN(self, total_tp, num_proc=1, verbose=False):
        """ 
        Generating STAFAN controllability and observability in parallel. 
        Random TPs are generated within the method itself and are not stored. 
        
        Arguments:
        ---------
        total_tp : (int) total number of test pattern vectors (not less than num_proc)
        num_proc : (int) number of processors that will be used in parallel processing 
        """
        if total_tp < num_proc:
            raise ValueError("Total TPs should be higher than process numbers")

        start_time = time.time()
        process_list = []
        for id_proc in range(num_proc):
            parent_conn, child_conn = Pipe()
            p = Process(target = self.STAFAN_ctrl_process, 
                    args =(child_conn, id_proc, total_tp, num_proc))
            p.start()
            process_list.append((p, parent_conn))

        one_count_list = [0] * len(self.nodes_lev) 
        zero_count_list = [0] * len(self.nodes_lev) 
        sen_count_list = [0] *  len(self.nodes_lev)

        for p, conn in process_list:
            tup = conn.recv()
            for i in range(len(tup[0])):
                one_count_list[i] += tup[0][i]
                zero_count_list[i] += tup[1][i]
                sen_count_list[i] += tup[2][i]
            p.join()
        
        for idx, node in enumerate(self.nodes_lev):
            node.C1 = one_count_list[idx] / total_tp
            node.C0 = zero_count_list[idx] / total_tp
            node.S = sen_count_list[idx] / total_tp

        if verbose: 
            for node in self.nodes_lev:
                if node.C0 == 0 or node.C1 == 0:
                    print("Warning: node {} controllability is zero".format(node.num))
        try: 
            self.STAFAN_B()
        except ZeroDivisionError:
            print("Node Ctrl is zero")
            pdb.set_trace()
        for node in self.nodes_lev:
            node.D1 = node.B0 * node.C0
            node.D0 = node.B1 * node.C1
        end_time = time.time()
        duration = end_time - start_time
        if verbose:
            print ("Processor count: {}, TP-count: {}, Time: {:.2f} sec".format(
                num_proc,total_tp ,duration))

    
    def save_TMs(self, fname=None, tp=None):
        if fname == None:
            path = config.STAFAN_DIR+"/"+self.c_name
            if not os.path.exists(path):
                os.mkdir(path)
            fname = os.path.join(path, self.c_name)
            if not os.path.exists(fname):
                os.mkdir(fname)
            fname = os.path.join(fname, "{}-TP{}.stafan".format(self.c_name, tp))

        outfile = open(fname, "w")
        outfile.write("Node,C0,C1,B0,B1,S\n")
        for node in self.nodes_lev:
            ss = ["{:e}".format(x) for x in [node.C0, node.C1, node.B0, node.B1, node.S]]
            outfile.write(",".join([node.num] + ss) + "\n")
        outfile.close()
        print("Saved circuit STAFAN TMs in {}".format(fname))

    
    def load_TMs(self, fname):
        lines = open(fname).readlines()[1:]
        for line in lines:
            words = line.strip().split(",")
            node = self.nodes[words[0]]
            node.C0 =   float(words[1])  
            node.C1 =   float(words[2]) 
            node.B0 =   float(words[3]) 
            node.B1 =   float(words[4]) 
            node.S  =   float(words[5]) 
            node.D0 = node.C1 * node.B1
            node.D1 = node.C0 * node.B0

        print("Loaded circuit STAFAN TMs loaded from: " + fname)


    def STAFAN_FC(self, tp_count):
        """ Estimation of fault coverage for all faults 
        All faults include all nodes, SS@0 and SS@1 
        pd stands for probability of detection 

        Arguments: 
        ----------
        tp_count : int
            number of test patterns, used in the fault coverage estimation formula 
        """

        nfc = 0
        for node in self.nodes_lev:
            nfc += math.exp(-1 * node.D1 * tp_count) 
            nfc += math.exp(-1 * node.D0 * tp_count) 
        return 1 - nfc/(2*len(self.nodes)) 


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

    
    def gen_fault_dic(self):
        """
        Fault Dictionary:
        key: input pattern value: detected fault (returned by PFS)
        Fault Dictionary can only be generated for small circuits
        because the file size will become too large for big circuits.
        """
        fault_dict = {}
        inputnum = len(self.input_num_list)
        total_pattern = pow(2,inputnum) # produce 2^n different input files for pfs to use

        for i in range(total_pattern):
            #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
            b = ('{:0%db}'%inputnum).format(i)
            list_to_pfs = []
            for j in range(inputnum):
                list_to_pfs.append(int(b[j]))

            #do pfs based on the prodeuced input files
            result = []
            result = self.pfs(list_to_pfs)
            fault = []
            for i in result:
                fault.append("%d@%d" % (i[0], i[1]))

            fault.sort(key = lambda i:int(re.match(r'(\d+)',i).group()))
            #jb51.net/article/164342.htm for referance to sort the output

            fault_dict.update({b: fault})

        fault_dict_result = open("../fault_dic/{}.fd".format(self.c_name), "w")
        for i in range(len(self.input_num_list)):
            if (i<len(self.input_num_list)-1):
                fault_dict_result.write('%d->' % self.input_num_list[i])
            else:
                fault_dict_result.write('%d' % self.input_num_list[i])

        fault_dict_result.write(' as sequence of inputs')
        fault_dict_result.write('\n')
        fault_dict_result.write('tps\t\t\tdetected_faults\n')
        for i in range(total_pattern):
            #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
            b = ('{:0%db}'%inputnum).format(i)
            fault_dict_result.write('%s\t\t\t\t' % b)
            for i in range(len(fault_dict.get(b))):
                fault_dict_result.write('%-5s ' % fault_dict.get(b)[i])#format ok?
            fault_dict_result.write('\n')

        fault_dict_result.close()


    def gen_fault_dic_multithreading(self, thread_cnt, idx):
        """
        Create threads to generate fault dictionaries.
        Speed up the fault dictionary generation process.
        """
        fault_dict = {}
        total_pattern = pow(2, len(self.PI))
        pattern_per_thread = int(total_pattern / thread_cnt)

        for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
            #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
            b = ('{:0%db}'%len(self.PI)).format(i)
            list_to_pfs = []
            for j in range(len(self.PI)):
                list_to_pfs.append(int(b[j]))
        #do pfs based on the prodeuced input files
            result = []
            result = self.pfs(list_to_pfs)
            fault = []
            #print(result)
            for i in result:
                fault.append("%d@%d" % (i[0], i[1]))

            fault.sort(key = lambda i:int(re.match(r'(\d+)',i).group()))
            fault_dict.update({b: fault})

        with open ("../fault_dic/{}_{}.fd".format(self.c_name, idx), "w") as fo:
            for i in range(len(self.PI)):
                if (i < len(self.PI) - 1):
                    fo.write('%d->' % self.input_num_list[i])
                else:
                    fo.write('%d' % self.input_num_list[i])
            fo.write(' as sequence of inputs')
            fo.write('\n')
            fo.write('tps\t\t\tdetected_faults\n')
            for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
                b = ('{:0%db}'%len(self.PI)).format(i)
                fo.write('%s\t\t\t\t' % b)
                for i in range(len(fault_dict.get(b))):
                    fo.write('%-5s ' % fault_dict.get(b)[i])#format ok?
                fo.write('\n')
        print("thread #{} of {} threads finished".format(idx, thread_cnt))

    
    def read_fault_dict(self):
        """read already generated fault dictionary"""
        fd = open("../fault_dic/{}.fd".format(self.c_name),"r")
        self.fd_data = fd.read()
        fd.close()

    
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
        new_brch = BRCH("PO", "BRCH", target.num+"-IPO") 
        old_brch = BRCH("FB", "BRCH", target.num+"-OLD")

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

    def all_shortest_distances_to_PO(self):
        """ Calculate shortest distace from any gate to any PO 
        using Dijktra algorithm
        """
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
        # print('Distances from node to the nearest output:', 
        #         *[f'{d[0].num}: {d[1]}' for d in dist.items()], sep='\n')
