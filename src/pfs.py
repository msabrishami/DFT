import re
import argparse
import numpy as np
from enum import Enum
from classdef import node
from classdef import gtype
from classdef import ntype
import sys
import math

# gatenodes class of node
# need to define  gatenodes.sa0, gatenodes.sa1
def pfs(gatenodes,input_num,input_val,pfs_fault_num,pfs_fault_val):
	faultnum = len(pfs_fault_num)
	n = sys.maxsize
	bitlen = int(math.log2(n))+1
	output_num = list()
	for i in gatenodes:
		if i.ntype == 'PO':
			output_num.append(i.num)
	node_num = list()
	node_val = list()
	node_num = input_num
	node_val = input_val
	# hash map
	node_input_dict	= dict(zip(node_num, node_val))
	
	# hash map: node_num is key, object of node is value
	node_all_num = list()
	for i in gatenodes:
		node_all_num.append(i.num)
	node_dict = dict(zip(node_all_num,gatenodes))
	for i in range(len(node_all_num)):
		node_dict[node_all_num[i]].parallel_value = 0
	# cal iter 
	if faultnum % (bitlen-1)==0:
		iter = int (faultnum / (bitlen - 1))
	else:
		iter = int (faultnum / (bitlen - 1))+1
	# write result
	detected_node =[]
	detected_node_value=[]
	output_empty=0
	while (iter != 0):
		fault_num = list()
		fault_val = list()
		for i in gatenodes:
			i.sa0 = 0
			i.sa1 = 0
		read_fault_ind = 0	
		# save bitlen -1 fault
		while(1):	
			content1 = len(pfs_fault_num)
			if content1==0:
				break
			fault_num.append(pfs_fault_num.pop())
			fault_val.append(pfs_fault_val.pop())
			read_fault_ind = read_fault_ind + 1
			if read_fault_ind == bitlen - 1:
				break
		for i in range (len(fault_num)):
			if fault_val[i]==1:
				node_dict[fault_num[i]].sa1 = node_dict[fault_num[i]].sa1 + 2**(i+1)
			else:
				node_dict[fault_num[i]].sa0 = node_dict[fault_num[i]].sa0 + 2**(i+1)

		for i in gatenodes:
			if i.gtype == 'IPT':
				if i.num in node_num:
					i.parallel_value = 0
					for j in range (bitlen):
						i.parallel_value = i.parallel_value + (int(node_input_dict[i.num])<<j)
					i.parallel_value = ((~i.sa0)&i.parallel_value) | i.sa1
			elif i.gtype == 'BRCH':
				i.parallel_value = ((~i.sa0)&(i.unodes[0].parallel_value)) | i.sa1

			elif i.gtype == 'XOR':
				for j in range(0, i.fin):
					if j == 0:
						temp_value = i.unodes[j].parallel_value
					else:
						temp_value = temp_value ^ i.unodes[j].parallel_value
				i.parallel_value = ((~i.sa0)&temp_value) | i.sa1
			elif i.gtype == 'OR':
				for j in range(0, i.fin):
					if j == 0:
						temp_value = i.unodes[j].parallel_value
					else:
						temp_value = temp_value | i.unodes[j].parallel_value
				i.parallel_value = ((~i.sa0)&temp_value) | i.sa1
			elif i.gtype == 'NOR':
				for j in range(0, i.fin):
					if j == 0:
						temp_value = i.unodes[j].parallel_value
					else:
						temp_value = temp_value | i.unodes[j].parallel_value
				i.parallel_value = ((~i.sa0)&(~temp_value)) | i.sa1
			elif i.gtype == 'NOT':
				i.parallel_value = ((~i.sa0)&(~i.unodes[0].parallel_value)) | i.sa1
			elif i.gtype == 'NAND':
				for j in range(0, i.fin):
					if j == 0:
						temp_value = i.unodes[j].parallel_value
					else:
						temp_value = temp_value & i.unodes[j].parallel_value
				i.parallel_value = ((~i.sa0)&(~temp_value)) | i.sa1
			elif i.gtype == 'AND':
				for j in range(0, i.fin):
					if j == 0:
						temp_value = i.unodes[j].parallel_value
					else:
						temp_value = temp_value & i.unodes[j].parallel_value
				i.parallel_value = ((~i.sa0)&temp_value) | i.sa1
		iter -= 1	
	
		for i in range (read_fault_ind):
			for j in output_num:
				temp = node_dict[j].parallel_value
				#t0 is to choose the value responding to the specific fault node in output
				#t1 is to move the value to most significant bit
				t0 = (temp & (1 << (i+1)))
				t1 = t0 << (bitlen-i-2)
				t2 = 1<<(bitlen-1)
				t3 = t1 & t2
				#t4 is to calculate most least bit which is fault free bit
				t4 = (temp & 1) << (bitlen-1)
				if  t3 != t4 :
					if fault_num[i] not in detected_node :
						detected_node.append(fault_num[i])
						detected_node_value.append(fault_val[i])
				 		#print(j,fault_num[i],fault_val[i])
		#output is a set of tuple
		if output_empty==0:
			output={(detected_node[0],detected_node_value[0])}
			output_empty+=1
		for i in range(len(detected_node)):
			output.add((detected_node[i],detected_node_value[i]))
	return output


