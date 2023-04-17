#TODO: conflicts in check()
#TODO: xor/xnor

import sys
sys.path.append('../')

from fault_simulation.fault import Fault
from circuit.circuit import Circuit

from collections import deque
import random

ONE_VALUE = 1
ZERO_VALUE = 0
D_VALUE = "D"
D_PRIME_VALUE = "~D"
X_VALUE = 'X'

class D_alg():
    def __init__(self, circuit: Circuit, fault: Fault) -> None:
        self.circuit = circuit
        self.D_frontier = deque() #when append? in imply and check? or after it
        self.J_frontier = deque() #when append? in imply and check? or after it
        # self.valued_nodes = []

        # set all nodes values to X
        for n in self.circuit.nodes_lev:
            self.reset_node(n)

        # set the faulty node to D or D'
        for n in self.circuit.nodes_lev:
            if n.num == fault.node_num:
                print(n.num)
                self.faulty_node = n
                if fault.stuck_val == "1":
                    n.value = D_PRIME_VALUE
                elif fault.stuck_val == "0":
                    n.value = D_VALUE
                print(n.value)
                break

        print(f'D-Algorithm initialized with fault {fault.__str__()} in circuit {circuit.c_name}.\n')

    def error_at_PO(self):
        for p in self.circuit.PO:
            if p.value == D_VALUE or p.value == D_PRIME_VALUE:
                return True
        return False
    
    def get_controlling_value(self, node):
        if node.gtype == 'AND' or node.gtype == 'NAND':
            return ZERO_VALUE
        elif node.gtype == 'OR' or node.gtype == 'NOR':
            return ONE_VALUE
        elif node.gtype =='XOR' or node.gtype == 'XNOR':
            raise Exception("Not yet!")
        #what about NOT, brch, buff

    def inverse(value):
        if value == ZERO_VALUE:
            return ONE_VALUE
        elif value == ONE_VALUE:
            return ZERO_VALUE
        elif value == D_VALUE:
            return D_PRIME_VALUE
        elif value == D_PRIME_VALUE:
            return D_VALUE
        else:
            raise Exception("Has no inverse")
    
    def set_unodes(self, n, value):
        # if n.num == self.faulty_node.num:
        #     return
        
        for u in n.unodes:
            if u.value == D_VALUE or u.value == D_PRIME_VALUE:
                continue
            
            elif (u.value == 0 and value == 1) or (u.value == 1 and value == 0):
                print('Conflict!')
                return False
            elif (u.value == 'X') and (value == 0 or value == 1):
                u.value = value


    def get_unodes_val(self, node):
        return [n.value for n in node.unodes]

    def eval_dnodes(self, node): #TODO: DETECT CONFLICT?!
        if len(node.dnodes) == 0 or node.dnodes[0].num == self.faulty_node.num:
            return
        
        if node.dnodes[0].gtype == 'IPT' or node.dnodes[0].gtype == 'BRCH' or node.dnodes[0].gtype == 'BUFF':
            for n in node.dnodes:
                n.value = node.value

        elif node.dnodes[0].gtype == 'OR':
            if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ONE_VALUE
            elif (D_VALUE in self.get_unodes_val(node.dnodes[0])) and (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ONE_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if D_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_VALUE
                if D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_PRIME_VALUE

        elif node.dnodes[0].gtype == 'NOR':
            if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ZERO_VALUE
            elif (D_VALUE in self.get_unodes_val(node.dnodes[0])) and (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ZERO_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if D_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_PRIME_VALUE
                if D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_VALUE

        elif node.dnodes[0].gtype == 'AND':
            if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_VALUE in self.get_unodes_val(node.dnodes[0])):                
                node.dnodes[0].value = ZERO_VALUE
            elif (D_VALUE in self.get_unodes_val(node.dnodes[0])) and (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ZERO_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if D_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_VALUE
                if D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_PRIME_VALUE

        elif node.dnodes[0].gtype == 'NAND':
            if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ONE_VALUE
            elif (D_VALUE in self.get_unodes_val(node.dnodes[0])) and (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ONE_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if D_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_PRIME_VALUE
                if D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0]):
                    node.dnodes[0].value = D_VALUE

        elif node.dnodes[0].gtype == 'XOR' or node.dnodes[0].gtype == 'XNOR':
            # flag = True
            # for udnode in node.dnodes[0].unodes:
            #     if udnode.value not in [ZERO_VALUE, ONE_VALUE]:
            #         flag = False
            #         break
            # if flag:
            #     node.dnodes[0].imply()
            raise NotImplemented

        elif node.dnodes[0].gtype == 'NOT':
            node.dnodes[0].value = D_alg.inverse(node.value)
    
    def eval_unodes(self, node):
        if node.gtype == 'IPT' or node.gtype == 'BRCH' or node.gtype == 'BUFF':
            res = self.set_unodes(node, node.value)

        elif node.gtype == 'OR':
            if node.value == ZERO_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'AND':
            if node.value == ONE_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NOR':
            if node.value == ONE_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NAND':
            if node.value == ZERO_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'XOR' or node.gtype == 'XNOR':
            res = self.set_unodes(node, X_VALUE)
        
        elif node.gtype == 'NOT':
            # res = self.set_unodes(node, D_alg.inverse(node.value))
            if node.value == ONE_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            elif node.value == ZERO_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            elif node.value == D_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            elif node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
        
        return res
            
    def imply_forward(self, node, value):
        node.value = value
        q = deque()
        q.append(node)

        while q:
            front = q.popleft()
            self.eval_dnodes(front)
            for dnode in front.dnodes:
                if dnode not in q:
                    q.append(dnode)

    def imply_backward(self, node, value):
        node.value = value
        q = deque()
        q.append(node)

        while q:
            front = q.popleft()
            res = self.eval_unodes(front)
            for unode in front.unodes:
                if unode not in q:
                    q.append(unode)
            if res == False:
                return res
        
        return True

    def imply_and_check(self, node):
        """
        Returns: boolean
            the booleans is the result of check part
        """
        before_values = [n.value for n in self.circuit.nodes_lev]
        self.imply_forward(node, node.value)
        after_values_f = [n.value for n in self.circuit.nodes_lev]
        # print('here')
        # print(before_values, after_values_f)

        updated_nodes_f = []
        for i in range(len(self.circuit.nodes_lev)):
            if after_values_f[i] != before_values[i]:
                updated_nodes_f.append(self.circuit.nodes_lev[i])

        res = self.imply_backward(node, node.value)
        if res == False:
            return False
        after_values_b = [n.value for n in self.circuit.nodes_lev]

        updated_nodes_b = []
        for i in range(len(self.circuit.nodes_lev)):
            if after_values_b[i] != before_values[i]:
                updated_nodes_b.append(self.circuit.nodes_lev[i])
        
        for n in updated_nodes_f+updated_nodes_b:
            self.imply_and_check(n)
        
        return True

    def reset_node(self, node):
        node.value = X_VALUE
    
    def run(self):
        """The exact recursive algorithm"""
        before_imply = [f'{n.num}:{n.value}' for n in self.circuit.nodes_lev]
        if not self.imply_and_check(self.faulty_node):
            return False
        after_imply = [f'{n.num}:{n.value}' for n in self.circuit.nodes_lev]

        print('BEFORE IMPLY:')
        print(before_imply)
        print('AFTER IMPLY:')
        print(after_imply)
        print()
        if self.error_at_PO():
            if len(self.D_frontier) == 0:
                return False
            
            untried_D = self.D_frontier.pop()
            while untried_D:
                controlling_value = self.get_controlling_value(untried_D)
                for k in untried_D:
                    if k.value == X_VALUE:
                        k.value = D_alg.inverse(controlling_value)
                if self.run():
                    return True

                if len(self.D_frontier):
                    untried_D = self.D_frontier.pop()
                untried_D = None

                #TODO: REVERSE UPDATED VALUES

            return False

        if len(self.J_frontier) == 0:
            return True

        untried_J = self.J_frontier.pop()
        c = self.get_controlling_value(untried_J)
                
        while X_VALUE in [inp.value for inp in untried_J.unodes]:
            
            j = random.random([inp for inp in untried_J if inp.value == X_VALUE])
            j.value = c
            if self.run():
                return True
            j.value = D_alg.inverse(c)

        return False
    
if __name__ == '__main__':
    """Remove this main scope later"""
    circuit = Circuit('../../data/ckt/c1.ckt')
    fault = Fault(18, 0)

    dalg = D_alg(circuit, fault)
    dalg.run()