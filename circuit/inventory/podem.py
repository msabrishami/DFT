from classdef import five_value
from classdef import podem_node_5val
from classdef import Node
from classdef import gtype
from classdef import ntype
from lev import lev

count = 0
error_at_PO = 0
control = (0,0,0,1,1,0,0,0)
inversion = (0,0,0,0,1,1,1,0)
# class defination for return pattern
class PResult:
    def __init__(self, result = 0, pattern = []):
        self.result = result
        self.pattern = pattern


#------------------------main part for podem------------------------#
# create elements needed, call pd and return the PResult
def podem(f_num, f_val, nodelist_test, nodelist_order):
    global count
    global error_at_PO 
    count = 0
    error_at_PO = 0
    # parameters that needed
    d_frontie = []#d_f saves index
    circuit_value = []
    pattern = []

    #call lev function to generate nodelist_order 
    # nodelist_order = lev(nodelist_test, Nnodes)

    # change node num to node index as most of the algorithm use index
    for i in nodelist_test:
        if(i.num == f_num):
            f_idx = i.index
            break
    # print which node and what kind of faults
    # if (f_val == 1):
    #     print(nodelist_test[f_idx].num, 'SA1')
    # elif (f_val == 0):
    #     print(nodelist_test[f_idx].num, 'SA0')

    # give initial value to circuit value
    for i in range (len(nodelist_test)):
        circuit_value.append(podem_node_5val())
    # call pd to generate input pattern
    if (pd (d_frontie, circuit_value,f_idx,f_val,nodelist_test,nodelist_order) == 0):
        #print ("podem fail")
        return(PResult(0))
    else:
        #print("sucess")

        for i in nodelist_test:
            pattern_node = []
            if (i.gtype == 'IPT'):
                pattern_node.append(i)
                pattern_node.sort(key = lambda x:x.num)
            for node in pattern_node:
                if (circuit_value[node.index].x == 1):
                    #print(i.num, 'x')
                    # 9 because 9 stands for 'X'
                    pattern.append('X')  
                else:
                    if (int(circuit_value[i.index].bit1) == 1):
                        if (int(circuit_value[i.index].bit1) == 1):
                            #print(i.num, '1')
                            pattern.append(1)
                        elif (int(circuit_value[i.index].bit0) == 0):
                            #print(i.num, 'D')
                            pattern.append(1)
                            # attention: you might want to change this 12 to 0, D represents the correct value is 1
                            # but now the value is 0, since it's input, I'm not sure to return a 12 or a 0
                    elif (int(circuit_value[i.index].bit1) == 0):
                        if (int(circuit_value[i.index].bit0) == 0):
                            #print(i.num, '0')
                            pattern.append(0)
                        elif (int(circuit_value[i.index].bit0) == 1):
                            #print(i.num, 'D_bar')
                            pattern.append(0)
                            # attention: you might want to change this 3 to 0, D_bar represents the correct value is 0
                            # but now the value is 1, since it's input, I'm not sure to return a 3 or a 0
        return(PResult(1,pattern))
#---------------------------------pd--------------------------------#
# main part of podem, call implt, objective
def pd (d_frontie, circuit_value,f_idx,f_val,nodelist_test,nodelist_order):
    global count
    #print(d_frontie)
    if (count > 1000):
        return 0
    else:
        count = count + 1
    if (error_at_PO == 1):
        return 1
    if ((circuit_value[f_idx].x == 0) & (len(d_frontie) == 0)):
        return 0
    guess = backtrace(obejective(d_frontie, circuit_value,f_idx,f_val,nodelist_test), circuit_value,nodelist_test)
    guesscpy = []
    guesscpy.append(guess[0])
    guesscpy.append(guess[1])
    imply(guesscpy, d_frontie, circuit_value,nodelist_order,f_idx,f_val)
    if (pd(d_frontie, circuit_value,f_idx,f_val,nodelist_test,nodelist_order) == 1): 
        return 1
    guesscpy[1] = not guesscpy[1]
    imply(guesscpy, d_frontie, circuit_value,nodelist_order,f_idx,f_val)
    if (pd(d_frontie, circuit_value,f_idx,f_val,nodelist_test,nodelist_order) == 1):
        return 1
    imply(guesscpy,d_frontie,circuit_value,nodelist_order,f_idx,f_val,1)
    return 0

#-------------------------------imply-------------------------------#
# imply: generate all value for every node base on current input patterns
def imply(assign, d_f, p_value, nodelist_order,f_idx,f_val, x=0):
    global error_at_PO
    d_f.clear()
    p_value[assign[0]].x = x
    p_value[assign[0]].bit0 = assign[1]
    p_value[assign[0]].bit1 = assign[1]

    for i in nodelist_order:
    # nodelist_order is the output of lev()
        if (i.gtype == 'BRCH'):

            p_value[i.index].bit0 = p_value[i.unodes[0].index].bit0
            p_value[i.index].bit1 = p_value[i.unodes[0].index].bit1
            p_value[i.index].x = p_value[i.unodes[0].index].x
        elif (i.gtype == 'XOR'):

            p_value[i.index] = p_value[i.unodes[0].index] ^ p_value[i.unodes[1].index]
            if (p_value[i.index].x == 1):
                for k in i.unodes:
                    if (p_value[k.index].is_d()):
                        d_f.append(i.index)
                        break
        elif (i.gtype == 'OR'):

            value = p_value[i.unodes[0].index]
            for k in range(1,i.fin):
                value = value | p_value[i.unodes[k].index]
            p_value[i.index] = value
            if (value.x == 1):
                for k in i.unodes:
                    if (p_value[k.index].is_d()):
                        d_f.append(i.index)
                        break
        elif (i.gtype == 'NOR'):

            value = p_value[i.unodes[0].index]
            for k in range(1,i.fin):
                value = value | p_value[i.unodes[k].index]
            p_value[i.index] =  ~ value
            if (value.x == 1):
                for k in i.unodes:
                    if (p_value[k.index].is_d()):
                        d_f.append(i.index)
                        break
        elif (i.gtype == 'NOT'):

            p_value[i.index] = ~ p_value[i.unodes[0].index]
        elif (i.gtype == 'NAND'):
            value = p_value[i.unodes[0].index]
            for k in range(1,i.fin):
                value = value & p_value[i.unodes[k].index]
            p_value[i.index] = ~ value
            if (value.x == 1):
                for k in i.unodes:
                    if (p_value[k.index].is_d()):
                        d_f.append(i.index)
                        break
        elif (i.gtype == 'AND'):
            value = p_value[i.unodes[0].index]
            for k in range(1,i.fin):
                value = value & p_value[i.unodes[k].index]
            p_value[i.index] = value

            if (value.x == 1):
                for k in i.unodes:
                    if (p_value[k.index].is_d()):
                        d_f.append(i.index)
                        break
        if (i.index == f_idx):
            if (p_value[i.index].bit1 != f_val):
                p_value[i.index].fault_node(f_val)
        if ((i.fout == 0) & (p_value[i.index].is_d())):
            error_at_PO = 1
    # for i in nodelist_order:
        # print(i.num, p_value[i.index].x, p_value[i.index].bit1, p_value[i.index].bit0)

#-------------------------------objective-------------------------------#
def obejective(d_frontie, circuit_value,f_idx,f_val,nodelist_test):
    # for i in range(len(nodelist_test)): 
    #     print(circuit_value[i].bit1)
    #print(d_frontie)
    # print("%d fnode x " % circuit_value[f_idx].x)
    # print("objective")
    if (circuit_value[f_idx].x == 1):
        pair = (f_idx, not f_val)
        # print (pair)
        # print ("found")
        # print('objective,fault_node',pair)
        return pair
    alter_node_index = d_frontie[len(d_frontie)-1]
    # print (nodelist_test[alter_node_index].num)
    # print (nodelist_test[alter_node_index].gtype)

    for i in (nodelist_test[alter_node_index].unodes):
        if (circuit_value[i.index].x == 1):
            pair = (i.index, not control[gtype[nodelist_test[alter_node_index].gtype].value])
            break
    # print('objective,d_frontie',pair)
    # print("alter")
    return pair

#-------------------------------backtrace-------------------------------#
def backtrace(start, circuit_value,nodelist_test):
    #print(nodelist_test[start[0]].gtype)
    # print("backtrace")
    # print(nodelist_test[start[0]].num)
    # print(start[1])
    #print("-------------")
    startcpy = []
    startcpy.append(start[0])
    startcpy.append(start[1])
    #print(startcpy)
    while (nodelist_test[startcpy[0]].gtype != 'IPT'):
        i = inversion[gtype[nodelist_test[startcpy[0]].gtype].value]
        # print(nodelist_test[startcpy[0]].num)
        # print(i)
        # print("test")
        for j in (nodelist_test[startcpy[0]].unodes):
            if (circuit_value[j.index].x == 1):
                #print(nodelist_test[j.index].num)
                #print("num")
                startcpy[0] = j.index
                break
        startcpy[1] = startcpy[1] ^ i
        #print(nodelist_test[startcpy[0]].num)
        #print(startcpy[1])
    pair = (startcpy[0], startcpy[1])
    # print("%d->%d" %(nodelist_test[pair[0]].num, pair[1]))
    # print("backtrace")
    return pair
