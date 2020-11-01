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


