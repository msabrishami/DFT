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
        elif fault_list_type == "user":
            fr = open(fname, mode='r')
            for line in fr:
                line=line.rstrip('\n').split("@")
                self.in_fault_num.append(line[0])
                self.in_fault_type.append(int(line[1]))
        else:
            raise NameError("fault list type is not accepted")



class FaultList_2:
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

    def write_file(self, fname):
        with open(fname, "w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "\n")
            print("Fault list is stored in {}".format(fname))

    def write_file_extra(self, fname):
        with open(fname, "w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "," + ",".join([str(x) for x in fault.D_count])+"\n")
            print("Fault list with D_counts is stored in {}".format(fname))

class FaultSim:
    
    def __init__(self, circuit):
        self.circuit = circuit
        self.flist = FaultList()
        # fault sim type: dfs / pfs
        self.fs_type = ""
        # 12.1 added
        self.fault_set_all = set()
        for node in self.circuit.nodes_lev:
            self.fault_set_all.add((node.num,0))
            self.fault_set_all.add((node.num,1))
        self.fault_set_rest = self.fault_set_all
     

    def fs_folder(self, tp_mode='rand', r_mode='b'):
        '''
        Create all directories required for fault simulation
        '''
        # create folder for whole fault sim of the given circuit
        paths = [config.FAULT_SIM_DIR, config.FAULT_DICT_DIR, 
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/', 
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/', 
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/dfs/', 
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/pfs/', 
                config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/compare/']
        
        for path in paths:
            if not os.path.exists(path):
                print("Creating dir in {}".format(path))
                os.mkdir(path)
               

    def fs_tp_gen(self, tp_num, t_mode, r_mode='b'):
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
        '''DFS/PFS for single test pattern'''
        raise NotImplementedError()


    def fs_for_atpg(self):
        '''DFS/PFS for ATPG use'''
        raise NotImplementedError()


    def multiple_separate(self, pattern_list, fname_log, mode="b"):
        """ 
        new dfs/pfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [('1','0'),('1','1'),('8','0'),('5','1'),('6','1')]
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")  

        fname_out = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + \
                self.fs_type + '/' + fname_log
        fw = open(fname_out, mode='w')
        for sub_pattern in pattern_list:
            fault_subset = self.single(sub_pattern)
            pattern_str = map(str,sub_pattern)
            pattern_str = ",".join(pattern_str)
            fw.write(pattern_str + '\n')
            fault_coverage = float(len(fault_subset) / (2*len(self.circuit.nodes_lev)))
            for fault in fault_subset:
                fw.write(str(fault[0]) + '@' + str(fault[1]) + '\n')
            fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
            fw.write('\n')
        fw.close()
        print(self.fs_type + " (Separate mode) completed. ")
        print("Log file saved in {}".format(fname_out))


    def multiple(self, pattern_list, fname_log, mode="b"):
        """ 
        new dfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [('1','0'),('1','1'),('8','0'),('5','1'),('6','1')]
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")
        output_path = "{}/{}/{}/{}".format(config.FAULT_SIM_DIR, 
                self.circuit.c_name, self.fs_type, fname_log)

        fw = open(output_path, mode='w')
        fault_set = set()
        for sub_pattern in pattern_list:
            fault_subset = self.single(sub_pattern)
            fault_set = fault_set.union(fault_subset)
            self.fault_set_rest = self.fault_set_rest.difference(fault_set)
        fault_coverage = float(len(fault_set) / (2*len(self.circuit.nodes_lev)))
        for fault in fault_set:
            fw.write(str(fault[0]) + '@' + str(fault[1]) + '\n')
        
        fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
        fw.close()
        print("{}-Multiple completed. \nLog file saved in {}".format(
            self.fs_type, output_path))
    

    def fs_exe(self, tp_num=1, t_mode='rand', r_mode='b'):
        """ Defined in children: DFS, PFS """
        raise NotImplementedError()


    # 12.1 added
    def return_rest_fault(self):
        return self.fault_set_rest

    def FD_new_generator(self):
        """
        Creat a new FD in excel using dfs results
        """
        # output golden file
        fw_path = config.FAULT_DICT_DIR + '/' + self.circuit.c_name + '/'
        fr_path = config.FAULT_DICT_DIR + '/' + self.circuit.c_name + '/dfs/'
        fr = open(fr_path + self.circuit.c_name + '_full_dfs_b.log','r')
        # To create Workbook
        workbook = xlwt.Workbook()   
        sheet = workbook.add_sheet("Sheet Name")  
        # Specifying style 
        # style = xlwt.easyxf('font: bold 1')     
        # Specifying column 
        PI_string = ""
        for node in self.circuit.PI:
            PI_string = PI_string + node.num + ','
        PI_string = PI_string[:-1]
        print(PI_string)
        # print(self.nodes)
        sheet.write(0, 0, PI_string)
        i = 1
        fault_mapping = {}
        for node in self.circuit.nodes_lev:
            sheet.write(0, i, node.num + '@' + '0')
            fault_mapping[node.num + '@' + '0'] = i
            sheet.write(0, i+1, node.num + '@' + '1')
            fault_mapping[node.num + '@' + '1'] = i+1
            print(0, i, node.num + '@' + '0')
            print(0, i+1, node.num + '@' + '1')
            i = i + 2
        j = 1
        sheet.write(j, 0, fr.readline()) 
        for line in fr.readlines():
            if line == '\n':
                j = j + 1
            elif '@' in line:
                sheet.write(j, fault_mapping[line[:-1]], 'X')
            else:
                sheet.write(j, 0, line)

        workbook.save(os.path.join(fw_path, self.circuit.c_name + '_FD_new.xls'))
