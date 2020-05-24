def equv_domain():
	# dict_for_equv is a map, index is every fault after rfl, value is all the input patterns that could test this fault
	dict_for_equv = {}
	file = open("../tests/fault_dict.txt","r")
	for i in file.readlines()[2:]:
		input_pattern = i.split()[0]
		for j in i.split()[1:]:
			if dict_for_equv.get(j) != None:
				dict_for_equv.get(j).append(input_pattern)
			else :
				dict_for_equv.update({j:[input_pattern]})
	file.close()
	# print(dict_for_equv)

	equv_fault_list = []	#each element is a list, contains equv relation
	domain_fault_list = {}  #key is the fault that can be ignored(which means key is larger)
	# if you want the value to be the fault that can be ignored, change issuperset to issubset
	temp_equv_fault_list = []
	temp_domian_fault_list = []
	full = open('../tests/full_fault_list.txt','r')
	full_fault_list = full.readlines()
	full.close()
	for i in range(len(full_fault_list)):	#delete \n after every line
		full_fault_list[i] = full_fault_list[i].split('\n')[0]
	equc_full_fault_list = full_fault_list.copy()	#full fault list used in equv
	domain_full_fault_list = full_fault_list.copy()	#full fault list used in domain
# equv 
	while full_fault_list != []:
		temp_equv_fault_list.clear()
		temp_equv_fault_list.append(full_fault_list[0])
		full_fault_list.remove(full_fault_list[0])
		for jtem in full_fault_list:
			if(set(dict_for_equv.get(temp_equv_fault_list[0])) == set(dict_for_equv.get(jtem))):
				temp_equv_fault_list.append(jtem)
				full_fault_list.remove(jtem)
		equv_fault_list.append(temp_equv_fault_list.copy())
# domain
	for item in domain_full_fault_list:
		temp_domian_fault_list.clear()
		for jtem in domain_full_fault_list:
			if (item != jtem):
				# if (set(dict_for_equv.get(item)) != set(dict_for_equv.get(jtem))): #delete equv situation
				if (set(dict_for_equv.get(item)).issuperset(set(dict_for_equv.get(jtem)))):
				# if (set(dict_for_equv.get(item)).issubset(set(dict_for_equv.get(jtem)))):
					temp_domian_fault_list.append(jtem)
		domain_fault_list.update({item:temp_domian_fault_list.copy()})
# write euqv result to txt file
	equv_faultlist_file = open("../tests/equv_faultlist.txt","w")
	for i in range(len(equv_fault_list)):
		equv_faultlist_file.write('%s\n' %equv_fault_list[i])
	equv_faultlist_file.close()
# write domain result to txt file
	domain_faultlist_file = open("../tests/domain_faultlist.txt","w")
	for i in domain_fault_list.keys():
		domain_faultlist_file.write('%s:%s\n' %(i, domain_fault_list[i]))
	domain_faultlist_file.close()
# return the result to see if it's correct	
	equv_domain_fault_list = [equv_fault_list,domain_fault_list]
	return equv_domain_fault_list
