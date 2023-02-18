# ---> methods that appears here must be removed from node.py

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
from circuit import circuit
from node import testnode

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


class TestCircuit(circuit.Circuit):
    """ 
        An extended version of Circuit(), which is capable of SCOAP, STAFAN, PPSF, PFS

        Attributes
        ---------
        STD_NODE_LIB : dict
            dictionary of node type to related node class
        fault_name : 
            full fault list in string format
        fault_node_num : 
            node numbers in full fault list
        """

    STD_NODE_LIB = {'AND':testnode.TestAND, 
                    'XOR':testnode.TestXOR,
                    'OR': testnode.TestOR, 
                    'XNOR':testnode.TestXNOR,
                    'BUFF':testnode.TestBUFF,
                    'BRCH':testnode.TestBRCH,
                    'NOR':testnode.TestNOR,
                    'NAND':testnode.TestNAND,
                    'NOT':testnode.TestNOT,
                    'IPT':testnode.TestIPT}

    def __init__(self, netlist_fname):
        super().__init__(netlist_fname, TestCircuit.STD_NODE_LIB)
    
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
                # b = (f'{random.randint(limit[0], limit[1]):0%db}'%len(self.PI))
                b = ('{:0%db}'%len(self.PI)).format(random.randint(limit[0], limit[1]))
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
    
    def STAFAN_ctrl_process(self, conn, id_proc, tot_tp_count, tot_proc):
        # circuit = TestCircuit(self.c_fname)
        # circuit.lev()
        circuit=self
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
        Calculating STAFAN controllability and observability in parallel. 
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
                    print(f"Warning: node {node.num} controllability is zero")
        try: 
            self.STAFAN_B()
        except ZeroDivisionError:
            print("Node Ctrl is zero")
            pdb.set_trace()
        
        end_time = time.time()
        duration = end_time - start_time
        if verbose:
            print (f"Processor count: {num_proc}, TP-count: {total_tp}, Time: {duration:.2f} sec")
    
    def save_TMs(self, fname=None, tp=None): # Better to be called in STAFAN / change name
        if fname == None:
            path = config.STAFAN_DIR+"/"+self.c_name
            if not os.path.exists(path):
                os.mkdir(path)
            fname = os.path.join(path, self.c_name)
            if not os.path.exists(fname):
                os.mkdir(fname)
            fname = os.path.join(fname, f"{self.c_name}-TP{tp}.stafan")

        outfile = open(fname, "w")
        outfile.write("Node,C0,C1,B0,B1,S\n")
        for node in self.nodes_lev:
            ss = [f"{x:e}" for x in [node.C0, node.C1, node.B0, node.B1, node.S]]
            outfile.write(",".join([node.num] + ss) + "\n")
        outfile.close()
        print(f"Saved circuit STAFAN TMs in {fname}")

    def load_TMs(self, fname): # change name
        lines = open(fname).readlines()[1:]
        for line in lines:
            words = line.strip().split(",")
            node = self.nodes[words[0]]
            node.C0 = float(words[1])  
            node.C1 = float(words[2]) 
            node.B0 = float(words[3]) 
            node.B1 = float(words[4]) 
            node.S  = float(words[5]) 

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
            if None in [node.C0,node.C1,node.B0,node.B1]:
                raise "STAFAN is not calculated or loaded completely. First, call STAFAN() or load_TMs()"
            nfc += math.exp(-1 * node.C1 * node.B1 * tp_count) 
            nfc += math.exp(-1 * node.C0 * node.B0 * tp_count) 
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
            print ('{:05b}'.format(i)) #str type output #Suit different input numbers!!!!
            # b = (f'{i:0%db}'%inputnum)
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

        fault_dict_result = open(f"../fault_dic/{self.c_name}.fd", "w")
        for i in range(len(self.input_num_list)):
            if (i<len(self.input_num_list)-1):
                fault_dict_result.write('%d->' % self.input_num_list[i])
            else:
                fault_dict_result.write('%d' % self.input_num_list[i])

        fault_dict_result.write(' as sequence of inputs')
        fault_dict_result.write('\n')
        fault_dict_result.write('tps\t\t\tdetected_faults\n')
        for i in range(total_pattern):
            print ('{:05b}'.format(i)) #str type output #Suit different input numbers!!!!
            # b = (f'{i:0%db}'%inputnum)
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
            print ('{:05b}'.format(i)) #str type output #Suit different input numbers!!!!
            # b = (f'{i:0%db}'%len(self.PI))
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

        with open (f"../fault_dic/{self.c_name}_{idx}.fd", "w") as fo:
            for i in range(len(self.PI)):
                if (i < len(self.PI) - 1):
                    fo.write('%d->' % self.input_num_list[i])
                else:
                    fo.write('%d' % self.input_num_list[i])
            fo.write(' as sequence of inputs')
            fo.write('\n')
            fo.write('tps\t\t\tdetected_faults\n')
            for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
                b = (f'{i:0%db}'%len(self.PI))
                fo.write('%s\t\t\t\t' % b)
                for i in range(len(fault_dict.get(b))):
                    fo.write('%-5s ' % fault_dict.get(b)[i])#format ok?
                fo.write('\n')
        print(f"thread #{idx} of {thread_cnt} threads finished")
    
    def read_fault_dict(self):
        """read already generated fault dictionary"""
        fd = open(f"../fault_dic/{self.c_name}.fd","r")
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