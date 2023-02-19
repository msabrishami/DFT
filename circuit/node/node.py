# -*- coding: utf-8 -*-

import pdb
import math 
import sys
import operator

from enum import Enum
from functools import reduce
from abc import ABC, abstractmethod

# We are using GNOT, etc. as we may later use X values

class gtype(Enum):
    IPT = 0
    BRCH = 1
    XOR = 2
    OR = 3
    NOR = 4
    NOT = 5
    NAND = 6
    AND = 7
    XNOR = 8
    BUFF = 9

class ntype(Enum):
    GATE = 0
    PI = 1
    FB = 2
    PO = 3

class Node(ABC):
    """ Representing the abstract of a circuit node, i.e. also representing its unique upnode gate.
        Difference of node type and gate type important, refer to ckt documentation.

    Attributes
    ----------
    num : str
        the node number as in ckt format
    value : int
        logical value on the node, currently only accepting 2-value logic
    lev : int
        level of the node in circuit
    gtype:      the upnode gate type
                supporting: IPT, BRCH, XOR, OR, NOR, NOT, NAND, AND, BUFF
    ntype:      the node type
                supporting: GATE, PI, FB, PO
    unodes:     list of upper hand node objects
    dnodes:     list of lower hand node objects
    cpt:        #TODO: possibly checkpoints
    sa0:        #TODO: possibly single stuck at 0 fault
    sa1:        #TODO: possibly single stuck at 1 fault
    index:      #TODO: Not known
    """

    def __init__(self, n_type, g_type, num):
        # Saeed confirms: 
        self.gtype = g_type
        self.ntype = n_type
        self.num = num
        self.lev = None # choose a more descriptive name
        self.value = None
        self.cval = None # ?
        self.inv = None
        self.unodes = []
        self.dnodes = []
        self.flagA = None # flag?
        self.flagB = None # flag?

        # used for PPSF and SPPF 
        # TODO
        bitlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**bitlen-1

        #Entropy
        self.Entropy =None      #entropy of the node

        # # SSTA Project
        self.dd_cell = None
        self.dd_node = None

    def __str__(self):
        res = ", ".join([str(self.num), self.ntype, self.gtype, str(self.lev)]) 
        res += " FIN: " + " ".join([str(fin.num) for fin in self.unodes])
        res += " FOUT: " + " ".join([str(fout.num) for fout in self.dnodes])
        if self.C0 and self.C1:
            res += f" C0={self.C0:.4f} C1={self.C1:.4f} B0={self.B0:.4f} B1={self.B1:.4f}"
        return res
    
    def add_unode(self, unode):
        self.unodes.append(unode)
    
    def add_dnode(self, dnode):
        self.dnodes.append(dnode)
    
    def unodes_val(self):
        return [int(unode.value) for unode in self.unodes]
    
    @abstractmethod
    def imply(self):
        ''' forward implication for a logic gate ''' 
        # raise NotImplementedError() --> it implicitly exist when we import ABC
        pass
    
    @abstractmethod
    def imply_b(self, bitwise_not):
        ''' forward parallel implication for a logic gate ''' 
        # raise NotImplementedError()
        pass

    def get_neighbors(self, value=False, inclusive=False):
        ''' Return a list of nodes (or the values of nodes)
        that have the same out gate as this node
        inclusive: if set True, includes this node itself.
        value: if set True, returns the value of neighbors node, by default list of nodes
        '''
        # TODO: Check this for all possible gates, specially branch
        # TODO: not tested
        res = []
        if inclusive:
            res.append(self.num)
        if self.dnodes:
            for node in self.dnodes[0].unodes:
                # if self.num == node.num and inclusive
                #     res.append(node)
                if self.num != node.num:
                    res.append(node)

        return [n.value for n in res] if value else res

    # TODO Move to children later
    def is_sensible(self, count=True):
        ''' Calculates if this node can propagate the gate in front of it.
        i.e. if current value changes, down-node (output gate) value will change.
        '''
        # TODO: implemented on two value system, not sure if it applies to others

        if self.ntype == 'PO':
            return True

        elif self.dnodes[0].gtype in ['NOT', 'XOR', 'XNOR', 'BRCH', 'BUFF']:
            return True

        elif self.dnodes[0].gtype in ['AND', 'NAND']:
            if 0 in self.get_neighbors(inclusive=False, value = True):
                return False
            else:
                return True

        elif (self.dnodes[0].gtype == 'OR') | (self.dnodes[0].gtype == 'NOR'):
            if 1 in self.get_neighbors(inclusive=False, value=True):
                return False
            else:
                return True
        else:
            print("Error: Not implemented yet") 
            pdb.set_trace()

    def print_info(self, get_labels=False, print_labels=True):
        # TODO: two if/else is wrong, create strings and print once
        # raises error when stafan is not calculated (move where stafan is, not here)
        if get_labels:
            return ["N", "LEV", "GATE", "CC0", "CC1", "CO", "C0",
                    "C1", "S", "B0", "B1"]
        if print_labels:
            print(f"N:{str(self.num).zfill(4)}\t", end="")
            print(f"LEV:{str(self.lev).zfill(2)}\t", end="")
            print(f"GATE:{self.gtype}\t", end="")
            print(f"CC0:{str(self.CC0).zfill(3)}\t", end="")
            print(f"CC1:{str(self.CC1).zfill(3)}\t", end="")
            print(f"CO:{str(self.CO).zfill(3)}\t", end="")
            print(f"C0:{self.C0:.2e}\t", end="")
            print(f"C1:{self.C1:.2e}\t", end="")
            print(f"S:{self.S:.2e}\t", end="")
            print(f"B0:{self.B0:.2e}\t", end="")
            print(f"B1:{self.B1:.2e}\t", end="")
            print()
        else:
            print(f"N:{str(self.num).zfill(4)}\t", end="")
            print(f"{str(self.lev).zfill(2)}\t", end="")
            print(f"{self.gtype}\t", end="")
            print(f"{str(self.CC0).zfill(3)}\t", end="")
            print(f"{str(self.CC1).zfill(3)}\t", end="")
            print(f"{str(self.CO).zfill(3)}\t", end="")
            print(f"{self.C0:.2e}\t", end="")
            print(f"{self.C1:.2e}\t", end="")
            print(f"{self.S:.2e}\t", end="")
            print(f"{self.B0:.2e}\t", end="")
            print(f"{self.B1:.2e}\t", end="")
            print()
    
    @staticmethod
    def gen_node(node_info, std_node_lib):
        """ Generate a node based on information in node_info
            
            Parameters
            ----------
            node_info : dict
                # TODO
         """
        
        if node_info['n_type'] == "PI" and node_info['g_type'] == "IPT":
            return std_node_lib['IPT'](node_info['n_type'], node_info['g_type'], node_info['num'])

        elif node_info['n_type'] == "FB" and node_info['g_type'] == "BRCH":
            return std_node_lib['BRCH'](node_info['n_type'], node_info['g_type'], node_info['num'])

        elif node_info['n_type'] == "GATE" or node_info['n_type'] == "PO":
            if node_info['g_type'] in ['XOR','OR','NOR','NOT','NAND','AND','BUFF','XNOR']:
                return std_node_lib[node_info['g_type']](node_info['n_type'], node_info['g_type'], node_info['num'])
        else:
            raise NotImplementedError()
    
class BUFF(Node):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)

    def imply(self):
        self.value = self.unodes[0].value

    def imply_b(self):
        self.value = self.unodes[0].value

class NOT(Node):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)

    def imply(self):
        self.value = 1 if (self.unodes[0].value == 0) else 0

    def imply_b(self):
        self.value = self.unodes[0].value ^ self.bitwise_not  

class OR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.cval = 15
        self.inv = 0

    def imply(self):
        self.value = 1 if (1 in self.unodes_val()) else 0
    
    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value | unode.value

class NOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.cval = 15
        self.inv = 15

    def imply(self):
        self.value = 0 if (1 in self.unodes_val()) else 1

    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value | unode.value
        self.value = self.value ^ self.bitwise_not

class AND(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.cval = 0
        self.inv = 0

    def imply(self):
        self.value = 0 if (0 in self.unodes_val()) else 1

    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value & unode.value

class NAND(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.cval = 0
        self.inv = 15
    
    def imply(self):
        self.value = 1 if (0 in self.unodes_val()) else 0
    
    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value & unode.value
        self.value = self.value ^ self.bitwise_not

class XOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0 # what is this?

    def imply(self):
        try:
            self.value = 1 if (sum(self.unodes_val())%2 == 1) else 0
        except:
            print("issue")
            pdb.set_trace()
    
    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value ^ unode.value

class XNOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0 # what is this?

    def imply(self):
        self.value = 0 if (sum(self.unodes_val())%2 == 1) else 1

    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value ^ unode.value
        self.value = self.value ^ self.bitwise_not
    
class IPT(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
    
    def imply(self, value):
        self.value = value
    
    def imply_b(self, value):
        self.value = value

class BRCH(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
    
    def imply(self):
        self.value = self.unodes[0].value
    
    def imply_b(self):
        self.value = self.unodes[0].value