from circuit import Circuit
from classdef import podem_node_5val
from podem import podem
import copy
from timeit import default_timer as timer
from collections import defaultdict
'''
data structure explaination:
full_fault_dict and reduced_fault_dict: Key is the tuple standing for faults. Value includes three possible value -1, 0, 1. -1 means untried, 0 means undetectable, 1 means detectable

list all the variable used in atpg inherited from Circuit class:
random input pattern  #return from self.get_random_input_pattern()
self.nodes #previously known as nodelist / nodelist test.
self.nodes_lev = None #previously known as nodelist_order
self.input_num_list = []
self.fault_name = []
self.fault_node_num = []
self.fault_type = []
self.rfl_node = []
self.rfl_ftype = []
'''
class ATPG(Circuit):
    """version 0"""
    def __init__(self, c_name):
        Circuit.__init__(self,c_name)
        self.input_val_list=[]
        self.total_faults = 0
        self.total_faults_after_reduced = 0
        self.full_fault_dict = {}
        self.reduced_fault_dict = {}
        self.fault_coverage= 0
        self.RFL_fault_coverage = 0
        self.input_pattern_collect = [] #collect all the input pattern
        self.input_pattern_to_fault_collect = []
        self.full_fault_dict_bit = 0
        #random_input_part
        self.cur_count_total_faults = 0
        self.cur_count_total_faults_after_reduced = 0
        self.pre_count_total_faults = 0
        self.pre_count_total_faults_after_reduced = 0
        self.hyper_parameter= 0
        self.random_counter = 0
        self.dfs_counter = 0
    def dfs_exectution(self):
        self.logic_sim(self.input_val_list)
        dfs_result = self.dfs()
        self.input_pattern_to_fault_collect.append(copy.deepcopy(dfs_result))
        return dfs_result
    def initialize_hyper_para(self):
        self.hyper_parameter = int(len(self.nodes)/10)
    def random_input_get_detectable_fault_set(self):
        self.input_val_list = self.get_random_input_pattern()
        self.input_pattern_collect.append(self.input_val_list)
        result = self.dfs_exectution()
        return result
    def atpg_input_get_detectable_fault_set(self):
        for j in range (len(self.input_val_list)):
            if self.input_val_list[j]=='X':
                self.input_val_list[j]=0
        if self.input_val_list not in self.input_pattern_collect:
            self.input_pattern_collect.append(copy.deepcopy(self.input_val_list))
            dfs_fault_set = self.dfs_exectution()
            for i in dfs_fault_set:
                if self.full_fault_dict.get(i)==-1:
                    self.full_fault_dict[i]=1
                    self.cur_count_total_faults+=1
                if self.full_fault_dict_bit==0:
                    if self.reduced_fault_dict.get(i)==-1:
                        self.reduced_fault_dict[i]=1
                        self.cur_count_total_faults_after_reduced+=1
    def get_fault_dicts(self):
        self.get_full_fault_list_for_dict()
        self.get_reduced_fault_list_for_dict()
    def get_full_fault_list_for_dict(self):
        for node in self.nodes_lev:
            sa0_str = "{}@0".format(node.num)
            self.fault_name.append(sa0_str)
            self.fault_node_num.append(node.num)
            self.fault_type.append(0)
            self.full_fault_dict.update({(node.num,0):-1})
            sa1_str = "{}@1".format(node.num)
            self.fault_name.append(sa1_str)
            self.fault_node_num.append(node.num)
            self.fault_type.append(1)  
            self.full_fault_dict.update({(node.num,1):-1})
    def get_reduced_fault_list_for_dict(self):
        faults_fanout = []
        for i in range(len(self.nodes)):
            if (self.nodes[i].cpt == 1):
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
                self.reduced_fault_dict.update({(self.nodes[i].num,0):-1})
            if self.nodes[i].sa1 == 1:
                self.rfl_node.append(self.nodes[i].num)
                self.rfl_ftype.append(1)
                self.reduced_fault_dict.update({(self.nodes[i].num,1):-1})

    
    def random_input_part(self):
        self.total_faults = len(self.full_fault_dict.keys())
        self.total_faults_after_reduced = len(self.reduced_fault_dict.keys())
        while True:
            if self.random_counter>self.hyper_parameter:
                break
            else:
                dfs_fault_set = self.random_input_get_detectable_fault_set()
                for i in dfs_fault_set:
                    if self.full_fault_dict.get(i)==-1:
                        self.full_fault_dict[i]=1
                        self.cur_count_total_faults+=1
                    if self.reduced_fault_dict.get(i)==-1:
                        self.reduced_fault_dict[i]=1
                        self.cur_count_total_faults_after_reduced+=1
                if self.cur_count_total_faults==self.pre_count_total_faults:
                    self.random_counter+=1
                self.pre_count_total_faults = self.cur_count_total_faults
                self.pre_count_total_faults_after_reduced = self.cur_count_total_faults_after_reduced
    def check_fault_coverage(self):
        self.fault_coverage = self.cur_count_total_faults/self.total_faults
    def check_RFL_fault_coverage(self):
        self.RFL_fault_coverage = self.cur_count_total_faults_after_reduced/self.total_faults_after_reduced
    def podem(self, i):
        res = podem(i[0], i[1], self.nodes, self.nodes_lev)
        return res
    def try_remained_fault_RFL(self):
        for i in self.reduced_fault_dict.keys():
            if self.reduced_fault_dict[i]==-1:
                res = self.podem(i)
                if res.result == 1:
                    self.input_val_list = res.pattern
                    self.atpg_input_get_detectable_fault_set()
                elif res.result == 0:
                    self.reduced_fault_dict[i]==0
                    self.full_fault_dict[i]==0
            self.check_RFL_fault_coverage()
            if int(self.RFL_fault_coverage)==1:
                break
    def try_remained_fault_FFL(self): #FFL means full_fault_dict
        for i in self.full_fault_dict.keys():
            if self.full_fault_dict[i]==-1:
                res = self.podem(i)
                if res.result == 1:
                    self.input_val_list = res.pattern
                    self.atpg_input_get_detectable_fault_set()
                elif res.result == 0:
                    self.full_fault_dict[i]==0
            self.check_fault_coverage()
            if int(self.fault_coverage)==1:
                break
    def reduce_input_pattern(self):
        test_pattern_list = {}
        all_test_pattern = defaultdict(set)
        all_fault = defaultdict(set)
        result = []
        count = 0
        for i in self.input_pattern_collect:
            strings = [str(integer) for integer in i]
            pattern = "".join(strings)
            fault = set() 
            for j in self.input_pattern_to_fault_collect[count]:
                f = str(j[0]) + "@" + str(j[1])
                fault.add(f) 
                all_fault[f].add(pattern)
            test_pattern_list[pattern] = len(fault)
            all_test_pattern[pattern] = fault
            count = count + 1
        while (len(all_fault) != 0):
            maxPattern = max(test_pattern_list, key = test_pattern_list.get) 
            temp = all_test_pattern.get(maxPattern)
            if temp != None:
                result.append(maxPattern)
                for i in temp: 
                    if all_fault.get(i) != None:
                        for j in all_fault.get(i): 
                            if test_pattern_list.get(j) != None:
                                remain = test_pattern_list.get(j) - 1 
                                if remain > 0:
                                    test_pattern_list.update({j:remain})
                                if remain == 0:
                                    test_pattern_list.pop(j)
                        all_fault.pop(i)
                if test_pattern_list.get(maxPattern) != None:
                    test_pattern_list.pop(maxPattern)
        return result
    def class_main(self):
        start = timer()
        self.read_circuit()
        self.lev()
        self.initialize_hyper_para()
        self.get_fault_dicts()
        self.random_input_part()
        self.check_fault_coverage()
        self.check_RFL_fault_coverage()
        print("The circuit is ",self.c_name)
        print("hyper_parameter is ",self.hyper_parameter)
        if int(self.RFL_fault_coverage)==1:
            #print("end")
            print(self.RFL_fault_coverage)
        else:
            print("After random input pattern, the fault coverage is: ",self.fault_coverage)
            self.try_remained_fault_RFL()
            self.check_fault_coverage()
        if int(self.RFL_fault_coverage)!=1:
            print("The final fault coverage is: ",self.fault_coverage)
        else:
            print("The final fault coverage is: ",self.RFL_fault_coverage)
  
        print("The origial number of input pattern is: ",len(self.input_pattern_collect))
        result = self.reduce_input_pattern()
        print("After reducing alg, the rest number of input pattern is: ",len(result))
        end = timer()
        print("The total time is ",end - start,"s")
class Imply_counter:
    def __init__(self, abort_cnt):
        self.cnt = 0
        self.abort_cnt = abort_cnt
    def increment(self):
        self.cnt += 1
    def initialize(self):
        self.cnt = 0