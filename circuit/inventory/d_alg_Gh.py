#TODO: conflicts in check()
#TODO: xor/xnor

from collections import deque

ONE_VALUE = 1
ZERO_VALUE = 0
D_VALUE = 2
D_PRIME_VALUE = 3
X_VALUE = 4

class D_alg():
    def __init__(self, circuit) -> None:
        self.circuit = circuit
        self.D_frontier = deque() #when append? in imply and check? or after it
        self.J_frontier = deque() #when append? in imply and check? or after it
        self.valued_nodes = []

        for n in self.circuit.nodes_lev:
            self.reset_node(n)

    def error_at_PO(self):
        for p in self.circuit.PO:
            if p.value == D_VALUE or p.value == D_PRIME_VALUE:
                return True
        return False

    def get_untried_from_D_frontier(self):
        if len(self.D_frontier):
            return self.D_frontier.pop()
        return None

    def get_controlling_value(self, node):
        if node.gtype == 'AND' or node.gtype == 'NAND':
            return ZERO_VALUE
        elif node.gtype == 'OR' or node.gtype == 'NOR':
            return ONE_VALUE
        elif node.gtype =='XOR' or node.gtype == 'XNOR':
            raise Exception("Not yet!")
        #what about NOT, brch, buff
    
    def get_from_J_frontrier(self): #re-check
        for j in self.J_frontier:
            if j.value == X_VALUE:
                return j
        return None

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

    def get_X_input_line(self, node):
        for u in node.unodes:
            if u.value == X_VALUE:
                return u
        return None
    
    def set_unodes(seld, n, value):
        for u in n.unodes:
            if (u.value == 0 and value == 1) or (u.value == 1 and value == 0):
                print('Conflict!')
            elif (u.value == 'X' or u.value == None or u.value == '_') and (value == 0 or value == 1):
                u.value = value
            elif (u.value == 0 or u.value == 1) and (value == 'X' or value == 'None'):
                pass


    def eval_dnodes(self, node):
        if len(node.dnodes) == 0:
            return
        
        if node.dnodes[0].gtype == 'IPT' or node.dnodes[0].gtype == 'BRCH' or node.dnodes[0].gtype == 'BUFF':
            for n in node.dnodes:
                n.value = node.value

        elif node.dnodes[0].gtype == 'OR':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == ONE_VALUE:
                    node.dnodes[0].value = ONE_VALUE
                    break

        elif node.dnodes[0].gtype == 'AND':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == ZERO_VALUE:
                    node.dnodes[0].value = ZERO_VALUE
                    break

        elif node.dnodes[0].gtype == 'NOR':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == ONE_VALUE:
                    node.dnodes[0].value = ZERO_VALUE
                    break

        elif node.dnodes[0].gtype == 'NAND':
            for udnode in node.dnodes[0].unodes:
                if udnode.value == ZERO_VALUE:
                    node.dnodes[0].value = ONE_VALUE
                    break
        
        elif node.dnodes[0].gtype == 'XOR' or node.dnodes[0].gtype == 'XNOR':
            flag = True
            for udnode in node.dnodes[0].unodes:
                if udnode.value not in [ZERO_VALUE, ONE_VALUE]:
                    flag = False
                    break
            if flag:
                node.dnodes[0].imply()

        elif node.dnodes[0].gtype == 'NOT':
            if node.value == ONE_VALUE:
                node.dnodes[0].value = ZERO_VALUE
            elif node.value == ZERO_VALUE:
                node.dnodes[0].value = ONE_VALUE
            elif node.value == D_VALUE:
                node.dnodes[0].value = D_PRIME_VALUE
            elif node.value == D_PRIME_VALUE:
                node.dnodes[0].value = D_VALUE
    
    def eval_unodes(self, node): #ADD D/D'
        if node.gtype == 'IPT' or node.gtype == 'BRCH' or node.gtype == 'BUFF':
            self.set_unodes(node, node.value)
        elif node.gtype == 'OR':
            if node.value == ZERO_VALUE:
                self.set_unodes(node, ZERO_VALUE)
            else:
                self.set_unodes(node, X_VALUE)
        elif node.gtype == 'AND':
            if node.value == ONE_VALUE:
                self.set_unodes(node, ONE_VALUE)
            else:
                self.set_unodes(node, X_VALUE)
        elif node.gtype == 'NOR':
            if node.value == ONE_VALUE:
                self.set_unodes(node, ZERO_VALUE)
            else:
                self.set_unodes(node, X_VALUE)
        elif node.gtype == 'NAND':
            if node.value == ZERO_VALUE:
                self.set_unodes(node, ONE_VALUE)
            else:
                self.set_unodes(node, X_VALUE)
        elif node.gtype == 'XOR' or node.gtype == 'XNOR':
            self.set_unodes(node, X_VALUE)
        elif node.gtype == 'NOT':
            if node.value == ONE_VALUE:
                self.set_unodes(node, ZERO_VALUE)
            elif node.value == ZERO_VALUE:
                self.set_unodes(node, ONE_VALUE)
            else:
                self.set_unodes(node, X_VALUE)

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
            self.eval_unodes(front)
            for unode in front.unodes:
                if unode not in q:
                    q.append(unode)

    def imply_and_check(self, node):
        before_values = [n.value for n in self.nodes_lev]
        self.imply_forward(node, node.value)
        after_values_f = [n.value for n in self.nodes_lev]

        updated_nodes_f = []
        for i in range(len(self.nodes_lev)):
            if after_values_f[i] != before_values[i]:
                updated_nodes_f.append(self.nodes_lev[i])

        self.imply_backward(node, node.value)
        after_values_b = [n.value for n in self.nodes_lev]

        updated_nodes_b = []
        for i in range(len(self.nodes_lev)):
            if after_values_b[i] != before_values[i]:
                updated_nodes_b.append(self.nodes_lev[i])
        
        for n in updated_nodes_f+updated_nodes_b:
            self.imply_and_check_v2(n)

    def reset_node(self, node):
        node.value = X_VALUE
    
    def run(self):
        """The exact recursive algorithm"""
        if not self.imply_and_check():
            return False

        if self.error_at_PO():
            if len(self.D_frontier) == 0:
                return False
            
            untried_D = self.get_untried_from_D_frontier()
            while untried_D:
                controlling_value = self.get_controlling_value(untried_D)
                for k in untried_D:
                    if k.value == X_VALUE:
                        k.value = self.inverse(controlling_value)
                if self.run():
                    return True
            return False

        if len(self.J_frontier) == 0:
            return True

        untried_J = self.get_from_J_frontrier()
        c = self.get_controlling_value(untried_J)
        
        j = self.get_X_input_line(untried_J)
        while j:
            j.value = c
            if self.run():
                return True
            j.value = self.inverse(c)

        return False