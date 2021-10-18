import sys
from circuit import Circuit
#TODO: change this style of import
from node import Node
import math
from fault_sim import FaultSim, FaultList
import pdb

class PFS(FaultSim):
    def __init__(self, circuit):
        FaultSim.__init__(self, circuit)
        self.in_fault_num = [] # input fault num, string format
        self.in_fault_type = [] # input fault type, integer format
        #node = [] # input fault num, string format
        #fault = []# input fault type, integer format

        self.fs_type = 'pfs'

    
    def fs_for_atpg(self, faultset, ipt_pattern):
        self.add_fault(mode="atpg", fname=None, faultset = faultset)
        return self.single(ipt_pattern)
    
    
    def add_fault(self, mode="full", fname=None, faultset = None):
        """ add faults to the fault list 
        mode = full: input fault list is full fault list
        mode = user: input fault list is given by user as a file name
        """
        #TODO: why did we overloaded this method from super? 
        if mode == "full":
            self.circuit.get_full_fault_list()
            self.in_fault_num = self.circuit.fault_node_num
            self.in_fault_type = self.circuit.fault_type
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
        pdb.set_trace()

        for _pass in range(pass_tot):
            print("Pass number: {}".format(_pass))
            
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
            
            # calculate stuck values of faults in this pass of PFS, 
            # generating masks for each fault_num
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
                #TODO: if this is something that is common for all nodes, 
                # ... why are we making it an atribute for the node? 
                # ... we need to pass it to each nodes pfs function
                #node.pfs_S = pfs_stuck_values

                # if fault should be inserted in this node
                if node.num in mask_dict:
                    node.pfs_I = mask_dict[node.num]

                if node.gtype == "IPT":
                    node.imply_p(bitwise_not,node_dict[node.num])
                else:
                    node.imply_p(bitwise_not)
                node.insert_f(bitwise_not,pfs_stuck_values)
            
            # output result
            for i in self.circuit.PO:
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
            fault_set = fault_set.union({(detected_fault_num[k],detected_fault_value[k])})

        return fault_set

    
    def fs_exe(self, tp_num, t_mode, r_mode, fault_list_type, fname):
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
        self.add_fault(fault_list_type, fname)

        if t_mode == 'rand':
            self.fs_folder(tp_mode='rand', r_mode='b')
            report_fname = self.circuit.c_name + '_' + str(tp_num) + \
                    '_' + self.fs_type + '_'+ r_mode + '.log'
            tp_fname = self.circuit.c_name + '_' + str(tp_num) + "_tp_b.tp"
            self.fs_tp_gen(tp_num, t_mode='rand', r_mode=r_mode)
            pattern_list = self.fs_input_fetch(tp_fname)
            self.multiple(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        elif t_mode == 'full':
            self.fs_folder(tp_mode='rand', r_mode='b')
            report_fname = self.circuit.c_name + \
                    '_full_' + self.fs_type + '_' + r_mode + '.log'
            tp_fname = self.circuit.c_name + '_full_tp_' + r_mode + '.tp'
            self.fs_tp_gen(tp_num, t_mode = 'full', r_mode = r_mode)
            pattern_list = self.fs_input_fetch(tp_fname)
            self.multiple_separate(pattern_list=pattern_list, \
                    fname_log=report_fname, mode="b")

        else:
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")
    
