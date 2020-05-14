# -*- coding: utf-8 -*-
from numpy import uint64
from enum import Enum

#__________________________________________________#
#_____________________CLASSDEF_____________________#
#__________________________________________________#

class five_value(Enum):
   ZERO = 0
   ONE = 15
   D = 12
   D_BAR = 3
   X = 9

class gtype(Enum):
    IPT = 0
    BRCH = 1
    XOR = 2
    OR = 3
    NOR = 4
    NOT = 5
    NAND = 6
    AND = 7

class ntype(Enum):
    GATE = 0
    PI = 1
    FB = 2
    PO = 3




class node:

    def __init__(self):
        self.value = None
        self.num = None
        self.lev = None
        self.gtype = None
        self.ntype = None
        self.unodes = []
        self.dnodes = []
        self.fin = None
        self.fout = None
        self.cpt = 0
        self.sa0 = 0
        self.sa1 = 0
        self.index = 0
        self.faultlist_dfs = []
        self.parallel_value = 0
        self.d_value = []
        self.CC0 = 0
        self.CC1 = 0
        self.CO = 0
        self.one_count = 0
        self.zero_count = 0
        self.sen_count = 0
        self.S = 0.0
        self.C1 = 0.0
        self.C0 = 0.0
        self.B1 = 0.0
        self.B0 = 0.0

    def add_unodes(self, unode):
        self.unodes.append(unode)
    def add_dnodes(self, dnode):
        self.dnodes.append(dnode)
    def add_faultlist(self, fault):
        self.faultlist_dfs.append(fault)
    def clear_faultlist(self):
        self.faultlist_dfs.clear()
    def copy_faultlist(self, faultlist):
        faultlist_dfs = faultlist.copy()



class podem_node_5val():
    def __init__(self):
        self.x = 1
        self.bit0 = 0
        self.bit1 = 0

    def fault_node(self, SA1):
        if (self.x == 0):
            self.bit0 = SA1
            self.bit1 = not SA1

    def is_0(self):
        if (self.x == 1):
            return False
        if ((self.bit0 | self.bit1) == 0):
            return True
        else:
            return False
    def is_1(self):
        if (self.x == 1):
            return False
        if ((self.bit0 & self.bit1) == 1):
            return True
        else:
            return False
    def is_d(self):
        if (self.x == 1):
            return False
        if ((self.bit0 ^ self.bit1) == 1):
            return True
        else:
            return False
    def is_sa0(self):
        if (self.x == 1):
            return False
        elif ((self.bit0 == 0) & (self.bit1 == 1)):
            return True
        else:
            return False
    def is_sa1(self):
        if (self.x == 1):
            return False
        elif ((self.bit0 == 1) & (self.bit1 == 0)):
            return True
        else:
            return False

    def __and__(self, other):
        val = podem_node_5val()
        val.bit0 = self.bit0 & other.bit0
        val.bit1 = self.bit1 & other.bit1
        val.x = 0
        if (self.x == 1):
            if (other.is_0()):
                val.x = 0
            else:
                val.x = 1
        if (other.x == 1):
            if(self.is_0()):
                val.x = 0
            else:
                val.x = 1
        return val

    def __or__(self, other):
        val = podem_node_5val()
        val.bit0 = self.bit0 | other.bit0
        val.bit1 = self.bit1 | other.bit1
        val.x = 0
        if (self.x == 1):
            if (other.is_1() == True):
                val.x = 0
            else:
                val.x = 1
        if (other.x == 1):
            if(self.is_1()):
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




