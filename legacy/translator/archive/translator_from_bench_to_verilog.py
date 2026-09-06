import re
file=open('c1355.bench.txt','r')
file_lines=file.readlines()
file.close()
file_lines=file_lines[6:]
#count_list=len(file_lines)


input_list=[]
output_list=[]
internal_list=[]

for item in file_lines:
    if item[0]=='I':
        input_list.append(item)
    if item[0]=='O':
        output_list.append(item)
    if item[0] == '0' or item[0] == '1' or item[0] == '2' or item[0] == '3'\
        or item[0] == '4' or item[0] == '5' or item[0] == '6' or item[0] == '7'\
        or item[0] == '8' or item[0] == '9':
        internal_list.append(item)

input_num=[]
pi=''
for item in input_list:
    input_num=input_num+re.findall('\d+',item)
##print(input_num)
for item in input_num:
    pi=str(pi)+str('N')+str(item)+str(',')
pi=pi.rstrip(',')
##print(pi)
nin=len(input_num)

output_num=[]
po=''
for item in output_list:
    output_num=output_num+re.findall('\d+',item)
for item in output_num:
    po=str(po)+str('N')+str(item)+str(',')
po=po.rstrip(',')
nout=len(output_num)

wire_num=[]
wire=''
for item in internal_list:
    wire_num=wire_num+re.findall('\d+', item)

wire_num=sorted(set(wire_num),key=wire_num.index)


internal=wire_num
for item in input_num:
    if item in internal:
        wire_num.remove(item)

for item in output_num:
    if item in internal:
        wire_num.remove(item)

for item in wire_num:
    wire=str(wire)+str('N')+str(item)+str(',')
wire=wire.rstrip(',')
nwire=len(wire_num)
##print(wire_num)

connection=file_lines
for item in input_list:
    if item in file_lines:
        connection.remove(item)
for item in output_list:
    if item in file_lines:
        connection.remove(item)

count_list = len(connection)
for i in range(count_list):
    connection[i] = connection[i].strip('\n')
connection.remove('')
connection.remove('')
#print(connection)

        
    

verilog=open('c1355.v','w')
verilog.write('module c1355('+pi+','+po+');'+'\n\n')
verilog.write('input '+pi+';'+'\n\n')
verilog.write('output '+po+';'+'\n\n')
verilog.write('wire '+wire+';'+'\n\n')

a='AND'
b='NAND'
c='NOT'
d='OR'
e='BUFF'
numb=[]
number=''
count_n=''
i=0
j=0
k=0
l=0
m=0
n=0
o=0
p=0
q=0

for item in connection:
    if b in item:
        numb=numb+re.findall('\d+', item)
        for item in numb:
            number=str(number)+str('N')+str(item)+str(',')
        number=number.rstrip(',')
        verilog.write('nand NAND2_'+str(i)+'('+str(number)+');\n')
        i=i+1
    elif a in item:
        numb=numb+re.findall('\d+', item)
        count_n=len(numb)   
        for item in numb:
            number=str(number)+str('N')+str(item)+str(',')
        number=number.rstrip(',')
        if count_n==3:
            verilog.write('and AND2_'+str(j)+'('+str(number)+');\n')
            j=j+1
        elif count_n==4:
            verilog.write('and AND3_'+str(k)+'('+str(number)+');\n')
            k=l+1
        elif count_n==5:
            verilog.write('and AND4_'+str(l)+'('+str(number)+');\n')
            l=l+1
        elif count_n==6:
            verilog.write('and AND5_'+str(m)+'('+str(number)+');\n')
            m=m+1
    elif c in item:
        numb=numb+re.findall('\d+', item)
        for item in numb:
            number=str(number)+str('N')+str(item)+str(',')
        number=number.rstrip(',')
        verilog.write('not NOT1_'+str(n)+'('+str(number)+');\n')
        n=n+1   
    elif d in item:
        numb=numb+re.findall('\d+', item)
        for item in numb:
            number=str(number)+str('N')+str(item)+str(',')
        number=number.rstrip(',')
        verilog.write('or OR4_'+str(o)+'('+str(number)+');\n')
        o=o+1
    elif e in item:
        numb=numb+re.findall('\d+', item)
        for item in numb:
            number=str(number)+str('N')+str(item)+str(',')
        number=number.rstrip(',')
        verilog.write('buf BUFF1_'+str(p)+'('+str(number)+');\n')
        p=p+1
                
    numb=[]
    number=''
verilog.write('\n'+'endmodule')

verilog.close()
print(numb)
print(number)

    





    
  
