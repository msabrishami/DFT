from circuit import Circuit
from ppsf import PPSF
from pfs import PFS

if __name__ == '__main__':

    circuit_path = '../data/verilog/ISCAS85/v1/c499_synV1.v'

    circuit = Circuit(circuit_path)
    circuit.lev()

    print(f"circuit {circuit.c_name} is read and levelized.")

    #################### PFS Example ####################
   
   # todo: fault drop!!!!!
    pfs = PFS(circuit)
    pfs.fault_list.add_all(circuit)

    tp = 500
    # tp = '../hello'
    # tp = '../data/patterns/c499_synV1_tp_1000.tp'
    pfs.fs_exe(tp, fault_drop=0, verbose=True)

    #################### PFS Example ####################
    
    ppsf = PPSF(circuit)
    ppsf.fault_list.add_all(circuit)
    tp = 200
    # tp = '../data/patterns/c432_synV1_tp_200.tp'
    # tp = '../hello_world'
    ppsf.fs_exe(tp, verbose=True)

    #################### STAFAN_FC Example ####################
    
    circuit.STAFAN(tp, num_proc=4)
    tp = 1000
    fc = circuit.STAFAN_FC(tp)
    print("Fault Coverage=", fc)