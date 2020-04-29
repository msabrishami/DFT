import re
from pfs import pfs
def faultdict_gen(input_nodes, nodelist_order):
    #generating full_fault_list for pfs to get full dictionary
    full = open('../tests/full_fault_list.txt', 'w')
    for i in range(len(nodelist_order)):
        full.write('%d@0\n' % nodelist_order[i].num)
        full.write('%d@1\n' % nodelist_order[i].num)
    full.close()


    #produce 2^n different input files for pfs to use
    fault_dict = {}
    inputnum = len(input_nodes)
    total_pattern = pow(2,inputnum)

    for i in range(total_pattern):
        #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
        b = ('{:0%db}'%inputnum).format(i)
        test_dict = open("../tests/temp_dict.txt", "w")
        for j in range(inputnum):
            test_dict.write("%d,%s\n" % (input_nodes[j],b[j]))
        test_dict.close()

    #do pfs based on the prodeuced input files
        fault = []
        pfs("../tests/temp_dict.txt", nodelist_order, '../tests/full_fault_list.txt')
        fault_list = open("../tests/pfsoutput.txt", "r")
        content1 = fault_list.readline()
        content1 = content1.strip('\n')
        while (content1 != ""):
            fault.append(content1)
            content1 = fault_list.readline()
            content1 = content1.strip('\n')
        fault_list.close()

        fault.sort(key = lambda i:int(re.match(r'(\d+)',i).group()))
        #jb51.net/article/164342.htm for referance to sort the output

        fault_dict.update({b: fault})
    
    dict_for_equv = {}
    for i in range (len(nodelist_order)):
        dict_for_equv.update({"%d@0" % nodelist_order[i].num:[]})
        dict_for_equv.update({"%d@1" % nodelist_order[i].num:[]})
    
    for i in (fault_dict):
        for j in (fault_dict.get(i)):
            dict_for_equv.get(j).append(i)

        


    fault_dict_result = open("../tests/fault_dict.txt", "w")
    for i in range(len(input_nodes)):
        if (i<len(input_nodes)-1):
            fault_dict_result.write('%d->' % input_nodes[i])
        else:
            fault_dict_result.write('%d' % input_nodes[i])
    fault_dict_result.write(' as sequence of inputs')    
    fault_dict_result.write('\n')
    fault_dict_result.write('input_patterns\t\t\tdetected_faults\n')
    for i in range(total_pattern):
        #print ('{:05b}'.format(i))#str type output #Suit different input numbers!!!!
        b = ('{:0%db}'%inputnum).format(i)
        fault_dict_result.write('%s\t\t\t\t' % b)
        for i in range(len(fault_dict.get(b))):
            fault_dict_result.write('%-5s ' % fault_dict.get(b)[i])#format ok?
        fault_dict_result.write('\n')
        
    fault_dict_result.close()
    
    #Requires full_fault_list for this dictionary!!!!!!!!!
    return dict_for_equv