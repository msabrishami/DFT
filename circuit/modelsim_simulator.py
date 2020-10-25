import os
import subprocess
import circuit
class Modelsim():
    def __init__(self):
        self.input_file_name=''
        self.circuit_name=''

    def __del__(self):
        pass

    def tb_gen(self, circuit, tp_count):
        """ What does this method do Ting-Yu???
        """ 
        # First: generate a input test patter file inside this path 
        #TODO the name of the test pattern file needs to be changed 
        self.circuit_name=circuit.c_name
        path = '../data/modelsim/' + circuit.c_name + '/'
        self.path = path
        print("Generating a test pattern file in " + self.path)
        circuit.gen_tp(tp_count, fname = path + "/mytp.txt")
        print("Generating a Modelsim project folder in " + self.path)
        #input file are stored in input folder
        #check number of input test patterns
        fr=open(input_file_name, mode='r')
        line_list=fr.readlines()
        number_of_test_patterns=len(line_list)-1
        fr.close()

        fw = open(path + str(circuit.c_name) + "_tb.v", mode='w')
        fw.write("`timescale 1ns/1ns" + "\n")
        fw.write('module ' + str(circuit.c_name) + "_tb;" + '\n')
        fw.write("integer fi, fo;\n")
        fw.write('integer statusI;\n')
        fw.write('integer in_name;\n')
        fw.write('reg in [0:' + str(len(circuit.PI)-1) + '];\n')
        fw.write('wire out [0:' + str(len(circuit.PO) - 1) + '];\n')
        fw.write('reg clk;\n')
        fw.write('\n')
        fw.write(str(circuit.c_name) + ' u_' + str(circuit.c_name) + ' (')
        in_index = 0
        for pi in circuit.PI:
            fw.write('.N' + str(pi.num) + '(in[' + str(in_index) + ']),')
            in_index += 1
        out_index = 0
        for po in circuit.PO:
            fw.write('.N' + str(po.num) + '(out[' + str(out_index) + '])')
            if out_index != len(circuit.PO)-1:
                fw.write(',')
                out_index += 1
            else:
                fw.write(');\n')

        fw.write('initial begin\n')
        fw.write('\tfi = $fopen("./input/'+input_file_name+'","r");\n')
        fw.write('\tstatusI = $fscanf(fi,"')
        for j in range(len(circuit.PI)):
            fw.write('%s')
            if j != len(circuit.PI) - 1:
                fw.write(',')
            else:
                fw.write('\\n",')
        for j in range(len(circuit.PI)):
            fw.write('in[' + str(j) + ']')
            if j != len(circuit.PI) - 1:
                fw.write(',')
            else:
                fw.write(');\n')
        fw.write('\t#1\n')

        fw.write('\tfo = $fopen("./gold/golden_' + str(circuit.c_name) + '.txt","w");\n')
        fw.write('\tfo = $fopen("./gold/golden_' + str(circuit.c_name) + '.txt","a");\n')
        fw.write('\t$fwrite(fo,"Inputs: ')
        in_index = 0
        for pi in circuit.PI:
            fw.write("N" + str(pi.num))
            if in_index != len(circuit.PI) - 1:
                fw.write(',')
                in_index += 1
            else:
                fw.write('\\n");\n')
        fw.write('\t$fwrite(fo,"Outputs: ')
        out_index = 0
        for pi in circuit.PO:
            fw.write("N" + str(pi.num))
            if out_index != len(circuit.PO) - 1:
                fw.write(',')
                out_index += 1
            else:
                fw.write('\\n");\n')
        for i in range(number_of_test_patterns):
            fw.write('\t//test pattern' + str(i) + '\n')
            fw.write('\tstatusI = $fscanf(fi,"')
            for j in range(len(circuit.PI)):
                fw.write('%h')
                if j != len(circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(circuit.PI)):
                fw.write('in[' + str(j) + ']')
                if j != len(circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')
            fw.write('\t#1\n')
            fw.write('\t$display("')
            for j in range(len(circuit.PI)):
                fw.write('%h')
                if j != len(circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(circuit.PI)):
                fw.write('in[' + str(j) + ']')
                if j != len(circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')
            fw.write('\t$display("')
            out_index = 0
            for po in circuit.PO:
                fw.write("N" + str(po.num) + '=%h')
                if out_index != len(circuit.PO) - 1:
                    fw.write(',')
                    out_index += 1
                else:
                    fw.write('\\n",')
                    for j in range(len(circuit.PO)):
                        fw.write('out[' + str(j) + ']')
                        if j != len(circuit.PO) - 1:
                            fw.write(',')
                            out_index += 1
                        else:
                            fw.write(');\n')
            fw.write('\t$fwrite(fo, "Test # = ' + str(i) + '\\n");\n')
            fw.write('\t$fwrite(fo,"')
            for j in range(len(circuit.PI)):
                fw.write('%h')
                if j != len(circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(circuit.PI)):
                fw.write('in[' + str(j) + ']')
                if j != len(circuit.PI) - 1:
                    fw.write(',')
                else:
                    fw.write(');\n')
            fw.write('\t$fwrite(fo,"')
            for j in range(len(circuit.PO)):
                fw.write('%h')
                if j != len(circuit.PO) - 1:
                    fw.write(',')
                else:
                    fw.write('\\n",')
            for j in range(len(circuit.PO)):
                fw.write('out[' + str(j) + ']')
                if j != len(circuit.PO) - 1:
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
        # path = './' + str(circuit.c_name) + '/'
        fw = open(path + "run.sh", mode='w')
        fw.write('vsim -c -do do_'+str(circuit.c_name)+'.do\n')
        fw.close()
        #create run.do
        fw = open(path + 'do_'+str(circuit.c_name)+'.do', mode='w')
        fw.write('vlib work\n')
        fw.write('vmap work work\n')
        fw.write('vlog -work work '+str(circuit.c_name)+'.v\n')
        fw.write('vlog -work work '+str(circuit.c_name)+'_tb.v\n')
        fw.write('onerror {resume}\n')
        fw.write('vsim -novopt work.'+str(circuit.c_name)+'_tb\n')
        fw.write('run -all\n')
        fw.close()


    def modelsim_simulation():
        """ #TODO: What does this method do???
        How should someone who is using this know that the process
        will run in the background? 
        Output:
            the golden IP file will be generated 
        """ 
        if os.path.exists(self.path + '/gold') == False:
            os.mkdir(self.path + '/gold')
        subprocess.call(['sh', self.path + '/run.sh'], 
                cwd = './'+ self.circuit_name)

    def check():
        """ What does this method do Ting-Yu??? 
        This method checks if the circuit.logicsim matches golden modelsim
            results
        """ 

        #output file created by our platform
        origin_output_file = open('./'+self.circuit_name+'/output/'+self.circuit_name + '_out.txt', "r+")
        #output file form ModelSim
        new_output_file = open('./'+self.circuit_name+'/gold/golden_'+self.circuit_name + '.txt', "r+")
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


        
