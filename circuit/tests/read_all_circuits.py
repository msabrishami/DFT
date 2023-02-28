# written in pfs_ppsf_test.py

import os
import sys

sys.path.append('../')
import config
from tp_generator import TPGenerator

from circuit.circuit import Circuit

PRINT_PASSED = True

if __name__ == '__main__':
    for dir in config.ALL_CIRCUIT_DIRS:
        for cname in os.listdir(dir):
            if cname.endswith('v') or cname.endswith('ckt'):
                passed = True
                try:
                    c = Circuit(os.path.join(dir,cname))
                except Exception as e:
                    # print(e)
                    passed = False
                    print(dir,cname, ':\terror in reading')
                
                # try: # [Test 1]
                #     tg = TPGenerator(c)
                #     single_tp = tg.gen_single()
                #     c.logic_sim(single_tp)
                # except Exception as e:
                #     # print(e)
                #     passed = False
                    # print(cname, ':\terror in single test implication')
                
                # try: # [Test 2]
                #     temp_fname = 'temp.txt'
                #     tg.gen_tp_file(1, tp_fname=temp_fname)
                #     single_tp = tg.load_tp_file(temp_fname)
                #     c.logic_sim(single_tp)
                # except Exception as e:
                #     # print(e)
                #     passed = False
                #     print(cname, ':\terror in test generating/reading test')

                if PRINT_PASSED and passed:
                    print(dir, cname, ':\tpassed')

    # os.system(f'rm {temp_fname}')

# OUTPUT: [Test 1]
# c1908.ckt :	error in reading
# c5315.ckt :	error in reading
# c3540.ckt :	error in reading
# arbiter.v :	error in reading
# bar.v :	error in reading

# OUTPUT: [Test 2]
# too long!