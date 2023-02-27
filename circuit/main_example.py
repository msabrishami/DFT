from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
import config
from tp_generator import TPGenerator


if __name__ == '__main__':

    # circuit_path = '../data/verilog/ISCAS85/v1/c17_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v2/c5315_synV2.v'
    # circuit_path = '../data/verilog/ISCAS85/v0/c880_synV0.v'
    circuit_path = '../data/ckt/add2.ckt'

    circuit = DFTCircuit(circuit_path)

    # #################### PPSF Example ###################

    ppsf = PPSF(circuit)
    
    # f_dict = ppsf.run(tps=100, verbose=True, faults=10)
    # print('_'*50)
    
    # ppsf.multiprocess_ci_run(tp_steps=[int(i) for i in config.PPSF_STEPS[1:7]],
    #                          verbose=True, ci=1, process=8, fault_count=200)
    print('_'*50)    
    ##################### PFS Example ####################
    tg = TPGenerator(circuit)
    tp = tg.gen_n_random(200)

    pfs = PFS(circuit, faults='all')
    pfs.run(tp, verbose=True, save_log=True)
    print('_'*50)

    # #################### STAFAN_FC Example ##############

    # circuit.STAFAN(len(tp))
    # fc = circuit.STAFAN_FC(tp)
    # print("Fault Coverage=", fc)
    # print('_'*50)