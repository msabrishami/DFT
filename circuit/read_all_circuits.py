# Later, these should be tested using pytest

from circuit.circuit import Circuit
import os
from tp_generator import TPGenerator

DIR1= '../data/ckt/'

DIR2= '../data/verilog/ISCAS85/v0/'
DIR3= '../data/verilog/ISCAS85/v1/'
DIR4= '../data/verilog/ISCAS85/v2/'

DIR5= '../data/verilog/EPFL/v0/'
DIR6= '../data/verilog/EPFL/v1/'
DIR7= '../data/verilog/EPFL/v2/'

DIR8 = '../data/verilog/ISCAS89'

ALL_DIRS = [DIR1,DIR2,DIR3,DIR4,DIR5,DIR6,DIR7,DIR8]

PRINT_PASSED = False

if __name__ == '__main__':
    for dir in ALL_DIRS:
        for cname in os.listdir(dir):
            if cname.endswith('v') or cname.endswith('ckt'):
                passed = True
                try:
                    c = Circuit(os.path.join(dir,cname))
                except Exception as e:
                    # print(e)
                    passed = False
                    print(cname, ':\terror in reading')
                
                try: # [Test 1]
                    tg = TPGenerator(c)
                    single_tp = tg.gen_single_tp()
                    c.logic_sim(single_tp)
                except Exception as e:
                    # print(e)
                    passed = False
                    print(cname, ':\terror in single test implication')
                
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
                    print(cname, ':\tpassed')

    # os.system(f'rm {temp_fname}')

# OUTPUT: [Test 1]
# c1908.ckt :	error in reading
# c5315.ckt :	error in reading
# c3540.ckt :	error in reading
# arbiter.v :	error in reading
# bar.v :	error in reading

# OUTPUT: [Test 2]
# too long!