# input file type : .bench
# output file type : .ckt658
# important : the finin parameter is not useable

import re
import argparse

def translator(src, dst):
    '''
    translates a bench circuit format to ckt-658 format.
    src: path for source bench file, with .bench suffix
    dst: path for destination ckt658 file, with .ckt suffix
    '''

    fin = open(src, 'r')
    f = fin.readlines()
    fin.close()
    for i in range(len(f)):
        f[i] = f[i].strip()

    input_list = []
    output_list = []
    internal_list = []

    for item in f:
        try:
            item[0]
        except:
            continue
        if item[0] != '#':
            if item[0] == 'I':
                input_list.append(item)
            if item[0] == 'O':
                output_list.append(item)
            if item.find('=')!=-1:
                internal_list.append(item)
    
    in_list = set()
    for item in input_list:
        item=item.split('#')
        item=re.findall('[0-9]+',item[0])
        in_list.add(item[0])
    
    out_list = set()
    for item in output_list:
        item=item.split('#')
        item=re.findall('[0-9]+',item[0])
        out_list.add(item[0])

    def gate_index(string):
        out = 0
        if string.upper().find('BUFF') >= 0:
            out=1
        elif string.upper().find('XOR') >= 0:
            out = 2
        elif string.upper().find('NOR') >= 0:
            out = 4
        elif string.upper().find('OR') >= 0:
            out = 3
        elif string.upper().find('NOT') >= 0:
            out = 5
        elif string.upper().find('NAND') >= 0:
            out = 6
        elif string.upper().find('AND') >= 0:
            out = 7
        return out

    finout={}
    for item in internal_list:
        item=item.split('#')
        item=item[0]
        item=re.findall('[0-9]+',item)
        for number in item[1:]:
            if number in finout:
                finout[number]=finout[number]+1
            else:
                finout[number]=1

    ckt_set=list()
    for item in in_list:
        if item in finout:
            fino=finout[number]
        else:
            fino=1
        node=[1,item,0,fino,0]
        ckt_set.append(node)

    for item in internal_list:
        item=item.split('#')
        item=item[0]
        item=re.findall('[a-zA-Z0-9]+',item)
        if item[0] in finout:
            fino=finout[item[0]]
        else:
            fino=0
        if(item[0] in out_list):
            if(gate_index(item[1])==1):
                node=[3,item[0],gate_index(item[1]),0,1,item[2]]
            else:
                node=[3,item[0],gate_index(item[1]),0,len(item[2:])]+item[2:]
            out_list.remove(item[0])
        else:
            if(gate_index(item[1])==1):
                node=[2,item[0],1,item[2]]
            else:
                node=[0,item[0],gate_index(item[1]),fino,len(item[2:])]+item[2:]
        ckt_set.append(node)

    for item in out_list:
        if(item in in_list):
            node=[3,item,0,0,0]
            ckt_set.append(node)
        else:
            print("error input",item)
    
    output_write=[]
    for item in ckt_set:
        item2 = [str(x) for x in item]
        output_str="    ".join(item2)+'\n'
        output_write.append(output_str)
    fv = open(dst, 'w')
    fv.writelines(output_write)
    fv.close()


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=True, help="path to store the ckt file")
    parser.add_argument("-bench", type=str, required=True, help="path to read the bench file")
    args = parser.parse_args()
    translator(args.bench, args.ckt)
    
