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


