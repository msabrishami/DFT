from collections import defaultdict

file = open("fault_dic/add2.fd","r")
test_pattern_list = {}
all_test_pattern = defaultdict(set)
all_fault = defaultdict(set)
result = []
for i in file.readlines()[1:]:
    pattern = i.split()[0]
    fault = set() 
    for j in i.split()[1:]:
        fault.add(j) 
        all_fault[j].add(i.split()[0])
    test_pattern_list[i.split()[0]] = len(fault)
    all_test_pattern[pattern] = fault
file.close()

fault_number = len(all_fault)

#create a graph, with faults and test pattern as a node, 
#their relation is stored in dictionary
#test pattern list recorn the number of remaining fault haven't been detected(test pattern, number)
#all test pattern store all the faults this test pattern can detect(test pattern, fault)
#all fault store the test pattern that can detect this fault(fault, test pattern)

#print these information from the file, it create a graph from two side, 
# the test pattern side and the fault side, test pattern list just a helper 
#sorted(test_pattern_list, key=lambda x: x.number)

#print information
#print("all_fault")
#for key,val in all_fault.items():
#      print (key, " ", val)

#print("\nall_test_pattern")
#for key,val in all_test_pattern.items():
#       print (key, " ", val)

#print("\ntest_pattern_list")
#for key,val in test_pattern_list.items():
#       print (key, " ", val)

#take_pattern = []

#use greedy to find the reduced test pattern, always find the test pattern that can detect
#the most remaining fault, the program will end when all the faults are detected, time complexity O(V + E)
#the meaningful graph contains all the fault, we want to find the least test pattern that connects
#to all the fault
#start from the most promising test pattern, find all the connections, then we can enlarge the graph
#by finding the second promising test pattern
#three steps to realize it: 
# 1.find a test pattern and its connected faults 
# 2.delete the connections for other test pattern related to these node
# 3.delete the fault node and test pattern node

while (len(all_fault) != 0):
    #find a test pattern that contains the most remaining fault
    maxPattern = max(test_pattern_list, key = test_pattern_list.get) 
    #print(maxPattern)

    #get all the fault related to this test pattern 
    #and check whether this test pattern exists in the graph
    temp = all_test_pattern.get(maxPattern)
     #print (temp)

    #we want to delete these fault in the graph, when the test pattern exists
    if temp != None:
        #add the test pattern we find
        result.append(maxPattern)
        for i in temp: 
        # get all fault related to the test pattern, and iterate it and delete 
        # from the graph for bothe edges and node
            
            if all_fault.get(i) != None:
                #step 1: delete the edges from the graph by updating the number 
                #of connection in test_pattern_list, from the test pattern side
                for j in all_fault.get(i): # get the test pattern related to the fault
                 #print(test_pattern_list.get(j))
                    #update the connection by deleting the connection between
                    #this test pattern and the node in the test pattern list. If it is 
                    #the only connection for this test pattern, we can remove the test
                    #pattern since no fault will be connected with it and it is outside 
                    #the graph
                    if test_pattern_list.get(j) != None:
                        remain = test_pattern_list.get(j) - 1 
                     #print(i,j,remain)
                        if remain > 0:
                            test_pattern_list.update({j:remain})
                        if remain == 0:
                            test_pattern_list.pop(j)
                            #all_test_pattern.pop(j)
            # step 2: delete the fault node when it exists in the graph
                all_fault.pop(i)
            # step 3: delete the test pattern
        if test_pattern_list.get(maxPattern) != None:
            #all_test_pattern.pop(maxPattern)
            test_pattern_list.pop(maxPattern)

print(result)

#check correctness
detected = set()
for a in result:
    detected.update(all_test_pattern.get(a))
print(len(detected))
print(fault_number)



