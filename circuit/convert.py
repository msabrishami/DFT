

import pdb


def convert_gate_node(verilog_path):

    infile = open(verilog_path)
    
    gate2node = dict()
    node2gate = dict()
    for line in infile:
        if (", .ZN(" in line) or (", .Z(" in line):
            words = line.split()
            gate = words[1]
            if ".ZN" in words[-2]:
                node = words[-2].replace(".ZN(", "").replace(")", "")
            elif ".Z" in words[-2]:
                node = words[-2].replace(".Z(", "").replace(")", "")
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


