import os
import sys

sys.path.append('../')

import pandas as pd

import config
from utils import bcolors
from fault_simulation.fault import FaultList
from fault_simulation.pfs import PFS
from fault_simulation.ppsf import PPSF
from tp_generator import TPGenerator

from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit

MAX_N_TP = (1<<6)
N_FAULT = 10
MAX_N_FAULT = 500

PFS_TESTING_DIR = '../../data/testings/pfs_single_fault_testing'
CIRCUIT_DIR_DSF_OLD = os.path.join(PFS_TESTING_DIR, 'dfs_phase2')
EPFL = [config.EPFL_V0_DIR, config.EPFL_V1_DIR, config.EPFL_V2_DIR]
ISCAS85 = [config.ISCAS85_V0_DIR, config.ISCAS85_V1_DIR, config.ISCAS85_V2_DIR]

PRINT_PASSED = True

def compare_two_lists(a , b):
    for x in a:
        if x not in b:
            print(f'{x} in the first list but not in the second one')
            return False
        
    for y in b:
        if y not in a:
            print(f'{y} in the second list but not in the first one')
            return False
    return True

def pfs_csv_generator():
    """Creates a csv, containing detected faults of each tp using PFS.
    tps are full, or randomly generated if input size is large
    """
    for c in os.listdir(config.CKT_DIR):
        c = c.replace('.ckt','')
        if c in ['add2','c1','c2','c3','c4','cmini','x3mult', 'c17']:
            circuit_path = '../../data/ckt/'+c+".ckt"
            print(c)
            circuit = DFTCircuit(circuit_path)
            faults = FaultList(circuit=circuit)
            faults.add_all()

            tp_fault_df = pd.DataFrame(columns = ['tp']+[f.__str__() for f in faults.faults])

            tg = TPGenerator(circuit)
            tps = []
            # if (1<<len(circuit.PI)) < MAX_N_TP:
            tps = tg.gen_full()
            # else:
            #     tps = tg.gen_n_random(MAX_N_TP, unique=True)
            
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
                _, pfs_faults =  pfs.run(tps, save_log=False)
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
    for c in os.listdir(config.CKT_DIR):
        c = c.replace('.ckt','')
        if c in ['add2','c1','c2','c3','c4','cmini','x3mult']:

            circuit_path = '../../data/ckt/'+c+".ckt"
            print(c)
            circuit = DFTCircuit(circuit_path)
            faults = FaultList(circuit=circuit)
            faults.add_all()

            tp_fault_df = pd.DataFrame(columns = ['tp']+[f.__str__() for f in faults.faults])

            tg = TPGenerator(circuit)
            tps = []
            # if (1<<len(circuit.PI)) < MAX_N_TP:
            tps = tg.gen_full()
            # else:
                # tps = tg.gen_n_random(MAX_N_TP, unique=True)
            
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
            ppsf_faults = []
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

def compare_pfs_ppsf_same_tps(circuit_dir: list):
    """ Check whether the results of PFS and PPSF match for multiple random test patterns"""
    for dir in circuit_dir:
        for c in os.listdir(dir):
            print(c)
            try:
                circuit_path = os.path.join(dir, c)
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
                _, pfs_faults =  pfs.run(tps, save_log=False)
                pfs_faults = [f.__str__() for f in pfs_faults]
                
                ppsf = PPSF(circuit,faults=fault_list)
                ppsf_faults = ppsf.run(tps).keys()

                res = compare_two_lists(ppsf_faults, pfs_faults)
                if res:
                    if PRINT_PASSED:
                        print(f"{bcolors.OKGREEN}Passed\n{bcolors.ENDC}")
                else:
                    print(f"{bcolors.FAIL}Failed\n{bcolors.ENDC}")
            except Exception as e:
                print(e)
                print(c,'errored')

def run_logic_sim(circuit_dir=config.CKT_DIR):
    for c in os.listdir(circuit_dir):
        try:
            circuit_path = os.path.join(circuit_dir, c)
            print(c)
            circuit = Circuit(circuit_path)
            
            tg = TPGenerator(circuit=circuit)
            tp = tg.gen_single()
            circuit.logic_sim(tp)
            print(f"{bcolors.OKGREEN}Passed\n{bcolors.ENDC}")

        except:
            print(f"{bcolors.FAIL}Failed\n{bcolors.ENDC}")

def run_logic_sim_bitwise(circuit_dir=config.CKT_DIR):
    for c in os.listdir(circuit_dir):
        try:
            circuit_path = os.path.join(circuit_dir, c)
            print(c)
            circuit = Circuit(circuit_path)
            
            tg = TPGenerator(circuit=circuit)
            tps = tg.gen_n_random(100)

            tps_bin = [0] * len(circuit.PI)
            for i in range(len(tps_bin)):
                for j in range(len(tps)):
                    tps_bin[i] += (tps[j][i]*(2**j))
            
            circuit.logic_sim_bitwise(tps_bin)
            print(f"{bcolors.OKGREEN}Passed\n{bcolors.ENDC}")

        except:
            print(f"{bcolors.FAIL}Failed\n{bcolors.ENDC}")

def compare_csvs():
    for file in os.listdir('../../data/testings/pfs_single_fault_testing/'):
        if 'PFS' in file:
            pfs_csv = '../../data/testings/pfs_single_fault_testing/'+file
            ppsf_csv = pfs_csv.replace('PFS','PPSF')

            pfs_lines = open(pfs_csv).readlines()
            ppfs_lines = open(ppsf_csv).readlines()

            if compare_two_lists(pfs_lines, ppfs_lines):
                print('passed', file)
            else:
                print('failed: ',file)

def get_undetected_faults():
    """From CSVs"""
    undetected_faults = {}
    for file in os.listdir('../../data/testings/pfs_single_fault_testing/'):
        if 'PFS' in file: # same as PPSF files
            undetected_faults[file] = []
            pfs_csv = pd.read_csv('../../data/testings/pfs_single_fault_testing/'+file)
            for fault in pfs_csv: 
                if pfs_csv[fault].sum() == 0:
                    # print(fault)
                    undetected_faults[file].append(fault)
            print(file, undetected_faults[file])
            print('_'*50)

if __name__ == '__main__':

    # pfs_csv_generator()
    # ppsf_csv_generator()

    # compare_csvs()

    # get_undetected_faults()

    # pfs_check_with_dfs_old()
    # Result: Failed for c6288. 129@1 only in dfs.

    # ppsf_check_with_dfs_old()
    # Result: Failed for c6288. 129@1 only in dfs.
    
    # MAX_N_FAULT = 1 # if you want single tp
    # for i in range(5000):

    # compare_pfs_ppsf_same_tps(circuit_dir=ISCAS85)
    
    # for e in ISCAS85:
        # run_logic_sim(circuit_dir=e)
        # run_logic_sim_bitwise(circuit_dir=e)

    """Trouble-shooting loading of some circuits"""

    # c = Circuit(os.path.join(config.CKT_DIR, 'c1908.ckt')) # Gate and PI IPT
