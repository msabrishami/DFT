# -*- coding: utf-8 -*-

import re
from classdef import node
from classdef import gtype
from classdef import ntype


#__________________________________________________#
#_____________________Read_CKT_____________________#
#__________________________________________________#
def cread(c_name, input_nodes):
    f = open(c_name,'r')
    indx = 0
    nodelist = []
    nodedict = {}
    fileList = []
    nodedict_list = [None] * 1355
    fileList_sorted = []
    temp_dict = {}
    lines = f.readlines()
    
    for line in lines:
        if (line != "\n"):
            fileList.append(line.split())
    for i in fileList:
        i[1] = int(i[1])
    #fileList_sorted = sorted(fileList, key = lambda x:x[1])
    # print (fileList_sorted)
    #cnt = 0
    for line in fileList:
        #print (cnt)
        #line = line.split()
        #print (line)
        new_node = node()
        new_node.ntype = ntype(int(line[0])).name
        new_node.num = int(line[1])
        new_node.gtype = gtype(int(line[2])).name
        
        if (ntype(int(line[0])).value == 2):   #if BRCH --> unodes
            # if (nodedict_list[int(line[3])] == None):
            #     new_node_temp = node()
            #     new_node_temp.num = int(line[3])
            #     nodedict.update({new_node_temp.num: new_node_temp})
            #     nodedict_list[new_node_temp.num] = new_node_temp
            #     new_node.add_unodes(nodedict_list[int(line[3])])
            # else:
            new_node.add_unodes(nodedict_list[int(line[3])])
            new_node.fout = 1 
        else:                                       #if not BRCH --> fout
            new_node.fout = int(line[3])

        if (ntype(int(line[0])).value != 2):
            new_node.fin = int(line[4])
            for i in range (int(line[4])):
                if (nodedict_list[int(line[5 + i])] == None):
                    new_node_temp = node()
                    new_node_temp.num = int(line[5 + i])
                    nodedict.update({new_node_temp.num: new_node_temp})
                    nodedict_list[new_node_temp.num] = new_node_temp
                    new_node.add_unodes(nodedict_list[int(line[5 + i])])
                    temp_dict.update({int(line[5 + i]): new_node.num})
                else:
                    new_node.add_unodes(nodedict_list[int(line[5 + i])])
        else:
            new_node.fin = 1
        
        if ((ntype(int(line[0])).value == 1) or (ntype(int(line[0])).value == 2)):
            new_node.cpt = 1
        
        new_node.index = indx
        indx = indx + 1
        nodelist.append(new_node)
        if (temp_dict.get(new_node.num) != None):
            #print(temp_dict.get(new_node.num))
            for i in nodelist:
                if (i.num == temp_dict.get(new_node.num)):
                    for j in i.unodes:
                        if (j.num == new_node.num):
                            i.unodes.remove(j)
                            i.unodes.append(new_node)         
        nodedict_list[new_node.num] = new_node
        nodedict.update({new_node.num: new_node})
        #TODO:feedback only to one gate
        #cnt = cnt+1
    # print(temp_dict)
    f.close()
    #print ("here")
    for i in range(len(nodelist)):
        #print (nodelist[i].ntype)
        if (nodelist[i].ntype != 'PI'):
            #print(nodelist[i].fin)
            for j in range (nodelist[i].fin):
                nodelist[i].unodes[j].add_dnodes(nodelist[i])
                #print (j)
        else:
            input_nodes.append(nodelist[i].num)
    # print (nodedict.get(723).fin)
    # print ("above in cread")
    return nodelist
