# pfs: 
#   single: each test pattern --> what faults it detect

# ideas: 1- check it with dfs existing results

# ppsf: in random k tps, how many times each fault is detected?

import os

from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
from fault_simulation.fault import FaultList
from tp_generator import TPGenerator
import pandas as pd

MAX_TP = (1<<6) #lower it
PFS_TESTING_DIR = '../data/testings/pfs_single_fault_testing'


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

def pfs_tester():
    """Creates a csv, containing detected faults of each tp.
    tps are full, or randomly generated if input size is large
    """
    for c in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        circuit_path = '../data/ckt/'+c+".ckt"
        
        circ = DFTCircuit(circuit_path)
        faults = FaultList()
        faults.add_all(circ)

        tp_fault_df = pd.DataFrame(columns = ['tp']+[f.__str__() for f in faults.faults])

        tg = TPGenerator(circ)
        tps = []
        if (1<<len(circ.PI)) < MAX_TP:
            tps = tg.gen_full_tp()
        else:
            tps = tg.gen_multiple_tp(MAX_TP, unique=True)
        
        for tp in tps:
            pfs = PFS(circ, faults) #rename to faults
            detected_faults = pfs._one_tp_run(tp)
            row = {}

            # each tp is int(binary_from)
            row['tp'] = int("".join(map(str, tp)), 2) #--> another idea: save tps in a file and use their line number in the csv as tp 
            for f in detected_faults:
                row[f.__str__()] = "1"
            # tp_fault_df = pd.concat([tp_fault_df, pd.DataFrame(row)], axis = 0)
            tp_fault_df = tp_fault_df.append(row, ignore_index = True)

        tp_fault_df.to_csv(f'{PFS_TESTING_DIR}/singleFS_{circ.c_name}_{len(faults.faults)}f_{len(tps)}tp.csv',index=False)            

def pfs_single_tp_checker_pfs_dfs_old():
    """Checks result of DFT.PFS._one_tp_run() and dfs_old for full faults and single tps from dfs_old."""

    for c_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        print('\n',c_file)
        circuit = None
        
        for tp_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/'):
            pfs_faults = []
            dfs_faults = []
            if 'count-1_' in tp_file:
                tp = open(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/{tp_file}','r')
                tp = list(map(int, tp.readlines()[1].replace('\n','').split(',')))
                circuit = DFTCircuit(f'../data/ckt/{c_file}.ckt')

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

                print(compare_fault_lists(dfs_faults, pfs_faults))

def pfs_multiple_tp_checker_pfs_dfs_old():
    """Checks result of DFT.PFS._multiple_run() or run() and dfs_old for full faults and multiple tps from dfs_old."""
    for c_file in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2'):
        print('\n',c_file)
        circuit = None    
        for tp_file_name in os.listdir(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/'):
            pfs_faults = []
            dfs_faults = []
            if 'count-1_' not in tp_file_name:
                tp_file = open(f'{PFS_TESTING_DIR}/dfs_phase2/{c_file}/input/{tp_file_name}','r')
                tps = []
                for line in tp_file.readlines()[1:]:
                    tps.append(list(map(int, line.replace('\n','').split(','))))
                circuit = DFTCircuit(f'../data/ckt/{c_file}.ckt')

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

                print(compare_fault_lists(pfs_faults, pfs_faults))
            
if __name__ == '__main__':

    # dft_pfs_tester()

    pfs_single_tp_checker_pfs_dfs_old()
    # Result: 6288
    # for all single tps in /dfs_phase2, dfs finds fault 1290@1 while pfs does not.

    # pfs_multiple_tp_checker_pfs_dfs_old()
    # Result: All passed!

    