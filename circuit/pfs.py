

# Please import your own libraries


### Yichen: 

class PFS():
    __init__(self):
        print("I have not been implemented yet! Maybe I'm the child of FaultSim?")

    def pfs_single(self, input_pattern):
        """
        Parallel Fault Simulation:
        For a given test pattern
        faults in self.fault_node_num 
        PFS simulates a set of faults detected by the test pattern.
        """
        faultnum = len(self.fault_node_num)
        n = sys.maxsize
        bitlen = int(math.log2(n))+1

        pass_tot = math.ceil(float(faultnum) / float(bitlen-1))

        # full fault list
        pfs_fault_val = []
        pfs_fault_num = []
        # pfs_fault_num = self.fault_node_num.copy()
        for n in self.fault_node_num:
            pfs_fault_num.append(n)
        for t in self.fault_type:
            pfs_fault_val.append(t)

        detected_fault_num = []
        detected_fault_value = []

        while (pass_tot != 0):
            pass_tot -= 1
            pfs_stuck_values = 0
            read_fault_ind = 0

            # fault list for one pass
            fault_num = []
            fault_val = []
            mask_dict = {}  # {key: fault_num, value: mask}

            # save bitlen -1 fault
            while(1):
                if len(pfs_fault_num)==0:
                    break

                fault_val.append(pfs_fault_val.pop())
                fault_num.append(pfs_fault_num.pop())

                read_fault_ind = read_fault_ind + 1
                if read_fault_ind == bitlen - 1:
                    break
            
            # calculate stuck values of faults in this pass of PFS, and mask for each fault_num
            for i in range(len(fault_val)):
                pfs_stuck_values = pfs_stuck_values + fault_val[i]*2**i

                if fault_num[i] in mask_dict:
                    mask_dict[fault_num[i]] = mask_dict[fault_num[i]] + 2**i
                else:
                    mask_dict[fault_num[i]] = 2**i
            
            #for k in range(len(fault_num)):
                #print(fault_num[k], "@",fault_val[k], "bit ",k)
            
            # pfs for one pass
            node_dict = dict(zip([x.num for x in self.PI], input_pattern))
            for node in self.nodes_lev:
                node.pfs_I = 0
                node.pfs_S = pfs_stuck_values

                # if fault should be inserted in this node
                if node.num in mask_dict:
                    node.pfs_I = mask_dict[node.num]

                if node.gtype == "IPT":
                    node.imply_p(node_dict[node.num])
                else:
                    node.imply_p()
                node.insert_f()
            
            # output result
            for i in self.nodes_lev:
                if i.ntype == 'PO':
                    # if some faults can be detected
                    if (i.pfs_V != 0) and (i.pfs_V != 2**bitlen-1):
                        pfs_V_str = format(i.pfs_V,"b").zfill(bitlen)
                        msb_pfs_V = pfs_V_str[0]        # MSB of pfs_V: good circuit
                        for j in range(bitlen-1):
                            if j == len(fault_num):
                                break
                            if pfs_V_str[bitlen-1-j] != msb_pfs_V:
                                detected_fault_num.append(fault_num[j])
                                detected_fault_value.append(fault_val[j])

        fault_set = set()
        for k in range(len(detected_fault_num)):
            fault_set = fault_set.union({(int(detected_fault_num[k]),detected_fault_value[k])})

        return fault_set


    def pfs_multiple(self, fname=None, mode="b"):
        """ prallel fault simulation (pfs) for multiple test patterns
        the pattern list is obtained as a list consists of sublists of each pattern:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (int(node_num), int(fault type))
            fault_list = [(1,0),(1,1),(8,0),(5,1),(6,1)]
        """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")
        if os.path.exists('../data/fault_sim/') == False:
            os.mkdir('../data/fault_sim/')
        input_path = '../data/modelsim/' + self.c_name + '/input/'
        fr=open(input_path + fname, mode='r')
        output_path = '../data/fault_sim/'+ fname.rstrip('_tp_b.txt') + '_pfs_out.txt'
        fw=open(output_path, mode='w')
        # drop the first row of input names
        line=fr.readline()
        # obtain a multiple test patterns list from the input file
        pattern_list = []
        for line in fr.readlines():
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            pattern_list.append(line_split)
        
        # output: detected fault list for each input pattern
        fault_list = []
        for sub_pattern in pattern_list:
            fw.write(",".join([str(elem) for elem in sub_pattern]) + '\n')
            fault_list = list(self.pfs_single(sub_pattern))
            fault_list.sort()
            for fault in fault_list:
                fw.write(str(fault[0]) + '@' + str(fault[1]) + '\n')
            fw.write('\n')
        fr.close()
        fw.close()
        print("PFS completed. \nLog file saved in {}".format(output_path))
 
