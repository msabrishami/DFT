import math
import os
import re
import time
from collections import deque
from multiprocessing import Pipe, Process

import config
from node import dft_node
from tp_generator import TPGenerator

from circuit import circuit

class DFTCircuit(circuit.Circuit):
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

    STD_NODE_LIB = {'AND':dft_node.DFTAND, 
                    'XOR':dft_node.DFTXOR,
                    'OR': dft_node.DFTOR, 
                    'XNOR':dft_node.DFTXNOR,
                    'BUFF':dft_node.DFTBUFF,
                    'BRCH':dft_node.DFTBRCH,
                    'NOR':dft_node.DFTNOR,
                    'NAND':dft_node.DFTNAND,
                    'NOT':dft_node.DFTNOT,
                    'IPT':dft_node.DFTIPT}

    def __init__(self, netlist_fname):
        super().__init__(netlist_fname, DFTCircuit.STD_NODE_LIB)
        self._stafan_executed = False
    
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
        tp : list 
            a single test pattern vector 
        """
        self.logic_sim(tp)
        self.STAFAN_reset_flags()
            
        for node in self.nodes_lev:
            node.one_count = node.one_count + 1 if node.value==1 else node.one_count
            node.zero_count = node.zero_count + 1 if node.value==0 else node.zero_count

            # sensitization
            if node.is_sensible():
                node.sense = True
                node.sen_count += 1

    def STAFAN_C(self, tp, limit=None):
        """ 
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
        """

        tg = TPGenerator(self)
        tps=[]
        if isinstance(tp, str):
            tps = tg.load_file(tp)
        elif isinstance(tp, int):
            tps = tg.gen_n_random(tp)
        else:
            raise TypeError
        
        # We need to reset the circuit
        self.STAFAN_reset_counts()
        self.STAFAN_reset_flags()
        
        if limit is None:
            limit = [0, pow(2, len(self.PI))-1]

        for t in tps:
            self.STAFAN_C_single(t)

        # Calculate percentage/prob
        for node in self.nodes_lev:
            node.C1 = node.one_count / len(tps)
            node.C0 = node.zero_count / len(tps)
            node.S = node.sen_count / len(tps)

    def STAFAN_B(self):
        """ Calculates the STAFAN observability probabilities for all nodes """
        for node in reversed(self.nodes_lev):
            if node.ntype=="PO":
                node.B0 = 1.0
                node.B1 = 1.0
            node.stafan_b()
    
    def STAFAN_C_handler(self, conn, id_proc, tp_count, tot_proc):
        limit = [int(pow(2, len(self.PI))/tot_proc) * id_proc, 
                int(pow(2, len(self.PI))/tot_proc) * (id_proc+1)-1]
        
        self.STAFAN_C(tp_count, limit)

        one_count_list = []
        zero_count_list = []
        sen_count_list = []

        for i in self.nodes_lev:
            one_count_list.append(i.one_count)
            zero_count_list.append(i.zero_count)
            sen_count_list.append(i.sen_count)
        
        conn.send((one_count_list, zero_count_list, sen_count_list))
        conn.close()

    def STAFAN(self, tp_count, num_proc=1, verbose=True, save_log=True):
        """ 
        Calculating STAFAN controllability and observability in parallel. 
        Random TPs are generated within the method itself and are not stored. 
        
        Arguments:
        ---------
        total_tp : (int) total number of test pattern vectors (not less than num_proc)
        num_proc : (int) number of processors that will be used in parallel processing 
        """
        self._stafan_tp = tp_count
        if verbose:
            print(f'\nCalculating STAFAN measurements (B0, B1, C0, C1) with:' + 
                  f'on {self.c_name} for all nodes ({len(self.nodes)}) with {tp_count} tps ' + 
                  f'on {num_proc} process(es) ...')

        if tp_count < num_proc:
            raise ValueError("Total TPs should be higher than process numbers")
        
        start_time = time.time()

        process_list = []
        for id_proc in range(num_proc):
            parent_conn, child_conn = Pipe()
            p = Process(target = self.STAFAN_C_handler, 
                    args =(child_conn, id_proc, tp_count//num_proc+1 , num_proc))
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
            node.C1 = one_count_list[idx] / tp_count
            node.C0 = zero_count_list[idx] / tp_count
            node.S = sen_count_list[idx] / tp_count

        if verbose: 
            for node in self.nodes_lev:
                if node.C0 == 0 or node.C1 == 0:
                    print(f"Warning: node {node.num} controllability is zero")
        try: 
            self.STAFAN_B()
        except ZeroDivisionError:
            print("Node Ctrl is zero")
            # pdb.set_trace() --> Take an action
        
        if verbose:
            # print (f"Processor count: {num_proc}, TP-count: {total_tp}, Time: {duration:.2f} sec")
            print(f"\nCalculations finished in {time.time() - start_time:.2f} sec.")
        
        self._stafan_executed = True
        
        if save_log:
            self.save_STAFAN(tp_count)
    
    def STAFAN_FC(self, tp):
        """ Estimation of fault coverage for all faults 
        All faults include all nodes, SS@0 and SS@1 
        pd stands for probability of detection 
        """
        self._stafan_tp = tp
        if not self._stafan_executed:
            if 'y' in input('STAFAN is not calculated. Calculate it here (y/n)? '):
                tp = int(input('Enter Number of test patterns: '))
                self.STAFAN(tp)
            else:
                raise "STAFAN is not calculated or loaded completely. First, call STAFAN() or load_TMs()."

        nfc = 0
        for node in self.nodes_lev:
            if None in [node.C0,node.C1,node.B0,node.B1]:
                raise "STAFAN is not calculated or loaded completely. First, call STAFAN() or load_TMs()."
            nfc += math.exp(-1 * node.C1 * node.B1 * tp) 
            nfc += math.exp(-1 * node.C0 * node.B0 * tp) 

        return 1 - nfc/(2*len(self.nodes)) 

    def save_STAFAN(self, fname=None, verbose=True):
        if not fname:
            fname = os.path.join(config.STAFAN_DIR, self.c_name)
            if not os.path.exists(fname):
                os.makedirs(fname)
            fname = os.path.join(fname, f"{self.c_name}_tp{self._stafan_tp}.stafan")

        with open(fname, 'w') as outfile:
            outfile.write("Node,C0,C1,B0,B1,S\n")
            for node in self.nodes_lev:
                ss = [f"{x:e}" for x in [node.C0, node.C1, node.B0, node.B1, node.S]]
                outfile.write(",".join([node.num] + ss) + "\n")
        if verbose:
            print(f"\nSaved STAFAN test measuress in {fname}")

    def load_STAFAN(self, fname): # change name
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
        self._stafan_executed = True

##### Ghazal's Experiments
    def get_fanout_PO(self, n):
        q = deque()
        q.append(n)
        PO_fanouts = set()
        
        while q:
            front = q.popleft()
            if front.ntype=='PO':
                PO_fanouts.add(front)
            for dnode in front.dnodes:
                if dnode not in q:
                    q.append(dnode)
        return PO_fanouts

    def get_fanin_PI(self, n):
        q = deque()
        q.append(n)
        PI_fanin = set()
        
        while q:
            front = q.popleft()
            if front.ntype=='PI':
                PI_fanin.add(front)
            for unode in front.unodes:
                if unode not in q:
                    q.append(unode)
        return PI_fanin

    def imply_and_check_v0(self, n):
        """
        Version 0:
        Gets a node (can be one of remaining faults of ppsf).
        Returns which PI nodes must be tested.
        """
        fanout_PO = self.get_fanout_PO(n)
        fanin_PI = set()
        for po in fanout_PO:
            for pi in self.get_fanin_PI(po):
                fanin_PI.add(pi)
        return fanin_PI

    def fault_to_node(self, fault):
        node_num = fault.__str__()[:-2]
        
        for n in self.nodes_lev:
            if n.num == node_num:
                return n
        
        return None    
    
    def reset_values(self):
        for n in self.nodes_lev:
            n.value = None

    def set_unodes(self, n , value):
        for u in n.unodes:
            if (u.value == 0 and value == 1) or (u.value == 1 and value == 0):
                print('Conflict!')
            elif (u.value == 'X' or u.value == None or u.value == '_') and (value == 0 or value == 1):
                u.value = value
            elif (u.value == 0 or u.value == 1) and (value == 'X' or value == 'None'):
                pass

    def evaluate_unodes(self, node): #TODO: if this is useful for the future, it should be move to node.py
        """Updates value of unodes of front node"""

        if node.gtype == 'IPT' or node.gtype == 'BRCH' or node.gtype == 'BUFF':
            self.set_unodes(node, node.value)
        elif node.gtype == 'OR':
            if node.value == 0:
                self.set_unodes(node, 0)
            else:
                self.set_unodes(node, config.X_VALUE)
        elif node.gtype == 'AND':
            if node.value == 1:
                self.set_unodes(node, 1)
            else:
                self.set_unodes(node, config.X_VALUE)
        elif node.gtype == 'NOR':
            if node.value == 1:
                self.set_unodes(node, 0)
            else:
                self.set_unodes(node, config.X_VALUE)
        elif node.gtype == 'NAND':
            # print(node.value)
            if node.value == 0:
                # print('Zero value')
                self.set_unodes(node, 1)
                # print(node.unodes)
                # for u in node.unodes:
                #     print(u.value)
            else:
                self.set_unodes(node, config.X_VALUE)
        elif node.gtype == 'XOR' or node.gtype == 'XNOR':
            self.set_unodes(node, 'X')
        elif node.gtype == 'NOT':
            if node.value == 1:
                self.set_unodes(node, 0)
            elif node.value == 0:
                self.set_unodes(node, 1)
            else:
                self.set_unodes(node, config.X_VALUE)
    
    def evaluate_dnodes(self, node): #TODO: if this is useful for the future, it should be move to node.py
        if len(node.dnodes) == 0:
            return
        
        if node.dnodes[0].gtype == 'IPT' or node.dnodes[0].gtype == 'BRCH' or node.dnodes[0].gtype == 'BUFF':
            for n in node.dnodes:
                n.value = node.value
            

        elif node.dnodes[0].gtype == 'OR':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == 1:
                    node.dnodes[0].value = 1
                    break

        elif node.dnodes[0].gtype == 'AND':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == 0:
                    node.dnodes[0].value = 0
                    break

        elif node.dnodes[0].gtype == 'NOR':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == 1:
                    node.dnodes[0].value = 0
                    break

        elif node.dnodes[0].gtype == 'NAND':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == 0:
                    node.dnodes[0].value = 1
                    break
        
        elif node.dnodes[0].gtype == 'XOR' or node.dnodes[0].gtype == 'XNOR':
            flag = True
            for udnode in node.dnodes[0].unodes:
                if udnode.value not in [0, 1]:
                    flag = False
                    break
            if flag:
                node.dnodes[0].imply()


        elif node.dnodes[0].gtype == 'NOT':
            if node.value == 1:
                node.dnodes[0].value = 0
            elif node.value == 0:
                node.dnodes[0].value = 1
    
    def forward_implication(self, node, value):
        """Update value of nodes as much as we can in fan-out of the given node"""
        """write v2: returns updated nodes"""
        node.value = value
        q = deque()
        q.append(node)

        while q:
            front = q.popleft()
            self.evaluate_dnodes(front)
            for dnode in front.dnodes:
                if dnode not in q:
                    q.append(dnode)

    def backward_implication(self, node, value):
        """Update value of nodes as much as we can in fan-in of node"""
        """write v2: returns updated nodes"""

        node.value = value
        q = deque()
        q.append(node)

        while q:
            front = q.popleft()
            self.evaluate_unodes(front)
            for unode in front.unodes:
                if unode not in q:
                    q.append(unode)

        for pi in self.PI:
            if pi.value is None:
                pi.value = '_' #Think! for outputs

    def print_values(self):
        for n in self.nodes_lev:
            print(n.num, n.value, end = '|')
    
    def print_unodes(self, n):
        print('node is: ', n.num)
        print('unodes are: ')
        print([f'{u.num}:{u.value}' for u in n.unodes])
    
    def print_inputs(self):
        print('PI:',[f'{p.num}:{p.value}' for p in self.PI])


    def imply_and_check_v1(self, fault):
        """Has a bug. did not fix it cuz the performance is so bad and it has to be upgraded"""
        """Find the tp consist of 1, 0, X and returns it"""
        self.reset_values()
        node = self.fault_to_node(fault)
        stuck_val = int(fault.__str__()[-1])
        self.forward_implication(node, 1-stuck_val)
        # print('\n_______________________________________\n')
        # print(fault.__str__())
        # print('\nAFTER FORWARD: ')
        # self.print_values()
        # for _ in range(20):
        # Question: should we forward again, OR repeat this procedure many times?
        # Write sth to test if values are updates?

        for _ in range(1):
            # print('round', round)
            for n in reversed(self.nodes_lev):
                if n.value is not None:
                    self.backward_implication(n, n.value)
            # print('\nAFTER BACKWARD: ')
            # print(len(self.nodes_lev))
            # self.print_values()
            # for n in self.nodes_lev: 
            #     self.print_unodes(n)
            # self.print_inputs()
            # input()

            for n in self.nodes_lev:
                if n.value is not None:
                    self.forward_implication(n, n.value)
            # print('\nAFTER FORWARD: ')
            # self.print_values()

        
        # not necessarily returns
        return [pi.value if pi.value is not None else '_' for pi in self.PI ] #
            
    def imply_and_check_v2(self, node):
        # self.reset_values()
        # node = self.fault_to_node(fault)
        # stuck_val = int(fault.__str__()[-1])
        before_values = [n.value for n in self.nodes_lev]
        self.forward_implication(node, node.value)
        after_values_f = [n.value for n in self.nodes_lev]
        # print('after forward:')
        # print([f'{n.num}:{n.value}' for n in self.nodes_lev])
        
        updated_nodes_f = []
        for i in range(len(self.nodes_lev)):
            if after_values_f[i] != before_values[i]:
                updated_nodes_f.append(self.nodes_lev[i])

        self.backward_implication(node, node.value)
        after_values_b = [n.value for n in self.nodes_lev]
        # print('after backward:')
        # print([f'{n.num}:{n.value}' for n in self.nodes_lev])
        
        # input()

        updated_nodes_b = []
        for i in range(len(self.nodes_lev)):
            if after_values_b[i] != before_values[i]:
                updated_nodes_b.append(self.nodes_lev[i])
        
        for n in updated_nodes_f+updated_nodes_b:
            self.imply_and_check_v2(n)

        


##### Entropy / OR not called anywhere

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