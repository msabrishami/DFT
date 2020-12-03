from d_alg import *
from podem_ting import *
from collections import deque

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
gtype:IPT, BRCH, XOR,OR,NOR,NOT,NAND,AND
ntype:GATE,PI,FB,PO
'''

'''
Function: imply_and_check, error_not_at_PO, 
'''

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

