# -*- coding: utf-8 -*-

import re
import random
from enum import Enum
import math
import sys
from node import gtype
from node import ntype
from node import *
# import networkx as nx
# import matplotlib.pyplot as plt

from random import randint
import time
import pdb
from multiprocessing import Process, Pipe
#import numpy as np
import os

import config
#import xlwt
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
        
        # Saeed confirms using these attributes
        self.c_name = c_name
        self.nodes = {}     # dict of all nodes, key is now string node-num
        self.nodes_lev = [] # list of all nodes, ordered by level
        self.PI = [] # this should repalce input_num_list
        self.PO = [] # this should be created to have a list of outputs
        
        # Saeed does not confirm using these attributes
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


        #pfs:
        self.in_fault_node_num = [] # input fault num, string format
        self.in_fault_node_type = [] # input fault type, integer format
        
    
    def add_node(self, line):
        """ Create a node based on 1 line of ckt file
        does not make the unodes/dnodes connections
        """
        # possible empty lines
        if len(line) < 6:
            return 
        
        attr = line.split()
        n_type = ntype(int(attr[0])).name
        g_type = gtype(int(attr[2])).name
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


    def connect_node(self, line):
        # As we move forward, find the upnodes and connects them
        
        attr = line.split()
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

    
    ## Inputs: Verilog gate input formats
    ## Outputs: gtype corresponding gate name
    def gtype_translator(self, gate_type):
        if gate_type == 'ipt':
            return gtype(0).name
        elif gate_type == 'xor':
            return gtype(2).name
        elif gate_type == 'or':
            return gtype(3).name
        elif gate_type == 'nor':
            return gtype(4).name
        elif gate_type == 'not':
            return gtype(5).name
        elif gate_type == 'nand':
            return gtype(6).name
        elif gate_type == 'and':
            return gtype(7).name
        ## new node type
        elif gate_type == 'xnor':
            return gtype(8).name
        elif gate_type == 'buf':
            return gtype(9).name


    ## This function is used for inserting the BRCH node
    ## u_node and d_node are connected originally
    ## i_node is the node be inserted between u_node and d_node
    def insert_node(self, u_node, d_node, i_node):
        u_node.dnodes.remove(d_node)
        u_node.dnodes.append(i_node)
        d_node.unodes.remove(u_node)
        d_node.unodes.append(i_node)
        i_node.unodes.append(u_node)
        i_node.dnodes.append(d_node)

    ## According to the Dict, this function will return the specific node
    ## It is similar to part of add_node()
    def node_generation(self, Dict):
        if Dict['n_type'] == "PI" and Dict['g_type'] == "IPT":
            node = IPT(Dict['n_type'], Dict['g_type'], Dict['num'])

        elif Dict['n_type'] == "FB" and Dict['g_type'] == "BRCH":
            node = BRCH(Dict['n_type'], Dict['g_type'], Dict['num'])

        elif Dict['n_type'] == "GATE" and Dict['g_type'] == "BRCH":
            raise NotImplementedError()

        elif Dict['n_type'] == "GATE" or Dict['n_type'] == "PO":
            if Dict['g_type'] == 'XOR':
                node = XOR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'OR':
                node = OR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NOR':
                node = NOR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NOT':
                node = NOR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NAND':
                node = NAND(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'AND':
                node = AND(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'BUFF':
                node = BUFF(Dict['n_type'], Dict['g_type'], Dict['num'])

            # elif Dict['g_type'] == 'XNOR':
            #     node = XNOR(Dict['n_type'], Dict['g_type'], Dict['num'])
        else:
            raise NotImplementedError()
        return node

    def read_verilog(self):
        """
        Read circuit from .v file, each node as an object
        """
        path = "../data/verilog/{}.v".format(self.c_name)

        ## Read the file and Deal with comment and ; issues
        infile = open(path, 'r')
        eff_line = ''
        lines = infile.readlines()
        new_lines=[]
        for line in lines:
            # eliminate comment first
            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            if line_syntax:
                line = line[:line.index('//')]

            # considering ';' issues
            if ';' not in line and 'endmodule' not in line:
                eff_line = eff_line + line.rstrip()
                continue
            line = eff_line + line.rstrip()
            eff_line = ''
            new_lines.append(line)
        infile.close()

        ## 1st time Parsing: Creating all nodes
        # Because the ntype and gtype information are separate, we need to use Dict to collect all information
        # Key: num
        # Value: num, ntype and gtype
        Dict = {}
        for line in new_lines:
            if line != "":
                # Wire
                line_syntax = re.match(r'^[\s]*wire (.*,*);', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(1).replace(' ', '').replace('\t', '').split(','):
                        Dict[n[1:]] = {'num': n[1:], 'n_type':ntype(0).name, 'g_type':None}

                # PI: n_type = 0 g_type = 0
                line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                        new_node = self.node_generation({'num': n[1:], 'n_type': ntype(1).name, 'g_type': self.gtype_translator('ipt')})
                        self.nodes[new_node.num] = new_node
                        self.PI.append(new_node)

                # PO n_type = 3 but g_type has an issue
                line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                        Dict[n[1:]] = {'num': n[1:], 'n_type': ntype(3).name, 'g_type': None}

                # Gate reading and Making Connection of nodes
                line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
                if line_syntax:
                    if line_syntax.group(1) != 'module':
                        node_order = line_syntax.group(3).replace(' ', '').split(',')
                        # Nodes Generation
                        Dict[node_order[0][1:]]['g_type'] = self.gtype_translator(line_syntax.group(1))
                        new_node = self.node_generation(Dict[node_order[0][1:]])
                        self.nodes[new_node.num] = new_node
                        if new_node.ntype == 'PO':
                            self.PO.append(new_node)

        # 2nd time Parsing: Making All Connections
        for line in new_lines:
            if line != "":
                line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
                if line_syntax:
                    if line_syntax.group(1) != 'module':
                        node_order = line_syntax.group(3).replace(' ', '').split(',')
                        for i in range(1, len(node_order)):
                            # Making connections
                            self.nodes[node_order[0][1:]].unodes.append(self.nodes[node_order[i][1:]])
                            self.nodes[node_order[i][1:]].dnodes.append(self.nodes[node_order[0][1:]])

        ###### Branch Generation ######
        # The basic way is looking for those nodes with more-than-1 fan-out nodes
        # Creating a new FB node
        # Inserting FB node back into the circuit
        # We cannot change the dictionary size while in its for loop,
        # so we create a new dictionary and integrate it back to nodes at the end
        B_Dict = {}
        for node in self.nodes.values():
            if len(node.dnodes) > 1:
                for index in range(len(node.dnodes)):
                    ## New BNCH
                    FB_node = self.node_generation({'num': node.num + '-' + str(index+1), 'n_type':ntype(2).name, 'g_type':gtype(1).name})
                    B_Dict[FB_node.num] = FB_node
                    self.insert_node(node, node.dnodes[0], FB_node)
        self.nodes.update(B_Dict)

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
        res.append("#PI: " + str(len(self.PI)) + " >> ")
        res.append(str([x.num for x in self.PI]))
        res.append("#PO: " + str(len(self.PO)) + " >> ")
        res.append(str([x.num for x in self.PO]))

        # for num, node in self.nodes.items():
        #     res.append(str(node))
        return "\n".join(res)
    

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
            # print(",".join(pat))
            infile.write(",".join(pat) + "\n")
        
        infile.close()

                

    def read_PO(self):
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

    
    def logic_sim_file(self, in_fname, out_fname, stil=False): 
        """
        This method does the logic simulation in our platform
        First: generate a output folder in ../data/modelsim/circuit_name/ directory
        Second: read a input file in input folder
        Third: generate a output file in output folder by using logic_sim() function
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


    def STAFAN_reset_counts(self):
        for node in self.nodes_lev:
            node.one_count = 0
            node.zero_count = 0
            node.D1_count = 0
            node.D0_count = 0
            node.sen_count = 0


    def STAFAN_reset_flags(self):
        for node in self.nodes_lev:
            node.sense = False
            node.D1 = False
            node.D0 = False
    
    
    ## TODO: What about inverter?
    def STAFAN_CS(self, num_pattern, limit=None, detect=False):
        ''' note:
        we are generating random numbers with replacement
        if u need to test all the patterns, add a new flag
        initial test showed when 10**7 in 4G patterns, 16M replacements
        random.choice is very inefficient
        '''
        
        # We need to resent the circuit
        self.STAFAN_reset_counts()
        
        limit = [0, pow(2, len(self.PI))-1] if limit==None else limit
        for t in range(num_pattern):
            b = ('{:0%db}'%len(self.PI)).format(randint(limit[0], limit[1]))
            test = [int(b[j]) for j in range(len(self.PI))]
            
            self.logic_sim(test)
            self.STAFAN_reset_flags()
            
            for node in self.nodes_lev:
                node.one_count = node.one_count + 1 if node.value == 1 else node.one_count
                node.zero_count = node.zero_count + 1 if node.value ==0 else node.zero_count

                # sensitization
                if node.is_sensible():
                    node.sense = True
                    node.sen_count += 1

            for node in reversed(self.nodes_lev):
                node.semi_detect()

        # calculate percentage/prob
        for node in self.nodes_lev:
            node.C1 = node.one_count / num_pattern
            node.C0 = node.zero_count / num_pattern
            node.S = node.sen_count / num_pattern
            node.D0_p = node.D0_count / num_pattern
            node.D1_p = node.D1_count / num_pattern

    def TPI_stat(self, HTO_th, HTC_th):
        """ this is a simple division of nodes, 
        the element C*B can also be used. 
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

    
    """
    def experiment_1(self):
        for node in self.nodes_lev:
            node.stat{"B0_old"} = node.B0
            node.stat{"B1_old"} = node.B1
        
        for node in self.nodes_lev:
            node.ntype="PO"
            self.STAFAN_B()
            for node in self.nodes_lev = 
    """ 

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

    """
    def IMOP_1(self, node):
        # Sum of all the observations of the fan-in cone, only if lower than HTO
        # if target becomes OP, how many node pass the threshold
        if node.seen:
            return 0
        delta_B0 = node.B0 / node.stat{"B0_old"}
        delta_B1 = node.B1 / node.stat{"B1_old"}
        elif delta_B0 < 2 and delta_B1 < 2:
            # no significant change
            return 
        for node in self.nodes_lev:
            node.seen = False

    """
    
    def STAFAN_B(self):
        # TODO: comment and also the issue of if C1==1
        # calculate observability
        # for node in self.PO:
        #     print(">>", node.num)
        #     node.B1 = 1.0
        #     node.B0 = 1.0
        
        for node in reversed(self.nodes_lev):
            # with checking node==PO we can add one node in the 
            # .... middle of the circuit as PO, and stefan is still correct
            if node in self.PO:
                node.B0 = 1.0
                node.B1 = 1.0
            node.stafan_b()
            node.CB1 = node.C1 * node.B1
            node.CB0 = node.C0 * node.B0
            node.B = (node.B0*node.C0) + (node.B1*node.C1)


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
            # n_num_normal = self.node_ids.index(n.num) #TODO: efficient search using dict
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
            G.nodes[n_num_normal]['D0_p'] = n.D0_p
            G.nodes[n_num_normal]['D1_p'] = n.D1_p
            G.nodes[n_num_normal]['D_p'] = n.D0_p + n.D1_p
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


