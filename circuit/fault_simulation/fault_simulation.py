import math
import os
import sys
from abc import ABC, abstractmethod

import config
from fault_simulation import fault


class FaultSim(ABC):

    def __init__(self, circuit, fault_mode=None):
        """
        Parameters
        ----------
        fault_mode : int or FaultList or str
            str: all: add all possible faults
            None: None
            integer: add n random faults
            FaultList: user has passed the desired faults
        """
        self.circuit = circuit

        if not isinstance(fault, fault.FaultList):
            self.fault_list = fault.FaultList()

        self.fs_type = ""
        self.fault_set_all = set()
        for node in self.circuit.nodes_lev:
            self.fault_set_all.add((node.num, 0))
            self.fault_set_all.add((node.num, 1))
        self.fault_set_rest = self.fault_set_all
        self.wordlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**self.wordlen-1

        if fault_mode == 'all':
            self.add_all()

        if isinstance(fault_mode, int):
            self.add_n_random(fault_mode)

    def add_n_random(self, n=1):
        self.fault_list.add_random(self.circuit, random_num=n)

    def add_all(self):
        self.fault_list.add_all(self.circuit)

    def fs_folder(self):
        """
        Creating the required directories for fault simulation
        """
        paths = [config.FAULT_SIM_DIR, config.FAULT_SIM_DIR + '/' + self.circuit.c_name]

        for path in paths:
            if not os.path.exists(path):
                print(f"Creating directory {path}")
                os.mkdir(path)

    # def single(self): -->renamed
    #     """ Single pass of simulation. 
    #     DFS/PFSP: single test pattern
    #     PPSF: single fault
    #     """
    #     raise NotImplementedError()

    # def fs_for_atpg(self):
    #     """ DFS/PFS for ATPG use """
    #     raise NotImplementedError()

    @abstractmethod
    def run(self, tp_num=1, t_mode='rand', r_mode='b'):
        """ Defined in children: DFS, PFS """
        pass

    def return_rest_fault(self):  # seems redundant
        return self.fault_set_rest
