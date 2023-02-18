class five_value(Enum): # what are these?
   ZERO = 0
   ONE = 15
   D = 12
   D_BAR = 3
   X = 9


class podem_node_5val(): # Change Case - move somewhere else
    def __init__(self):
        self.x = 1
        self.bit0 = 0
        self.bit1 = 0

    def fault_node(self, SA1):
        if self.x == 0:
            self.bit0 = SA1
            self.bit1 = not SA1

    def is_0(self):
        if self.x == 1:
            return False
        elif (self.bit0 | self.bit1) == 0:
            return True 

        return False

    def is_1(self):
        if self.x == 1:
            return False
        elif (self.bit0 & self.bit1) == 1:
            return True
        
        return False

    def is_d(self):
        if self.x == 1:
            return False
        elif (self.bit0 ^ self.bit1) == 1:
            return True

        return False

    def is_sa0(self):
        if self.x == 1:
            return False
        elif (self.bit0 == 0) & (self.bit1 == 1):
            return True

        return False

    def is_sa1(self):
        if self.x == 1:
            return False
        elif (self.bit0 == 1) & (self.bit1 == 0):
            return True

        return False

    def __and__(self, other):
        val = podem_node_5val()
        val.bit0 = self.bit0 & other.bit0
        val.bit1 = self.bit1 & other.bit1
        val.x = 0
        if self.x == 1:
            if other.is_0():
                val.x = 0
            else:
                val.x = 1
        if other.x == 1:
            if self.is_0():
                val.x = 0
            else:
                val.x = 1
        return val

    def __or__(self, other):
        val = podem_node_5val()
        val.bit0 = self.bit0 | other.bit0
        val.bit1 = self.bit1 | other.bit1
        val.x = 0
        if self.x == 1:
            if other.is_1() == True:
                val.x = 0
            else:
                val.x = 1
        if other.x == 1:
            if self.is_1():
                val.x = 0
            else:
                val.x = 1
        return val

    def __xor__(self, other):
        val = podem_node_5val()
        val.bit0 = self.bit0 ^ other.bit0
        val.bit1 = self.bit1 ^ other.bit1
        val.x = self.x | other.x
        return val

    def __invert__(self):
        val = podem_node_5val()
        val.bit0 = not self.bit0
        val.bit1 = not self.bit1
        val.x = self.x
        return val


# ---> methods that appears here must be removed from node.py

# -*- coding: utf-8 -*-

import pdb
import math 
import sys
from enum import Enum
import node.node as node

sys.path.insert(0,'..')
import utils


##### DFS Functions #####
class TestNode(node.Node):

    def dfs(self):
        ''' deductive fault simulation (dfs) using unodes ''' 
        raise NotImplementedError()


class TestBUFF(node.BUFF):
    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs = self.unodes[0].faultlist_dfs.copy()
        self.faultlist_dfs.add((self.num, utils.not_gate(self.value)))

class TestNOT(node.NOT):
    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs = self.unodes[0].faultlist_dfs.copy()
        self.faultlist_dfs.add((self.num, utils.not_gate(self.value)))

class TestOR(node.OR):
    def dfs(self):
        self.faultlist_dfs.clear()
        dfs_general(self, 1)

class TestNOR(node.NOR):
    def dfs(self):
        # the controling value of NOR is 1
        self.faultlist_dfs.clear()
        dfs_general(self, 1)

class TestAND(node.AND):
    def dfs(self):
        # the controling value of AND is 0
        self.faultlist_dfs.clear()
        dfs_general(self, 0)

class TestNAND(node.NAND):
    def dfs(self):
        # the controling value of NAND is 0
        self.faultlist_dfs.clear()
        dfs_general(self, 0)

class TestXOR(node.XOR):
    def dfs(self):
        self.faultlist_dfs.clear()
        xor_FL_set = set()
        for unode in self.unodes:
            xor_FL_set = xor_FL_set.symmetric_difference(unode.faultlist_dfs)
        xor_FL_set.add((self.num, utils.not_gate(self.value)))
        self.faultlist_dfs = xor_FL_set

class TestXNOR(node.XNOR):
    def dfs(self):
        self.faultlist_dfs.clear()
        xnor_FL_set = set()
        for unode in self.unodes:
            xnor_FL_set = xnor_FL_set.symmetric_difference(unode.faultlist_dfs)
        xnor_FL_set.add((self.num, utils.not_gate(self.value)))
        self.faultlist_dfs = xnor_FL_set

class TestIPT(node.IPT):
    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs.add((self.num, utils.not_gate(self.value)))

class TestBRCH(node.BRCH):
    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs = self.unodes[0].faultlist_dfs.copy()
        self.faultlist_dfs.add((self.num, utils.not_gate(self.value)))

def dfs_general(node, c_val):
    """
    Helper function; it doesn't belong to any node class
    The general dfs algorithm is suitable for (gates with controlling),
        such as AND, NAND, OR, NOR, etc., and does not include XOR, XNOR, INV, etc.
    node: an object from class Node
    c_val: controlling value for this node
    functionality: 
    Making changes on node.faultlist_dfs, based on the fault list of node.unodes
    For PI nodes, faultlist_dfs is fault list on itself
    """
    # the fault list of the gate output
    fault_set = set()
    # intersection set of all faults implied by controling inputs
    c_FL_set = set()
    # union set of all faults implied by non-controling inputs
    nc_FL_set = set()
    # imply if there is any control value amoung the inputs
    flag_c = 0
    first_c = 1
    for unode in node.unodes:
        if unode.value == c_val :
            flag_c = 1
            # for the first controling value, use its FL as initialization
            if first_c == 1:
                c_FL_set = unode.faultlist_dfs.copy()
                first_c = 0
            else:
                c_FL_set = c_FL_set.intersection(unode.faultlist_dfs)
        else :
            nc_FL_set = nc_FL_set.union(unode.faultlist_dfs)
    
    # none of the inputs are controlling value
    if flag_c == 0:
        node.faultlist_dfs.clear()
        nc_FL_set.add((node.num, utils.not_gate(node.value)))
        # print(list(nc_FL_set))
        node.faultlist_dfs = nc_FL_set.copy()
    
    # there is a controlling value on inputs 
    else :
        node.faultlist_dfs.clear()
        node.faultlist_dfs = c_FL_set.difference(nc_FL_set)
        node.faultlist_dfs.add((node.num, utils.not_gate(node.value)))
    c_FL_set.clear()
    nc_FL_set.clear()
    #TODO: clear this return, if it is correct, document it
    return fault_set