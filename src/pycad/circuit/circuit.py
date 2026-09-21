import random
import warnings
from collections import deque

import networkx as nx

from pycad.circuit.circuit_loader import CircuitLoader
from pycad.config import X_VALUE
from pycad.node import node

#TODO: we need a flag to make sure no new nodes are added to the circuit, 
#           for example, we all cell types in method foo after loading the circuit, 
#           after adding new nodes, results of foo may still not be valid. 

class Circuit:
    """ Representing a digital logic circuit, capable of doing logic simulation.  

        Attributes
        ---------
        STD_NODE_LIB : dict
            dictionary of node type to related node class
        c_fname : str
            circuit name, full with path and format
        c_name : str
            circuit name, without path or format
        nodes : list
            list of nodes objects-->Wrong
            dict of node.num to object of node
        input_num_list : list
            list of PI node numbers
        nodes_cnt : 
            total number of nodes in the circuit
        nodes_lev : list
            list of all nodes, ordered by level
        """
    
    STD_NODE_LIB = {'AND':node.AND, 
                    'XOR':node.XOR,
                    'OR': node.OR, 
                    'XNOR':node.XNOR,
                    'BUFF':node.BUFF,
                    'BRCH':node.BRCH,
                    'NOR':node.NOR,
                    'NOT':node.NOT,
                    'NAND':node.NAND,
                    'IPT':node.IPT}


    def __init__(self, c_fname, std_node_lib=STD_NODE_LIB):
        """ 
        Attributes 
        ----------
        c_fname : str
            the name of the circuit with path and format
        c_name : str
            the full name of the circuit without path and format 
        nodes : dict
            from each node_num to Node object
        nodes_lev: list
            nodes ordered by level. Ready for logicsim.
        PI : list
            list of intput nodes
        PO : list
            list of output nodes
        """

        self.c_fname = c_fname 
        self.c_name = c_fname.split('/')[-1].split('.')[0]
        self.nodes = {}
        self.nodes_lev = []
        self.inputs = []  # primary input nodes, in netlist order
        self.outputs = []  # primary output nodes, in netlist order
        
        self._load(c_fname, std_node_lib)
        self.levelize()

    def _load(self, netlist_fname, std_node_lib):
        CircuitLoader(self, netlist_fname, std_node_lib)

    def levelize(self):
        """Assign a level to every node and order ``nodes_lev`` by level.

        Inputs are at level 0 and every other node is one level above its
        highest fan-in. Fan-out branches count as gates: the level of a branch
        is the level of its stem plus one. Levels of all nodes are recomputed,
        so this can be called again after the circuit was modified.

        Raises
        ------
        ValueError
            If the circuit has a combinational loop.
        """
        pending = {}  # node -> number of fan-ins whose level is still unknown
        ready = deque()
        for node in self.nodes.values():
            node.lev = None
            pending[node] = len(node.unodes)
            if not node.unodes:
                if node.gtype != "IPT":
                    warnings.warn(f"Node {node.num} has no fan-in, its level is set to zero")
                node.lev = 0
                ready.append(node)

        while ready:
            node = ready.popleft()
            for dnode in node.dnodes:
                pending[dnode] -= 1
                if pending[dnode] == 0:
                    dnode.lev = max(unode.lev for unode in dnode.unodes) + 1
                    ready.append(dnode)

        unleveled = [node.num for node in self.nodes.values() if node.lev is None]
        if unleveled:
            raise ValueError(f"The circuit has a combinational loop through nodes {unleveled[:5]}")

        self.nodes_lev = sorted(self.nodes.values(), key=lambda x: x.lev)

    def levelize_backward(self):
        """ Calculate shortest distace from node to POs for all nodes
            using Dijktra algorithm """
        #TODO: test it

        dist = {} 
        MAX_WEIGHT = 10**9
        nodes = list(self.nodes.values()) + self.outputs + self.inputs #~

        for node in nodes:
            dist[node] = MAX_WEIGHT
            
        unvisited_nodes = []
        for po in self.outputs:
            dist[po] = min(0,dist[po])
            unvisited_nodes.append(po)
            
        while unvisited_nodes:
            for node in unvisited_nodes:
                for unode in node.unodes:
                    dist[unode] = min(1+dist[node],dist[unode])
                    unvisited_nodes.append(unode)
                unvisited_nodes.remove(node)
            
        return dist

    def __str__(self):
        res = ["Circuit name: " + self.c_name]
        res.append("#Nodes: " + str(len(self.nodes)))
        res.append("#PI: " + str(len(self.inputs)) + " >> ") 
        res.append("\t" + str([x.num for x in self.inputs]))
        res.append("#PO: " + str(len(self.outputs)) + " >> ")
        res.append("\t" + str([x.num for x in self.outputs]))

        for node in self.nodes_lev:
            res.append(str(node))
        return "\n".join(res)

    def get_rand_nodes(self, count=1):
        if count > len(self.nodes):
            print("Error: count should be less than count of total nodes")
            return None

        return random.choices(self.nodes_lev,k=count)
    
    def print_fanin(self, target_node, depth):
        # TODO: needs to be checked and tested -- maybe using utils.get_fanin?
        from collections import deque
        queue = deque()
        queue.append(target_node)
        min_level = max(0, target_node.lev - depth) 
        self.print_fanin_rec(queue, min_level)

    def print_fanin_rec(self, queue, min_level):
        # TODO: needs to be checked and tested -- maybe using utils.get_fanin?
        """ prints the nodes in the fanin cone 
        first time it is called, queue should be a list with target node as its only element
        this is a simple BFS in the opposite direction of lines
        
        Arguments:
        ----------
        queue : list
            a list of nodes, representing our queue for BFS
        depth : int 
            search depth for BFS, final node to be printed has depth=zero
        """

        print("queue is: " + ",".join([node.num for node in queue]))
        if len(queue) == 0:
            return 
        
        target_node = queue.popleft()
        print(target_node)
        
        if target_node.lev == min_level:
            return 
        
        for node in target_node.unodes:
            print(f"added node {node.num} to the queue")
            queue.append(node)
            
        self.print_fanin_rec(queue, min_level)

    def logic_sim(self, tp):
        """
        Logic simulation:
        Read a given pattern and perform the logic simulation
        Currently just works with binary logic
        tp is a list of values (currently int) in the same order as in self.inputs

        Return
        ------
        list of output values
        """
        if X_VALUE in tp:
            raise Exception('You have X in test pattern. Use logic_sim_t() instead.')
        
        node_dict = dict(zip([x.num for x in self.inputs], tp))

        for node in self.nodes_lev:
            if node.gtype == "IPT":
                node.imply(node_dict[node.num])
            else:
                node.imply()
        
        return [po.value for po in self.outputs]
    
    def logic_sim_t(self, tp):
        """
        Logic simulation:
        Read a given pattern and perform the logic simulation
        Currently just works with binary logic
        tp is a list of values (currently int) in the same order as in self.inputs

        Return
        ------
        list of output values
        """

        node_dict = dict(zip([x.num for x in self.inputs], tp))

        for node in self.nodes_lev:
            if node.gtype == "IPT":
                node.imply_t(node_dict[node.num])
            else:
                node.imply_t()
        
        return [po.value for po in self.outputs]

    def logic_sim_bitwise(self, tp, fault=None):
        """
        Logic simulation bitwise mode:
        Reads a given pattern and perform the logic simulation bitwise

        Arguments
        ---------
        tp : list of int 
            input pattern in the same order as in self.inputs
        fault : Fault
            node.num@fault --> example: N43@0 means node N43 single stuck at zero 
        
        Return
        ------
        list of output values
        """

        node_dict = dict(zip([x.num for x in self.inputs], tp))
    
        if fault:
            for node in self.nodes_lev:
                if node.gtype == "IPT":
                    node.imply_b(node_dict[node.num])
                else:
                    node.imply_b()
                if node.num == fault.node_num:
                    if fault.stuck_val == '0':
                        node.value = 0
                    else:
                        node.value = node.bitwise_not

        else:
            for node in self.nodes_lev:
                if node.gtype == "IPT":
                    node.imply_b(node_dict[node.num])
                else:
                    node.imply_b()

        return [po.value for po in self.outputs]
        
    def logic_sim_file(self, in_fname, out_fname, stil=False): 
        #TODO: test
        """
        logic simulation with given input vectors from a file
        - generate an output folder in ../data/modelsim/circuit_name/ directory
        - read an input file in the input folder
        - generate a output file in output folder by using logic_sim() function
        """
        # Saeed needs to rewrite this method using 'yield' in load_tp_file     
        fr = open(in_fname, mode='r')
        fw = open(out_fname, mode='w')
        fw.write('Inputs: ')
        fw.write(",".join(['N'+str(node.num) for node in self.inputs]) + "\n")
        fw.write('Outputs: ')
        fw.write(",".join(['N'+str(node.num) for node in self.outputs]) + "\n")
        temp = fr.readline()
        i=1
        for line in fr.readlines():
            line=line.rstrip('\n')
            line_split=line.split(',')
            for x in range(len(line_split)):
                line_split[x]=int(line_split[x])
            self.logic_sim(line_split)
            fw.write('Test # = '+str(i)+'\n')
            fw.write(line+'\n')
            fw.write(",".join([str(node.value) for node in self.outputs]) + "\n")
            i+=1
        fw.close()
        fr.close()
        
        if stil:
            infile = open(in_fname, "r")
            lines = infile.readlines()
            outfile = open(out_fname, "w")
            outfile.write("PI:")
            outfile.write(",".join([node.num for node in self.inputs]) + "\n")
            outfile.write("PO:")
            outfile.write(",".join([node.num for node in self.outputs]) + "\n")
            for idx, line in enumerate(lines[1:]):
                tp=line.rstrip('\n').split(",")
                # for x in range(len(line_split)):
                #    line_split[x]=int(line_split[x])
                # self.logic_sim(line_split)
                self.logic_sim(tp)
                outfile.write("\"pattern " + str(idx) + "\": Call \"capture\" {\n")
                outfile.write("\"_pi\"=")
                outfile.write("".join(line.strip().split(",")))
                outfile.write(";\n")
                outfile.write("      \"_po\"=")
                for node in self.outputs:
                    val = "H" if node.value==1 else "L"
                    outfile.write(val)
                outfile.write("; } \n")
            outfile.close()

    def golden_test(self, golden_io_filename):
        # compares the results of logic-sim of this circuit, 
        #  ... provided a golden input/output file
        # Saeed: this needs to be tested by myself later
        infile = open(golden_io_filename, "r")
        lines = infile.readlines()
        PI_t_order  = [x[1:] for x in lines[0][8:].strip().split(',')]
        PO_t_order = [x[1:] for x in lines[1][8:].strip().split(',')]
        print(PI_t_order)
        PI_num = [x.num for x in self.inputs]
        print(PI_num)
        print(f"Logic-Sim validation with {int((len(lines)-2)/3)} patterns")
        if PI_t_order != PI_num:
            print("Error: PI node order does not match! ")
            return False
        for t in range(int((len(lines)-2)/3)):
            test_in  = [int(x) for x in lines[(t+1)*3].strip().split(',')]
            test_out = [int(x) for x in lines[(t+1)*3+1].strip().split(',')]
            self.logic_sim(test_in)
            logic_out = self.read_outputs()
            for i in range(len(PO_t_order)):
                out_node = PO_t_order[i]
                out_node_golden = test_out[i]
                if out_node_golden != logic_out["out"+str(out_node)]:
                    print("Error: PO node order does not match! ")
                    return False
        print("Validation completed successfully - all correct")
        return True
    
    def make_num_int(self):
        node2int = dict()
        for idx, node in enumerate(self.nodes_lev):
            node2int[node.num] = idx
        return node2int

    def gen_graph(self):
        """
        Generate directed graph of the circuit 
        Each node has attributes: lev
        """
        G = nx.DiGraph()
        for n in self.nodes_lev:
            n_num_normal = n.num
            G.add_node(n_num_normal)
            G.nodes[n_num_normal]['lev'] = n.lev
            G.nodes[n_num_normal]['gtype'] = n.gtype
            G.nodes[n_num_normal]['ntype'] = n.ntype
            if n.gtype != 'IPT':
                for unode in n.unodes:
                    G.add_edge(unode.num, n_num_normal)
            else:
                pass
        return G

    def get_node_attr(self, node_attr):
        data = []
        for node in self.nodes_lev:
            data.append(getattr(node, node_attr))

        return data
  
    def make_PO(self, target):
        """ connects this target node to a PO using a branch 
        """
        if target.ntype == "PO":
            return 
        # target becomes stem, create new branches:
        new_brch = node.BRCH("PO", "BRCH", target.num+"-IPO") 
        old_brch = node.BRCH("FB", "BRCH", target.num+"-OLD")

        # fixing unodes for new branches
        new_brch.unodes.append(target)
        old_brch.unodes.append(target)
        old_brch.dnodes = target.dnodes
        
        # fixing unodes for target.dnodes
        # if target was stem:
        if len(target.dnodes) > 1:
            for dnode in target.dnodes:
                dnode.unodes = [old_brch]
        # if target was a gate
        else:
            new_unodes = []
            for unode in target.dnodes[0].unodes:
                if unode.num != target.num:
                    new_unodes.append(unode)
            new_unodes.append(old_brch)
            target.dnodes[0].unodes = new_unodes

        self.outputs.append(new_brch)    
        self.nodes[new_brch.num] = new_brch

    def read_outputs(self):
        """ Read the values of POs in a dictionary.
        The key to the dictionary is the PO node and value is the value of node
        """ 
        res = {}
        for node in self.outputs:
            res[str(node.num)] = node.value
        return res
