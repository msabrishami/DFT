# written in pfs_ppsf_test.py

import os
import sys

sys.path.append('../')
import config
from tp_generator import TPGenerator

from circuit.circuit import Circuit

PRINT_PASSED = True

if __name__ == '__main__':
    for dir in [config.CKT_DIR]:
        for cname in os.listdir(dir):
            if cname.endswith('v') or cname.endswith('ckt') and '_new' in cname:
                passed = True
                try:
                    c = Circuit(os.path.join(dir,cname))
                except Exception as e:
                    print(e)
                    passed = False
                    print(dir,cname, ':\terror in reading\n\n\n')
                # try: # [Test 1]
                    tg = TPGenerator(c)
                #     single_tp = tg.gen_single()
                #     c.logic_sim(single_tp)
                #     print('logic_sim passed')
                # except Exception as e:
                #     # print(e)
                #     passed = False
                #     print(cname, ':\terror in single test implication')
                
                # try: # [Test 2]
                #     temp_fname = 'temp.txt'
                #     tg.gen_file(1, tp_fname=temp_fname)
                #     single_tp = tg.load_file(temp_fname)
                #     c.logic_sim(single_tp)
                # except Exception as e:
                #     print(e)
                #     passed = False
                #     print(cname, ':\terror in test generating/reading test')

                # if PRINT_PASSED and passed:
                #     print(dir, cname, ':\tpassed')

                # or_count = 0
                # and_count = 0
                # nand_count = 0
                # nor_count = 0
                # other_count = 0
                # xor_count = 0
                # xnor_count = 0
                # brch_count = 0
                # ipt_count = 0
                # buff_count = 0
                # not_count = 0
                # po_count = 0
                # for n in c.nodes_lev:
                #     if n.gtype == 'NOR':
                #         nor_count += 1
                #     elif n.gtype == 'OR':
                #         or_count += 1
                #     elif n.gtype == 'NAND':
                #         nand_count += 1
                #     elif n.gtype == 'AND':
                #         and_count += 1
                #     elif n.gtype == 'XOR':
                #         xor_count += 1
                #     elif n.gtype == 'XNOR':
                #         xnor_count += 1
                #     elif n.gtype == 'BRCH':
                #         brch_count += 1
                #     elif n.gtype == 'IPT':
                #         ipt_count += 1
                #     elif n.gtype == 'BUFF':
                #         buff_count += 1
                #     elif n.gtype == 'NOT':
                #         not_count += 1
                #     if n.ntype == 'PO':
                #         po_count += 1
                    
                    
                #     else:
                #         other_count += 1
                # print(f'{or_count=}, {and_count=}, {nand_count=}, {nor_count=}, {xor_count=}, {xnor_count=}\n'
                #     f'{ipt_count=}, {brch_count=}, {not_count=}, {buff_count=},  {other_count=}')
                # print(f'{po_count=}')
                # print(f'#GATES = ',not_count+and_count+or_count+nand_count+nor_count+xor_count+xnor_count,'\n\n')
    # os.system(f'rm {temp_fname}')