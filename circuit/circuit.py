# -*- coding: utf-8 -*-

import re
import random
from enum import Enum
import math
import sys
from classdef import gtype
from classdef import ntype
from classdef import *
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import time
import pdb
from multiprocessing import Process, Pipe
import numpy as np

# Note: the node-ID in ckt is just an integer number
#TODO: one issue with ckt (2670 as example) is that some nodes are both PI and PO
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
    def __init__(self, c_name):
        ''' a digital logic circuit
        c_name:             circuit name, without .ckt extension
        nodes:              list of nodes objects
        input_num_list:     list of PI node numbers
        nodes_cnt:          total number of nodes in the circuit
        nodes_lev:          circuit information after levelization,
                            each node has level info, previous nodelist_order
        nodes_sim:          circuit information after logic simulation, each node has value
        fautl_name:         full fault list in string format
        fault_node_num:     node numbers in full fault list
        '''
        #TODO: we need a list of PI nodes
        #TODO: we need a list of PO nodes


        # self.nodes = []           # has been changed to a dict
        # self.input_num_list = []    # redundant
        # self.nodes_cnt = None       # redundant
        self.nodes_sim = None
        self.fault_name = []
        self.fault_node_num = []
        self.fault_type = [] # fault type for each node in fault list, (stuck at)1 or (stuck at)0
        self.d_coverage = None
        self.pd_coverage = None
        self.fd_data = None
        self.d_correctness_rate = None
        self.pd_correctness_rate = None
        self.pass_cnt = 0
        self.input_cnt = None
        self.rfl_node = []
        self.rfl_ftype = []
        self.lvls_list = [] #controllability and observability
        self.node_ids = [] #for mapping random node ids to 0-len(nodes)

        # Saeed  
        self.c_name = c_name
        self.PI = [] # this should repalce input_num_list
        self.PO = [] # this should be created to have a list of outputs
        self.nodes = {}         # dict of all nodes, key is node-num
        self.nodes_lev = []     # list of all nodes, ordered by level

    
    def add_node(self, line):
        """ Create a node based on 1 line of ckt file
        does not make the unodes/dnodes connections
        """
        # possible empty lines
        if len(line) < 6:
            return 
        
        attr = [int(x) for x in line.split()]
        n_type = ntype(attr[0]).name
        g_type = gtype(attr[2]).name
        num = attr[1]
        
        if n_type == "PI" and g_type=="IPT":
            node = IPT(n_type, g_type, num)

        elif n_type == "FB" and g_type=="BRCH":
            node = BRCH(n_type, g_type, num)
        
        elif n_type == "GATE" and g_type=="BRCH":
            raise NotImplementedError()

        elif n_type == "GATE" or n_type == "PO":
            if g_type == 'XOR':
                node = XOR(n_type, g_type, num)

            elif g_type == 'OR':
                node = OR(n_type, g_type, num)

            elif g_type == 'NOR':
                node = NOR(n_type, g_type, num)

            elif g_type == 'NOT':
                node = NOR(n_type, g_type, num)

            elif g_type == 'NAND':
                node = NAND(n_type, g_type, num)

            elif g_type == 'AND':
                node = AND(n_type, g_type, num)

        node.ntype = n_type
        node.gtype = g_type
        if node.ntype == "PI":
            self.PI.append(node)

        elif node.ntype == "PO":
            self.PO.append(node)
        return node 

    
    def connect_node(self, line):
        # As we move forward, find the upnodes and connects them
        
        attr = [int(x) for x in line.split()]
        ptr = self.nodes[attr[1]]
        
        # ntype=PI and gtype=IPT: good
        # we don't care about #fan-out
        if ptr.ntype == "PI" and ptr.gtype=="IPT":
            None
        
        # ntype=FB and gtyep=BRCH
        elif ptr.ntype == "FB" and ptr.gtype=="BRCH":
            unode = self.nodes[attr[3]]
            ptr.unodes.append(unode)
            unode.dnodes.append(ptr)
        
        # ntype=GATE and gtype=BRCH
        elif ptr.ntype == "GATE" and ptr.gtype=="BRCH":
            print("ERROR: gate and branch", ptr.num)

        # ntype=GATE or ntype=PO 
        # we don't care about #fan-out
        # some gates have a single input, they are buffer
        elif ptr.ntype == "GATE" or ptr.ntype == "PO":
            for unode_num in attr[5:]:
                unode = self.nodes[unode_num]
                ptr.unodes.append(unode)
                unode.dnodes.append(ptr)
        else:
            print("ERROR: not known!", ptr.num)

    
    def read_verilog(self):
        raise NameError("Not implemented yet, DFT team is responsible")

    def read_ckt(self):
        """
        Read circuit from .ckt file, each node as an object
        """
        path = "../data/ckt/{}.ckt".format(self.c_name)
        infile = open(path, 'r')
        lines = infile.readlines()
        self.nodes= {}

        # First time over the netlist
        for line in lines:
            new_node = self.add_node(line.strip())
            self.nodes[new_node.num] = new_node
            
        for line in lines:
            self.connect_node(line.strip())
                    
    
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
                    else:
                        node.lev = max(lev_u) + 1
                        flag_change = True
    
        self.nodes_lev = sorted(list(self.nodes.values()), key=lambda x:x.lev)
    

    def __str__(self):
        res = ["Circuit name: " + self.c_name]
        res.append("#Nodes: " + str(len(self.nodes)))
        res.append("#PI: " + str(len(self.PI)))
        res.append("#PP: " + str(len(self.PO)))

        for num, node in self.nodes.items():
            res.append(str(node))
        return "\n".join(res)
    

    def get_random_input_pattern(self):
        """
        Randomly generate a test pattern for input nodes.
        Could be used to check the validity of logic simulation
        and deductive fault simulation.
        """
        rand_input_val_list = []
        for i in range(len(self.input_num_list)):
            rand_input_val_list.append(random.randint(0,1))
        return rand_input_val_list
    
    def gen_test_pattern_file(self, test_count, fname=None, mode="b"):
        """ create single file with multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        """ 
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")
        fn = "./" + self.c_name + "_" + str(test_count) + "_tp_" + mode + ".txt"
        fname = fn if fname==None else fname
        infile = open(fname, 'w')
        infile.write(",".join([str(node.num) for node in self.PI]) + "\n")
        
        for t in range(test_count):
            if mode == "b":
                pat = [str(random.randint(0,1)) for x in range(len(self.PI))]
            elif mode == "x":
                pat = [str(random.randint(0,2)) for x in range(len(self.PI))]
                pat = ["X" if x=="2" else x for x in pat]
            print(",".join(pat))
            infile.write(",".join(pat) + "\n")
        
        infile.close()


    def read_PO(self):
        res = {}
        for node in self.PO:
            res["out" + str(node.num)] = node.value
        return res


    def logic_sim(self, input_val_list):
        """
        Logic simulation:
        Reads a given pattern and perform the logic simulation
        Currently just works with binary logic
        """
        node_dict = dict(zip([x.num for x in self.PI], input_val_list))

        for node in self.nodes_lev:
            if node.gtype == "IPT":
                node.imply(node_dict[node.num])
            else:
                node.imply()


    def golden_test(self, golden_io_filename):
        infile = open(golden_io_filename, "r")
        lines = infile.readlines()
        PI_t_order  = [int(x[1:]) for x in lines[0][8:].strip().split(',')]
        PO_t_order = [int(x[1:]) for x in lines[1][8:].strip().split(',')]
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
    
    
    def co_ob_info(self):
        print("\t".join(self.nodes_lev[0].print_info(get_labels=True)))
        for node in self.nodes_lev:
            node.print_info(print_labels=False)


    def SCOAP_CC(self):
        for node in self.nodes_lev:
            node.eval_CC()
    

    def SCOAP_CO(self):

        for node in self.PO:
            node.CO = 0

        for node in reversed(self.nodes_lev):
            node.eval_CO()


    ## TODO: What about inverter?
    def STAFAN_CS(self, num_pattern, limit=None, detect=False):
        ''' note:
        we are generating random numbers with replacement
        if u need to test all the patterns, add a new flag
        initial test showed when 10**7 in 4G patterns, 16M replacements
        random.choice is very inefficient
        '''
        limit = [0, pow(2, len(self.PI))-1] if limit==None else limit
        # patterns = np.random.choice(limit[1]-limit[0], num_pattern, replace=False)
        # patterns = [x+limit[0] for x in patterns]

        # for pattern in patterns:
        for t in range(num_pattern):
            b = ('{:0%db}'%len(self.PI)).format(randint(limit[0], limit[1]))
            test = [int(b[j]) for j in range(len(self.PI))]
            self.logic_sim(test)

            for node in self.nodes_lev:

                # counting values
                node.one_count = node.one_count + 1 if node.value == 1 else node.one_count
                node.zero_count = node.zero_count + 1 if node.value ==0 else node.zero_count

                # sensitization
                if node.is_sensible():
                    node.sen_count += 1

            for node in reversed(self.nodes_lev):
                node.sense = node.is_sensible()
                node.is_detectable()

        # calculate percentage/prob
        for node in self.nodes_lev:
            node.C1 = node.one_count / num_pattern
            node.C0 = node.zero_count / num_pattern
            node.S = node.sen_count / num_pattern
            node.D0_p = node.D0_count / num_pattern
            node.D1_p = node.D1_count / num_pattern


    def STAFAN_B(self):
        # TODO: comment and also the issue of if C1==1
        # calculate observability
        for node in self.PO:
            node.B1 = 1.0
            node.B0 = 1.0
        
        for node in reversed(self.nodes_lev):
            node.stafan_b()
 

    def dfs(self):
        """
        Deductive fault simulation:
        For a given test pattern,
        DFS simulates a set of faults detected by the test pattern.
        Validate the test pattern return by D or Podem
        """
        control = {'AND':0, 'NAND':0, 'OR':1, 'NOR':1}
        c_list = []
        nc_list = []
        fault_list = set()
        for item in self.nodes_sim:
            if item.gtype == 'IPT':
                item.add_faultlist((item.num, GNOT(item.value)))
                # print(item.num, item.faultlist_dfs)
            elif item.gtype == 'BRCH':
                item.faultlist_dfs = item.unodes[0].faultlist_dfs.copy()
                item.add_faultlist((item.num, GNOT(item.value)))
            elif item.gtype == 'XOR':
                s = set()
                for i in item.unodes:
                    s = s.symmetric_difference(set(i.faultlist_dfs))
                s.add((item.num, GNOT(item.value)))
                item.faultlist_dfs = list(s)
                if item.ntype == 'PO':
                    fault_list = fault_list.union(set(item.faultlist_dfs))
            elif item.gtype == 'NOT':
                item.faultlist_dfs = item.unodes[0].faultlist_dfs.copy()
                item.add_faultlist((item.num, GNOT(item.value)))
                if item.ntype == 'PO':
                    fault_list = fault_list.union(set(item.faultlist_dfs))
            else :  #gtype = gate beside xor
                flag = 0
                # find if input has control value
                for i in item.unodes:
                    c = control[item.gtype]
                    # print(item.num,i.num)
                    if i.value == c:
                        flag = 1
                        c_list.append(i)
                    else :
                        nc_list.append(i)
                # all input is no controlling value
                if flag == 0:
                    s = set()
                    for j in nc_list:
                        s = s.union(set(j.faultlist_dfs))
                    item.faultlist_dfs.clear()
                    item.faultlist_dfs = list(s)
                    item.add_faultlist((item.num, GNOT(item.value)))
                # input has control value
                else :
                    s_control = set(c_list[0].faultlist_dfs)
                    for j in c_list:
                        s_control = s_control.intersection(set(j.faultlist_dfs))
                    if nc_list == []:
                        s_ncontrol = set()
                    else:
                        s_ncontrol = set(nc_list[0].faultlist_dfs)
                        for j in nc_list:
                            s_ncontrol = s_ncontrol.union(set(j.faultlist_dfs))
                    s_control.difference(s_ncontrol)
                    item.faultlist_dfs.clear()
                    item.faultlist_dfs = list(s_control)
                    item.add_faultlist((item.num, GNOT(item.value)))
                c_list.clear()
                nc_list.clear()
                if item.ntype == 'PO':
                    fault_list = fault_list.union(set(item.faultlist_dfs))

        return fault_list


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



    def pfs(self,input_val):
        """
        Parallel Fault Simulation:
        For a given test pattern,
        PFS simulates a set of faults detected by the test pattern.
        """
        faultnum = len(self.fault_node_num)
        n = sys.maxsize
        bitlen = int(math.log2(n))+1

        output_num = list()
        for i in self.nodes_lev:
            if i.ntype == 'PO':
                output_num.append(i.num)

        node_num = []
        node_val = []

        node_num = self.input_num_list
        node_val = input_val
        # hash map
        node_input_dict = dict(zip(node_num, node_val))

        # hash map: node_num is key, object of node is value
        node_all_num = list()
        for i in self.nodes_lev:
            node_all_num.append(i.num)
        node_dict = dict(zip(node_all_num, self.nodes_lev))
        for i in range(len(node_all_num)):
            node_dict[node_all_num[i]].parallel_value = 0

        # cal iter
        if faultnum % (bitlen-1) == 0:
            iter = int(faultnum / (bitlen - 1))
        else:
            iter = int(faultnum / (bitlen - 1))+1
        #print("the value of iter: %d"%(iter))

        # write result
        detected_node = []
        detected_node_value = []

        output_empty = 0
        pfs_fault_val = []
        pfs_fault_num = []
        for n in self.fault_node_num:
            pfs_fault_num.append(n)
        for t in self.fault_type:
            pfs_fault_val.append(t)
        while (iter != 0):
            fault_num = []
            fault_val = []
            for i in self.nodes_lev:
                i.sa0 = 0
                i.sa1 = 0
            read_fault_ind = 0
        #print("begin to while")

            # save bitlen -1 fault
            while(1):
                content1 = len(pfs_fault_num)
                if content1==0:
                    break

                fault_val.append(pfs_fault_val.pop())
                fault_num.append(pfs_fault_num.pop())


                read_fault_ind = read_fault_ind + 1
                if read_fault_ind == bitlen - 1:
                    break
            for i in range(len(fault_num)):
                if fault_val[i] == 1:
                    node_dict[fault_num[i]
                            ].sa1 = node_dict[fault_num[i]].sa1 + 2**(i+1)
                else:
                    node_dict[fault_num[i]
                            ].sa0 = node_dict[fault_num[i]].sa0 + 2**(i+1)

            for i in self.nodes_lev:
                if i.gtype == 'IPT':
                    if i.num in node_num:
                        i.parallel_value = 0
                        for j in range(bitlen):
                            i.parallel_value = i.parallel_value + \
                                (int(node_input_dict[i.num]) << j)
                        i.parallel_value = ((~i.sa0) & i.parallel_value) | i.sa1
                elif i.gtype == 'BRCH':
                    i.parallel_value = ((~i.sa0) & (
                        i.unodes[0].parallel_value)) | i.sa1

                elif i.gtype == 'XOR':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value ^ i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & temp_value) | i.sa1
                elif i.gtype == 'OR':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value | i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & temp_value) | i.sa1
                elif i.gtype == 'NOR':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value | i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & (~temp_value)) | i.sa1
                elif i.gtype == 'NOT':
                    i.parallel_value = ((~i.sa0) & (
                        ~i.unodes[0].parallel_value)) | i.sa1
                elif i.gtype == 'NAND':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value & i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & (~temp_value)) | i.sa1
                elif i.gtype == 'AND':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value & i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & temp_value) | i.sa1
            iter -= 1

            for i in range(read_fault_ind):
                for j in output_num:
                    temp = node_dict[j].parallel_value
                    # t0 is to choose the value responding to the specific fault node in output
                    # t1 is to move the value to most significant bit
                    t0 = (temp & (1 << (i+1)))
                    t1 = t0 << (bitlen-i-2)
                    t2 = 1 << (bitlen-1)
                    t3 = t1 & t2
                    # t4 is to calculate most least bit which is fault free bit
                    t4 = (temp & 1) << (bitlen-1)
                    if t3 != t4:
                        if fault_num[i] not in detected_node:
                            detected_node.append(fault_num[i])
                            detected_node_value.append(fault_val[i])
                            # print(j,fault_num[i],fault_val[i])
            # output is a set of tuple
            if output_empty == 0:
                output = {(detected_node[0], detected_node_value[0])}
                output_empty += 1
            for i in range(len(detected_node)):
                output.add((detected_node[i], detected_node_value[i]))

        return output


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
        total_pattern = pow(2, self.input_cnt)
        pattern_per_thread = int(total_pattern / thread_cnt)

        for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
            #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
            b = ('{:0%db}'%self.input_cnt).format(i)
            list_to_pfs = []
            for j in range(self.input_cnt):
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
            for i in range(self.input_cnt):
                if (i < self.input_cnt - 1):
                    fo.write('%d->' % self.input_num_list[i])
                else:
                    fo.write('%d' % self.input_num_list[i])
            fo.write(' as sequence of inputs')
            fo.write('\n')
            fo.write('input_patterns\t\t\tdetected_faults\n')
            for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
                b = ('{:0%db}'%self.input_cnt).format(i)
                fo.write('%s\t\t\t\t' % b)
                for i in range(len(fault_dict.get(b))):
                    fo.write('%-5s ' % fault_dict.get(b)[i])#format ok?
                fo.write('\n')
        print("thread #{} of {} threads finished".format(idx, thread_cnt))

    def get_reduced_fault_list(self):
        """
        Using checkpoint theorem,
        generate reduced fault list
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

    #to be continued
    def equvalenceAndDominance(self):
        return

    def D_alg(self, fault_index, imply_counter):
        """
        Given a fault, returns whether it can be detected,
        if can, returns a test pattern.
        """
        res = D_alg(self.nodes, fault_index, imply_counter)
        return res
    #to be continued
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
        self.d_correctness_rate = ((len(self.fault_node_num) - d_error_cnt) / len(self.fault_node_num)) * 100
        print ("D algorithm correctness rate: {}%".format(self.d_correctness_rate))

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
        self.d_coverage = (self.pass_cnt / len(self.fault_node_num)) * 100
        print ("D algorithm fault coverage: {}".format(self.d_coverage))
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
                    print("Podem algorithm Error at fault {}, type SUCCESS".format(self.fault_name[i]))
                    pd_error_cnt += 1
                else:
                    pass
            else:
                # print("Podem_alg FAILURE")
                error_not_found = self.check_failure(self.fault_name[i])
                if error_not_found == 0:
                    print("Podem algorithm Error at fault {}, type FAILURE".format(self.fault_name[i]))
                    pd_error_cnt += 1
                else:
                    pass
        self.pd_correctness_rate = ((len(self.fault_node_num) - pd_error_cnt) / len(self.fault_node_num)) * 100
        print ("Podem algorithm correctness rate: {}%".format(self.pd_correctness_rate))

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
        self.pd_coverage = self.pass_cnt / len(self.fault_node_num) * 100
        self.pass_cnt = 0
        print ("Podem algorithm fault coverage: {}%".format(self.pd_coverage))


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


            

    


    def control_thread(self, conn, c_name, i, total_T,num_proc):
        circuit = Circuit(c_name)
        circuit.read_circuit()
        circuit.lev()
        inputnum = len(circuit.input_num_list)
        circuit.STAFAN_CS(int(total_T/num_proc), [int(pow(2, inputnum)/num_proc)*i,int(pow(2, inputnum)/num_proc)*(i+1)-1])
        circuit.nodes_lev.sort(key=lambda x: x.num)
        one_count_list = []
        zero_count_list = []
        sen_count_list = []
        D0_count = []
        D1_count = []
        for i in circuit.nodes_lev:
            one_count_list.append(i.one_count)
            zero_count_list.append(i.zero_count)
            sen_count_list.append(i.sen_count)
            D0_count.append(i.D0_count)
            D1_count.append(i.D1_count)
        circuit.nodes_lev.sort(key=lambda x: x.lev)
        conn.send((one_count_list, zero_count_list, sen_count_list, D0_count, D1_count))
        conn.close()


    def STAFAN(self, total_T, num_proc=1):
        start_time = time.time()
        # thread_cnt = 1
        process_list = []
        for i in range(num_proc):
        # for idx in process_list:
            parent_conn, child_conn = Pipe()
            p = Process(target = self.control_thread, args =(child_conn, self.c_name, i, total_T,num_proc, ))
            p.start()
            process_list.append((p, parent_conn))

        one_count_list = [0] * self.nodes_cnt
        zero_count_list = [0] * self.nodes_cnt
        sen_count_list = [0] * self.nodes_cnt
        D1_count_list = [0] * self.nodes_cnt
        D0_count_list = [0] * self.nodes_cnt

        for p, conn in process_list:
            tup = conn.recv()
            for i in range(len(tup[0])):
                one_count_list[i] += tup[0][i]
                zero_count_list[i] += tup[1][i]
                sen_count_list[i] += tup[2][i]
                D0_count_list[i] += tup[3][i]
                D1_count_list[i] += tup[4][i]
            p.join()
        self.nodes_lev.sort(key=lambda x: x.num)
        for i in range(len(self.nodes_lev)):
            self.nodes_lev[i].C1 = one_count_list[i] / total_T
            self.nodes_lev[i].C0 = zero_count_list[i] / total_T
            self.nodes_lev[i].S = sen_count_list[i] / total_T
            self.nodes_lev[i].D0_count = D0_count_list[i]
            self.nodes_lev[i].D1_count = D1_count_list[i]
            self.nodes_lev[i].D0_p = D0_count_list[i] / total_T
            self.nodes_lev[i].D1_p = D1_count_list[i] / total_T

        #print (self.nodes_lev[i].num, self.nodes_lev[i].one_control, self.nodes_lev[i].zero_control,self.nodes_lev[i].sen_p)
        self.nodes_lev.sort(key=lambda x: x.lev)
        self.STAFAN_B()
        end_time = time.time()
        duration = end_time - start_time
        print ("Processor count: {}, Time taken: {:.2f} sec".format(num_proc, duration))


    def gen_graph(self):
        """
        Generate directed graph of the circuit, each node has attributes: CC0, CC1, CO, lev
        """
        G = nx.DiGraph()
        for n in self.nodes_lev:
            n_num_normal = self.node_ids.index(n.num) #TODO: efficient search using dict
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
            G.nodes[n_num_normal]['D0_p'] = n.D0_p
            G.nodes[n_num_normal]['D1_p'] = n.D1_p
            G.nodes[n_num_normal]['D_p'] = n.D0_p + n.D1_p
            if n.gtype != 'IPT':
                for unode in n.unodes:
                    G.add_edge(self.node_ids.index(unode.num), n_num_normal)
            else:
                pass
        return G

    def get_node_attr(self, node_attr):
        data = []
        for node in self.nodes_lev:
            data.append(getattr(node, node_attr))

        return data

    def get_hist(self, node_attr, plot=False, fname=None):
        plt.clf()
        data = self.get_node_attr(node_attr)
        res = plt.hist(data)
        plt.title(self.c_name)
        plt.xlabel(node_attr)
        plt.ylabel("Occurrence")
        if plot:
            plt.show()
        else:
            fname = self.c_name + "_" + node_attr + ".png" if fname==None else fname
            plt.savefig(fname)

# prevent D algorithm deadlock. For debug purposes only
class Imply_counter:
    def __init__(self, abort_cnt):
        self.cnt = 0
        self.abort_cnt = abort_cnt
    def increment(self):
        self.cnt += 1
    def initialize(self):
        self.cnt = 0


