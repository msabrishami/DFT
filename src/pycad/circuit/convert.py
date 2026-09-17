from pycad import config
import os
import re

from pycad.circuit.circuit_loader import CircuitLoader
from pycad.library import cells as library_cells

read_verilog_syntax = CircuitLoader.read_verilog_syntax

class Converter:
    def __init__(self, ckt, verilog_format):
        assert verilog_format in config.V_FORMATS, \
                "This verilog format ({}) is not supported".format(verilog_format)
        
        self.verilog_format = verilog_format
        path = os.path.join(config.VERILOG_DIR, ckt + ".v")
        self.convert_gate_node(path)

       
        if verilog_format == "EPFL":
            self.gateIO = library_cells.NanGate_15nm() 
        elif verilog_format == "ISCAS85":
            self.gateIO = library_cells.default()


    def g2n(self, gate):
        return self.gate2node[gate]
    
    def n2g(self, node):
        if "-" in node:
            node=node.split("-")[0]
        return self.node2gate[node]

    def nodes2tmax_OP(self, ops, output_fname):
        """ converts a list of nodes in our own format to 
        Synopsys TestMax Observation Point format
        TODO: special case of EPFL""" 
        buff = []
        outfile = open(output_fname, "w")
        for idx, op_node in enumerate(ops):
            buff.append(op_node)
            if len(buff) == 5 or idx==len(ops)-1:
                res = "set_test_point_element { "
                for node in buff:
                    gate = self.node2gate[node]
                    cell = self.gate2cell[gate]
                    outPin = self.gateIO[cell][-1]
                    res += gate + "/" + outPin + " "
                buff = []
                res += " } -type observe"
                outfile.write(res + "\n")
                # print(res)
        
        outfile.close()

    def tmax2nodes_OP(self, tmax_fname):
        """ reads a OP file in tmax format, 
        returns a list of OP nodes """
        mstr = re.compile(r"(?:(?:[A-Z]+\d*\_\d+)|(?:[A-Z]+\d+))\/[A-Z]+")
        op_list= []
        infile = open(tmax_fname)
        lines = infile.readlines()
        for l in lines:
            mlist = re.findall(mstr, l)
            op_list.extend(mlist)
        infile.close()
        return op_list


    def convert_gate_node_OLD(self, path):
        """ for every gate, there are two information:
        1- gate name
        2- node number, which is basically the down-node of gate
        Some applications need the gate name (like TestMax-OPI) some others node name
        both gate name and node number are unique
        This function geenrates and returns 2 dicts: (gat2node, node2gate)
        Bug: cannot read verilog files with gate definition in more than one line
        """
        infile = open(path)
        
        self.gate2node = dict()
        self.node2gate = dict()
        self.gate2cell = dict()
        for line in infile:
                
            # Similar to EPFL circuits
            # if self.verilog_format == "EPFL":
            if (", .ZN(" in line) or (", .Z(" in line):

                words = line.split()
                gate = words[1]
                if ".ZN" in words[-2]:
                    node = words[-2].replace(".ZN(", "").replace(")", "")
                elif ".Z" in words[-2]:
                    node = words[-2].replace(".Z(", "").replace(")", "")
                self.gate2node[gate] = node
                self.node2gate[node] = gate
                self.gate2cell[gate] = words[0]
            
            # Similar to ISCAS85 circuits
            # elif self.verilog_format == "ISCAS85":
            elif (");" in line) and ("(" in line) and not ("module" in line):

                words = line.replace("(", " ").replace(")"," ").replace(",", " ").split()
                gate = words[1]
                node = words[2] 
                self.gate2node[gate] = node
                self.node2gate[node] = gate
                self.gate2cell[gate] = words[0]

    def convert_gate_node(self, path):
        """ for every gate, there are two information:
        1- gate name
        2- node number, which is basically the down-node of gate
        Some applications need the gate name (like TestMax-OPI) some others node name
        both gate name and node number are unique
        This function geenrates and returns 2 dicts: (gat2node, node2gate)
        Bug: cannot read verilog files with gate definition in more than one line
        """
        self.gate2node = dict()
        self.node2gate = dict()
        self.gate2cell = dict()

        infile = open(path)
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
                continue
                        
            line = eff_line + line.rstrip()
            eff_line = ''
            new_lines.append(line)

        infile.close()

        for line in new_lines:
            x_type, _ = read_verilog_syntax(line)
            if x_type != "GATE":
                continue

            line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
            pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3).replace(" ", ""))
            if not pin_format:
                raise ValueError(f"Cannot parse pins in line: {line.strip()}")
            if "Z" not in pin_format[-1][0]:
                raise NameError("Cannot detect the output pin as the last argumet, check code")
            words = line.split()
            gate = words[1]
            node = pin_format[-1][1]
            self.gate2node[gate] = node
            self.node2gate[node] = gate
            self.gate2cell[gate] = words[0]
