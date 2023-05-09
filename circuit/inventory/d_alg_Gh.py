# TODO: which D_frontier is better
# TODO: which J_frontier is better

import sys
sys.path.append('../')

import typing
from collections import deque
from circuit.dft_circuit import DFTCircuit
from fault_simulation.fault import Fault, FaultList
from fault_simulation.ppsf import PPSF
from node.dft_node import DFTNode

ONE_VALUE = 1
ZERO_VALUE = 0
D_VALUE = "D"
D_PRIME_VALUE = "~D"
X_VALUE = "X"

PRINT_LOG = False


class D_alg():
    def __init__(self, circuit: DFTCircuit, fault: Fault) -> None:
        self.circuit = circuit
        # set all nodes values to X
        for n in self.circuit.nodes_lev:
            self.reset_node(n)

        # set the faulty node to D or D'
        for n in self.circuit.nodes_lev:
            if n.num == fault.node_num:
                self.faulty_node = n
                if fault.stuck_val == "1" or fault.stuck_val == ONE_VALUE:
                    n.value = D_PRIME_VALUE
                elif fault.stuck_val == "0" or fault.stuck_val == ZERO_VALUE:
                    n.value = D_VALUE
                break

        self.x_inputs = {}
        if PRINT_LOG: print(f'D-Algorithm initialized with fault {fault.__str__()} in circuit {circuit.c_name}.\n')

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
        flag1 = False
        for p in self.circuit.PO:
            if p.value == D_VALUE or p.value == D_PRIME_VALUE:
                flag1 = True
                break
        # flag2= False
        # for p in self.circuit.PO:
        #     if p.value == X_VALUE:
        #         flag2 = True

        return flag1

    def get_controlling_value(self, node):
        if node.gtype == 'AND' or node.gtype == 'NAND':
            return ZERO_VALUE
        elif node.gtype == 'OR' or node.gtype == 'NOR':
            return ONE_VALUE
        elif node.gtype == 'XOR' or node.gtype == 'XNOR': #only for use in J section.
            return ONE_VALUE
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

            elif (u.value == X_VALUE):
                if (value == ZERO_VALUE or value == ONE_VALUE):
                    u.value = value
            elif u.value != value and value != X_VALUE:
                return False

        return True

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
            old_value = node.dnodes[0].value
        
        if len(node.dnodes) == 0:
            return True
        
        elif node.dnodes[0].gtype == 'BUFF' or node.dnodes[0].gtype == 'BRCH':
            for n in node.dnodes:
                if n.value not in [D_VALUE, D_PRIME_VALUE]:
                    n.value = node.value

        elif node.dnodes[0].gtype == 'OR': #what if all zero and D_PRIME / zero and D_VALUE
            if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_VALUE in self.get_unodes_val(node.dnodes[0]) and D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                    node.dnodes[0].value = ONE_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ZERO_VALUE):
                    node.dnodes[0].value = ZERO_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_VALUE):
                    node.dnodes[0].value = D_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_PRIME_VALUE):
                    node.dnodes[0].value = D_PRIME_VALUE

        elif node.dnodes[0].gtype == 'NOR': 
            if (ONE_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_VALUE in self.get_unodes_val(node.dnodes[0]) and D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                    node.dnodes[0].value = ZERO_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ZERO_VALUE):
                    node.dnodes[0].value = ONE_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_VALUE):
                    node.dnodes[0].value = D_PRIME_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_PRIME_VALUE):
                    node.dnodes[0].value = D_VALUE

        elif node.dnodes[0].gtype == 'AND':#what if all one and D_Prime / one and D-value
            if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_VALUE in self.get_unodes_val(node.dnodes[0]) and D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ZERO_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ONE_VALUE):
                    node.dnodes[0].value = ONE_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_VALUE):
                    node.dnodes[0].value = D_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_PRIME_VALUE):
                    node.dnodes[0].value = D_PRIME_VALUE
                elif ONE_VALUE in self.get_unodes_val(node.dnodes[0]):
                    if D_VALUE in self.get_unodes_val(node.dnodes[0]):
                        node.dnodes[0].value = D_VALUE
                    elif D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0]):
                        node.dnodes[0].value = D_PRIME_VALUE

        elif node.dnodes[0].gtype == 'NAND':
            if (ZERO_VALUE in self.get_unodes_val(node.dnodes[0])) or (D_VALUE in self.get_unodes_val(node.dnodes[0]) and D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0])):
                node.dnodes[0].value = ONE_VALUE
            elif X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if self.if_all(node.dnodes[0].unodes, ONE_VALUE):
                    node.dnodes[0].value = ZERO_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_VALUE):
                    node.dnodes[0].value = D_PRIME_VALUE
                elif self.if_all(node.dnodes[0].unodes, D_PRIME_VALUE):
                    node.dnodes[0].value = D_VALUE
                elif ONE_VALUE in self.get_unodes_val(node.dnodes[0]):
                    if D_VALUE in self.get_unodes_val(node.dnodes[0]):
                        node.dnodes[0].value = D_PRIME_VALUE
                    elif D_PRIME_VALUE in self.get_unodes_val(node.dnodes[0]):
                        node.dnodes[0].value = D_VALUE
                
        elif node.dnodes[0].gtype == 'XNOR':
            if X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if len(node.dnodes[0].unodes) == 2:
                    a = node.dnodes[0].unodes[0].value
                    b = node.dnodes[0].unodes[1].value

                    if (a in [ONE_VALUE, ZERO_VALUE]) and (b in [ONE_VALUE, ZERO_VALUE]):
                        node.dnodes[0].value = (1+a+b)%2
                    elif a == D_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = D_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                    elif a == D_PRIME_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = D_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                    elif a==ONE_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = D_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                    elif a==ZERO_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = D_VALUE
                else:
                    raise Exception('Not Implemented')
            
        elif node.dnodes[0].gtype == 'XOR':
            if X_VALUE not in self.get_unodes_val(node.dnodes[0]):
                if len(node.dnodes[0].unodes) == 2:
                    a = node.dnodes[0].unodes[0].value
                    b = node.dnodes[0].unodes[1].value

                    if (a in [ONE_VALUE, ZERO_VALUE]) and (b in [ONE_VALUE, ZERO_VALUE]):
                        node.dnodes[0].value = (1+a+b)%2
                    elif a == D_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = D_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                    elif a == D_PRIME_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = D_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                    elif a==ZERO_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = D_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                    elif a==ONE_VALUE:
                        if b == ZERO_VALUE:
                            node.dnodes[0].value = ONE_VALUE
                        elif b == ONE_VALUE:
                            node.dnodes[0].value = ZERO_VALUE
                        elif b == D_VALUE:
                            node.dnodes[0].value = D_PRIME_VALUE
                        elif b == D_PRIME_VALUE:
                            node.dnodes[0].value = D_VALUE

                else:
                    raise Exception('Not Implemented')

        elif node.dnodes[0].gtype == 'NOT':
            if node.value != X_VALUE:
                node.dnodes[0].value = D_alg.inverse(node.value)

        if one_output:
            new_value = node.dnodes[0].value
            if old_value == D_VALUE:
                if new_value == ZERO_VALUE or new_value == D_PRIME_VALUE:
                    node.dnodes[0].value = old_value
                    return False
                node.dnodes[0].value = D_VALUE

            elif old_value == D_PRIME_VALUE:
                if new_value == ONE_VALUE or new_value == D_VALUE:
                    node.dnodes[0].value = old_value
                    return False
                node.dnodes[0].value = D_PRIME_VALUE
            
            elif old_value == ONE_VALUE or old_value == ZERO_VALUE:
                if old_value!=new_value:
                    node.dnodes[0].value = old_value
                    return False
                
        return True
        
    def eval_unodes(self, node):
        res = True

        if node.gtype == 'BRCH' or node.gtype == 'BUFF':
            if node.value == D_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
            elif node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            else:
                res = self.set_unodes(node, node.value)

        elif node.gtype == 'OR':
            if node.value == ZERO_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)

        elif node.gtype == 'NOR':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)

        elif node.gtype == 'AND':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ONE_VALUE)

        elif node.gtype == 'NAND':
            if node.value == ZERO_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ONE_VALUE)

        elif node.gtype == 'NOT':
            if node.value == ONE_VALUE or node.value == D_VALUE:
                res = self.set_unodes(node, ZERO_VALUE)
            elif node.value == ZERO_VALUE or node.value == D_PRIME_VALUE:
                res = self.set_unodes(node, ONE_VALUE)
                
        return res

    def imply_forward(self, node, value) -> bool: # only run on updated ones
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
                if PRINT_LOG: print(f'CONFLICT ON DNODES ',front.num, front.value)
                return res

        return True

    def imply_backward(self, node, value) -> bool: # only run on updated ones
        # print('\nBackward Implication is called on ', node.num, value,'\n')
        node.value = value
        q = deque()
        q.append(node)
        while q:
            # print(f'q={[n.num for n in q]}')
            front = q.popleft()
            res = self.eval_unodes(front)
            for unode in front.unodes:
                if unode not in q:
                    q.append(unode)
            if res is False:
                # print(f'evaluating unodes of {front.num}:{front.value} -> {self.get_unodes_val(front)}')
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
        if res is False: #repeated code here
            if PRINT_LOG: print('Backward Conflict on unodes of', node.num)

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

    def propagate_error(self, node) -> set:
        if PRINT_LOG: print('propagate called on ', node.num)
        n = node.unodes[0]
        
        if n.dnodes[0].value != X_VALUE:
            return
        
        if n.dnodes[0].gtype == 'OR' or n.dnodes[0].gtype == 'AND':
            if D_VALUE in self.get_unodes_val(n.dnodes[0]):
                    n.dnodes[0].value = D_VALUE
            elif D_PRIME_VALUE in self.get_unodes_val(n.dnodes[0]):
                n.dnodes[0].value = D_PRIME_VALUE

        elif n.dnodes[0].gtype == 'NAND' or n.dnodes[0].gtype == 'NOR':
            if D_PRIME_VALUE in self.get_unodes_val(node):
                n.dnodes[0].value = D_VALUE
            elif D_VALUE in self.get_unodes_val(node):
                n.dnodes[0].value = D_PRIME_VALUE

        elif n.dnodes[0].gtype == 'XOR':
            if len(n.dnodes[0].unodes) > 2:
                raise Exception('Not Implemented')
            if D_VALUE in self.get_unodes_val(n.dnodes[0]):
                if ONE_VALUE in self.get_unodes_val(n.dnodes[0]):
                    n.dnodes[0].value = D_PRIME_VALUE
                else:
                    n.dnodes[0].value = D_VALUE
            if D_PRIME_VALUE in self.get_unodes_val(n.dnodes[0]):
                if ONE_VALUE in self.get_unodes_val(n.dnodes[0]):
                    n.dnodes[0].value = D_VALUE
                else:
                    n.dnodes[0].value = D_PRIME_VALUE

        elif n.dnodes[0].gtype == 'XNOR':
            if len(n.dnodes[0].unodes) > 2:
                raise Exception('Not Implemented')
            if D_VALUE in self.get_unodes_val(n.dnodes[0]):
                if ONE_VALUE in self.get_unodes_val(n.dnodes[0]):
                    n.dnodes[0].value = D_VALUE
                else:
                    n.dnodes[0].value = D_PRIME_VALUE
            if D_PRIME_VALUE in self.get_unodes_val(n.dnodes[0]):
                if ONE_VALUE in self.get_unodes_val(n.dnodes[0]):
                    n.dnodes[0].value = D_PRIME_VALUE
                else:
                    n.dnodes[0].value = D_VALUE
                
    def reset_node(self, node):
        if isinstance(node, DFTNode):
            node.value = X_VALUE
        else:
            for n in self.circuit.nodes_lev:
                if n.num == node:
                    n.value = X_VALUE
                    return

    def get_J_index(self, untried_J):
        L=[inp for inp in range(len(untried_J.unodes)) if untried_J.unodes[inp].value == X_VALUE]
        return L[-1]

    def get_X_inputs(self, D_node) -> list:
        x = []
        for u in D_node.unodes:
            if u.value == X_VALUE:
                x.append(u)
        return x

    def get_inp_plus_one(self, tp) -> typing.Tuple[bool, list]:
        if PRINT_LOG: print('Plus one called')
        i = len(tp)-1
        success = False
        while i>=0:
            if tp[i] == ZERO_VALUE:
                tp[i] = ONE_VALUE
                success = True
                break
            else:
                tp[i] = ZERO_VALUE
                i-=1
                if i == -1:
                    success = False
                    print('***********No more tps')
                    break

        return success, tp
    
    def set_X_inputs_values(self, D_node) -> bool:
        """
        if there exist no next input values, return False
        """
        if D_node.num not in self.x_inputs.keys():
            self.x_inputs[D_node.num] = self.get_X_inputs(D_node)
            
        xs = self.x_inputs[D_node.num]
        current_inp = [n.value for n in xs]
        if PRINT_LOG: print(f'{current_inp=}')
        if X_VALUE in current_inp:
            for n in xs:
                n.value = ZERO_VALUE
            return True
        else:
            current_inp = []
            for n in xs:
                current_inp.append(n.value)
            succ, next_tp = self.get_inp_plus_one(current_inp)
            if PRINT_LOG: print('Next TP for the chosen X node: ', next_tp)
            if succ:
                for i in range(len(xs)):
                    xs[i].value = next_tp[i]
                return True
            return False
        
    def run(self, node,  J_updated_nodes=set(), save_J_node = False, save_D_node=False, D_updated_nodes=set(), X_updated_nodes=set(), save_X_node=False):
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
                J_updated_nodes.add(n.num)
        if save_D_node:
            for n in new_valued_nodes:
                D_updated_nodes.add(n.num)
        if save_X_node:
            for n in new_valued_nodes:
                X_updated_nodes.add(n.num)

        if PRINT_LOG:
            print('AFTER IMPLY:')
            print(after_imply)
            print()

            input()
        
        if not imply_result:
            return False, J_updated_nodes, D_updated_nodes, X_updated_nodes

        ### RUN_D() ###
        D_frontier = self.get_D_frontier()
        J_frontier = self.get_J_frontier()

        if PRINT_LOG:
            print(f'D: {[n.num for n in D_frontier]}')
            print(f'J: {[n.num for n in J_frontier]}')


        if not self.error_at_PO():
            tried_Ds = set()

            if len(D_frontier) == 0:
                return False, J_updated_nodes, D_updated_nodes, X_updated_nodes

            untried_D = D_frontier.pop()
            while untried_D.num in tried_Ds:
                if len(D_frontier):
                    untried_D = D_frontier.pop()
                else:
                    untried_D = None

                    return False, J_updated_nodes, D_updated_nodes, X_updated_nodes
            
            if untried_D and (untried_D.num not in tried_Ds):

                tried_Ds.add(untried_D.num)
            else:
                untried_D = None

            if PRINT_LOG: print('Chosen D:', untried_D.num)
                        
            while untried_D:
                save_D_node=True

                if save_J_node:
                    J_updated_nodes.add(untried_D.num)
                if save_D_node:
                    D_updated_nodes.add(untried_D.num)

                is_X_node = True if untried_D.gtype in ['XOR', 'XNOR'] else False
                X_finished = False
                
                updated_unodes = set()

                if not is_X_node:
                    self.propagate_error(untried_D)
                    controlling_value = self.get_controlling_value(untried_D)

                    for k in untried_D.unodes:
                        if k.value == X_VALUE:
                            k.value = D_alg.inverse(controlling_value)

                            if PRINT_LOG: (f'{k.num} is set to {k.value}')
                            if save_J_node:
                                J_updated_nodes.add(k.num)
                            if save_D_node:
                                D_updated_nodes.add(k.num)
                            if save_X_node:
                                X_updated_nodes.add(k.num)
                            updated_unodes.add(k.num)
                else:
                    save_X_node = True
                    self.propagate_error(untried_D)
                    success = self.set_X_inputs_values(untried_D)

                    if success: # the algorithm is continued
                        untried_D.value = X_VALUE
                        self.eval_dnodes(untried_D.unodes[0])
                        if PRINT_LOG: print(f'selected X as D: {untried_D.num}, its inputs{[u.value for u in untried_D.unodes]}')
                        for u in untried_D.unodes:
                            if u in self.x_inputs[untried_D.num]:
                                if save_J_node:
                                    J_updated_nodes.add(u.num)
                                if save_D_node:
                                    D_updated_nodes.add(u.num)
                                updated_unodes.add(u.num)

                    else: #no more tp possible
                        if PRINT_LOG: print('(no more tp possible) X reset:', [n.num for n in self.x_inputs[untried_D.num]])
                        for n in self.x_inputs[untried_D.num]:
                            if n not in untried_D.unodes:
                                self.reset_node(n)
                        X_finished = True

                new_set = set([untried_D.num])
                if len(untried_D.dnodes) and (untried_D.dnodes[0].value in [D_VALUE, D_PRIME_VALUE]):
                    for d in untried_D.dnodes:
                        new_set.add(d.num)
                for u in updated_unodes:
                    new_set.add(u)
                
                res, new_updated_j, new_updated_d, new_updated_x = self.run(untried_D, 
                                                            J_updated_nodes=J_updated_nodes.copy(), save_J_node=True,
                                                            D_updated_nodes=new_set, save_D_node=True,
                                                            X_updated_nodes=set(), save_X_node=True)
                
                if save_J_node:
                    for n in new_updated_j:
                        J_updated_nodes.add(n)
                if save_D_node:
                    for n in new_updated_d:
                        D_updated_nodes.add(n)
                if save_X_node:
                    for n in new_updated_x:
                        X_updated_nodes.add(n)

                if res:
                    return True, J_updated_nodes, D_updated_nodes, X_updated_nodes

                if is_X_node:
                    if PRINT_LOG: print('Xs to be reset:', [x.num for x in new_updated_x])
                    for x in new_updated_x:
                        self.reset_node(x)
                    if not X_finished:
                        continue
                    else:
                        if PRINT_LOG: print('Also reset:', untried_D.num, [u.num for u in untried_D.unodes])
                        self.reset_node(untried_D)
                        for u in untried_D.unodes:
                            self.reset_node(u)
                        return False, J_updated_nodes, D_updated_nodes, X_updated_nodes
                        
                if PRINT_LOG: print('Reversing from last D:', untried_D.num,[n for n in new_updated_d])
                for n in new_updated_d:
                    self.reset_node(n)
                
                D_frontier = self.get_D_frontier()
                if len(D_frontier):
                    untried_D = D_frontier.pop()
                    while untried_D.num in tried_Ds:
                        if len(D_frontier):
                            untried_D = D_frontier.pop()
                        else:
                            untried_D = None
                            break
                else:
                    untried_D = None
                    break                

                if untried_D and (untried_D.num not in tried_Ds):
                    tried_Ds.add(untried_D.num)
                    if PRINT_LOG and untried_D: print('Chosen D-2:', untried_D.num)
            
            return False, J_updated_nodes, D_updated_nodes, X_updated_nodes

        ### RUN_J() ###

        # error at PO
        J_frontier = self.get_J_frontier()
        # tested_Js = set()

        if len(J_frontier) == 0:
            return True, J_updated_nodes, D_updated_nodes, X_updated_nodes

        if PRINT_LOG: print('Go back to run on ',node.num)        

        untried_J = J_frontier.pop()
        # while untried_J.num in tested_Js:
        #     if len(J_frontier):
        #         untried_J = J_frontier.pop()
        #     else:
        #         untried_J = None
            
        # if untried_J:
        #     tested_Js.add(untried_J.num)
        # else:
        #     return True, J_updated_nodes, D_updated_nodes, X_updated_nodes
            # raise Exception('What happens next?')

        if PRINT_LOG: print('Chosen J', untried_J.num)
        c = self.get_controlling_value(untried_J)

        save_J_node=True

        while X_VALUE in [inp.value for inp in untried_J.unodes]:
            J_frontier = self.get_J_frontier()
            j_idx = self.get_J_index(untried_J)
            untried_J.unodes[j_idx].value = c

            # if save_J_node:
                # J_updated_nodes.add(untried_J.unodes[j_idx].num)
            # if save_D_node:
                # D_updated_nodes.add(untried_J.unodes[j_idx].num)
            if PRINT_LOG: print(f'set {untried_J.unodes[j_idx].num} to {c}.')
            if save_X_node:
                X_updated_nodes.add(untried_J.unodes[j_idx].num)
            res, new_updated_j, new_updated_d, new_updated_x = self.run(untried_J.unodes[j_idx],  
                                                                        J_updated_nodes=set([untried_J.unodes[j_idx].num]),save_J_node=True,
                                                                        D_updated_nodes=set(), save_D_node=True)
            
            if save_J_node:
                for n in new_updated_j:
                    J_updated_nodes.add(n)
            if save_D_node:
                for n in new_updated_d:
                    D_updated_nodes.add(n)
            if save_X_node:
                for n in new_updated_x:
                    X_updated_nodes.add(n)
            
            if res:
                return True, J_updated_nodes, D_updated_nodes, X_updated_nodes

            if PRINT_LOG: print('Going Back on node J', untried_J.unodes[j_idx].num, ', be reset nodes:', [n for n in new_updated_j])
            
            for n in new_updated_j:
                self.reset_node(n)
                J_updated_nodes.remove(n)
            
            untried_J.unodes[j_idx].value = D_alg.inverse(c)

            
            if PRINT_LOG: print('set inverse controlling value of', untried_J.unodes[j_idx].num, untried_J.unodes[j_idx].value)

            res, new_j, new_d, new_x= self.run(untried_J.unodes[j_idx],J_updated_nodes= J_updated_nodes.copy(), save_J_node=True,
                                                                    D_updated_nodes=D_updated_nodes.copy(), save_D_node=True, 
                                                                    X_updated_nodes=X_updated_nodes.copy(), save_X_node=save_X_node)

            if res:
                if save_J_node:
                    for n in new_j:
                        J_updated_nodes.add(n)
                if save_D_node:
                    for n in new_d:
                        D_updated_nodes.add(n)
                if save_X_node:
                    for n in new_x:
                        X_updated_nodes.add(n)

                J_frontier = self.get_J_frontier()
                if len(J_frontier):
                    untried_J = J_frontier.pop()
                else:
                    untried_J = None
                    return True, J_updated_nodes, D_updated_nodes, X_updated_nodes
            else:
                if PRINT_LOG: print('\nreversing from latest chosen D:', [n for n in new_d])

                for n in new_d:
                    self.reset_node(n)
                    if n in D_updated_nodes:
                        D_updated_nodes.remove(n)
                return False, J_updated_nodes, D_updated_nodes, X_updated_nodes
            
        return False, J_updated_nodes, D_updated_nodes, X_updated_nodes

    def get_final_tp(self):
        tp = []
        for n in circuit.PI:
            if n.value == D_PRIME_VALUE:
                tp.append(ZERO_VALUE)
            elif n.value == D_VALUE:
                tp.append(ONE_VALUE)
            else:
                tp.append(n.value)
        return tp

def gen_all_tps(tp: list):
    """If len(X) is less than 6, generates all tps. Else, generates all for 6 Xs and set others randomly."""
    SUBS_X_COUNT = 6
    x_count = tp.count(X_VALUE)

    if x_count > SUBS_X_COUNT:
        x_indexes = [i for i in range(len(tp)) if tp[i] == X_VALUE]
        import random
        random_x_indices = random.choices(x_indexes,k=x_count-SUBS_X_COUNT)
        for i in random_x_indices:
            tp[i] = random.randint(0,1)

    from collections import deque

    all_tps = deque()
    all_tps.append(tp)

    while True:
        front_tp = all_tps.popleft()
        if not X_VALUE in front_tp:
            all_tps.append(front_tp)
            break
        
        first_x = None
        for t in range(len(front_tp)):
            if front_tp[t] == X_VALUE:
                first_x = t
                break
        
        #substitute zero and one
        if first_x is not None:
            tp_copy = front_tp.copy()
            tp_copy[first_x] = '1'
            all_tps.append(tp_copy)

            front_tp[first_x] = '0'
            all_tps.append(front_tp)
    
    return list(all_tps)

def gen_random_tp(tp):
    ans = []
    for t in tp:
        if t != X_VALUE:
            ans.append(t)
        else:
            import random
            str(ans.append(random.randint(0,1)))
    return [ans]

def check_answer(given_tp, circuit, fault_str):
    """
    mode:
        calculate: check answer using PPSF
    """
   
    passed = True
    answer_result = given_tp
    fault_list = FaultList(circuit)
    fault_list.add_str(fault_str)
    ppsf = PPSF(circuit, faults=fault_list)
    if len(answer_result)>1:
        answer_result = answer_result[1]
        stu_tp = given_tp

        all_stu_tps = gen_all_tps(stu_tp)
        if len(all_stu_tps) > 32:
            import random
            all_stu_tps = random.sample(all_stu_tps, 20)
        
        for st_tp in all_stu_tps:
            tp = [int(t) for t in st_tp]
            fd_dict = ppsf.run(tps=[tp])
            if fault_str not in fd_dict.keys():
                passed = False
                if True:
                    print(f'tp {tp} does not detect {fault_str}.')

    return passed


if __name__ == '__main__':
    """Remove this main scope later"""

    ckt = 'c4.ckt'
    # type = 'large'
    type = 'mini'

    circuit = DFTCircuit(f'../../data/ckt/{ckt}')
    good_faults = FaultList(circuit)
    if type == 'large':
        good_faults.add_file(f'./good_faults/{ckt.replace(".ckt","")}_good_faults.txt')
    elif type == 'mini':
        good_faults.add_all()
    
    # PRINT_LOG = True
    # for n in circuit.nodes_lev:
    #     for sv in [ZERO_VALUE, ONE_VALUE]:
    # if True:
    for fault in good_faults.faults:
        # fault = Fault(f.node_num), int(f.stuck_val))
        # fault = Fault(16, 1)
        # fault = Fault(n.num, sv)
        circuit = DFTCircuit(f'../../data/ckt/{ckt}')
        dalg = D_alg(circuit, fault)

        res, *_= dalg.run(dalg.faulty_node)
        
        print('\nIs fault ', fault, 'detectable?', res)
        
        if res:
            print('Detector Test Pattern:')
            print(dalg.get_final_tp())
        if res:
            print(check_answer(dalg.get_final_tp(), circuit, fault.__str__()))
        
        del dalg
        del circuit
        input()