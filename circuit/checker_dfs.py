import xlrd
import os
from itertools import groupby
from circuit import *

def FD_excel_extractor(c_name):
    # output golden file
    output_path = '../data/modelsim/' + c_name + '/input/'
    fw = open(output_path + c_name + '_FD_golden.txt', mode='w')
    # Give the location of the file
    fr = ("../../simple_circuits/" + c_name + "/" + c_name + "_FD.xlsx")
    # To open Workbook
    wb = xlrd.open_workbook(fr)
    sheet = wb.sheet_by_index(0)
    for i in range(2, sheet.nrows):
        pattern = list(sheet.cell_value(i, 0))
        pattern_str = ','.join(pattern)
        fw.write(pattern_str + '\n')
        for j in range(2, sheet.ncols):
            if sheet.cell_value(i, j) == 'x':
                fw.write(str(int(sheet.cell_value(1, j))) + '@' + str(int(sheet.cell_value(0, j))) + '\n')
        fw.write('\n')






def dfs_pfs_checker(circuit, tp_num=1, mode='rand'): 
    golden_path = config.FAULT_SIM_DIR + '/' + circuit.c_name + '/dfs/'
    output_path = config.FAULT_SIM_DIR + '/' + circuit.c_name + '/pfs/'
    result_path = config.FAULT_SIM_DIR + '/' + circuit.c_name + '/compare/'
    if not os.path.exists(result_path):
                os.mkdir(result_path)
    if mode == 'rand':
        dfs_report_fname = circuit.c_name + '_' + str(tp_num) + '_dfs_b.log'
        pfs_report_fname = circuit.c_name + '_' + str(tp_num) + '_pfs_b.log'
        path_golden = golden_path + dfs_report_fname
        path_output = output_path + pfs_report_fname
        result_file = result_path + circuit.c_name + '_' + str(tp_num) + '_dfs_pfs_compare.txt'
        fw = open(result_file, 'w')
        file_golden = open(path_golden, mode='r+')
        file_out = open(path_output, mode='r+')
        line_golden = file_golden.readlines()
        line_golden = line_golden[:-1]
        line_out = file_out.readlines()
        line_out = line_out[:-1]

        pass_flag = 0
        for i in range(len(line_golden)):
            if line_golden[i] == line_out[i]:
                pass
            elif line_golden[i] != line_out[i]:
                fw.write('results are different!\n')
                pass_flag=1
                break

        if pass_flag == 0:
            fw.write('results are the same!\n')


    elif mode == 'full':
        dfs_report_fname = circuit.c_name + "_full_dfs_b.log"
        pfs_report_fname = circuit.c_name + "_full_pfs_b.log"
        path_golden = golden_path + dfs_report_fname
        path_output = output_path + pfs_report_fname
        result_file = result_path + circuit.c_name + '_full_dfs_pfs_compare.txt'
        fw = open(result_file, 'w')
        if os.stat(path_golden).st_size == 0:
            print('Golden file is empty!')
            fw.write('Golden file is empty!\n')
            return   
        if os.stat(path_output).st_size == 0:
            print('Output file is empty!')
            fw.write('Output file is empty!\n')
            return
        file_golden = open(path_golden, mode='r+')
        file_out = open(path_output, mode='r+')

        content_golden = map(lambda line: len(line) > 1 and line[:-1], list(file_golden))
        content_out = map(lambda line: len(line) > 1 and line[:-1], list(file_out))
        
        gen_golden = (list(g) for _, g in groupby(content_golden, key='\n'.__ne__))
        patterns_golden = [a + b for a, b in zip(gen_golden, gen_golden)]  
        gen_out = (list(g) for _, g in groupby(content_out, key='\n'.__ne__))
        patterns_out = [a + b for a, b in zip(gen_out, gen_out)]
        
        i, j = 0, 0
        while i < len(patterns_golden) and j < len(patterns_out):
            if patterns_golden[i] == patterns_out[j]:
                print(patterns_golden[i][0] + ': correct')
                fw.write(patterns_golden[i][0] + ': correct\n')
            else:
                print(patterns_golden[i][0]+ ': wrong')
                fw.write(patterns_golden[i][0]+ ': wrong\n')
                set_golden, set_out = set(patterns_golden[i]), set(patterns_out[j])
                dif_golden, dif_out = set_golden - set_out, set_out - set_golden
                longer_dif = dif_golden if len(dif_golden) > len(dif_out) else dif_out
                longer_dif = sorted(list(longer_dif), key = lambda dif: int(dif[:-2]))
                print('Golden\tOutput')
                fw.write('Golden\tOutput\n')
                for dif in longer_dif:
                    num0, num1 = dif[:-1] + '0', dif[:-1] + '1'
                    ele_golden = num0 if num0 in dif_golden else num1 if num1 in dif_golden else 'None'
                    ele_out = num0 if num0 in dif_out else num1 if num1 in dif_out else 'None'
                    print(ele_golden + '\t' + ele_out)
                    fw.write(ele_golden + '\t' + ele_out + '\n')
            print('\n')
            fw.write('\n')       
                
            i, j = i + 1, j + 1
        
        if i < len(patterns_golden):
            print('Golden not compared patterns:')
            fw.write('Golden not compared patterns:\n')
            for idx in range(i, len(patterns_golden)):
                print(patterns_golden[idx][0])
                fw.write(str(patterns_golden[idx][0]) + '\n')
                
        if j < len(patterns_out):
            print('Output not compared patterns:')
            fw.write('Output not compared patterns:\n')
            for idx in range(j, len(patterns_out)):
                print(patterns_out[idx][0])
                fw.write(str(patterns_out[idx][0]) + '\n')
    else:
        raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")


    file_golden.close()
    file_out.close()


    # compare the dfs results with golden file
    # path = '../data/fault_sim/' + c_name + '/'
    # file_golden = open(path + c_name + '_FD_golden.txt', mode='r+')
    # file_out = open(path + c_name + '_full_dfs_out.txt', mode='r+')
    # number_of_line = 1
    # golden_line = file_golden.readline()
    # out_line = file_out.readline()
    # flag = 1
    # if len(golden_line) == 0:
    #     print("original file is empty!")
    #     flag = 0
    # if len(out_line) == 0:
    #     print("new file is empty!")
    #     flag = 0
    
    # if golden_line is not None and out_line is not None:
    #     while golden_line :
    #         if golden_line != '\n':
                
    #             if golden_line != out_line:
    #             print('file different! different line is #', number_of_line)
    #             flag = 0
    #         elif golden_line == '\n':

    #         else:
    #             flag = 1
    #         golden_line = file_golden.readline()
    #         out_line = file_out.readline()
    #         number_of_line += 1

    # if flag == 1:
    #     print('result are the same')
    # else:
    #     print("result are not same!")
    # file_golden.close()
    # file_out.close()

# dfs_checker(c_name = 'c17')