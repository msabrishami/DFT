import os

import config
from fault_simulation.fault_simulation import FaultSim
from tp_generator import TPGenerator
class PFS(FaultSim):
    """ 
    Parallel Fault Single Pattern, Fault Simulation 
    """
    def __init__(self, circuit, faults):
        super().__init__(circuit, faults=faults)
        self.fs_type = "pfs"
        self.fs_folder()
        
    def fs_folder(self):
        super().fs_folder()
        path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + "pfs"
        if not os.path.exists(path):
            os.makedirs(path)

    def _one_tp_run(self, tp, fault_drop=None):
        """
        Run PFS for one test pattern
        If fault drop is given, faults that have D_count < fault_drop are considered, 
            o.w. all faults in the fault_list are considered.
        Updates the fault.D_count of fault_list.faults
        Returns a list of detected faults in this pass
        tp sequence is important, if circuit.PI=[Na, Nb, Nc], then tp=[Xa, Xb, Xc]
        #TODO: Fix fault drop
        """        
        detected_faults = set() 
        
        ptr0 = 0
        while (ptr0 < len(self.fault_list.faults)):
            pfs_stuck_values = 0

            # fault list for one pass
            mask_dict = {}  # {key: fault_num, value: mask}
            faults_pass = []
            faults_pass_idx = []

            if fault_drop:    
                ptr1 = ptr0
                while len(faults_pass) < self.wordlen-1 and \
                        ptr1 != len(self.fault_list.faults) :
                    fault = self.fault_list.faults[ptr1]
                    if fault.D_count < fault_drop:
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
                    node.imply_p(node.bitwise_not, node_dict[node.num])
                else:
                    node.imply_p(node.bitwise_not)
                
                # Fault injection 
                node.insert_f(node.bitwise_not, pfs_stuck_values)
            
            # output result
            for i in self.circuit.PO:
                # if some faults can be detected
                if (i.pfs_V != 0) and (i.pfs_V != node.bitwise_not):
                    pfs_V_str = format(i.pfs_V,"b").zfill(self.wordlen)
                    msb_pfs_V = pfs_V_str[0]        # MSB of pfs_V: good circuit
                    for j in range(self.wordlen-1):
                        if pfs_V_str[self.wordlen-1-j] != msb_pfs_V:
                            # tp found this fault_pass[j]
                            detected_faults.add(faults_pass[j])

        for fault in detected_faults:
            fault.D_count += 1

        return list(detected_faults)

    def _multiple_tp_run(self, tps, log_fname: list = [None, None], fault_drop=None, verbose=False):
        """ 
        FS for multiple input patterns
        the pattern list is obtained as a list consists of sublists of each pattern like:
            input_file = [[1,1,0,0,1],[1,0,1,0,0],[0,0,0,1,1],[1,0,0,1,0]]
        """ 
        fault_log_fname, tpfc_log_fname = log_fname
        fault_log_file, tpfc_log_file = None, None
        if fault_log_fname:
            fault_log_file = open(fault_log_fname,'w')
        if tpfc_log_fname:
            tpfc_log_file = open(tpfc_log_fname, 'w')
        

        fault_coverage = []
        tpfc = []
        all_detected_faults = set()

        for idx, tp in enumerate(tps):
            detected_faults = self._one_tp_run(tp, fault_drop)
            
            for df in detected_faults:
                all_detected_faults.add(df)
            tpfc.append(len(detected_faults))
            fault_coverage.append(self.fault_list.calc_fc())
            
            if verbose and idx%50 == 0:
                    print(f"{idx:5} \t New faults: {tpfc[-1]:5}"+
                        f"  Total detected faults: {len(all_detected_faults):5}"+
                        f"  FC={100*len(all_detected_faults)/len(self.fault_list.faults):.4f}%")

            if tpfc_log_fname and tpfc_log_file:
                       tpfc_log_file.write(f"{idx:5} \t New faults: {tpfc[-1]:5}"+
                        f"  Total detected faults: {len(all_detected_faults):5}"+
                        f"  FC={100*len(all_detected_faults)/len(self.fault_list.faults):.4f}%\n")
            
            if fault_log_fname and fault_log_file:
                fault_log_file.write(",".join(map(str, tp)) + '\n')
                fault_log_file.write(f"Detected {len(detected_faults)} faults below: \n")
                
                for fault in detected_faults:
                    fault_log_file.write(f'{fault}' + '\n')
                fault_log_file.write("Fault Coverage = " + f'{[f"{f:.4f}" for f in fault_coverage]}'.replace('\'','') + '\n')
                fault_log_file.write('\n')
                fault_log_file.write("------------\n")
            
            if fault_coverage[-1] == 1:
                if verbose:
                    print(f'\nAll faults were found on test pattern {idx}\n')
                break   
                
        if fault_log_fname and fault_log_file:
            fault_log_file.write(f"Fault Coverage = {fault_coverage[-1]*100:.4f}%\n")
        if tpfc_log_file and tpfc_log_fname:
            tpfc_log_file.write(f"Fault Coverage = {fault_coverage[-1]*100:.4f}%\n")
        
        fault_log_file.close()
        tpfc_log_file.close()
        
        if fault_log_fname: print(f'\nLog file for faults saved in {fault_log_fname}')
        if tpfc_log_fname: print(f'Log file for tpfc saved in {tpfc_log_fname}')

        return fault_coverage, list(all_detected_faults)

    def run(self, tps, fault_drop=None, verbose=False, save_log=True):
        """ 
        Running the PFS simulation and calculating fault coverage (FC) for the number of
        test patterns (tps), which is referred to as TPFC. 
        If the real test pattern is given (i.e. tp is a list indicating a set of test patterns), 
        then those test patterns will be used for fault simulation, if tp is just an integer, 
        then tps number of test patterns will be generated randomly and used for TPFC. 
        In calculating FC, faults in the fault list are considered.  

        Parameters
        ----------
        tps : two options
            1. list of lists , test patterns 
            2. int , number of random test patterns to be generated 
        
        fault_drop : int (default None) , number of tps that must detect a fault so that the fault is
         dropped from fault_list, in other words considered completely detected. 

        Returns
        -------
        fc, detected_faults
        facult_coverage list and list of detected faults' strings
        """
        # TODO: should we take faults as an argument here?

        tg = TPGenerator(self)
        if isinstance(tps, int):
            tps = tg.gen_n_random(tps)
        elif isinstance(tps, str):
            tps = tg.load_file(tps)
        elif not isinstance(tps, list):
            raise TypeError("tps should be either int, or file name")

        faults_log_fname=None
        tpfc_log_fname = None
        if save_log:
            log_dir = os.path.join(config.FAULT_SIM_DIR, self.circuit.c_name)+'/pfs/'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            faults_log_fname = f"{log_dir}{self.circuit.c_name}_PFS_Fault_tp{len(tps)}_f{len(self.fault_list.faults)}.log"
            tpfc_log_fname = f"{log_dir}{self.circuit.c_name}_PFS_TPFC_tp{len(tps)}_f{len(self.fault_list.faults)}.log"


        fc, detected_faults = self._multiple_tp_run(tps=tps, fault_drop=fault_drop, 
                                                    log_fname=[faults_log_fname, tpfc_log_fname], verbose=verbose)

        if verbose: 
            print(f"\nTPFC completed:\tFC={100*fc[-1]:.4f}%, tot-faults={len(detected_faults)}")
        
        return  fc, detected_faults