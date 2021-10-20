
import sys
import math
from circuit import Circuit
from node import Node
from fault_sim import FaultList_2
import utils 
import pdb

import time
from multiprocessing import Process, Pipe




class PPSF():
    """ 
    Parallel Patern Single Fault, Fault Simulation 
    """

    def __init__(self, circuit):
        self.circuit = circuit 
        self.wordlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**self.wordlen-1
        self.fault_list = FaultList_2() 

    def add_fault(self, fault):
        """ add a single fault to the fault list """ 
        self.fault_list.add(fault)

 
    def single(self, tps, fault):
        """ 
        One pass of fault simulation for test patterns over a single fault 
        Number of tps should be less than system word length 
        If a fault is given, injects the fault and then runs logic simulation (bitwise)

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
            print("Error - len tps should be bitlen")
            return None

        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):  #5 
            for j in range(len(tps)): 
                tps_bin[i] += (tps[j][i]*(2**j))

        self.circuit.logic_sim_bitwise(tps_bin)
        Zg = self.circuit.read_PO()
        self.circuit.logic_sim_bitwise(tps_bin, fault)
        Zf = self.circuit.read_PO()
        res = utils.comp_Zg_Zf_bin(Zg, Zf, self.wordlen)
        # The order of tp and res are reversed
        res_fixed = set()
        for k in res:
            res_fixed.add(self.wordlen-1-k)
        # print(res_fixed)
        return res_fixed

    
    def parallel(self, num_proc, tp_count=None, in_tp_fname=None, out_tp_fname=None):
        """ 
        Using parallelization for multi-threading 
        All the existing faults are considered 
        TPs can be generated here, or can be read from a file? 
        """
        if tp_count == None and in_tp_fname==None and out_tp_fname==None:
            print("Error! not all of them can be None")
        elif tp_count and out_tp_fname and in_tp_fname==None:
            tps = self.circuit.gen_tp_file(tp_count, out_tp_fname) 
        elif tp_count==None and in_tp_fname and out_tp_fname==None:
            tps = self.circuit.load_tp_file(in_tp_fname)
        else:
            print("Error! ")
            return None

        start_time = time.time()
        process_list = []
        # You need to define a specific thread method here
        
    

    def fs_exe(self, tp_fname): 
        """ runs ppfs for all the fault in the fault list 
        given the tps (either filename or tp arrays)
        currently does NOT return results """ 
        tps = self.circuit.load_tp_file(tp_fname)
        for fault in self.fault_list.faults:

            tot_pass = int(len(tps)/self.wordlen)

            for _pass in range(tot_pass):
                tps_pass = tps[_pass*64:(_pass+1)*64]
                res = self.single(tps_pass, fault)
                fault.D_count += len(res)
            
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

