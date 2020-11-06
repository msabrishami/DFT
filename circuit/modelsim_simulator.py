
import os
import subprocess
import circuit
import config
from shutil import copyfile

'''
This class can be reused for different circuits, and it will create different modelsim project folders for different circuits 
'''
class Modelsim():
    def __init__(self):
        '''
        Create the ModelSim folder
        '''
        self.tp_fname =None
        if os.path.exists(config.MODELSIM_DIR): 
            #print("Modelsim project folder exists: {}".format(config.MODELSIM_DIR))
            pass
        else:
            #print("Creating a Modelsim project: {}".format(config.MODELSIM_DIR))
            os.mkdir(config.MODELSIM_DIR)


    def __del__(self):
        pass
    
    def project(self, circuit):
        '''
        Create the project folder for the specific circuit
        '''
        self.circuit = circuit
        self.path = os.path.join(config.MODELSIM_DIR, self.circuit.c_name) #project path for a specific netlist
        self.path_in = os.path.join(self.path, config.MODELSIM_INPUT_DIR)
        self.path_gold = os.path.join(self.path, config.MODELSIM_GOLD_DIR)
        self.path_out = os.path.join(self.path, config.MODELSIM_OUTPUT_DIR)
        if os.path.exists(self.path): 
            #print("Modelsim project folder for circuit {} alread exists in {}".format(self.circuit.c_name, self.path))
            pass
        else: 
            #print("Creating a Modelsim project folder for circuit {} in {}".format(self.circuit.c_name, self.path))
            os.mkdir(self.path)
        
        if not os.path.exists(self.path_in):
            os.mkdir(self.path_in)
        
        if not os.path.exists(self.path_gold):
            os.mkdir(self.path_gold)
        
        if not os.path.exists(self.path_out):
            os.mkdir(self.path_out)

        return 
    
    def gen_rand_tp(self, tp_count, tp_fname=None):
        '''
        Generates a random test patter file for this circuit
        '''
        #print("Generating a test pattern file in {}".format(self.path_in))
        #get test pattern file name
        if tp_fname is None:
            self.tp_fname = os.path.join(self.path_in,
                    self.circuit.c_name + "_" + str(tp_count) + "_b.txt")
        else:
            self.tp_fname = os.path.join(self.path_in, tp_fname)
        #create test pattern file
        self.circuit.gen_tp_file(tp_count, fname=self.tp_fname)
        #return tp_fname 

    def gen_tb(self):
        """ 
        Generate test_bench.v, run.sh, run.do for the specific circuit 
           in the circuit project folder
        """ 
        #print(self.tp_fname)

        #check number of input test patterns
        fr = open(self.tp_fname, mode='r')
        line_list = fr.readlines()
        tp_count = len(line_list)-1
        fr.close()
        self.tp_count=tp_count
        #get testbemch file name
        tb_fname = os.path.join(self.path, self.circuit.c_name + "_" + str(tp_count) + "_b_tb.v")

        #generate different tb for different test input        
        fw = open(tb_fname, mode='w')
        fw.write("`timescale 1ns/1ns" + "\n")
        fw.write('module ' + str(self.circuit.c_name) + "_" + str(tp_count) + "_b_tb;" + '\n')
        fw.write("integer fi, fo;\n")
        fw.write('integer statusI;\n')
        fw.write('integer in_name;\n')
        fw.write('reg in [0:' + str(len(self.circuit.PI)-1) + '];\n')
        fw.write('wire out [0:' + str(len(self.circuit.PO) - 1) + '];\n')
        fw.write('reg clk;\n')
        fw.write('\n')
        fw.write(str(self.circuit.c_name) + ' u_' + str(self.circuit.c_name) + ' (')
        in_index = 0
        for pi in self.circuit.PI:
            fw.write('.N' + str(pi.num) + '(in[' + str(in_index) + ']),')
            in_index += 1
        out_index = 0
        for po in self.circuit.PO:
            fw.write('.N' + str(po.num) + '(out[' + str(out_index) + '])')
            if out_index != len(self.circuit.PO)-1:
                fw.write(',')
                out_index += 1
            else:
                fw.write(');\n')

        fw.write('initial begin\n')
        fw.write('\tfi = $fopen("'+ './input/'  + self.circuit.c_name + "_" + str(tp_count) + "_b.txt"+'","r");\n')
        fw.write('\tstatusI = $fscanf(fi,"')
        for j in range(len(self.circuit.PI)):
            fw.write('%s')
            if j != len(self.circuit.PI) - 1:
                fw.write(',')
            else:
                fw.write('\\n",')
        for j in range(len(self.circuit.PI)):
            fw.write('in[' + str(j) + ']')
            if j != len(self.circuit.PI) - 1:
                fw.write(',')
            else:
                fw.write(');\n')
        fw.write('\t#1\n')

        fw.write('\tfo = $fopen("./gold/golden_' + str(self.circuit.c_name) + "_" + str(tp_count) + '_b.txt","w");\n')
        fw.write('\tfo = $fopen("./gold/golden_' + str(self.circuit.c_name) + "_" + str(tp_count) + '_b.txt","a");\n')
        fw.write('\t$fwrite(fo,"Inputs: ')
        in_index = 0
        for pi in self.circuit.PI:
            fw.write("N" + str(pi.num))
            if in_index != len(self.circuit.PI) - 1:
                fw.write(',')
                in_index += 1
            else:
                fw.write('\\n");\n')
        fw.write('\t$fwrite(fo,"Outputs: ')
        out_index = 0
        for pi in self.circuit.PO:
            fw.write("N" + str(pi.num))
            if out_index != len(self.circuit.PO) - 1:
                fw.write(',')
                out_index += 1
            else:
                fw.write('\\n");\n')
        for i in range(tp_count):
            fw.write('\t//test pattern' + str(i) + '\n')
            fw.write('\tstatusI = $fscanf(fi,"')
            for j in range(len(self.circuit.PI)):
                fw.write('%h')
                if j != len(self.circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(self.circuit.PI)):
                fw.write('in[' + str(j) + ']')
                if j != len(self.circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')
            fw.write('\t#1\n')
            '''
            fw.write('\t$display("')
            for j in range(len(self.circuit.PI)):
                fw.write('%h')
                if j != len(self.circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(self.circuit.PI)):
                fw.write('in[' + str(j) + ']')
                if j != len(self.circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')
                    '''
            '''
            fw.write('\t$display("')
            out_index = 0
            for po in self.circuit.PO:
                fw.write("N" + str(po.num) + '=%h')
                if out_index != len(self.circuit.PO) - 1:
                    fw.write(',')
                    out_index += 1
                else:
                    fw.write('\\n",')
                    for j in range(len(self.circuit.PO)):
                        fw.write('out[' + str(j) + ']')
                        if j != len(self.circuit.PO) - 1:
                            fw.write(',')
                            out_index += 1
                        else:
                            fw.write(');\n')
                            '''
            fw.write('\t$fwrite(fo, "Test # = ' + str(i+1) + '\\n");\n')
            fw.write('\t$fwrite(fo,"')
            for j in range(len(self.circuit.PI)):
                fw.write('%h')
                if j != len(self.circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(self.circuit.PI)):
                fw.write('in[' + str(j) + ']')
                if j != len(self.circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')
            fw.write('\t$fwrite(fo,"')
            for j in range(len(self.circuit.PO)):
                fw.write('%h')
                if j != len(self.circuit.PO) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(self.circuit.PO)):
                fw.write('out[' + str(j) + ']')
                if j != len(self.circuit.PO) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')


        fw.write('\t$fclose(fi);\n')
        fw.write('\t$fclose(fo);\n')

        fw.write('\t$finish;\n')
        fw.write('end\n')
        fw.write('endmodule\n')
        fw.close()

        #create run.sh
        fw = open(os.path.join(self.path, self.circuit.c_name + "_" + str(tp_count) + "_run.sh"), mode = 'w')
        fw.write('vsim -c -do ' + self.circuit.c_name + "_" + str(tp_count) +'_b.do\n')
        fw.close()
        
        #create run.do
        fw = open(os.path.join(self.path, self.circuit.c_name + "_" + str(tp_count) +'_b.do'), mode='w')
        fw.write('vlib work\n')
        fw.write('vmap work work\n')
        fw.write('vlog -work work '+str(self.circuit.c_name)+'.v\n')
        fw.write('vlog -work work '+str(self.circuit.c_name)+ "_" + str(tp_count) + '_b_tb.v\n')
        fw.write('onerror {resume}\n')
        fw.write('vsim -novopt work.'+str(self.circuit.c_name)+"_" + str(tp_count) + '_b_tb\n')
        fw.write('run -all\n')
        fw.close()



    def simulation(self, fname_sh=None):
        """ 
        First: copy verilog file from ./data/verilog to the project folder
        Second: This function will call a subprocess which will run the ModelSim in the background(No GUI pop up). After it finishes, ModelSim will close automatically.
        Third: ModelSim will generate the golden I/O file in gold folder
        Fourth: After ModelSim finishes, the function will end
        """ 
        #copy .v file to the ModelSim project folder
        filepath=os.path.join(self.path, self.circuit.c_name+'.v')
        if os.path.isfile(filepath):
            pass
        else:
            copyfile(os.path.join(config.VERILOG_DIR, self.circuit.c_name + ".v"), filepath)
        #get the shell file name which will run the ModelSim for different circuit with different pattern count
        if fname_sh == None:
            fname_sh = self.circuit.c_name + "_" + str(self.tp_count) + "_run.sh"
        #run ModelSim in subprocess
        subprocess.call(['sh',fname_sh], cwd = self.path)
        #end of subprocess
        #return to main function

    #We do not use this function
    #We use golden_test() function in circuit.py now.
    def check(self):
        """
        This method checks if the circuit.logicsim matches golden modelsim
        First: read output files from our platfrom and ModelSim
        Second: check if two files are the same
        """ 
        #output file created by our platform
        origin_output_file = open(self.path+'output/'+self.circuit_name + '_out.txt', "r+")
        #output file form ModelSim
        new_output_file = open(self.path+'gold/golden_'+self.circuit_name + '.txt', "r+")
        number_of_line = 1
        origin_line = origin_output_file.readline()
        new_line = new_output_file.readline()
        flag = 1
        if len(origin_line) == 0:
            print("original file is empty!")
            flag = 0
        if len(new_line) == 0:
            print("new file is empty!")
            flag = 0
        if origin_line is not None and new_line is not None:
            while origin_line:
                if origin_line.lower() != new_line.lower():
                    print('file different! different line is #', number_of_line)
                    flag = 0

                else:
                    flag = 1
                origin_line = origin_output_file.readline()
                new_line = new_output_file.readline()
                number_of_line += 1
        if flag == 1:
            print('result are the same')
        else:
            print("result are not same!")
        origin_output_file.close()
        new_output_file.close()

