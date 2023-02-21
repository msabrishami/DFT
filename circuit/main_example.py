from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
import config

if __name__ == '__main__':

    # circuit_path = '../data/verilog/ISCAS85/v1/c17_synV1.v'
    circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v2/c5315_synV2.v'
    # circuit_path = '../data/ckt/c880.ckt'

    circuit = DFTCircuit(circuit_path)

    # #################### PFS Example ####################

    ppsf = PPSF(circuit, fault_mode='all')
    # ppsf.add_all_faults()
    print('all faults:', len(ppsf.fault_list.faults))
    tp = 100
    # ppsf.pd_ppsf(tp=tp, steps=config.PPSF_STEPS, verbose=True, cpu=3, ci = 2) #conf
    print('_'*50)
    ppsf.pd_ppsf(tp=tp, verbose=True, cpu=2)

    # # tp = 200
    # # tp = '../data/patterns/c432_synV1_tp_200.tp'
    # # tp = '../hello_world'
    # # tp = circuit.gen_multiple_tp(20)
    # # tp = circuit.gen_full_tp()
    # ppsf.fs_exe(tp, verbose=True)

    # print(circuit.__str__())
    # for n in circuit.nodes_lev:
    #     print(n.gtype,len(n.unodes))

    # print(circuit)

    # my_test_circuit = DFTCircuit(circuit_path)
    # # print(circuit.nodes.keys())
    # # print(my_test_circuit.nodes_lev)

    # print(f"circuit {my_test_circuit.c_name} is read and levelized.")

    # ### TEST ###
    # # tp = circuit.gen_multiple_tp(1e6)
    # # tp = circuit.gen_full_tp()
    # # tp = circuit.gen_tp_file_full() --> returns string not int
    # # print(tp)
    # #################### PFS Example ####################

    # pfs = PFS(circuit, faults_mode='all')

    # tp = 5000
    # tp = '../hello'
    # tp = '../data/patterns/c432_synV1_tp_1000.tp'
    # pfs.fs_exe(tp, verbose=True)

    # #################### STAFAN_FC Example ####################

    # # tp = 1000
    # my_test_circuit.STAFAN(tp, num_proc=4)
    # fc = my_test_circuit.STAFAN_FC(tp)
    # print("Fault Coverage=", fc)
