
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

 
    def single(self, tps):
        """ 
        one run with given tps, size of tps should be less than self.bitlen
        """
        if len(tps) != self.bitlen:
            print("Error - len tps should be bitlen")
            return None
        
        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):  #5 
            for j in range(len(tps)): 
                tps_bin[i] += (tps[j][i]*(2**j))

        # for tp_bin in tps_bin:
        #     print(tp_bin)
        self.circuit.logic_sim_bitwise(tps_bin)

