# -*- coding: utf-8 -*-
#from numpy import uint64
import pdb
import math 
import sys
from enum import Enum
from functools import reduce

# We are using GNOT, etc. as we may later use X values
"""" GENERAL NOTES AND SUGGESTIONS: 
    Class 1: Simple node in a graph
    Class 2: Node with test features
    Class 3: Node with SSTA features 
"""

""" helper function
returns multiplication of values in a list"""
mul_list = lambda arr: reduce(lambda a,b: a*b, arr, 1) # faster / move it to utils
# def mul_list(arr):
#     res = 1
#     for a in arr:
#         res  = res*a
#     return res

class five_value(Enum): # what are these?
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
    XNOR = 8
    BUFF = 9

class ntype(Enum):
    GATE = 0
    PI = 1
    FB = 2
    PO = 3

class Node:
    """ Representing a circuit node, i.e. also representing its unique upnode gate.
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
    TODO: add information about the rest of the attributes,
    including paper references for STAFAN and SCOAP
    """

    def __init__(self, n_type, g_type, num):
        # Saeed confirms: 
        self.gtype = g_type
        self.ntype = n_type
        self.num = num
        self.lev = None
        self.value = None
        self.cval = None
        self.inv = None
        self.unodes = []
        self.dnodes = []
        self.flagA = None # flag?
        self.flagB = None

        # used for PPSF and SPPF 
        # TODO
        bitlen = int(math.log2(sys.maxsize))+1
        self.bitwise_not = 2**bitlen-1

        # PFS:
        self.pfs_V = None   # PFS value
        self.pfs_I = None   # PFS mask
        #self.pfs_S = None  # stuck values of fault for each pass

        # Saeed does not confirm
        self.faultlist_dfs = set() # will be aset

        # SCOAP measures
        self.CC0 = None
        self.CC1 = None
        self.CO = None

        # STAFAN for all test measures
        self.one_count = 0      # count
        self.zero_count = 0     # count
        self.sen_count = 0      # count
        
        # STAFAN Forward for every test measure
        self.sense = False      # Boolean, maybe redundant

        # STAFAN 
        self.S = None           # prob
        self.C1 = None          # prob
        self.C0 = None          # prob
        self.B1 = None          # prob
        self.B0 = None          # prob
        self.D0 = None          # prob
        self.D1 = None          # prob

        #Entropy
        self.Entropy =None      #entropy of the node

        # Test Point Insertion Measurements
        self.stat = {}
        
        # SSTA Project
        self.dd_cell = None
        self.dd_node = None

    def __str__(self):
        res = ", ".join([str(self.num), self.ntype, self.gtype, str(self.lev)]) 
        res += " FIN: " + " ".join([str(fin.num) for fin in self.unodes])
        res += " FOUT: " + " ".join([str(fout.num) for fout in self.dnodes])
        if self.C0 and self.C1:
            res += " C0={:.4f} C1={:.4f} B0={:.4f} B1={:.4f}".format(self.C0, self.C1, self.B0, self.B1)
        return res
    
    def imply(self):
        ''' forward implication for a logic gate ''' 
        raise NotImplementedError()
    
    def imply_p(self, bitwise_not):
        ''' forward parallel implication for a logic gate ''' 
        raise NotImplementedError()

    def insert_f(self, bitwise_not, pfs_S):
        """ insert a fault for pdf in this node """ 
        pfs_I_bar = self.pfs_I ^ bitwise_not
        self.pfs_V = (pfs_I_bar & self.pfs_V) | (self.pfs_I & pfs_S)         

    def unodes_val(self):
        return [int(unode.value) for unode in self.unodes]
    
    def eval_CC(self):
        ''' forward assignment of SCOAP-CC for this node based on unodes''' 
        raise NotImplementedError()
    
    def eval_CO(self):
        ''' backward assignment of SCOAP-CO for unodes of this node''' 
        raise NotImplementedError()
    
    def stafan_b(self):
        ''' backward assignment of STAFAN observability for unodes of this node''' 
        raise NotImplementedError()

    def dfs(self):
        ''' deductive fault simulation (dfs) using unodes ''' 
        raise NotImplementedError()

    
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
        ''' Return a list of nodes (or the values of nodes)
        that have the same out gate as this node
        inclusive: if set True, includes this node itself.
        value: if set True, returns the value of neighbors node, by default list of nodes
        '''
        # TODO: Check this for all possible gates, specially branch
        # TODO: not tested
        # TODO: optimize: why not append the node itself out of for?
        res = []
        if self.dnodes:
            for node in self.dnodes[0].unodes:
                if self.num == node.num and inclusive:
                    res.append(node)
                elif self.num != node.num:
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
    
class BUFF(Node):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)

    def imply(self):
        self.value = self.unodes[0].value

    def imply_b(self):
        self.value = self.unodes[0].value

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V

    def eval_CC(self):
        self.CC0 = 1 + self.unodes[0].CC0
        self.CC1 = 1 + self.unodes[0].CC1
    
    def eval_CO(self):
        self.unodes[0].CO = self.CO + 1
    
    def stafan_b(self):
        self.unodes[0].B1 = self.B1
        self.unodes[0].B0 = self.B0
    
    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs = self.unodes[0].faultlist_dfs.copy()
        self.faultlist_dfs.add((self.num, GNOT(self.value)))

class NOT(Node):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)

    def imply(self):
        self.value = 1 if (self.unodes[0].value == 0) else 0

    def imply_b(self):
        self.value = self.unodes[0].value ^ self.bitwise_not  

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V ^ bitwise_not    # invert pfs_V using xor "1111..."

    def eval_CC(self):
        self.CC0 = 1 + self.unodes[0].CC1
        self.CC1 = 1 + self.unodes[0].CC0
    
    def eval_CO(self):
        self.unodes[0].CO = self.CO + 1
    
    def stafan_b(self):
        self.unodes[0].B1 = self.B0
        self.unodes[0].B0 = self.B1

    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs = self.unodes[0].faultlist_dfs.copy()
        self.faultlist_dfs.add((self.num, GNOT(self.value)))

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

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V
        for unode in self.unodes[1:]:
            self.pfs_V = self.pfs_V | unode.pfs_V

    def eval_CC(self):
        self.CC0 = 1 + sum([unode.CC0 for unode in self.unodes])
        self.CC1 = 1 + min([unode.CC1 for unode in self.unodes])
    
    def eval_CO(self):
        for unode in self.unodes:
            unode.CO = sum([unode.CC0 for unode in self.unodes]) - unode.CC0 + self.CO + 1
    
    def stafan_b(self):
        for unode in self.unodes:
            try: 
                unode.B1 = self.B1 * (unode.S - self.C0) / unode.C1
            except ZeroDivisionError:
                print("Warning (OR.stafan_b): C1=0 for node {}".format(unode.num), end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C0)), end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (OR.stafan_b): unresolved issue")
                unode.B1 = self.B1
                for x in ne_C0:
                    unode.B1 *= x
                print(" ==> B1 ~ {:.2e}".format(unode.B1))
                
            try:
                unode.B0 = self.B0 * self.C0 / unode.C0
            except ZeroDivisionError:
                print("Warning (OR.stafan_b): C0=0 for node {}".format(unode.num), end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C0)), end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (OR.stafan_b): unresolved issue")
                unode.B0 = self.B0
                for x in ne_C0:
                    unode.B0 *= x
                print(" ==> node.B0 ~ {:.2e}".format(unode.B0))

    def dfs(self):
        self.faultlist_dfs.clear()
        dfs_general(self, 1)

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
    
    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V
        for unode in self.unodes[1:]:
            self.pfs_V = self.pfs_V | unode.pfs_V
        self.pfs_V = self.pfs_V ^ bitwise_not

    def eval_CC(self):
        self.CC1 = 1 + sum([unode.CC0 for unode in self.unodes])
        self.CC0 = 1 + min([unode.CC1 for unode in self.unodes])
    
    def eval_CO(self):
        for unode in self.unodes:
            unode.CO = sum([unode.CC0 for unode in self.unodes]) - unode.CC0 + self.CO + 1

    def stafan_b(self):
        
        for unode in self.unodes:
            try:
                unode.B1 = self.B0 * (unode.S - self.C1) / unode.C1
            except ZeroDivisionError:
                print("Warning (NOR.stafan_b): C1=0 for node {}".format(unode.num), end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C0)), end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (NOR.stafan_b): unresolved issue")
                unode.B1 = self.B0 
                for x in ne_C0:
                    unode.B1 *= x
                print(" ==> B1 ~ {:.2e}".format(unode.B1))

            try:
                unode.B0 = self.B1 * self.C1 / unode.C0
            except ZeroDivisionError:
                print("Warning (NOR.stafan_b): C0=0 for node {}".format(unode.num), end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C0)), end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (NOR.stafan_b): unresolved issue")
                unode.B0 = self.B1
                for x in ne_C0:
                    unode.B0 *= x
                print(" ==> B0 ~ {:.2e}".format(unode.B0))

    def dfs(self):
        # the controling value of NOR is 1
        self.faultlist_dfs.clear()
        dfs_general(self, 1)

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
    
    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V
        for unode in self.unodes[1:]:
            self.pfs_V = self.pfs_V & unode.pfs_V

    def eval_CC(self):
        self.CC1 = 1 + sum([unode.CC1 for unode in self.unodes])
        self.CC0 = 1 + min([unode.CC0 for unode in self.unodes])

    def eval_CO(self):
        for unode in self.unodes:
            unode.CO = sum([unode.CC1 for unode in self.unodes]) - unode.CC1 + self.CO + 1

    def stafan_b(self):
        for unode in self.unodes:
            try:
                unode.B1 = self.B1 * self.C1 / unode.C1
            except ZeroDivisionError:
                print("Warning (AND.stafan_b): C1=0 for node {}".format(unode.num), end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C1)), end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (AND.stafan_b): unresolved issue")
                unode.B1 = self.B1
                for x in ne_C1:
                    unode.B1 *= x 
                print(" ==> B1 ~ {:.2e}".format(unode.B1))
            try:
                unode.B0 = self.B0 * (unode.S - self.C1) / unode.C0
            except ZeroDivisionError:
                print("Warning (AND.stafan_b): C0=0 for node {}".format(unode.num), end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C1)), end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (NAND.stafan_b): unresolved issue")
                unode.B0 = self.B0
                for x in ne_C1:
                    unode.B0 *= x 
                print(" ==> node.B0 ~ {:.2e}".format(unode.B0))

    def dfs(self):
        # the controling value of AND is 0
        self.faultlist_dfs.clear()
        dfs_general(self, 0)

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

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V
        for unode in self.unodes[1:]:
            self.pfs_V = self.pfs_V & unode.pfs_V
        self.pfs_V = self.pfs_V ^ bitwise_not

    def eval_CC(self):
        self.CC0 = 1 + sum([unode.CC1 for unode in self.unodes])
        self.CC1 = 1 + min([unode.CC0 for unode in self.unodes])

    def eval_CO(self):
        for unode in self.unodes:
            unode.CO = sum([unode.CC1 for unode in self.unodes]) - unode.CC1 + self.CO + 1
    
    def stafan_b(self):
        # Note: Formula in the original paper has a typo
        for unode in self.unodes:
            try: 
                unode.B1 = self.B0 * self.C0 / unode.C1
            except ZeroDivisionError:
                print("Warning (NAND.stafan_b): C1=0 for node {}".format(unode.num), end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C1)), end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (NAND.stafan_b): unresolved issue")
                unode.B1 = self.B0
                for x in ne_C1:
                    unode.B1 *= x 
                print(" ==> B1 ~ {:.2e}".format(unode.B1))
            try:
                unode.B0 = self.B1 * (unode.S - self.C0) / unode.C0 
            except ZeroDivisionError:
                print("Warning (NAND.stafan_b): C0=0 for node {}".format(unode.num), end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={}".format(len(ne_C1)), end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (NAND.stafan_b): unresolved issue")
                unode.B0 = self.B1
                for x in ne_C1:
                    unode.B0 *= x 
                print(" ==> node.B0 ~ {:.2e}".format(unode.B0))

    def dfs(self):
        # the controling value of NAND is 0
        self.faultlist_dfs.clear()
        dfs_general(self, 0)

class XOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0

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

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V
        for unode in self.unodes[1:]:
            self.pfs_V = self.pfs_V ^ unode.pfs_V

    def eval_CC(self):
        #TODO: only 2 inputs supported for now, we can later add multiple inputs
        if len(self.unodes) != 2:
            raise NameError('XOR with more than 2 inputs not implemented')
        # u_CC1 = [unode.CC1 for unode in self.unodes]
        # u_CC0 = [unode.CC0 for unode in self.unodes]
        self.CC1 = 1 + min(self.unodes[0].CC1+self.unodes[1].CC0, 
                self.unodes[0].CC0+self.unodes[1].CC1)
        self.CC0 = 1 + min(self.unodes[0].CC0+self.unodes[1].CC0, 
                self.unodes[0].CC1+self.unodes[1].CC1)

    def eval_CO(self):
        if len(self.unodes) != 2:
            raise NameError('XOR with more than 2 inputs not implemented')
        self.unodes[0].CO = min(self.unodes[1].CC0, self.unodes[1].CC1) + self.CO + 1
        self.unodes[1].CO = min(self.unodes[0].CC0, self.unodes[0].CC1) + self.CO + 1
    
    def stafan_b(self):
        for unode in self.unodes:
            unode.B1 = self.B0
            unode.B0 = self.B1

    def dfs(self):
        self.faultlist_dfs.clear()
        xor_FL_set = set()
        for unode in self.unodes:
            xor_FL_set = xor_FL_set.symmetric_difference(unode.faultlist_dfs)
        xor_FL_set.add((self.num, GNOT(self.value)))
        self.faultlist_dfs = xor_FL_set

class XNOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0

    def imply(self):
        self.value = 0 if (sum(self.unodes_val())%2 == 1) else 1

    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value ^ unode.value
        self.value = self.value ^ self.bitwise_not
    
    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V
        for unode in self.unodes[1:]:
            self.pfs_V = self.pfs_V ^ unode.pfs_V
        self.pfs_V = self.pfs_V ^ bitwise_not

    def eval_CC(self):
        #TODO: only 2 inputs supported for now, we can later add multiple inputs
        if len(self.unodes) != 2:
            raise NameError('XOR with more than 2 inputs not implemented')
        # u_CC1 = [unode.CC1 for unode in self.unodes]
        # u_CC0 = [unode.CC0 for unode in self.unodes]
        self.CC1 = 1 + min(self.unodes[0].CC0+self.unodes[1].CC0, 
                self.unodes[0].CC1+self.unodes[1].CC1)
        self.CC0 = 1 + min(self.unodes[0].CC0+self.unodes[1].CC1, 
                self.unodes[0].CC1+self.unodes[1].CC0)

    def eval_CO(self):
        if len(self.unodes) != 2:
            raise NameError('XNOR with more than 2 inputs not implemented')
        self.unodes[0].CO = min(self.unodes[1].CC0, self.unodes[1].CC1) + self.CO + 1
        self.unodes[1].CO = min(self.unodes[0].CC0, self.unodes[0].CC1) + self.CO + 1
    
    def stafan_b(self):
        for unode in self.unodes:
            unode.B1 = self.B0
            unode.B0 = self.B1

    def dfs(self):
        self.faultlist_dfs.clear()
        xnor_FL_set = set()
        for unode in self.unodes:
            xnor_FL_set = xnor_FL_set.symmetric_difference(unode.faultlist_dfs)
        xnor_FL_set.add((self.num, GNOT(self.value)))
        self.faultlist_dfs = xnor_FL_set

class IPT(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
    
    def imply(self, value):
        self.value = value
    
    def imply_b(self, value):
        self.value = value

    def imply_p(self, bitwise_not, pfs_V):
        self.pfs_V = pfs_V * bitwise_not

    def eval_CC(self):
        self.CC0 = 0 
        self.CC1 = 0

    def eval_CO(self):
        return 

    def stafan_b(self):
        return 

    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs.add((self.num, GNOT(self.value)))

class BRCH(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
    
    def imply(self):
        self.value = self.unodes[0].value
    
    def imply_b(self):
        self.value = self.unodes[0].value

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V

    def eval_CC(self):
        self.CC0 = self.unodes[0].CC0
        self.CC1 = self.unodes[0].CC1

    def eval_CO(self): 
        # CO measurement for a stem is done by it's branches
        # This causes redundant computation, but OK! 
        self.unodes[0].CO = min([node.CO for node in self.unodes[0].dnodes])

    def stafan_b(self):
        # STAFAN-B measurement for a stem has redundancy, similar to SCOAP-CO
        # This calculation is VERY approximate, read STAFAN paper
        brchs = self.unodes[0].dnodes
        brchs_B1_c = [(1-brch.B1) for brch in brchs]
        brchs_B0_c = [(1-brch.B0) for brch in brchs]
        self.unodes[0].B1 = 1 - mul_list(brchs_B1_c)
        self.unodes[0].B0 = 1 - mul_list(brchs_B0_c)

    def dfs(self):
        self.faultlist_dfs.clear()
        self.faultlist_dfs = self.unodes[0].faultlist_dfs.copy()
        self.faultlist_dfs.add((self.num, GNOT(self.value)))

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
        nc_FL_set.add((node.num, GNOT(node.value)))
        # print(list(nc_FL_set))
        node.faultlist_dfs = nc_FL_set.copy()
    
    # there is a controlling value on inputs 
    else :
        node.faultlist_dfs.clear()
        node.faultlist_dfs = c_FL_set.difference(nc_FL_set)
        node.faultlist_dfs.add((node.num, GNOT(node.value)))
    c_FL_set.clear()
    nc_FL_set.clear()
    #TODO: clear this return, if it is correct, document it
    return fault_set

def GNOT(a):
    '''NOT gate'''
    return 1-a
    # if a == 1:
    #     out = 0
    # elif a == 0:
    #     out = 1
    # return out

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
            if (other.is_1() == True):
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