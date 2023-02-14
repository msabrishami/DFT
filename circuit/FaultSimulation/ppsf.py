
import sys
import math
import utils 
import time
from multiprocessing import Process, Pipe
import os

# from fault_sim import FaultSim
from FaultSimulation.simulation import FaultSim
import config
import pdb


class PPSF(FaultSim):
    """ 
    Parallel Patern Single Fault, Fault Simulation 
    """
    def __init__(self, circuit):
        super().__init__(circuit)
        self.fs_type = "ppsf"
        self.wordlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**self.wordlen-1
        self.fs_folder()


    def fs_folder(self):
        super().fs_folder()
        path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + "pfs"
        if not os.path.exists(path):
            os.makedirs(path)


    def single_run(self, tps, fault):
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
        #TODO: Add verbose
        if len(tps) > self.wordlen:
            print("Error: number of tps should be wordlen")
            return None

        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):  #5 
            for j in range(len(tps)): 
                tps_bin[i] += (tps[j][i]*(2**j))

        self.circuit.logic_sim_bitwise(tps_bin)
        Zg = self.circuit.read_PO()
        self.circuit.logic_sim_bitwise(tps_bin, fault)
        Zf = self.circuit.read_PO()
        res = utils.comp_Zg_Zf_bin(Zg, Zf, len(tps))
        
        # The order of tp and res are reversed
        res_fixed = set()
        for k in res:
            res_fixed.add(self.wordlen-1-k)
        
        return res_fixed

    def fs_exe(self, tps, log_fname=None, verbose=False): 
        """ 
        Runs PPSF for the faults in the fault list, given tp count/list/fname
        For each fault, it counts the number of times it has been detected
        WARNING: this method is not tested after a few modifications 
        """
        print("WARNING: ppsf.fs_exe is not tested after a few modifications")
        if isinstance(tps, int):
            tps = self.circuit.gen_multiple_tp(tps)
        elif isinstance(tps, str):
            if os.path.exists(tps):
                tps = self.circuit.load_tp_file(tps)
            else:
                raise "path not exist."

        elif not isinstance(tps, list):
            raise TypeError("tps should be either int, list, or file name")

        for fault in self.fault_list.faults:
            tot_pass = math.ceil(len(tps)/self.wordlen)
            for _pass in range(tot_pass):
                tps_pass = tps[_pass*64:(_pass+1)*64]
                res = self.single_run(tps_pass, fault)
                fault.D_count += len(res)

        if verbose: 
            print("PPFS completed")
            print(f"FC={100*self.fault_list.calc_fc():.4f}%, tot-faults={len(self.fault_list.faults)}")