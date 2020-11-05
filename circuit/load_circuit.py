# -*- coding: utf-8 -*-
import os
import re
from circuit import *
from node import *
import config

class LoadCircuit:
    def __init__(self, circuit, mode = 'ckt'):
        self.c_name = circuit.c_name
        if mode == 'ckt':
            self.read_ckt(circuit)
        elif mode == 'v':
            self.read_verilog(circuit)
        else:
            raise NotImplementedError()


    def add_node(self, circuit,  line):
        """ Create a node based on 1 line of ckt file
        does not make the unodes/dnodes connections
        """
        # possible empty lines
        if len(line) < 6:
            return 
        
        attr = line.split()
        n_type = ntype(int(attr[0])).name
        g_type = gtype(int(attr[2])).name
        num = attr[1]
        
        if n_type == "PI" and g_type=="IPT":
            node = IPT(n_type, g_type, num)

        elif n_type == "FB" and g_type=="BRCH":
            node = BRCH(n_type, g_type, num)
        
        elif n_type == "GATE" and g_type=="BRCH":
            raise NotImplementedError()

        elif n_type == "GATE" or n_type == "PO":
            if g_type == 'XOR':
                node = XOR(n_type, g_type, num)

            elif g_type == 'OR':
                node = OR(n_type, g_type, num)

            elif g_type == 'NOR':
                node = NOR(n_type, g_type, num)

            elif g_type == 'NOT':
                node = NOR(n_type, g_type, num)

            elif g_type == 'NAND':
                node = NAND(n_type, g_type, num)

            elif g_type == 'AND':
                node = AND(n_type, g_type, num)

        node.ntype = n_type
        node.gtype = g_type
        if node.ntype == "PI":
            circuit.PI.append(node)

        elif node.ntype == "PO":
            circuit.PO.append(node)
        return node 
    

    def connect_node(self, circuit,  line):
        # As we move forward, find the upnodes and connects them
        
        attr = line.split()
        ptr = circuit.nodes[attr[1]]
        
        # ntype=PI and gtype=IPT: good
        # we don't care about #fan-out
        if ptr.ntype == "PI" and ptr.gtype=="IPT":
            None
        
        # ntype=FB and gtyep=BRCH
        elif ptr.ntype == "FB" and ptr.gtype=="BRCH":
            unode = circuit.nodes[attr[3]]
            ptr.unodes.append(unode)
            unode.dnodes.append(ptr)
        
        # ntype=GATE and gtype=BRCH
        elif ptr.ntype == "GATE" and ptr.gtype=="BRCH":
            print("ERROR: gate and branch", ptr.num)

        # ntype=GATE or ntype=PO 
        # we don't care about #fan-out
        # some gates have a single input, they are buffer
        elif ptr.ntype == "GATE" or ptr.ntype == "PO":
            for unode_num in attr[5:]:
                unode = circuit.nodes[unode_num]
                ptr.unodes.append(unode)
                unode.dnodes.append(ptr)
        else:
            print("ERROR: not known!", ptr.num)

    
    ## Inputs: Verilog gate input formats
    ## Outputs: gtype corresponding gate name
    def gtype_translator(self, gate_type):
        if gate_type == 'ipt':
            return gtype(0).name
        elif gate_type == 'xor':
            return gtype(2).name
        elif gate_type == 'or':
            return gtype(3).name
        elif gate_type == 'nor':
            return gtype(4).name
        elif gate_type == 'not':
            return gtype(5).name
        elif gate_type == 'nand':
            return gtype(6).name
        elif gate_type == 'and':
            return gtype(7).name
        ## new node type
        elif gate_type == 'xnor':
            return gtype(8).name
        elif gate_type == 'buf':
            return gtype(9).name


    ## This function is used for inserting the BRCH node
    ## u_node and d_node are connected originally
    ## i_node is the node be inserted between u_node and d_node
    def insert_node(self, u_node, d_node, i_node):
        u_node.dnodes.remove(d_node)
        u_node.dnodes.append(i_node)
        d_node.unodes.remove(u_node)
        d_node.unodes.append(i_node)
        i_node.unodes.append(u_node)
        i_node.dnodes.append(d_node)

    ## According to the Dict, this function will return the specific node
    ## It is similar to part of add_node()
    def node_generation(self, Dict):
        if Dict['n_type'] == "PI" and Dict['g_type'] == "IPT":
            node = IPT(Dict['n_type'], Dict['g_type'], Dict['num'])

        elif Dict['n_type'] == "FB" and Dict['g_type'] == "BRCH":
            node = BRCH(Dict['n_type'], Dict['g_type'], Dict['num'])

        elif Dict['n_type'] == "GATE" and Dict['g_type'] == "BRCH":
            raise NotImplementedError()

        elif Dict['n_type'] == "GATE" or Dict['n_type'] == "PO":
            if Dict['g_type'] == 'XOR':
                node = XOR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'OR':
                node = OR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NOR':
                node = NOR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NOT':
                node = NOR(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NAND':
                node = NAND(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'AND':
                node = AND(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'BUFF':
                node = BUFF(Dict['n_type'], Dict['g_type'], Dict['num'])
            #TODO
            # elif Dict['g_type'] == 'XNOR':
            #     node = XNOR(Dict['n_type'], Dict['g_type'], Dict['num'])
        else:
            raise NotImplementedError()
        return node


    def read_verilog(self, circuit):
        """
        Read circuit from .v file, each node as an object
        """
        path = os.path.join(config.VERILOG_DIR, self.c_name + '.v')

        ## Read the file and Deal with comment and ; issues
        infile = open(path, 'r')
        eff_line = ''
        lines = infile.readlines()
        new_lines=[]
        for line in lines:
            # eliminate comment first
            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            if line_syntax:
                line = line[:line.index('//')]

            # considering ';' issues
            if ';' not in line and 'endmodule' not in line:
                eff_line = eff_line + line.rstrip()
                continue
            line = eff_line + line.rstrip()
            eff_line = ''
            new_lines.append(line)
        infile.close()

        ## 1st time Parsing: Creating all nodes
        # Because the ntype and gtype information are separate, we need to use Dict to collect all information
        # Key: num
        # Value: num, ntype and gtype
        Dict = {}
        for line in new_lines:
            if line != "":
                # Wire
                line_syntax = re.match(r'^[\s]*wire (.*,*);', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(1).replace(' ', '').replace('\t', '').split(','):
                        Dict[n] = {'num': n, 'n_type': 'GATE', 'g_type':None}

                # PI: n_type = 0 g_type = 0
                line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                        new_node = self.node_generation({'num': n, 'n_type': 'PI', 'g_type': 'IPT'})
                        circuit.nodes[new_node.num] = new_node
                        circuit.PI.append(new_node)

                # PO n_type = 3 but g_type has an issue
                line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                        Dict[n] = {'num': n, 'n_type': 'PO', 'g_type': None}

                # Gate reading and Making Connection of nodes
                line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
                if line_syntax:
                    if line_syntax.group(1) == 'module':
                        continue

                    # detect if gate is introduced with or without pin IDs.
                    # e.g. AND2_X1 C1031 ( .A1(a_0_), .A2(b_0_), .Z(n389) );
                    # regex for detecting paranthesis inside the paranthesis
                    input_pattern = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3))
                    if input_pattern != []:
                        for set in input_pattern:
                            print(set)
                            pdb.set_trace()

                            # set[0] --> A1, A2, Z
                            # set[1] --> a_0_, b_0_, n389
                        # TODO: Acquire the input/output order of the gate and create the nodes

                    else:
                        node_order = line_syntax.group(3).replace(' ', '').split(',')
                        # Nodes Generation
                        Dict[node_order[0]]['g_type'] = self.gtype_translator(line_syntax.group(1))
                        new_node = self.node_generation(Dict[node_order[0]])
                        circuit.nodes[new_node.num] = new_node
                        if new_node.ntype == 'PO':
                            circuit.PO.append(new_node)

        # 2nd time Parsing: Making All Connections
        # we have to change this part according to the input/output order of the gate
        for line in new_lines:
            if line != "":
                line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
                if line_syntax:
                    if line_syntax.group(1) != 'module':
                        node_order = line_syntax.group(3).replace(' ', '').split(',')
                        for i in range(1, len(node_order)):
                            # Making connections
                            circuit.nodes[node_order[0]].unodes.append(circuit.nodes[node_order[i]])
                            circuit.nodes[node_order[i]].dnodes.append(circuit.nodes[node_order[0]])

        ###### Branch Generation ######
        # The basic way is looking for those nodes with more-than-1 fan-out nodes
        # Creating a new FB node
        # Inserting FB node back into the circuit
        # We cannot change the dictionary size while in its for loop,
        # so we create a new dictionary and integrate it back to nodes at the end
        B_Dict = {}
        for node in circuit.nodes.values():
            if len(node.dnodes) > 1:
                for index in range(len(node.dnodes)):
                    ## New BNCH
                    FB_node = self.node_generation({'num': node.num + '-' + str(index+1), 'n_type':'FB', 'g_type':'BRCH'})
                    B_Dict[FB_node.num] = FB_node
                    circuit.insert_node(node, node.dnodes[0], FB_node)
        circuit.nodes.update(B_Dict)

    def read_ckt(self, circuit):
        """
        Read circuit from .ckt file, each node as an object
        """
        path = os.path.join(config.CKT_DIR, self.c_name + '.ckt')
        infile = open(path, 'r')
        lines = infile.readlines()
        circuit.nodes= {}
        # First time over the netlist
        for line in lines:
            new_node = self.add_node(circuit, line.strip())
            circuit.nodes[new_node.num] = new_node
            
        for line in lines:
            self.connect_node(circuit, line.strip())
        


try:
    circuit = Circuit('c17')
    #LoadCircuit(circuit)
    LoadCircuit(circuit, mode= 'v')
    circuit.lev()
    print(circuit)

except IOError:
    print("error in the code")
