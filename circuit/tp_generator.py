import random
import config
import os

class TPGenerator:
    def __init__(self, circuit):
        self.circuit = circuit
        
    def gen_single_tp(self, mode="b"):
        """ Generate a random input pattern.
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a single input pattern
            """
        if mode not in ["b", "x"]:
            raise NameError("Mode is not acceptable")

        bits = ["0","1","X"]
        if mode == "b":
            tp = [int(bits[random.randint(0,1)]) for _ in range(len(self.circuit.PI))]
        elif mode == "x":
            tp = [bits[random.randint(0,2)] for _ in range(len(self.circuit.PI))]
        
        return tp 
    
    def gen_multiple_tp(self, tp_count, mode="b"):
        """ Generate multiple random input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a list of random test patterns
        does not store the generated tps in file 
        """

        tps = [self.gen_single_tp(mode) for _ in range(int(tp_count))]

        return tps

    def gen_tp_file(self, tp_count, tp_fname=None, mode="b", verbose=False):
        """ Create single file with multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a list of random test patterns
        mention the sequence of inputs and tps
        """ 
        fn = os.path.join(config.PATTERN_DIR, 
                self.circuit.c_name + "_" + str(tp_count) + "_tp_" + mode + ".tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.circuit.PI]) + "\n")
        tps = self.gen_multiple_tp(tp_count=tp_count,mode=mode)
        for tp in tps:
            tp_str = [str(val) for val in tp]
            outfile.write(",".join(tp_str) + "\n")
        
        outfile.close()
        if verbose:
            print(f"Generated {tp_count} test patterns and saved in {tp_fname}")

        return tps # better to return the file name

    def gen_full_tp(self):
        """
        Return all possible test patterns
        #TODO: should we implement all with mode = x?
        """ 
        tps = []
        for t in range(2**len(self.circuit.PI)):
            tp = list(map(int, bin(t)[2:].zfill(len(self.circuit.PI))))
            tps.append(tp)
        
        return tps

    def gen_tp_file_full(self, tp_fname=None):
        """Create a single file including all possible test patterns""" 
        if len(self.circuit.PI) > 12:
            print("Error: cannot generate full tp file for circuits with PI > 12")
            return []
        fn = os.path.join(config.PATTERN_DIR, self.circuit.c_name + "_tp_full.tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.circuit.PI]) + "\n")
        tps = self.gen_full_tp()
        for t in tps:
            outfile.write(",".join(str(t)) + "\n")
        outfile.close()
        print(f"Generated full test patterns and saved in {tp_fname}")
        
        return tps # better to return the file name

    @staticmethod
    def load_tp_file(fname):
        """ Load single file with multiple test pattern vectors. 
            Does not warn if the size of input nodes is less than each test pattern""" 
        # do we need to check the order of the inputs in the file?  
        # this can be done using "yield" or "generate" -- check online 

        if not os.path.exists(fname):
            raise 'Test file does not exist. Use gen_tp_file() or gen_full_tp_file() instead'
            # return self.gen_tp_file(tp_count=tp_count,tp_fname=fname)
        
        infile = open(fname, 'r')
        tps = []
        lines = infile.readlines()

        for line in lines[1:]:
            words = line.rstrip().split(',')
            words = [int(word) if word == '1' or word == '0' else 'X' for word in words]
            tps.append(words)
        infile.close()
        return tps