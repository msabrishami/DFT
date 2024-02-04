
import math 
import sys

from enum import Enum
from abc import ABC, abstractmethod

sys.path.append('../')
from config import X_VALUE
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
    gtype : TODO
        the upnode gate type
        supporting: IPT, BRCH, XOR, OR, NOR, NOT, NAND, AND, BUFF
    ntype : TODO
        the node type
        supporting: GATE, PI, FB, PO
    unodes : list 
        list of upper hand node objects
    dnodes : list 
        list of lower hand node objects
    """

    bitlen = int(math.log2(sys.maxsize))+1 # move to utils
    bitwise_not = 2**bitlen-1

    def __init__(self, n_type, g_type, num):
        self.bitwise_not = Node.bitwise_not
        self.bitlen = Node.bitlen
        self.gtype = g_type
        self.ntype = n_type
        self.num = num
        self.lev = None 
        self.value = None
        self.cval = None    #TODO: controlling value, set to 15 by mistake 
        self.inv = None     #TODO: inverting value, set to 15 by mistake
        self.unodes = []
        self.dnodes = []
        self.flagA = None   # Very professional 
        self.flagB = None   # Very professional 

        # # SSTA Project
        self.dd_cell = None
        self.dd_node = None

    def __str__(self):
        res = ", ".join([str(self.num), self.ntype, self.gtype, str(self.lev)]) 
        res += ", FIN: [" + " ".join([str(fin.num) for fin in self.unodes])
        res += "], FOUT: [" + " ".join([str(fout.num) for fout in self.dnodes])
        res += "]"
        return res
    
    def add_unode(self, unode):
        self.unodes.append(unode)
    
    def add_dnode(self, dnode):
        self.dnodes.append(dnode)
    
    def unodes_val(self):
        return [int(unode.value) if unode.value=='0' or unode.value=='1' else unode.value for unode in self.unodes]
    
    @abstractmethod
    def imply(self):
        ''' forward implication for a logic gate ''' 
        pass
    
    @abstractmethod
    def imply_b(self, bitwise_not):
        ''' forward parallel implication for a logic gate ''' 
        pass
    
    @abstractmethod
    def imply_t(self):
        ''' forward implication for logic gate with ternary input ''' 
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


    def print_info(self, get_labels=False, print_labels=True):
        if get_labels:
            return ["N", "LEV", "GATE"]
        if print_labels:
            print(f"N:{str(self.num).zfill(4)}\t", end="")
            print(f"LEV:{str(self.lev).zfill(2)}\t", end="")
            print(f"GATE:{self.gtype}\t", end="")
            print()
        else:
            print(f"N:{str(self.num).zfill(4)}\t", end="")
            print(f"{str(self.lev).zfill(2)}\t", end="")
            print(f"{self.gtype}\t", end="")
            print()
    
    @staticmethod
    def gen_node(node_info, std_node_lib):
        """ Generate a node based on information in node_info
            
            Parameters
            ----------
            node_info : dict
         """
        
        # TODO: How about when n_type is GATE and g_type is IPT? e.g. on 1908.ckt
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
    
    def imply_t(self):
        self.value = self.unodes[0].value
    
class NOT(Node):
    """ This gate is yet not tested""" 
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)

    def imply(self):
        try: 
            self.value = 1 if (self.unodes[0].value == 0) else 0
        except:
            import IPython
            IPython.embed()

    def imply_b(self):
        self.value = self.unodes[0].value ^ Node.bitwise_not
    
    def imply_t(self):
        if self.unodes[0].value == 0 or self.unodes[0].value == 1:
            self.value = 1 - self.unodes[0].value
        elif self.unodes[0].value == X_VALUE:
                self.value = X_VALUE

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
    
    def imply_t(self):
        if 1 in self.unodes_val():
            self.value = 1
        elif X_VALUE in self.unodes_val():
            self.value = X_VALUE
        else:
            self.value = 0

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
        self.value = self.value ^ Node.bitwise_not
    
    def imply_t(self):
        if 1 in self.unodes_val():
            self.value = 0
        elif X_VALUE in self.unodes_val():
            self.value = X_VALUE
        else:
            self.value = 1
        
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

    def imply_t(self):
        if 0 in self.unodes_val():
            self.value = 0

        elif X_VALUE in self.unodes_val():
            self.value = X_VALUE
        
        else:
            self.value = 1

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
        self.value = self.value ^ Node.bitwise_not

    def imply_t(self):
        if 0 in self.unodes_val():
            self.value = 1

        elif X_VALUE in self.unodes_val():
            self.value = X_VALUE
        
        else:
            self.value = 0

class XOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0 

    def imply(self):
        try:
            self.value = sum(self.unodes_val())%2
        except:
            print("(NODE) ERROR") # TODO: raise exception 
    
    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value ^ unode.value

    def imply_t(self):
        if X_VALUE in self.unodes_val():
            self.value = X_VALUE
        else:
            self.value = sum(self.unodes_val())%2

class XNOR(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0 

    def imply(self):
        self.value = (sum(self.unodes_val())+1)%2

    def imply_b(self):
        self.value = self.unodes[0].value
        for unode in self.unodes[1:]:
            self.value = self.value ^ unode.value
        self.value = self.value ^ Node.bitwise_not
    
    def imply_t(self):
        if X_VALUE in self.unodes_val():
            self.value = X_VALUE
        else:
            self.value = (sum(self.unodes_val())+1) %2

class IPT(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
    
    def imply(self, value):
        self.value = value
    
    def imply_b(self, value):
        self.value = value

    def imply_t(self, value):
        self.value = value

class BRCH(Node):
    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
    
    def imply(self):
        self.value = self.unodes[0].value
    
    def imply_b(self):
        self.value = self.unodes[0].value

    def imply_t(self):
        self.value = self.unodes[0].value
