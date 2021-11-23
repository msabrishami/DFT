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
    def __init__(self):
        node = []
        fault = []
        detected = []
    
    def add_fault(self, circuit, mode="full", fname=None):
        """ add faults to the fault list 
        mode = full: fault list will be all SS@ faults 
        mode = user: fault list will be read from file fname
        """ 
        if mode == "full":
            circuit.get_full_fault_list()
            self.in_fault_num = self.circuit.fault_node_num
            self.in_fault_type = self.circuit.fault_type

        elif mode == "user":
            fr = open(fname, mode='r')
            for line in fr:
                line=line.rstrip('\n').split("@")
                self.in_fault_num.append(line[0])
                self.in_fault_type.append(int(line[1]))

        else:
            raise NameError("fault list type is not accepted")



class FaultList_2:
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
    

class FaultSim:
    
    def __init__(self, circuit):
        self.circuit = circuit
        self.fault_list = FaultList_2()
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
        paths = [config.FAULT_SIM_DIR, config.FAULT_DICT_DIR, 
                # config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/', 
                # config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/', 
                # TODO
                # config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/dfs/', 
                # TODO
                # config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/compare/',
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/pfs/'
                ]
        
        for path in paths:
            if not os.path.exists(path):
                print("Creating directory {}".format(path))
                os.mkdir(path)
               

    # TODO: deprecate this method
    def fs_tp_gen(self, tp_num, t_mode, r_mode='b'):
        raise NameError("Error: This method is deprecated!")
        '''
        Generate test patterns for DFS/PFS
        Arguments:
        ----------
        tp_num : int
                number of test patterns to generate, only used in "rand" mode
        t_mode : str
                rand : random mode, create certain number of random test pattterns
                full : create all possible test patterns in order
        '''
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/'
        tp_fname = tp_path + self.circuit.c_name
        
        if t_mode == 'rand':
            tp_fname += '_' + str(tp_num) + '_tp_' + r_mode + '.tp'
            self.circuit.gen_tp_file(tp_num, fname = tp_fname, mode = "b")
        
        elif t_mode == 'full':
            tp_fname += '_full_tp_' + r_mode + '.tp'
            times = pow(2, len(self.circuit.PI))
            fw = open(tp_fname, mode='w')
            PI_string = ','.join([node.num for node in self.circuit.PI])
            fw.write(PI_string + '\n')
            for i in range(times):
                pattern = list(bin(i)[2:].zfill(num))
                pattern_str = ",".join(pattern)
                fw.write(pattern_str + '\n')
        else: 
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")

        print("Test patterns were saved in {}".format(tp_fname))


    def fs_tp_gen_golden(self, tp_num=1, no=1, t_mode='rand', r_mode='b'):
        print("Error: this method is deprecated")

    
    def fs_input_fetch(self, fname_tp):
        raise NameError("Error: This method is deprecated!")
        '''
        Fetch input pattern list from a input file
        pattern_list = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        '''
        input_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/'
        fr = open(input_path + fname_tp, mode='r')
        lines = fr.readlines()
        pattern_list = []
        for line in lines[1:]:
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            pattern_list.append(line_split)
        fr.close()
        return pattern_list


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


    
