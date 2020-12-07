
import functools
import operator
from node import *
from random import randint
import random

class Podem:
	def __init__(self, circuit, node_num, s_a_v, count_set):
		'''
		set s_a_v on the target node in specific circuit
		'''
		self.circuit = circuit
		self.d_frontier = []
		self.s_a_v = s_a_v*15
		self.check_s_a_v = 9 #check if target value matches s_a_v
		'''
		if node_num not in self.circuit.nodes.keys():
			raise NameError('The node_num is not exist in the circuit')
		else:
			self.target_num = node_num
		'''
		self.target_num = node_num #test
		if self.s_a_v != 15 and self.s_a_v != 0:
			raise NameError('s_a_v should be 1 or 0')
		self.target_node = circuit.nodes.get(node_num)
		self.d_frontier.append(self.target_node)

		#test
		self.count = 0
		self.count_set = count_set

	def test(self):
		for node in self.circuit.nodes_lev:
			node.f_value = 9
			node.trace_count = 0
		return self.podem_recursive()


	def podem_recursive(self):
		#wrapper of Podem
		'''
		check 
		1. if target value matches s_a_v 
		2. output appears at the OPT
		3. d_frontier is empty
		recursively call podem function
		'''
		if self.count > self.count_set:
			return False
		self.count += 1

		if self.s_a_v == self.check_s_a_v == 0 or self.s_a_v == self.check_s_a_v == 15:
			return False

		if self.target_node.ntype != 'PO':
			for output in self.circuit.PO:
				if (output.f_value in [3, 12]) and (self.s_a_v == self.check_s_a_v ^ 15):
					return True
		else:
			if (self.s_a_v == self.check_s_a_v ^ 15):
				return True
				
		if len(self.d_frontier) == 0:
			return False
		
		k, vk = self.objective()
		j, vj = self.backtrace(k, vk)
		self.implication(j, vj)

		if self.podem_recursive() == True:
			return True
		
		self.implication(j, vj ^ 15)
		if self.podem_recursive() == True:
			return True

		self.implication(j, 9)
		return False

	def objective(self):
		#select the object from d_frontier and return backtrace target and value
		'''
		select the target at the first time
		select from d_frontier after the first time
		'''
		if self.target_node.f_value == 9:
			self.d_frontier.pop(0)
			if self.s_a_v == 0:
				self.target_node.f_value = 12			
			elif self.s_a_v == 15:
				self.target_node.f_value = 3
			if self.target_node.gtype == 'IPT':
				return (self.target_node, self.target_node.f_value)
			else:
				return (self.target_node, self.s_a_v ^ 15)
		else:
			if self.d_frontier[0] == self.target_node:
				gate_d = self.d_frontier.pop(0)
			else:
				gate_d = sorted(self.d_frontier, key = lambda x: x.CO)[0]

			if gate_d.gtype in ['NAND', 'AND']:
				for gate_in in sorted(gate_d.unodes, key = lambda x : x.CC1):
					if gate_in.f_value == 9:
						return (gate_in, 15)
			else:
				for gate_in in sorted(gate_d.unodes, key = lambda x : x.CC0):
					if gate_in.f_value == 9:
						return (gate_in, 0)

	def backtrace(self, node, v):
		#backtrace from object to IPT
		'''
		invert target value if it is inversion gate
		'''
		'''# for test
		while node.gtype != 'IPT':
			if 9 in [n.f_value for n in node.unodes]:
				if node.gtype in ['NOT', 'NOR', 'NAND', 'XNOR']:
						v = v ^ 15
				unknown_list = []
				for upnode in node.unodes:
					if upnode.f_value == 9:
						unknown_list.append(upnode)
				node = random.choice(unknown_list)
		'''
		while node.gtype != 'IPT':
			
			#if len(node.unodes) > 3:
			if (node.lev < self.circuit.nodes_lev[-1].lev / 2) and (len(node.unodes) < 3): # for test
				if 9 in [n.f_value for n in node.unodes]:
					if node.gtype in ['NOT', 'NOR', 'NAND', 'XNOR']:
						v = v ^ 15
					unknown_list = []
					trace_count_list = []
					for upnode in node.unodes:
						if upnode.f_value == 9:
							unknown_list.append(upnode)
							trace_count_list.append(upnode.trace_count)
					index = trace_count_list.index(min(trace_count_list))
					unknown_list[index].trace_count += 1
					node = unknown_list[index]
			else:
				if node.gtype in ['NOT', 'NOR', 'NAND', 'XNOR']:
					v = v ^ 15
				if v == 0:
					for up_node in sorted(node.unodes, key = lambda x : x.CC0):
						if up_node.f_value == 9:
							node = up_node
							break
				else:
					for up_node in sorted(node.unodes, key = lambda x : x.CC1):
						if up_node.f_value == 9:
							node = up_node
							break
		return (node, v)

	def implication(self, node_num, v):
		#given IPT values and do the simulation of the circuit
		'''
		use five values to differentiate 1,0,D,D_BAR,X -> 15,0,12,3,9
		use bitwise operation
		mask 0b1111 are use to flip each bit of the value
		do not modify value at the target node but store simulation value in check_s_a_v for future check
		after each simulation, set all the other value except 15,0,12,3 to 9
		update d_frontier 
		'''
		if self.target_node.gtype == 'IPT':
			self.check_s_a_v = self.s_a_v ^ 15
		
		node_num.f_value = v
		for node in self.circuit.nodes_lev:
			if node.gtype != 'IPT':
				unodes_list = self.unodes_val(node)
				count = 0
				for value_unode in unodes_list:#deal with xor xnor
					if value_unode == 9:
						count += 1
				imply_value = 0
				if (node.gtype == 'BRCH'):
					imply_value = node.unodes[0].f_value
				elif (node.gtype == 'OR'):
					imply_value = functools.reduce(lambda x, y: x | y, unodes_list)
				elif (node.gtype == 'NOR'):
					imply_value = functools.reduce(lambda x, y: x | y, unodes_list) ^ 0b1111
				elif (node.gtype == 'AND'):
					imply_value = functools.reduce(lambda x, y: x & y, unodes_list)
				elif (node.gtype == 'NAND'):
					imply_value = functools.reduce(lambda x, y: x & y, unodes_list) ^ 0b1111
				elif (node.gtype == 'XOR'):
					if count == 0:
						imply_value = functools.reduce(lambda x, y: x ^ y, unodes_list)
					else:
						imply_value = 9
				elif (node.gtype == 'XNOR'):
					if count == 0:
						imply_value = functools.reduce(lambda x, y: x ^ y, unodes_list) ^ 0b1111
					else:
						imply_value = 9
				elif (node.gtype == 'BUFF'):
					imply_value = node.unodes[0].f_value
				elif (node.gtype == 'NOT'):
					imply_value = node.unodes[0].f_value ^ 0b1111

				if node.num == self.target_num :
					self.check_s_a_v = imply_value
				else:
					node.f_value = imply_value

				if node.f_value not in [0, 3, 12, 15]:
					node.f_value = 9
				if self.check_s_a_v not in [0, 15]:
					self.check_s_a_v = 9
		
		self.d_frontier = []
		for node in self.circuit.nodes_lev:
			if node.f_value == 9 :
				if any(node_value in self.unodes_val(node) for node_value in (12,3)):
					#self.d_frontier.append(node)
					self.d_frontier.insert(0, node)

		if self.check_s_a_v == 9:
			self.d_frontier.insert(0, self.target_node)

	def unodes_val(self, node):
		#return all values of upnodes of a gate
		return [unode.f_value for unode in node.unodes]

	def print_IPT_OPT(self):
		#print PI and PO value
		print('PI:')
		for node in self.circuit.PI:
			print(node.num,'>>\t',five_value(node.f_value).name)
		print('PO:')
		for node in self.circuit.PO:
			print(node.num,'>>\t',five_value(node.f_value).name)

	def return_IPT(self):
		#return PI and PO value
		return_list = []
		for i in range(len(self.circuit.PI)):
			return_list.append(self.circuit.PI[i].f_value)
		return return_list

	def reset_and_get_fault(self, num, sav):
		for node in self.circuit.nodes_lev:
			node.f_value = 9
			node.trace_count = 0
		self.target_num = num
		self.s_a_v = sav*15
		self.d_frontier = []
		self.check_s_a_v = 9
		self.target_node = self.circuit.nodes.get(num)
		self.d_frontier.append(self.target_node)
		self.count = 0
