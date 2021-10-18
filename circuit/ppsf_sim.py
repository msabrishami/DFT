
import sys
import math
from circuit import Circuit
from node import Node
from fault_sim import FaultSim, FaultList

import pdb





class PPSF(FaultSim):
    """ 
    Parallel Patern Single Fault, Fault Simulation 
    """

    def __init__(self, circuit):
        super().__init__(circuit)
        self.fs_type = "ppsf"
        n = sys.maxsize
        self.bitlen = int(math.log2(n))+1
        self.bitwise_not = 2**self.bitlen-1
        print("System bitlen is {}".format(self.bitlen))
        self.fault_num = []
        self.fault_val = []


    def add_fault(self, fault):
        """ add a single fault to the fault list """ 
        self.fault_num.append(fault.split('@')[0])
        self.fault_val.append(fault.split('@')[1])

 
    def single(self, tps, fault=None):
        """ 
        one run with given tps, size of tps should be less than self.bitlen
        """
        if len(tps) > self.bitlen:
            print("Error - len tps should be bitlen")
            return None

        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):  #5 
            for j in range(len(tps)): 
                tps_bin[i] += (tps[j][i]*(2**j))

        # for tp_bin in tps_bin:
        #     print(tp_bin)
        self.circuit.logic_sim_bitwise(tps_bin)
    

    def fs_exe(self, tp_num, t_mode='rand', r_mode='b'): 
        for idx in range(len(self.fault_num)):
            fault_num = self.fault_num[idx]
            fault_val = self.fault_val[idx]
            fault = fault_num + '@' + fault_val
            tps = []
            for i in range(64):
                tps.append(self.circuit.gen_tp())
            self.single(tps, fault)
