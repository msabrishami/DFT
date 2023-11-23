import math
import os
import sys
import time
from multiprocessing import Pipe, Process
import pdb

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


        Returns
        -------
        fault_dict: {fault_str: D_count} only for detected faults
        """
        
        if isinstance(tps, int):
            tg = TPGenerator(self.circuit)
            tps = tg.gen_n_random(tps) # Not unique tps 
        elif isinstance(tps, str):
            tg = TPGenerator(self.circuit)
            tps = tg.load_file(tps)
        elif not isinstance(tps, list):
            raise TypeError("tps should be either int, or file name")

        if isinstance(faults, FaultList):
            pass
        elif (faults == 'all') or \
                (faults is None and len(self.fault_list.faults) == 0):
            faults = FaultList(self.circuit)
            faults.add_all()
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

    def _multiprocess_handler(self, tp, fl_curr, num_proc=1, log_fname=None, 
            count_cont=False, verbose = False):
        """ Run ppsf in parallel for one step with given list or number of 
            test patterns and fault list, counts the number of the 
            times faults in fault list are detected. 
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
                        args=(child_conn, tp, fault_copy, verbose))
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
    
    #TODO MSA: add the value of dp to node.stat["DP0"] and ["DP1"]
    def multiprocess_ci_run(self, tp_steps=[], op=None, verbose=False, 
            num_proc=1, ci=1, depth=1, fault_count=None, save_log=True, 
            log_fname=None, mode="basic", moe=0.1, target_fault=None):
        """ (many times ppsf) Run Parallel Fault Simulation with count of 
        test patterns in tp_steps list over the given number of Processes.
        All faults are considered. 
        TODO: optional faults
        The fault is dropped if the times of o detection is in the confidential interval.
        Finally, for each fault the mean of detection times and the standard
        deviation is stored in the log file.

        Parameters
        ----------
        circuit : Circuit 
        tp_steps : list
            Lengths of tps in each run

        op : Node
            Node used for observation point insertion (default is None)
        depth : int
            Applicable when op is given. Used in backward BFS of op
        verbose : boolean
            If True, print results (default is False)
        log : boolean
            If True, save logs in log file (default is True).
            Logs are list of faults and the mean of times they were detected 
            over process times of processes. Logs are separated by 
            the line '#TP=tp_counts' in each step.
        fault_count : int, str
            if None or 'all', all faults are considered. Else, fault_count 
            unique random faults are considered.
        
        # TODO: processes might get similar TPs as they are generated randomly
        # TODO: pass a list of faults (now, doable in the constructor)

        Returns
        ------
        dict : str to float
            A dictionary of remained faults to the mean of their detection times \
            over process times of process with cumulative count of test patterns.
        """

        fl_curr = FaultList(self.circuit)
        fl_cont = FaultList(self.circuit)
        
        if target_fault is not None:
            if isinstance(target_fault, list):
                fl_curr.add_str_list(target_fault)
                fl_cont.add_str_list(target_fault)
            if isinstance(target_fault, str):
                fl_curr.add_str(target_fault)
                fl_cont.add_str(target_fault)

        # Creating fault list (fl_curr) based on given OP and fault_count
        elif op is None:
            if fault_count is None or fault_count == 'all':
                fl_cont.add_all()
                fl_curr.add_all()
        else:
            fanin_nodes = utils.get_fanin_BFS(self.circuit, op, depth)
            
            if fault_count is None or fault_count == 'all':
                for node in fanin_nodes:
                    fl_cont.add(node.num, "1")
                    fl_cont.add(node.num, "0")
                    fl_curr.add(node.num, "1")
                    fl_curr.add(node.num, "0")
            else:
                import random
                for node in random.choices(fanin_nodes, k =fault_count):
                    fl_cont.add(node.num, "1")
                    fl_cont.add(node.num, "0")
                    fl_curr.add(node.num, "1")
                    fl_curr.add(node.num, "0")

        if verbose:
            pr =f"Running PPSF with:\n"
            pr+=f"\t| tp steps = {tp_steps}\n"
            pr+=f"\t| confidence interval = {ci}\n"
            pr+=f"\t| fault count = {len(fl_curr.faults)}\n"
            pr+=f"\t| CPU count = {num_proc}\n"
        
            if op:
                pr+=f"\t| observation point (node_num) = {op.num}\n"
                pr+=f"\t| BFS depth = {depth}\n"
            
            print(pr)
            
        fault_idx = {}
        for idx, fault in enumerate(fl_cont.faults):
            fault_idx[str(fault)] = idx
            fault.D_count_list = np.zeros(num_proc)

        path = os.path.join(config.FAULT_SIM_DIR, self.circuit.c_name) + '/ppsf/'
        if not os.path.exists(path):
            os.makedirs(path)
            
        
        ### Setting log file name and path 
        if log_fname is None:
            log_fname = utils.path_ppsf_ci(self.circuit.c_name, ci, num_proc)
        
        #TODO: consider an automatic fname with given op or at least 
        #       add this info in the description 
        log_fname = os.path.join(path, log_fname)
        if save_log:
            outfile = open(log_fname, "w")
        
        
        ### Starting PPSF simulation 
        tp_tot = 0
        res_final = {}
        
        for tp in tp_steps:
            tp = int(tp)
            tp_tot += tp
            time_s = time.time()

            # To be used for recording faults that still need simulation  
            fl_temp = FaultList(self.circuit)

            # fl_curr is only used for this simulation pass with given tp
            # therefore, D_count_list of faults in fl_curr record a list, each item 
            # of the list is corresponding to number of detections for a processor 
            for f in fl_curr.faults:
                f.D_count_list = []
            # fl_curr will be updated by parallel simulation below 
            # for faults in fl_curr, D_count_list will be updated, and not D_count
            self._multiprocess_handler(fl_curr=fl_curr, tp=tp, num_proc=num_proc, 
                    log_fname=None, count_cont=True)
            if save_log:
                outfile.write(f"#TP={tp}\n")
            
            for fault in fl_curr.faults:
                is_done = False
                fault_cont = fl_cont.faults[fault_idx[str(fault)]]
                fault_cont.D_count_list += np.array(fault.D_count_list)
                mu = np.mean(fault_cont.D_count_list/tp_tot)
                std = np.std(fault_cont.D_count_list/tp_tot)
                if mu == 0 and std == 0: # all zero
                    fl_temp.copy_fault(fault)
                    continue
                elif std == 0: 
                    #TODO Why this happens at low number of tps (sometimes)?
                    print(f'(Warning) {str(fault)}\tmu={mu}, {fault_cont.D_count_list}')
                    continue

                se = np.sqrt(mu*(1-mu)/(tp_tot*num_proc))
                e_rel = ci*se/mu 

                if mode=="basic" and mu/std > ci:
                    is_done = True
                elif mode=="advanced" and (mu/std > ci) and (e_rel<moe):
                    is_done = True

                if is_done:
                    fault_cont.final_mu = mu
                    fault_cont.final_std = std
                    fault_cont.final_tp = tp_tot 
                    msg = "STOP:\t"
                else:
                    fl_temp.copy_fault(fault)
                    msg = "CONT:\t"

                if save_log:
                    # outfile.write(f"{fault}\t{mu:.4e}\t{std:.4e}\n")
                    _counts = ",".join([str(int(x)) for x in fault_cont.D_count_list])
                    msg += f"{fault}\t{mu:.4e}\t{std:.4e}\t{se:.4e}\t{e_rel:.4e}"
                    msg += f"\t{_counts}\n"
                    outfile.write(msg)

            if verbose:
                msg = f"TP = {tp:5}: Simulated faults = #{len(fl_curr.faults)}\t"
                msg += f"Finalized faults = #{len(fl_curr.faults)-len(fl_temp.faults):4}"
                msg += f"\tRemaining faults = #{len(fl_temp.faults):4}"
                msg += f"\tElpased time = {time.time()-time_s:.2f}s"
                print(msg)

            fl_curr = fl_temp

            if len(fl_curr.faults) == 0:
                break

        # Writing down the remaining faults
        if save_log and (len(fl_curr.faults) != 0):
            outfile.write("\n#TP: (remaining faults)\n")
        
            for fault in fl_curr.faults:
                fault_cont = fl_cont.faults[fault_idx[str(fault)]]
                fault_cont.D_count_list += np.array(fault.D_count_list)
                mu = np.mean(fault_cont.D_count_list/tp_tot)
                std = np.std(fault_cont.D_count_list/tp_tot)
                outfile.write(f"{fault}\t{mu:.4e}\t{std:.4e}\n")
                
                res_final[str(fault)] = mu

            print(f"\nLog for step-based PPSF is saved in {log_fname}")
            outfile.close()
        
        return res_final, fl_cont

    def load_ppsf_parallel(fname):
        """load a ppsf_parallel simulated log file 
        the last line is time """ 
        if not os.path.exists(fname):
            raise Exception(f'File {fname} not exist.')
        lines = open(fname, "r").readlines()
        res = {}
        for line in lines[:-1]:
            words = line.strip().split(",")
            res[words[0]] = [int(x) for x in words[1:]]
        return res

    def load_pd_ppsf_conf(self, fname, mode="advanced"):
        """load a ppsf log file with confidence log file """ 
        #TODO We need to make sure files are saved correctly 
        #TODO Consider writing down the policy for continual TP 
        #TODO This method is also defined in utils and other places! 
        if not os.path.exists(fname):
            raise Exception(f'File {fname} not exists')
        if mode not in ["basic", "advanced"]:
            raise Exception(f"(ERROR) mode should be either \"basic\" or \"advance\"")
        lines = open(fname, "r").readlines()
        res = {}
        current_tp = 0
        for line in lines:
            if line == "\n":
                continue
            elif line.startswith("#TP="):
                current_tp += float(line.split("=")[-1])
            elif line.startswith("#TP: (remaining"):
                print("(Warning) PPSF was not completed with the given " + 
                        "confidence interval for some of the faults")
            elif mode == "basic":
                fault, mu_d, sigma_d = line.split()
                node, ssaf = fault.split('@')
                node = self.circuit.nodes[node]
                node.stat["DP" + ssaf] = float(mu_d)
                res[fault] = float(mu_d)
            elif mode == "advanced":
                """
                1. stat: 
                    CONT fault.pd was not yet finalized in this round
                    STOP fault.pd was finalized given its criteria
                2. fault: node-number@stuck-value
                3. mu_d: mean of fault.pd among all processes
                4. sigma_d: standard deviation of fault.md among all processes
                5. se: standard error for fault, given all observations of RVs
                6. e_rel: relative error given ci, calculated by ci*se/mu 
                7. counts: list of count of RV observations (Binomial ~ N*p)
                """
                stat, fault, mu_d, sigma_d, se, e_rel, counts = line.split("\t")
                node, ssaf = fault.split('@')
                node = self.circuit.nodes[node]
                node.stat["DP" + ssaf] = float(mu_d)
                res[fault] = float(mu_d)


        print(f'Loaded PPSF data from: {fname}')
        return res
