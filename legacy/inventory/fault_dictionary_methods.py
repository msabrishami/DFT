"""Code removed from pycad because it cannot run (undefined names or missing
dependencies) and nothing called it. Kept here for reference only.

Source: DFTCircuit (pycad/circuit/dft_circuit.py): fault dictionary methods
"""

    def gen_fault_dic(self):
        """
        Fault Dictionary:
        key: input pattern value: detected fault (returned by PFS)
        Fault Dictionary can only be generated for small circuits
        because the file size will become too large for big circuits.
        """
        fault_dict = {}
        inputnum = len(self.input_num_list)
        total_pattern = pow(2,inputnum) # produce 2^n different input files for pfs to use

        for i in range(total_pattern):
            print ('{:05b}'.format(i)) #str type output #Suit different input numbers!!!!
            # b = (f'{i:0%db}'%inputnum)
            list_to_pfs = []
            for j in range(inputnum):
                list_to_pfs.append(int(b[j]))

            #do pfs based on the prodeuced input files
            result = []
            result = self.pfs(list_to_pfs)
            fault = []
            for i in result:
                fault.append("%d@%d" % (i[0], i[1]))

            fault.sort(key = lambda i:int(re.match(r'(\d+)',i).group()))
            #jb51.net/article/164342.htm for referance to sort the output

            fault_dict.update({b: fault})

        fault_dict_result = open(f"../fault_dic/{self.c_name}.fd", "w")
        for i in range(len(self.input_num_list)):
            if (i<len(self.input_num_list)-1):
                fault_dict_result.write('%d->' % self.input_num_list[i])
            else:
                fault_dict_result.write('%d' % self.input_num_list[i])

        fault_dict_result.write(' as sequence of inputs')
        fault_dict_result.write('\n')
        fault_dict_result.write('tps\t\t\tdetected_faults\n')
        for i in range(total_pattern):
            print ('{:05b}'.format(i)) #str type output #Suit different input numbers!!!!
            # b = (f'{i:0%db}'%inputnum)
            fault_dict_result.write('%s\t\t\t\t' % b)
            for i in range(len(fault_dict.get(b))):
                fault_dict_result.write('%-5s ' % fault_dict.get(b)[i])#format ok?
            fault_dict_result.write('\n')

        fault_dict_result.close()

    def gen_fault_dic_multithreading(self, thread_cnt, idx):
        """
        Create threads to generate fault dictionaries.
        Speed up the fault dictionary generation process.
        """
        fault_dict = {}
        total_pattern = pow(2, len(self.PI))
        pattern_per_thread = int(total_pattern / thread_cnt)

        for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
            print ('{:05b}'.format(i)) #str type output #Suit different input numbers!!!!
            # b = (f'{i:0%db}'%len(self.PI))
            list_to_pfs = []
            for j in range(len(self.PI)):
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

        with open (f"../fault_dic/{self.c_name}_{idx}.fd", "w") as fo:
            for i in range(len(self.PI)):
                if (i < len(self.PI) - 1):
                    fo.write('%d->' % self.input_num_list[i])
                else:
                    fo.write('%d' % self.input_num_list[i])
            fo.write(' as sequence of inputs')
            fo.write('\n')
            fo.write('tps\t\t\tdetected_faults\n')
            for i in range(idx * pattern_per_thread, (idx + 1) * pattern_per_thread):
                b = (f'{i:0%db}'%len(self.PI))
                fo.write('%s\t\t\t\t' % b)
                for i in range(len(fault_dict.get(b))):
                    fo.write('%-5s ' % fault_dict.get(b)[i])#format ok?
                fo.write('\n')
        print(f"thread #{idx} of {thread_cnt} threads finished")
    
    def read_fault_dict(self):
        """read already generated fault dictionary"""
        fd = open(f"../fault_dic/{self.c_name}.fd","r")
        self.fd_data = fd.read()
        fd.close()
