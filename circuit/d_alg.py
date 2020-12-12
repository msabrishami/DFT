import copy
from enum import Enum
# from classdef import five_value
import json
from collections import OrderedDict 
import os, sys
sys.setrecursionlimit(10000)

'''
Last Modification: 12/12
Works well: c1, c2, c3, c4, FA, FA_NAND, add2, c17, cmini, c880
Some tests not correct: c432 ((N199-2,0), (N296-2,0), (N296-1,1), (N357-1,0), (N399-1,0))
Some tests have infinite loop: c499 (like: N113)
Note:
    only suitable for 2-input XOR / XNOR

'''

class D_alg:
    ################### change initial, add fault conversion
    def __init__(self, circuit, fault_node, fault_val, count_limit):
        """
        fault_node: the node number that has fault
        fault_val: 0: SA0    1: SA1
        """
        self.circuit = circuit
        # fault sim type: dfs / pfs
        self.fs_type = ""
        # forward and backward imply stacks
        self.S_fwd = []
        self.S_bwd = []
        self.D_frontier = []
        self.J_frontier = []
        self.eval_node = []
        # store the node.value, J_frontier
        self.checkpoint_val = []
        self.checkpoint_J = []
        self.checkpoint_D = []
        self.checkpoint_eval = []

        # to see if the elem has been chosen, avoid repeating
        self.used_J = {}

        #for observation
        self.dalg_cnt = 0
        self.fwd_cnt = 0
        self.bwd_cnt = 0
        self.d_cnt = 0

        self.count_limit = count_limit

        # convert the input fault to 5-val
        # fault_val = 1: 0/1---D'    fault_val = 0: 1/0---D  
        self.fault_node = fault_node
        if fault_val == 1:
            self.fault_val = 3
        elif fault_val == 0:
            self.fault_val = 12
        # initialize all nodes to X(9)
        for i in self.circuit.nodes_lev:
            i.value = 9

        ############ initialize used_J
        for elem in self.circuit.nodes_lev:
            self.used_J[elem.num] = 0



    # input: node name, value
    def Imply_Check(self, node, val):
        # forward implication
        # if the dnodes has BRCH, then all the dnodes are BRCH
        # in this case, we can directly assign val to dnodes and put their dnode in front of S_fwd     


        # if no BRCH, it must have only 1 dnode
        print ("S_fwd: ************  START  *************")
        center_node = node
        print("FWD center node: ", center_node.num, "---------", center_node.value)
        for dnode in center_node.dnodes:
            self.S_fwd.append(dnode)
            print(dnode.num)
        print (self.S_fwd)
        print('\n')

        # do recursive I&C until the stack is empty
        while self.S_fwd:
            if self.fwd_cnt > self.count_limit:
                self.fwd_cnt = 0
                print("fwd cnt out of range!!!!!!!!")
                return 0
            else:
                self.fwd_cnt = self.fwd_cnt + 1
                node = self.S_fwd.pop()
                if node in self.eval_node:
                    if not self.fwd_imply_check_5val(node):
                        print("Node is already evaluated, but check is wrong!!")
                        return 0
                    print("Node is already evaluated, and check is correct!!")
                
                elif node not in self.eval_node:
                    if not self.fwd_imply_check_5val(node):
                        print("ERROR fwd: " + node.num + '----' + str(node.value) + '\n')
                        return 0
                    print(node.num + '----' + str(node.value) + '\n')
                    if node.value == 9:
                        continue
                    ## 12.4: prob2 solve: should add during fwd
                    # 12.5: if the output is not X, we can remove it from D frontier
                    if node in self.D_frontier:
                        self.D_frontier.remove(node)
                        print("Remove from D frontier: already evaluated:  ", node.num)

                    print ("S_fwd")
                    for dnode in node.dnodes:
                        self.S_fwd.append(dnode)
                        print(dnode.num)
                    print (self.S_fwd)
                    print('\n')

        print ("S_bwd: ************  START  *************")
        print("BWD center node: ", center_node.num, "---------", center_node.value)
        for unode in center_node.unodes:
            self.S_bwd.append(unode)
            print(unode.num , ": " , unode.value)
        print (self.S_bwd)
        print ('\n')
        
        # do recursive I&C until the stack is empty
        while self.S_bwd:
            if self.bwd_cnt > self.count_limit:
                self.bwd_cnt = 0
                print("bwd cnt out of range!!!!!!!!")
                return 0
            else:
                self.bwd_cnt = self.bwd_cnt + 1
                node = self.S_bwd.pop()
                if node in self.eval_node:
                    if not self.bwd_imply_check_5val(node):
                        return 0
                if node not in self.eval_node:
                    if not self.bwd_imply_check_5val(node):
                        print("ERROR bwd:  " + node.num + '----' + str(node.value) + '\n')
                        return 0
                    print("BWD Result: " + node.num + '----' + str(node.value))
                    print("BWD Result: " + str(node.dnodes[0].unodes_val()) + '\n')
                    
                    if node.value == 9:       # stop implying
                        continue

                    if node.gtype != "BRCH":
                        if node not in self.eval_node:
                            self.eval_node.append(node)

                    if node.dnodes[0].gtype != "BRCH":
                        if node not in self.eval_node:
                            self.eval_node.append(node)
                    else:
                        print("I'm stem or brch, and I have value now! Check again! ")
                        if not self.Imply_Check(node, node.value):
                            return 0

                    print ("S_bwd: ************  END  ************")
                    for unode in node.unodes:
                        self.S_bwd.append(unode)
                        print(unode.num , ": " , unode.value)
                    print (self.S_bwd)
                    print ('\n')

                else:
                    print(node.num, " is already evaluated!!!")

        return 1



    def fwd_imply_check_5val(self, node):
        """
        Forward Imply and Check
        The input is node type (the output of gates, should be assigned)
        we use its unodes to imply the node value
        Note that during fwd, it's likely to remove elem from D frontier
        """
        # forward imply, get the value of its only dnode
        # in ntype, Fb includes PO
        # first calculate a temp value, see if any conflict exit at the end
        if node.gtype == 'BRCH':
            temp_val = node.unodes[0].value

        elif node.gtype in ['NAND', 'AND', 'NOR', 'OR']:
            temp_val = self.fwd_imply_5val_gen(node)
        

        elif node.gtype == 'XNOR':
            unodes_value = unodes_val_list(node)
            # if inputs have x
            if (9 in unodes_value ):
                temp_val = 9
                flag = 1
                if (12 in unodes_value) | (3 in unodes_value):
                    if node not in self.D_frontier:
                        self.D_frontier.append(node)
                        print("**********Add D front:  " + node.num)
                        flag = 2
            else:
                temp_val = unodes_value[0] ^ unodes_value[1] ^ 15
                flag = 1
        
        elif node.gtype == 'XOR':
            unodes_value = unodes_val_list(node)
            # if inputs have x
            if (9 in unodes_value ):
                temp_val = 9
                flag = 1
                if (12 in unodes_value) | (3 in unodes_value):
                    if node not in self.D_frontier:
                        self.D_frontier.append(node)
                        print("**********Add D front:  " + node.num)
                        flag = 2
            else:
                temp_val = unodes_value[0] ^ unodes_value[1]
                flag = 1
        
        elif node.gtype == 'NOT':
            unodes_value = unodes_val_list(node)
            # if input is x
            if (unodes_value[0] == 9):
                temp_val = 9
            else:
                temp_val = unodes_value[0] ^ 15
            flag = 1
        elif node.gtype == 'BUFF':
            unodes_value = node.unodes_val()
            if (unodes_value[0] == 9):
                temp_val = 9
            else:
                temp_val = unodes_value[0]
            flag = 1


        # check if any conflict
        if self.fwd_check_5val_gen(node, temp_val):
            # if the evaluation result is X
            # regardless of its previous value, we shouldn't add it to eval nodes
            if temp_val != 9:
                self.eval_node.append(node)
                # if temp_val != 9, means the inputs can imply output
                # the output node should be remove from J & Dfrontier
                if node in self.J_frontier:
                    self.J_frontier.remove(node)
                if node in self.D_frontier:
                    self.D_frontier.remove(node)
                
            return 1
        else:
            return 0
        




    def bwd_imply_check_5val(self, node):
        """
        Backward Imply and Check
        Node: gate input, from the gate output imply current input
        """
        print("BWD: " + node.num + ": " + str(node.value))
        if node.dnodes[0].gtype == 'BRCH':
            print("Hello I'm the stem of BRCH!!!")

            # the stem has been assigned
            # add other branches to dnode value set
            dnodes_val = dnodes_val_set(node)

            print("dnode value set: ", dnodes_val)

            if node.value != 9:
                # compare to see if any conflict, no need to assign to stem
                # remove the X since it won't cause conflict
                if 9 in dnodes_val:
                    dnodes_val.remove(9)
                # the rest brach values can be 0, 1, D', D
                # the branches have the same value
                if len(dnodes_val) == 1:
                    return 1
                elif len(dnodes_val) == 2:
                    if (15 in dnodes_val) & (12 in dnodes_val):
                        return 1
                    elif (0 in dnodes_val) & (3 in dnodes_val):
                        return 1
                    else:
                        return 0
                # the branch have more than 3 value
                else:
                    return 0
            # the stem has not been assigned
            else:
                # check other branches, assign to stem
                if (15 in dnodes_val) | (12 in dnodes_val):
                    node.value = 15
                elif (0 in dnodes_val) | (3 in dnodes_val):
                    node.value = 0
                return 1

                

        elif node.dnodes[0].gtype in ['NAND', 'AND', 'NOR', 'OR']:
            print("Hello I'm a input of ", node.dnodes[0].gtype)
            if self.bwd_imply_check_5val_gen(node):
                return 1
            else:
                return 0

        ############# 12.7 XOR XNOR
        elif node.dnodes[0].gtype == 'XNOR':
            print("Hello I'm a input of ", node.dnodes[0].gtype)
            val = node.dnodes[0].value
            unodes_value = unodes_val_list(node.dnodes[0])
            # if the output is not X #####
            # if 2 inputs are both X
            if (unodes_value[0] == 9) and (unodes_value[1] == 9):
                if node.dnodes[0] not in self.J_frontier:
                    self.J_frontier.append(node.dnodes[0])
                    print("**********Add J front:  " + node.dnodes[0].num)
                    return 2
                if node.dnodes[0] in self.eval_node:
                    self.eval_node.remove(node.dnodes[0])
                    print("Already in J front: remove from eval_node")
                return 1

            # if 1 input is X and node.value is X
            elif (node.value == 9):
                if (unodes_value[0] == 9):
                    temp_val = val ^ unodes_value[1]
                else:
                    temp_val = val ^ unodes_value[0]
                
                if (val in [0,15] ) and (temp_val in [3,12]):
                    return 0
                else:
                    node.value = temp_val
                    # input cannot be D or D'
                    if temp_val in [3,12]:
                        node.value = temp_val ^ 3

                # 12.5: two inputs can be known
                if node.dnodes[0] in self.J_frontier:
                    self.J_frontier.remove(node.dnodes[0])
                return 1
            # if 1 input is X
            elif (9 in unodes_value):
                if (node.value in [3,12]) and (val in [0,15]):
                    return 0
                return 1            
            # 2 inputs are not X
            # if output != input1 ^ input2 ^15
            else:
                if val != (unodes_value[0] ^ unodes_value[1] ^ 15):
                    # if output is D or D'
                    if val != (unodes_value[0] ^ unodes_value[1] ^ 15 ^ 3):
                        return 0
                return 1
        
        
        elif node.dnodes[0].gtype == 'XOR':
            print("Hello I'm a input of ", node.dnodes[0].gtype)
            val = node.dnodes[0].value
            unodes_value = unodes_val_list(node.dnodes[0])
            # if the output is not X#####
            # if 2 inputs are both X
            if (unodes_value[0] == 9) and (unodes_value[1] == 9):
                if node.dnodes[0] not in self.J_frontier:
                    self.J_frontier.append(node.dnodes[0])
                    print("**********Add J front:  " + node.dnodes[0].num)
                    return 2
                if node.dnodes[0] in self.eval_node:
                    self.eval_node.remove(node.dnodes[0])
                    print("Already in J front: remove from eval_node")
                return 1

            # if 1 input is X and node.value is X
            elif (node.value == 9):
                if (unodes_value[0] == 9):
                    temp_val = val ^ unodes_value[1]
                else:
                    temp_val = val ^ unodes_value[0]
                
                if (val in [0,15]) and (temp_val in [3,12]):
                    return 0
                else:
                    node.value = temp_val
                    # input cannot be D or D'
                    if temp_val in [3,12]:
                        node.value = temp_val ^ 3
                
                # 12.5: two inputs can be known
                if node.dnodes[0] in self.J_frontier:
                    self.J_frontier.remove(node.dnodes[0])
                return 1
            # if 1 input is X
            elif (9 in unodes_value):
                if (node.value in [3,12]) and (val in [0,15]):
                    return 0
                return 1   
            # 2 inputs are not X
            # if output != input1 ^ input2 ^15
            else:
                if val != (unodes_value[0] ^ unodes_value[1]):
                    if val != (unodes_value[0] ^ unodes_value[1] ^ 3):
                        return 0
                return 1

        elif node.dnodes[0].gtype == 'NOT':
            print("Hello I'm a input of ", node.dnodes[0].gtype)
            val = node.dnodes[0].value
            # if the input is X
            if node.value == 9:
                if val in [0, 15]:
                    node.value = val ^ 15
                # out = D, in should be 0->1--1/0 D
                # out = D', in should be 1->0--0/1 D'
                else:
                    node.value = val ^ 3 ^ 15
                return 1
            else:
                if node.value != val ^ 15:
                    if node.value != val ^ 15 ^ 3:
                        return 0
                return 1

        
        elif node.dnodes[0].gtype == 'BUFF':
            print("Hello I'm a input of ", node.dnodes[0].gtype) 
            val = node.dnodes[0].value
            unodes_value = node.dnodes[0].unodes_val()
            # if the input is X
            if (node.value == 9):
                node.value = val
                if val in [3, 12]:
                    node.value = node.value ^ 3
                return 1
            else:
                if node.value != val:
                    if node.value != val ^ 3:
                        return 0
                return 1
            


    def dalg_recur(self, node_num, val):
        if self.dalg_cnt > self.count_limit:
            self.dalg_cnt = 0
            print("dalg recursive cnt out of range!!!!!!!!")
            return 0
        else:
            self.dalg_cnt = self.dalg_cnt + 1

            node = self.circuit.nodes[node_num]
            node.value = val
            if not self.Imply_Check(node,val):
                print("I AND C wrong")
                self.S_fwd.clear()
                self.S_bwd.clear()
                print("FAIL: Return back to last dalg\n")
                return 0
            if not self.err_at_PO():
                if len(self.D_frontier) == 0:
                    print("ERROR NOT PO:  D frontier is empty!!")
                    print("FAIL: Return back to last dalg\n")
                    return 0
                else:
                    po_val = set()
                    for po in self.circuit.PO:
                        po_val.add(po.value)
                    print(po_val)
                    if (12 not in po_val) & (3 not in po_val) & (9 not in po_val):
                        print("ERROR NOT PO:  D frontier is not empty!! Should choose another")
                        print("FAIL: Return back to last dalg\n")
                        return 0


                #############################################################
                ##                D frontier assignment
                #############################################################
                while (len(self.D_frontier) != 0):
                    if self.d_cnt > self.count_limit:
                        self.d_cnt = 0
                        print("d front assmt cnt out of range!!!!!!!!")
                        return 0
                    else:
                        self.d_cnt = self.d_cnt + 1

                        print("D_frontier before poping: ")
                        self.print_node(self.D_frontier)
                        d_fr_node = self.D_frontier.pop() #should be in string format
                        print("Pop D front:  " + d_fr_node.num)



                        for unode in d_fr_node.unodes:
                            print("For d_fr_node ", d_fr_node.num, "'s unodes:")
                            print(unode.num + ': ' + str(unode.value))
                            if unode.value == 9:
                                # if the gate type is XOR, it has no cval, we can assign either 0 or 1
                                # 12.5: 
                                # by default: assign 1, but we cannot move it from D frontier
                                # if error occurs, we assign 0 to it, then we can remove it
                                # the following code did this

                                for elem in self.circuit.nodes_lev:
                                    self.used_J[elem.num] = 0


                                ################## should save checkpoint when you assign!!!! Not pop!!!!!
                                #######################################
                                #####    save the check points    #####
                                #######################################
                                print("D frontier: new assignment, save the checkpointing")
                                self.save_checkpoint()
                                

                                if d_fr_node.gtype in ["XOR", "XNOR"]:
                                    if not d_fr_node.c_flag:
                                        unode.value = 15
                                        d_fr_node.c_flag = 1 
                                    else:
                                        unode.value = 0
                                        d_fr_node.c_flag = 0
                                    print("Assign XOR / XNOR: " + unode.num + "---" + str(unode.value))
                                # if the gate type is AND, OR, NAND, NOR
                                else:
                                    unode.value = d_fr_node.cval ^ 15
                                    print("Assign: " + unode.num + "---" + str(unode.value))
                                
                                print("D frontier after poping: ")
                                self.print_node(self.D_frontier)


                                if self.dalg_recur(unode.num,unode.value):
                                    print("DALG_RECUR:  D frontier assignment successed! ")
                                    print("SUCCESS: Return back to last dalg\n")
                                    return 1
                                # the latest D frontier choice is wrong
                                # we should recover our previous node values, then choose another
                                else:
                                    print("DALG FAIL: Wrong D front choice: should recover previous node values")
                                    print("Fail node: ", d_fr_node.num)
                                    print("Recover previous node values......")

                                    if not self.recover_checkpoint():
                                        return 0

                                    if (d_fr_node.gtype in ["XOR","XNOR"]):
                                        if (d_fr_node.c_flag == 1):
                                            self.D_frontier.append(d_fr_node)
                                            print("**********XOR / XNOR wrong assignment: add bakc D front:  " + node.num)

                            else:
                                print("The unode is not X!! ", unode.num, ": ", unode.value)
                print("FAIL: Return back to last dalg\n")
                return 0
            
            
            # error propagated to a PO
            print("\n\n")
            print("Fault already propagated to PO!! We can only focus on J front")
            self.print_node(self.circuit.PO)
            print("J frontier length: ", len(self.J_frontier))
            if len(self.J_frontier) == 0:
                print("J frontier empty")
                print("SUCCESS: Return back to last dalg\n")
                return 1
            
            # when we make an assignment from J frontier, we need to save checkpoints
            # if we need to reverse the decision, we have to recover the previous checkpoints
            #############################################################
            ##                J frontier assignment
            #############################################################
            j_fr_node = self.J_frontier.pop()
            print("Pop first J front:  " + j_fr_node.num)
            ###### 12.8:  (FUNC?)  when pop from J frontier, see if it's tried and failed within the D choice
            j_used_status = self.used_J[j_fr_node.num]
            print("J used status: ", self.used_J[j_fr_node.num])
            # if the status = 1: already tried and failed! should choose anotehr one
            while(j_used_status == 1):
                print("The J elem has been tried and failed! Choose another! Fail: ", j_fr_node.num)
                if not self.J_frontier:
                    print("J frontier is empty!! No more choice!!")
                    print("SUCCESS: Return back to last dalg\n")
                    return 1
                j_fr_node = self.J_frontier.pop()
                j_used_status = self.used_J[j_fr_node.num]

            print("Pop J front:  " + j_fr_node.num + '\n')
            print("J front rest:  ", self.print_node(self.J_frontier),"   length: ",  len(self.J_frontier), '\n')
            
            for unode in j_fr_node.unodes:
                if unode.value == 9:
                    #######################################
                    #####    save the check points    #####
                    #######################################
                    print("J frontier: new assignment, save the checkpointing")
                    self.save_checkpoint()

                    # if the gate type is XOR, it has no cval
                    if j_fr_node.gtype in ["XOR", "XNOR"]:
                        # first: assign 1
                        # j_jr_node.c_flag=0: means we haven't assign any input
                        if not j_fr_node.c_flag:
                            unode.value = 15
                            j_fr_node.c_flag = 1
                        # second: assign the same as backward imply
                        else:
                            if j_fr_node.value in [15, 12]:
                                unode.value = 0
                            elif j_fr_node.value in [0, 3]:
                                unode.value = 15             
                            j_fr_node.c_flag = 0
                        print("Assign: " + unode.num + "---" + str(unode.value))
                        #### 12.4 prob1 solve: every time assign to J, clear the eval nodes
                        print("Clear the eval_nodes......")
                        self.eval_node.clear()


                        if self.dalg_recur(j_fr_node.num, j_fr_node.value):
                            print("J frontier choice correct! ")
                            print("SUCCESS: Return back to last dalg\n")
                            return 1
                    
                    # if the gate type is AND, OR, NAND, NOR
                    else:
                        unode.value = j_fr_node.cval
                        print("Assign: " + unode.num + "---" + str(j_fr_node.cval))
                        if self.dalg_recur(unode.num, unode.value):
                            print("J frontier choice correct! ")
                            # self.print_PI()
                            # self.print_all()
                            print("SUCCESS: Return back to last dalg\n")
                            return 1


                    ################# Reverse the decision #######################
                    # the dalg failed, we need to reassign the inverse value to J front elem
                    print("DALG FAIL: Reverse the decision in J frontier assignment")
                    print("Re-assign for input of: ", j_fr_node.num)
                    print("Recover preovious node values......")

                    for elem in self.circuit.nodes_lev:
                        self.used_J[elem.num] = 0

                    if not self.recover_checkpoint():
                        return 0

                    self.save_checkpoint()

                    # if the gate type is XOR, it has no cval
                    if j_fr_node.gtype in ["XOR", "XNOR"]:
                        unode.value = 0
                        print("Assign: " + unode.num + "---" + str(unode.value) + '\n')
                        if self.dalg_recur(j_fr_node.num, j_fr_node.value):
                            print("J frontier reverse choice correct! ")
                            print("SUCCESS: Return back to last dalg\n")
                            return 1
                    # if the gate type is AND, OR, NAND, NOR, assign the inverse value
                    else:
                        unode.value = j_fr_node.cval ^ 15
                        print("Assign: " + unode.num + "---" + str(unode.value) + '\n')
                        if self.dalg_recur(unode.num, unode.value):
                            print("J frontier reverse choice correct! ")
                            print("SUCCESS: Return back to last dalg\n")
                            return 1
                    
            if not self.recover_checkpoint():
                return 0
            print("J reverse failed again: ", j_fr_node.num)


            self.used_J[j_fr_node.num] = 1
            print("J used status: ", self.used_J[j_fr_node.num])   


            print("END")
            print("J frontier elem: all inputs failed!!!!  Back to D frontier to find another elem")
            print("FAIL: Return back to last dalg\n")
            return 0




    def test(self):
        # blockPrint()
        if self.dalg_recur(self.fault_node, self.fault_val):
            print("\n\n")
            print("==================== END FOUND  ========================")
            self.print_PI()
            self.print_all()
            for node in self.circuit.nodes_lev:
                if node.gtype in ["XOR", "XNOR"]:
                    node.c_flag = 0
            print("XOR / XNOR c_flag reset is finish!\n")
            return 1
        else:
            print("\n\n")
            print("==================== END NOT FOUND  ========================")
            self.print_PI()
            self.print_all()
            for node in self.circuit.nodes_lev:
                if node.gtype in ["XOR", "XNOR"]:
                    node.c_flag = 0
            print("XOR / XNOR c_flag reset is finish!\n")
            return 0





    def return_IPT(self):
        """
        Return the generated test pattern
        Return: a list of PI value, in the order of self.ciruit.PI
        """
        PI_list = []
        for node in self.circuit.PI:
            PI_list.append(node.value)
        return PI_list



        
    def fwd_imply_5val_gen(self, node):
        """
        General Function for forward imply
        For: NAND, AND, NOR, OR
        Need controling value and inversion
        cval and inv are both 5-value
        """
        print("FWD: type: " + node.gtype)
        # the expected output when input has cval
        cval = node.cval
        inv = node.inv
        cout = cval ^ inv

        unodes_value = unodes_val_set(node)

        print("Unode value: " + str(unodes_value) + '\n')
        print("INV: " + str(inv) + "    CVAL: " + str(cval))
        if (cval in unodes_value):
            temp_val = cout
            flag = 1
            if node in self.J_frontier:
                print("Inputs already have cval! Remove from J frontier: ", node.num)
                self.J_frontier.remove(node)
        # no controling value in inputs
        else:
            # inputs have D and D'
            if (12 in unodes_value) & (3 in unodes_value):
                temp_val = cout
                flag = 1
            # inputs have X
            elif (9 in unodes_value):
                temp_val = 9
                if (12 in unodes_value) | (3 in unodes_value):
                    if node not in self.D_frontier:
                        self.D_frontier.append(node)
                        print("**********Add D front:  " + node.num)
                        flag = 2
                flag = 1
            # inputs have only D and 1
            elif (12 in unodes_value):
                temp_val = 12 ^ inv
                flag = 1
            # inputs have only D' and 1
            elif (3 in unodes_value):
                temp_val = 3 ^ inv
                flag = 1
            # inputs have only non c
            else:
                temp_val = cout ^ 15
                flag = 1
        print("FWD Imply Result: " + str(temp_val) + '\n')
        return temp_val


    # 12.5: when temp_val = 9 but node already has value, put the node's unodes to S_bwd
    def fwd_check_5val_gen(self, node, temp_val):   
        """
        General Function for forward check
        For: all types
        """
        print("General FWD: ", node.gtype)
        if temp_val == 9:
            print("Imply result is X, no conflict!")
            # if the node already has value, put the unodes of the node to S_bwd
            # maybe we can backward imply the other inputs!
            if node.value != 9:
                for unode in node.unodes:
                    self.S_bwd.append(unode)
            return 1
        if node.value == 9:
            node.value = temp_val
            print("node is X: " + str(temp_val))
            return 1
        # conflict
        elif node.value != temp_val:
            if (node.value == 12) & (temp_val == 15):
                print("node is not X, but no conflict, activate D: " + str(temp_val))
                return 1
            elif (node.value == 3) & (temp_val == 0):
                print("node is not X, but no conflict, activate D': " + str(temp_val))
                return 1
            # conflict, or fault cannot be activated
            else:
                print("node is not X, conflict: " + str(temp_val))
                return 0
        else:
            print("node is not X, but no conflict: " + str(temp_val))
            return 1




    
    def bwd_imply_check_5val_gen(self, node):
        """
        General Function for backward imply
        For: NAND, AND, NOR, OR
        Need controling value and inversion
        cval and inv are both 5-value
        input node: a input of the evaluated gate
        Note that during bwd, it's likely to remove elem in J frontier
        """
        print("BWD: type: " + node.dnodes[0].gtype)
        cval = node.dnodes[0].cval
        inv = node.dnodes[0].inv
        cout = cval ^ inv        # the expected output when input has cval
        cout_bar = cout ^ 15     # the expected output when input are all non-cval
        cval_bar = cval ^ 15     # the non-c value
        print("cout: "+str(cout)+"  cout_bar: "+str(cout_bar)+"  cval_bar: "+str(cval_bar)+'\n')

        val = node.dnodes[0].value
        unodes_value = unodes_val_set(node.dnodes[0])

        print("dnode: " + node.dnodes[0].num + ":  " + str(val) + '\n')
        print("unodes values: " + str(unodes_value) + '\n')
        # in the backward imply, input cannot have D / D'
        # c-val in inputs: the output is 1 or 1/0: D
        # return value:   1: no conflict, no J;  0: conflict;  2: no conf, J
        if (cval in unodes_value):
            # if input has cval, cannot imply any other input
            # 12.5: J front elem should be remove
            if ((val == cout) | (val == cout ^ 3)):
                if node.dnodes[0] in self.J_frontier:
                    print("Inputs already have cval! Remove from J frontier: ", node.dnodes[0].num)
                    self.J_frontier.remove(node.dnodes[0])

                return 1
            else:
                print("BWD:  Conflict:  In has cval , but out is not cout/fault")
                return 0

        # no c-val in inputs, so if the inputs have fault, it must can be propagated
        else:
            # count how many X in inputs
            x_list = []
            for unode in node.dnodes[0].unodes:
                if unode.value == 9:
                    x_list.append(unode)
            x_num = len(x_list)

            if (val == cout_bar):
                # input has no cval, output has no fault
                # if fault free: output = cout_bar, means all input = cval_bar
                if (12 in unodes_value) | (3 in unodes_value):
                    print("BWD:  Conflict:  In has fault & no-cval , but out is not cout/fault")
                    return 0
                else:
                    for unode in node.dnodes[0].unodes:
                        unode.value = cval_bar
                    return 1

                
            elif (val == 3 ^ cout_bar):
                # 3 ^ cout_bar: means the fault can be activated when the output is cout_bar
                # if fault free: output = cout_bar, means all input = cval_bar
                # input: no cval, and fault has been propagated, so the inputs other than fault is cval_bar
                # input: if fault' exist, or no fault, then conflict
                # fault: activated by cval_bar, = cval_bar^3;
                # fault': activated by cval, = cval^3
                if (cval^3 in unodes_value):
                    print("BWD:  Conflict:  In has wrong fault, but out is fault")
                    return 0
                # only fault & X in inputs
                # case1: input has fault & X
                # case2: input has only X
                # since the input should be all cval_bar, these two cases are the same
                else:
                    for unode in node.dnodes[0].unodes:
                        if unode.value == 9:
                            unode.value = cval_bar
                    return 1


            
            elif (val == 3 ^ cout):
                # 3 ^ cout: means the fault can be activated when the output is cout
                # if fault free: output = cout, means at least 1 input is cval
                # input: no cval, can only be X, D, D'
                # input: if fault' exist, or no fault, then conflict
                # fault: activated by cval, = cval^3;
                # fault': activated by cval_bar, = cval_bar^3
                if cval_bar^3 in unodes_value:
                    print("BWD:  Conflict:  In has wrong fault, but out is fault")
                    return 0
                # input has fault and X, the fault has to be propagated
                elif cval^3 in unodes_value:
                    for unode in node.dnodes[0].unodes:
                        if unode.value == 9:
                            unode.value = cval_bar
                    return 1   
                # no fault in input, all X
                # input should have 1 cval, put it into J frontier
                else:
                    if node.dnodes[0] not in self.J_frontier:
                        self.J_frontier.append(node.dnodes[0])
                        print("**********Add J front:  " + node.dnodes[0].num)
                        return 2
                    if node.dnodes[0] in self.eval_node:
                        self.eval_node.remove(node.dnodes[0])
                        print("Already in J front: remove from eval_node") 
                    return 1

            
            elif (val == cout):
                # the inputs have at least 1 cval
                # no cval, if only 1 X, X=cval
                # if no conflict and input has >1 X, put it into J_frontier
                if (9 in unodes_value):
                    if (x_num == 1):
                        # input has only 1 X, imply: X=cval
                        print(str(unodes_value) + '\n')
                        print("cval is " + str(cval) + '\n')
                        x_list[0].value = cval
                        if node.dnodes[0] in self.J_frontier:
                            print("Remove from J frontier: inputs already have cval: ", node.dnodes[0].num)
                            self.J_frontier.remove(node.dnodes[0])
                        return 1
                    else:
                        # X >= 2, put it in J frontier if haven't been there
                        if node.dnodes[0] not in self.J_frontier:
                            self.J_frontier.append(node.dnodes[0])
                            print("**********Add J front:  " + node.dnodes[0].num)
                            return 2
                        if node.dnodes[0] in self.eval_node:
                            self.eval_node.remove(node.dnodes[0])
                            print("Already in J front : remove from eval_node")
                        return 1
                # no X, input has only cval_bar & X, check conflict       
                else:
                    if (3 in unodes_value) | (12 in unodes_value):
                        print("BWD:  Conflict:  In has only fault & cval_bar, but out is cout")
                        return 0
                    # no X, no fault, only cbar
                    else:
                        print("BWD:  Conflict:  In has no X or cval, but out is cout")
                        return 0





    #################################################
    #####        Inner Helper Functions         #####
    #################################################


    def err_at_PO(self):
        for po_node in self.circuit.PO:
            if ((po_node.value == 12) | (po_node.value == 3)):
                print("SUCCESS: Return back to last dalg\n")
                return 1
        print("FAIL: Return back to last dalg\n")
        return 0

    def print_PI(self):
        for node in self.circuit.PI:
            print(node.num + '-----' + str(node.value) + '\n')
        print("============Finish 1 round================")
    
    def print_all(self):
        for node in self.circuit.nodes_lev:
            print(node.num + '-----' + str(node.value) + '\n')
        print("==============Finish all==================")
    
    def print_node(self, node_list):
        if node_list == []:
            print("======= Empty =======")
        else:
            for node in node_list:
                print(node.num + '-----' + str(node.value))
            print("======= all nodes printed =======")

    
    def save_checkpoint(self):
        sublist_val = []       # sublist for node values
        for node in self.circuit.nodes_lev:
            sublist_val.append(node.value)
        # whole stack storing all node.value sublists
        self.checkpoint_val.append(sublist_val.copy())
        # whole stack storing all J frontier / D frontier
        # the D frontier must be the vesion after poping
        # but the J frontier or values do not need to be
        self.checkpoint_J.append(self.J_frontier.copy())
        self.checkpoint_D.append(self.D_frontier.copy())
        self.checkpoint_eval.append(self.eval_node.copy())
        print("checkpoint_val: ", len(self.checkpoint_val))
        print("checkpoint_J: ", len(self.checkpoint_J))
        print("checkpoint_D: ", len(self.checkpoint_D))
        print("************ save checkpoint finish *****************\n")


    def recover_checkpoint(self):
        if self.checkpoint_J == []:
            return 0
        self.J_frontier = self.checkpoint_J.pop()
        self.D_frontier = self.checkpoint_D.pop()
        self.eval_node = self.checkpoint_eval.pop()
        prev_val = self.checkpoint_val.pop()
        i = 0
        for node in self.circuit.nodes_lev:
            if node.value != prev_val:
                node.value = prev_val[i]
            i = i + 1
        print("After recovering.......")
        print("checkpoint_val: ", len(self.checkpoint_val))
        print("checkpoint_J: ", len(self.checkpoint_J))
        # self.print_node(self.J_frontier)
        print("checkpoint_D: ", len(self.checkpoint_D))
        # self.print_node(self.D_frontier)
        return 1



#################################################
#####        Outer Helper Functions         #####
#################################################

# the following 3 functions: generate all unode val
def unodes_val_list(node):
    val_list = []
    for unode in node.unodes:
        val_list.append(unode.value)
    return val_list

def unodes_val_set(node):
    val_set = set()
    for unode in node.unodes:
        val_set.add(unode.value)
    return val_set
    
def unodes_val_dict(node):
    val_dict = {}
    for unode in node.unodes:
        val_dict[unode.num] = unode.value
    return val_dict

def dnodes_val_set(node):
    val_set = set()
    for dnode in node.dnodes:
        val_set.add(dnode.value)
    return val_set





