
from d_alg import *
from podem_new import *
from parallel_fs import *
from deductive_fs import *
from collections import deque
from circuit import Circuit

import time

'''
D     1/0
D_BAR 0/1
five value define
access value:five_value.ZERO.value
access variable:five_value(0).name
class five_value(Enum):
   ZERO = 0
   ONE = 15
   D = 12
   D_BAR = 3
   X = 9
gtype:IPT, BRCH, XOR, OR, NOR, NOT, NAND, AND
ntype:GATE, PI, FB, PO
'''

class ATPG:
   def __init__(self, circuit):
      self.circuit = circuit
      
      self.total_fault_list = []
      #self.reduce_fault_list = []
      for node in self.circuit.nodes_lev:
         #if node.gtype in ['BRCH', 'IPT']:
            #self.reduce_fault_list.append((node.num,0))
            #self.reduce_fault_list.append((node.num,1))
         self.total_fault_list.append((node.num,0))
         self.total_fault_list.append((node.num,1))

   #TODO print ATPG information
   #def __str__(self):
   #   res = []
   #   return '\n'.join(res)

   def atpg_det(self, DFS_PFS = 'DFS', Podem_Dalg = 'Podem'):
      print('#####DETERMINISTIC#####')
      start = time.time()
      self.total_fault_set = set(self.total_fault_list)
      #self.reduce_fault_set = set(self.reduce_fault_list)
      #self.circuit.lev()
      self.circuit.SCOAP_CC()
      self.circuit.SCOAP_CO()
      flag = 0
      count_set = 100
      while(flag < 2):
         for fault in self.total_fault_set:
            if Podem_Dalg == 'Podem':
               test = Podem(self.circuit, fault[0], fault[1], count_set)
            else:
               test = D_alg(self.circuit, fault[0], fault[1], count_set)
            if test.test() == True: #TODO there should be a wrapper function in Podem and DAlg whose name is test
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

         count_set += 5000 #TODO there is a count in Podem and DAlg to terminate the search for each fault which is initialized to 100
         flag += 1
         if len(self.total_fault_set) == 0:
             flag = 2
      end = time.time()
      #TODO comment
      print('fault can not be detected >>',self.total_fault_set)
      print('total num of fault >>',len(self.total_fault_list))
      print('total num of fault can not be detected >>',len(self.total_fault_set))
      print('fault coverage >>',(len(self.total_fault_list)-len(self.total_fault_set))/len(self.total_fault_list))  
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
      #self.reduce_fault_set = set(self.reduce_fault_list)
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
      count_set = 100
      while(flag < 2):
         for fault in self.total_fault_set:
            if Podem_Dalg == 'Podem':
               test = Podem(self.circuit, fault[0], fault[1], count_set)
            else:
               test = D_alg(self.circuit, fault[0], fault[1], count_set)
            if test.test() == True: #TODO there should be a wrapper function in Podem and DAlg whose name is test
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

         count_set += 5000 #TODO there is a count in Podem and DAlg to terminate the search for each fault which is initialized to 100
         flag += 1
         if len(self.total_fault_set) == 0:
             flag = 2
      end = time.time()
      #TODO comment
      print('fault can not be detected >>',self.total_fault_set)
      print('total num of fault >>',len(self.total_fault_list))
      print('total num of fault can not be detected >>',len(self.total_fault_set))
      print('fault coverage >>',(len(self.total_fault_list)-len(self.total_fault_set))/len(self.total_fault_list))  
      print('run time >>', end - start) 

def ATPG_DET(circuit, alg_type):
   """
   Stand alone function:
   execulte DALG or PODEM for a fault based on alg_type
   when the alg_type is chosen, all faults in the fault set will be exe by this alg
   """
   ############## Is it good??????????????????????
   fault_sim = FaultSim(circuit)

   # set: fault cannot be detected
   fault_non_det = set()
   fault_set_rest = fault_sim.fault_set_rest

   # record time
   start_time = time.time()

   if alg_type == "DALG":
      while fault_set_rest:
         fault = fault_set_rest.pop()
         alg_obj = D_alg(circuit, fault[0], fault[1])

         if alg_obj.dalg():
            IPI_list = alg_obj.return_IPI()
            IPI_binary_list = []
            #print(IPT_list)
            for x in IPI_list:
               if x == 15 or x == 12 or x == 9: 
                     IPI_binary_list.append(1)
               else:
                     IPI_binary_list.append(0)

            #print(IPT_binary_list)
            dfs_test = DFS(circuit)
            fault_subset = dfs_test.single(IPI_binary_list)
            fault_set_rest = fault_set_rest.difference(fault_subset)
         else:
            # if the dalg fails, add the fault to non-det set
            fault_non_det.add(fault)

      end_time = time.time()
      exe_time = end_time - start_time

      fault_coverage = (len(circuit.nodes_lev) - len(fault_non_det)) / len(circuit.nodes_lev)

      print("Algorithm: DALG")
      print("Circuit: ", circuit.c_name)
      print("Fault Coverage: ", fault_coverage)
      print("Time: ", exe_time)
      print("None detectable faults: ", fault_non_det, "\n")

   elif alg_type == "PODEM":
      raise NameError("PODEM TBC")

   else:
      raise NameError("Algorithm type is invalid! alg_type = 'DALG' or 'PODEM'!")

