from circuit.circuit import Circuit
from circuit.testcircuit import TestCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS

if __name__ == '__main__':

    circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'

    # circuit = Circuit(circuit_path)
    my_test_circuit = TestCircuit(circuit_path)
    my_test_circuit.lev()
    # print(circuit.nodes.keys())
    # print(my_test_circuit.nodes_lev)

    print(f"circuit {my_test_circuit.c_name} is read and levelized.")

    ### TEST ###
    # tp = circuit.gen_multiple_tp(1e6)
    # tp = circuit.gen_full_tp()
    # tp = circuit.gen_tp_file_full() --> returns string not int
    # print(tp)
    #################### PFS Example ####################
   
    pfs = PFS(my_test_circuit)
    pfs.fault_list.add_all(my_test_circuit)

    tp = 100
    # # tp = '../hello'
    # # tp = '../data/patterns/c432_synV1_tp_1000.tp'
    pfs.fs_exe(tp, verbose=True)

    #################### PFS Example ####################
    
    ppsf = PPSF(my_test_circuit)
    ppsf.fault_list.add_all(my_test_circuit)
    # tp = 200
    # tp = '../data/patterns/c432_synV1_tp_200.tp'
    # tp = '../hello_world'
    # tp = circuit.gen_multiple_tp(20)
    # tp = circuit.gen_full_tp()
    ppsf.fs_exe(tp, verbose=True)

    #################### STAFAN_FC Example ####################
    
    # tp = 1000
    my_test_circuit.STAFAN(tp, num_proc=4)
    fc = my_test_circuit.STAFAN_FC(tp)
    print("Fault Coverage=", fc)