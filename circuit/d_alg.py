import copy
from enum import Enum
# from classdef import five_value
import json
import sys
from collections import OrderedDict 
sys.setrecursionlimit(10000)

#Introduction
#For XOR gate, this code is only suitable for two inputs XOR


'''
D     1/0
D_BAR 0/1
five value define
access value:five_value.ZERO.value
access variable:five_value(0).name
class five_value(Enum):
   ZERO = 0
   ONE = 15
   D = 12
   D_BAR = 3
   X = 9
gtype:IPT, BRCH, XOR,OR,NOR,NOT,NAND,AND
ntype:GATE,PI,FB,PO
'''

'''
Function: imply_and_check, error_not_at_PO, 
'''

class D_alg:
    ################### change initial, add fault conversion
    # def __init__(self, circuit, fault_node, fault_val):
    def __init__(self, circuit, fault_node, fault_val):
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
        self.checkpoint_eval = []
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

    # input: node name, value
    def Imply_Check(self, node, val):
        # forward implication
        # if the dnodes has BRCH, then all the dnodes are BRCH
        # in this case, we can directly assign val to dnodes and put their dnode in front of S_fwd     


        # if no BRCH, it must have only 1 dnode
        # should we have a loop here ???? only 1 element ???
        print ("S_fwd")
        center_node = node
        for dnode in center_node.dnodes:
            self.S_fwd.append(dnode)
            print(dnode.num)
        print (self.S_fwd)
        print('\n')

        # do recursive I&C until the stack is empty
        while self.S_fwd:
            node = self.S_fwd.pop()
            if node not in self.eval_node:
                if not self.fwd_imply_check_5val(node):
                    print("ERROR fwd: " + node.num + '----' + str(node.value) + '\n')
                    return 0
                print(node.num + '----' + str(node.value) + '\n')
                if node.value == 9:
                    continue
                self.eval_node.append(node)

                print ("S_fwd")
                for dnode in node.dnodes:
                    self.S_fwd.append(dnode)
                    print(dnode.num)
                print (self.S_fwd)
                print('\n')

            # self.Imply_Check(node, node.value)

        print ("S_bwd: ************  START  *************")
        print("center node: ", center_node.num)
        for unode in center_node.unodes:
            self.S_bwd.append(unode)
            print(unode.num , ": " , unode.value)
        print (self.S_bwd)
        print ('\n')
        
        # do recursive I&C until the stack is empty
        while self.S_bwd:
            node = self.S_bwd.pop()
            if node not in self.eval_node:
                if not self.bwd_imply_check_5val(node):
                    print("ERROR bwd:  " + node.num + '----' + str(node.value) + '\n')
                    return 0
                print("BWD Result: " + node.num + '----' + str(node.value))
                print("BWD Result: " + str(node.dnodes[0].unodes_val()) + '\n')
                
                if node.value == 9:       # stop implying
                    continue
                
                #################################
                ## inefficient  improve later
                #################################
                if node.gtype != "BRCH":
                    self.eval_node.append(node)

                if node.dnodes[0].gtype != "BRCH":
                    self.eval_node.append(node)
                else:
                    self.Imply_Check(node, node.value)

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
        The input is node type
        The dnode gtype is NAND or BRCH
        """
        # forward imply, get the value of its only dnode
        # in ntype, Fb includes PO
        # first calculate a temp value, see if any conflict exit at the end
        if node.gtype == 'BRCH':
            temp_val = node.unodes[0].value

        elif node.gtype in ['NAND', 'AND', 'NOR', 'OR']:
            temp_val = self.fwd_imply_5val_gen(node)
        

        elif node.gtype == 'XNOR':
            unodes_value = node.unodes_val()
            # if inputs have x
            if (9 in unodes_value ):
                temp_val = 9
                flag = 1
                if (12 in unodes_value) | (3 in unodes_value):
                    if node not in self.D_frontier:
                        self.D_frontier.append(node)
                        flag = 2
            else:
                temp_val = unodes_value[0] ^ unodes_value[1] ^ 15
                flag = 1
        
        elif node.gtype == 'XOR':
            unodes_value = node.unodes_val()
            # if inputs have x
            if (9 in unodes_value ):
                temp_val = 9
                flag = 1
                if (12 in unodes_value) | (3 in unodes_value):
                    if node not in self.D_frontier:
                        self.D_frontier.append(node)
                        flag = 2
            else:
                temp_val = unodes_value[0] ^ unodes_value[1]
                flag = 1
        
        elif node.gtype == 'NOT':
            unodes_value = node.unodes_val()
            # if input is x
            if (unodes_value[0] == 9):
                temp_val = 9
            else:
                temp_val = unodes_value[0] ^ 15
            flag = 1
        elif node.gtype == 'BUFF':
            #--- Not sure if we have buffer ---#
            if (unodes_value[0] == 9):
                temp_val = 9
            else:
                temp_val = unodes_value[0]
            flag = 1

        # check if any conflict
        if self.fwd_check_5val_gen(node, temp_val):
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
            # print("Hello my dnode is BRCH!!!")
            # dnodes_val = []
            # for dnode in node.dnodes:
            #     dnodes_val.append(dnode.value)
            # if (15 in dnodes_val) | (12 in dnodes_val):
            #     node.value = 15
            # elif (0 in dnodes_val) | (3 in dnodes_val):
            #     node.value = 0
            # else:
            #     node.value = 9

            # return 1
            print("Hello I'm BRCH!!!")
            dnodes_val = set()
            # the stem has been assigned
            # add other branches to dnode value set
            for dnode in node.dnodes:
                dnodes_val.add(dnode.value)

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
            if self.bwd_imply_check_5val_gen(node):
                return 1
            else:
                return 0
        
        elif node.dnodes[0].gtype == 'XNOR':
            val = node.dnodes[0].value
            unodes_value = node.dnodes[0].unodes_val()
            # if the output is not X #####
            # if 2 inputs are both X
            if (unodes_value[0] == 9) & (unodes_value[1] == 9):
                if node.dnodes[0] not in self.J_frontier:
                    self.J_frontier.append(node.dnodes[0])
                    return 2
            # if 1 input is X
            elif (node.value == 9):
                if (unodes_value[0] == 9):
                    node.value = val ^ 15 ^ unodes_value[1]
                else:
                    node.value = val ^ 15 ^ unodes_value[0]
                # input cannot be D or D'
                if node.value in [3, 12]:
                    node.value = node.value ^ 3
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
            val = node.dnodes[0].value
            unodes_value = node.dnodes[0].unodes_val()
            # if the output is not X#####
            # if 2 inputs are both X
            if (unodes_value[0] == 9) & (unodes_value[1] == 9):
                if node.dnodes[0] not in self.J_frontier:
                        self.J_frontier.append(node.dnodes[0])
                        return 2
                return 1
            # if 1 input is X
            elif (node.value == 9):
                if (unodes_value[0] == 9):
                    node.value = val ^ unodes_value[1]
                else:
                    node.value = val ^ unodes_value[0]
                #input cannot be D or D'
                if node.value in [3, 12]:
                    node.value = node.value ^ 3
                return 1
            # 2 inputs are not X
            # if output != input1 ^ input2 ^15
            else:
                if val != (unodes_value[0] ^ unodes_value[1]):
                    if val != (unodes_value[0] ^ unodes_value[1] ^ 3):
                        return 0
                return 1
        
        elif node.dnodes[0].gtype == 'NOT':
            print("Hello I'm INV!!!")
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


            # val = node.dnodes[0].value
            # unodes_value = node.dnodes[0].unodes_val()
            # # if the output is not X
            # if (val != 9):
            #     unodes_value[0] = ~(val ^ 3)
            #     return 1
        
        elif node.dnodes[0].gtype == 'BUFF':
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
            

        
    # def fwd_implementation(self):
    #     if (self.D_frontier):
    #         while (node.gtype in ['AND', 'NAND', ''])
    #         node = D_frontier.pop[0]
    #         for unode in node.unodes:
    #             if unode.value == 9:
    #                 unode.value = node.cval

    #     else:
    #         return False

    def err_at_PO(self):
        for po_node in self.circuit.PO:
            if ((po_node.value == 12) | (po_node.value == 3)):
                return 1
        return 0

    def print_PI(self):
        for node in self.circuit.PI:
            print(node.num + '-----' + str(node.value) + '\n')
        print("============Finish 1 round================")
    
    def print_all(self):
        for node in self.circuit.nodes_lev:
            print(node.num + '-----' + str(node.value) + '\n')
        print("==============Finish all==================")


    def dalg_recur(self, node_num, val):
        node = self.circuit.nodes[node_num]
        node.value = val
        if not self.Imply_Check(node,val):
            print("I AND C wrong")
            # self.print_PI()
            # self.print_all()
            return 0
        if not self.err_at_PO():
            if len(self.D_frontier) == 0:
                print("ERROR NOT PO:  D frontier is empty!!")
                # self.print_PI()
                # self.print_all()
                return 0
            else:
                po_val = set()
                for po in self.circuit.PO:
                    po_val.add(po.value)
                print(po_val)
                if (12 not in po_val) & (3 not in po_val) & (9 not in po_val):
                    print("ERROR NOT PO:  D frontier is not empty!! Should choose another")
                    return 0

            while (len(self.D_frontier) != 0):
                print(self.D_frontier)
                d_fr_node = self.D_frontier.pop() #should be in string format
                #######################################
                #####    store the check points   #####
                #######################################
                sublist_val = []       # sublist for node values
                for node in self.circuit.nodes_lev:
                    sublist_val.append(node.value)
                # whole stack storing all node.value sublists
                print("D frontier: new pop out, save the checkpointing")
                self.checkpoint_val.append(sublist_val)
                # whole stack storing all J frontier
                self.checkpoint_J.append(self.J_frontier)
                # self.checkpoint_eval.append(self.eval_node)
                print("checkpoint_val: ", len(self.checkpoint_val))
                print("checkpoint_J: ", len(self.checkpoint_J))

                print("Pop D front:  " + d_fr_node.num)
                for unode in d_fr_node.unodes:
                    print(unode.num + ': ' + str(unode.value) + '\n')
                    if unode.value == 9:
                        # if the gate type is XOR, it has no cval, we can assign either 0 or 1
                        if d_fr_node.gtype in ["XOR", "XNOR"]:
                            if not d_fr_node.c_flag:
                                unode.value = 15
                                d_fr_node.c_flag = 1
                            else:
                                unode.value = 0
                                d_fr_node.c_flag = 0
                            print("Assign: " + unode.num + "---" + str(unode.value))
                        # if the gate type is AND, OR, NAND, NOR
                        else:
                            unode.value = d_fr_node.cval ^ 15
                            print("Assign: " + unode.num + "---" + str(unode.value))
                    
                        # print("Last D front choice: ", d_fr_node.num)
                        if self.dalg_recur(unode.num,unode.value):
                            print("DALG_RECUR:  D frontier select")
                            self.print_PI()
                            self.print_all()
                            return 1
                        # the latest D frontier choice is wrong
                        # we should recover our previous node values, then choose another
                        else:
                            print("DALG FAIL: Wrong D front choice: should recover preovious node values")
                            print("checkpoint_val: ", len(self.checkpoint_val))
                            print("checkpoint_J: ", len(self.checkpoint_J))
                            # print("checkpoint_eval: " + str(self.checkpoint_eval))
                            if self.checkpoint_J == []:
                                return 0
                            self.J_frontier = self.checkpoint_J.pop()
                            # self.eval_node = self.checkpoint_eval.pop()
                            prev_val = self.checkpoint_val.pop()
                            # put the XOR or XNOR if we have other choice
                            if (d_fr_node.gtype in ["XOR","XNOR"]):
                                if (d_fr_node.c_flag == 1):
                                    self.D_frontier.append(d_fr_node)
                            i = 0
                            for node in self.circuit.nodes_lev:
                                if node.value != prev_val:
                                    node.value = prev_val[i]
                                    if node in self.eval_node:
                                        self.eval_node.remove(node) 
                                i = i + 1

            # self.print_PI()
            # self.print_all()
            return 0
        
        # error propagated to a PO
        if len(self.J_frontier) == 0:
            print("J frontier empty")
            # self.print_PI()
            # self.print_all()
            return 1
        
        j_fr_node = self.J_frontier.pop()
        print("Pop J front:  " + j_fr_node.num + '\n')
        for unode in j_fr_node.unodes:
            if unode.value == 9:
                # if the gate type is XOR, it has no cval
                if j_fr_node.gtype in ["XOR", "XNOR"]:
                    # first: assign 1
                    if not j_fr_node.c_flag:
                        unode.value = 15
                        j_fr_node.c_flag = 1
                        self.J_frontier.append(j_fr_node)
                    # second: assign the same as backward imply
                    else:
                        if j_fr_node.value in [15, 12]:
                            unode.value = 0
                        elif j_fr_node.value in [0, 3]:
                            unode.value = 15                        
                        j_fr_node.c_flag = 0
                    print("Assign: " + unode.num + "---" + str(unode.value))
                # if the gate type is AND, OR, NAND, NOR
                else:
                    unode.value = j_fr_node.cval
                    print("Assign: " + unode.num + "---" + str(j_fr_node.cval))
                
                if self.dalg_recur(unode.num,unode.value):
                    print("DALG_RECUR")
                    # self.print_PI()
                    # self.print_all()
                    return 1

                # the dalg failed, we need to reassign the inverse value to J front elem
                print("DALG FAIL: Reverse the decision in J frontier assignment")
                # if the gate type is XOR, it has no cval
                if j_fr_node.gtype in ["XOR", "XNOR"]:
                    unode.value = 0
                # if the gate type is AND, OR, NAND, NOR
                else:
                    unode.value = j_fr_node.cval ^ 15
                print("Assign: " + unode.num + "---" + str(j_fr_node.cval) + '\n')
        
        print("END")
        # self.print_PI()
        # self.print_all()
        return 0




    def dalg(self):
        if self.dalg_recur(self.fault_node, self.fault_val):
            return 1
        else:
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

        unodes_value = node.unodes_val()
        print("Unode value: " + str(unodes_value) + '\n')
        print("INV: " + str(inv) + "    CVAL: " + str(cval))
        if (cval in unodes_value):
            temp_val = cout
            flag = 1
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
                        print("Add D front:  " + node.num)
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



    def fwd_check_5val_gen(self, node, temp_val):   
        """
        General Function for forward check
        For: all types
        """
        print("General FWD: ", node.gtype)
        if temp_val == 9:
            print("Imply result is X, no conflict!")
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
        """
        print("BWD: type: " + node.dnodes[0].gtype)
        cval = node.dnodes[0].cval
        inv = node.dnodes[0].inv
        cout = cval ^ inv        # the expected output when input has cval
        cout_bar = cout ^ 15     # the expected output when input are all non-cval
        cval_bar = cval ^ 15     # the non-c value
        print("cout: "+str(cout)+"  cout_bar: "+str(cout_bar)+"  cval_bar: "+str(cval_bar)+'\n')

        val = node.dnodes[0].value
        unodes_value = node.dnodes[0].unodes_val()
        print("dnode: " + node.dnodes[0].num + ":  " + str(val) + '\n')
        print("unodes values: " + str(unodes_value) + '\n')
        # in the backward imply, input cannot have D / D'
        # c-val in inputs: the output is 1 or 1/0: D
        # return value:   1: no conflict, no J;  0: conflict;  2: no conf, J
        if ((cval in unodes_value)) & ((val != cout) & (val != cout ^ 12)):
            print("BWD:  Conflict:  In has cval , but out is not cout/fault")
            return 0
        # no c-val in inputs
        else:
            # count how many X in inputs
            x_list = []
            for unode in node.dnodes[0].unodes:
                if unode.value == 9:
                    x_list.append(unode)
            x_num = len(x_list)

            if (val == cout_bar) | (val == 12 ^ cout):
                # case1: input has no cval, output has no fault
                # case2: input has no cval, output has fault
                #        inputs cannot contain D or D', only non-c or X
                #        in fault free: output should be cout_bar
                for unode in node.dnodes[0].unodes:
                    unode.value = cval_bar
                return 1
        
            elif (val == cout) | (val == 12 ^ cout_bar):
                # case1: input has c, output has no fault
                # case2: input has cval, output has fault
                #        inputs cannot contain D or D', only c or X
                #        in fault free: output should be cout
                if (9 in unodes_value):   # inputs have X
                    if (x_num == 1) & (cval not in unodes_value):
                        print(str(unodes_value) + '\n')
                        print("cval is " + str(cval) + '\n')
                        x_list[0].value = cval
                        return 1
                    # X >= 2 or inputs have X and cval
                    else:
                        if node.dnodes[0] not in self.J_frontier:
                            self.J_frontier.append(node.dnodes[0])
                            print("Add J front:  " + node.dnodes[0].num)
                            return 2
                        return 1
                # no X
                else: 
                    # no cval exist in inputs, conflict
                    if (cval not in unodes_value):
                        print("BWD:  Conflict:  In has no X or cval, but out is cout")
                        return 0
                    # input has cval, no conflict
                    else: 
                        return 1