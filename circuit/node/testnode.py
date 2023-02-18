# -*- coding: utf-8 -*-

import pdb
import math 
import sys
from enum import Enum
from abc import ABC, abstractmethod

sys.path.insert(0,'..')
import utils
import node.node as node

# We are using GNOT, etc. as we may later use X values
class TestNode(ABC):
    """For now, it is designed for STAFAN, SCOAP, PFS and PPSF"""
    def __init__(self):
        # used for PPSF and SPPF 
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
    
    @abstractmethod
    def eval_CC(self):
        ''' forward assignment of SCOAP-CC for this node based on unodes''' 
        # raise NotImplementedError()
        pass
    
    @abstractmethod
    def eval_CO(self):
        ''' backward assignment of SCOAP-CO for unodes of this node''' 
        # raise NotImplementedError()
        pass
    
    @abstractmethod
    def stafan_b(self):
        ''' backward assignment of STAFAN observability for unodes of this node''' 
        # raise NotImplementedError()
        pass

class TestBUFF(node.BUFF, TestNode):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        node.BUFF.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestNOT(node.NOT, TestNode):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        node.NOT.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestOR(node.OR, TestNode):
    def __init__(self, n_type, g_type, num):
        node.OR.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestNOR(node.NOR, TestNode):
    def __init__(self, n_type, g_type, num):
        node.NOR.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestAND(node.AND, TestNode):
    def __init__(self, n_type, g_type, num):
        node.AND.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestNAND(node.NAND, TestNode):
    def __init__(self, n_type, g_type, num):
        node.NAND.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestXOR(node.XOR, TestNode):
    def __init__(self, n_type, g_type, num):
        basnode.XOR.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestXNOR(node.XNOR, TestNode):
    def __init__(self, n_type, g_type, num):
        node.XNOR.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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

class TestIPT(node.IPT, TestNode):
    def __init__(self, n_type, g_type, num):
        node.IPT.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

    def imply_p(self, bitwise_not, pfs_V):
        self.pfs_V = pfs_V * bitwise_not

    def eval_CC(self):
        self.CC0 = 0 
        self.CC1 = 0

    def eval_CO(self):
        return 

    def stafan_b(self):
        return 

class TestBRCH(node.BRCH, TestNode):
    def __init__(self, n_type, g_type, num):
        node.BRCH.__init__(self, n_type, g_type, num)
        TestNode.__init__(self)

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
        self.unodes[0].B1 = 1 - utils.mul_list(brchs_B1_c)
        self.unodes[0].B0 = 1 - utils.mul_list(brchs_B0_c)