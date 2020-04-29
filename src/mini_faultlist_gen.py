# -*- coding: utf-8 -*-
import re
import argparse
import numpy as np
from enum import Enum
from classdef import node
from classdef import gtype
from classdef import ntype
import sys
import math


#explaintation
#This code is used to generate minimum fault list. 
#Fist step: Read from FLR_Results.txt to get a list called faultlist_afterflr and read from fault_dict.txt to get a dictionary called dict_for_equv
#Second step: Build a dictionary called mini_faultlist. This is used to add a valid bit for all the faults from faultlist_afterflr
#Assume that in faultlist_afterflr, we have N faults and for every fault, there are T numbers of input pattern that could test this fault.
#Third step: We need to check whether any two of faults are equvalence and dominance. So, totally,we need O(N**2) for loop all the faults. 
#Fouth step: For every two fault, we first detemine which fault has less responding input patterns that could test it. And we check whether all the input patterns from this fault that also belongs to the other fault. If it is true, which means there is an equvalence or dominance between two faults.
#Fifth step: When we find there is an equvalence or dominance between two faults. We will erase valid bit for dominating fault.
#Final step: we form new fault list according to mini_faultlist
#Big O complexity analyse: For Traversal all the possibilities of every two fault, we need O(N**2). And for every two faults, we need O(T) to check equvalence and dominance. So, the total complexity is O(N**2T)



def mini_faultlist_gen():
	#faultlist_afterflr is a faultlist after rfl
	faultlist_afterflr = []
	file = open("../tests/FLR_Results.txt","r")
	while 1:
		fault = file.readline()
		if fault == "":
			break
		else:
			faultlist_afterflr.append(fault.strip("\n"))
	file.close()
	#dict_for_equv is a map, index is every fault after rfl, value is all the input patterns that could test this fault
	dict_for_equv = {}
	for i in faultlist_afterflr:
		dict_for_equv.update({i:[]})
	file = open("../tests/fault_dict.txt","r")
	for i in file.readlines()[2:]:
		input_pattern = i.split()[0]
		for j in i.split()[1:]:
			if dict_for_equv.get(j) != None:
				dict_for_equv.get(j).append(input_pattern)
	file.close()
	#mini_faultlist is a map used to set valid_bit for all the fault. Initial, all the valid_bit is 1. if one fault dominances other faults, valid_bit is turned to 0 
	mini_faultlist = {}
	for i in range (len(faultlist_afterflr)):
		mini_faultlist.update( {faultlist_afterflr[i]:1})
	for i in range(len(faultlist_afterflr)-1): #choose one fault 
		if mini_faultlist.get(faultlist_afterflr[i]) == 0: #if we find this fault has domainced other fault, we could skip it
			continue
		for j in range(i+1,(len(faultlist_afterflr))): #choose other fault
			if mini_faultlist.get(faultlist_afterflr[j]) == 0: #if we find this fault has domainced other fault, we could skip it
				continue
			flag =0; #flag is used to determine whether two faults have equvalence and domaince 
			if len(dict_for_equv.get(faultlist_afterflr[i]))>len(dict_for_equv.get(faultlist_afterflr[j])): #compare the number of input patterns
				compared_fault_map = {}
				for k in dict_for_equv.get(faultlist_afterflr[i]):
					compared_fault_map.update({k:1})
				for k in dict_for_equv.get(faultlist_afterflr[j]): 	
					if compared_fault_map.get(k) == None:
						flag =1
						break
				if flag == 0:
					mini_faultlist[faultlist_afterflr[i]] = 0
			else:
				compared_fault_map = {}
				for k in dict_for_equv.get(faultlist_afterflr[j]):
					compared_fault_map.update({k:1})
				for k in dict_for_equv.get(faultlist_afterflr[i]): 	
					if compared_fault_map.get(k) == None:
						flag =1
						break
				if flag == 0:
					mini_faultlist[faultlist_afterflr[j]] = 0
	#write result to txt
	mini_faultlist_file = open("mini_faultlist.txt","w")
	for i in range(len(mini_faultlist)):
		if mini_faultlist.get(faultlist_afterflr[i]) == 1:
			mini_faultlist_file.write(faultlist_afterflr[i]+'\n')
	mini_faultlist_file.close()
	#write reduce fault
	reduce_faultlist_file = open("reduce_faultlist_file.txt","w")
	for i in range(len(mini_faultlist)):
		if mini_faultlist.get(faultlist_afterflr[i]) == 0:
			reduce_faultlist_file.write(faultlist_afterflr[i]+'\n')
	reduce_faultlist_file.close()

	