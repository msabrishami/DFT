from collections import defaultdict

file = open("../tests/fault_dict.txt","r")
test_pattern_list = {}
all_test_pattern = defaultdict(set)
all_fault = defaultdict(set)
result = []
for i in file.readlines()[2:]:
    pattern = i.split()[0]
    fault = set()
    for j in i.split()[1:]:
        fault.add(j)
        all_fault[j].add(i.split()[0])
    test_pattern_list[i.split()[0]] = len(fault)
    all_test_pattern[pattern] = fault
file.close()

#sorted(test_pattern_list, key=lambda x: x.number)
#for key,val in all_fault.items():
#       print (key, " ", val)

#for key,val in all_test_pattern.items():
#       print (key, " ", val)

take_pattern = []
while (len(all_fault) != 0):
    maxPattern = max(test_pattern_list, key = test_pattern_list.get) #find a test pattern
    print(maxPattern)
    result.append(maxPattern)

    for i in all_test_pattern.pop(maxPattern): # get all fault related to the test pattern
        for j in all_fault.get(i): # get the test pattern related to the fault
            remain = test_pattern_list.get(j) - 1 
            print(i,j,remain)
            if remain > 1:
                test_pattern_list.update({j:remain-1})
            if remain == 1:
                test_pattern_list.pop(j)

print(result)
       

#for key,val in test_pattern_list.items():
#    print (key, " ", val)

#for i in all_test_pattern:
#    print (i.pattern)
#    print (i.fault)





