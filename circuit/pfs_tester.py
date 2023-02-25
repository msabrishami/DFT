# pfs: 
#   single: each test pattern --> what faults it detect

# ideas: 1- check it with dfs existing results

# ppsf: in random k tps, how many times each fault is detected?

import os
import config

from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
from fault_simulation.fault import FaultList
from tp_generator import TPGenerator
import pandas as pd

MAX_TP = (1<<6)
PFS_TESTING_DIR = '../data/testings/pfs_single_fault_testing'

def dft_pfs_tester():
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


def pfs_checker_dft_dfs_old():
    for c in os.listdir('../data/testings/pfs_single_fault_testing/dfs_phase2'):
        pass
        # tp_fault_df = pd.read_csv(f'../data/testing/pfs_single_fault_testing/singleFS_{circ.c_name}_{len(faults.faults)}f_{len(tps)}tp.csv')


if __name__ == '__main__':


    # dft_pfs_tester()
    # pfs_checker_dft_dfs_old()
    myc = DFTCircuit('../data/ckt/c6288.ckt')
    tg = TPGenerator(myc)
    tps = tg.gen_full_tp()
    print(len(myc.PI))
    print(len(tps))
    # for t in tps:
    #     print(t)