from fault_simulation.simulation import FaultSim
from fault_simulation.fault import FaultList
import utils
import config as cfg
import config
from multiprocessing import Pipe, Process
import time
import os
import math
import sys
from tp_generator import TPGenerator

import numpy as np

sys.path.append('../')

"""
Trace functions called during Parallel Fault Simulation: 
    single_run() -> fs_exe() -> _ppsf_thread() ->
   _pd_ppsf_step() -> [pd_ppsf_conf() | pd_ppsf_basic()] -> pd_ppsf()
"""

class PPSF(FaultSim):
    """ 
    Parallel Patern Single Fault, Fault Simulation 
    """

    def __init__(self, circuit, fault_mode):
        super().__init__(circuit, fault_mode=fault_mode)
        self.fs_type = "ppsf"
        self.fs_folder()

    def fs_folder(self):
        super().fs_folder()
        path = config.FAULT_SIM_DIR + '/' + self.circuit.c_name + '/' + "pfs"
        if not os.path.exists(path):
            os.makedirs(path)

    def single_run(self, tps, fault):
        """ 
        One pass of fault simulation for the given list of test patterns over a single fault. 
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
        # TODO: Add verbose
        if len(tps) > self.wordlen:
            print("Error: number of tps should be wordlen")
            return None

        tps_bin = [0] * len(self.circuit.PI)
        for i in range(len(tps_bin)):
            for j in range(len(tps)):
                tps_bin[i] += (tps[j][i]*(2**j))

        self.circuit.logic_sim_bitwise(tps_bin)
        Zg = self.circuit.read_PO()  # Run without fault
        self.circuit.logic_sim_bitwise(tps_bin, fault)
        Zf = self.circuit.read_PO()  # Run with fault
        res = utils.comp_Zg_Zf_bin(Zg, Zf, len(tps))

        # The order of tp and res are reversed
        res_fixed = set([self.wordlen-1-k for k in res])

        return res_fixed

    def fs_exe(self, tps, log_fname=None, verbose=False):  # good
        """ 
        Runs PPSF for the faults in the fault list, given tp count/list/fname
        For each fault, it counts the number of times it has been detected
        WARNING: this method is not tested after a few modifications 
        TODO: log_fname
        """
        print("WARNING: ppsf.fs_exe is not tested after a few modifications")

        tg = TPGenerator(self.circuit)
        if isinstance(tps, int):
            tps = tg.gen_multiple_tp(tps)
        elif isinstance(tps, str):
            if os.path.exists(tps):
                tps = tg.load_tp_file(tps)
            else:
                raise "path not exist."
        elif not isinstance(tps, list):
            raise TypeError(f"tps should be either int, list, or file name ({type(tps)})")

        if len(self.fault_list.faults) == 0:
            print("Warning: No fault is added.")

        for idx, fault in enumerate(self.fault_list.faults):
            tot_pass = math.ceil(len(tps)/self.wordlen)
            for _pass in range(tot_pass):
                tps_pass = tps[_pass*64:(_pass+1)*64]
                # print(f'pass {_pass}: from {_pass*64} to {(_pass+1)*64}')
                res = self.single_run(tps_pass, fault)
                fault.D_count += len(res)
            if verbose and idx % 10 == 0:
                print(f"{idx:5} \tFC: {100*self.fault_list.calc_fc():.4f}%")

        if verbose:
            print("PPFS completed")
            print(
                f"FC: {100*self.fault_list.calc_fc():.4f}%, tot-faults={len(self.fault_list.faults)}")

    def _ppsf_thread(self, conn, tp):  # good
        self.fs_exe(tp)
        conn.send(self.fault_list)  # not necessarily

    def _pd_ppsf_step(self, tp, fl_curr, cpu=1, log_fname=None, count_cont=False):  # good
        """ Run ppsf in parallel for one step with given list or number of test patterns and fault list, \
        counts the number of the times faults in fault list are detected. 
        The tps are generated in each process separately, but are not stored by default.

        Parameters
        ----------
        fl_curr : FaultList --> self.fault_list
            Initially is total faults
        tp : int
            The number of test patterns for each process  
        cpu : int
            Count of parallel processes
        log_fname : str
            File name for the final log fil. If None, does not log results (default is None)
        count_cont: int
            #TODO: define this (default is False)

        Returns
        ------
        list
            A fault list with D_count with length equal to given count of CPUs
            An updated version of fault_list --> D-count is added
        """
        time_s = time.time()
        process_list = []
        print(f'running parallel {tp} test patterns on {cpu} cpu)')
        for _ in range(cpu):
            parent_conn, child_conn = Pipe()
            p = Process(target=self._ppsf_thread,
                        args=(child_conn, tp))
            p.start()
            print('Process', p.name, 'started')
            process_list.append((p, parent_conn))

        fault_lists = []
        for p, conn in process_list:
            tup = conn.recv()
            fault_lists.append(tup)
            p.join()

        # why exactly the same for all f?
        for f in fault_lists:
            print(f.faults[:5])
            print(f.faults[-5:])

        for fault in fl_curr.faults:
            fault.D_count = []

        for fl in fault_lists:
            for idx in range(len(fl_curr.faults)):
                fl_curr.faults[idx].D_count.append(fl.faults[idx].D_count)

        if log_fname:
            # tot_fl.write_file_extra(log_fname) #TODO: tot_fl not defined in this scope
            with open(log_fname, "a") as outfile:
                outfile.write(f"Total time: {time.time() - time_s:.2f}\n")

        return fl_curr

    def pd_ppsf_basic(self, tp, cpu, fault_count=None):
        """ Basic parallel PPSF fault simulation
        If fault_count is given, randomly selects faults, o.w. it generates a fault list \
        with all the faults in the circuit. 
        Logs the results in a file with a default name. 
        The result is a fault list, and D_count attribute of each fault is a list of \
        the number of times the fault is detected in each process. 

        Parameters
        ----------
        circuit : Circuit 
        tp : int
            The number of test patterns for each process  
        cpu : int
            count of parallel processes
        fault_count : int
            Number of random faults, if None, all faults are considered 

        Returns
        ------
        list
            A fault list with D_count with length equal to given count of CPUs
        """

        tot_fl = FaultList()
        path = os.path.join(cfg.FAULT_SIM_DIR, self.circuit.c_name)
        if fault_count:
            tot_fl.add_random(self.circuit, fault_count)
            log_fname = os.path.join(path, f"{self.circuit.c_name}-ppsf-fpb{fault_count}-tp{tp}-cpu{cpu}.ppsf")
        else:
            tot_fl.add_all(self.circuit)
            log_fname = os.path.join(path, f"{self.circuit.c_name}-ppsf-all-tp{tp}-cpu{cpu}.ppsf")

        return self._pd_ppsf_step(fl_curr=tot_fl, tp=tp, cpu=cpu, log_fname=log_fname)

    def pd_ppsf_conf(self, tp_steps, op=None, verbose=False, log=True, cpu=1, ci=1, depth=1):
        """ (many times ppsf) Run Parallel Fault Simulation with count of test patterns in tp_steps list over the given number of CPUs.\
        All faults are considered.
        The fault is dropped if the ???? times of or probability detection is in the confidential interval.
        Finally, for each fault the mean of detection times and the standard \
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
            Logs are list of faults and the mean of times they were detected over cp times of \
            process. Logs are separated by the line '#TP=tp_counts' in each step.

        Returns
        ------
        dict : str to float
            A dictionary of faults to the mean of their detection times \
            over cpu times of process with cumulative count of test patterns.
        """

        fl_cont = FaultList()
        fl_curr = FaultList()
        
        if op is None:
            fl_cont.add_all(self.circuit)
            fl_curr.add_all(self.circuit)
        
        else:
            fanin_nodes = utils.get_fanin_BFS(self.circuit, op, depth)
            for node in fanin_nodes:
                fl_cont.add(node.num, "1")
                fl_cont.add(node.num, "0")
                fl_curr.add(node.num, "1")
                fl_curr.add(node.num, "0")

        fault_idx = {}
        for idx, fault in enumerate(fl_cont.faults):
            fault_idx[str(fault)] = idx
            fault.D_count = np.zeros(cpu)

        path = os.path.join(cfg.FAULT_SIM_DIR, self.circuit.c_name)
        if log == False:
            log_fname = None
        elif op == None:
            log_fname = os.path.join(path, f"{self.circuit.c_name}-ppsf-steps-ci{ci}-cpu{cpu}.ppsf")
        else:
            log_fname = os.path.join(path, f"{self.circuit.c_name}-{op.num}-ppsf-steps-ci{ci}-cpu{cpu}.ppsf")

        if log:
            outfile = open(log_fname, "w")
            if verbose:
                print(f"Log for step based PPSF is being stored in {log_fname}")
                
        tp_tot = 0
        res_final = {}
        for tp in tp_steps:
            tp = int(tp)
            tp_tot += tp
            time_s = time.time()
            fl_temp = FaultList()
            
            #D_count is added to the fault objects in fl_curr
            fl_curr = self._pd_ppsf_step(fl_curr=fl_curr, tp=tp, cpu=cpu, log_fname=None,
                                         count_cont=True)
            if log:
                outfile.write(f"#TP={tp}\n")

            for fault in fl_curr.faults:
                fault_cont = fl_cont.faults[fault_idx[str(fault)]]
                fault_cont.D_count += np.array(fault.D_count)
                mu = np.mean(fault_cont.D_count)
                std = np.std(fault_cont.D_count)
                if mu == 0 and std == 0:
                    fl_temp.add_str(str(fault))
                elif mu/std > ci:
                    res_final[str(fault)] = mu/tp_tot
                    if log:
                        outfile.write(f"{fault}\t{mu:.2f}\t{std:.2f}\n")
                else:
                    fl_temp.add_str(str(fault))

            if verbose:
                print(f"TP={tp} #FL={len(fl_curr.faults)} -> #FL={len(fl_temp.faults)}\ttime={time.time()-time_s:.2f}")
            
            if len(fl_curr.faults) == 0:
                # No new fault is found / Correct?
                break

        # Writing down the remaining faults
        if log:
            outfile.write("#TP: (remaining faults)\n")
        
        for fault in fl_curr.faults:
            mu = np.mean(fault.D_count)
            std = np.std(fault.D_count)
            res_final[str(fault)] = mu/tp_tot
            
            if log:
                outfile.write(f"{fault}\t{mu:.2f}\t{std:.2f}\n")
        
        if log:
            outfile.close()

        return res_final

    def pd_ppsf(self, tp, fault_count=None, steps=None, op=None, verbose=False, log=True, cpu=1, ci=1): # good
        """ Parallel Pattern Fault Simulation
        If steps is given, the ppsfs will be run for all tp counts over the \
        given count of processes in the args and the mean and std will be save into log file. Else, \
        the simple parallel pattern fault simulation with the given count of test patterns will be run.

        Parameters
        ----------
        circuit : Circuit 
        args : args
            Command-line arguments
        steps : list of ints
            A list of tp counts for each run
            (default is None)
        op : None
            Node used for observation point insertion (default is None)
        verbose : boolean
            If True, print results (default is False)
        log : boolean
            If save logs in log file (default is True)
            Logs are list of faults and the mean of times they were detected over cp times of \
                process. Logs are separated by the line '#TP=tp_counts' in each step

        Returns
        ------
        dict or list
            According to the steps, it will be determined. If steps is given, returns \
            a dictionary of faults to means of fault coverage. Otherwise, A fault list with D_count  \
            with length equal to cpu is returned
        """
        if steps:
            return self.pd_ppsf_conf(tp_steps=steps, op=op, verbose=verbose, log=log, ci = ci)
        
        else:
            # because of where we call Process()
            if not isinstance(tp, int):
                raise TypeError
            return self.pd_ppsf_basic(tp=tp//cpu, cpu=cpu, fault_count=fault_count)