# ---> methods that appears here must be removed from node.py

# -*- coding: utf-8 -*-

import pdb
import math 
import sys
import operator
from enum import Enum
from functools import reduce
import node.node as basenode

# We are using GNOT, etc. as we may later use X values
""" helper function
returns multiplication of values in a list"""

mul_list = lambda arr: reduce(operator.mul, arr, 1) # faster / move it to utils

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

# class TestNode(basenode.Node):
#     """ #TODO: complete
#     Extended version of Node, containing testing attributes and methods.
#         1- STAFAN
#         2- SCOAP
#     """

#     def __init__(self, n_type, g_type, num):
        
#         super.__init__(self, n_type, gtype, num)
#         # used for PPSF and SPPF 
#         # print("I WAS CALLED")
#         bitlen = int(math.log2(sys.maxsize))+1
#         self.bitwise_not = 2**bitlen-1

#         # PFS:
#         self.pfs_V = None   # PFS value
#         self.pfs_I = None   # PFS mask
#         #self.pfs_S = None  # stuck values of fault for each pass

#         # Saeed does not confirm
#         self.faultlist_dfs = set() # will be aset

#         # SCOAP measures
#         self.CC0 = None
#         self.CC1 = None
#         self.CO = None

#         # STAFAN for all test measures
#         self.one_count = 0      # count
#         self.zero_count = 0     # count
#         self.sen_count = 0      # count
        
#         # STAFAN Forward for every test measure
#         self.sense = False      # Boolean, maybe redundant

#         # STAFAN 
#         self.S = None           # prob
#         self.C1 = None          # prob
#         self.C0 = None          # prob
#         self.B1 = None          # prob
#         self.B0 = None          # prob
#         self.D0 = None          # prob
#         self.D1 = None          # prob

#         #Entropy
#         self.Entropy =None      #entropy of the node

#         # Test Point Insertion Measurements
#         self.stat = {}
        
#         # SSTA Project
#         self.dd_cell = None
#         self.dd_node = None
    
    def imply_p(self, bitwise_not):
        ''' forward parallel implication for a logic gate ''' 
        raise NotImplementedError()

    def insert_f(self, bitwise_not, pfs_S):
        """ insert a fault for pdf in this node """ 
        pfs_I_bar = self.pfs_I ^ bitwise_not
        self.pfs_V = (pfs_I_bar & self.pfs_V) | (self.pfs_I & pfs_S)         

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


class TestBUFF(basenode.BUFF):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)

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
        self.faultlist_dfs.add((self.num, not_gate(self.value)))

class TestNOT(basenode.NOT):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        # print('I was called')
        super().__init__(n_type, g_type, num)
        # super(TestNode, self).__init__(n_type, g_type, num)
        # super(basenode.NOT, self).__init__(n_type, g_type, num)

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
        self.faultlist_dfs.add((self.num, not_gate(self.value)))

class TestOR(basenode.OR):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)
        self.cval = 15
        self.inv = 0

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
                print(f"Warning (OR.stafan_b): C1=0 for node {unode.num}", end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C0)}", end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (OR.stafan_b): unresolved issue")
                unode.B1 = self.B1
                for x in ne_C0:
                    unode.B1 *= x
                print(f" ==> B1 ~ {unode.B1:.2e}")
                
            try:
                unode.B0 = self.B0 * self.C0 / unode.C0
            except ZeroDivisionError:
                print(f"Warning (OR.stafan_b): C0=0 for node {unode.num}", end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C0)}", end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (OR.stafan_b): unresolved issue")
                unode.B0 = self.B0
                for x in ne_C0:
                    unode.B0 *= x
                print(f" ==> node.B0 ~ {unode.B0:.2e}")

    def dfs(self):
        self.faultlist_dfs.clear()
        dfs_general(self, 1)

class TestNOR(basenode.NOR):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)
        self.cval = 15
        self.inv = 15

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
                print(f"Warning (NOR.stafan_b): C1=0 for node {unode.num}", end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C0)}", end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (NOR.stafan_b): unresolved issue")
                unode.B1 = self.B0 
                for x in ne_C0:
                    unode.B1 *= x
                print(f" ==> B1 ~ {unode.B1:.2e}")

            try:
                unode.B0 = self.B1 * self.C1 / unode.C0
            except ZeroDivisionError:
                print(f"Warning (NOR.stafan_b): C0=0 for node {unode.num}", end="\t")
                ne_C0 = [x.C0 for x in unode.get_neighbors(inclusive=False)]
                print("|ne|={len(ne_C0)}", end="\t")
                if 0 in ne_C0:
                    raise ValueError("Error (NOR.stafan_b): unresolved issue")
                unode.B0 = self.B1
                for x in ne_C0:
                    unode.B0 *= x
                print(f" ==> B0 ~ {unode.B0:.2e}")

    def dfs(self):
        # the controling value of NOR is 1
        self.faultlist_dfs.clear()
        dfs_general(self, 1)

class TestAND(basenode.AND):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)
        self.cval = 0
        self.inv = 0

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
                print(f"Warning (AND.stafan_b): C1=0 for node {unode.num}", end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C1)}", end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (AND.stafan_b): unresolved issue")
                unode.B1 = self.B1
                for x in ne_C1:
                    unode.B1 *= x 
                print(f" ==> B1 ~ {unode.B1:.2e}")
            try:
                unode.B0 = self.B0 * (unode.S - self.C1) / unode.C0
            except ZeroDivisionError:
                print(f"Warning (AND.stafan_b): C0=0 for node {unode.num}", end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C1)}", end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (NAND.stafan_b): unresolved issue")
                unode.B0 = self.B0
                for x in ne_C1:
                    unode.B0 *= x 
                print(f" ==> node.B0 ~ {unode.B0:.2e}")

    def dfs(self):
        # the controling value of AND is 0
        self.faultlist_dfs.clear()
        dfs_general(self, 0)

class TestNAND(basenode.NAND):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)
        self.cval = 0
        self.inv = 15
    
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
                print(f"Warning (NAND.stafan_b): C1=0 for node {unode.num}", end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C1)}", end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (NAND.stafan_b): unresolved issue")
                unode.B1 = self.B0
                for x in ne_C1:
                    unode.B1 *= x 
                print(f" ==> B1 ~ {unode.B1:.2e}")
            try:
                unode.B0 = self.B1 * (unode.S - self.C0) / unode.C0 
            except ZeroDivisionError:
                print(f"Warning (NAND.stafan_b): C0=0 for node {unode.num}", end="\t")
                ne_C1 = [x.C1 for x in unode.get_neighbors(inclusive=False)]
                print(f"|ne|={len(ne_C1)}", end="\t")
                if 0 in ne_C1:
                    raise ValueError("Error (NAND.stafan_b): unresolved issue")
                unode.B0 = self.B1
                for x in ne_C1:
                    unode.B0 *= x 
                print(f" ==> node.B0 ~ {unode.B0:.2e}")

    def dfs(self):
        # the controling value of NAND is 0
        self.faultlist_dfs.clear()
        dfs_general(self, 0)

class TestXOR(basenode.XOR):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)
        self.c_flag = 0 # what is this?

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
        xor_FL_set.add((self.num, not_gate(self.value)))
        self.faultlist_dfs = xor_FL_set

class TestXNOR(basenode.XNOR):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)
        self.c_flag = 0 # what is this?

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
        xnor_FL_set.add((self.num, not_gate(self.value)))
        self.faultlist_dfs = xnor_FL_set

class TestIPT(basenode.IPT):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)

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
        self.faultlist_dfs.add((self.num, not_gate(self.value)))

class TestBRCH(basenode.BRCH):
    def __init__(self, n_type, g_type, num):
        super().__init__(n_type, g_type, num)

    def imply_b(self):
        self.value = self.unodes[0].value

    def imply_p(self, bitwise_not):
        self.pfs_V = self.unodes[0].pfs_V

    def eval_CC(self):
        self.CC0 = self.unodes[0].CC0
        self.CC1 = self.unodes[0].CC1

    def eval_CO(self): 
        # CO measurement for a stem is done by its branches
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
        self.faultlist_dfs.add((self.num, not_gate(self.value)))

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
        nc_FL_set.add((node.num, not_gate(node.value)))
        # print(list(nc_FL_set))
        node.faultlist_dfs = nc_FL_set.copy()
    
    # there is a controlling value on inputs 
    else :
        node.faultlist_dfs.clear()
        node.faultlist_dfs = c_FL_set.difference(nc_FL_set)
        node.faultlist_dfs.add((node.num, not_gate(node.value)))
    c_FL_set.clear()
    nc_FL_set.clear()
    #TODO: clear this return, if it is correct, document it
    return fault_set

def not_gate(a):
    '''NOT gate'''
    return 1-a