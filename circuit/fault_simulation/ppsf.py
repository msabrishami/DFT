import math
import os
import sys
import time
from multiprocessing import Pipe, Process

sys.path.append('../')
import config
import numpy as np
import utils
from fault_simulation.fault import FaultList
from fault_simulation.fault_simulation import FaultSim
from tp_generator import TPGenerator


class PPSF(FaultSim):
    """ Parallel Patern Single Fault, Fault Simulation """

    def __init__(self, circuit, faults=None):
        super().__init__(circuit, faults=faults)
        self.fs_type = "ppsf"
        self.fs_folder()

    def fs_folder(self):
        super().fs_folder()
        path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + "pfs"
        if not os.path.exists(path):
            os.makedirs(path)

    def _one_fault_run(self, tps, fault):
        """ 
        One pass of fault simulation for the given list of test patterns and a single fault. 
        Number of tps should be less than the system's word length. 
        If a fault is given, injects the fault and then runs logic simulation (bitwise).

        Arguments
        ---------
        tps : list of lists
                test patterns. Each tp is itself a list. 
                The order of tp values is the same as circuit.PI 
        Returns
        -------
        res_fixed : set of the indices of tps that could detect the given fault
        """
        if len(tps) > self.wordlen:
            print("Error: number of tps should be wordlen")
            return None

        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):
            for j in range(len(tps)):
                tps_bin[i] += (tps[j][i]*(2**j))

        # Run without fault
        self.circuit.logic_sim_bitwise(tps_bin) 
        Zg = self.circuit.read_PO() 

        # Run with fault
        self.circuit.logic_sim_bitwise(tps_bin, fault)
        Zf = self.circuit.read_PO()

        res = utils.comp_Zg_Zf_bin(Zg, Zf, len(tps))

        # The order of tp and res are reversed
        res_fixed = set([self.wordlen-1-k for k in res])
        
        return res_fixed

    def run(self, tps, faults=None, save_log=False, verbose=False):
        """ 
        Runs PPSF for the faults in the fault list, given tp count/list/fname
        For each fault, it counts the number of times it has been detected
        WARNING: this method is not tested after a few modifications 

        Updates fault.D_count

        faults: None: consider self.fault_list if already set, else all faults
                FaultList: consider given FaultList
                int: n random

        tps : int: number of random tps
              str: address of file containing tps
              list: list of test patterns

        num_proc : int
            Number of processes. Default is 1. if more than 1, algorithm is run in parallel.

        Returns
        -------
        fault_dict: {fault_str: D_count} only for detected faults
        """
        
        if isinstance(tps, int):
            tg = TPGenerator(self.circuit)
            tps = tg.gen_n_random(tps) # Not unique. Pass unique=True if want so --> as warning?
        elif isinstance(tps, str):
            tg = TPGenerator(self.circuit)
            tps = tg.load_file(tps)

        if faults is None and len(self.fault_list.faults) == 0:
            faults = FaultList(circuit=self.circuit)
            faults.add_all()

            if verbose:
                print('All faults are added.')

        elif len(self.fault_list.faults):
            faults=self.fault_list
        elif isinstance(faults, str):
            faults = FaultList(self.circuit)
            faults.add_file(str)
        elif isinstance(faults, int):
            nf = faults
            faults = FaultList(self.circuit)
            faults.add_n_random(nf)

        if len(faults.faults) == 0:
            raise "Warning: No fault is added."

        if verbose:
            pr =f"Running PPSF with:\n"
            pr+=f"\t| tp count = {len(tps)}\n"
            pr+=f"\t| fault count = {len(faults.faults)}\n"        
            print(pr)
        
        path = None
        log_fname = None
        log_file = None
        if save_log:
            path = os.path.join(config.FAULT_SIM_DIR, self.circuit.c_name) + '/ppsf/'
            if not os.path.exists(path):
                os.makedirs(path)
            log_fname = os.path.join(path, f"{self.circuit.c_name}_PPSF_f{len(faults.faults)}_tp{len(tps)}.ppsf")
            log_file = open(log_fname, 'w')
            log_file.write(f"#TP={len(tps)}\n")
            
        # Reset D_counts
        for f in faults.faults:
            f.D_count = 0

        for idx, fault in enumerate(faults.faults):
            tot_pass = math.ceil(len(tps)/self.wordlen)
            for _pass in range(tot_pass):
                tps_pass = tps[_pass*64:(_pass+1)*64]
                res = self._one_fault_run(tps_pass, fault)
                fault.D_count += len(res)

            if verbose and idx % 50 == 0:
                print(f"#Faults:{idx:5} \tFC: {100*faults.calc_fc():.4f}%")
            
            if log_file:
                log_file.write(f"{idx:5} \tFC: {100*faults.calc_fc():.4f}%\n")

        if verbose:
            print("\nPPFS completed")
            print(f"FC: {100*faults.calc_fc():.4f}%, total-faults={len(faults.faults)}")
            
            # print('\nRemaining Faults:')`
            # for f in faults.faults:
            #     if f.D_count == 0:
            #         print(f.__str__())`

        if save_log:
            log_file.write("remaining faults\n")
            for f in faults.faults:
                if f.D_count == 0:
                    log_file.write(f.__str__()+'\n')
            print('log saved in', log_fname)

        fault_dict = {}
        
        for f in faults.faults:
            if f.D_count:
                fault_dict[f.__str__()] = f.D_count
        
        return fault_dict #TODO: return fc and Faults Dict
    
    def _single_process_runner(self, conn, tp, faults, verbose=False):
        self.run(tps=tp, faults=faults, verbose=verbose, save_log=False)
        conn.send(faults)

    def _multiprocess_handler(self, tp, fl_curr, num_proc=1, log_fname=None, count_cont=False, verbose = False):
        """ Run ppsf in parallel for one step with given list or number of test patterns and fault list, \
        counts the number of the times faults in fault list are detected. 
        The tps are generated in each process separately, but are not stored by default.

        Parameters
        ----------
        fl_curr : FaultList --> self.fault_list
            Initially is total faults
        tp : int
            The number of test patterns for each process  
        num_proc : int
            Count of parallel processes
        log_fname : str
            File name for the final log fil. If None, does not log results (default is None)
        count_cont: int
            #TODO: define this (default is False). Still required?

        Returns
        ------
        list
            A fault list with D_count_list with length equal to given count of processes
            An updated version of fault_list --> D-count is added
        """
        time_s = time.time()
        process_list = []
        for _ in range(num_proc):
            parent_conn, child_conn = Pipe()
            fault_copy = FaultList()
            fault_copy.faults = fl_curr.faults.copy()
            p = Process(target=self._single_process_runner,
                        args=(child_conn, tp//num_proc+1, fault_copy, verbose))
            p.start()
            process_list.append((p, parent_conn))

        fault_lists = []
        for p, conn in process_list:
            faults_with_D_count = conn.recv()
            fault_lists.append(faults_with_D_count)
            p.join()

        for fl in fault_lists:
            for idx in range(len(fl_curr.faults)):
                fl_curr.faults[idx].D_count_list.append(fl.faults[idx].D_count)

        if log_fname:
            with open(log_fname, "a") as outfile:
                outfile.write(f"Total time: {time.time() - time_s:.2f}\n")

        return fl_curr

    def multiprocess_ci_run(self, tp_steps=[], op=None, verbose=False, num_proc=1, ci=1, depth=1, fault_count=None, save_log=False):
        """ (many times ppsf) Run Parallel Fault Simulation with count of test patterns in tp_steps list over the given number of Processes.\
        All faults are considered. 
        TODO: optional faults
        The fault is dropped if the times of o detection is in the confidential interval.
        Finally, for each fault the mean of detection times and the standard \
        deviation is stored in the log file.

        Parameters
        ----------
        circuit : Circuit 
        tp_steps : list
            Lengths of tps in each run
        #TODO: processes might get similar test patterns since they are generated randomly
        op : Node
            Node used for observation point insertion (default is None)
        depth : int
            Applicable when op is given. Used in backward BFS of op
        verbose : boolean
            If True, print results (default is False)
        log : boolean
            If True, save logs in log file (default is True).
            Logs are list of faults and the mean of times they were detected over process times of \
            processes. Logs are separated by the line '#TP=tp_counts' in each step.
        fault_count : int, str
            if None or 'all', all faults are considered. Else, fault_count unique random faults are considered.
        # TODO: pass a list of faults (now, doable in the constructor)

        Returns
        ------
        dict : str to float
            A dictionary of remained faults to the mean of their detection times \
            over process times of process with cumulative count of test patterns.
        """

        cont_faults = FaultList(self.circuit)
        all_faults = FaultList(self.circuit)
        
        if op is None:
            if fault_count is None or fault_count == 'all':
                cont_faults.add_all()
                all_faults.add_all()

            elif isinstance(fault_count, int):
                cont_faults.add_n_random(n=fault_count)
                all_faults.faults = cont_faults.faults.copy()

        else:
            fanin_nodes = utils.get_fanin_BFS(self.circuit, op, depth)
            
            if fault_count is None or fault_count == 'all':
                for node in fanin_nodes:
                    cont_faults.add(node.num, "1")
                    cont_faults.add(node.num, "0")
                    all_faults.add(node.num, "1")
                    all_faults.add(node.num, "0")
            else:
                import random
                for node in random.choices(fanin_nodes, k =fault_count):
                    cont_faults.add(node.num, "1")
                    cont_faults.add(node.num, "0")
                    all_faults.add(node.num, "1")
                    all_faults.add(node.num, "0")

        if verbose:
            pr =f"Running PPSF with:\n"
            pr+=f"\t| tp count = {tp_steps}\n"
            pr+=f"\t| confidence interval = {ci}\n"
            pr+=f"\t| fault count = {len(all_faults.faults)}\n"
            pr+=f"\t| num_proc(es) = {num_proc}\n"
            pr+=f"\t| BFS depth = {depth}\n"
        
            if op:
                pr+=f"\t| observation point (node_num) = {op.num}\n"
            
            print(pr)
            
        fault_idx = {}
        for idx, fault in enumerate(cont_faults.faults):
            fault_idx[str(fault)] = idx

        path = os.path.join(config.FAULT_SIM_DIR, self.circuit.c_name) + '/ppsf/'
        if not os.path.exists(path):
            os.makedirs(path)
            
        log_fname = None

        # Add BFS depth to the log_fname?
        if op == None:
            log_fname = os.path.join(path, f"{self.circuit.c_name}_PPSF_steps_f{len(all_faults.faults)}_ci{ci}_proc{num_proc}.ppsf")
        else:
            log_fname = os.path.join(path, f"{self.circuit.c_name}_PPSF_steps_f{len(all_faults.faults)}_op{op.num}_ci{ci}_proc{num_proc}.ppsf")
        
        if save_log:
            outfile = open(log_fname, "w")
                
        tp_tot = 0
        res_final = {}
        for tp in tp_steps:
            tp = int(tp)
            tp_tot += tp
            time_s = time.time()
            detected_faults = FaultList(self.circuit)

            # D_count_list is calculated here
            self._multiprocess_handler(fl_curr=all_faults, tp=tp, num_proc=num_proc, log_fname=None, count_cont=True)

            if save_log:
                outfile.write(f"#TP={tp}\n")

            for fault in all_faults.faults:
                fault_cont = cont_faults.faults[fault_idx[str(fault)]]
                fault_cont.D_count_list += fault.D_count_list
                
                mu = np.mean(fault_cont.D_count_list)
                std = np.std(fault_cont.D_count_list)
                if mu == 0 and std == 0: # All zero
                    detected_faults.add_str(str(fault))
                elif std == 0: # Why this happens at low number of tps (sometimes)?
                    print(f'(logging) {mu=}, {fault_cont.D_count_list}')
                elif mu/std > ci:
                    res_final[str(fault)] = mu/tp_tot
                    if save_log:
                        outfile.write(f"{fault}\t{mu:.2f}\t{std:.2f}\n")
                else:
                    detected_faults.add_str(str(fault))

            if verbose:
                print(f"TP = {tp:5}: #All faults = {len(all_faults.faults)} / #Detected faults = {len(detected_faults.faults):4}"+
                      f" / #Remaining faults = {len(all_faults.faults)-len(detected_faults.faults):4}" +
                      f" / FC = {100*len(detected_faults.faults)/len(all_faults.faults):.3f}%"+
                      f" / time = {time.time()-time_s:.2f}s")

        # Writing down the remaining faults
        if save_log:
            outfile.write("#TP: (remaining faults)\n")
        
        for fault in all_faults.faults:
            mu = np.mean(fault.D_count_list)
            std = np.std(fault.D_count_list)
            res_final[str(fault)] = mu/tp_tot
            
            if save_log:
                outfile.write(f"{fault}\t{mu:.2f}\t{std:.2f}\n")
        
        if save_log:
            outfile.close()

        if save_log:
            print(f"\nLog for step based PPSF is being stored in {log_fname}")

        return res_final