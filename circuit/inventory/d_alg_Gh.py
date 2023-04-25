# TODO: xor/xnor

import sys
sys.path.append('../')
import random
import typing
from collections import deque
from circuit.circuit import Circuit
from fault_simulation.fault import Fault, FaultList

ONE_VALUE = 1
ZERO_VALUE = 0
D_VALUE = "D"
D_PRIME_VALUE = "~D"
X_VALUE = 'X'

PRINT_LOG = True
# be_reset_nodes = {}
class D_alg():
    def __init__(self, circuit: Circuit, fault: Fault) -> None:
        self.circuit = circuit

        # set all nodes values to X
        for n in self.circuit.nodes_lev:
            self.reset_node(n)

        # set the faulty node to D or D'
        for n in self.circuit.nodes_lev:
            if n.num == fault.node_num:
                if PRINT_LOG: print(n.num)
                self.faulty_node = n
                if fault.stuck_val == "1":
                    n.value = D_PRIME_VALUE
                elif fault.stuck_val == "0":
                    n.value = D_VALUE
                if PRINT_LOG: print(n.value)
                break

        if PRINT_LOG: print(
            f'D-Algorithm initialized with fault {fault.__str__()} in circuit {circuit.c_name}.\n')

    def D_in_input(self, node):
        for n in node.unodes:
            if n.value == D_VALUE or n.value == D_PRIME_VALUE:
                return True
        return False

    def get_D_frontier(self):  # optimize later
        D_frontier = []
        for n in self.circuit.nodes_lev:
            if n.value == X_VALUE and self.D_in_input(n):
                D_frontier.append(n)

        return D_frontier

    def get_J_frontier(self):  # optimize later
        J_frontier = []
        for n in self.circuit.nodes_lev:
            if n.value != X_VALUE:
                for inp in n.unodes:
                    if inp.value == X_VALUE:
                        J_frontier.append(n)
                        break
        return J_frontier

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
        elif node.gtype == 'XOR' or node.gtype == 'XNOR':
            raise Exception("Not yet!")
        elif node.gtype == 'NOT':
            return D_alg.inverse(node.value)
        elif node.gtype == 'BUFF' or node.gtype == 'BRCH':
            return node.value
        
    def inverse(value):
        if value == ZERO_VALUE:
            return ONE_VALUE
        elif value == ONE_VALUE:
            return ZERO_VALUE
        elif value == D_VALUE:
            return D_PRIME_VALUE
        elif value == D_PRIME_VALUE:
            return D_VALUE

    def set_unodes(self, n, value):

        for u in n.unodes:
            if u.value == D_VALUE or u.value == D_PRIME_VALUE:
                continue

            elif (u.value == ZERO_VALUE and value == ONE_VALUE) or (u.value == ONE_VALUE and value == ZERO_VALUE):
                return False

            elif (u.value == X_VALUE) and (value == ZERO_VALUE or value == ONE_VALUE):
                u.value = value

    def get_unodes_val(self, node):
        return [n.value for n in node.unodes]

    def if_all(self, nodes, value):
        for n in nodes:
            if n.value != value:
                return False
        return True

    def eval_dnodes(self, node):
        one_output = True if len(node.dnodes) == 1 else False
        old_value = None

        if len(node.dnodes) == 1:
            one_output = True
            old_value = node.dnodes[0].value
        
        if len(node.dnodes) == 0:
            return True

        elif node.dnodes[0].gtype == 'BRCH' or node.dnodes[0].gtype == 'BUFF':
            for n in node.dnodes:
                if n.value != D_VALUE and n.value != D_PRIME_VALUE:
                    if (n.value == ZERO_VALUE and node.value == ONE_VALUE) or (n.value == ONE_VALUE and node.value == ZERO_VALUE):
                        return False
                    n.value = node.value

        elif node.dnodes[0].gtype == 'OR':
            if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])):
                if node.dnodes[0].value == ZERO_VALUE:
                    return False
                node.dnodes[0].value = ONE_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ZERO_VALUE):
                    if node.dnodes[0].value == ONE_VALUE:
                        return False
                    else:
                        node.dnodes[0].value = ZERO_VALUE

        elif node.dnodes[0].gtype == 'NOR':
            if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])):
                if node.dnodes[0].value == ONE_VALUE:
                    return False
                node.dnodes[0].value = ZERO_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ONE_VALUE): # all zero
                    if node.dnodes[0].value == ONE_VALUE:
                        return False
                    else:
                        node.dnodes[0].value = ONE_VALUE

        elif node.dnodes[0].gtype == 'AND':
            if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])):
                if node.dnodes[0].value == ONE_VALUE:
                    return False
                node.dnodes[0].value = ZERO_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ONE_VALUE): #all one
                    if node.dnodes[0].value == ZERO_VALUE:
                        return False
                    else:
                        node.dnodes[0].value = ONE_VALUE

        elif node.dnodes[0].gtype == 'NAND':
            if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])):
                if node.dnodes[0].value == ZERO_VALUE:
                    return False
                node.dnodes[0].value = ONE_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ONE_VALUE): #all one
                    if node.dnodes[0].value == ONE_VALUE:
                        return False
                    else:
                        node.dnodes[0].value = ZERO_VALUE

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
            if node.value == ONE_VALUE:
                if node.dnodes[0].value == X_VALUE:
                    node.dnodes[0].value = ZERO_VALUE
                elif node.dnodes[0].value == ONE_VALUE:
                    return False
            elif node.value == ZERO_VALUE:
                if node.dnodes[0].value == X_VALUE:
                    node.dnodes[0].value = ONE_VALUE
                elif node.dnodes[0].value == ZERO_VALUE:
                    return False
            elif node.value == D_VALUE:
                    node.dnodes[0].value = D_PRIME_VALUE
            elif node.value == D_PRIME_VALUE:
                node.dnodes[0].value = D_VALUE

        if one_output:
            new_value = node.dnodes[0].value
            # print(f'{node.num}, old {old_value}, new {new_value}')
            if old_value == D_VALUE:
                if new_value == ZERO_VALUE:
                    return False
                elif new_value == ONE_VALUE:
                    node.dnodes[0].value = D_VALUE
            elif old_value == D_PRIME_VALUE:
                if new_value == ONE_VALUE:
                    return False
                elif new_value == ZERO_VALUE:
                    node.dnodes[0].value = D_PRIME_VALUE

        return True
        
    def eval_unodes(self, node):
        if node.gtype == 'IPT' or node.gtype == 'BRCH' or node.gtype == 'BUFF':
            if node.value == D_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            elif node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, node.value)

        elif node.gtype == 'OR':
            if node.value == ZERO_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NOR':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'AND':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NAND':
            if node.value == ZERO_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'XOR' or node.gtype == 'XNOR':
            res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NOT':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            elif node.value == ZERO_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        return res

    def imply_forward(self, node, value) -> bool:
        node.value = value
        q = deque()
        q.append(node)

        while q:
            front = q.popleft()
            res = self.eval_dnodes(front)
            for dnode in front.dnodes:
                if dnode not in q:
                    q.append(dnode)
            if res is False:
                print(f'CONLIFCT ON DNODES ',front.num)
                return res

        return True

    def imply_backward(self, node, value) -> bool:
        node.value = value
        q = deque()
        q.append(node)

        while q:
            front = q.popleft()
            res = self.eval_unodes(front)
            for unode in front.unodes:
                if unode not in q:
                    q.append(unode)
            if res is False:
                return res

        return True

    def imply_and_check(self, node) -> typing.Tuple[bool, list]:  # optimize get updated nodes.
        """
        Returns: boolean, list
            booleans: the result of check part
            list: list of updated nodes
        """
        initial_values = [n.value for n in self.circuit.nodes_lev]
        res = self.imply_forward(node, node.value)

        if res is False: #repeated code here.
            if PRINT_LOG: print('Forward Conflict on ',node.num)
            changed_nodes = []
            final_values = [n.value for n in self.circuit.nodes_lev]

            for i in range(len(self.circuit.nodes_lev)):
                if initial_values[i] != final_values[i]:
                    changed_nodes.append(self.circuit.nodes_lev[i])
            
            return res, changed_nodes+[node]
        after_values_f = [n.value for n in self.circuit.nodes_lev]

        updated_nodes_f = []
        for i in range(len(self.circuit.nodes_lev)):
            if after_values_f[i] != initial_values[i]:
                updated_nodes_f.append(self.circuit.nodes_lev[i])

        res = self.imply_backward(node, node.value)
        if res is False: #repeated code here.
            if PRINT_LOG: print('Backward Conflict')

            changed_nodes = []
            final_values = [n.value for n in self.circuit.nodes_lev]

            for i in range(len(self.circuit.nodes_lev)):
                if initial_values[i] != final_values[i]:
                    changed_nodes.append(self.circuit.nodes_lev[i])
            
            return res, changed_nodes
        
        after_values_b = [n.value for n in self.circuit.nodes_lev]

        updated_nodes_b = []
        for i in range(len(self.circuit.nodes_lev)):
            if after_values_b[i] != initial_values[i]:
                updated_nodes_b.append(self.circuit.nodes_lev[i])

        for n in updated_nodes_f+updated_nodes_b:
            res, _ = self.imply_and_check(n)
            if not res:
                new_values = [n.value for n in self.circuit.nodes_lev]
                changed_nodes = []
                for i in range(len(self.circuit.nodes_lev)):
                    if initial_values[i] != new_values[i]:
                        changed_nodes.append(self.circuit.nodes_lev[i])
                return False, changed_nodes

        final_values = [n.value for n in self.circuit.nodes_lev]
        changed_nodes = []

        for i in range(len(self.circuit.nodes_lev)):
            if initial_values[i] != final_values[i]:
                changed_nodes.append(self.circuit.nodes_lev[i])

        return True, changed_nodes

    def eval_D_frontier_node(self, node):
        n = node.unodes[0]
        if n.dnodes[0].gtype == 'OR' or n.dnodes[0].gtype == 'AND':
            if D_VALUE in self.get_unodes_val(n.dnodes[0]):
                    n.dnodes[0].value = D_VALUE
            elif D_PRIME_VALUE in self.get_unodes_val(n.dnodes[0]):
                n.dnodes[0].value = D_PRIME_VALUE
            else:
                print('THIS CASE')
        elif n.dnodes[0].gtype == 'NAND' or n.dnodes[0].gtype == 'NOR':
            if D_PRIME_VALUE in self.get_unodes_val(n.dnodes[0]):
                n.dnodes[0].value = D_VALUE
            elif D_VALUE in self.get_unodes_val(n.dnodes[0]):
                n.dnodes[0].value = D_PRIME_VALUE

    def reset_node(self, node):
        node.value = X_VALUE

    def run_D():
        pass
    def run_j():
        pass

    def run(self, node,  J_updated_nodes=set(), save_J_node = False, save_D_node=False, D_updated_nodes=set()):
        """The exact recursive algorithm"""
        before_imply = [f'{n.num}:{n.value}' for n in self.circuit.nodes_lev]
        
        if PRINT_LOG: 
            print('run is called on node', node.num, node.value)
            print('BEFORE IMPLY:')
            print(before_imply)
            
        imply_result, new_valued_nodes = self.imply_and_check(node)
        after_imply = [f'{n.num}:{n.value}' for n in self.circuit.nodes_lev]
        
        if save_J_node:
            for n in new_valued_nodes:
                J_updated_nodes.add(n)

        D_frontier = self.get_D_frontier()
        J_frontier = self.get_J_frontier()

        if PRINT_LOG:
            print('AFTER IMPLY:')
            print(after_imply)
            print()
            print(f'D: {[n.num for n in D_frontier]}')
            print(f'J: {[n.num for n in J_frontier]}')

            input()
        
        if not imply_result:
            return False, J_updated_nodes

        if not self.error_at_PO(): # HEre must reset nodes that has been updated by the previous DNODE
            if len(D_frontier) == 0:
                return False, J_updated_nodes

            untried_D = D_frontier.pop()
            if PRINT_LOG: print('Chosen D:', untried_D.num)
            while untried_D:
                self.eval_D_frontier_node(untried_D)
                if save_J_node:
                    J_updated_nodes.add(untried_D)
                controlling_value = self.get_controlling_value(untried_D)
                for k in untried_D.unodes:
                    if k.value == X_VALUE:
                        k.value = D_alg.inverse(controlling_value)
                        if save_J_node:
                            J_updated_nodes.add(k)
                
                
                res, new_updated = self.run(k, J_updated_nodes.copy())
                if save_J_node:
                    for n in new_updated:
                        J_updated_nodes.add(n)
                
                if res:
                    return True, J_updated_nodes

                if len(D_frontier):
                    untried_D = D_frontier.pop()
                    if PRINT_LOG: print('Chosen D:', untried_D.num)
                else:
                    untried_D = None

            return False, J_updated_nodes

        # error at PO
        if len(J_frontier) == 0:
            return True, J_updated_nodes

        untried_J = J_frontier.pop()
        if PRINT_LOG: print('Chosen J', untried_J.num)
        c = self.get_controlling_value(untried_J)
        save_J_node=True
        while X_VALUE in [inp.value for inp in untried_J.unodes]:

            j_idx = random.choice([inp for inp in range(len(untried_J.unodes)) if untried_J.unodes[inp].value == X_VALUE])
            untried_J.unodes[j_idx].value = c
            if save_J_node:
                J_updated_nodes.add(untried_J.unodes[j_idx])
                print(f'updated_nodes={[f.num for f in J_updated_nodes]}')
            if PRINT_LOG: print(f'set {untried_J.unodes[j_idx].num} to {c}.')
            res, new_updated = self.run(untried_J.unodes[j_idx], J_updated_nodes.copy(), save_J_node=True)
            
            if save_J_node:
                for n in new_updated:
                    J_updated_nodes.add(n)

            # input()
            if res:
                return True, J_updated_nodes

            if PRINT_LOG: print('Going Back on node', untried_J.unodes[j_idx].num, 'be reset nodes:', [n.num for n in new_updated])
            
            for n in new_updated:
                self.reset_node(n)
                J_updated_nodes.remove(n)
            
            untried_J.unodes[j_idx].value = D_alg.inverse(c)
            res, new = self.run(untried_J.unodes[j_idx],J_updated_nodes.copy() ,True)

            for n in new:
                J_updated_nodes.add(n)
            
            # if res is False:

            
            if len(J_frontier):
                untried_D = J_frontier.pop()
            else:
                untried_D = None

        return False, J_updated_nodes

if __name__ == '__main__':
    """Remove this main scope later"""

    circuit = Circuit('../../data/ckt/c3.ckt')
    
    # for n in circuit.nodes_lev:
    for n in [circuit.nodes_lev[0]]:
        # for stuck_val in [ONE_VALUE, ZERO_VALUE]:
        for stuck_val in [0]:
    # fault = Fault(1, 1)
            fault = Fault(n.num, stuck_val)
            dalg = D_alg(circuit, fault)
            res, _ = dalg.run(dalg.faulty_node)
            print('\nIs fault ', fault, 'detectable?', res)
            if res:
                if PRINT_LOG: print('Final Test Pattern:')
                if PRINT_LOG: print([f'{n.num}:{n.value}' for n in circuit.PI])
                input()