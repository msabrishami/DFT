import os
from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
import config
from tp_generator import TPGenerator


if __name__ == '__main__':

    circuit_path = '../data/verilog/ISCAS85/v1/c17_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v2/c5315_synV2.v'
    # circuit_path = '../data/verilog/ISCAS85/v0/c880_synV0.v'
    circuit_path = '../data/ckt/c17.ckt'
    # circuit_path = os.path.join(config.ISCAS89_DIR,'arbiter.v')
    # circuit_path = os.path.join(config.ISCAS89_DIR,'bar.v')

    circuit = DFTCircuit(circuit_path)

    # #################### PPSF Example ###################

    # ppsf = PPSF(circuit)

    # f_dict = ppsf.run(tps=5, verbose=True, save_log=True)
    # # print('_'*50)
    # ppsf.multiprocess_ci_run(tp_steps=[10, 20, 30],#op=circuit.nodes_lev[5],
    #                          verbose=True, ci=1, process=8, fault_count='all', save_log=True)
    # ppsf.
    # print('_'*50)    
    
    ##################### PFS Example ####################

    tg = TPGenerator(circuit)
    tp = tg.gen_single(mode='x')

    print(circuit.logic_sim_t(tp))


    # pfs = PFS(circuit, faults='all')
    # pfs.run(tps=10000, verbose=True, save_log=True)
    # print('_'*50)

    # #################### STAFAN_FC Example ##############
    # tp_count = 10000
    # circuit.STAFAN(tp_count, num_proc=1)
    # fc = circuit.STAFAN_FC()
    # print("Fault Coverage Estimation=", fc)
    # print('_'*50)