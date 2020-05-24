# input file type : .bench
# output file type : .ckt658
import re
def translator(src,dst):
    fin = open ('../circuits/' + src,'r')
    f = fin.readlines()
    fin.close()
    f = f[6:]
    count_list = len(f)
    for i in range(count_list):
        f[i] = f[i].strip('\n')
    f.remove('')
    f.remove('')
    # input file lists include 3 lists: PI list, PO list, internal list
    input_list = []
    output_list = []
    internal_list = []
    for item in f:
        if item[0] == 'I':
            input_list.append(item)
        if item[0] == 'O':
            output_list.append(item)
        if item[0] == '0' or item[0] == '1'or item[0] == '2'\
        or item[0] == '3'or item[0] == '4'or item[0] == '5'\
        or item[0] == '6'or item[0] == '7'or item[0] == '8'\
        or item[0] == '9':
            internal_list.append(item)

    ##print(input_list)
    ##print(output_list)
    ##print(internal_list)
    all_line_list = []
    input_of_gate_list = []
    gate_input_line = []
    for item in internal_list:
        all_line_list = all_line_list + re.findall('\d+', item)
        item_tmp = item.split('=')
        input_of_gate_list = input_of_gate_list + item_tmp

    for i in range(len(input_of_gate_list)):
        if (i % 2) == 1:
            gate_input_line = gate_input_line + re.findall('\d+', input_of_gate_list[i])

    line = [0] * len(all_line_list)
    line2 = [0] * len(gate_input_line)
    for i in range(len(all_line_list)):
        line[i] = int(all_line_list[i])
    for i in range(len(gate_input_line)):
        line2[i] = int(gate_input_line[i])

    line.sort(reverse=False)
    line2.sort(reverse=False)
    ##print(line)
    ##print(line2)
    branch_list = [0,0] * len(line2)
    a = line2
    b = set(a)
    i = 0
    for each_b in b:
        count = 0
        for each_a in a:
            if each_b == each_a:
                count += 1
        branch_list[i] = [each_b, count]
        i += 1
    while 0 in branch_list:
        branch_list.remove(0)
    ##print(branch_list)
    number_of_branch = 0
    for num in branch_list:
        if num[1] > 1:
            number_of_branch += 1
    ##print('number_of_branch = ', number_of_branch)
    number_of_line = len(line2) + len(output_list) + number_of_branch

    first_column = [-1] * number_of_line
    second_column = [-1] * number_of_line
    third_column = [-1] * number_of_line
    fourth_column = [-1] * number_of_line
    fifth_column = [-1] * number_of_line
    sixth_column = [''] * number_of_line

    ##print('number_of_line = ', number_of_line)

    new_line = list(set(line))
    ##print(new_line)
    for num in branch_list:
        if num[1] > 1:
            x = num[0]
            for index in range(len(new_line)):
                if x == new_line[index]:
                    for i in range(num[1]):
                        new_line.insert(index+i+1, x+i+1)
                        first_column[index+i+1] = 2
                        third_column[index+i+1] = 1
                        fourth_column[index+i+1] = num[0]
                    break
    ##print(len(new_line))
    for i in range(number_of_line):
        second_column[i] = new_line[i]

    PI_list = []
    for item in input_list:
        PI_list = PI_list + re.findall('\d+', item)
    for item in PI_list:
        a = second_column.index(int(item))
        first_column[a] = 1
        third_column[a] = 0
        fifth_column[a] = 0
    PO_list = []
    for item in output_list:
        PO_list = PO_list + re.findall('\d+', item)
    for item in PO_list:
        a = second_column.index(int(item))
        first_column[a] = 3
        fourth_column[a] = 0

    ## for third column gate indication
    def gate_index(string):
        out = 0
        if string.find('XOR') >= 0:
            out = 2
        elif string.find('NOR') >= 0:
            out = 4
        elif string.find('OR') >= 0:
            out = 3
        elif string.find('NOT') >= 0:
            out = 5
        elif string.find('NAND') >= 0:
            out = 6
        elif string.find('AND') >= 0:
            out = 7
        return out

    c = []
    for item in internal_list:
        c = item.split('=')
        a1 = int(c[0])
        a2 = second_column.index(a1)
        third_column[a2] = gate_index(item)
        a3 = len(re.findall('\d+', c[1]))
        fifth_column[a2] = a3

    for i in range(len(first_column)):
        if first_column[i] == -1:
            first_column[i] = 0

    branch_list_ext = []
    for num in branch_list:
        if num[1] > 1:
            fourth_column[second_column.index(num[0])] = num[1]
            branch_list_ext.append(num[0])

    for i in range(len(fourth_column)):
        if fourth_column[i] == -1:
            fourth_column[i] = 1

    for i in range(len(fifth_column)):
        if fifth_column[i] == -1:
            fifth_column[i] = ''

    gate_line_list = []
    for item in internal_list:
        d = re.findall('\d+', item)
        for i in range(len(d)):
            d[i] = int(d[i])
    ##    print(d)
        gate_line_list.append(d)

    for branch_num in branch_list_ext:
        count = 1
        for item in gate_line_list:
            item_input = item[1:]
            for n in item_input:
                if n == branch_num:
                    f = item.index(n)
                    e = second_column.index(branch_num)
                    item[f] = second_column[e + count]
                    count += 1
    ##print(gate_line_list)
    for item in gate_line_list:
        r = second_column.index(item[0])
        sixth_column[r] = item[1:]


    ##print(first_column)
    ##print(second_column)
    ##print(third_column)
    ##print(fourth_column)
    ##print(fifth_column)
    ##print(sixth_column)

    fv = open('../circuits/'+dst,'w')
    for i in range(number_of_line):
        fv.writelines([str(first_column[i]),' ',str(second_column[i]),' ',str(third_column[i]),' ',\
                    str(fourth_column[i]),' ',str(fifth_column[i]),' '])
        if sixth_column[i] != '':
            for num in sixth_column[i]:
                fv.writelines([str(num),' '])
        fv.writelines(['\n'])
    fv.close()





