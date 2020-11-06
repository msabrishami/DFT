import sys
from circuit import *
from node import *
from FaultSim import *

class PFS(FaultSim):
    def __init__(self, circuit):
        FaultSim.__init__(self, circuit)
        self.in_fault_num = [] # input fault num, string format
        self.in_fault_type = [] # input fault type, integer format
        self.fs_type = "PFS"
    
    def pfs_in_fault_list(self,fname,fault_list_type):
        """
        Parallel Fault Simulation:
        fault_list_type = 1: input fault list is full fault list
        fault_list_type = 0: input fault list is given by user.

        For a given input fault list
        generate two lists: in_fault_num, in_fault_type.
        """
        self.in_fault_num = []
        self.in_fault_type = []
        if fault_list_type == 1:
            self.circuit.get_full_fault_list()
            self.in_fault_num = self.circuit.fault_node_num
            self.in_fault_type = self.circuit.fault_type
        else:
            fr = open(fname, mode='r')
            lines = fr.readlines()
            for line in lines:
                line=line.rstrip('\n')
                line_split=line.split('@')
                self.in_fault_num.append(line_split[0])
                self.in_fault_type.append(int(line_split[1]))
    
    def single(self, input_pattern):
        """
        Parallel Fault Simulation:
        For a given test pattern
        PFS simulates a set of faults detected by the test pattern
        fault_set = {('1','0'),('1','1'),('8','0'),('5','1'),('6','1')}
        """        
        pfs_fault_num = self.in_fault_num.copy()
        pfs_fault_val = self.in_fault_type.copy()
        faultnum = len(self.in_fault_num)

        n = sys.maxsize
        bitlen = int(math.log2(n))+1
        bitwise_not = 2**bitlen-1

        pass_tot = math.ceil(float(faultnum) / float(bitlen-1))

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
            
            # pfs for one pass
            node_dict = dict(zip([x.num for x in self.circuit.PI], input_pattern))
            for node in self.circuit.nodes_lev:
                node.pfs_I = 0
                node.pfs_S = pfs_stuck_values

                # if fault should be inserted in this node
                if node.num in mask_dict:
                    node.pfs_I = mask_dict[node.num]

                if node.gtype == "IPT":
                    node.imply_p(bitwise_not,node_dict[node.num])
                else:
                    node.imply_p(bitwise_not)
                node.insert_f(bitwise_not)
            
            # output result
            for i in self.circuit.nodes_lev:
                if i.ntype == 'PO':
                    # if some faults can be detected
                    if (i.pfs_V != 0) and (i.pfs_V != bitwise_not):
                        pfs_V_str = format(i.pfs_V,"b").zfill(bitlen)
                        msb_pfs_V = pfs_V_str[0]        # MSB of pfs_V: good circuit
                        for j in range(bitlen-1):
                            if pfs_V_str[bitlen-1-j] != msb_pfs_V:
                                detected_fault_num.append(fault_num[j])
                                detected_fault_value.append(fault_val[j])

        fault_set = set()
        for k in range(len(detected_fault_num)):
            fault_set = fault_set.union({(detected_fault_num[k],str(detected_fault_value[k]))})

        return fault_set

    
    def fs_exe(self, tp_num, t_mode, r_mode, fault_list_type):
        """
        Execute pfs in rand or full mode
        rand: the total faults can be detected by several random patterns
        full: the faults can be detected by each single pattern; all possible patterns are included
        """
        fname = 'c17_f0.saf'
        self.pfs_in_fault_list(fname,fault_list_type)

        if t_mode == 'rand':
            report_fname = self.circuit.c_name + '_' + str(tp_num) + '_' + self.fs_type + '_'+ r_mode + '.log'
            tp_fname = self.circuit.c_name + '_' + str(tp_num) + "_tp_b.txt"

            self.fs_tp_gen(tp_num, t_mode = 'rand', r_mode = r_mode)
            # tp_fname is bare name, the path is given in the method
            pattern_list = self.fs_input_fetch(tp_fname)
            # run pfs multiple
            self.multiple(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        elif t_mode == 'full':
            report_fname = self.circuit.c_name + '_full_' + self.fs_type + '_' + r_mode + '.log'
            tp_fname = self.circuit.c_name + '_full_tp_' + r_mode + '.txt'
            # generate all possible patterns in order
            self.fs_tp_gen(tp_num, t_mode = 'full', r_mode = r_mode)
            pattern_list = self.fs_input_fetch(tp_fname)
            # run pfs
            self.multiple_separate(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        else:
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")