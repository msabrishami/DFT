import math
import os
import config
from circuit import Circuit

def regular_tp_gen(circuit):
        num = len(circuit.PI)
        times = pow(2, num)
        pattern = []
        output_path = config.FAULT_SIM_DIR
        if not os.path.exists(output_path):
                os.mkdir(output_path)
        output_path = (output_path + '/' + circuit.c_name + '/')
        if not os.path.exists(output_path):
                os.mkdir(output_path)
        output_path = (output_path + '/input/')
        if not os.path.exists(output_path):
                os.mkdir(output_path)
        fw = open(output_path + circuit.c_name + '_full_tp_b.txt', mode='w')
        PI_list = []
        for node in circuit.PI:
                PI_list.append(node.num)
        PI_string = ','.join(PI_list)
        print(PI_string)
        fw.write(PI_string + '\n')
        for i in range(times):
                # print(bin(i)[2:].zfill(num))
                pattern = list(bin(i)[2:].zfill(num))
                pattern_str = ",".join(pattern)
                print(pattern_str)
                fw.write(pattern_str + '\n')

