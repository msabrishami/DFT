# TODO: conflicts in check()
# TODO: xor/xnor

import sys
sys.path.append('../')
import random
from collections import deque
from circuit.circuit import Circuit
from fault_simulation.fault import Fault


ONE_VALUE = 1
ZERO_VALUE = 0
D_VALUE = "D"
D_PRIME_VALUE = "~D"
X_VALUE = 'X'


class D_alg():
    def __init__(self, circuit: Circuit, fault: Fault) -> None:
        self.circuit = circuit

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

        print(
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
        # what about NOT, brch, buff

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
                print('Conflict!')
                return False

            elif (u.value == X_VALUE) and (value == ZERO_VALUE or value == ONE_VALUE):
                u.value = value

    def get_unodes_val(self, node):
        return [n.value for n in node.unodes]

    def eval_dnodes(self, node):  # TODO: DETECT CONFLICT?!
        if len(node.dnodes) == 0:
            return
        
        elif node.dnodes[0].value == D_VALUE or node.dnodes[0].value == D_PRIME_VALUE:
            return

        elif node.dnodes[0].gtype == 'IPT' or node.dnodes[0].gtype == 'BRCH' or node.dnodes[0].gtype == 'BUFF':
            for n in node.dnodes:
                if n.value != D_VALUE and n.value != D_PRIME_VALUE:
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

    # def eval_dnodes(self, node): #TODO: DETECT CONFLICT?!
    #     if len(node.dnodes) == 0:
    #         return

    #     if node.dnodes[0].gtype == 'IPT' or node.dnodes[0].gtype == 'BRCH' or node.dnodes[0].gtype == 'BUFF':
    #         for n in node.dnodes:
    #             # if n.value != D_VALUE and n.value != D_PRIME_VALUE:
    #                 n.value = node.value

    #     elif node.dnodes[0].gtype == 'OR':
    #         if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])):# or (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
    #             node.dnodes[0].value = ONE_VALUE

    #     elif node.dnodes[0].gtype == 'NOR':
    #         if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])):# or (D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
    #             node.dnodes[0].value = ZERO_VALUE

    #     elif node.dnodes[0].gtype == 'AND':
    #         if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])):# or (D_VALUE in self.get_unodes_val(node.dnodes[0])):
    #             node.dnodes[0].value = ZERO_VALUE

    #     elif node.dnodes[0].gtype == 'NAND':
    #         if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])):# or (D_VALUE in self.get_unodes_val(node.dnodes[0])):
    #             node.dnodes[0].value = ONE_VALUE

    #     elif node.dnodes[0].gtype == 'XOR' or node.dnodes[0].gtype == 'XNOR':
    #         # flag = True
    #         # for udnode in node.dnodes[0].unodes:
    #         #     if udnode.value not in [ZERO_VALUE, ONE_VALUE]:
    #         #         flag = False
    #         #         break
    #         # if flag:
    #         #     node.dnodes[0].imply()
    #         raise NotImplemented

    #     elif node.dnodes[0].gtype == 'NOT':
    #         if node.dnodes[0].value == ONE_VALUE:
    #             node.dnodes[0].value = ZERO_VALUE
    #         elif node.dnodes[0].value == ZERO_VALUE:
    #             node.dnodes[0].value = ONE_VALUE

    #         # node.dnodes[0].value = D_alg.inverse(node.value)

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
            if node.value == ONE_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'AND':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NAND':
            if node.value == ZERO_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            else:
                res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'XOR' or node.gtype == 'XNOR':
            res = self.set_unodes(node, X_VALUE)

        elif node.gtype == 'NOT':
            res = self.set_unodes(node, D_alg.inverse(node.value))
            # if node.value == ONE_VALUE:
            #     res = self.set_unodes(node, ZERO_VALUE)
            # elif node.value == ZERO_VALUE:
            #     res = self.set_unodes(node, ONE_VALUE)
            # elif node.value == D_VALUE:
            #     res = self.set_unodes(node, ZERO_VALUE)
            # elif node.value == D_PRIME_VALUE:
            #     res = self.set_unodes(node, ONE_VALUE)

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
            if res is False:
                print('______', front.num)
                return res

        return True

    def imply_and_check(self, node):  # optimize get updated nodes.
        """
        Returns: boolean, list
            booleans: the result of check part
            list: list of updated nodes
        """
        initial_values = [n.value for n in self.circuit.nodes_lev]
        self.imply_forward(node, node.value)
        after_values_f = [n.value for n in self.circuit.nodes_lev]

        updated_nodes_f = []
        for i in range(len(self.circuit.nodes_lev)):
            if after_values_f[i] != initial_values[i]:
                updated_nodes_f.append(self.circuit.nodes_lev[i])

        res = self.imply_backward(node, node.value)
        if res == False:
            return False
        after_values_b = [n.value for n in self.circuit.nodes_lev]

        updated_nodes_b = []
        for i in range(len(self.circuit.nodes_lev)):
            if after_values_b[i] != initial_values[i]:
                updated_nodes_b.append(self.circuit.nodes_lev[i])

        for n in updated_nodes_f+updated_nodes_b:
            self.imply_and_check(n)

        final_values = [n.value for n in self.circuit.nodes_lev]
        changed_nodes = []

        for i in range(len(self.circuit.nodes_lev)):
            if initial_values[i] != final_values[i]:
                changed_nodes.append(self.circuit.nodes_lev[i])

        return True, changed_nodes

    def reset_node(self, node):
        node.value = X_VALUE

    def run(self, node, updated_nodes=set()):
        """The exact recursive algorithm"""
        # print('run is called on node', node.num, node.value)
        before_imply = [f'{n.num}:{n.value}' for n in self.circuit.nodes_lev]
        imply_result, new_valued_nodes = self.imply_and_check(node)

        for n in new_valued_nodes:
            updated_nodes.add(n)

        if not imply_result:
            return False
        after_imply = [f'{n.num}:{n.value}' for n in self.circuit.nodes_lev]

        D_frontier = self.get_D_frontier()
        J_frontier = self.get_J_frontier()

        print('BEFORE IMPLY:')
        print(before_imply)
        print('AFTER IMPLY:')
        print(after_imply)
        # print()
        print(f'D: {[n.num for n in D_frontier]}')
        print(f'J: {[n.num for n in J_frontier]}')
        input()

        if not self.error_at_PO():
            if len(D_frontier) == 0:
                return False, updated_nodes

            untried_D = D_frontier.pop()
            print('Chosen D:', untried_D.num)
            while untried_D:
                controlling_value = self.get_controlling_value(untried_D)
                # print('Controlling Value:', controlling_value)
                for k in untried_D.unodes:
                    if k.value == X_VALUE:
                        k.value = D_alg.inverse(controlling_value)
                        print('set', k.num, k.value)
                        updated_nodes.add(k)
                res, updated_nodes = self.run(k, updated_nodes.copy())
                if res:
                    return True, updated_nodes

                if len(D_frontier):
                    untried_D = D_frontier.pop()
                untried_D = None
            return False, updated_nodes

        # error not at PO
        if len(J_frontier) == 0:
            return True, updated_nodes

        untried_J = J_frontier.pop()
        print('Chosen J', untried_J.num)
        c = self.get_controlling_value(untried_J)

        while X_VALUE in [inp.value for inp in untried_J.unodes]:

            j_idx = random.choice([inp for inp in range( len(untried_J.unodes)) if untried_J.unodes[inp].value == X_VALUE])
            untried_J.unodes[j_idx].value = c
            updated_nodes.add(untried_J.unodes[j_idx])
            print('J=', untried_J.unodes[j_idx].num, 'set to', c)
            res, updated_nodes = self.run(
                untried_J.unodes[j_idx], updated_nodes.copy())

            if res:
                return True, updated_nodes

            # REVERSE UPDATED VALUES
            print('Going Back on node', node.num)
            for n in updated_nodes:
                self.reset_node(n)
            untried_J.unodes[j_idx].value = D_alg.inverse(c)

        return False, updated_nodes


if __name__ == '__main__':
    """Remove this main scope later"""

    circuit = Circuit('../../data/ckt/c1.ckt')
    fault = Fault(19, 0)

    dalg = D_alg(circuit, fault)
    res, _ = dalg.run(dalg.faulty_node)
    print('\nIs fault ', fault, 'detectable?', res)
    if res:
        print('Final Test Pattern:')
        print([f'{n.num}:{n.value}' for n in circuit.PI])
