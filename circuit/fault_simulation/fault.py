import numpy as np

class Fault():
    def __init__(self, node_num, stuck_val):
        self.node_num = str(node_num)
        self.stuck_val = str(stuck_val)
        self.D_count = 0 
        # Issue: in PPSFm D_count is set as an array

    def __str__(self):
        return self.node_num + "@" + self.stuck_val

    def __repr__(self):
        return self.__str__()


class FaultList:
    """ Fault list """
    #TODO: maybe using dictionary or set instead of a list for faults
    def __init__(self):
        self.faults = []

    def add(self, node_num, stuck_val):
        self.faults.append(Fault(node_num, stuck_val))

    def add_str(self, fault_str):
        """ add a fault if the fault format is <node-num>@<stuck value> """ 
        num, val = fault_str.strip().split("@")
        self.faults.append(Fault(num, val))

    def add_str_list(self, faults_str_list):
        """ add faults with their string in faults_str_list """
        for fault in faults_str_list:
            self.add_str(fault)

    def add_all(self, circuit):
        for node in circuit.nodes_lev:
            self.add_node(node)

    def add_random(self, circuit, random_num=1):
        idx_random = np.random.choice(len(circuit.nodes_lev), random_num, replace=False)
        for i in range(random_num):
            self.add(circuit.nodes_lev[idx_random[i]].num, 
                    np.random.randint(0,2))
    
    def add_fault(self, fault):
        self.faults.append(fault)

    def remove_faults(self, faults):
        # TODO: this is not a good method, to be modified after
        # the main data structure is changed to a dict or set
        # Does not change the current faults
        current_faults = set([str(x) for x in self.faults])
        if isinstance(faults, list):
            faults = set([str(x) for x in faults])
        new_faults = current_faults - faults
        # self.faults = []
        # for fault in new_faults:
        #     self.faults.add_str(fault)
        return list(new_faults)

    def add_node(self, node):
        """ adds both S@0 and S@1 faults for node """
        self.add(node.num, 0)
        self.add(node.num, 1)

    def add_nodes(self, nodes):
        assert isinstance(nodes, list), "the input should be a list of nodes"
        for node in nodes:
            self.add_node(node)

    def add_file(self, fname):
        """ read faults from a file and add it to the fault list 
        file format: each fault <node-num>@<stuck value> in separate lines

        Arguments
        ---------
        fname : str
            the path and file name of the fault file 
        """ 
        with open(fname, "r") as infile:
            for line in infile:
                self.add_str(line)

    def write_file(self, fname, verbose=False):
        with open(fname, "+w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "\n")
            if verbose:
                print("Fault list is stored in {}".format(fname))

    def write_file_extra(self, fname, verbose=False):
        with open(fname, "w") as outfile:
            for fault in self.faults:
                outfile.write(str(fault) + "," + ",".join([str(x) for x in fault.D_count])+"\n")
            if verbose:
                print("Fault list with D_counts is stored in {}".format(fname))
    
    def calc_fc(self):
        detected_count = 0
        for fault in self.faults:
            if fault.D_count > 0:
                detected_count += 1
        return detected_count / len(self.faults)
   
    def get_D_count(self):
        res = {}
        for fault in self.faults:
            res[str(fault)] = fault.D_count
        return res
