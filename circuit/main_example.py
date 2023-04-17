import os
from circuit.circuit import Circuit
from circuit.dft_circuit import DFTCircuit
from fault_simulation.ppsf import PPSF
from fault_simulation.pfs import PFS
from fault_simulation.fault import FaultList
import config
from tp_generator import TPGenerator

# RUN = 'TEST'
RUN = 'V3'
# RUN = 'logicsim'

if __name__ == '__main__':

    # circuit_path = '../data/ckt/c499.ckt'
    circuit_path = '../data/ckt/add2.ckt'
    # circuit_path = '../data/ckt/c2.ckt'
    # circuit_path = '../data/ckt/c4.ckt'
    # circuit_path = '../data/ckt/c17.ckt'
    # circuit_path = '../data/ckt/c3540.ckt'
    # circuit_path = '../data/ckt/c1908.ckt'

    circuit = DFTCircuit(circuit_path)
    f = FaultList(circuit)
    f.add_all()
    for fa in f.faults:
        print(fa)
    # circuit.SCOAP_CC()
    # circuit.SCOAP_CO()

    # for n in circuit.nodes_lev:
    #     # print(n.num, f'{n.CO=}', f'{n.CC=}')
    #     print(n.num, f'{n.CC0=}', f'{n.CC1=}', f'{n.CO=}')

    if RUN == "logicsim":
        for _ in range(100):
            # circuit_path =  '../data/ckt/c1355_new.ckt'
            circuit_path =  '../data/verilog/ISCAS85/v0/c880_synV0.v'
            circuit = DFTCircuit(circuit_path)
            tg = TPGenerator(circuit)
            tp = tg.gen_single()
            a = circuit.logic_sim(tp)

            circuit_path = '../data/ckt/c880_new.ckt'
            circuit = DFTCircuit(circuit_path)
            b = circuit.logic_sim(tp)
            if a != b:
                print(False)
    
    ########################TEST PFS ###############################
    if RUN == 'TEST':
        tg = TPGenerator(circuit)
        tps= tg.gen_full()
        faults = FaultList(circuit)
        faults.add_n_random()
        pfs = PFS(circuit, faults)

        for tp in tps:
            print(tp)
            print(pfs._one_tp_run(tp))
    # #################### Ghazal's Experiments ###################
    """V0"""
    if RUN == "V0":
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
        plt.show()
        
    """V1"""
    if RUN == 'V1': # Not correct
        fl = FaultList(circuit)
        # fl.add_n_random(100)
        fl.add_all()
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
            # print(random_fault.__str__())
            # for n in circuit.nodes_lev:
            #     print(n.num, n.value, n.gtype)

            """PART 2"""
            # print(tp)
            tg = TPGenerator(circuit)
            be_tested_tps = tg.gen_partial(tp)
            # print('TP:')
            # # print('PARTIALS:')
            # print(be_tested_tps)
            # for k in be_tested_tps:
            #     print(k)
            faults = FaultList()
            faults.add_fault(random_fault)
            # for fault in faults.faults:
                # print(fault.__str__())
            # x = input()
            
            # print(be_tested_tps)
            # print(random_fault.__str__())
            pfs = PFS(circuit, faults)
            # for f in faults.faults:
                # print(f)

            is_detectable = False
            for tp_b in be_tested_tps:
                detected_faults = pfs._one_tp_run(tp_b)
                if random_fault in detected_faults:
                    is_detectable = True
                    break

            if not is_detectable:
                print(f'Fault {random_fault.__str__()} is not detectable.')
                # print(detected_faults)
            print('______________________')

            # ppsf = PPSF(circuit, faults)
            # pfs.run(be_tested_tps, verbose=True)
            # ppsf.run(be_tested_tps, verbose=True)

            # print(f'fault={random_fault.__str__():<5}, gate type={circuit.fault_to_node(random_fault).gtype:<4}'
            #       f', --> all={len(tp)}, {constants=}, {variables=}, {ineffective=}, input reduction percent={100*(len(tp)-variables)/len(tp):.1f}%')
            # print(tp)
            # new_tps.append(tp)

    if RUN == 'V2':
        circuit.nodes_lev[11].value = 0
        print('Before:')
        print([f'{n.num}:{n.value}' for n in circuit.nodes_lev])

        circuit.imply_and_check_v2(circuit.nodes_lev[5])
        print('After')
        print([f'{n.num}:{n.value}' for n in circuit.nodes_lev])

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

    # pfs = PFS(circuit)
    # pfs.run(tps=10000, verbose=True, save_log=True, faults = 'all')
    # print('_'*50)

    # #################### STAFAN_FC Example ##############
    # tp_count = 10000
    # circuit.STAFAN(tp_count, num_proc=1)
    # fc = circuit.STAFAN_FC()
    # print("Fault Coverage Estimation=", fc)
    # print('_'*50)