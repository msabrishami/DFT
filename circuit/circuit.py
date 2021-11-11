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
from distributions import Distribution, Normal, SkewNormal, MaxOp, SumOp, NumDist


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
        c_name : str
            the full name of the circuit with path and format 
        """

        self.c_fname = netlist_fname 
        self.c_name = netlist_fname.split('/')[-1].split('.')[0]

        self.nodes = {}     # dict of all nodes, key is now string node-num
        self.nodes_lev = [] # list of all nodes, ordered by level
        self.PI = [] # this should repalce input_num_list
        self.PO = [] # this should be created to have a list of outputs

        load_circuit.LoadCircuit(self, netlist_fname)
        
        # Saeed does not confirm using these attributes
        self.fault_name = []
        self.fault_node_num = []
        self.fault_type = [] # fault type for each node in fault list, s-a-1 or s-a-0
        self.fd_data = None
        self.pass_cnt = 0
        self.rfl_node = []
        self.rfl_ftype = []
        # PFS: 
        self.in_fault_node_num = [] # input fault num, string format
        self.in_fault_node_type = [] # input fault type, integer format
        
    
    def add_node(self, line):
        raise NameError("This method is deprecated")
    
    
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
                    # print(num, lev_u)
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
    
    def print_fanin(self, target_node, depth):
        queue = collections.deque()
        queue.append(target_node)
        min_level = max(0, target_node.lev - depth) 
        self.print_fanin_rec(queue, min_level)

    def print_fanin_rec(self, queue, min_level):
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

    def gen_tp(self):
        """
        Randomly generate a test pattern for input nodes.
        Could be used to check the validity of logic simulation
        and deductive fault simulation.
        """
        rand_input_val_list = []
        for i in range(len(self.PI)):
            rand_input_val_list.append(random.randint(0,1))
        return rand_input_val_list
    

    def gen_tp_file(self, test_count, fname=None, mode="b"):
        """ Create single file with multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        """ 
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")
        fn = "./" + self.c_name + "_" + str(test_count) + "_tp_" + mode + ".txt"
        fname = fn if fname==None else fname
        outfile = open(fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.PI]) + "\n")
        tps = [] 
        
        bits = ["0","1","X"]
        for t in range(test_count):
            if mode == "b":
                pat = [bits[random.randint(0,1)] for x in range(len(self.PI))]
            elif mode == "x":
                pat = [bits[random.randint(0,2)] for x in range(len(self.PI))]
            tp = pat 
            tps.append(tp)
            outfile.write(",".join(pat) + "\n")
        
        outfile.close()
        print("Generated {} test patterns and saved in {}".format(test_count, fname))
        return tps

    # do we need to check the order of the inputs in the file?  
    # this can be done using "yield" or "generate" -- check online 
    def load_tp_file(self, fname):
        """ Load single file with multiple test pattern vectors.
        """ 
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


    def logic_sim(self, input_pattern):
        """
        Logic simulation:
        Reads a given pattern and perform the logic simulation
        Currently just works with binary logic
        input_pattern is a list of values (currently int) in the ... 
            ... same order as in self.PI
        """
        node_dict = dict(zip([x.num for x in self.PI], input_pattern))

        for node in self.nodes_lev:
            if node.gtype == "IPT":
                node.imply(node_dict[node.num])
            else:
                node.imply()

    def logic_sim_bitwise(self, input_pattern, test_len,fault=None):
        """
        Logic simulation bitwise mode:
        Reads a given pattern and perform the logic simulation bitwise

        Arguments
        ---------
        input_pattern : list of int 
            input pattern in the same order as in self.PI
        fault : str
            node.num@fault --> example: N43@0 means node N43 single stuck at zero 

        fault
        """
        node_dict = dict(zip([x.num for x in self.PI], input_pattern))
        # TODO: get rid of this shit! Why did we not implement this within constructor?
        # print(max(input_pattern))
        n = sys.maxsize
        # bitlen = min(math.log2(n)+1,test_len)
        bitlen = math.log2(n)+1

        bitwise_not = 2**bitlen-1
        
        if fault:
            # print("PPSF for faulty circuit")
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
                # tmp = str(node)
                # print(tmp, " ".join([""]*(60-len(tmp))) + "{:064b}".format(
                #     node.value) )

        else:
            # print("PPSF for good circuit")
            for node in self.nodes_lev:
                if node.gtype == "IPT":
                    node.imply_b(node_dict[node.num])
                else:
                    node.imply_b()

                # tmp = str(node)
                # print(tmp, " ".join([""]*(60-len(tmp))) + "{:064b}".format(
                #     node.value) )
    
    # Saeed needs to rewrite this method using 'yield' in load_tp_file     
    def logic_sim_file(self, in_fname, out_fname, stil=False): 
        """
        logic simulation with given input vectors from a file
        - generates an output folder in ../data/modelsim/circuit_name/ directory
        - read a input file in input folder
        - generate a output file in output folder by using logic_sim() function
        """
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

    # Saeed: this needs to be tested by myself later
    def golden_test(self, golden_io_filename):
        # compares the results of logic-sim of this circuit, 
        #  ... provided a golden input/output file
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

    
    def STAFAN_CS(self, tp, limit=None):
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
        else:
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


    def get_full_fault_list(self):
        """
        Generate a list of all SSAFs in the circuit.
        Given N nodes, there should be 2N SSAFs.
        """
        for node in self.nodes_lev:
            sa0_str = "{}@0".format(node.num)
            self.fault_name.append(sa0_str)
            self.fault_node_num.append(node.num)
            self.fault_type.append(0)

            sa1_str = "{}@1".format(node.num)
            self.fault_name.append(sa1_str)
            self.fault_node_num.append(node.num)
            self.fault_type.append(1)

    def pfs_in_fault_list(self,fname_fl):
        """
        Parallel Fault Simulation:
        For a given input fault list
        generate two lists: in_fault_node_num, in_fault_node_type.
        """
        fr = open(fname_fl, mode='r')
        lines = fr.readlines()
        self.in_fault_node_num = []
        self.in_fault_node_type = []
        for line in lines:
            line=line.rstrip('\n')
            line_split=line.split('@')
            self.in_fault_node_num.append(line_split[0])
            self.in_fault_node_type.append(int(line_split[1]))

    
    def pfs_single(self, input_pattern,in_fl_mode):
        """
        Parallel Fault Simulation:
        For a given test pattern
        faults in self.fault_node_num 
        PFS simulates a set of faults detected by the test pattern.
        """
        
        pfs_fault_val = []
        pfs_fault_num = []
        if in_fl_mode == 1:
            faultnum = len(self.fault_node_num)
            pfs_fault_num = self.fault_node_num.copy()
            pfs_fault_val = self.fault_type.copy()
        else:
            faultnum = len(self.in_fault_node_num)
            pfs_fault_num = self.in_fault_node_num.copy()
            pfs_fault_val = self.in_fault_node_type.copy()

        n = sys.maxsize
        bitlen = int(math.log2(n))+1
        # bitlen = min(math.log2(n)+1,test_len)
        bitwise_not = 2**bitlen-1

        pass_tot = math.ceil(float(faultnum) / float(bitlen-1))

        detected_fault_num = []
        detected_fault_value = []

        while (pass_tot != 0):
            pass_tot -= 1
            pfs_stuck_values = 0
            read_fault_ind = 0

            # fault list for one pass
            fault_num = []
            fault_val = []
            mask_dict = {}  # {key: fault_num, value: mask}

            # save bitlen -1 fault
            while(1):
                if len(pfs_fault_num)==0:
                    break

                fault_val.append(pfs_fault_val.pop())
                fault_num.append(pfs_fault_num.pop())

                read_fault_ind = read_fault_ind + 1
                if read_fault_ind == bitlen - 1:
                    break
            
            # calculate stuck values of faults in this pass of PFS, and mask for each fault_num
            for i in range(len(fault_val)):
                pfs_stuck_values = pfs_stuck_values + fault_val[i]*2**i

                if fault_num[i] in mask_dict:
                    mask_dict[fault_num[i]] = mask_dict[fault_num[i]] + 2**i
                else:
                    mask_dict[fault_num[i]] = 2**i
            
            # pfs for one pass
            node_dict = dict(zip([x.num for x in self.PI], input_pattern))
            for node in self.nodes_lev:
                node.pfs_I = 0
                node.pfs_S = pfs_stuck_values

                # if fault should be inserted in this node
                if node.num in mask_dict:
                    node.pfs_I = mask_dict[node.num]

                if node.gtype == "IPT":
                    node.imply_p(bitwise_not,node_dict[node.num])
                else:
                    node.imply_p(bitwise_not)
                node.insert_f(bitwise_not)
            
            # output result
            for i in self.nodes_lev:
                if i.ntype == 'PO':
                    # if some faults can be detected
                    if (i.pfs_V != 0) and (i.pfs_V != bitwise_not):
                        pfs_V_str = format(i.pfs_V,"b").zfill(bitlen)
                        msb_pfs_V = pfs_V_str[0]        # MSB of pfs_V: good circuit
                        for j in range(bitlen-1):
                            #if j == len(fault_num):
                                #break
                            if pfs_V_str[bitlen-1-j] != msb_pfs_V:
                                detected_fault_num.append(fault_num[j])
                                detected_fault_value.append(fault_val[j])

        fault_set = set()
        for k in range(len(detected_fault_num)):
            fault_set = fault_set.union({(detected_fault_num[k],detected_fault_value[k])})

        return fault_set

    def pfs_multiple_separate(self, fname_tp, fname_log, in_fl_mode, mode="b"):
        """ 
        new pfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [(1,0),(1,1),(8,0),(5,1),(6,1)]
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")
        # if os.path.exists('../data/fault_sim/') == False:
        #     os.mkdir('../data/fault_sim/')
        # input_path = '../data/modelsim/' + self.c_name + '/input/'
        # if os.path.exists(input_path) == False:
        #     os.mkdir(input_path)
        # output_path = '../data/fault_sim/' + self.c_name + '/'
        # if os.path.exists(output_path) == False:
        #     os.mkdir(output_path)
        output_path = config.FAULT_SIM_DIR + '/' + self.c_name + '/pfs/'
        input_path = config.FAULT_SIM_DIR + '/' + self.c_name + '/input/'
        if not os.path.exists(output_path):
                os.mkdir(output_path)
        if not os.path.exists(input_path):
            raise NameError("No test pattern folder!")
        fr = open(input_path + fname_tp, mode='r')
        # output_path = output_path + fname.rstrip('tp_b.txt') + '_dfs_out.txt'
        fw = open(output_path + fname_log, mode='w')
        
        lines = fr.readlines()
        # obtain a multiple test patterns list from the input file
        pattern_list = []
        for line in lines[1:]:
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            pattern_list.append(line_split)
        for sub_pattern in pattern_list:
            fault_subset = self.pfs_single(sub_pattern,in_fl_mode)
            fault_sublist = list(fault_subset)
            updated_fault_sublist = []
            for subset in fault_sublist:
                if '-' in subset[0]:
                    updated_fault_sublist.append((subset[0].split('-')[0], subset[0].split('-')[1], subset[1]))
                else:
                    updated_fault_sublist.append((subset[0], '0', subset[1]))
            updated_fault_sublist.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
            pattern_str = map(str,sub_pattern)
            pattern_str = ",".join(pattern_str)
            fw.write(pattern_str + '\n')
            fault_coverage = float(len(fault_sublist) / (2*len(self.nodes_lev)))
            for fault in updated_fault_sublist:
                if fault[1] == '0':
                    fw.write(str(fault[0]) + '@' + str(fault[2]) + '\n')
                else:
                    fw.write(str(fault[0]) + '-' + str(fault[1]) + '@' + str(fault[2]) + '\n')
            fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
            fw.write('\n')
        fr.close()
        fw.close()
        print("PFS-Separate completed. \nLog file saved in {}".format(fname_log))


    def pfs_multiple(self, fname_tp, fname_log, in_fl_mode, mode="b"):
        """ 
        new pfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [(1,0),(1,1),(8,0),(5,1),(6,1)]
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")

        output_path = config.FAULT_SIM_DIR + '/' + self.c_name + '/pfs/'
        input_path = config.FAULT_SIM_DIR + '/' + self.c_name + '/input/'
        if not os.path.exists(output_path):
                os.mkdir(output_path)
        if not os.path.exists(input_path):
            raise NameError("No test pattern folder!")
        fr = open(input_path + fname_tp, mode='r')
        # output_path = output_path + fname.rstrip('tp_b.txt') + '_dfs_out.txt'
        fw = open(output_path + fname_log, mode='w')
        
        lines = fr.readlines()
        # obtain a multiple test patterns list from the input file
        pattern_list = []
        for line in lines[1:]:
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            pattern_list.append(line_split)
        fault_set = set()
        for sub_pattern in pattern_list:
            fault_subset = self.pfs_single(sub_pattern,in_fl_mode)
            fault_set = fault_set.union(fault_subset)
        fault_list = list(fault_set)
        updated_fault_sublist = []
        for subset in fault_list:
            if '-' in subset[0]:
                updated_fault_sublist.append((subset[0].split('-')[0], subset[0].split('-')[1], subset[1]))
            else:
                updated_fault_sublist.append((subset[0], '0', subset[1]))
        updated_fault_sublist.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
        fault_coverage = float(len(fault_list) / (2*len(self.nodes_lev)))
        for fault in updated_fault_sublist:
            if fault[1] == '0':
                fw.write(str(fault[0]) + '@' + str(fault[2]) + '\n')
            else:
                fw.write(str(fault[0]) + '-' + str(fault[1]) + '@' + str(fault[2]) + '\n')
        fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
        fr.close()
        fw.close()
        print("PFS-Separate completed. \nLog file saved in {}".format(fname_log))
    


    def pfs_exe(self, in_fl_mode, tp_num=1, mode='rand',fname_fl=None):
        """
        Execute pfs in rand or full mode
        rand: the total faults can be detected by several random patterns
        full: the faults can be detected by each single pattern; all possible patterns are included
        """
        if in_fl_mode == 1:
            self.get_full_fault_list()
        else:
            self.pfs_in_fault_list(fname_fl)
        if mode == 'rand':
            pfs_report_fname = self.c_name + '_' + str(tp_num) + '_pfs_b.log'
            tp_path = config.FAULT_SIM_DIR
            if not os.path.exists(tp_path):
                os.mkdir(tp_path)
            tp_path = config.FAULT_SIM_DIR + '/' + self.c_name + '/'
            if not os.path.exists(tp_path):
                os.mkdir(tp_path)
            tp_path = config.FAULT_SIM_DIR + '/' + self.c_name + '/input/'
            if not os.path.exists(tp_path):
                os.mkdir(tp_path)
            #tp_fname = tp_path + self.c_name + '_' + str(tp_num) + "_tp_b.txt"
            #tp_fname_bare = self.c_name + '_' + str(tp_num) + "_tp_b.txt"
            # generate given number random patterns
            '''
            self.gen_tp_file(
            tp_num, 
            fname=tp_fname,
            mode = "b")
            '''
            # run pfs
            self.pfs_multiple(
            fname_tp = self.tp_fname_bare,
            fname_log=pfs_report_fname,
            in_fl_mode = in_fl_mode,
            mode='b')

        elif mode == 'full':
            pfs_report_fname = self.c_name + "_full_pfs_b.log"
            tp_fname_bare = self.c_name + '_full_tp_b.txt'
            # generate all possible patterns in order
            self.regular_tp_gen()
            # run pfs
            self.pfs_multiple_separate(
            fname_tp = tp_fname_bare,
            fname_log=pfs_report_fname,
            in_fl_mode = in_fl_mode,
            mode='b')

        else:
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")


   

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
        fault_dict_result.write('input_patterns\t\t\tdetected_faults\n')
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
            fo.write('input_patterns\t\t\tdetected_faults\n')
            for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
                b = ('{:0%db}'%len(self.PI)).format(i)
                fo.write('%s\t\t\t\t' % b)
                for i in range(len(fault_dict.get(b))):
                    fo.write('%-5s ' % fault_dict.get(b)[i])#format ok?
                fo.write('\n')
        print("thread #{} of {} threads finished".format(idx, thread_cnt))

    def get_reduced_fault_list(self):
        """
        Using checkpoint theorem,
        generate reduced fault list
        Warning: Checkpoint theorem does not apply to XOR/XNOR gates
        """
        faults_fanout = []
        for i in range(len(self.nodes)):
            if (self.nodes[i].cpt == 1):
                #print self.nodes[i].num
                for j in range(self.nodes[i].fout):
                    faults_fanout.append(self.nodes[i].dnodes[j].index)
                self.nodes[i].sa0 = 1
                self.nodes[i].sa1 = 1
        # uniquefanout = sorted(set(faults_fanout))
        # print uniquefanout
        for i in range(len(faults_fanout)):
            cptflag = 0
            if ((self.nodes[faults_fanout[i]].gtype == 'NOR') or (self.nodes[faults_fanout[i]].gtype == 'OR')):
                for j in range(self.nodes[faults_fanout[i]].fin):
                    if self.nodes[faults_fanout[i]].unodes[j].cpt == 1:
                        if cptflag == 0:
                            cptflag = 1
                        else: self.nodes[faults_fanout[i]].unodes[j].sa1 = 0
            elif ((self.nodes[faults_fanout[i]].gtype == 'NAND') or (self.nodes[faults_fanout[i]].gtype == 'AND')):
                for j in range(self.nodes[faults_fanout[i]].fin):
                    if self.nodes[faults_fanout[i]].unodes[j].cpt == 1:
                        if cptflag == 0:
                            cptflag = 1
                        else: self.nodes[faults_fanout[i]].unodes[j].sa0 = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].sa0 == 1:
                self.rfl_node.append(self.nodes[i].num)
                self.rfl_ftype.append(0)
            if self.nodes[i].sa1 == 1:
                self.rfl_node.append(self.nodes[i].num)
                self.rfl_ftype.append(1)


    def D_alg(self, fault_index, imply_counter):
        """
        Given a fault, returns whether it can be detected,
        if can, returns a test pattern.
        """
        res = D_alg(self.nodes, fault_index, imply_counter)
        return res
    
    
    def podem(self, i):
        """
        Given a fault, returns whether it can be detected,
        if can, returns a test pattern.
        """
        res = podem(self.fault_node_num[i], self.fault_type[i], self.nodes, self.nodes_lev)
        return res

    
    def read_fault_dict(self):
        """read already generated fault dictionary"""
        fd = open("../fault_dic/{}.fd".format(self.c_name),"r")
        self.fd_data = fd.read()
        fd.close()

    
    def get_patterns(self, test_pattern):
        """
        Given a test pattern with "X"s,
        generate all possible patterns represent by that pattern.
        """
        xidx = []
        xcnt = 0
        for i in range(len(test_pattern)):
            if test_pattern[i] == 'X':
                xidx.append(i)
                xcnt += 1

        fmt_str = '{0:0%db}'%(xcnt)
        bit = []

        plist = []
        for i in range(2 ** (xcnt)):
            bit = [int(j) for j in fmt_str.format(i)]
            plist.append(bit)

        search = []
        for p in plist:
            binary_patterns = test_pattern
            for i in range(xcnt):
                binary_patterns[xidx[i]] = p[i]
            search.append(''. join(map(str, binary_patterns)))
        return search


    def check_failure(self, fault_name):
        """
        Check if the fault is undetected by searching the fault dictionary
        called for small circuit with fault fictionary only.
        """
        srch_str = '\s{}'.format(fault_name)
        if re.findall(srch_str, self.fd_data):
            return False
        else:
            return True


    def check_success(self, fault_name, search_patterns):
        """
        Check if the returned pattern can detected the given fault
        by searching the fault dictionary.
        called for small circuit with fault fictionary only.
        """
        pattern_found = 0
        for p in search_patterns:
            srch_str = '{}.*?\s{}'.format(p, fault_name)
            # print (srch_str)
            res = re.findall(srch_str, self.fd_data)
            if res:
                pattern_found = 1
            else:
                pattern_found = 0
        if pattern_found:
            return True
        else:
            return False

    def get_Xless_pattern(self, pattern):
        """
        For big circuit with too many Xs,
        randomly assign 1 or 0 to each X and returns a pattern.
        """
        pattern_Xless = []
        for v in pattern:
            if v == 'X':
                entry = random.getrandbits(1)
            else:
                entry = v
            pattern_Xless.append(entry)
        return pattern_Xless


    def get_d_correctness(self):
        """
        Check correctness of D algorithm for both detected and undetected faults.
        Called for small circuit.
        """
        self.read_fault_dict()
        d_error_cnt = 0
        # run the faults in full fault list
        for j in range(len(self.fault_node_num)):
            fault_index = -1
            for i in range(len(self.nodes_lev)):
                self.nodes_lev[i].value = five_value.X.value
                if self.nodes_lev[i].num == self.fault_node_num[j]:
                    # stuck at 0
                    if self.fault_type[j] == 0:
                        self.nodes_lev[i].value = five_value.D.value
                        fault_index = i
                    # stuck at 1
                    elif self.fault_type[j] == 1:
                        self.nodes_lev[i].value = five_value.D_BAR.value
                        fault_index = i
                    else:
                        print("operator error")
            imply_counter = Imply_counter(8000)
            res = self.D_alg(fault_index, imply_counter)

            # If the fault is detectable in
            if res.result == 1:
                # print("D_alg SUCCESS")
                search_patterns = self.get_patterns(res.pattern)
                pattern_found = self.check_success(self.fault_name[j], search_patterns)
                if pattern_found == 0:
                    print("D algorithm Error at fault {}, type SUCCESS".format(self.fault_name[j]))
                    d_error_cnt += 1
                else:
                    pass

            else:
                # print("D_alg FAILURE")
                error_not_found = self.check_failure(self.fault_name[j])
                if error_not_found == 0:
                    print("D algorithm Error at fault {}, type FAILURE".format(self.fault_name[j]))
                    d_error_cnt += 1
                else:
                    pass
        d_correctness_rate = ((len(self.fault_node_num) - d_error_cnt) / 
                len(self.fault_node_num)) * 100
        print ("D algorithm correctness rate: {}%".format(d_correctness_rate))


    def get_d_coverage(self):
        """
        Count the percentage of faults in the full fault list D algorithm claimed as detected.
        Further revise the coverage by passing the test pattern returned by D to DFS to see
        if the given fault is in the detected fault set.
        called for big circuits
        """
        failure_fault_list = []
        check_cnt = 0
        self.pass_cnt = 0

        for j in range(len(self.fault_node_num)):
            fault_index = -1
            for i in range(len(self.nodes)):
                if self.nodes[i].num == self.fault_node_num[j]:
                    # stuck at 0
                    if self.fault_type[j] == 0:
                        self.nodes[i].d_value.append(five_value.D.value)
                        fault_index = i
                    # stuck at 1
                    elif self.fault_type[j] == 1:
                        self.nodes[i].d_value.append(five_value.D_BAR.value)
                        fault_index = i
                    else:
                        print("operator error")
                else:
                    self.nodes[i].d_value.append(five_value.X.value)
            imply_counter = Imply_counter(8000)
            res = self.D_alg(fault_index, imply_counter)

            if res.result == 1:
                self.pass_cnt += 1

            else:
                failure_fault_list.append(self.fault_name[j])


            check_cnt += 1
            print ("check_cnt={}".format(check_cnt))
        d_coverage = (self.pass_cnt / len(self.fault_node_num)) * 100
        print ("D algorithm fault coverage: {}".format(d_coverage))
        self.pass_cnt = 0
        return failure_fault_list


    def get_podem_correctness(self):
        """
        Check correctness of Podem for both detected and undetected faults.
        Called for small circuit.
        """
        self.read_fault_dict()
        pd_error_cnt = 0
        for i in range(len(self.fault_node_num)):
            res = self.podem(i)
            if res.result == 1:
                search_patterns = self.get_patterns(res.pattern)
                pattern_found = self.check_success(self.fault_name[i], search_patterns)
                if pattern_found == 0:
                    print("Podem algorithm Error at fault {}, type SUCCESS".format(
                        self.fault_name[i]))
                    pd_error_cnt += 1
                else:
                    pass
            else:
                # print("Podem_alg FAILURE")
                error_not_found = self.check_failure(self.fault_name[i])
                if error_not_found == 0:
                    print("Podem algorithm Error at fault {}, type FAILURE".format(
                        self.fault_name[i]))
                    pd_error_cnt += 1
                else:
                    pass
        pd_correctness_rate = 100 *( (len(self.fault_node_num) - pd_error_cnt) / 
                len(self.fault_node_num) )
        print ("Podem algorithm correctness rate: {}%".format(pd_correctness_rate))


    def get_podem_coverage(self):
        """
        Count the percentage of faults in the full fault list Podem claimed as detected.
        Further revise the coverage by passing the test pattern returned by Podem to DFS to see
        if the given fault is in the detected fault set.
        called for big circuits
        """
        self.pass_cnt = 0
        for i in range(len(self.fault_node_num)):
            res = self.podem(i)
            if res.result == 1:
                self.pass_cnt += 1
                pattern = res.pattern
                input_pattern = self.get_Xless_pattern(pattern)
                # print(input_pattern)
                self.logic_sim(input_pattern)
                fault_set = self.dfs()
                fault = (self.fault_node_num[i],self.fault_type[i])
                if fault in fault_set:
                    pass
                else:
                    self.pass_cnt -= 1
                    print("Test Pattern error for Podem at fault {}".format(fault))
            else:
                pass
        pd_coverage = self.pass_cnt / len(self.fault_node_num) * 100
        self.pass_cnt = 0
        print ("Podem algorithm fault coverage: {}%".format(pd_coverage))


    def podem_single_test(self, fault_node_num, fault_type):
        res = podem(fault_node_num, fault_type, self.nodes, self.nodes_lev)
        return res


    def time_for_podem(self):
        totaltime = 0
        for i in range(len(self.fault_node_num)):
            starttime = time.time()
            res = self.podem_single_test(self.fault_node_num[i], self.fault_type[i])
            endtime = time.time()
            totaltime = totaltime + (endtime - starttime)
        print(totaltime)


    # @Ghazal this needs to be checked and tested
    def control_process(self, conn, id_proc, tot_tp_count, tot_proc):
        #TODO: we can have some analysis on variance right here!
        circuit = Circuit(self.c_fname)
        circuit.lev()
        PI_num = len(circuit.PI)
        tp_count = int(tot_tp_count / tot_proc)
        limit = [int(pow(2, PI_num)/tot_proc) * id_proc, 
                int(pow(2, PI_num)/tot_proc)*(id_proc+1)-1]
        circuit.STAFAN_CS(tp_count, limit)

        one_count_list = []
        zero_count_list = []
        sen_count_list = []
        for i in circuit.nodes_lev:
            one_count_list.append(i.one_count)
            zero_count_list.append(i.zero_count)
            sen_count_list.append(i.sen_count)
        conn.send((one_count_list, zero_count_list, sen_count_list))
        conn.close()


    # @Ghazal this needs to be checked and tested 
    def STAFAN(self, total_tp, num_proc=1):
        """ 
        Generating STAFAN controllability and observability in parallel  
        
        Arguments:
        ---------
        total_tp : (int) total number of test pattern vectors(not less than num_proc)
        num_proc : (int) number of processors that will be used in parallel processing 
        """

        if total_tp < num_proc:
            raise ValueError("Total number of test pattern vetors must be at least the same as process numbers")

        start_time = time.time()
        process_list = []
        for id_proc in range(num_proc):
            parent_conn, child_conn = Pipe()
            p = Process(target = self.control_process, 
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
        
        # self.nodes_lev.sort(key=lambda x: x.num)
        for idx, node in enumerate(self.nodes_lev):
            node.C1 = one_count_list[idx] / total_tp
            node.C0 = zero_count_list[idx] / total_tp
            node.S = sen_count_list[idx] / total_tp

        for node in self.nodes_lev:
            if node.C0 == 0 or node.C1 == 0:
                print("Warning: node {} controllability is zero".format(node.num))


        self.STAFAN_B()
        for node in self.nodes_lev:
            node.D1 = node.B0 * node.C0
            node.D0 = node.B1 * node.C1
        end_time = time.time()
        duration = end_time - start_time
        print ("Processor count: {}, Test pattern vectors: {}, Time taken: {:.2f} sec".format(num_proc,total_tp ,duration))

    
    def save_TMs(self, fname):
        outfile = open(fname, "w")
        for node in self.nodes_lev:
            arr = [node.num,node.C0,node.C1,node.B0,node.B1,node.S,node.CB0,node.CB1, node.B] 
            arr = [str(x) for x in arr]
            ss = ",".join(arr)
            outfile.write(ss + "\n")
        outfile.close()
        print("Saved circuit with STAFAN values in " + fname)

    
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


    def load_circuit(self, fname):
        infile = open(fname)
        for line in infile:
            words = line.strip().split(",")
            node = self.nodes[words[0]]
            node.C0 =   float(words[1])  
            node.C1 =   float(words[2]) 
            node.B0 =   float(words[3]) 
            node.B1 =   float(words[4]) 
            node.S  =   float(words[5]) 
            node.CB0 =  float(words[6]) 
            node.CB1 =  float(words[7]) 
            node.B =    float(words[8]) 
        # print("Circuit loaded: " + fname)

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


    def ssta_pmf(self):
        # all gate distributions are pmf and all process is numerical on pmfs 
        for node in self.nodes_lev:
            # if int(node.num) > 10:
            #     return 
            # print("-----------------------------------------------")
            # print(node)

            # Initiate the PIs first:
            if node.ntype == "PI":
                node.dd_node = Normal(0, 1)
            elif node.ntype == "FB":
                node.dd_node = node.unodes[0].dd_node
            elif node.ntype in ["GATE", "PO"]:
                opmax = MaxOp()
                dd_node_unodes = [unode.dd_node for unode in node.unodes]
                dd_node_max = dd_node_unodes[0]
                for n in range(1, len(dd_node_unodes)):
                    dd_node_max = opmax.max_num(dd_node_max, dd_node_unodes[n])

                opsum = SumOp()
                dd_cell = self.cell_ssta[node.gtype]
                node.dd_node = opsum.sum_num(dd_cell, dd_node_max)


    def ssta_plot(self, fname, select="gate"):
        """ Saves the plot of the delay distribution of the nodes 
        It can be modified to only plot the internal gates and outputs
        
        Parameters
        ---------
        fname : str 
            output file name 
        select : string
            what nodes should be plotted
            all plots all nodes
            gate plots only gates and POs, no PI, FB
            output plots only outputs
        """
        if select not in ["gate", "all", "output"]:
            raise NameError("Error (ssta_plot): select arg is not valid")
        
        cmap = utils.get_cmap(20)
        plt.figure(figsize=(20,10))
        cnt = 0
        lines = ["-","--","-.",":"]
        linecycler = cycle(lines)

        for idx, node in enumerate(self.nodes_lev):
            if select == "output" and node.ntype != "PO":
                continue
            elif select == "gate" and node.ntype not in ["GATE", "PO"]:
                continue

            if isinstance(node.dd_node, NumDist):
                T, f_T = node.dd_node.pmf()
            elif isinstance(node.dd_node, Distribution):
                T, f_T = node.dd_node.pmf(samples=config.SAMPLES)
            else:
                print("Warning: a tuple distribution is found in circuit!")
                T = node.dd_node[0]
                f_T = node.dd_node[1]
            plt.plot(T, f_T, linewidth=3, color=cmap(cnt), \
                    alpha=0.5, linestyle=next(linecycler), label=node.num)
            cnt += 1
        
        plt.grid()
        plt.legend(loc=1, prop={'size': 10})
        # plt.xlim([-5,25])
        plt.savefig("{}".format(fname))
        plt.close()
        print("Circuit SSTA plot saved in {}".format(fname))
    

    def set_cell_ssta_delay(self, src="mcraw", tech=config.TECH, pvs=config.PVS):
        """ Reads Monte Carlo simulation results and generates ssta delay for cells 
        
        Parameters
        ----------
        src : str
            mcraw > raw data of MC simulations results
            mchist > Monte Carlo histogram, it can be filtered or cut before
            text > not implemented yet, txt file with distribution info 
        tech : str 
            the name of the technology, e.g. MOSFET_45nm_HP
        pvs : str
            process variation specifier, refer to CSM package
            e.g. vth0-N0.05_lg-N0.05_w-N0.10_toxe-N0.10_MC1000
        """ 
        cell_ssta_delay = dict()
        for node in self.nodes_lev:
            if node.ntype in ["PI", "FB"]: #TODO: delay of inputs and FB?
                node.cell_name = node.ntype
                continue
            
            cell_name = utils.get_node_gtype_fin(node) # gate name with fin 
            node.cell_name = cell_name
            if cell_name in cell_ssta_delay:
                continue
            
            # Store the delay distribution for this cell in circuit
            if src == "mchist":
                fname = tech + "_" + cell_name + "_" + pvs + "." + src 
                fname = os.path.join(config.SSTA_DATA_DIR, src + "/" + fname)
                print("Loading mchist file for {}: {}".format(cell_name, fname))
                T, h_T = utils.load_mchist(fname)
                h_T = utils.smooth_hist(h_T, 11) #TODO: mchist smooth hard-coded
                T, f_T = utils.hist2pmf(T, h_T)
                print("\tArea: {}".format(Distribution.area_pmf(T, f_T)))
                utils.plot_pmf(NumDist(T,f_T), fname=cell_name+".pdf")
                cell_ssta_delay[cell_name] = NumDist(T, f_T)
            
            elif src == "default":
                cell_ssta_delay[cell_name] = self.get_cell_delay(node.gtype)
            
            elif src == "mcraw":
                fname = tech + "_" + cell_name + "_" + pvs + "." + src 
                fname = os.path.join(config.SSTA_DATA_DIR, src + "/" + fname)
                print("Loading mcraw file for {}: {}".format(cell_name, fname))
                delays = utils.load_mcraw(fname)
                T, f_T = utils.mcraw2mchist(delays, 200, pad=3)
                f_T = utils.smooth_hist(f_T, window=5) 
                print("\tArea: {}".format(Distribution.area_pmf(T, f_T)))
                # utils.plot_pmf(NumDist(T,f_T), fname=cell_name+".pdf")
                cell_ssta_delay[cell_name] = NumDist(T, f_T)

            else:
                raise NameError("WRONG VALUES -- still developing")
        self.cell_ssta_delay = cell_ssta_delay
        

    def ssta_sim(self, mode, src, samples):
        """ Runs SSTA on the circuit. Currently the cell distributions are hard-coded

        Parameters
        ----------
        mode : str
            SSTA mode for statistical operations
            alt, analytical
            num, numerical 
        samples : int
            number of samples used for the numerical statistical operations

        Note: the delay of PI and FB is considered as 0
        """

        # First, what is the delay distribution of each gate? (num/alt)
        self.set_cell_ssta_delay(src, tech=config.TECH, pvs=config.PVS)
        for node in self.nodes_lev:
            if node.ntype in ["PI", "FB"]:
                node.dd_cell = 0 
            elif node.ntype in ["GATE", "PO"]:
                node.dd_cell = self.cell_ssta_delay[node.cell_name] 

        # Second, go over each gate and run a MAX-SUM simulation
        print("Node\tLevel\tMean\tSTD")
        for node in self.nodes_lev:
            t_s = time.time()
            print("Node: {}\t".format(node.num))
            if node.ntype == "PI":
                node.dd_node = 0 
            elif node.ntype == "FB":
                node.dd_node = node.unodes[0].dd_node
            elif node.ntype in ["GATE", "PO"]:
                opmax = MaxOp()
                dd_unodes = [unode.dd_node for unode in node.unodes]
                dd_max = dd_unodes[0]
                for n in range(1, len(dd_unodes)):
                    if mode == "alt":
                        dd_max = opmax.max_alt(dd_max, dd_unodes[n])
                    elif mode == "num":
                        print("\t- unode: {}".format(node.unodes[n].num))
                        dd_max = opmax.max_num(dd_max, dd_unodes[n], samples=samples, 
                            eps_error_area=0.01)
                        if dd_max != 0:
                            print("\tArea: {:.5f}".format(dd_max.area()))
                
                print("\tMAX time: {:2.4f}".format(time.time() - t_s))
                if dd_max != 0:
                    print("\tMAX Area: {:.5f}".format(dd_max.area()))
                t_s = time.time()
                opsum = SumOp()
                if mode == "alt":
                    node.dd_node = opsum.sum_alt(node.dd_cell, dd_max)
                elif mode == "num":
                    node.dd_node = opsum.sum_num(node.dd_cell, dd_max, samples=samples)
                    print("\tSUM time: {:3.4f}".format(time.time() - t_s))

                print("\tSUM Area: {:.5f}".format(node.dd_node.area()))
                utils.plot_pmf(node.dd_node, fname=self.c_name + "-" + node.num + ".pdf")

    def get_cell_delay(self):
        """ This method assigns temporary distributions to cells """ 
        cell_dg = {}
        # cell_dg["NOT"] = Normal(1, 1)
        # cell_dg["NAND"] = Normal(3, 1)
        # cell_dg["AND"] = Normal(4.2, 1)
        # cell_dg["NOR"] = Normal(3, 1)
        # cell_dg["OR"] = Normal(4.2, 1)
        # cell_dg["XOR"] = Normal(8, 1)
        # cell_dg["XNOR"] = Normal(8, 1)
        # cell_dg["BUFF"] = Normal(2, 1)
        cell_dg["NOT"] =    SkewNormal(1,   1, 10)
        cell_dg["NAND"] =   SkewNormal(4,   1, 10)
        cell_dg["AND"] =    SkewNormal(4.2, 1, 10)
        cell_dg["NOR"] =    SkewNormal(3,   1, 10)
        cell_dg["OR"] =     SkewNormal(4.2, 1, 10)
        cell_dg["XOR"] =    SkewNormal(8,   1, 10)
        cell_dg["XNOR"] =   SkewNormal(8,   1, 10)
        cell_dg["BUFF"] =   SkewNormal(2,   1, 10)
        return cell_dg


   
    
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
