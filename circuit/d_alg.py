import copy
from enum import Enum
from classdef import five_value
import json
import sys
from collections import OrderedDict 
sys.setrecursionlimit(10000)

#Introduction
#For XOR gate, this code is only suitable for two inputs XOR

'''
D     1/0
D_BAR 0/1
five value define
access value:five_value.ZERO.value
access variable:five_value(0).name
class five_value(Enum):
   ZERO = 0
   ONE = 15
   D = 12
   D_BAR = 3
   X = 9
gtype:IPT, BRCH, XOR,OR,NOR,NOT,NAND,AND
ntype:GATE,PI,FB,PO
'''

#Global list
d_frontier_list = [] #Save all the class of D_frontier
d_frontier_list_history = [] #D frontier list history
j_frontier_list = [] #Save all the class of j_frontier
assigned_node_list = [] #save all the node assigned new value when we call d_alg agaiin
circuit_copy_list = [] #Save all the nodelist_order when call new d_alg
imply_avoid_repeat_dict = {} #Avoid same forward implication or backward implication happening repeatedly
five_value_to_bin = {0 : 0, 15: 1, 12: 1, 3: 0, 9 : 'X'}
#Everytime, when it comes to source_num to dest_num implication, we check whether this is the first time occuring
#If this is the first time, we just save it in dict and return 0. Otherwise, return 1
def assign_unrepeated_node_list(node_class):
    if node_class.index not in assigned_node_list:
        assigned_node_list.append(node_class.index)
def avoid_repeat_imply(source_num,dest_num):
    imply_avoid_repeat_list = []
    imply_avoid_repeat_list.append(dest_num)
    #The reason why we use list to save dest_num is that maybe one source responds mult dest_num
    if imply_avoid_repeat_dict.get(source_num) == None:
        imply_avoid_repeat_dict.update({source_num:imply_avoid_repeat_list})
    elif dest_num in imply_avoid_repeat_dict.get(source_num):
        return 1
    else:
        imply_avoid_repeat_dict.get(source_num).append(dest_num)
    return 0
#Convert D to one, D_bar to zero
def backward_convert_faultvalue(temp_value):
    if temp_value== five_value.D.value:
        return five_value.ONE.value
    if temp_value == five_value.D_BAR.value:
        return five_value.ZERO.value

def find_j_frontier(node_class):
    #All the inputs value do implication output
    j_frontier_temp_value = 0
    if node_class.gtype == "AND" or node_class.gtype == "NAND":
        j_frontier_temp_value = five_value.ONE.value
    for j_fontier_fanin in node_class.unodes:
        if node_class.gtype == "AND" or node_class.gtype == "NAND":
            j_frontier_temp_value = j_frontier_temp_value & j_fontier_fanin.d_value[-1]
        if node_class.gtype == "OR" or node_class.gtype == "NOR":
            j_frontier_temp_value = j_frontier_temp_value | j_fontier_fanin.d_value[-1]
    if node_class.gtype == "XOR":
            j_frontier_temp_value = node_class.unodes[0].d_value[-1] ^ node_class.unodes[1].d_value[-1]
    if node_class.gtype == "NAND" or node_class.gtype == "NOR":
        j_frontier_temp_value = 15 - j_frontier_temp_value
    j_frontier_temp_value = convert_other_value_to_x(j_frontier_temp_value)
    #Count inut is 1, 0, d, D_bar
    j_fontier_count_1=0
    j_fontier_count_0=0
    j_fontier_count_d=0
    j_fontier_count_d_bar=0
    j_fontier_count_x = 0
    for j_fontier_fanin in node_class.unodes:
        if j_fontier_fanin.d_value[-1]==five_value.ZERO.value:
            j_fontier_count_0+=1
        elif j_fontier_fanin.d_value[-1]==five_value.ONE.value:
            j_fontier_count_1+=1
        elif j_fontier_fanin.d_value[-1]==five_value.D.value:
            j_fontier_count_d+=1
        elif j_fontier_fanin.d_value[-1]==five_value.D_BAR.value:
            j_fontier_count_d_bar+=1
        elif j_fontier_fanin.d_value[-1]==five_value.X.value:
            j_fontier_count_x+=1
    #If it is xor gate, and all the input are x, it is j_fontier and return 1. Otherwise, it is not j_fontier and return 0
    if node_class.gtype=="XOR":
        if j_fontier_count_0>0 or j_fontier_count_1>0 or j_fontier_count_d>0 or j_fontier_count_d_bar>0:
            return 0
        else:
            return 1
    #For 4 primiary gate, if input logic calculation is not equal output value, it is possible a j_fontier
    if node_class.d_value[-1]!=j_frontier_temp_value:
        #If there is controling value in nand gate and output is D, it is not a j_fontier
        if node_class.gtype=="NAND" and (j_fontier_count_0>0) and node_class.d_value[-1]==five_value.D.value:
            return 0
        #If there is controling value in or gate and output is D, it is not a j_fontier
        elif node_class.gtype=="OR" and (j_fontier_count_1>0) and node_class.d_value[-1]==five_value.D.value:
            return 0
        #If there is controling value in and gate and output is D_BAR, it is not a j_fontier
        elif node_class.gtype=="AND" and (j_fontier_count_0>0) and node_class.d_value[-1]==five_value.D_BAR.value:
            return 0
        ##If there is controling value in nor gate and output is D_BAR, it is not a j_fontier
        elif node_class.gtype=="NOR" and (j_fontier_count_1>0) and node_class.d_value[-1]==five_value.D_BAR.value:
            return 0
        #For nand or or gate, if output is 0, we could use backward implicatoin to get input.So, it is not j_fontier
        if node_class.d_value[-1]==five_value.ZERO.value and (node_class.gtype=="NAND" or node_class.gtype=="OR"):
            return 0
        #For nor or and, if output is 1, we could use backward implicatoin to get input.So, it is not j_fontier
        elif node_class.d_value[-1]==five_value.ONE.value and (node_class.gtype=="NOR" or node_class.gtype=="AND"):
            return 0
        #add new
        elif j_fontier_count_x==1:
            return 0
        #Otherwise, if output is 0 or 1, it is j_fronter
        elif (node_class.d_value[-1]==five_value.ZERO.value or node_class.d_value[-1]==five_value.ONE.value) and j_fontier_count_x>=2:
            return 1
        #add 4.16
        #If this gate is OR or NAND and output is D and there are not any controling value in inputs, it is j_fronter
        elif (node_class.gtype=="OR" or node_class.gtype=="NAND") and node_class.d_value[-1]==five_value.D.value and j_fontier_count_x>=2:
            return 1
        #If this gate is NOR or AND and output is D_BAR and there are not any controling value in inputs, it is j_fronter
        elif (node_class.gtype=="AND" or node_class.gtype=="NOR") and node_class.d_value[-1]==five_value.D_BAR.value and j_fontier_count_x>=2:
            return 1
        else:
            return 0
    return 0
#Since we use five value 0,3,9,12,15, if the value is not one of five value, we convert it to 9
def convert_other_value_to_x(value):
    if value!=0 and value!=15 and value!=12 and value!=3:
        return 9
    else:
        return value
#If this gate is not BRCH or NOT and inputs of value is D or D_BAR. It is d_fontier
def find_d_frontier(node_class):
    if node_class.gtype == "BRCH" or node_class.gtype == "NOT":
        return 0
    else:
        for d_frontier_fanin in node_class.unodes:
            if d_frontier_fanin.d_value[-1] == five_value.D.value or d_frontier_fanin.d_value[-1] == five_value.D_BAR.value:
                return 1
        return 0
#Get controling value for different gate. For OR, NOR, return 1. For and, nand, xor, return 1
def get_control_value(node_class):
    if node_class.gtype == "OR" or node_class.gtype == "NOR":
        return five_value.ONE.value
    elif node_class.gtype == "AND" or node_class.gtype == "NAND" or node_class.gtype == "XOR":
        return five_value.ZERO.value
#Check whether there are any D or D_BAR at output
def error_not_at_PO(nodelist):
    for i in nodelist:
        if i.ntype == "PO":
            if i.d_value[-1] == five_value.D.value or i.d_value[-1] == five_value.D_BAR.value:
                return 0
    return 1
#Imply and check recursive method
def imply_and_check(node_class, imply_counter):
    if node_class.d_value[-1] == five_value.X.value:
        return 1
    #Forward implication
    if node_class.ntype != "PO":
        for fanout in node_class.dnodes:
            #Initial temp_value
            temp_value = node_class.d_value[-1]
            if fanout.gtype == "XOR" or fanout.gtype == "OR" or fanout.gtype == "NOR" or fanout.gtype == "AND" or fanout.gtype == "NAND":
                temp_value = 0
                if fanout.gtype == "AND" or fanout.gtype == "NAND":
                    temp_value = 15
            #Gate logic simulation and asssign result to temp_value
            for forward_fanin in fanout.unodes:
                temp_fin = forward_fanin.d_value[-1]
                if fanout.gtype == "AND" or fanout.gtype == "NAND":
                    temp_value = temp_value & temp_fin
                if fanout.gtype == "OR" or fanout.gtype == "NOR":
                    temp_value = temp_value | temp_fin
                if fanout.gtype == "XOR":
                    temp_value = temp_value ^ temp_fin
            if fanout.gtype == "NAND" or fanout.gtype == "NOR" or fanout.gtype == "NOT":
                temp_value = 15 - temp_value
            temp_value = convert_other_value_to_x(temp_value)
            #If this gate's output value is x
            if fanout.d_value[-1] == five_value.X.value:
                #If  temp_value is also x,  we check whether this gate is d_fontier or not
                if temp_value == five_value.X.value:
                    if find_d_frontier(fanout) == 1:          
                        d_frontier_list.append(fanout)
                    return 1
                #Else if temp_value is not x, we assign temp_value to this gate's output and call imply_and_check
                else:
                    fanout.d_value.append(temp_value)
                    assigned_node_list.append(fanout.index)
                    #assign_unrepeated_node_list(fanout)
                    if avoid_repeat_imply(node_class.num,fanout.num) ==1:
                        return 1
                    if imply_and_check(fanout, imply_counter) == 0:
                        return 0
            #Else if this gate's output is not equal to temp_value. However, if temp_value is 1 or 0, responding output value is D OR D_BAR, we just imply_and_check. Otherwise return 0
            elif temp_value!=fanout.d_value[-1]:
                if temp_value==five_value.ONE.value and fanout.d_value[-1]==five_value.D.value:
                    pass
                elif temp_value==five_value.ZERO.value and fanout.d_value[-1]==five_value.D_BAR.value:
                    pass
                elif temp_value == five_value.X.value:
                    pass
                else:
                    return 0
                if avoid_repeat_imply(node_class.num,fanout.num) ==1:
                    return 1
                if imply_and_check(fanout, imply_counter) == 0:
                    return 0
            #Else just do imply_and_check
            else:
                if avoid_repeat_imply(node_class.num,fanout.num) ==1:
                    return 1
                if imply_and_check(fanout, imply_counter) == 0:
                    return 0
    #Backward implication if this gate is not IPT
    if node_class.gtype != "IPT":
        #If this gate is BRCH, it only has one unode
        if node_class.gtype == "BRCH":
            temp_value = node_class.d_value[-1]
            #If this gate's value is not equal to its unode
            if node_class.unodes[0].d_value[-1] !=temp_value:
                #If its unode's value is x, we just assign this gate's value to its unode and do imply_and_check
                if node_class.unodes[0].d_value[-1] == five_value.X.value:
                    node_class.unodes[0].d_value.append(temp_value)
                    assigned_node_list.append(node_class.unodes[0].index)
                    if temp_value==five_value.D.value or temp_value==five_value.D_BAR.value:
                        node_class.unodes[0].d_value.append(backward_convert_faultvalue(temp_value))
                #Else if this gate's value is D or D_BAR, its unode's value is 1 or o respectively, we also just do imply_and_check
                elif temp_value==five_value.D.value and node_class.unodes[0].d_value[-1]==five_value.ONE.value:
                    pass
                elif temp_value==five_value.D_BAR.value and node_class.unodes[0].d_value[-1]==five_value.ZERO.value:
                    pass
                #Otherwise return 0
                else:
                    return 0
                if avoid_repeat_imply(node_class.num,node_class.unodes[0].num) ==1:
                    return 1
                if imply_and_check(node_class.unodes[0], imply_counter) == 0:
                    return 0
            #If this gate's value is equal to its unode,do imply_and_check
            else:
                if avoid_repeat_imply(node_class.num,node_class.unodes[0].num) ==1:
                    return 1
                if imply_and_check(node_class.unodes[0], imply_counter) == 0:
                    return 0
        #If this gate is NOT, it only has one unode
        elif node_class.gtype == "NOT":
            temp_value = 15 - node_class.d_value[-1]
            #If this gate's value is not equal to 15 - unode's value
            if node_class.unodes[0].d_value[-1] !=temp_value:
                #If its unode's value is x, we assign 15 - this gate's value to its unode and do imply_and_check
                if node_class.unodes[0].d_value[-1] == five_value.X.value:
                    node_class.unodes[0].d_value.append(temp_value)
                    assigned_node_list.append(node_class.unodes[0].index)
                    if temp_value==five_value.D.value or temp_value==five_value.D_BAR.value:
                        node_class.unodes[0].d_value.append(backward_convert_faultvalue(temp_value))
                #If its unode's value is 0 or 1, and this gate's value is D or D_BAR, respectively, we just do imply_and_check
                elif node_class.d_value[-1] == five_value.D.value and node_class.unodes[0].d_value[-1]==five_value.ZERO.value:
                    pass
                elif node_class.d_value[-1] == five_value.D_BAR.value and node_class.unodes[0].d_value[-1]==five_value.ONE.value:
                    pass
                #Else return 0
                else:
                    return 0
                if avoid_repeat_imply(node_class.num,node_class.unodes[0].num) ==1:
                    return 1
                if imply_and_check(node_class.unodes[0], imply_counter) == 0:
                    return 0
            #If this gate's value is equal to 15 - unode's value, just do imply_and_check
            else:
                if avoid_repeat_imply(node_class.num,node_class.unodes[0].num) ==1:
                    return 1
                if imply_and_check(node_class.unodes[0], imply_counter) == 0:
                    return 0
        else:
            #For other gates, we check j_fontier first. If this gate is j_fontier, we return 1. Otherwise, we continue to check
            if find_j_frontier(node_class) ==1:
                j_frontier_list.append(node_class)
                return 1
            # no J Frontier
            #If this gate is NAND
            elif node_class.gtype == "NAND":
                #If this gate's value is 0
                if node_class.d_value[-1] == five_value.ZERO.value:
                    backward_fanin_temp_value = five_value.ONE.value
                    #For all the nodes, if its value is x, we assign 1 to this unode and do imply_and_check. If its value is not x or 1, return 0. Otherwise, just do imply_and_check
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.X.value:
                            backward_fanin.d_value.append(backward_fanin_temp_value)
                            assigned_node_list.append(backward_fanin.index)
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                        elif backward_fanin.d_value[-1]!=backward_fanin_temp_value:
                            return 0
                        else:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                #If this gate's value is 1 and not j_fontier meaning at least there is one unode's values is 0. If there is not any 0 in unode, we return 0. Otherwise just do imply_and_check
                elif node_class.d_value[-1] == five_value.ONE.value:
                    backward_nand_flag = 0
                    backward_nand_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ZERO.value:
                            backward_nand_flag+=1
                        elif  backward_fanin.d_value[-1] == five_value.X.value:
                            backward_nand_x+=1
                    if backward_nand_x==1 and backward_nand_flag==0:
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ZERO.value)
                                assigned_node_list.append(backward_fanin.index)
                    elif backward_nand_flag==0:
                        return 0  
                    for backward_fanin in node_class.unodes:
                        if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                            return 1
                        if imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
                #If this gate's value is D_BAR, we count 1,0,D,D_BAR of every unodes
                elif node_class.d_value[-1] == five_value.D_BAR.value:  
                    backward_fanin_temp_value =backward_convert_faultvalue(node_class.d_value[-1])
                    all_fanin = len(node_class.unodes)
                    nand_find_D = 0
                    nand_find_one = 0
                    nand_find_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1]==five_value.ZERO.value or backward_fanin.d_value[-1]==five_value.D_BAR.value:
                            all_fanin-=1
                        if backward_fanin.d_value[-1]==five_value.D.value:
                            nand_find_D+=1
                        if backward_fanin.d_value[-1]==five_value.X.value:
                            nand_find_x+=1
                        if backward_fanin.d_value[-1]==five_value.ONE.value:
                            nand_find_one+=1
                    #If there are any 0 or D_BAR in unodes, reutrn 0
                    if all_fanin!=len(node_class.unodes):
                        return 0
                    #If x and D exist in unodes at the same time, return 0
                    elif nand_find_x>0 and nand_find_D>0:
                        return 0
                    #If all the unodes' value are x or 0, we assign all the x to 1, and do imply_and_check
                    elif (nand_find_x == len(node_class.unodes)) or ( nand_find_one>0 and nand_find_x>0):
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(15 - backward_fanin_temp_value)
                                assigned_node_list.append(backward_fanin.index)
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                    #Else every unodes do imply_and_check
                    else:
                        for backward_fanin in node_class.unodes:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                #If this gate's value is D, we just do imply_and_check for every unodes
                elif node_class.d_value[-1] == five_value.D.value:  
                    backward_nand_zero = 0
                    backward_nand_x = 0
                    backward_nand_d = 0
                    backward_nand_d_bar = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ZERO.value:
                            backward_nand_zero+=1
                        elif  backward_fanin.d_value[-1] == five_value.X.value:
                            backward_nand_x+=1 
                        elif backward_fanin.d_value[-1] == five_value.D.value:
                            backward_nand_d+=1
                        elif backward_fanin.d_value[-1] == five_value.D_BAR.value:
                            backward_nand_d_bar+=1

                    if  backward_nand_zero>0:
                        pass
                    elif  backward_nand_d>0:
                        return 0
                    elif  backward_nand_x==1:
                        if backward_nand_d_bar>0:
                            return 0
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ZERO.value)
                                assigned_node_list.append(backward_fanin.index)
                    else:
                        pass
                      
                    for backward_fanin in node_class.unodes:
                        if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                            return 1
                        if imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0   
            #If this gate is AND       
            elif node_class.gtype == "AND":
                # when output = 1 for AND, we can imply that every input = 1 as long as they are not previously assigned to other values
                if node_class.d_value[-1] == five_value.ONE.value:
                    backward_fanin_temp_value = five_value.ONE.value
                    for backward_fanin in node_class.unodes:
                        # assign 1 to fan in nodes with value x & do the further imply and check on fan in nodes
                        if backward_fanin.d_value[-1] == five_value.X.value:
                            #backward_fanin.value = backward_fanin_temp_value
                            backward_fanin.d_value.append(backward_fanin_temp_value)
                            assigned_node_list.append(backward_fanin.index)
                            # if implied and check before, avoid repetition of imply and check
                            if avoid_repeat_imply(node_class.num, backward_fanin.num) ==1:
                                return 1
                            # if any fan in nodes fail the imply and check then imply and check fails
                            elif imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                        # if contradiction value exists in fan in nodes, abort, imply and check fails
                        elif backward_fanin.d_value[-1] != backward_fanin_temp_value:
                            return 0
                        # if fan in node is already 1, no value assignment needed, directly do the further imply and check
                        else:
                            if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                                return 1
                            elif imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                # when output = 0 for AND (No J Frontier), there must be at least one ZERO in fan in nodes
                elif node_class.d_value[-1] == five_value.ZERO.value:
                    fanin_zero_cnt = 0
                    fanin_x_cnt = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ZERO.value:
                            fanin_zero_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            fanin_x_cnt += 1
                    # if no zero in fan in nodes, and there is no J Frontier then backward imply and check fails
                    if fanin_x_cnt == 1 and fanin_zero_cnt==0:
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                #backward_fanin.value = five_value.ZERO.value
                                backward_fanin.d_value.append(five_value.ZERO.value)
                                assigned_node_list.append(backward_fanin.index)
                    elif fanin_zero_cnt == 0:
                        return 0
                    for backward_fanin in node_class.unodes:
                        if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                            return 1
                        elif imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
                # when output = D output s@0 for AND (No J Frontier)
                # use the fault free value ONE to do the backward imply and check fan in nodes
                elif node_class.d_value[-1] == five_value.D.value:
                    # convert D into fault free value ONE
                    backward_fanin_temp_value = backward_convert_faultvalue(node_class.d_value[-1])
                    unode_find_D = 0
                    unode_find_X = 0
                    unode_find_ONE = 0
                    for backward_fanin in node_class.unodes:
                        # if no J frontier exists, when output = 1 (note that D_BAR fault free value is ZERO)
                        # if any fan in node = 0, contradiction occurs,
                        # imply and check fails
                        if backward_fanin.d_value[-1] == five_value.ZERO.value or backward_fanin.d_value[-1] == five_value.D_BAR.value:
                            return 0
                        # count D for input nodes
                        elif backward_fanin.d_value[-1] == five_value.D.value:
                            unode_find_D += 1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            unode_find_X += 1
                        elif backward_fanin.d_value[-1] == five_value.ONE.value:
                            unode_find_ONE += 1
                    # D and X cannot coexist in the fan in nodes
                    if unode_find_X != 0 and unode_find_D != 0:
                        return 0
                    # fan in nodes are consisted of 1s and Xs
                    #4.16 double check
                    elif unode_find_X != 0 or unode_find_ONE != 0:
                        for backward_fanin in node_class.unodes:
                            # if fan in node = X, then assign 1 to it
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append( backward_fanin_temp_value)
                                assigned_node_list.append(backward_fanin.index)
                            # if fan in node = 1, directly do the further backward imply and check
                            # if checked before, avoid repetion
                            if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                                return 1
                            elif imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                    # fan in nodes are consisted of 1s and Ds, directly do the further imply and check
                    else:
                        for backward_fanin in node_class.unodes:
                            # avoid check repetition
                            if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                                return 1
                            elif imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                # output = D_BAR, output s @ 1 for AND (No J Frontier)
                # use the fault free value ZERO to do the backward imply and check fan in nodes
                else:
                    fanin_zero_cnt = 0
                    fanin_x_cnt = 0
                    fanin_d_cnt = 0
                    fanin_d_bar_cnt = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ZERO.value:
                            fanin_zero_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            fanin_x_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.D.value:
                            fanin_d_cnt+=1
                        elif backward_fanin.d_value[-1] == five_value.D_BAR.value:
                            fanin_d_bar_cnt+=1
                    if fanin_zero_cnt!=0:
                        pass
                    elif fanin_d_cnt>0:
                        return 0
                    elif fanin_x_cnt==1:
                        if fanin_d_bar_cnt>0:
                            return 0
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ZERO.value)
                                assigned_node_list.append(backward_fanin.index)
                    else:
                        pass
                    for backward_fanin in node_class.unodes:
                        # avoid repetition
                        if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                            return 1
                        elif imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
            #If this gate is OR
            elif node_class.gtype == "OR":
                #If this gate's value is 0
                if node_class.d_value[-1] == five_value.ZERO.value:
                    backward_fanin_temp_value = five_value.ZERO.value
                    for backward_fanin in node_class.unodes:
                        #If its unodes'value is x, we assign 0 to this unode and do imply_and_check
                        if backward_fanin.d_value[-1] == five_value.X.value:
                            backward_fanin.d_value.append(backward_fanin_temp_value)
                            assigned_node_list.append(backward_fanin.index)
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                        #If its unodes' value is not x or 0, we jus return 0
                        elif backward_fanin.d_value[-1]!=backward_fanin_temp_value:
                            return 0
                        #Else just do imply_and_check
                        else:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                #If this gate's value is 1 or D, we just check whether there is any 1 in unodes. If not, we return 0. Else, do imply_and_check for every unodes
                elif node_class.d_value[-1] == five_value.ONE.value:
                    backward_or_flag =0
                    backward_or_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ONE.value:
                            backward_or_flag+=1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            backward_or_x+=1
                    if backward_or_x==1 and backward_or_flag==0:
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ONE.value)
                                assigned_node_list.append(backward_fanin.index)
                    elif backward_or_flag==0:
                        return 0  
                    for backward_fanin in node_class.unodes:
                        if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                            return 1
                        if imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
                #If this gate's value is D_BAR, we count 1,0,D,D_BAR of every unodes
                elif node_class.d_value[-1] == five_value.D_BAR.value:
                    backward_fanin_temp_value =backward_convert_faultvalue(node_class.d_value[-1])
                    or_all_fanin = len(node_class.unodes)
                    or_find_d_bar = 0
                    or_find_zero = 0
                    or_find_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1]==five_value.ONE.value or backward_fanin.d_value[-1]==five_value.D.value:
                            all_fanin-=1
                        if backward_fanin.d_value[-1]==five_value.D_BAR.value:
                            or_find_d_bar+=1
                        if backward_fanin.d_value[-1]==five_value.X.value:
                            or_find_x+=1
                        if backward_fanin.d_value[-1]==five_value.ZERO.value:
                            or_find_zero+=1
                    #If there are any 1 or D in unodes, return 0
                    if or_all_fanin!=len(node_class.unodes):
                        return 0
                    #If there are any x and D_BAR in unodes at the same time, return 0
                    elif or_find_x>0 and or_find_d_bar>0:
                        return 0
                    #If every unodes' value are x or 0, we assign 0 to x the unodes and do imply_and_check
                    elif or_find_x==len(node_class.unodes) or (or_find_x>0 and or_find_zero>0 ):
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(backward_fanin_temp_value)
                                assigned_node_list.append(backward_fanin.index)
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                    #Else, just do imply_and_check
                    else:
                        for backward_fanin in node_class.unodes:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                else:
                    fanin_one_cnt = 0
                    fanin_x_cnt = 0
                    fanin_d_cnt = 0
                    fanin_d_bar_cnt = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ONE.value:
                            fanin_one_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            fanin_x_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.D.value:
                            fanin_d_cnt+=1
                        elif backward_fanin.d_value[-1] == five_value.D_BAR.value:
                            fanin_d_bar_cnt+=1
                    if fanin_one_cnt!=0:
                        pass
                    elif fanin_d_bar_cnt>0:
                        return 0
                    elif fanin_x_cnt==1:
                        if fanin_d_cnt>0:
                            return 0
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ONE.value)
                                assigned_node_list.append(backward_fanin.index)
                    else:
                        pass
                    for backward_fanin in node_class.unodes:
                        # avoid repetition
                        if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                            return 1
                        elif imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0

            #If this gate is NOR
            elif node_class.gtype == "NOR":  
                #If this gate's value is 1
                if node_class.d_value[-1] == five_value.ONE.value:
                    backward_fanin_temp_value = five_value.ZERO.value
                    for backward_fanin in node_class.unodes:
                        #For all the unodoes, if thier values are x, we assign 0 to x and do imply_and_check
                        if backward_fanin.d_value[-1] == five_value.X.value:
                            #backward_fanin.value = backward_fanin_temp_value
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(backward_fanin_temp_value)
                                assigned_node_list.append(backward_fanin.index)
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                        #If all the unodes'value are not x or 0, return 0
                        elif backward_fanin.d_value[-1]!=backward_fanin_temp_value:
                            return 0
                        #Else do imply_and_check for all the unodes
                        else:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                #If this gate's value is 0 or D_BAR,
                elif node_class.d_value[-1]==five_value.ZERO.value:
                    backward_nor_flag =0
                    backward_nor_x = 0
                    #If there are not any 1 in unodes, return 0. Else do imply_and_check
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ONE.value:
                            backward_nor_flag+=1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            backward_nor_x+=1
                    if backward_nor_x == 1 and backward_nor_flag==0:
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ONE.value)
                                assigned_node_list.append(backward_fanin.index)
                    elif backward_nor_flag==0:
                        return 0  
                    for backward_fanin in node_class.unodes:
                        if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                            return 1
                        if imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
                #If this gate's value is D, we count 1,0,D,D_BAR for every unodes
                elif node_class.d_value[-1]==five_value.D.value:
                    backward_fanin_temp_value=five_value.ZERO.value
                    nor_all_fanin = len(node_class.unodes)
                    nor_find_d_bar = 0
                    nor_find_zero = 0
                    nor_find_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1]==five_value.ONE.value or backward_fanin.d_value[-1]==five_value.D.value:
                            nor_all_fanin-=1
                        if backward_fanin.d_value[-1]==five_value.D_BAR.value:
                            nor_find_d_bar+=1
                        if backward_fanin.d_value[-1]==five_value.X.value:
                            nor_find_x+=1
                        if backward_fanin.d_value[-1]==five_value.ZERO.value:
                            nor_find_zero+=1
                    #If there are any 1 or D in unodes, return 0
                    if nor_all_fanin!=len(node_class.unodes):
                        return 0
                    #If there are x and D_BAR in unodes at the same time, return 0
                    elif nor_find_x>0 and nor_find_d_bar>0:
                        return 0
                    #If every unodes are x or 0 we assign 0 to all x and do imply_and_check. If unodes' value is 0, we just do imply_and_check
                    elif nor_find_x==len(node_class.unodes) or (nor_find_x>0 and nor_find_zero>0):
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(backward_fanin_temp_value)
                                assigned_node_list.append(backward_fanin.index)
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                    #Else just do imply_and_check
                    else:
                        for backward_fanin in node_class.unodes:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                else:
                    fanin_one_cnt = 0
                    fanin_x_cnt = 0
                    fanin_d_cnt = 0
                    fanin_d_bar_cnt = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.ONE.value:
                            fanin_one_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.X.value:
                            fanin_x_cnt += 1
                        elif backward_fanin.d_value[-1] == five_value.D.value:
                            fanin_d_cnt+=1
                        elif backward_fanin.d_value[-1] == five_value.D_BAR.value:
                            fanin_d_bar_cnt+=1
                    if fanin_one_cnt!=0:
                        pass
                    elif fanin_d_bar_cnt>0:
                        return 0
                    elif fanin_x_cnt==1:
                        if fanin_d_cnt>0:
                            return 0
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                backward_fanin.d_value.append(five_value.ONE.value)
                                assigned_node_list.append(backward_fanin.index)
                    else:
                        pass
                    for backward_fanin in node_class.unodes:
                        # avoid repetition
                        if avoid_repeat_imply(node_class.num, backward_fanin.num) == 1:
                            return 1
                        elif imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
            #If this gate is XOR
            elif node_class.gtype == "XOR":
                #If this gate's value is 1 or 0, we count 1, 0, D, D_BAR
                if node_class.d_value[-1]==five_value.ONE.value or node_class.d_value[-1]==five_value.ZERO.value:
                    xor_find_1 = 0
                    xor_find_0 = 0
                    xor_find_d = 0
                    xor_find_d_bar = 0
                    xor_find_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1]==five_value.ONE.value:
                            xor_find_1+=1
                        elif backward_fanin.d_value[-1]==five_value.D_BAR.value:
                            xor_find_d_bar+=1
                        elif backward_fanin.d_value[-1]==five_value.D.value:
                            xor_find_d+=1
                        elif backward_fanin.d_value[-1]==five_value.ZERO.value:
                            xor_find_0+=1
                        elif backward_fanin.d_value[-1]==five_value.X.value:
                            xor_find_x+=1
                    #If there are x and (D or D_BAR) in unodes at the same time, return 0
                    #question:maybe less some conditions
                    if xor_find_x>0 and (xor_find_d_bar>0 or xor_find_d>0):
                        return 0
                    #Since this gate is not j_fontier, at least one of its unodes'value is not x. So we can get the value of the other unodes. Then for all unodes, we do imply_and_check
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1] == five_value.X.value:
                            if node_class.unodes[0].d_value[-1]==five_value.X.value:
                                node_class.unodes[0].d_value.append(node_class.unodes[1].d_value[-1] ^ node_class.d_value[-1])
                                assigned_node_list.append(node_class.unodes[0].index)
                            else:
                                node_class.unodes[1].d_value.append(node_class.unodes[0].d_value[-1] ^ node_class.d_value[-1])
                                assigned_node_list.append(node_class.unodes[1].index)
                    for backward_fanin in node_class.unodes:
                        if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                            return 1
                        if imply_and_check(backward_fanin, imply_counter) == 0:
                            return 0
                #If this gate's value is D or D_BAR, we count 1, 0, D, D_BAR
                elif node_class.d_value[-1]==five_value.D.value or node_class.d_value[-1]==five_value.D_BAR.value:
                    backward_fanin_temp_value = backward_convert_faultvalue(node_class.d_value[-1])
                    xor_find_1 = 0
                    xor_find_0 = 0
                    xor_find_d = 0
                    xor_find_d_bar = 0
                    xor_find_x = 0
                    for backward_fanin in node_class.unodes:
                        if backward_fanin.d_value[-1]==five_value.ONE.value:
                            xor_find_1+=1
                        elif backward_fanin.d_value[-1]==five_value.D_BAR.value:
                            xor_find_d_bar+=1
                        elif backward_fanin.d_value[-1]==five_value.D.value:
                            xor_find_d+=1
                        elif backward_fanin.d_value[-1]==five_value.ZERO.value:
                            xor_find_0+=1
                        elif backward_fanin.d_value[-1]==five_value.X.value:
                            xor_find_x+=1
                    #Since this gate is not j_fontier, at least one of its unodes'value is not x. So we can get the value of the other unodes. Then for all unodes, we do imply_and_check
                    if xor_find_x>0 and (xor_find_0>0 or xor_find_1>0):
                        for backward_fanin in node_class.unodes:
                            if backward_fanin.d_value[-1] == five_value.X.value:
                                if node_class.unodes[0].d_value[-1]==five_value.X.value:
                                    node_class.unodes[0].d_value.append(node_class.unodes[1].d_value[-1] ^ backward_fanin_temp_value)
                                    assigned_node_list.append(node_class.unodes[0].index)
                                else:
                                    node_class.unodes[1].d_value.append(node_class.unodes[0].d_value[-1] ^ backward_fanin_temp_value)
                                    assigned_node_list.append(node_class.unodes[1].index)
                        for backward_fanin in node_class.unodes:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
                    #If there are x and (D or D_BAR) in unodes at the same time, return 0
                    elif xor_find_x>0 and (xor_find_d_bar>0 or xor_find_d>0):
                        return 0
                    #question:need to consider
                    elif xor_find_d_bar>0 and xor_find_d>0:
                        return 0
                    else:
                        for backward_fanin in node_class.unodes:
                            if avoid_repeat_imply(node_class.num,backward_fanin.num) ==1:
                                return 1
                            if imply_and_check(backward_fanin, imply_counter) == 0:
                                return 0
    return 1

class DResult:
    def __init__(self, result = 0, pattern = []):
        self.result = result
        self.pattern = []



def D_alg(nodelist_test,fault_index, imply_counter):
    #Clear d_frontier, j_fronter and imply_avoid_repeat_dict when call new d_alg
    imply_counter.increment()
    if imply_counter.cnt > imply_counter.abort_cnt:
        return DResult(0)
    imply_avoid_repeat_dict.clear()
    d_frontier_list.clear()
    j_frontier_list.clear()
    assigned_node_list.clear()
    temp_d_frontier_list = []
    fault_index = fault_index

    #imply_and_check
    if imply_and_check(nodelist_test[fault_index], imply_counter) == 0 :
        for i in assigned_node_list:
            nodelist_test[i].d_value.pop()
        return DResult(0)
    circuit_copy_list.append(assigned_node_list)
    #Check error at output or not
    if error_not_at_PO(nodelist_test) == 1:
        #Append d_frontier_list to d_frontier_list_history
        if d_frontier_list != []:
            for i in d_frontier_list:
                temp_d_frontier_list.append(i)
            d_frontier_list_history.append(temp_d_frontier_list)
        else:
            return DResult(0)
        while 1:
            if imply_counter.cnt > imply_counter.abort_cnt:
                return DResult(0)
            #If all the element in the d_fontier has been tried, pop this d_fontier and return 0
            if len(d_frontier_list_history[-1]) ==0:
                d_frontier_list_history.pop()
                circuit_copy_list.pop()
                return DResult(0)
            original_selected_d_fontier = copy.deepcopy(d_frontier_list_history[-1][-1])
            #Try an element from d_fontier and choose controling value of this gate
            selected_gate = d_frontier_list_history[-1][-1]
            control_value = get_control_value(selected_gate)
            d_fontier_check_x = 0
            #Before assigning uncontroling value for all unodes'value is x, we need to check whether any unodes'value are x
            for fin in selected_gate.unodes:
                if fin.d_value[-1] == five_value.X.value:  
                    d_fontier_check_x+=1
            #If all the unodes'value are not x, this gate is not d_fontier. we pop it and try others
            if d_fontier_check_x==0 or find_d_frontier(selected_gate)==0:
                d_frontier_list_history[-1].pop()
            #If this gate is a real d_fontier
            else:
                #Assign uncontroling value to x in unodes and call d_alg again
                for fin in selected_gate.unodes:
                    if fin.d_value[-1] == five_value.X.value:  
                        #fin.value = 15 - control_value
                        fin.d_value.append(15 - control_value)
                #If d_alg success, return 1
                p_res = D_alg(nodelist_test,fault_index, imply_counter)
                if p_res.result == 1:
                    return p_res
                #If d_fontier is empty, return 0. Else try other gates
                else:                 
                    if len(d_frontier_list_history) == 0:
                        return DResult(0)
                    if len(d_frontier_list_history[-1]) == 0:
                        d_frontier_list_history.pop()
                        circuit_copy_list.pop()
                        return DResult(0)
                    nodelist_test[original_selected_d_fontier.index].d_value[-1]=original_selected_d_fontier.d_value[-1]

                    for d_fontier_input in original_selected_d_fontier.unodes:
                        nodelist_test[d_fontier_input.index].d_value[-1] = d_fontier_input.d_value[-1]
                    d_frontier_list_history[-1].pop()
    #add 4.17 check real j_fontier
    for froniter in range(len(j_frontier_list)):
        if find_j_frontier(j_frontier_list[froniter]) ==0:
            p_res = D_alg(nodelist_test,fault_index, imply_counter)
            return p_res
    # If j_fronter is empty, success and write input pattern into json file
    if len(j_frontier_list) == 0:
        pattern = []
        pattern_node = []
        for i in nodelist_test:
            if i.gtype == "IPT":
                pattern_node.append(i)
        pattern_node.sort(key = lambda x:x.num)
        for node in pattern_node:
            pattern.append(five_value_to_bin[node.d_value[-1]])
        return DResult(1, pattern)
    #Else try a j_fontier
    selected_gate = j_frontier_list[-1]
    control_value = get_control_value(selected_gate)
    if selected_gate.gtype == "XOR":
        selected_gate.unodes[0].d_value.append(control_value)
        p_res = D_alg(nodelist_test,fault_index, imply_counter)
        if p_res.result == 1:
                return p_res
        else:
            selected_gate.unodes[0].d_value[-1] = 15 - control_value
            p_res = D_alg(nodelist_test,fault_index, imply_counter)
            if p_res.result == 1:
                return p_res
    else:
        for i in selected_gate.unodes:
            if i.d_value[-1] == five_value.X.value:
                i.d_value.append(control_value)
                p_res = D_alg(nodelist_test,fault_index, imply_counter)
                if p_res.result == 1:
                    return p_res
                else:
                    i.d_value.pop()
                    i.d_value.append(15 - control_value)
    return DResult(0)
    
