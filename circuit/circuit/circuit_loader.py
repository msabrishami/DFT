# -*- coding: utf-8 -*-

import os
import re
import config

from node.node import Node

class CircuitLoader:
    """ Read a circuit netlist (gate level), 
    currently support .ckt (refer to USC EE658) and .v (Verilog) 
    """
    
    def __init__(self, circuit, circuit_fname, std_node_lib):
        """ Read a gate level netlist and feed the Circuit object 

        Parameters
        ----------
        circuit : Circuit 
            A Circuit object that will be be initialized and filled with the given node types
        circuit_name : str
            the name of the circuit netlist file, with path and format
        std_node_lib : dict
            A dictionary of each node type to its class
        """ 

        circuit_name   = circuit_fname.split('/')[-1].split('.')[0]
        circuit_format = circuit_fname.split('/')[-1].split('.')[1]

        if circuit_format == 'ckt':
            self.read_ckt(circuit, circuit_fname, std_node_lib)
        elif circuit_format == 'v':
            self.read_verilog(circuit, circuit_fname, std_node_lib)
        else:
            raise NotImplementedError(f"Circuit format {mode} is not supported!")

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

    def read_verilog(self, circuit, circuit_fname, std_node_lib):
        """
        Read circuit from .v file, each node as an object
        """
        infile = open(circuit_fname, 'r')
        eff_line = ''
        lines = infile.readlines()
        new_lines=[]
        for line in lines:
            # Remove comment in lines 
            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            line = line[:line.index('//')] if line_syntax else line

            # If there is no ";" or "endmodule" it means the line is continued
            # Stack the contniuous lines to each other
            if ';' not in line and 'endmodule' not in line:
                eff_line = eff_line + line.rstrip()
            else:
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
                    new_node = Node.gen_node({'num': pi, 'n_type': "PI", 'g_type': "IPT"}, std_node_lib)
                    circuit.nodes[new_node.num] = new_node
                    circuit.PI.append(new_node)

            # PO: n_type=PO, g_type=unknown, Node will NOT be added
            if x_type == "PO":
                for po in nets:
                    _nodes[po] = {'num': po, 'n_type':"PO", 'g_type': None}

            # GATE, n_type = PO or GATE
            # Node was seen before, in wire or in input/output, node will be added
            if x_type == "GATE":
                gtype, nets = nets
                if nets[0] not in _nodes:
                    pdb.set_trace()
                _nodes[nets[0]]['g_type'] = gtype 
                new_node = Node.gen_node(_nodes[nets[0]], std_node_lib)
                circuit.nodes[new_node.num] = new_node
                if new_node.ntype == 'PO':
                    circuit.PO.append(new_node)

        # 2nd time Parsing: Making All Connections
        for line in new_lines:
            x_type, nets = read_verilog_syntax(line)
            if x_type == "GATE":
                gtype, nets = nets
                for net in nets[1:]:
                    circuit.nodes[nets[0]].unodes.append(circuit.nodes[net])
                    circuit.nodes[net].dnodes.append(circuit.nodes[nets[0]])


        # Branch modification 
        # Inserting FB node back into the circuit
        branches = {}
        for node in circuit.nodes.values():
            if len(node.dnodes) > 1:
                for idx in range(len(node.dnodes)):
                    ## New BNCH
                    branch = Node.gen_node({'num': node.num + '-' + str(idx+1), 
                        'n_type':"FB", 'g_type':"BRCH"}, std_node_lib)
                    branches[branch.num] = branch
                    insert_branch(node, node.dnodes[0], branch)
        circuit.nodes.update(branches)

    def read_ckt(self, circuit, circuit_fname, std_node_lib):
        """
        Read circuit from .ckt file, each node as an object
        """
        infile = open(circuit_fname, 'r')
        lines = infile.readlines()
        circuit.nodes= {}
        # First time over the netlist
        for line in lines:
            if len(line) < 6:
                continue
            # node_info = self.read_node_ckt(circuit, line.strip())
            attr = line.split()
            node_info = dict()
            node_info["n_type"] = Node.ntype(int(attr[0])).name
            node_info["g_type"] = Node.gtype(int(attr[2])).name
            node_info["num"] = attr[1]
            new_node = Node.gen_node(node_info, std_node_lib)
            # new_node.ntype = n_type
            # new_node.gtype = g_type
            if new_node.ntype == "PI":
                circuit.PI.append(new_node)
            elif new_node.ntype == "PO":
                circuit.PO.append(new_node)
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
    raise NameError(f"Cell type {cell_name} was not found")

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
        
        # TODO: Saeed fixed this but was not tested on all circuits
        # It had issues with netlists that have gate description in multiple lines
        # pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3))
        pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3).replace(" ", ""))
        if pin_format:
            #TODO: for now, we considered PO as the last pin
            if "Z" not in pin_format[-1][0]:
                pdb.set_trace()
                raise NameError("Cannot detect the output pin as the last argumet, check code")
            nets = [pin_format[-1][1]]
            for x in pin_format[:-1]:
                nets.append(x[1])
        else:
            # verilog with no pin format
            nets = line_syntax.group(3).replace(' ', '').split(',')

        return ("GATE", (gtype, nets) )
    
    raise NameError(f"No suggestion for \n>{line}<\n was found")