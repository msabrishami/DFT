# -*- coding: utf-8 -*-

import re
from enum import Enum
from translator import *
from cread import cread
from flr import flr
from classdef import node
from classdef import gtype
from classdef import ntype
from gate import GAND
from gate import GOR
from gate import GXOR
from gate import GNOT
from lev import lev
from logicsim import LogicSim
from dfs import dfs
from pfs import pfs
from faultdict_gen import faultdict_gen
from mini_faultlist_gen import mini_faultlist_gen
from equv_domain import equv_domain
from d_alg import D_alg
from classdef import five_value
from classdef import podem_node_5val
from checker import Checker
from podem import *
#from D_alg import imply_and_check
#__________________________________________________#
#________________main_test for cread_______________#
#__________________________________________________#

input_nodes = []
nodelist_test = cread('../circuits/c17.ckt',input_nodes)
Nnodes = len(nodelist_test)


#__________________________________________________#
#________________main_test for flr_________________#
#__________________________________________________#

#print ('before flr test')
#for i in range(len(nodelist_test)):
#    if nodelist_test[i].cpt == 1:
#        print (nodelist_test[i].num, 'cpt')
#flr(nodelist_test)


# print ('cpt sa0 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt == 1:
#         print (nodelist_test[i].num,'cptSA0',nodelist_test[i].sa0)

# print ('cpt sa1 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt == 1:
#         print (nodelist_test[i].num,'cptSA1',nodelist_test[i].sa1)

# print ('normal sa0 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt != 1:
#         print (nodelist_test[i].num,'SA0',nodelist_test[i].sa0)

# print ('normal sa1 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt != 1:
#         print (nodelist_test[i].num,'SA1',nodelist_test[i].sa1)

#__________________________________________________#
#________________main_test for lev_________________#
#__________________________________________________#
# for i in nodelist_test:
#     if (i.num == 481):
#         for j in i.unodes:
#             print(j.num,end=" ")
#             print(j.fin)
# nodelist_order = lev(nodelist_test, Nnodes)

# for i in nodelist_test:
#   print('{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num))


nodelist_order = lev(nodelist_test, Nnodes)
input_num = [1, 2, 3, 6, 7]
input_val = [0, 0, 0, 0, 0]
pfs_fault_num = [2, 7, 10, 16, 19]
pfs_fault_val = [1, 1, 0, 0, 0]
output = pfs(nodelist_order,input_num,input_val,pfs_fault_num,pfs_fault_val)
print(output)

# for i in nodelist_test:
#   print('{}\t{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num, i.index))
# for i in nodelist_order:
    #   print('{}\t{}\t{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num, i.index, i.fin))

#__________________________________________________#
#_____________main_test for logic_sim______________#
#__________________________________________________#
# lsim = LogicSim(nodelist_order)
# lsim.read_from_file()
# lsim.simulate()
# nodelist_order_simulated = lsim.nodelist_order
# nodelist_order = lev(nodelist_test, Nnodes)
# logic_sim(nodelist_order)
# for i in nodelist_test:
#     print('{}\t{}\t'.format(i.num,i.value))

#__________________________________________________#
#_____________main_test for dfs&pfs________________#
#__________________________________________________#
# nodelist_order = lev(nodelist_test, Nnodes)
# logic_sim(nodelist_order)
# fault_list = dfs(nodelist_order_simulated, Nnodes)
# pfs('../tests/input.txt', nodelist_order,'../tests/full_fault_list.txt')
# print(fault_list)
# for i in nodelist_test:
#     print('{}\t{}\t{}'.format(i.num, i.faultlist_dfs, i.value))


#__________________________________________________#
#__________main_test for faultdict_gen_____________#
#__________________________________________________#
# dict_for_equv = faultdict_gen(input_nodes, nodelist_test)
# pfs('../tests/input.txt', nodelist_test, '../tests/full_fault_list.txt')
# print (dict_for_equv)

#__________________________________________________#
#__________main_test for mini_faultlist_gen________#
#__________________________________________________#
#faultlist_afterflr = flr(nodelist_test)


#print(dict_for_equv_new)
# mini_faultlist_gen()


#__________________________________________________#
#__________main_test for equv and domain___________#
#__________________________________________________#
# dict_for_equv = faultdict_gen(input_nodes, nodelist_test)
# print(dict_for_equv)
#equv = equv_domain()
#print(equv[0]) #print equv
#print(equv[1]) #print domain

#__________________________________________________#
#__________D_algorithm_____________________________#
#__________________________________________________#
# run D algorithm and Podem algorithm, check correctness and return fault coverage
# checker = Checker(nodelist_order, nodelist_test, Nnodes)
# checker.get_full_fault_list()
# failure_fault_list = checker.d_checker()
# checker.read_fault_dict()
# checker.get_d_correctness()
# checker.get_d_coverage()


#__________________________________________________#
#_____________________PODEM________________________#
#__________________________________________________#
# checker.get_pd_correctness()
# checker.get_pd_coverage()
# f_num = 1
# f_val = 1
# p = podem(f_num, f_val, nodelist_test, nodelist_order)

#__________________________________________________#
#____________________translator_test_______________#
#__________________________________________________#
#translator("c6288.bench", "c6288.ckt")