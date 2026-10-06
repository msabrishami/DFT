# from g-exp

# # TODO-Ghazal: not checked by MSA
# def diff_tp_stafan(circuit, tps): #TODO: Must be changed
#     """
#     Fault coverage estimation
#     STAFAN measures are calculates many times with different tpLoad count of test patterns.
#     Then, the fault coverage is calculated using STAFAN values with the correspoing tp count.
#     TODO: list of tps should be generated automatically according to ?
#     """

#     set = 0
#     fc_sequence = []
#     tp_sequence = []
#     for tp in tps:
#         f = f"{tp}-{set}"
#         path = f"{config.STAFAN_DIR}/{circuit.c_name}"
#         if not os.path.exists(path):
#             os.makedirs(path)
#         fname = f"{path}/{circuit.c_name}-tp{f}.stafan"
#         if not os.path.exists(fname):
#             tpc = re.findall(r"\d+", f)[0]
#             circuit.STAFAN(int(tpc))
#             circuit.save_STAFAN(tp=tp, fname=fname)
#         else:
#             circuit.load_TMs(fname)

#         try:
#             fc_sequence.append(circuit.STAFAN_FC(tp)*100)
#             tp_sequence.append(tp)
#         except:
#             continue

#     plot = sns.lineplot(x=tp_sequence, y=fc_sequence,
#                         color="green", label = "STAFAN (different tpLoads)")
#     plot = sns.scatterplot(x=tp_sequence, y=fc_sequence, color="green") #draw dots
    
#     plt.xscale("log")
#     plot.set_ylabel(f"Fault Coverage (FC%)", fontsize=13)
#     plot.set_xlabel("Test Pattern Count #TP", fontsize=13)
#     plot.set_title(
#         f"Dependency of fault coverage on random test patterns\n\
#         for circuit {circuit.c_name}\n \
#         method: STAFAN (different tpLoads)", fontsize=13)

#     # path = f"{config.FIG_DIR}/{circuit.c_name}/estimation-diff-tploads/"
#     path = "./results/figures/"
#     if not os.path.exists(path):
#         os.makedirs(path)

#     fname = path+f"tpfc-stafan-diff-tpLoad-{circuit.c_name}.png"
#     print(f"Figure saved in {fname}")
#     plt.tight_layout()
#     plt.savefig(fname)

# experiments for reconvergent fanouts.
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
                fl_temp = pfs._one_tp_run(tp_b)
                if random_fault in fl_temp:
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

    ################# Manually testing ####################
    # for p in circuit.PI:
    #     print(p.num)
    # tp = [1, 1, 1, 1, 1]
    # print(circuit.logic_sim(tp))
    # tp = [1, 0, 1, 1, 1]
    # print(circuit.logic_sim(tp))
