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

        # Saeed & Erfan:
        self.D1 = False
        self.D0 = False
        self.D1_count = 0
        self.D0_count = 0
        self.sense = True

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

    def get_neighbors(self, value=False, inclusive=False):
        ''' returns a list of nodes (or the values of ndoes) 
        that have the same out gate as this node
        inclusive: if set True, includes this node itself. 
        value: if set True, returns the value of neighbors node, by default list of nodes
        '''
        # TODO: Check this for all possible gates, specially branch
        # TODO: not tested
        res = []
        for node in self.dnodes[0].unodes:
            if self.num == node.num:
                res = res.append(node) if inclusive else res
            else:
                res.append(node)
        
        return [n.value for n in res] if value else res


    def is_sensible(self):
        ''' calculates if this node can propagate the gate infront of it. 
        i.e. if current value changes, down-node (output gate) value will change.
        '''
        # TODO: implemented on two value system, not sure if it applies to others

        if self.ntype == 'PO':
            return True

        elif self.dnodes[0].gtype in ['NOT', 'XOR', 'XNOR', 'BRCH']:
            return True

        elif self.dnodes[0].gtype in ['AND', 'NAND']:
            if 0 in self.get_neighbors(inclusive=False, value = True):
                return False
            else:
                return True

        elif ((self.dnodes[0].gtype == 'OR') | (self.dnodes[0].gtype == 'NOR')):
            if 1 in self.get_neighbors(inclusive=False, value=True):
                return False
            else:
                return True

        else:
            print("Error: Not implemented yet")

    def is_detectable(self):
        ''' checks if a node is detectable with current values
        logic-sim and sense should be pre-calculated
        updates D0/D1 flag and D0/D1 count 
        D_count is set to 0 when circuit is initilized
        D0: 
        D1: 
        '''
        # Jiayi please check this method, 
        self.D1 = False
        self.D0 = False

        if self.ntype == 'PO':
            self.D1 = True if (self.value == 1) else False
            self.D0 = True if (self.value == 0) else False

        elif self.sense:
            
            dn = self.dnodes[0]

            if dn.gtype == 'AND':
                self.D1 = True if ((self.value == 1) & (dn.D1)) else False
                self.D0 = True if ((self.value == 0) & (dn.D0)) else False
            
            elif dn.gtype == 'NAND':
                self.D1 = True if ((self.value == 1) & (dn.D0)) else False
                self.D0 = True if ((self.value == 0) & (dn.D1)) else False
            
            elif dn.gtype == 'OR':
                self.D1 = True if ((self.value == 1) & (dn.D1)) else False
                self.D0 = True if ((self.value == 0) & (dn.D0)) else False
            
            elif dn.gtype == 'NOR':
                self.D1 = True if ((self.value == 1) & (dn.D0)) else False
                self.D0 = True if ((self.value == 0) & (dn.D1)) else False
            
            elif dn.gtype == 'NOT':
                self.D1 = True if ((self.value == 1) & (dn.D0)) else False
                self.D0 = True if ((self.value == 0) & (dn.D1)) else False
            
            elif dn.gtype == 'XOR':
                if dn.value == 1:
                    self.D1 = dn.D1
                    self.D0 = dn.D1
                elif dn.value == 0:
                    self.D1 = dn.D0
                    self.D0 = dn.D0

            elif dn.gtype == 'BRCH':
                if (self.value == 1):
                    for branch in self.dnodes:
                        if branch.D1:
                            self.D1 = True
                            break
                elif (self.value == 0):
                    for branch in self.dnodes:
                        if branch.D0:
                            self.D0 = True
                            break
            else:
                print("gate type is {}".format(self.gtype))
                print("This gate is not supported yet")

        self.D1_count = (self.D1_count + 1) if self.D1 else self.D1_count
        self.D0_count = (self.D0_count + 1) if self.D0 else self.D0_count


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
    

