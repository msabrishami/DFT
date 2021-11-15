
import sys
import math
import os

from circuit import Circuit
from node import Node
from fault_sim import FaultSim
import config
import pdb


class PFS(FaultSim):
    """ 
    Parallel Fault Single Pattern, Fault Simulation 
    """
    def __init__(self, circuit):
        super().__init__(circuit)
        self.fs_type = "pfs"
        self.wordlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**self.wordlen-1
    

    def single(self, tp, fault_drop=None):
        """
        For one test pattern
        If fault drop is given, faults that have D_count < fault_drop are considered, 
            o.w. all faults in the fault_list are considered.
        Updates the fault.D_count of fault_list.faults
        Returns a list of detected faults in this pass
        tp sequence is important, if circuit.PI=[Na, Nb, Nc], then tp=[Xa, Xb, Xc]
        """        
        detected_faults = set() 
        
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
            
            ptr0 = ptr1+1
            for i in range(len(faults_pass)):
                pfs_stuck_values += int(faults_pass[i].stuck_val) * (2**i)

                if faults_pass[i].node_num in mask_dict:
                    mask_dict[faults_pass[i].node_num] += 2**i
                else:
                    mask_dict[faults_pass[i].node_num] = 2**i

            # pfs for one pass
            node_dict = dict(zip([x.num for x in self.circuit.PI], tp))
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
                            detected_faults.add(faults_pass[j])

        for fault in detected_faults:
            fault.D_count += 1
        return list(detected_faults)


    def multiple_separate(self, tps, log_fname, fault_drop):
        """ 
        FS for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        """ 
        outfile = open(log_fname, mode='w')

        for tp in tps:
            detected_faults = self.single(tp, fault_drop)
            outfile.write(",".join(map(str, tp)) + '\n')
            outfile.write("Detected {} faults below: \n".format(len(detected_faults)))
            for fault in detected_faults:
                outfile.write(str(fault) + '\n')
            # outfile.write("Fault Coverage = " + str(fault_coverage) + '\n')
            # outfile.write('\n')
            outfile.write("------------\n")
        fc = self.fault_list.calc_fc()
        outfile.write("Fault Coverage = {:.2f}%\n".format(fc*100))
        outfile.close()
        print(self.fs_type + " (Separate mode) completed. ")
        print("Fault coverage = {:.2f}%".format(fc*100))
        print("Log file saved in {}".format(log_fname))


    def tpfc(self, tps, log_fname=None, fault_drop=None, verbose=False):
        """ 
        Calculate the FC for each TP
        Arguments: 
        ----------
        tps : list of lists 
        """
        tpfc = []
        for idx, tp in enumerate(tps):
            tpfc.append(len(self.single(tp, fault_drop)))
            if verbose:
                print("{:4} \t New: {:5} \t Total: {:5} \t FC: {:.4f}%".format(
                    idx, tpfc[-1], sum(tpfc), 100*sum(tpfc)/len(self.fault_list.faults)))
        fault_coverage = self.fault_list.calc_fc() 
        if log_fname:
            outfile = open(log_fname, mode='w')
            for k in range(len(tpfc)):
                outfile.write("{:3} \t New: {} \t Total: {} \t FC: {:.4f}%\n".format(
                    k, tpfc[k], sum(tpfc[:k]), 100*sum(tpfc[:k])/len(self.fault_list.faults)))
            outfile.write("Fault Coverage = {:.4f}%\n".format(fault_coverage*100))
            outfile.close()
            print("Log file saved in {}".format(log_fname))

        print("TPFC completed. ".format(self.fs_type))
        return tpfc 

    
    def fs_exe(self, tp_fname, log_fname=None, fault_drop=None):
        """
        Runs PFS for the faults in the fault list, given the tp file.  
        Arguments:
        ---------
        """
        self.fs_folder()
        tps = self.circuit.load_tp_file(tp_fname)
        fn = config.FAULT_SIM_DIR + "/" + self.circuit.c_name + "/pfs/"
        fn += tp_fname.split("/")[-1].replace(".tp", ".log")
        log_fname = fn if log_fname==None else log_fname
        print("PFS for tp file: {}".format(tp_fname))
        # self.multiple_separate(tps=tps, log_fname=log_fname, fault_drop=fault_drop)
        tpfc = self.tpfc(tps=tps, log_fname=log_fname, fault_drop=1)
        print("PFS completed")
        print("FC={:.4f}%, tot-faults={}".format(
            100*self.fault_list.calc_fc(), len(self.fault_list.faults)))
    
