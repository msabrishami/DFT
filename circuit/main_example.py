from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
import config
from tp_generator import TPGenerator


if __name__ == '__main__':

    # circuit_path = '../data/verilog/ISCAS85/v1/c17_synV1.v'
    circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v2/c5315_synV2.v'
    # circuit_path = '../data/ckt/c880.ckt'

    circuit = DFTCircuit(circuit_path)

    # #################### PPSF Example ###################

    # ppsf = PPSF(circuit, fault_mode='all')
    ppsf = PPSF(circuit)
    tp = 1000
    
    # good
    # ppsf.fs_exe(tps = tp, verbose=True)
    # print('_'*50)
    
    # error
    ppsf.parallel_run(steps=config.PPSF_STEPS, verbose=True, cpu=3, ci=2)
    print('_'*50)
    
    # good
    # ppsf.parallel_run(tp=tp, verbose=True, cpu=2)
    # print('_'*50)
    
    ##################### PFS Example ####################
    # tg = TPGenerator(circuit)
    # # tp = tg.gen_full_tp()
    # tp = tg.gen_multiple_tp(100)

    # pfs = PFS(circuit, faults_mode=20)
    # pfs.fs_exe(tp, verbose=True)
    # print('_'*50)

    # #################### STAFAN_FC Example ##############

    # circuit.STAFAN(len(tp))
    # fc = circuit.STAFAN_FC(tp)
    # print("Fault Coverage=", fc)
    # print('_'*50)