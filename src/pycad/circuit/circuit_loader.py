"""Reading gate-level netlists (``.ckt`` and Verilog) into a :class:`Circuit`."""
import os
import re

from pycad import config
from pycad.node.node import GateType, Node, NodeType


class CircuitLoader:
    """Read a gate-level netlist and fill a Circuit with node objects.

    Supported formats are ``.ckt`` (the format of USC EE658, see ``docs``) and
    structural Verilog (``.v``). Creating the loader performs the reading.

    Parameters
    ----------
    circuit : Circuit
        The circuit to fill. Its ``nodes``, ``inputs`` and ``outputs`` are set.
    circuit_fname : str
        Netlist file name, with path and format.
    std_node_lib : dict
        Gate type name -> node class (see ``Circuit.STD_NODE_LIB``).
    """

    def __init__(self, circuit, circuit_fname, std_node_lib):
        circuit_format = os.path.splitext(circuit_fname)[1].lstrip(".")

        if circuit_format == 'ckt':
            self.read_ckt(circuit, circuit_fname, std_node_lib)
        elif circuit_format == 'v':
            self.read_verilog(circuit, circuit_fname, std_node_lib)
        else:
            raise NotImplementedError(f"Circuit format {circuit_format} is not supported!")

    @staticmethod
    def connect_node(circuit, line):
        """Connect the node described by a ``.ckt`` line to its fan-in nodes."""
        attr = line.split()
        ptr = circuit.nodes[attr[1]]

        if ptr.gtype == "IPT":
            # primary input (possibly also a primary output): nothing drives it
            return
        if ptr.ntype == "FB" and ptr.gtype == "BRCH":
            # fan-out branch: the single fan-in is the stem
            unode_nums = attr[3:4]
        elif ptr.ntype in ("GATE", "PO") and ptr.gtype != "BRCH":
            # gates with a single input behave as buffers
            unode_nums = attr[5:]
        else:
            raise ValueError(
                f"Node {ptr.num} has an inconsistent node type {ptr.ntype} and gate type {ptr.gtype}")

        for unode_num in unode_nums:
            unode = circuit.nodes[unode_num]
            ptr.unodes.append(unode)
            unode.dnodes.append(ptr)

    @staticmethod
    def _read_verilog_statements(circuit_fname):
        """Verilog statements of a file: comments removed, continued lines joined."""
        statements = []
        pending = ''
        with open(circuit_fname) as infile:
            for line in infile:
                line = line.split('//')[0]
                # without ";" or "endmodule" the statement continues on the next line
                if ';' not in line and 'endmodule' not in line:
                    pending += line.rstrip()
                else:
                    statements.append(pending + line.rstrip())
                    pending = ''
        return statements

    def read_verilog(self, circuit, circuit_fname, std_node_lib):
        """Read a structural Verilog netlist, each net as a node object.

        Nets driven by a gate become nodes of that gate type, and a fan-out
        branch node is inserted on every net that drives more than one gate.
        """
        statements = self._read_verilog_statements(circuit_fname)

        # 1st pass: create all nodes. Wires and outputs are only declared here,
        # their gate type is known when the gate that drives them is read.
        declared = {}
        for statement in statements:
            x_type, nets = self.read_verilog_syntax(statement)

            if x_type == "wire":
                for wire in nets:
                    declared[wire] = {'num': wire, 'n_type': "GATE", 'g_type': None}

            elif x_type == "PI":
                for pi in nets:
                    new_node = Node.gen_node(
                        {'num': pi, 'n_type': "PI", 'g_type': "IPT"}, std_node_lib)
                    circuit.nodes[new_node.num] = new_node
                    circuit.inputs.append(new_node)

            elif x_type == "PO":
                for po in nets:
                    declared[po] = {'num': po, 'n_type': "PO", 'g_type': None}

            elif x_type == "GATE":
                gtype, nets = nets
                if nets[0] not in declared:
                    raise ValueError(f"Net {nets[0]} is used by a gate but was never declared")
                declared[nets[0]]['g_type'] = gtype
                new_node = Node.gen_node(declared[nets[0]], std_node_lib)
                circuit.nodes[new_node.num] = new_node
                if new_node.ntype == 'PO':
                    circuit.outputs.append(new_node)

        # 2nd pass: connect the gates
        for statement in statements:
            x_type, nets = self.read_verilog_syntax(statement)
            if x_type == "GATE":
                _, nets = nets
                for net in nets[1:]:
                    circuit.nodes[nets[0]].unodes.append(circuit.nodes[net])
                    circuit.nodes[net].dnodes.append(circuit.nodes[nets[0]])

        # Insert a fan-out branch node on every connection of a stem
        branches = {}
        for stem in circuit.nodes.values():
            if len(stem.dnodes) > 1:
                for idx in range(len(stem.dnodes)):
                    branch = Node.gen_node({'num': stem.num + '-' + str(idx + 1),
                                            'n_type': "FB", 'g_type': "BRCH"}, std_node_lib)
                    branches[branch.num] = branch
                    CircuitLoader.insert_branch(stem, stem.dnodes[0], branch)
        circuit.nodes.update(branches)

    def read_ckt(self, circuit, circuit_fname, std_node_lib):
        """Read a ``.ckt`` netlist, each node as an object."""
        with open(circuit_fname) as infile:
            lines = infile.readlines()
        circuit.nodes = {}

        # 1st pass: create all nodes
        for line in lines:
            if len(line) < 6:
                continue
            attr = line.split()
            node_info = {
                "n_type": NodeType.from_ckt_code(int(attr[0])).value,
                "g_type": GateType.from_ckt_code(int(attr[2])).value,
                "num": attr[1],
            }
            new_node = Node.gen_node(node_info, std_node_lib)
            if new_node.gtype == "IPT":
                circuit.inputs.append(new_node)
            if new_node.ntype == "PO":
                circuit.outputs.append(new_node)
            circuit.nodes[new_node.num] = new_node

        # 2nd pass: connect the nodes
        for line in lines:
            if len(line) < 6:
                continue
            self.connect_node(circuit, line.strip())

    @staticmethod
    def cell2gate(cell_name):
        ## Inputs: Verilog gate input formats
        ## Outputs: gtype corresponding gate name
        for gname, cell_names in config.CELL_NAMES.items():
            if cell_name in cell_names:
                return gname
        raise NameError(f"Cell type {cell_name} was not found")
    
    @staticmethod
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

    @staticmethod
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
            
            gtype = CircuitLoader.cell2gate(line_syntax.group(1))
            # #we may not use gname for now. 
            # gname = line_syntax.group(2)
            
            # TODO: Saeed fixed this but was not tested on all circuits
            # It had issues with netlists that have gate description in multiple lines
            # pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3))
            pin_format = re.findall(r'\.(\w+)\((\w*)\)', line_syntax.group(3).replace(" ", ""))
            if pin_format:
                #TODO: for now, we considered PO as the last pin
                if "Z" not in pin_format[-1][0]:
                    raise NameError("Cannot detect the output pin as the last argumet, check code")
                nets = [pin_format[-1][1]]
                for x in pin_format[:-1]:
                    nets.append(x[1])
            else:
                # verilog with no pin format
                nets = line_syntax.group(3).replace(' ', '').split(',')

            return ("GATE", (gtype, nets) )
        
        raise NameError(f"No suggestion for \n>{line}<\n was found")