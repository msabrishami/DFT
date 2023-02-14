
from d_alg import *
from podem_new import *
from parallel_fs import *
from faul_simuation import deductive_fs
from collections import deque
from circuit.circuit import Circuit

import time
import os, sys

class ATPG:
   def __init__(self, circuit):
      self.circuit = circuit
      
      self.total_fault_list = []
      self.reduce_fault_list = []
      #self.reduce_fault_list = []
      for node in self.circuit.nodes_lev:
         self.total_fault_list.append((node.num,0))
         self.total_fault_list.append((node.num,1))
         #self.total_fault_list.insert(0,(node.num,0))
         #self.total_fault_list.insert(0,(node.num,1))
      for node in self.circuit.nodes_lev:
         if node.gtype in ['BRCH', 'IPT']:
            self.reduce_fault_list.append((node.num,0))
            self.reduce_fault_list.append((node.num,1))

   def atpg_det(self, DFS_PFS = 'DFS', Podem_Dalg = 'Podem'):
      print('#####DETERMINISTIC#####')
      start = time.time()
      self.total_fault_set = set(self.total_fault_list)
      #self.reduce_fault_set = set(self.reduce_fault_list)
      self.fault_detected = set()
      self.error_list = []
      #self.circuit.lev()
      self.circuit.SCOAP_CC()
      self.circuit.SCOAP_CO()
      flag = 0
      count_set = 100 #500
      while(flag < 2 and len(self.total_fault_set) != 0):#len(self.reduce_fault_set) != 0):#len(self.total_fault_set) != 0):
         fault = self.total_fault_set.pop()
         #fault = self.reduce_fault_set.pop()
         #for fault in self.total_fault_set:
         #print('rest fault list', len(self.total_fault_set))
         #print('rest fault list', len(self.reduce_fault_set))
         #print(fault)
         if Podem_Dalg == 'Podem':
            test = Podem(self.circuit, fault[0], fault[1], count_set)
         else:
            test = D_alg(self.circuit, fault[0], fault[1], count_set)
         #blockPrint()
         if test.test() == True:        
            IPT_list = test.return_IPT()
            IPT_binary_list = []
            for x in IPT_list:
               if x == 15 or x == 12 or x == 9: 
                  IPT_binary_list.append(1)
               else:
                  IPT_binary_list.append(0)
            if DFS_PFS == 'DFS':
               dfs_test = DFS(self.circuit)
               fault_list_set = dfs_test.fs_for_atpg(IPT_binary_list)
            else:
               pfs_test = PFS(self.circuit)
               fault_list_set = pfs_test.fs_for_atpg(self.total_fault_set, IPT_binary_list)
            self.total_fault_set = self.total_fault_set - fault_list_set
            #self.reduce_fault_set = self.reduce_fault_set - fault_list_set
            self.fault_detected = self.fault_detected | fault_list_set
            if fault in self.error_list:
               self.error_list.remove(fault)
            self.error_list = list(set(self.error_list) - fault_list_set)
         else:
            if fault in self.error_list:
               pass
            else:
               self.error_list.append(fault)
         enablePrint()
         if len(self.total_fault_set) == 0 and len(self.error_list) != 0:
         #if len(self.reduce_fault_set) == 0 and len(self.error_list) != 0:
            self.total_fault_set = set(self.error_list)
            #self.reduce_fault_set = set(self.error_list)
            flag += 1
            count_set += 5000 #200000 
         if len(self.total_fault_set) == 0 and len(self.error_list) == 0:
         #if len(self.reduce_fault_set) == 0 and len(self.error_list) == 0:
             flag = 2
      end = time.time()
      
      print('fault can not be detected >>',self.error_list)
      print('total num of fault >>',len(self.total_fault_list))
      print('total num of fault can not be detected >>',len(self.error_list))
      #print('fault coverage >>',(len(self.total_fault_list)-len(self.error_list))/len(self.total_fault_list))  
      print('fault coverage >>',len(self.fault_detected)/len(self.total_fault_list))  
      print('run time >>', end - start) 


   def atpg_ran(self, DFS_PFS = 'DFS', Podem_Dalg = 'Podem', RAN_percentage = 75):
      if RAN_percentage > 100:
         raise ValueError('RAN_percentage should be smaller than 100')
      print('#####RANDOM#####')
      start = time.time()
      #self.circuit.lev()
      self.circuit.SCOAP_CC()
      self.circuit.SCOAP_CO()
      self.total_fault_set = set(self.total_fault_list)
      while((len(self.total_fault_list)-len(self.total_fault_set))/len(self.total_fault_list) < RAN_percentage/100):
         IPT_binary_list = self.circuit.gen_tp()
         if DFS_PFS == 'DFS':
            dfs_test = DFS(self.circuit)
            fault_list_set = dfs_test.fs_for_atpg(IPT_binary_list)
         else:
            pfs_test = PFS(self.circuit)
            fault_list_set = pfs_test.fs_for_atpg(self.total_fault_set, IPT_binary_list)
         self.total_fault_set = self.total_fault_set - fault_list_set
      flag = 0
      count_set = 100 #500
      while(flag < 2 and len(self.total_fault_set) != 0):
         fault = self.total_fault_set.pop()
         #print('rest fault list', len(self.total_fault_set))
         #print(fault)
         if Podem_Dalg == 'Podem':
            test = Podem(self.circuit, fault[0], fault[1], count_set)
         else:
            test = D_alg(self.circuit, fault[0], fault[1], count_set)
         #blockPrint()
         if test.test() == True:
            IPT_list = test.return_IPT()
            IPT_binary_list = []
            for x in IPT_list:
               if x == 15 or x == 12 or x == 9: 
                  IPT_binary_list.append(1)
               else:
                  IPT_binary_list.append(0)
            if DFS_PFS == 'DFS':
               dfs_test = DFS(self.circuit)
               fault_list_set = dfs_test.fs_for_atpg(IPT_binary_list)
            else:
               pfs_test = PFS(self.circuit)
               fault_list_set = pfs_test.fs_for_atpg(self.total_fault_set, IPT_binary_list)
            self.total_fault_set = self.total_fault_set - fault_list_set
            if fault in self.error_list:
               self.error_list.remove(fault)
            self.error_list = list(set(self.error_list) - fault_list_set)
         else:
            if fault in self.error_list:
               pass
            else:
               self.error_list.append(fault)
         enablePrint()
         if len(self.total_fault_set) == 0 and len(self.error_list) != 0:
            self.total_fault_set = set(self.error_list)
            flag += 1
            count_set += 5000 #200000
         if len(self.total_fault_set) == 0 and len(self.error_list) == 0:
             flag = 2
      end = time.time()
      
      print('fault can not be detected >>',self.error_list)
      print('total num of fault >>',len(self.total_fault_list))
      print('total num of fault can not be detected >>',len(self.error_list))
      print('fault coverage >>',(len(self.total_fault_list)-len(self.error_list))/len(self.total_fault_list))  
      print('run time >>', end - start) 

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
