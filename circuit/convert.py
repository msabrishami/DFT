

import pdb
import config
import os

class Converter:
    def __init__(self, ckt):
        path = os.path.join(config.VERILOG_DIR, ckt + ".v")
        gate2node, node2gate = convert_gate_node(path)
        self.gate2node = gate2node
        self.node2gate = node2gate

    def g2n(self, gate):
        return self.gate2node[gate]
    
    def n2g(self, node):
        if "-" in node:
            node=node.split("-")[0]
        return self.node2gate[node]

def convert_gate_node(verilog_path):

    infile = open(verilog_path)
    print(verilog_path)
    
    gate2node = dict()
    node2gate = dict()
    for line in infile:

        # Similar to EPFL circuits
        if (", .ZN(" in line) or (", .Z(" in line):
            words = line.split()
            gate = words[1]
            if ".ZN" in words[-2]:
                node = words[-2].replace(".ZN(", "").replace(")", "")
            elif ".Z" in words[-2]:
                node = words[-2].replace(".Z(", "").replace(")", "")
            gate2node[gate] = node
            node2gate[node] = gate
        
        # Similar to ISCAS85 circuits
        elif (");" in line) and ("(" in line) and not ("module" in line):
            words = line.replace("(", "").replace(")","").replace(",", "").split()
            gate = words[1]
            node = words[2] 
            gate2node[gate] = node
            node2gate[node] = gate
    
    
    return gate2node, node2gate


def convert_opi_gate2node(verilog_path, opi_path, out_path):
    gate2node, node2gate = convert_gate_node(verilog_path)
    infile_op = open(opi_path)
    outfile = open(out_path, "w")
    for line in infile_op:
        words = line.strip().split()
        gate = words[3].split("/")[0]
        node = gate2node[gate]
        temp = "\t".join(words)
        outfile.write(temp + "\t" + node + "\n")

if __name__ == "__main__":
    verilog_path = "../data/EPFL/arbiter_syn.v"
    opi_path = "../data/arbiter_opi_60.txt"
    out_path = "../data/arbiter_opi_60_ready.txt"
    convert_opi_gate2node(verilog_path, opi_path, out_path)


