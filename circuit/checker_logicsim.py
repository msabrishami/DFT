import re
import config
import os
from circuit import *
from modelsim_simulator import *

class Checker():
    def __init__(self):
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
    def run(self, ckt_name, tp_count):
        '''
        Given the circuit name and test pattern count, it will do the logic_sim on our platform and the simulation on ModelSim
        Return the check result between logic_sim and ModelSim
        #We use read_verilog() here
        '''
        circuit = Circuit(ckt_name)
        circuit.read_verilog()
        circuit.lev()
        sim = Modelsim()
        sim.project(circuit)
        sim.gen_rand_tp(tp_count= tp_count)
        sim.gen_tb()
        sim.simulation()
        tp_path = os.path.join(sim.path_gold, 'golden_' + circuit.c_name + '_'+ str(tp_count)+ '_tp_b.txt')
        return self.check_IO_golden(circuit, tp_path)


    def run_all(self, tp_count):
        '''
        It will run all of .v files in VERILOG_DIR and compare results between ModelSim and our Simulator
        '''
        file_names = []
        #r=root, d=directories, f = files
        #find all .v files in the VERILOG_DIR
        for r, d, f in os.walk(config.VERILOG_DIR):
            for file in f:
                if '.v' in file:
                    file_names.append(os.path.splitext(file)[0])
        #check the result by using function run()
        for c_name in file_names:
            if self.run(c_name, tp_count) == False:
                print('Test: {} fails !'.format(c_name))
                return False
        print('#########################################################')
        print('############## All Circuits Tests Pass ! ################')
        print('#########################################################')
        return True


    def check_PI_PO(self, fname_ckt, fname_verilog):
        '''
        from http://sportlab.usc.edu/~msabrishami/benchmarks.html
        between CKT-658 and verilog
        circuit: 1355 has different PI/PO pins
        circuit: 17, 432, 499, 880, 1908, 3540, 5315, 6288 has the same PI/PO pins 
        '''
        ckt_path = os.path.join(config.CKT_DIR,fname_ckt)
        verilog_path = os.path.join(config.VERILOG_DIR,fname_verilog)
        fr_ckt = open(ckt_path, mode = 'r')
        fr_verilog = open(verilog_path, mode = 'r')
        PI_ckt = []
        PO_ckt = []
        PI_verilog = []
        PO_verilog = []
        eff_line = ''
        #get the PI number and PO number in .ckt file
        for line in fr_ckt:
            line_split = line.split(' ')
            if line[0] == '1':
                PI_ckt.append(line_split[1])
            if line[0] == '3':
                PO_ckt.append(line_split[1])
        #get the PI number and PO number in .v file
        for line in fr_verilog:
            #get rid of commented information
            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            if line_syntax:
                line = line[:line.index('//')]
            #combine separated lines
            if ';' not in line and 'endmodule' not in line:
                eff_line = eff_line + line.rstrip()
                continue
            line = eff_line + line.rstrip()
            eff_line = ''
            if line != "":
                # find PI
                line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                       PI_verilog.append(n.lstrip('N'))
                # find PO
                line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                        PO_verilog.append(n.lstrip('N'))

        PI_ckt.sort()
        PI_verilog.sort() 
        PO_ckt.sort() 
        PO_verilog.sort()
        #check if the pin number in .ckt and .v are the same
        if PI_ckt == PI_verilog and PO_ckt == PO_verilog:
            print('{} and {} are the same!'.format(fname_ckt, fname_verilog))
        else:
            print('{} and {} are not the same!'.format(fname_ckt, fname_verilog))

    def run_check_PI_PO(self):
        '''
        check all of .ckt and .v files automatically by using function check_PI_PO()
        '''
        file_names_ckt = []
        file_names_ckt_and_verilog = []
        # r=root, d=directories, f = files

        #check if .ckt exists for the specific circuit
        for r, d, f in os.walk(config.CKT_DIR):
            for file in f:
                if '.ckt' in file:
                    file_names_ckt.append(os.path.splitext(file)[0])
        #check if .ckt and .v both exist for the specific ciruict
        for r, d, f in os.walk(config.VERILOG_DIR):
            for file in f:
                if '.v' in file:
                    if os.path.splitext(file)[0] in file_names_ckt:
                        file_names_ckt_and_verilog.append(os.path.splitext(file)[0])
        #check by function check_PI_PO()
        for file in file_names_ckt_and_verilog:
            self.check_PI_PO(file + '.ckt', file + '.v')


    def check_IO_golden(self, circuit, golden_io_filename):
        #we have golden_test() in circuit
        #compares the results of logic-sim of this circuit,
        #... provided a golden input/output file
        infile = open(golden_io_filename, "r")
        lines = infile.readlines()
        PI_t_order  = [x[1:] for x in lines[0][8:].strip().split(',')]
        PO_t_order = [x[1:] for x in lines[1][8:].strip().split(',')]
        PI_num = [x.num for x in circuit.PI]
        print("Logic-Sim validation with {} patterns".format(int((len(lines)-2)/3)))
        if PI_t_order != PI_num:
            print("Error: PI node order does not match! ")
            return False
        for t in range(int((len(lines)-2)/3)):
            test_in  = [int(x) for x in lines[(t+1)*3].strip().split(',')]
            test_out = [int(x) for x in lines[(t+1)*3+1].strip().split(',')]
            circuit.logic_sim(test_in)
            logic_out = circuit.read_PO()
            for i in range(len(PO_t_order)):
                out_node = PO_t_order[i]
                out_node_golden = test_out[i]
                if out_node_golden != logic_out["out"+str(out_node)]:
                    print("Error: PO node order does not match! ")
                    return False
        print("Validation completed successfully - all correct")
        return True
'''
try:
    Checker().run_all(50)

except TypeError:
    print('TypeError!')
'''