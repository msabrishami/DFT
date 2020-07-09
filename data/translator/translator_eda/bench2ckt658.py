# input file type : .bench
# output file type : .ckt658
import re

class Gate:
    def __init__(self, line):
        # for example: 2537 = NAND(2286, 2315, 2361, 2104, 1171)
        self.type = (line.split(" = ")[1]).split("(")[0]
        self.numbers = re.findall('\d+', line)
        for i in range(len(self.numbers)):
            self.numbers[i] = int(self.numbers[i])
        self.output = self.numbers[0]
        self.inputs = self.numbers[1:]
    def write_back(self):
        item = str(self.output) + " = " + self.type + "("
        for input in self.inputs:
            item = item + str(input) + ", "
        item = item.strip(", ")
        item = item + ")"
        return item
    def get_type_number(self):
        if self.type == 'XOR':
            out = 2
        elif self.type == 'NOR':
            out = 4
        elif self.type == 'OR':
            out = 3
        elif self.type == 'NOT':
            out = 5
        elif self.type == 'NAND':
            out = 6
        elif self.type == 'AND':
            out = 7
        return out

def bench2ckt658(ckt):
    fin = open (ckt + '.bench','r')
    f = fin.readlines()
    fin.close()
    f = f[6:]
    count_list = len(f)
    for i in range(count_list):
        f[i] = f[i].strip('\n')
    f.remove('')
    f.remove('')

    # delete all buffers
    buff_exist = 1
    while buff_exist == 1:
        buff_exist = 0
        for line in f:
            if "BUFF" in line:
                buff_exist = 1
                buff = line
                break
        if buff_exist == 1:
            n = re.findall('\d+', buff)
            f.remove(buff)
            for i in range(len(f)):
                if n[0] in re.findall('\d+', f[i]):
                    if f[i][0] == "O":
                        f[i] = f[i].replace(n[0], n[1])
                        continue
                    numbers = re.findall('\d+', f[i])
                    # print(f[i])
                    type = (f[i].split(" = ")[1]).split("(")[0]
                    for index, item in enumerate(numbers):
                        if item == n[0]:
                            numbers[index] = n[1]
                    new_fi = numbers[0] + " = " + type + "("
                    for num in numbers[1:]:
                        new_fi = new_fi + num + ", "
                    new_fi = new_fi.strip(", ")
                    new_fi = new_fi + ")"
                    f[i] = new_fi
        
    # input file lists include 3 lists: PI list, PO list, internal list
    input_list = []
    output_list = []
    internal_list = []
    gate_list = []
    for line in f:
        if line[0] == "I":
            input_list.append(int(re.findall('\d+', line)[0]))
        elif line[0] == "O":
            output_list.append(int(re.findall('\d+', line)[0]))
        else:
            internal_list.append(line)
            gate_list.append(Gate(line))

    net_all = []
    for line in internal_list:
        net_all = net_all + re.findall('\d+', line)
    for i in range(len(net_all)):
        net_all[i] = int(net_all[i])
    max_net = max(net_all)
    net_all.sort(reverse=False)

    # find the number of each net and save into branch_list
    branch_list = [0,0] * len(net_all)
    a = net_all
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
    for input in input_list:
        for i in range(len(branch_list)):
            if input == branch_list[i][0]:
                branch_list[i][1] += 1
    # print("branch_list = " , branch_list)

    branch_dict = dict() # to record new fan-out number for a branch net
    for net_branch in branch_list:
        if net_branch[1] <= 2:
            continue
        else:
            net_name = net_branch[0]
            n_fanout = net_branch[1]
            branch_dict[net_name] = []
            for gate in gate_list:
                if net_name not in gate.inputs:
                    continue
                else:
                    for index, item in enumerate(gate.inputs):
                        if item == net_name:
                            gate.inputs[index] = max_net + 1
                            branch_dict[net_name].append(max_net + 1)
                            max_net += 1
    # for gate in gate_list:
        # print(gate.write_back())
    # for key in branch_dict:
        # print(key, branch_dict[key])

    all_nets = input_list + output_list
    for gate in gate_list:
        all_nets = all_nets + gate.inputs + [gate.output]
    all_nets = set(all_nets)

    n_all_nets = len(all_nets)
    first_column = [-1] * n_all_nets
    second_column = [-1] * n_all_nets
    third_column = [-1] * n_all_nets
    fourth_column = [-1] * n_all_nets
    fifth_column = [-1] * n_all_nets
    sixth_column = [-1] * n_all_nets

    for index, item in enumerate(all_nets):
        second_column[index] = item
    # print(second_column)
    # second_column is taken care of

    for input in input_list:
        in_index = second_column.index(input)
        first_column[in_index] = 1
        third_column[in_index] = 0
    for gate in gate_list:
        g_o_index = second_column.index(gate.output)
        first_column[g_o_index] = 0
        third_column[g_o_index] = gate.get_type_number()
    for output in output_list:
        out_index = second_column.index(output)
        first_column[out_index] = 3
    for key in branch_dict:
        fan_out_list = branch_dict[key]
        for fanout in fan_out_list:
            f_o_index = second_column.index(fanout)
            first_column[f_o_index] = 2
            third_column[f_o_index] = 1
    # first_column and third_column are taken care of

    for input in input_list:
        in_index = second_column.index(input)
        fourth_column[in_index] = 1
    for gate in gate_list:
        g_o_index = second_column.index(gate.output)
        fourth_column[g_o_index] = 1
    for key in branch_dict:
        fan_out_list = branch_dict[key]
        key_index = second_column.index(key)
        fourth_column[key_index] = len(fan_out_list)
        for fanout in fan_out_list:
            f_o_index = second_column.index(fanout)
            fourth_column[f_o_index] = key
    for output in output_list:
        out_index = second_column.index(output)
        fourth_column[out_index] = 0
    # fourth_column is taken care of

    for input in input_list:
        in_index = second_column.index(input)
        fifth_column[in_index] = 0
    for gate in gate_list:
        g_o_index = second_column.index(gate.output)
        fifth_column[g_o_index] = len(gate.inputs)
    for key in branch_dict:
        fan_out_list = branch_dict[key]
        for fanout in fan_out_list:
            f_o_index = second_column.index(fanout)
            fifth_column[f_o_index] = '\t'
    # fifth_column is taken care of

    for gate in gate_list:
        g_o_index = second_column.index(gate.output)
        sixth_column[g_o_index] = gate.inputs
    for input in input_list:
        in_index = second_column.index(input)
        sixth_column[in_index] = ''
    for key in branch_dict:
        fan_out_list = branch_dict[key]
        for fanout in fan_out_list:
            f_o_index = second_column.index(fanout)
            sixth_column[f_o_index] = ''
    # sixth_column is taken care of

    for i in range(n_all_nets):
        if first_column[i] == -1 or second_column[i] == -1 or\
           third_column[i] == -1 or fourth_column[i] == -1 or\
           fifth_column[i] == -1 or sixth_column[i] == -1:
            print("error found : line index " + i + " has -1 value")
    # error checking

    ##print(first_column)
    ##print(second_column)
    ##print(third_column)
    ##print(fourth_column)
    ##print(fifth_column)
    ##print(sixth_column)

    fv = open(ckt + '.ckt658','w')
    for i in range(n_all_nets):
        fv.writelines([str(first_column[i]),'\t',str(second_column[i]),'\t',str(third_column[i]),'\t',\
                       str(fourth_column[i]),'\t',str(fifth_column[i]),'\t'])
        if sixth_column[i] != '':
            for num in sixth_column[i]:
                fv.writelines([str(num),'\t'])
        fv.writelines(['\n'])
    fv.close()





