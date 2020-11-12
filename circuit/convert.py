

import pdb
import config
import os
import re
import sys
sys.path.insert(1, config.LIB_CELLS_PATH)
import library_cells

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

    def nodes2tmax_OP_file(self, ops, output_fname):
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
                print(res)
        
        outfile.close()


    def convert_gate_node(self, path):
        """ for every gate, there are two information:
        1- gate name
        2- node number, which is basically the down-node of gate
        Some applications need the gate name (like TestMax-OPI) some others node name
        both gate name and node number are unique
        This function geenrates and returns 2 dicts: (gat2node, node2gate)
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
                words = line.replace("(", "").replace(")","").replace(",", "").split()
                gate = words[1]
                node = words[2] 
                self.gate2node[gate] = node
                self.node2gate[node] = gate
                self.gate2cell[gate] = words[0]


def convert_opi_gate2node(verilog_path, opi_path, out_path):
    """ given a path to a file with OPI gates, converts them to nodes
    not unique to OPIs, can be any points or general gates
    """
    gate2node, node2gate = convert_gate_node(verilog_path)
    infile_op = open(opi_path)
    outfile = open(out_path, "w")
    for line in infile_op:
        words = line.strip().split()
        gate = words[3].split("/")[0]
        node = gate2node[gate]
        temp = "\t".join(words)
        outfile.write(temp + "\t" + node + "\n")


def add_op_verilog(path_in, op,  
        verilog_version,
        path_out=None, 
        new_buff="RESEARCHBUFF", 
        new_po="RESEARCHPO"):
    """ reads the verilog file in path_in
    converts this netlist to a netlist with inserting op as observation point
    connects a buffer called new_buff  with node called new_po
    stores the new verilog file in path_out
    does NOT check if op is already a PO
    TODO: we could detect ourselves if this is EPFL or ISCAS by syntax!
    Note: this function changes the top module name!
    """
    if verilog_version not in ["ISCAS85", "EPFL"]:
        raise NameError("Verilog version {} not supported".format(verilog_version))

    lines = read_verilog_lines(path_in)

    c0 = lines[0].startswith("module") 
    c1 = lines[1].strip().startswith("input")
    c2 = lines[2].strip().startswith("output")
    c3 = lines[3].strip().startswith("wire")
    c4 = lines[-1].strip().startswith("endmodule")
    if not (c0 and c1 and c2 and c3 and c4):
        raise NameError("Cannot read this verilog file!")
    
    if verilog_version == "EPFL":
        new_module_name = "top"
        path_out = path_in.split("/")[-1][:-2]+"_OP_"+op+".v" if path_out==None else path_out
        # buff buff-name (output, input)
        lines[-1] = "BUF_X1 {} ( .I({}) , .Z({}) );".format(new_buff, op, new_po) 
    
    elif verilog_version == "ISCAS85":
        new_module_name = lines[0].split()[1] + "_OP_" + op
        # BUFF_X1 buff-name (.I (input-name), .Z(output-name))
        path_out = new_module_name + ".v" if path_out==None else path_out 
        lines[-1] = "buf {} ({},{});".format(new_buff, new_po, op)

    # add op-node to module
    lines[0] = lines[0].replace(lines[0].split()[1], new_module_name)
    ptr = lines[0].find(");")
    lines[0] = lines[0][0:ptr] + "," + new_po + ");"

    # add op-node to output
    ptr = lines[2].find(";")
    lines[2] = lines[2][0:ptr] + "," + new_po + ";"

    lines.append("endmodule")
    # print("\n".join(lines))
    
    outfile = open(path_out, "w")
    outfile.write("\n".join(lines))
    outfile.close()
    print("output file saved as {}".format(path_out))


def read_verilog_lines(path):
    """ reads a verilog file and returs the lines as a list
    removes comments, and endlines """ 
    infile = open(path)
    lines = infile.readlines()
    eff_line = ''
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
    return new_lines





if __name__ == "__main__":
    verilog_path = "../data/EPFL/arbiter_syn.v"
    opi_path = "../data/arbiter_opi_60.txt"
    out_path = "../data/arbiter_opi_60_ready.txt"
    convert_opi_gate2node(verilog_path, opi_path, out_path)


