"""Logic nodes of a gate-level circuit.

A node represents a signal together with the gate that drives it. Every gate
class can evaluate its output from the values of its input nodes in three modes:

``imply``    two-valued logic (0 and 1)
``imply_t``  three-valued logic (0, 1 and ``X_VALUE`` for unknown)
``imply_b``  bit-parallel logic: the values are integers whose bits are
             independent simulations, e.g. one test pattern per bit
"""
import math
import operator
import sys
from abc import ABC, abstractmethod
from enum import StrEnum
from functools import reduce

from pycad.config import X_VALUE

# Integer codes of the types in the .ckt file format (the index is the code).
_CKT_GATE_CODES = ("IPT", "BRCH", "XOR", "OR", "NOR", "NOT", "NAND", "AND", "XNOR", "BUFF")
_CKT_NODE_CODES = ("GATE", "PI", "FB", "PO")


class GateType(StrEnum):
    """Type of the gate that drives a node. Members compare equal to their names."""
    IPT = "IPT"
    BRCH = "BRCH"
    XOR = "XOR"
    OR = "OR"
    NOR = "NOR"
    NOT = "NOT"
    NAND = "NAND"
    AND = "AND"
    XNOR = "XNOR"
    BUFF = "BUFF"

    @classmethod
    def from_ckt_code(cls, code: int) -> "GateType":
        """Gate type for the integer code used in the ``.ckt`` file format."""
        return cls(_CKT_GATE_CODES[code])


class NodeType(StrEnum):
    """Role of a node in the circuit. Members compare equal to their names."""
    GATE = "GATE"
    PI = "PI"
    FB = "FB"
    PO = "PO"

    @classmethod
    def from_ckt_code(cls, code: int) -> "NodeType":
        """Node type for the integer code used in the ``.ckt`` file format."""
        return cls(_CKT_NODE_CODES[code])


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
    gtype : GateType
        the upnode gate type (a plain string such as "NAND" is converted)
    ntype : NodeType
        the node type (a plain string such as "PI" is converted)
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
        self.gtype = GateType(g_type)
        self.ntype = NodeType(n_type)
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
    def imply_b(self):
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
    
class _PassThrough(Node):
    """A gate whose output is simply the value of its single input, in every mode."""

    def imply(self):
        self.value = self.unodes[0].value

    imply_b = imply
    imply_t = imply


class BUFF(_PassThrough):
    """Buffer."""


class BRCH(_PassThrough):
    """Fan-out branch: a copy of the stem signal."""


class NOT(Node):
    """Inverter."""

    def imply(self):
        self.value = 1 if (self.unodes[0].value == 0) else 0

    def imply_b(self):
        self.value = self.unodes[0].value ^ Node.bitwise_not

    def imply_t(self):
        value = self.unodes[0].value
        if value == 0 or value == 1:
            self.value = 1 - value
        elif value == X_VALUE:
            self.value = X_VALUE


class _ControlledGate(Node):
    """AND, NAND, OR and NOR: a controlling input value decides the output on its own.

    Subclasses set ``CONTROL`` (the controlling input value), ``INVERT`` (1 if the
    output is inverted) and ``_combine`` (the bitwise operation that merges inputs).

    ``cval`` and ``inv`` hold the same information as 4-bit masks (15 is logic one,
    0 is logic zero), the encoding used by the D-algorithm.
    """

    CONTROL: int
    INVERT: int

    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.cval = 15 * self.CONTROL
        self.inv = 15 * self.INVERT

    @staticmethod
    def _combine(a, b):
        raise NotImplementedError

    def imply(self):
        controlled = self.CONTROL in self.unodes_val()
        self.value = (self.CONTROL if controlled else 1 - self.CONTROL) ^ self.INVERT

    def imply_t(self):
        values = self.unodes_val()
        if self.CONTROL in values:
            self.value = self.CONTROL ^ self.INVERT
        elif X_VALUE in values:
            self.value = X_VALUE
        else:
            self.value = (1 - self.CONTROL) ^ self.INVERT

    def imply_b(self):
        self.value = reduce(self._combine, (unode.value for unode in self.unodes))
        if self.INVERT:
            self.value ^= Node.bitwise_not


class AND(_ControlledGate):
    CONTROL, INVERT = 0, 0
    _combine = staticmethod(operator.and_)


class NAND(_ControlledGate):
    CONTROL, INVERT = 0, 1
    _combine = staticmethod(operator.and_)


class OR(_ControlledGate):
    CONTROL, INVERT = 1, 0
    _combine = staticmethod(operator.or_)


class NOR(_ControlledGate):
    CONTROL, INVERT = 1, 1
    _combine = staticmethod(operator.or_)


class _ParityGate(Node):
    """XOR and XNOR: the output depends on the parity of the number of ones."""

    INVERT: int

    def __init__(self, n_type, g_type, num):
        Node.__init__(self, n_type, g_type, num)
        self.c_flag = 0

    def imply(self):
        self.value = (sum(self.unodes_val()) + self.INVERT) % 2

    def imply_t(self):
        if X_VALUE in self.unodes_val():
            self.value = X_VALUE
        else:
            self.imply()

    def imply_b(self):
        self.value = reduce(operator.xor, (unode.value for unode in self.unodes))
        if self.INVERT:
            self.value ^= Node.bitwise_not


class XOR(_ParityGate):
    INVERT = 0


class XNOR(_ParityGate):
    INVERT = 1


class IPT(Node):
    """Primary input. Unlike the other gates, ``imply*`` take the value to apply."""

    def imply(self, value):
        self.value = value

    imply_b = imply
    imply_t = imply
