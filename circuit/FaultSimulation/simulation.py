import os
import numpy as np

import sys

import config
from FaultSimulation import fault

class FaultSim:
    
    def __init__(self, circuit):
        self.circuit = circuit
        self.fault_list = fault.FaultList()
        self.fs_type = ""
        self.fault_set_all = set()
        for node in self.circuit.nodes_lev:
            self.fault_set_all.add((node.num,0))
            self.fault_set_all.add((node.num,1))
        self.fault_set_rest = self.fault_set_all # seems redundant

    def fs_folder(self):
        """
        Creating the required directories for fault simulation
        """
        paths = [config.FAULT_SIM_DIR, 
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name]
        
        for path in paths:
            if not os.path.exists(path):
                print("Creating directory {}".format(path))
                os.mkdir(path)
               
    def single(self, input_pattern):
        """ Single pass of simulation. 
        DFS/PFSP: single test pattern
        PPSF: single fault
        """
        raise NotImplementedError()

    def fs_for_atpg(self):
        """ DFS/PFS for ATPG use """ 
        raise NotImplementedError()
        
    def fs_exe(self, tp_num=1, t_mode='rand', r_mode='b'):
        """ Defined in children: DFS, PFS """
        raise NotImplementedError()

    def return_rest_fault(self): # seems redundant
        return self.fault_set_rest 