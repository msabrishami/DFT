



### Ruochen: 

class DFS():
    __init__(self):
        print("I have not been implemented yet! Maybe I'm the child of FaultSim?")

    
    def dfs_single(self, input_pattern):
        """ running deductive fault simulation on the circuit 
        needs to make sure the levelization is updated """ 
        self.logic_sim(input_pattern)
        fault_set = set()
        for node in self.nodes_lev:
            node.dfs()
        for node in self.PO:
            fault_set = fault_set.union(node.faultlist_dfs)
        # return a fault list / set??????????
        return list(fault_set)
   

    def dfs_multiple_separate(self, fname_tp, fname_log, mode="b"):
        """ 
        new dfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [('1','0'),('1','1'),('8','0'),('5','1'),('6','1')]
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")
        # if os.path.exists('../data/fault_sim/') == False:
        #     os.mkdir('../data/fault_sim/')
        # input_path = '../data/modelsim/' + self.c_name + '/input/'
        # if os.path.exists(input_path) == False:
        #     os.mkdir(input_path)
        # output_path = '../data/fault_sim/' + self.c_name + '/'
        # if os.path.exists(output_path) == False:
        #     os.mkdir(output_path)
        fr = open(fname_tp, mode='r')
        # output_path = output_path + fname.rstrip('tp_b.txt') + '_dfs_out.txt'
        fw = open(fname_log, mode='w')
        
        lines = fr.readlines()
        # obtain a multiple test patterns list from the input file
        pattern_list = []
        for line in lines[1:]:
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            pattern_list.append(line_split)
        for sub_pattern in pattern_list:
            # print("hello pattern list")
            fault_subset = self.dfs_single(sub_pattern)
            fault_sublist = list(fault_subset)
            fault_sublist.sort(key=lambda x: (int(x[0]), int(x[1])))
            pattern_str = map(str,sub_pattern)
            pattern_str = ",".join(pattern_str)
            fw.write(pattern_str + '\n')
            for fault in fault_sublist:
                fw.write(str(fault[0]) + '@' + str(fault[1]) + '\n')
            fw.write('\n')
        fr.close()
        fw.close()
        print("DFS-Separate completed. \nLog file saved in {}".format(fname_log))


    def dfs_multiple(self, fname_tp, fname_log, mode="b"):
        """ 
        new dfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [('1','0'),('1','1'),('8','0'),('5','1'),('6','1')]
        """
        # if mode not in ["b", "x"]:
        #     raise NameError("Mode is not acceptable")
        # if os.path.exists(config.FAULT_SIM_DIR) == False:
        #     os.mkdir(config.FAULT_SIM_DIR)
        # input_path = '../data/modelsim/' + self.c_name + '/input/'
        # if os.path.exists(input_path) == False:
        #     os.mkdir(input_path)
        # output_path = '../data/fault_sim/' + self.c_name + '/'
        # if os.path.exists(output_path) == False:
        #     os.mkdir(output_path)
        fr = open(fname_tp, mode='r')
        # output_path = output_path + fname.rstrip('tp_b.txt') + '_dfs_out.txt'
        fw = open(fname_log, mode='w')
        # drop the first row of input names
        line = fr.readline()
        # obtain a multiple test patterns list from the input file
        pattern_list = []
        for line in fr.readlines():
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            pattern_list.append(line_split)
        # print(pattern_list)
        fault_set = set()
        for sub_pattern in pattern_list:
            # print("hello pattern list")
            fault_subset = self.dfs_single(sub_pattern)
            fault_set = fault_set.union(fault_subset)
        # generate output file
        fault_list = list(fault_set)
        # print(fault_list)
        fault_list.sort(key=lambda x: (int(x[0]), int(x[1])))
        # fault is a tuple like: (1,0): node 1 ss@0
        for fault in fault_list:
             fw.write(str(fault[0]) + '@' + str(fault[1]) + '\n')
             # print(str(fault[0]) + '@' + str(fault[1]) + '\n')
        fr.close()
        fw.close()
        print("DFS-Multiple completed. \nLog file saved in {}".format(fname_log))


