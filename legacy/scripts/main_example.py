import os
from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
from fault_simulation.fault import FaultList
import config
from tp_generator import TPGenerator
import pdb

# RUN = 'TEST'
RUN = '-'
# RUN = 'logicsim'

if __name__ == '__main__':

    # circuit_path = '../data/ckt/c17.ckt'
    # circuit_path = '../data/ckt/add2.ckt'
    # circuit_path = '../data/ckt/c2.ckt'
    # circuit_path = '../data/ckt/c4.ckt'
    # circuit_path = '../data/ckt/c3540.ckt'
    # circuit_path = '../data/ckt/c1908.ckt'
    # circuit_path = '../data/ckt/c5315.ckt'
    circuit_path = '../data/verilog/ISCAS85/v0/c1355_synV0.v'

    circuit = DFTCircuit(circuit_path)
    f = FaultList(circuit)
    # f.add_all()
    # print(circuit)
    # for fa in f.faults:
    #     print(fa)
    circuit.SCOAP_CC()
    circuit.SCOAP_CO()

    # for n in circuit.nodes_lev:
    #     # print(n.num, f'{n.CO=}', f'{n.CC=}')
    #     print(n.num, f'{n.CC0=}', f'{n.CC1=}', f'{n.CO=}')

    # #################### PPSF Example ###################

    ppsf = PPSF(circuit)
    # tg = TPGenerator(circuit)
    ppsf.multiprocess_ci_run(tp_steps=[50, 100, 500, 1000, 5000, 10000, 20000, 50000],
            #op=circuit.nodes_lev[5],
            verbose=True, ci=3, num_proc=8, fault_count='all', save_log=True)
    
    # tps = tg.gen_full()
    # f_dict = ppsf.run(tps=20000, verbose=True, save_log=True)
    # # print('_'*50)
    # print('_'*50)    
    
    ##################### PFS Example ####################

    # tg = TPGenerator(circuit)

    # pfs = PFS(circuit)
    # pfs.tpfc(1000, verbose=True)
    # pfs.run(tps=10000, verbose=True, save_log=True, faults = 'all')
    # print('_'*50)

    # #################### STAFAN_FC Example ##############
    # tp = 10000
    # circuit.STAFAN(tp, num_proc=1)
    # fc = circuit.STAFAN_FC(tp)
    # print("Fault Coverage Estimation=", fc)
    # print('_'*50)
