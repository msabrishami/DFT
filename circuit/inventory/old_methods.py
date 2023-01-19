    def dfs(self):
        """
        Deductive fault simulation:
        For a given test pattern,
        DFS simulates a set of faults detected by the test pattern.
        Validate the test pattern return by D or Podem
        """
        control = {'AND':0, 'NAND':0, 'OR':1, 'NOR':1}
        c_list = []
        nc_list = []
        fault_list = set()
        for item in self.nodes_sim:
            if item.gtype == 'IPT':
                item.add_faultlist((item.num, GNOT(item.value)))
                # print(item.num, item.faultlist_dfs)
            elif item.gtype == 'BRCH':
                item.faultlist_dfs = item.unodes[0].faultlist_dfs.copy()
                item.add_faultlist((item.num, GNOT(item.value)))
            elif item.gtype == 'XOR':
                s = set()
                for i in item.unodes:
                    s = s.symmetric_difference(set(i.faultlist_dfs))
                s.add((item.num, GNOT(item.value)))
                item.faultlist_dfs = list(s)
                if item.ntype == 'PO':
                    fault_list = fault_list.union(set(item.faultlist_dfs))
            elif item.gtype == 'NOT':
                item.faultlist_dfs = item.unodes[0].faultlist_dfs.copy()
                item.add_faultlist((item.num, GNOT(item.value)))
                if item.ntype == 'PO':
                    fault_list = fault_list.union(set(item.faultlist_dfs))
            else :  #gtype = gate beside xor
                flag = 0
                # find if input has control value
                for i in item.unodes:
                    c = control[item.gtype]
                    # print(item.num,i.num)
                    if i.value == c:
                        flag = 1
                        c_list.append(i)
                    else :
                        nc_list.append(i)
                # all input is no controlling value
                if flag == 0:
                    s = set()
                    for j in nc_list:
                        s = s.union(set(j.faultlist_dfs))
                    item.faultlist_dfs.clear()
                    item.faultlist_dfs = list(s)
                    item.add_faultlist((item.num, GNOT(item.value)))
                # input has control value
                else :
                    s_control = set(c_list[0].faultlist_dfs)
                    for j in c_list:
                        s_control = s_control.intersection(set(j.faultlist_dfs))
                    if nc_list == []:
                        s_ncontrol = set()
                    else:
                        s_ncontrol = set(nc_list[0].faultlist_dfs)
                        for j in nc_list:
                            s_ncontrol = s_ncontrol.union(set(j.faultlist_dfs))
                    s_control.difference(s_ncontrol)
                    item.faultlist_dfs.clear()
                    item.faultlist_dfs = list(s_control)
                    item.add_faultlist((item.num, GNOT(item.value)))
                c_list.clear()
                nc_list.clear()
                if item.ntype == 'PO':
                    fault_list = fault_list.union(set(item.faultlist_dfs))

        return fault_list

def pfs(self,input_val):
        """
        Parallel Fault Simulation:
        For a given test pattern,
        PFS simulates a set of faults detected by the test pattern.
        """
        faultnum = len(self.fault_node_num)
        n = sys.maxsize
        bitlen = int(math.log2(n))+1

        output_num = list()
        for i in self.nodes_lev:
            if i.ntype == 'PO':
                output_num.append(i.num)

        node_num = []
        node_val = []

        node_num = self.input_num_list
        node_val = input_val
        # hash map
        node_input_dict = dict(zip(node_num, node_val))

        # hash map: node_num is key, object of node is value
        node_all_num = list()
        for i in self.nodes_lev:
            node_all_num.append(i.num)
        node_dict = dict(zip(node_all_num, self.nodes_lev))
        for i in range(len(node_all_num)):
            node_dict[node_all_num[i]].parallel_value = 0

        # cal iter
        if faultnum % (bitlen-1) == 0:
            iter = int(faultnum / (bitlen - 1))
        else:
            iter = int(faultnum / (bitlen - 1))+1
        #print("the value of iter: %d"%(iter))

        # write result
        detected_node = []
        detected_node_value = []

        output_empty = 0
        pfs_fault_val = []
        pfs_fault_num = []
        for n in self.fault_node_num:
            pfs_fault_num.append(n)
        for t in self.fault_type:
            pfs_fault_val.append(t)
        while (iter != 0):
            fault_num = []
            fault_val = []
            for i in self.nodes_lev:
                i.sa0 = 0
                i.sa1 = 0
            read_fault_ind = 0
        #print("begin to while")

            # save bitlen -1 fault
            while(1):
                content1 = len(pfs_fault_num)
                if content1==0:
                    break

                fault_val.append(pfs_fault_val.pop())
                fault_num.append(pfs_fault_num.pop())


                read_fault_ind = read_fault_ind + 1
                if read_fault_ind == bitlen - 1:
                    break
            for i in range(len(fault_num)):
                if fault_val[i] == 1:
                    node_dict[fault_num[i]
                            ].sa1 = node_dict[fault_num[i]].sa1 + 2**(i+1)
                else:
                    node_dict[fault_num[i]
                            ].sa0 = node_dict[fault_num[i]].sa0 + 2**(i+1)

            for i in self.nodes_lev:
                if i.gtype == 'IPT':
                    if i.num in node_num:
                        i.parallel_value = 0
                        for j in range(bitlen):
                            i.parallel_value = i.parallel_value + \
                                (int(node_input_dict[i.num]) << j)
                        i.parallel_value = ((~i.sa0) & i.parallel_value) | i.sa1
                elif i.gtype == 'BRCH':
                    i.parallel_value = ((~i.sa0) & (
                        i.unodes[0].parallel_value)) | i.sa1

                elif i.gtype == 'XOR':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value ^ i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & temp_value) | i.sa1
                elif i.gtype == 'OR':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value | i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & temp_value) | i.sa1
                elif i.gtype == 'NOR':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value | i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & (~temp_value)) | i.sa1
                elif i.gtype == 'NOT':
                    i.parallel_value = ((~i.sa0) & (
                        ~i.unodes[0].parallel_value)) | i.sa1
                elif i.gtype == 'NAND':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value & i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & (~temp_value)) | i.sa1
                elif i.gtype == 'AND':
                    for j in range(0, i.fin):
                        if j == 0:
                            temp_value = i.unodes[j].parallel_value
                        else:
                            temp_value = temp_value & i.unodes[j].parallel_value
                    i.parallel_value = ((~i.sa0) & temp_value) | i.sa1
            iter -= 1

            for i in range(read_fault_ind):
                for j in output_num:
                    temp = node_dict[j].parallel_value
                    # t0 is to choose the value responding to the specific fault node in output
                    # t1 is to move the value to most significant bit
                    t0 = (temp & (1 << (i+1)))
                    t1 = t0 << (bitlen-i-2)
                    t2 = 1 << (bitlen-1)
                    t3 = t1 & t2
                    # t4 is to calculate most least bit which is fault free bit
                    t4 = (temp & 1) << (bitlen-1)
                    if t3 != t4:
                        if fault_num[i] not in detected_node:
                            detected_node.append(fault_num[i])
                            detected_node_value.append(fault_val[i])
                            # print(j,fault_num[i],fault_val[i])
            # output is a set of tuple
            if output_empty == 0:
                output = {(detected_node[0], detected_node_value[0])}
                output_empty += 1
            for i in range(len(detected_node)):
                output.add((detected_node[i], detected_node_value[i]))

        return output

    def FD_new_generator(self):
        """
        Creat a new FD in excel using dfs results
        """
        # output golden file
        fw_path = os.path.join(config.FAULT_DICT_DIR, self.c_name)
        if not os.path.exists(config.FAULT_DICT_DIR):
            print("Creating fault dictionary directory in {}".format(config.FAULT_DICT_DIR))
            os.mkdir(config.FAULT_DICT_DIR)
        if not os.path.exists(fw_path):
            print("Creating fault dictionary directory for circuit {} in {}".format(
                self.c_name, fw_path))
            os.mkdir(fw_path)
        fr_path = '../data/fault_sim/' + self.c_name + '/'
        fr = open(fr_path + self.c_name + '_full_dfs_out.txt','r')
        # To create Workbook
        workbook = xlwt.Workbook()   
        sheet = workbook.add_sheet("Sheet Name")  
        # Specifying style 
        # style = xlwt.easyxf('font: bold 1')     
        # Specifying column 
        PI_string = ""
        for node in self.PI:
            PI_string = PI_string + node.num + ','
        PI_string = PI_string[:-1]
        print(PI_string)
        # print(self.nodes)
        sheet.write(0, 0, PI_string)
        i = 1
        fault_mapping = {}
        for node in self.nodes_lev:
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
                
            
        # sheet.write(0, 0, 'SAMPLE')
        # for line in fr.readlines():
        # sheet.write(0, 0, 'SAMPLE') 
        # sheet.write(1, 0, 'ISBT DEHRADUN') 
        # sheet.write(2, 0, 'SHASTRADHARA') 
        # sheet.write(3, 0, 'CLEMEN TOWN') 
        # sheet.write(4, 0, 'RAJPUR ROAD') 
        # sheet.write(5, 0, 'CLOCK TOWER') 
        workbook.save(os.path.join(fw_path, self.c_name + '_FD_new.xls'))


    def D_alg(self, fault_index, imply_counter):
        """
        Given a fault, returns whether it can be detected,
        if can, returns a test pattern.
        """
        res = D_alg(self.nodes, fault_index, imply_counter)
        return res
    #to be continued
    def podem(self, i):
        """
        Given a fault, returns whether it can be detected,
        if can, returns a test pattern.
        """
        res = podem(self.fault_node_num[i], self.fault_type[i], self.nodes, self.nodes_lev)
        return res


    def read_fault_dict(self):
        """read already generated fault dictionary"""
        fd = open("../fault_dic/{}.fd".format(self.c_name),"r")
        self.fd_data = fd.read()
        fd.close()

    def get_patterns(self, test_pattern):
        """
        Given a test pattern with "X"s,
        generate all possible patterns represent by that pattern.
        """
        xidx = []
        xcnt = 0
        for i in range(len(test_pattern)):
            if test_pattern[i] == 'X':
                xidx.append(i)
                xcnt += 1

        fmt_str = '{0:0%db}'%(xcnt)
        bit = []

        plist = []
        for i in range(2 ** (xcnt)):
            bit = [int(j) for j in fmt_str.format(i)]
            plist.append(bit)

        search = []
        for p in plist:
            binary_patterns = test_pattern
            for i in range(xcnt):
                binary_patterns[xidx[i]] = p[i]
            search.append(''. join(map(str, binary_patterns)))
        return search


    def check_failure(self, fault_name):
        """
        Check if the fault is undetected by searching the fault dictionary
        called for small circuit with fault fictionary only.
        """
        srch_str = '\s{}'.format(fault_name)
        if re.findall(srch_str, self.fd_data):
            return False
        else:
            return True

    def check_success(self, fault_name, search_patterns):
        """
        Check if the returned pattern can detected the given fault
        by searching the fault dictionary.
        called for small circuit with fault fictionary only.
        """
        pattern_found = 0
        for p in search_patterns:
            srch_str = '{}.*?\s{}'.format(p, fault_name)
            # print (srch_str)
            res = re.findall(srch_str, self.fd_data)
            if res:
                pattern_found = 1
            else:
                pattern_found = 0
        if pattern_found:
            return True
        else:
            return False

    def get_Xless_pattern(self, pattern):
        """
        For big circuit with too many Xs,
        randomly assign 1 or 0 to each X and returns a pattern.
        """
        pattern_Xless = []
        for v in pattern:
            if v == 'X':
                entry = random.getrandbits(1)
            else:
                entry = v
            pattern_Xless.append(entry)
        return pattern_Xless

    def get_d_correctness(self):
        """
        Check correctness of D algorithm for both detected and undetected faults.
        Called for small circuit.
        """
        self.read_fault_dict()
        d_error_cnt = 0
        # run the faults in full fault list
        for j in range(len(self.fault_node_num)):
            fault_index = -1
            for i in range(len(self.nodes_lev)):
                self.nodes_lev[i].value = five_value.X.value
                if self.nodes_lev[i].num == self.fault_node_num[j]:
                    # stuck at 0
                    if self.fault_type[j] == 0:
                        self.nodes_lev[i].value = five_value.D.value
                        fault_index = i
                    # stuck at 1
                    elif self.fault_type[j] == 1:
                        self.nodes_lev[i].value = five_value.D_BAR.value
                        fault_index = i
                    else:
                        print("operator error")
            imply_counter = Imply_counter(8000)
            res = self.D_alg(fault_index, imply_counter)

            # If the fault is detectable in
            if res.result == 1:
                # print("D_alg SUCCESS")
                search_patterns = self.get_patterns(res.pattern)
                pattern_found = self.check_success(self.fault_name[j], search_patterns)
                if pattern_found == 0:
                    print("D algorithm Error at fault {}, type SUCCESS".format(self.fault_name[j]))
                    d_error_cnt += 1
                else:
                    pass

            else:
                # print("D_alg FAILURE")
                error_not_found = self.check_failure(self.fault_name[j])
                if error_not_found == 0:
                    print("D algorithm Error at fault {}, type FAILURE".format(self.fault_name[j]))
                    d_error_cnt += 1
                else:
                    pass
        self.d_correctness_rate = ((len(self.fault_node_num) - d_error_cnt) / len(self.fault_node_num)) * 100
        print ("D algorithm correctness rate: {}%".format(self.d_correctness_rate))

    def get_d_coverage(self):
        """
        Count the percentage of faults in the full fault list D algorithm claimed as detected.
        Further revise the coverage by passing the test pattern returned by D to DFS to see
        if the given fault is in the detected fault set.
        called for big circuits
        """
        failure_fault_list = []
        check_cnt = 0
        self.pass_cnt = 0

        for j in range(len(self.fault_node_num)):
            fault_index = -1
            for i in range(len(self.nodes)):
                if self.nodes[i].num == self.fault_node_num[j]:
                    # stuck at 0
                    if self.fault_type[j] == 0:
                        self.nodes[i].d_value.append(five_value.D.value)
                        fault_index = i
                    # stuck at 1
                    elif self.fault_type[j] == 1:
                        self.nodes[i].d_value.append(five_value.D_BAR.value)
                        fault_index = i
                    else:
                        print("operator error")
                else:
                    self.nodes[i].d_value.append(five_value.X.value)
            imply_counter = Imply_counter(8000)
            res = self.D_alg(fault_index, imply_counter)

            if res.result == 1:
                self.pass_cnt += 1

            else:
                failure_fault_list.append(self.fault_name[j])


            check_cnt += 1
            print ("check_cnt={}".format(check_cnt))
        self.d_coverage = (self.pass_cnt / len(self.fault_node_num)) * 100
        print ("D algorithm fault coverage: {}".format(self.d_coverage))
        self.pass_cnt = 0
        return failure_fault_list

    def get_podem_correctness(self):
        """
        Check correctness of Podem for both detected and undetected faults.
        Called for small circuit.
        """
        self.read_fault_dict()
        pd_error_cnt = 0
        for i in range(len(self.fault_node_num)):
            res = self.podem(i)
            if res.result == 1:
                search_patterns = self.get_patterns(res.pattern)
                pattern_found = self.check_success(self.fault_name[i], search_patterns)
                if pattern_found == 0:
                    print("Podem algorithm Error at fault {}, type SUCCESS".format(self.fault_name[i]))
                    pd_error_cnt += 1
                else:
                    pass
            else:
                # print("Podem_alg FAILURE")
                error_not_found = self.check_failure(self.fault_name[i])
                if error_not_found == 0:
                    print("Podem algorithm Error at fault {}, type FAILURE".format(self.fault_name[i]))
                    pd_error_cnt += 1
                else:
                    pass
        self.pd_correctness_rate = ((len(self.fault_node_num) - pd_error_cnt) / len(self.fault_node_num)) * 100
        print ("Podem algorithm correctness rate: {}%".format(self.pd_correctness_rate))

    def get_podem_coverage(self):
        """
        Count the percentage of faults in the full fault list Podem claimed as detected.
        Further revise the coverage by passing the test pattern returned by Podem to DFS to see
        if the given fault is in the detected fault set.
        called for big circuits
        """
        self.pass_cnt = 0
        for i in range(len(self.fault_node_num)):
            res = self.podem(i)
            if res.result == 1:
                self.pass_cnt += 1
                pattern = res.pattern
                input_pattern = self.get_Xless_pattern(pattern)
                # print(input_pattern)
                self.logic_sim(input_pattern)
                fault_set = self.dfs()
                fault = (self.fault_node_num[i],self.fault_type[i])
                if fault in fault_set:
                    pass
                else:
                    self.pass_cnt -= 1
                    print("Test Pattern error for Podem at fault {}".format(fault))
            else:
                pass
        self.pd_coverage = self.pass_cnt / len(self.fault_node_num) * 100
        self.pass_cnt = 0
        print ("Podem algorithm fault coverage: {}%".format(self.pd_coverage))


    def podem_single_test(self, fault_node_num, fault_type):
        res = podem(fault_node_num, fault_type, self.nodes, self.nodes_lev)
        return res


    def time_for_podem(self):
        totaltime = 0
        for i in range(len(self.fault_node_num)):
            starttime = time.time()
            res = self.podem_single_test(self.fault_node_num[i], self.fault_type[i])
            endtime = time.time()
            totaltime = totaltime + (endtime - starttime)
        print(totaltime)


# prevent D algorithm deadlock. For debug purposes only
class Imply_counter:
    def __init__(self, abort_cnt):
        self.cnt = 0
        self.abort_cnt = abort_cnt
    def increment(self):
        self.cnt += 1
    def initialize(self):
        self.cnt = 0

    # Circuit
    def gen_fault_dic_multithreading(self, thread_cnt, idx):
        """
        Create threads to generate fault dictionaries.
        Speed up the fault dictionary generation process.
        """
        fault_dict = {}
        total_pattern = pow(2, self.input_cnt)
        pattern_per_thread = int(total_pattern / thread_cnt)

        for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
            #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
            b = ('{:0%db}'%self.input_cnt).format(i)
            list_to_pfs = []
            for j in range(self.input_cnt):
                list_to_pfs.append(int(b[j]))
        #do pfs based on the prodeuced input files
            result = []
            result = self.pfs(list_to_pfs)
            fault = []
            #print(result)
            for i in result:
                fault.append("%d@%d" % (i[0], i[1]))

            fault.sort(key = lambda i:int(re.match(r'(\d+)',i).group()))
            fault_dict.update({b: fault})

        with open ("../fault_dic/{}_{}.fd".format(self.c_name, idx), "w") as fo:
            for i in range(self.input_cnt):
                if (i < self.input_cnt - 1):
                    fo.write('%d->' % self.input_num_list[i])
                else:
                    fo.write('%d' % self.input_num_list[i])
            fo.write(' as sequence of inputs')
            fo.write('\n')
            fo.write('input_patterns\t\t\tdetected_faults\n')
            for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
                b = ('{:0%db}'%self.input_cnt).format(i)
                fo.write('%s\t\t\t\t' % b)
                for i in range(len(fault_dict.get(b))):
                    fo.write('%-5s ' % fault_dict.get(b)[i])#format ok?
                fo.write('\n')
        print("thread #{} of {} threads finished".format(idx, thread_cnt))

    # Circuit
    def get_reduced_fault_list(self):
        """
        Using checkpoint theorem,
        generate reduced fault list
        """
        faults_fanout = []
        for i in range(len(self.nodes)):
            if (self.nodes[i].cpt == 1):
                #print self.nodes[i].num
                for j in range(self.nodes[i].fout):
                    faults_fanout.append(self.nodes[i].dnodes[j].index)
                self.nodes[i].sa0 = 1
                self.nodes[i].sa1 = 1
        # uniquefanout = sorted(set(faults_fanout))
        # print uniquefanout
        for i in range(len(faults_fanout)):
            cptflag = 0
            if ((self.nodes[faults_fanout[i]].gtype == 'NOR') or (self.nodes[faults_fanout[i]].gtype == 'OR')):
                for j in range(self.nodes[faults_fanout[i]].fin):
                    if self.nodes[faults_fanout[i]].unodes[j].cpt == 1:
                        if cptflag == 0:
                            cptflag = 1
                        else: self.nodes[faults_fanout[i]].unodes[j].sa1 = 0
            elif ((self.nodes[faults_fanout[i]].gtype == 'NAND') or (self.nodes[faults_fanout[i]].gtype == 'AND')):
                for j in range(self.nodes[faults_fanout[i]].fin):
                    if self.nodes[faults_fanout[i]].unodes[j].cpt == 1:
                        if cptflag == 0:
                            cptflag = 1
                        else: self.nodes[faults_fanout[i]].unodes[j].sa0 = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].sa0 == 1:
                self.rfl_node.append(self.nodes[i].num)
                self.rfl_ftype.append(0)
            if self.nodes[i].sa1 == 1:
                self.rfl_node.append(self.nodes[i].num)
                self.rfl_ftype.append(1)
 
