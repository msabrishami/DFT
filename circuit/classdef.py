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


class Node:
    ''' Implementation is node based.
    A node also represents the upnode gate, as it is always unique.
    Difference of node type and gate type important, refer to ckt document.
    value:      value on the node, currently only accepting 2-value logic
    num:        the node number as in ckt format
    lev:        level of the node in circuit
    gtype:      the upnode gate type
                supporting: IPT, BRCH, XOR, OR, NOR, NOT, NAND, AND
    ntype:      the node type
                supporting: GATE, PI, FB, PO
    unodes:     list of upper hand node objects
    dnodes:     list of lower hand node objects
    cpt:        #TODO: possibly checkpoints
    sa0:        #TODO: possibly single stuck at 0 fault
    sa1:        #TODO: possibly single stuck at 1 fault
    index:      #TODO: Not known
    TODO: add information about the rest of the attributes,
    including paper references for STAFAN and SCOAP
    '''
    def __init__(self, n_type, g_type, num):
        # Saeed confirms: 
        self.gtype = g_type
        self.ntype = n_type
        self.num = num
        self.lev = None
        self.value = None
        self.unodes = []
        self.dnodes = []
        self.scoap = {}

        # Saeed does not confirm
        self.cpt = 0
        self.sa0 = 0
        self.sa1 = 0
        # self.index = 0 # should be removed
        # self.faultlist_dfs = []
        # self.parallel_value = 0
        # self.d_value = []

        # SCOAP measures
        # self.CC0 = 0            # INT value
        # self.CC1 = 0            # INT value
        # self.CO = 0             # INT value

        # STAFAN measures
        self.one_count = 0      # count
        self.zero_count = 0     # count

        self.sen_count = 0      # count
        self.S = 0.0            # prob
        self.C1 = 0.0           # prob
        self.C0 = 0.0           # prob
        self.B1 = 0.0           # prob
        self.B0 = 0.0           # prob

        # GNN-CAD (our work)
        self.sense = True       # Boolean, maybe redundant
        self.D1 = False         # Boolean
        self.D0 = False         # Boolean
        self.D1_count = 0       # Count
        self.D0_count = 0       # Count
    
    def __str__(self):
        return(", ".join([str(self.num), self.ntype, self.gtype, str(self.lev), 
            str(len(self.unodes)), str(len(self.dnodes))]))
    
    def imply(self):
        ''' forward implication for a logic gate ''' 
        raise NotImplementedError()
    
    def unodes_val(self):
        return [unode.value for unode in self.unodes]
    
    
    # TODO: Saeed thinks many of these are redundant! 
    '''
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
    '''

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

    # TODO Move to children later
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

    def print_info(self, get_labels=False, print_labels=True):
        # TODO: two if/else is wrong, create strings and print once
        if get_labels:
            return ["N", "LEV", "GATE", "CC0", "CC1", "CO", "C0",
                    "C1", "S", "B0", "B1", "D0#", "D1#", "D0%", "D1%"]
        if print_labels:
            print("N:{}\t".format(str(self.num).zfill(4)), end="")
            print("LEV:{}\t".format(str(self.lev).zfill(2)), end="")
            print("GATE:{}\t".format(self.gtype), end="")
            print("CC0:{}\t".format(str(self.CC0).zfill(3)), end="")
            print("CC1:{}\t".format(str(self.CC1).zfill(3)), end="")
            print("CO:{}\t".format(str(self.CO).zfill(3)), end="")
            print("C0:{:.2f}\t".format(self.C0), end="")
            print("C1:{:.2f}\t".format(self.C1), end="")
            print("S:{:.2f}\t".format(self.S), end="")
            print("B0:{:.2f}\t".format(self.B0), end="")
            print("B1:{:.2f}\t".format(self.B1), end="")
            print("#D0:{}\t".format(str(self.D0_count).zfill(4)), end="")
            print("#D1:{}\t".format(str(self.D1_count).zfill(4)), end="")
            print("%D0:{:.2f}\t".format(self.D0_p), end="")
            print("%D1:{:.2f}\t".format(self.D1_p))
        else:
            print("N:{}\t".format(str(self.num).zfill(4)), end="")
            print("{}\t".format(str(self.lev).zfill(2)), end="")
            print("{}\t".format(self.gtype), end="")
            print("{}\t".format(str(self.CC0).zfill(3)), end="")
            print("{}\t".format(str(self.CC1).zfill(3)), end="")
            print("{}\t".format(str(self.CO).zfill(3)), end="")
            print("{:.2f}\t".format(self.C0), end="")
            print("{:.2f}\t".format(self.C1), end="")
            print("{:.2f}\t".format(self.S), end="")
            print("{:.2f}\t".format(self.B0), end="")
            print("{:.2f}\t".format(self.B1), end="")
            print("{}\t".format(str(self.D0_count).zfill(4)), end="")
            print("{}\t".format(str(self.D1_count).zfill(4)), end="")
            print("{:.2f}\t".format(self.D0_p), end="")
            print("{:.2f}\t".format(self.D1_p))
    

class NAND(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)
    
    def imply(self):
        self.value = 1 if (0 in self.unodes_val) else 0


class NAND(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)
    
    def imply(self):
        self.value = 1 if (0 in self.unodes_val) else 0


class OR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)

    def imply(self):
        self.value = 1 if (1 in self.unodes_val) else 0


class NOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)

    def imply(self):
        self.value = 0 if (1 in self.unodes_val) else 0


class AND(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)

    def imply(self):
        self.value = 0 if (0 in self.unodes_val) else 0


class XOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)

    def imply(self):
        self.value = 1 if (sum(val_list)%2 == 1) else 0


class IPT(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)
    
    def imply(self, value):
        self.value = value 


class BRCH(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, ntype, g_type, num)
    
    def imply(self, value):
        self.value = self.unodes[0].value




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


