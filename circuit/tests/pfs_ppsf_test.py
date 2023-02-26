# pfs: 
#   single: each test pattern --> what faults it detect

# ideas: 1- check it with dfs existing results

# ppsf: in random k tps, how many times each fault is detected?

#experiments: check_psf_vs_ppsf

import os
import sys
sys.path.append('../')

import pandas as pd

from circuit.dft_circuit import DFTCircuit
from fault_simulation.pfs import PFS
from fault_simulation.ppsf import PPSF
from fault_simulation.fault import FaultList
from tp_generator import TPGenerator
from utils import bcolors

MAX_N_TP = (1<<4)
MAX_N_FAULT = 500

PFS_TESTING_DIR = '../../data/testings/pfs_single_fault_testing'
CIRCUIT_DIR = os.path.join(PFS_TESTING_DIR, 'dfs_phase2')

def compare_fault_lists(a , b):
    for x in a:
        if x not in b:
            print(f'{x=}')
            return False
        
    for y in b:
        if y not in a:
            print(f'{y=}')
            return False
        
    return True

def pfs_csv_generator():
    """Creates a csv, containing detected faults of each tp using PFS.
    tps are full, or randomly generated if input size is large
    """
    for c in os.listdir(CIRCUIT_DIR):
        circuit_path = '../../data/ckt/'+c+".ckt"
        print(c)
        circuit = DFTCircuit(circuit_path)
        faults = FaultList(circuit=circuit)
        faults.add_all()

        tp_fault_df = pd.DataFrame(columns = ['tp']+[f.__str__() for f in faults.faults])

        tg = TPGenerator(circuit)
        tps = []
        if (1<<len(circuit.PI)) < MAX_N_TP:
            tps = tg.gen_full()
        else:
            tps = tg.gen_n_random(MAX_N_TP, unique=True)
        
        for tp in tps:
            pfs = PFS(circuit, faults)
            detected_faults = pfs._one_tp_run(tp)
            row = {}
            # each tp is int(binary_from)
            row['tp'] = int("".join(map(str, tp)), 2) #--> if not fit in int: save tps in a file and use their line number in the csv as tp 
            for f in detected_faults:
                row[f.__str__()] = "1"

            tp_fault_df = pd.concat([tp_fault_df, pd.DataFrame.from_records([row])])

        tp_fault_df.to_csv(f'{PFS_TESTING_DIR}/single_tp_PFS_{circuit.c_name}_{len(faults.faults)}f_{len(tps)}tp.csv',index=False)            
        print(f'{PFS_TESTING_DIR}/single_tp_PFS_{circuit.c_name}_{len(faults.faults)}f_{len(tps)}tp.csv was saved.')

def pfs_single_tp_checker_pfs_dfs_old():
    """Checks result of DFT.PFS._one_tp_run() and dfs_old for full faults and single tps from dfs_old."""

    for c_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        print(c_file)
        circuit = None
        
        for tp_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/'):
            pfs_faults = []
            dfs_faults = []
            if 'count-1_' in tp_file:
                tp = open(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/{tp_file}','r')
                tp = list(map(int, tp.readlines()[1].replace('\n','').split(',')))
                circuit = DFTCircuit(f'../../data/ckt/{c_file}.ckt')

                fault_list_file = None
                for fl in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/'):
                    if '_fs.txt' in fl:
                        fault_list_file = fl
                
                if fault_list_file:
                    fault_list = FaultList(fname=f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/{fault_list_file}')
                    pfs = PFS(circuit,faults=fault_list)
                    pfs_faults = [f.__str__() for f in pfs._one_tp_run(tp)]
                    
                x = tp_file.replace('.tp','.fs')
                dfs_list_dir = f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/dfs/{x}'
                if os.path.exists(dfs_list_dir):
                    dfs_lines = open(dfs_list_dir).readlines()
                    for line in dfs_lines:
                        if '@' in line:
                            dfs_faults.append(line.replace('\n',''))

                print(compare_fault_lists(dfs_faults, pfs_faults)) # Add colors

def pfs_multiple_tp_checker_pfs_dfs_old():
    """Checks result of DFT.PFS._multiple_run() or run() and dfs_old for full faults and multiple tps from dfs_old."""
    for c_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        print(c_file)
        circuit = None    
        for tp_file_name in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/'):
            pfs_faults = []
            dfs_faults = []
            if 'count-1_' not in tp_file_name:
                tp_file = open(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/{tp_file_name}','r')
                tps = []
                for line in tp_file.readlines()[1:]:
                    tps.append(list(map(int, line.replace('\n','').split(','))))
                circuit = DFTCircuit(f'../../data/ckt/{c_file}.ckt')

                fault_list_file = None
                for fl in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/'):
                    if '_fs.txt' in fl:
                        fault_list_file = fl
                
                if fault_list_file:
                    fault_list = FaultList(fname=f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/{fault_list_file}')
                    pfs = PFS(circuit,faults=fault_list)
                    _, pfs_faults = [f.__str__() for f in pfs.run(tps)]
                    
                x = tp_file_name.replace('.tp','.fs')
                dfs_list_dir = f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/dfs/{x}'

                if os.path.exists(dfs_list_dir):
                    dfs_lines = open(dfs_list_dir).readlines()
                    for line in dfs_lines:
                        if '@' in line:
                            dfs_faults.append(line.replace('\n',''))

                print(compare_fault_lists(pfs_faults, pfs_faults)) # Add colors
            
def ppsf_csv_generator():
    """Creates a csv, containing detected faults of each tp using PPSF.
    tps are full, or randomly generated if input size is large
    """
    for c in os.listdir(CIRCUIT_DIR):
        circuit_path = '../../data/ckt/'+c+".ckt"
        print(c)
        circuit = DFTCircuit(circuit_path)
        faults = FaultList(circuit=circuit)
        faults.add_all()

        tp_fault_df = pd.DataFrame(columns = ['tp']+[f.__str__() for f in faults.faults])

        tg = TPGenerator(circuit)
        tps = []
        if (1<<len(circuit.PI)) < MAX_N_TP:
            tps = tg.gen_full()
        else:
            tps = tg.gen_n_random(MAX_N_TP, unique=True)
        
        for tp in tps:
            ppsf = PPSF(circuit, faults)
            row = ppsf.run(tps=[tp], faults=faults) # fault_dict
            # each tp is int(binary_from)
            row['tp'] = int("".join(map(str, tp)), 2) #--> another idea: save tps in a file and use their line number in the csv as tp 

            tp_fault_df = pd.concat([tp_fault_df, pd.DataFrame.from_records([row])])

        tp_fault_df.to_csv(f'{PFS_TESTING_DIR}/single_tp_PPSF_{circuit.c_name}_{len(faults.faults)}f_{len(tps)}tp.csv',index=False)            
        print(f'{PFS_TESTING_DIR}/single_tp_PPSF_{circuit.c_name}_{len(faults.faults)}f_{len(tps)}tp.csv was saved.')

def compare_pfs_vs_ppsf_multiple_tps(fault_count=None):
    """ Check whether the results of PFS and PPSF match for multiple random test patterns"""
    
    for c in os.listdir(CIRCUIT_DIR):
        circuit_path = '../../data/ckt/'+c+".ckt"
        print(c)
        circuit = DFTCircuit(circuit_path)
        
        tg = TPGenerator(circuit=circuit)
        tps = []
        if (1<<len(circuit.PI)) < MAX_N_TP:
            tps = tg.gen_full()
        else:
            tps = tg.gen_n_random(MAX_N_TP, unique=True)

        fault_list = FaultList(circuit)
        if isinstance(fault_count, int):
            fault_list.add_n_random(fault_count)
        elif len(circuit.nodes_lev) < MAX_N_FAULT:
            fault_list.add_all()
        else:
            fault_list.add_n_random(MAX_N_FAULT)

        pfs = PFS(circuit=circuit, faults=fault_list)
        pfs.run(tps=tps, verbose=False)
    
        ppsf = PPSF(circuit=circuit, faults=fault_list)
        ppsf.run(tps=tps, verbose=False)
    
        pfs_res = dict()
        for fault in pfs.fault_list.faults:
            pfs_res[str(fault)] = fault.D_count
        error = False
        for fault in ppsf.fault_list.faults:
            if fault.D_count != pfs_res[str(fault)]:
                error = True
                print(f"Error: Fault={str(fault)} PFS={pfs_res[str(fault)]} PPSF={fault.D_count}")
        if not error:
            print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}")

if __name__ == '__main__':

    # pfs_csv_generator()
    # ppsf_csv_generator()

    pfs_single_tp_checker_pfs_dfs_old()
    # Result: 6288
    # for all single tps in /dfs_phase2, dfs finds fault 1290@1 while pfs does not.

    # pfs_multiple_tp_checker_pfs_dfs_old()
    # Result: All passed.

    # compare_pfs_vs_ppsf_multiple_tps()
    # Result: All passed.