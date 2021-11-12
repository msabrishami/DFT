from fault_sim import FaultSim, FaultList_2
import math

class Fault_coverage():
    def __init__(self, circuit, fault_mode='full', fault_count = 0,fname = ''):
        self.circuit = circuit
        self.fault_list = FaultList_2()

        if fault_mode == 'full':
            self.fault_list.add_all(self.circuit)
        elif fault_mode == 'user':
            self.fault_list.add_random(fault_count)
        elif fault_mode == 'file':
            self.fault_list.add_file(fname)




class Fault_coverage_estimation(Fault_coverage):
    """
    Calculate fault coverage estimation using STAFAN parameters. 
    """
    
    def __init__(self, circuit, fault_mode, tps_count):
        super().__init__(circuit, fault_mode)
        self.tps_count = tps_count
        self.fc_type = 'tp'

    def calculate(self):
        expected_value_of_fault_coverage = 1
        total_faults_no = len(self.fault_list.faults)
        for fault in self.fault_list.faults:
            node = self.circuit.nodes[fault.node_num]
            
            detectability  = 0
            if fault.stuck_val == '1':
                detectability = node.C1 * node.B1
            elif fault.stuck_val == '0':
                detectability = node.C0 * node.B0
            expected_value_of_fault_coverage -= math.exp(
                -detectability*self.tps_count)/len(self.fault_list.faults)

        # print("Expected value of fault coverage =",expected_value_of_fault_coverage)
        return expected_value_of_fault_coverage

class Fault_coverage_simulation(Fault_coverage):
    def __init__(self, circuit, fault_list, fault_mode,tps_count):
        super().__init__(circuit, fault_list, fault_mode)
        self.tps_count = tps_count
        self.fc_type = 'fs'
