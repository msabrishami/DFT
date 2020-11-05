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
            raise NotImplementedError("Circuit format {} is not supported!".format(mode))


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

    
    def add_node_v(self, Dict):
        
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
                node = NOT(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'NAND':
                node = NAND(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'AND':
                node = AND(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'BUFF':
                node = BUFF(Dict['n_type'], Dict['g_type'], Dict['num'])

            elif Dict['g_type'] == 'XNOR':
                node = XNOR(Dict['n_type'], Dict['g_type'], Dict['num'])
        else:
            raise NotImplementedError()
        
        return node


    def read_verilog(self, circuit):
        """
        Read circuit from .v file, each node as an object
        """
        path = os.path.join(config.VERILOG_DIR, "{}.v".format(self.c_name))
        infile = open(path, 'r')
        eff_line = ''
        lines = infile.readlines()
        new_lines=[]
        
        for line in lines:
            if line == "":
                continue

            # Remove comment in lines 
            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            line = line[:line.index('//')] if line_syntax else line

            # If there is no ";" or "endmodule" it means the line is continued
            # Stack the contniuous lines to each other
            if ';' not in line or 'endmodule' not in line:
                eff_line = eff_line + line.rstrip()
                continue
                        
            line = eff_line + line.rstrip()
            eff_line = ''
            new_lines.append(line)

        infile.close()

        ## 1st time Parsing: Creating all nodes
        # we need to use _nodes dict to collect all information
        _nodes = {}
        for line in new_lines:

            x_type, nets = read_verilog_syntax(line)

            if x_type == "module":
                continue
             
            # Wire: n_type=GATE, gtype=unknown
            if x_type == "wire":
                for wire in nets:
                    _nodes[wire] = {'num':wire, 'n_type':"GATE", 'g_type':None}

            # PI: n_type=PI, g_type=IPT, Node will be added! 
            if x_type == "PI":
                for pi in nets:
                    new_node = self.add_node_v({'num': pi, 'n_type': "PI", 'g_type': "IPT"})
                    self.nodes[new_node.num] = new_node
                    self.PI.append(new_node)

            # PO: n_type=PO, g_type=unknown, Node will NOT be added
            if x_type == "PO":
                for po in nets:
                    _nodes[po] = {'num': po, 'n_type':"PO", 'g_type': None}

            # GATE, n_type = PO or GATE
            # Node was seen before, in wire or in input/output, node will be added
            if x_type == "GATE":
                gtype, nets = nets
                _nodes[nets[0]]['g_type'] = gtype 
                new_node = self.add_node_v(_nodes[nets[0]])
                self.nodes[new_node.num] = new_node
                if new_node.ntype == 'PO':
                    self.PO.append(new_node)

        # 2nd time Parsing: Making All Connections
        for line in new_lines:
            x_type, nets = read_verilog_syntax(line)
            if x_type == "GATE":
                gtype, nets = nets
                for net in nets[1:]:
                    self.nodes[nets[0]].unodes.append(self.nodes[net])
                    self.nodes[net].dnodes.append(self.nodes[nets[0]])


        # Branch modification 
        # Inserting FB node back into the circuit
        branches = {}
        for node in self.nodes.values():
            if len(node.dnodes) > 1:
                for idx, dnode in enumerate(node.dnodes):
                    ## New BNCH
                    branch = self.add_node_v({'num': node.num + '-' + str(idx+1), 
                        'n_type':"FB", 'g_type':"BRCH"})
                    branches[branch.num] = branch
                    insert_branch(node, node.dnodes[0], branch)
        self.nodes.update(branches)

        print("Loading verilog file is done")


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
        

def verilog_version_gate(line):
    return {"gate type":"gate", "input-list":[], "output-list":[]}


def cell2gate(cell_name):
    ## Inputs: Verilog gate input formats
    ## Outputs: gtype corresponding gate name
    for gname, cell_names in config.CELL_NAMES.items():
        if cell_name in cell_names:
            return gname
    raise NameError("Cell type {} was not found".format(cell_name))


def insert_branch(u_node, d_node, i_node):
    """ This function is used for inserting the BRCH node
    u_node and d_node are connected originally
    i_node is the node be inserted between u_node and d_node """ 
    u_node.dnodes.remove(d_node)
    u_node.dnodes.append(i_node)
    d_node.unodes.remove(u_node)
    d_node.unodes.append(i_node)
    i_node.unodes.append(u_node)
    i_node.dnodes.append(d_node)


def read_verilog_syntax(line):
    
    
    if line.strip() == "endmodule":
        return ("module", None)

    # If there is a "wire" in this line:
    line_syntax = re.match(r'^[\s]*wire (.*,*);', line, re.IGNORECASE)
    if line_syntax:
        nets = line_syntax.group(1).replace(' ', '').replace('\t', '').split(',')
        return ("wire", nets)
     
    # PI: 
    line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
    if line_syntax:
        nets = line_syntax.group(2).replace(' ', '').replace('\t', '').split(',')
        return ("PI", nets)
    
    # PO 
    line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
    if line_syntax:
        nets = line_syntax.group(2).replace(' ', '').replace('\t', '').split(',')
        return ("PO", nets)

    # Gate
    line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
    if line_syntax:
        if line_syntax.group(1) == "module":
            return ("module", None)
        
        gtype = cell2gate(line_syntax.group(1))
        #we may not use gname for now. 
        gname = line_syntax.group(2)

        pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3))
        if pin_format:
            #TODO: for now, we considered PO as the last pin
            if "Z" not in pin_format[-1][0]:
                raise NameError("Order of pins in verilog does not match")
            nets = [pin_format[-1][1]]
            for x in pin_format[:-1]:
                nets.append(x[1])
        else:
            # verilog with no pin format
            nets = line_syntax.group(3).replace(' ', '').split(',')

        return ("GATE", (gtype, nets) )
    
    raise NameError("No suggestion for \n>{}<\n was found".format(line))



try:
    circuit = Circuit('c17')
    #LoadCircuit(circuit)
    LoadCircuit(circuit, mode= 'v')
    circuit.lev()
    print(circuit)


except IOError:
    print("error in the code")



