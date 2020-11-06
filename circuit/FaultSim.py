import config


class FaultSim:
    def __init__(self, circuit):
        self.circuit = circuit
        # fault sim type: dfs / pfs
        self.fs_type = ""
        

    def fs_folder(self, tp_mode='rand', r_mode='b'):
        '''
        Create all folder needed for fault simulation
        '''
        # create folder for whole fault sim of the given circuit
        tp_path = config.FAULT_SIM_DIR
        if not os.path.exists(tp_path):
            os.mkdir(tp_path)
            print("Creating fault dictionary directory in {}".format(config.FAULT_DICT_DIR))
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/'
        if not os.path.exists(tp_path):
            os.mkdir(tp_path)

        # create folder for input patterns
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/'
        if not os.path.exists(tp_path):
            os.mkdir(tp_path)
        # create folder for dfs/pfs log files
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/dfs/'
        if not os.path.exists(tp_path):
            os.mkdir(tp_path)
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/pfs/'
        if not os.path.exists(tp_path):
            os.mkdir(tp_path)
        # create folder for dfs/pfs compare results
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/compare/'
        if not os.path.exists(tp_path):
            os.mkdir(tp_path)


    def fs_tp_gen(self, tp_num=1, t_mode='rand', r_mode='b'):
        '''
        Generate test patterns for DFS/PFS
        rand: random mode, create certain number of random test pattterns
        full: create all possible test patterns in order
        '''
        tp_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/'
        if t_mode == 'rand':
            tp_fname = tp_path + self.circuit.c_name + '_' + str(tp_num) + '_tp_' + r_mode + '.txt'
            self.circuit.gen_tp_file(
                tp_num, 
                fname = tp_fname,
                mode = "b")
        elif t_mode == 'full':
            tp_fname = tp_path + self.circuit.c_name + '_full_tp_' + r_mode + '.txt'
            num = len(self.circuit.PI)
            times = pow(2, num)
            pattern = []
            fw = open(tp_fname, mode='w')
            PI_list = []
            for node in self.circuit.PI:
                PI_list.append(node.num)
            PI_string = ','.join(PI_list)
            print(PI_string)
            fw.write(PI_string + '\n')
            for i in range(times):
                pattern = list(bin(i)[2:].zfill(num))
                pattern_str = ",".join(pattern)
                print(pattern_str)
                fw.write(pattern_str + '\n')
        else: 
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")



    def fs_input_fetch(self, fname_tp):
        '''
        Fetch input pattern list from a input file
        pattern_list = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        '''
        output_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + self.fs_type + '/'
        input_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/input/'
        fr = open(input_path + fname_tp, mode='r')
        # read the test pattern
        lines = fr.readlines()
        # obtain a multiple test patterns list from the input file
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

        output_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + self.fs_type + '/'
        fw = open(output_path + fname_log, mode='w')
        for sub_pattern in pattern_list:
            # print("hello pattern list")
            fault_subset = self.single(sub_pattern)
            fault_sublist = list(fault_subset)
            updated_fault_sublist = []
            for subset in fault_sublist:
                if '-' in subset[0]:
                    updated_fault_sublist.append((subset[0].split('-')[0], subset[0].split('-')[1], subset[1]))
                else:
                    updated_fault_sublist.append((subset[0], '0', subset[1]))
            updated_fault_sublist.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
            pattern_str = map(str,sub_pattern)
            pattern_str = ",".join(pattern_str)
            fw.write(pattern_str + '\n')
            fault_coverage = float(len(fault_sublist) / (2*len(self.circuit.nodes_lev)))
            for fault in updated_fault_sublist:
                if fault[1] == '0':
                    fw.write(str(fault[0]) + '@' + str(fault[2]) + '\n')
                else:
                    fw.write(str(fault[0]) + '-' + str(fault[1]) + '@' + str(fault[2]) + '\n')
            fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
            fw.write('\n')
        fw.close()
        print(self.fs_type + "-Separate completed. \nLog file saved in {}".format(fname_log))



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
        output_path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + self.fs_type + '/'
        fw = open(output_path + fname_log, mode='w')
        fault_set = set()
        for sub_pattern in pattern_list:
            # print("hello pattern list")
            fault_subset = self.single(sub_pattern)
            fault_set = fault_set.union(fault_subset)
        # generate output file
        fault_list = list(fault_set)
        updated_fault_list = []
        for subset in fault_list:
            if '-' in subset[0]:
                updated_fault_list.append((subset[0].split('-')[0], subset[0].split('-')[1], subset[1]))
            else:
                updated_fault_list.append((subset[0], '0', subset[1]))
        #fault_list.sort(key=lambda x: (int(x[0]), int(x[1])))
        updated_fault_list.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
        # fault is a tuple like: (1,0): node 1 ss@0
        fault_coverage = float(len(fault_list) / (2*len(self.circuit.nodes_lev)))
        for fault in updated_fault_list:
            if fault[1] == '0':
                fw.write(str(fault[0]) + '@' + str(fault[2]) + '\n')
            else:
                fw.write(str(fault[0]) + '-' + str(fault[1]) + '@' + str(fault[2]) + '\n')
        fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
        fw.close()
        print(self.fs_type + "-Multiple completed. \nLog file saved in {}".format(fname_log))



    def fs_exe(self, tp_num=1, t_mode='rand', r_mode='b'):
        """
        Defined in extended class: DFS, PFS
        """
        raise NotImplementedError()



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
