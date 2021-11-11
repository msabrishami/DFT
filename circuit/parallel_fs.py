
import sys
import math
import pdb
import config

from circuit import Circuit
from node import Node
from fault_sim import FaultSim


class PFS(FaultSim):
    """ 
    Parallel Fault Single Pattern, Fault Simulation 
    """
    def __init__(self, circuit):
        super().__init__(circuit)
        self.fs_type = "pfs"
        self.wordlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**self.wordlen-1
    
    def fs_for_atpg(self, faultset, ipt_pattern):
        raise NameError("Error: this method is not updated!")
        self.add_fault(mode="atpg", fname=None, faultset = faultset)
        return self.single(ipt_pattern)
    
    
    def add_fault(self, mode="full", fname=None, faultset=None):
        # raise NameError("Error: this method is deprecated!")
        """ add faults to the fault list 
        mode = full: input fault list is full fault list
        mode = user: input fault list is given by user as a file name
        """
        #TODO: why did we overloaded this method from super? 
        if mode == "full":
            # self.circuit.get_full_fault_list()
            self.fault_list.add_all(self.circuit)
            # self.in_fault_num = self.circuit.fault_node_num
            # self.in_fault_type = self.circuit.fault_type
        elif mode == "user":
            fr = open(fname, mode='r')
            lines = fr.readlines()
            for line in lines:
                line=line.rstrip('\n')
                line_split=line.split('@')
                self.in_fault_num.append(line_split[0])
                self.in_fault_type.append(int(line_split[1]))
        elif mode == "atpg":
            for fault in faultset:
                self.in_fault_num.append(fault[0])
                self.in_fault_type.append(int(fault[1]))
        
        else:
            raise NameError("fault list type is not accepted")
    
   
    def single(self, input_pattern, fault_drop):
        """
        For one test pattern, and all faults in the fault list 
        No fault dropping is used 
        Updates the fault.D_count for now
        Returns a list of detected faults in this pass
        """        
        detected_faults = []
        
        ptr0 = 0
        while (ptr0 < len(self.fault_list.faults)):
            pfs_stuck_values = 0
            read_fault_ind = 0

            # fault list for one pass
            mask_dict = {}  # {key: fault_num, value: mask}
            faults_pass = []
            faults_pass_idx = []
            if fault_drop:
                
                ptr1 = ptr0
                while(len(faults_pass) < self.wordlen-1 and \
                        ptr1 != len(self.fault_list.faults)):
                    fault = self.fault_list.faults[ptr1]
                    if (fault.D_count < fault_drop):
                        faults_pass.append(fault)
                        faults_pass_idx.append(ptr1)
                    ptr1 += 1
            else:
                ptr1 = min(ptr0+self.wordlen-2, len(self.fault_list.faults)-1)
                for x in range(ptr0, ptr1+1):
                    faults_pass.append(self.fault_list.faults[x])
                    faults_pass_idx.append(x)
            
            # print("processing faults from {}-{}".format(ptr0, ptr1))
            ptr0 = ptr1+1

            for i in range(len(faults_pass)):
                pfs_stuck_values += int(faults_pass[i].stuck_val) * (2**i)

                if faults_pass[i].node_num in mask_dict:
                    mask_dict[faults_pass[i].node_num] += 2**i
                else:
                    mask_dict[faults_pass[i].node_num] = 2**i

            # for k, v in mask_dict.items():
            #     print("{}:\t{:b}".format(k, v))

            # print("{:b}".format(pfs_stuck_values))
            
            # pfs for one pass
            node_dict = dict(zip([x.num for x in self.circuit.PI], input_pattern))
            for node in self.circuit.nodes_lev:

                # PFS mask 
                node.pfs_I = 0
                if node.num in mask_dict:
                    node.pfs_I = mask_dict[node.num]
                
                # Simple parallel simulation of a node 
                if node.gtype == "IPT":
                    node.imply_p(self.bitwise_not, node_dict[node.num])
                else:
                    node.imply_p(self.bitwise_not)
                
                # Fault injection 
                node.insert_f(self.bitwise_not, pfs_stuck_values)
            
            # output result
            for i in self.circuit.PO:
                # if some faults can be detected
                if (i.pfs_V != 0) and (i.pfs_V != self.bitwise_not):
                    pfs_V_str = format(i.pfs_V,"b").zfill(self.wordlen)
                    msb_pfs_V = pfs_V_str[0]        # MSB of pfs_V: good circuit
                    for j in range(self.wordlen-1):
                        if pfs_V_str[self.wordlen-1-j] != msb_pfs_V:
                            # tp found this fault_pass[j]
                            faults_pass[j].D_count += 1
                            detected_faults.append(faults_pass[j])

        # fault_set = set()
        # for k in range(len(detected_fault_num)):
        #     fault_set = fault_set.union({(detected_fault_num[k],detected_fault_value[k])})
        print("Done -- detected {} faults".format(len(detected_faults)))
        return detected_faults 


    def multiple_separate(self, tps, fname_log):
        raise NameError("Error: this method is not tested!")
        """ 
        FS for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [('1','0'),('1','1'),('8','0'),('5','1'),('6','1')]
        """
        
        fname_out = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + \
                self.fs_type + '/' + fname_log
        fw = open(fname_out, mode='w')
        for tp in tps:
            fault_subset = self.single(tp)
            pattern_str = map(str, tp)
            pattern_str = ",".join(pattern_str)
            fw.write(pattern_str + '\n')
            fault_coverage = float(len(fault_subset) / (2*len(self.circuit.nodes_lev)))
            for fault in fault_subset:
                fw.write(str(fault[0]) + '@' + str(fault[1]) + '\n')
            fw.write("Fault Coverage = " + str(fault_coverage) + '\n')
            fw.write('\n')
        fw.close()
        print(self.fs_type + " (Separate mode) completed. ")
        print("Fault coverage = {:.2f}%".format(fault_coverage))
        print("Log file saved in {}".format(fname_out))


    def multiple(self, tps, fname_log, fault_drop=None):
        """ 
        new dfs for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        fault_list should be like the following format: (string in the tuples)
            fault_list = [('1','0'),('1','1'),('8','0'),('5','1'),('6','1')]
        """

        for tp in tps:
            detected_faults = self.single(tp, fault_drop)
            # fault_set = fault_set.union(detected_faults)
            # self.fault_set_rest = self.fault_set_rest.difference(detected_faults)
        
        fault_coverage = self.fault_list.calc_fc() 
        
        output_path = "{}/{}/{}/{}".format(config.FAULT_SIM_DIR, 
                self.circuit.c_name, self.fs_type, fname_log)
        outfile = open(output_path, mode='w')
        for fault in self.fault_list.faults:
            if fault.D_count > 0:
                outfile.write(str(fault) + '\n')
        outfile.write("Fault Coverage = " + str(fault_coverage) + '\n')
        outfile.close()
        print("Fault coverage = {:.2f}%".format(fault_coverage*100))
        print("{}-Multiple completed. \nLog file saved in {}".format(
            self.fs_type, output_path))

    
    def fs_exe(self, tp_fname, fault_list_type):
        """
        Execute pfs in rand or full mode
        Arguments:
        ---------
        tp_num : int
                number of test patterns to be used for fault sim
        t_mode : string 
                can be rand or full
                rand: the total faults can be detected by several random patterns
                full: the faults can be detected by each single pattern; 
                all possible patterns are included
        """
        self.fs_folder()
        print("PFS for tp file: {}".format(tp_fname))
        tps = self.circuit.load_tp_file(tp_fname)
        print(tps)
        print("----------------------")


        # report_fname = self.circuit.c_name + '_' + str(tp_num) + \
        #         '_' + self.fs_type + '_'+ r_mode + '.log'
        report_fname = "./some_report_fname.log"
        # self.multiple(tps=tps, fname_log=report_fname, fault_drop=5)
        self.multiple(tps=tps, fname_log=report_fname)
        print("PFS completed")
        for fault in self.fault_list.faults:
            if fault.D_count > 0:
                print(fault, fault.D_count)
        print("FC={:.4f}%, tot-faults={}".format(
            100*self.fault_list.calc_fc(), len(self.fault_list.faults)))

        # elif t_mode == 'full':
        #     report_fname = self.circuit.c_name + \
        #             '_full_' + self.fs_type + '_' + r_mode + '.log'
        #     tp_fname = self.circuit.c_name + '_full_tp_' + r_mode + '.tp'
        #     self.fs_tp_gen(tp_num, t_mode = 'full', r_mode = r_mode)
        #     tps = self.fs_input_fetch(tp_fname)
        #     self.multiple_separate(tps=tps, \
        #             fname_log=report_fname, mode="b")

        # else:
        #     raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")
    
