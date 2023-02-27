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

MAX_N_TP = (1<<6)
N_FAULT = 10
MAX_N_FAULT = 500

PFS_TESTING_DIR = '../../data/testings/pfs_single_fault_testing'
CIRCUIT_DIR = os.path.join(PFS_TESTING_DIR, 'dfs_phase2')

def compare_two_lists(a , b):
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

def pfs_check_with_dfs_old():
    """Checks result of DFT.PFS.run() and dfs_old for full faults and multiple tps from dfs_old."""
    for c_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        print('_'*50+'\n')
        circuit = None    
        for tp_file_name in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/'):
            print(tp_file_name)
            pfs_faults = []
            dfs_faults = []

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
                _, pfs_faults =  pfs.run(tps)
                pfs_faults = [f.__str__() for f in pfs_faults]
                
            x = tp_file_name.replace('.tp','.fs')
            dfs_list_dir = f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/dfs/{x}'

            if os.path.exists(dfs_list_dir):
                dfs_lines = open(dfs_list_dir).readlines()
                for line in dfs_lines:
                    if '@' in line:
                        dfs_faults.append(line.replace('\n',''))

            res = compare_two_lists(pfs_faults, dfs_faults)

            if res:
                print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}Failed{bcolors.ENDC}")
            
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

def ppsf_check_with_dfs_old():
    """Checks result of DFT.PPSF.run() and dfs_old for full faults and multiple tps from dfs_old."""
    for c_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        print('_'*50+'\n')
        circuit = None    
        for tp_file_name in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/'):
            print(tp_file_name)
            pfs_faults = []
            dfs_faults = []

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
                ppsf = PPSF(circuit,faults=fault_list)
                ppsf_faults = ppsf.run(tps).keys()
                
            x = tp_file_name.replace('.tp','.fs')
            dfs_list_dir = f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/dfs/{x}'

            if os.path.exists(dfs_list_dir):
                dfs_lines = open(dfs_list_dir).readlines()
                for line in dfs_lines:
                    if '@' in line:
                        dfs_faults.append(line.replace('\n',''))

            res = compare_two_lists(ppsf_faults, dfs_faults)

            if res:
                print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}Failed{bcolors.ENDC}")

def compare_pfs_ppsf_multiple_tps():
    """ Check whether the results of PFS and PPSF match for multiple random test patterns"""
    for c in os.listdir('../../data/ckt/'):
        try:
            circuit_path = '../../data/ckt/'+c
            print(c)
            circuit = DFTCircuit(circuit_path)
            
            tg = TPGenerator(circuit=circuit)
            tps = []
            if (1<<len(circuit.PI)) < MAX_N_TP:
                tps = tg.gen_full()
            else:
                tps = tg.gen_n_random(MAX_N_TP, unique=True)

            fault_list = FaultList(circuit)
            
            if len(circuit.nodes) < MAX_N_FAULT:
                    fault_list.add_all()
            else:
                fault_list.add_n_random(MAX_N_FAULT)

            pfs = PFS(circuit=circuit, faults=fault_list)
            _, pfs_faults =  pfs.run(tps)
            pfs_faults = [f.__str__() for f in pfs_faults]
            
            ppsf = PPSF(circuit,faults=fault_list)
            ppsf_faults = ppsf.run(tps).keys()

            res = compare_two_lists(ppsf_faults, pfs_faults)
            if res:
                print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}Failed{bcolors.ENDC}")
        except:
            print(c,'errored')

if __name__ == '__main__':

    # pfs_csv_generator()
    # ppsf_csv_generator()

    # pfs_check_with_dfs_old()
    # Result: Failed for c6288.

    # ppsf_check_with_dfs_old()
    # Result: Failed for c6288 with different errors compared to pfs!
    # compare_pfs_ppsf_multiple_tps()
    
    # MAX_N_FAULT = 1 # if you want single tp
    compare_pfs_ppsf_multiple_tps() # all faults or 500
    # Result: All passed, even c6288!
