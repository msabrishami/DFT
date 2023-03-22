# input file type : .bench
# output file type : .ckt658
import re
import sys
import pdb

class Nets:
    def __init__(self):
        self.gtype = None
        self.ntype = None
        self.output = None
        self.fanouts = []
        self.fanins = []
        self.ntypes = {"GATE":0, "PI":1, "FB":2, "PO":3}
        self.gtypes = {"XOR":2, 'XOR':2, 'NOR':4, 'OR':3, 
                'NOT':5, 'NAND':6, 'AND':7}
    def __str__(self):
        print(f"{self.ntype}\t{self.output}")

class Stem(Nets):
    def __init__(self, brch, stem, net_number):
        """ brch and stem are Gate type """
        super().__init__()
        self.ntype = "FB"
        self.gtype = 1
        self.fanins = [brch]
        self.fanouts = [stem]
        self.output = net_number

    def ckt_line(self):
        line = f"2 {self.output} 1 {self.fanins[0].output}"
        return line

class Gate(Nets):
    def __init__(self, line):
        super().__init__()
        self.fanouts = []
        self.fanins = []
        self.inputs = []

        if line.lower().startswith("input("):
            self.ntype = "PI"
            self.gtype = 0
            self.output = line[:-1].split('(')[-1]

        elif '=' in line:
            words = re.split(r',|=|\(|\)', line.replace(')', ''))
            self.ntype = "GATE"
            self.gtype = self.gtypes[words[1]]
            self.output = words[0]
            self.inputs = words[2:]

    def ckt_line(self):
        if self.ntype == "PI":
            line = f"1 {self.output} 0 {len(self.fanouts)} 0"
        elif self.ntype in ["GATE", "PO"]:
            line = f"{self.ntypes[self.ntype]} "
            line += f"{self.output} {self.gtype} {len(self.fanouts)} "
            line += f"{len(self.fanins)} "
            line += " ".join([x.output for x in self.fanins])
        return line 
    

def new_net(gates):
    nets = set([int(gate.output) for gate in gates.values()])
    for net in range(1, max(nets)):
        if net not in nets:
            return net

def read_bench(bench_fname):
    with open(bench_fname, "r") as infile:
        lines = infile.readlines()
    lines = [line.strip().replace(' ','') for line in lines if len(line) > 3]
    lines = [line for line in lines if line[0] != '#']

    lines_po = [line for line in lines if line.startswith("OUTPUT")]
    lines_pi = [line for line in lines if line.startswith("INPUT")]
    POs = set([line[:-1].split('(')[-1] for line in lines_po])
    PIs = set([line[:-1].split('(')[-1] for line in lines_pi])

    gates = dict()
    for line in lines:
        if '=' in line or "INPUT" in line:
            new_gate = Gate(line)
            gates[new_gate.output] = new_gate
    
    # setting the data structure
    for output, gate in gates.items():
        for inline in gate.inputs:
            gates[inline].fanouts.append(gate)
            gate.fanins.append(gates[inline])

    # Sanity checks
    for po in POs:
        # Checking if PO net is not shared with another gate
        if po in gates:
            if len(gates[po].fanouts) > 1:
                print(f"(ERROR): PO {po} is also a branch")
                pdb.set_trace()
            else:
                gates[po].ntype = "PO"
        # Checking if PO net is also PI net
        elif po in PIs:
            print(f"(ERROR): PO {po} is also a PI")
        # PO should be something! 
        else:
            print(f"(ERROR): PO {po} is also a PI")

    FB_gates = [gate for gate in gates.values() if len(gate.fanouts) > 1]
    for gate in FB_gates: 
        if len(gate.fanouts) > 1:
            # Branch! We need to create stems
            for stem in gate.fanouts:
                new_stem = Stem(gate, stem, new_net(gates))
                gates[new_stem.output] = new_stem

    return gates    


def write_ckt(ckt_fname):
    with open(ckt_fname, 'w') as outfile:
        for gate in gates.values():
            outfile.write(gate.ckt_line() + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("(ERROR) bench and ckt file names should be given as arguments")
        exit()
    gates = read_bench(sys.argv[1])
    write_ckt(sys.argv[2])

