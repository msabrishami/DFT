
import re
import config
import os

# change these
from circuit.circuit import *
from circuit.inventory.modelsim_simulator import *
from circuit.load_circuit import *

class Checker():
    def __init__(self, c_name, tp_count):
        """ create a circuit and a modelsim simulation
        we have two types of inputs: "gate-level-circuit" and a "verilog"
        verilog can be anything, gate level, behavioral, etc. 
        But gate-level-circuit can only be gate-level ckt or gate-level verilog 
        For now we are only supporting ckt for gate-level-circuit
        It is possible that both are the same, if we have a gate-level-verilog
        Objective: 
        we want to simulate the gate-level-circuit  with methods in class Circuit 
            and compare the results with modelsim simulation of the verilog. 
        Tasks: 
        - Check if the PI/PO of the files are the same -- raise error if not match
        - etc. 
        """
        self.c_name = c_name
        self.tp_count = tp_count


    def modelsim_wrapper(self):
        '''
        Given the circuit name and test pattern count, it will do the logic_sim on our platform and the simulation on ModelSim
        Return the check result between logic_sim and ModelSim
        #We use read_verilog() here
        '''
        #Generate random inputs patterns for circuit
        #Simulate the random input patterns with modelsim, using Modelsim class
        #Store the golden results in correct locations
        #This is simply a wrapper around class Modelsim
        circuit = Circuit(self.c_name)
        #self.circuit = circuit
        LoadCircuit(circuit, 'v')
        circuit.lev()
        sim = Modelsim()
        sim.project(circuit)
        #sim.gen_tb(sim.gen_rand_tp(tp_count= tp_count))
        sim.gen_rand_tp(tp_count= self.tp_count)
        sim.gen_tb()
        sim.simulation()
        self.tp_path = os.path.join(sim.path_gold, 'golden_' + circuit.c_name + '_'+ str(self.tp_count)+ '_b.txt')
        #return self.check_IO_golden(circuit, self.tp_path)

    def check_ckt_verilog(self, ckt_format = 'verilog'):
        #check verilog with golden_IO
        #check ckt with golden_IO

        circuit = Circuit(self.c_name)
        if ckt_format == 'verilog':
            LoadCircuit(circuit, 'v')
        elif ckt_format == 'ckt':
            LoadCircuit(circuit)
        circuit.lev()
        if self.check_IO_golden(circuit) == True:
            print(ckt_format + ': ' + circuit.c_name + ' matches golden_IO!')
        else:
            print(ckt_format + ': ' + circuit.c_name + ' does not match golden_IO!')

    def check_PI_PO(self):
        #Given a circuit name, check the PI/PO pins between verilog and ckt
        #from http://sportlab.usc.edu/~msabrishami/benchmarks.html
        #between CKT-658 and verilog
        #circuit: 1355 has different PI/PO pins
        #circuit: 17, 432, 499, 880, 1908, 3540, 5315, 6288 has the same PI/PO pins 
        
        if self.find_file(config.VERILOG_DIR, self.c_name + '.v') == True and self.find_file(config.CKT_DIR, self.c_name + '.ckt'):
            circuit_verilog = Circuit(self.c_name)
            LoadCircuit(circuit_verilog, 'v')
            circuit_ckt = Circuit(self.c_name)
            LoadCircuit(circuit_ckt)
            if self.get_pin_num(circuit_verilog.PO) == self.get_pin_num(circuit_ckt.PO) and self.get_pin_num(circuit_verilog.PI) == self.get_pin_num(circuit_ckt.PI):
                print('PI/PO pins between ckt and verilog of {} are the same!'.format(self.c_name))
                return True
            else:
                print('PI/PO pins between ckt and verilog of {} are different!'.format(self.c_name))
                return False
        else:
            print('miss ckt or verilog files for {} circuit'.format(self.c_name))
            return False

    def get_pin_num(self, node_list):
        #get the pins number list
        num_list = []
        for node in node_list:
            num_list.append(node.num)
        return num_list

    def find_file(self, path, fname):
        #check if the file is exist
        for r, d, f in os.walk(path):
            if fname in f:
                return True
            else:
                return False

    def check_IO_golden(self, circuit):
        #we have golden_test() in circuit
        #We already generated golden-results
        #Now we just want to check if circuit.logicsim of ckt or verilog matches
        infile = open(self.tp_path, "r")
        lines = infile.readlines()
        PI_t_order  = [x.lstrip('N') for x in lines[0][8:].strip().split(',')]
        PO_t_order = [x.lstrip('N') for x in lines[1][8:].strip().split(',')]
        PI_num = [x.num.lstrip('N') for x in circuit.PI]
        PO_num = [x.num.lstrip('N') for x in circuit.PO]
        
        #print("Logic-Sim validation with {} patterns".format(int((len(lines)-2)/3)))
        if PI_t_order != PI_num:
            print("Error:{} PI node order does not match! ".format(circuit.c_name))
            return False
        if PO_t_order != PO_num:
            print("Error:{} PO node order does not match! ".format(circuit.c_name))
            return False
        for t in range(int((len(lines)-2)/3)):
            test_in  = [int(x) for x in lines[(t+1)*3].strip().split(',')]
            test_out = [int(x) for x in lines[(t+1)*3+1].strip().split(',')]
            circuit.logic_sim(test_in)
            logic_out = circuit.read_PO()

            logic_out = { k.replace('N', ''): v for k, v in logic_out.items() }
            for i in range(len(PO_t_order)):
                out_node = PO_t_order[i]
                out_node_golden = test_out[i]
                if out_node_golden != logic_out[out_node]:
                    print("Error:{} PO values do not match! ".format(circuit.c_name))
                    return False
        #print("Validation completed successfully - all correct")
        return True
