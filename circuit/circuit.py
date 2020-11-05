# -*- coding: utf-8 -*-

import re
import random
from enum import Enum
import math
import sys
# import networkx as nx
# import matplotlib.pyplot as plt
from random import randint
import time
import pdb
from multiprocessing import Process, Pipe
import numpy as np
import os

import config
from node import gtype
from node import ntype
from node import *


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

            elif g_type == "XNOR":
                node = XNOR(n_type, g_type, num)

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

    
    
        
    def add_node_v(self, Dict):

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
                node = NOT(Dict['n_type'], Dict['g_type'], Dict['num'])

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
        path = os.path.join(config.VERILOG_DIR, "{}.v".format(self.c_name))
        print("Reading verilog file in {}".format(path))
        infile = open(path, 'r')
        eff_line = ''
        lines = infile.readlines()
        new_lines=[]
        
        for line in lines:
            if line == "":
                continue

            # Remove comment in lines 
            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            line = line[:line.index('//')] if line_syntax else line

            # If there is no ";" or "endmodule" it means the line is continued
            # Stack the contniuous lines to each other
            if (';' not in line) and ('endmodule' not in line):
                eff_line = eff_line + line.rstrip()
                continue
                        
            line = eff_line + line.rstrip()
            eff_line = ''
            new_lines.append(line)

        infile.close()

        ## 1st time Parsing: Creating all nodes
        # we need to use _nodes dict to collect all information
        _nodes = {}
        for line in new_lines:

            x_type, nets = read_verilog_syntax(line)

            if x_type == "module":
                continue
             
            # Wire: n_type=GATE, gtype=unknown
            if x_type == "wire":
                for wire in nets:
                    _nodes[wire] = {'num':wire, 'n_type':"GATE", 'g_type':None}

            # PI: n_type=PI, g_type=IPT, Node will be added! 
            if x_type == "PI":
                for pi in nets:
                    new_node = self.add_node_v({'num': pi, 'n_type': "PI", 'g_type': "IPT"})
                    self.nodes[new_node.num] = new_node
                    self.PI.append(new_node)

            # PO: n_type=PO, g_type=unknown, Node will NOT be added
            if x_type == "PO":
                for po in nets:
                    _nodes[po] = {'num': po, 'n_type':"PO", 'g_type': None}

            # GATE, n_type = PO or GATE
            # Node was seen before, in wire or in input/output, node will be added
            if x_type == "GATE":
                gtype, nets = nets
                _nodes[nets[0]]['g_type'] = gtype 
                new_node = self.add_node_v(_nodes[nets[0]])
                self.nodes[new_node.num] = new_node
                if new_node.ntype == 'PO':
                    self.PO.append(new_node)

        # 2nd time Parsing: Making All Connections
        for line in new_lines:
            x_type, nets = read_verilog_syntax(line)
            if x_type == "GATE":
                gtype, nets = nets
                for net in nets[1:]:
                    self.nodes[nets[0]].unodes.append(self.nodes[net])
                    self.nodes[net].dnodes.append(self.nodes[nets[0]])


        # Branch modification 
        # Inserting FB node back into the circuit
        branches = {}
        for node in self.nodes.values():
            if len(node.dnodes) > 1:
                for idx, dnode in enumerate(node.dnodes):
                    ## New BNCH
                    branch = self.add_node_v({'num': node.num + '-' + str(idx+1), 
                        'n_type':"FB", 'g_type':"BRCH"})
                    branches[branch.num] = branch
                    insert_branch(node, node.dnodes[0], branch)
        self.nodes.update(branches)

        print("Loading verilog file is done")

    
    def read_ckt(self):
        """
        Read circuit from .ckt file, each node as an object
        """
        path = os.path.join(config.CKT_DIR, "{}.ckt".format(self.c_name))
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

        for node in self.nodes_lev:
            res.append(str(node))
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
            res[node.num] = node.value
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
        PI_t_order  = [x for x in lines[0][8:].strip().split(',')]
        PO_t_order = [x for x in lines[1][8:].strip().split(',')]
        # print(PI_t_order)
        PI_num = [x.num for x in self.PI]
        # print(PI_num)

        print(PO_t_order)
        PO_num = [x.num for x in self.PO]
        print(PO_num)

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
                if out_node_golden != logic_out[out_node]:
                    print("Error: PO node values do not match! ")
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
    
    #TODO: there shoul be a seed for random numbers
    # seed should be given in config file
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
   

    def control_thread(self, conn, c_name, i, total_T,num_proc):
        circuit = Circuit(c_name)
        circuit.read_circuit()
        circuit.lev()
        inputnum = len(circuit.input_num_list)
        circuit.STAFAN_CS(int(total_T/num_proc), 
                [int(pow(2, inputnum)/num_proc)*i, 
                    int(pow(2, inputnum)/num_proc)*(i+1)-1])
        
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
            p = Process(target = self.control_thread, 
                    args =(child_conn, self.c_name, i, total_T,num_proc, ))
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

        self.nodes_lev.sort(key=lambda x: x.lev)
        self.STAFAN_B()
        end_time = time.time()
        duration = end_time - start_time
        print ("Processor count: {}, Time taken: {:.2f} sec".format(num_proc, duration))

    

    def gen_graph(self):
        """
        Generate directed graph of the circuit, 
        each node has attributes: CC0, CC1, CO, lev
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

def verilog_version_gate(line):
    return {"gate type":"gate", "input-list":[], "output-list":[]}


def cell2gate(cell_name):
    ## Inputs: Verilog gate input formats
    ## Outputs: gtype corresponding gate name
    for gname, cell_names in config.CELL_NAMES.items():
        if cell_name in cell_names:
            return gname
    raise NameError("Cell type {} was not found".format(cell_name))


def insert_branch(u_node, d_node, i_node):
    """ This function is used for inserting the BRCH node
    u_node and d_node are connected originally
    i_node is the node be inserted between u_node and d_node """ 
    u_node.dnodes.remove(d_node)
    u_node.dnodes.append(i_node)
    d_node.unodes.remove(u_node)
    d_node.unodes.append(i_node)
    i_node.unodes.append(u_node)
    i_node.dnodes.append(d_node)


def read_verilog_syntax(line):
    
    
    if line.strip() == "endmodule":
        return ("module", None)

    # If there is a "wire" in this line:
    line_syntax = re.match(r'^[\s]*wire (.*,*);', line, re.IGNORECASE)
    if line_syntax:
        nets = line_syntax.group(1).replace(' ', '').replace('\t', '').split(',')
        return ("wire", nets)
     
    # PI: 
    line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
    if line_syntax:
        nets = line_syntax.group(2).replace(' ', '').replace('\t', '').split(',')
        return ("PI", nets)
    
    # PO 
    line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
    if line_syntax:
        nets = line_syntax.group(2).replace(' ', '').replace('\t', '').split(',')
        return ("PO", nets)

    # Gate
    line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
    if line_syntax:
        if line_syntax.group(1) == "module":
            return ("module", None)
        
        gtype = cell2gate(line_syntax.group(1))
        #we may not use gname for now. 
        gname = line_syntax.group(2)

        pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3))
        if pin_format:
            #TODO: for now, we considered PO as the last pin
            if "Z" not in pin_format[-1][0]:
                raise NameError("Order of pins in verilog does not match")
            nets = [pin_format[-1][1]]
            for x in pin_format[:-1]:
                nets.append(x[1])
        else:
            # verilog with no pin format
            nets = line_syntax.group(3).replace(' ', '').split(',')

        return ("GATE", (gtype, nets) )
    
    raise NameError("No suggestion for \n>{}<\n was found".format(line))


