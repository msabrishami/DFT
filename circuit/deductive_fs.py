from fault_sim import *

class DFS(FaultSim):
    def __init__(self, circuit):
        FaultSim.__init__(self, circuit)
        self.fs_type = 'dfs'

    def fs_for_atpg(self, ipt_pattern):
        return self.single(ipt_pattern)

    def single(self, input_pattern):
        """ running deductive fault simulation on the circuit 
        needs to make sure the levelization is updated """ 
        self.circuit.logic_sim(input_pattern)
        fault_set = set()
        for node in self.circuit.nodes_lev:
            node.dfs()
        for node in self.circuit.PO:
            # print(node.faultlist_dfs)
            fault_set = fault_set.union(node.faultlist_dfs)
        # return a fault set
        return fault_set



    def fs_exe(self, tp_num=1, t_mode='rand', r_mode='b'):
        """
        Execute fs in rand or full mode
        rand: the total faults can be detected by several random patterns
        full: the faults can be detected by each single pattern; all possible patterns are included
        """

        if t_mode == 'rand':
            self.fs_folder(tp_mode='rand', r_mode='b')
            report_fname = self.circuit.c_name + '_' + str(tp_num) + '_dfs_'+ r_mode + '.log'
            # tp_fname = tp_path + self.c_name + '_' + str(tp_num) + "_tp_b.txt"
            tp_fname = self.circuit.c_name + '_' + str(tp_num) + "_tp_b.txt"

            self.fs_tp_gen(tp_num = tp_num, t_mode = 'rand', r_mode = r_mode)
            # tp_fname is bare name, the path is given in the method
            pattern_list = self.fs_input_fetch(tp_fname)
            # run fs multiple
            self.multiple(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        elif t_mode == 'full':
            self.fs_folder(tp_mode='full', r_mode='b')
            report_fname = self.circuit.c_name + '_full_dfs_' + r_mode + '.log'
            tp_fname = self.circuit.c_name + '_full_tp_' + r_mode + '.txt'
            # generate all possible patterns in order
            self.fs_tp_gen(tp_num = tp_num, t_mode = 'full', r_mode = r_mode)
            pattern_list = self.fs_input_fetch(tp_fname)
            # run dfs
            self.multiple_separate(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        else:
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")


######################## just for golden file ########################################################
    def fs_exe_golden(self, tp_num=1, no=1, t_mode='rand', r_mode='b'):
        """
        Execute fs in rand or full mode
        rand: the total faults can be detected by several random patterns
        full: the faults can be detected by each single pattern; all possible patterns are included
        """

        if t_mode == 'rand':
            report_fname = self.circuit.c_name + '_' + str(tp_num) + '_' + str(no) +'_dfs_'+ r_mode + '.log'
            # tp_fname = tp_path + self.c_name + '_' + str(tp_num) + "_tp_b.txt"
            tp_fname = self.circuit.c_name + '_' + str(tp_num) + '_' + str(no) + "_tp_b.txt"
            self.fs_folder(tp_mode='rand', r_mode='b')

            self.fs_tp_gen_golden(tp_num = tp_num, no=no, t_mode = 'rand', r_mode = r_mode)
            # tp_fname is bare name, the path is given in the method
            pattern_list = self.fs_input_fetch(tp_fname)
            # run fs multiple
            self.multiple(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        elif t_mode == 'full':
            report_fname = self.circuit.c_name + '_full_dfs_' + r_mode + '.log'
            tp_fname = self.circuit.c_name + '_full_tp_' + r_mode + '.txt'
            self.fs_folder(tp_mode='full', r_mode='b')
            # generate all possible patterns in order
            self.fs_tp_gen(tp_num = tp_num, t_mode = 'full', r_mode = r_mode)
            pattern_list = self.fs_input_fetch(tp_fname)
            # run dfs
            self.multiple_separate(pattern_list=pattern_list, fname_log=report_fname, mode="b")

        else:
            raise NameError("Mode is not acceptable! Mode = 'rand' or 'full'!")
