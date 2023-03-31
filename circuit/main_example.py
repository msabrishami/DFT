import os
from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
from fault_simulation.fault import FaultList
import config
from tp_generator import TPGenerator


if __name__ == '__main__':

    # circuit_path = '../data/verilog/ISCAS85/v1/c17_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v1/c432_synV1.v'
    # circuit_path = '../data/verilog/ISCAS85/v2/c5315_synV2.v'
    # circuit_path = '../data/verilog/ISCAS85/v0/c880_synV0.v'
    # circuit_path = '../data/ckt/c432_old.ckt'
    # circuit_path = '../data/ckt/c432.ckt'
    # circuit_path = '../data/ckt/c3540_old.ckt'
    # circuit_path = '../data/ckt/c499.ckt'
    # circuit_path = '../data/ckt/c1.ckt'
    # circuit_path = '../data/ckt/c2.ckt'
    circuit_path = '../data/ckt/c4.ckt'
    # circuit_path = '../data/ckt/c17.ckt'
    # circuit_path = '../data/ckt/c3540.ckt'
    # circuit_path = '../data/ckt/c1908.ckt'
    # circuit_path = os.path.join(config.ISCAS89_DIR,'arbiter.v')
    # circuit_path = os.path.join(config.ISCAS89_DIR,'bar.v')

    circuit = DFTCircuit(circuit_path)
    # circuit.SCOAP_CC()
    # circuit.SCOAP_CO()

    # for n in circuit.nodes_lev:
    #     # print(n.num, f'{n.CO=}', f'{n.CC=}')
    #     print(n.num, f'{n.CC0=}', f'{n.CC1=}', f'{n.CO=}')

    # #################### Ghazal's Experiments ###################
    """V0"""
    po_nums = []
    print('#All PO', len(circuit.PO))

    for n in circuit.PI:
        print('node=',n.num, '--> #po=', len(circuit.get_fanout_PO(n)))
        po_nums.append(len(circuit.get_fanout_PO(n)))

    import matplotlib.pyplot as plt
    # plt.hist(x=po_nums)
    # plt.title(circuit.c_name)
    # plt.show()
    
    print('_'*50)
    pi_nums = []
    print('#All PI', len(circuit.PI))

    for n in circuit.PO:
        print('node=',n.num, '<-- #pi=', len(circuit.get_fanin_PI(n)))
        pi_nums.append(len(circuit.get_fanin_PI(n)))

    # plt.hist(x=pi_nums)
    # plt.title(circuit.c_name)
    # plt.show()
    print('_'*50)

    for n in circuit.nodes_lev:
        print(f'node:{n.num}, lev={n.lev}, reach to {len(circuit.get_fanout_PO(n))} POs, is fed by {len(circuit.get_fanin_PI(n))} PIs')
    
    print('_'*50)
    
    fanins_of_fanouts = []
    for n in circuit.nodes_lev:
        print(f'node:{n.num}, len(fanins of fanouts) = {len(circuit.imply_and_check_v0(n))}')
        fanins_of_fanouts.append(len(circuit.imply_and_check_v0(n)))
    plt.hist(x=fanins_of_fanouts)
    plt.title(circuit.c_name)
    # plt.show()
    
    """V1"""
    fl = FaultList(circuit)
    # fl.add_n_random(100)
    fl.add_all()
    # random_fault = fl.faults[0]
    for random_fault in fl.faults:
        tp = circuit.imply_and_check_v1(random_fault)
        constants = 0
        variables = 0
        ineffective = 0
        for t in tp:
            if t == 1 or t == 0:
                constants+=1
            elif t == config.X_VALUE:
                variables+=1
            elif t == '_':
                ineffective += 1
        
        tg = TPGenerator(circuit)
        be_tested_tps = tg.gen_partial(tp)
        print('TP:')
        print(tp)
        print('PARTIALS:')
        print(be_tested_tps)
        print('______________________')
        # input()
        # faults = FaultList()
        # faults.add(circuit.fault_to_node(random_fault), int(random_fault.__str__()[-1]))
        # pfs = PFS(circuit, faults)
        # pfs.run(be_tested_tps)

        # print(f'fault={random_fault.__str__():<5}, gate type={circuit.fault_to_node(random_fault).gtype:<4}'
            #   f', --> all={len(tp)}, {constants=}, {variables=}, {ineffective=}, input reduction percent={100*(len(tp)-variables)/len(tp):.1f}%')
        # print(tp)
        # new_tps.append(tp)


    ################# Manially testing ####################
    # for p in circuit.PI:
    #     print(p.num)
    # tp = [1, 1, 1, 1, 1]
    # print(circuit.logic_sim(tp))
    # tp = [1, 0, 1, 1, 1]
    # print(circuit.logic_sim(tp))

    # #################### PPSF Example ###################

    # ppsf = PPSF(circuit)
    # tg = TPGenerator(circuit)
    # # tps = tg.gen_full()
    # f_dict = ppsf.run(tps=20000, verbose=True, save_log=True)
    # ppsf._multiprocess_handler()
    # # print('_'*50)
    # ppsf.multiprocess_ci_run(tp_steps=[10, 20, 30],#op=circuit.nodes_lev[5],
    #                          verbose=True, ci=1, process=8, fault_count='all', save_log=True)
    # ppsf.
    # print('_'*50)    
    
    ##################### PFS Example ####################

    # tg = TPGenerator(circuit)
    # tp = tg.gen_single(mode='x')

    # print(circuit.logic_sim_t(tp))


    # pfs = PFS(circuit, faults='all')
    # pfs.run(tps=10000, verbose=True, save_log=True)
    # print('_'*50)

    # #################### STAFAN_FC Example ##############
    # tp_count = 10000
    # circuit.STAFAN(tp_count, num_proc=1)
    # fc = circuit.STAFAN_FC()
    # print("Fault Coverage Estimation=", fc)
    # print('_'*50)