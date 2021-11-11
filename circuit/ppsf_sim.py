
import sys
import math
import utils 
import time
from multiprocessing import Process, Pipe
import pdb

from circuit import Circuit
from node import Node
from fault_sim import FaultSim


class PPSF(FaultSim):
    """ 
    Parallel Patern Single Fault, Fault Simulation 
    """

    def __init__(self, circuit):
        super().__init__(circuit)
        self.fs_type = "ppsf"
        self.wordlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**self.wordlen-1

    def add_fault(self, fault):
        """ add a single fault to the fault list """ 
        self.fault_list.add(fault)

 
    def single(self, tps, fault):
        """ 
        One pass of fault simulation for test patterns over a single fault. 
        Number of tps should be less than the system's word length. 
        If a fault is given, injects the fault and then runs logic simulation (bitwise).

        Arguments
        ---------
        tps : list of lists
                test patterns. Each tp is itself a list. 
                The order of tp values is the same as circuit.PI 
        Returns
        -------
        res_fixed : set of the index of tps that could detect the given fault
        """
        if len(tps) > self.wordlen:
            print("Error: number of tps should be wordlen")
            return None

        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):  #5 
            for j in range(len(tps)): 
                tps_bin[i] += (tps[j][i]*(2**j))

        self.circuit.logic_sim_bitwise(tps_bin,test_len=len(tps))
        Zg = self.circuit.read_PO()
        self.circuit.logic_sim_bitwise(tps_bin, test_len=len(tps),fault = fault)
        Zf = self.circuit.read_PO()
        res = utils.comp_Zg_Zf_bin(Zg, Zf, min(self.wordlen,len(tps)))
        
        # The order of tp and res are reversed
        res_fixed = set()
        for k in res:
            res_fixed.add(self.wordlen-1-k)
        
        return res_fixed

    def fs_exe(self, tp_fname): 
        """ 
        Runs PPSF for the fault in the fault list, given the tp file. 
        For each fault, it counts the number of times it has been detected.
        """ 
        self.fs_folder()
        print("PPSF for tp file: {}".format(tp_fname))
        tps = self.circuit.load_tp_file(tp_fname)
        print(tps)
        print("----------------------")
        
        for fault in self.fault_list.faults:

            tot_pass = math.ceil(len(tps)/self.wordlen)

            for _pass in range(tot_pass):
                tps_pass = tps[_pass*64:(_pass+1)*64]
                res = self.single(tps_pass, fault)
                fault.D_count += len(res)
                
        print("PPFS completed")
        for fault in self.fault_list.faults:
            if fault.D_count > 0:
                print(fault, fault.D_count)
        print("FC={:.4f}%, tot-faults={}".format(
            100*self.fault_list.calc_fc(), len(self.fault_list.faults)))
   
            # D_p = fault.D_count / len(tps)
            # node = self.circuit.nodes[fault.node_num]
            # if fault.stuck_val == '0':
            #     err = 100*(D_p - node.D0)/D_p
            #     print("{}\tD0_ppsf={:.4f}\tD0={:.4f}\terror={:.2f}%".format(
            #         str(fault), D_p, node.D0, err))
            # elif fault.stuck_val == '1':
            #     err =100* (D_p - node.D1)/D_p
            #     print("{}\tD1_ppsf={:.4f}\tD0={:.4f}\terror={:.2f}%".format(
            #         str(fault), D_p, node.D1, err))

