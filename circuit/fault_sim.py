import config
import os
import numpy as np

class Fault:
    def __init__(self, node_num, stuck_val):
        self.node_num = str(node_num)
        self.stuck_val = str(stuck_val)


class Fault_C (Fault):
    def __init__(self, node_num, stuck_val):
        super().__init__(node_num, stuck_val)
        self.D_count = 0

    def __str__(self):
        return self.node_num + "@" + self.stuck_val

    def __repr__(self):
        return self.node_num + "@" + self.stuck_val


class FaultList:
    """ Fault list """
    #TODO: maybe using dictionary or set instead of a list for faults
    def __init__(self):
        self.faults = []

    def add(self, node_num, stuck_val):
        self.faults.append(Fault_C(node_num, stuck_val))

    def add_str(self, fault_str):
        """ add a fault if the fault format is <node-num>@<stuck value> """ 
        num, val = fault_str.strip().split("@")
        self.faults.append(Fault_C(num, val))

    def add_all(self, circuit):
        for node in circuit.nodes_lev:
            self.add(node.num, 0)
            self.add(node.num, 1)

    def add_random(self, circuit, random_num):
        idx_random = np.random.choice(len(circuit.nodes_lev), random_num, replace=False)
        for i in range(random_num):
            self.add(circuit.nodes_lev[idx_random[i]].num, 
                    np.random.randint(0,2))
    
    def add_fault(self, fault):
        self.faults.append(fault)
    
    def add_file(self, fname):
        """ read faults from a file and add it to the fault list 
        file format: each fault <node-num>@<stuck value> in separate lines

        Arguments
        ---------
        fname : str
            the path and file name of the fault file 
        """ 
        with open(fname, "r") as infile:
            for line in infile:
                self.add_str(line)

    def write_file(self, fname, verbose=False):
        with open(fname, "+w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "\n")
            if verbose:
                print("Fault list is stored in {}".format(fname))

    def write_file_extra(self, fname, verbose=False):
        with open(fname, "w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "," + ",".join([str(x) for x in fault.D_count])+"\n")
            if verbose:
                print("Fault list with D_counts is stored in {}".format(fname))
    
    def calc_fc(self):
        detected_count = 0
        for fault in self.faults:
            if fault.D_count > 0:
                detected_count += 1
        return detected_count / len(self.faults)
   
    def get_D_count(self):
        res = {}
        for fault in self.faults:
            res[str(fault)] = fault.D_count
        return res

class FaultSim:
    
    def __init__(self, circuit):
        self.circuit = circuit
        self.fault_list = FaultList()
        self.fs_type = ""
        self.fault_set_all = set()
        for node in self.circuit.nodes_lev:
            self.fault_set_all.add((node.num,0))
            self.fault_set_all.add((node.num,1))
        self.fault_set_rest = self.fault_set_all
     

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


    def return_rest_fault(self):
        return self.fault_set_rest

