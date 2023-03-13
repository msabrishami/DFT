import random
import config
import os
import utils

class TPGenerator:
    def __init__(self, circuit):
        self.circuit = circuit
        
    def gen_single(self, mode="b"):
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
    
    def gen_n_random(self, tp_count, mode="b", unique=False):
        """ Generate multiple random input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a list of random test patterns
        does not store the generated tps in file 
        """

        if not unique:
            return [self.gen_single(mode) for _ in range(int(tp_count))]

        tps = []
        # Bad performance
        # Can't use random.choices() since it can't fit in integer for large circuits
        while len(tps) < tp_count: 
            x = self.gen_single()
            if x not in tps:
                tps.append(x)

        return tps

    def gen_file(self, tp_count, tp_fname=None, mode="b", verbose=False, unique=False):
        """ Create single file with multiple input patterns
        mode b: generate values in {0, 1}
        mode x: generate values in {0, 1, X}
        returns a list of random test patterns
        mention the sequence of inputs and tps

        Returns
        ------
        tp_fname, tps
        """ 
        fn = os.path.join(config.PATTERN_DIR, 
                self.circuit.c_name + "_" + str(tp_count) + "_tp_" + mode + ".tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.circuit.PI]) + "\n")
        tps = self.gen_n_random(tp_count=tp_count,mode=mode,unique=unique)
        for tp in tps:
            tp_str = [str(val) for val in tp]
            outfile.write(",".join(tp_str) + "\n")
        
        outfile.close()
        if verbose:
            print(f"Generated {tp_count} test patterns and saved in {tp_fname}")

        return tp_fname, tps

    def gen_full(self):
        """
        Return all possible test patterns
        #TODO: should we implement all with mode = x?
        """ 
        from queue import Queue
        tps = Queue()
    
        n_digits = len(self.circuit.PI)
        tps.put(utils.fix_size("0", n_digits))
        n = 1<<n_digits
        
        while n:
            n -= 1
            s1 = tps.get()    
            s2 = s1  

            tps.put(utils.fix_size(s1+"0", n_digits)) 
            tps.put(utils.fix_size(s2+"1", n_digits))
        
        tps = [list(map(int, [*tp])) for tp in [['0']*n_digits]+list(tps.queue)[:-2]]

        return tps

    def gen_full_file(self, tp_fname=None):
        """Create a single file including all possible test patterns""" 
        if len(self.circuit.PI) > 12:
            print("Error: cannot generate full tp file for circuits with PI > 12")
            return []
        fn = os.path.join(config.PATTERN_DIR, self.circuit.c_name + "_tp_full.tp")
        tp_fname = fn if tp_fname==None else tp_fname
        outfile = open(tp_fname, 'w')
        outfile.write(",".join([str(node.num) for node in self.circuit.PI]) + "\n")
        tps = self.gen_full()
        for t in tps:
            outfile.write(",".join(str(t)) + "\n")
        outfile.close()
        print(f"Generated full test patterns and saved in {tp_fname}")
        
        return tps # better to return the file name

    @staticmethod
    def load_file(fname):
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