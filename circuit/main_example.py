from Circuit import circuit
from FaultSimulation.ppsf import PPSF
from FaultSimulation.pfs import PFS

if __name__ == '__main__':

    circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'

    circuit = circuit.Circuit(circuit_path)
    circuit.lev()

    print(f"circuit {circuit.c_name} is read and levelized.")

    ### TEST ###
    # tp = circuit.gen_multiple_tp(1e6)
    # tp = circuit.gen_full_tp()
    # tp = circuit.gen_tp_file_full() --> returns string not int
    # print(tp)
    #################### PFS Example ####################
   
   # todo: fault drop!!!!!
    pfs = PFS(circuit)
    pfs.fault_list.add_all(circuit)

    # tp = 500
    # tp = '../hello'
    tp = '../data/patterns/c432_synV1_tp_1000.tp'
    pfs.fs_exe(tp, fault_drop=2, verbose=True)

    #################### PFS Example ####################
    
    # ppsf = PPSF(circuit)
    # ppsf.fault_list.add_all(circuit)
    # tp = 200
    # tp = '../data/patterns/c432_synV1_tp_200.tp'
    # tp = '../hello_world'
    # tp = circuit.gen_multiple_tp(20)
    # tp = circuit.gen_full_tp()
    # ppsf.fs_exe(tp, verbose=True)

    #################### STAFAN_FC Example ####################
    
    tp = 1000
    circuit.STAFAN(tp, num_proc=4)
    fc = circuit.STAFAN_FC(tp)
    print("Fault Coverage=", fc)
    # for n in circuit.nodes_lev:
    #     n.print_info()