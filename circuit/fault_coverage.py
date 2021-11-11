from fault_sim import FaultSim, FaultList_2
import math

"""The detection probability of a fault is equal to the number of vectors that
# detect it, called its detecting set, divided by the total number of input vectors, 2n,
# where n is the number of primary inputs.
"""

class fault_coverage():
    def __init__(self, circuit, fault_list=[], fault_mode='user'):
        self.circuit = circuit
        if fault_mode == 'full':
            self.fault_list = FaultList_2()
            self.fault_list.add_all(self.circuit)


class FC_test_pattern(fault_coverage):
    def __init__(self, circuit, fault_list, fault_mode,tps_count):
        super().__init__(circuit, fault_list, fault_mode)
        self.tps_count = tps_count
        self.fc_type = 'tp'

    def calculate(self):
        # print(self.fault_list.faults,len(self.fault_list.faults))
        # print(len(self.circuit.nodes))
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
                detectability*self.tps_count)/total_faults_no

        print("Expected value of fault coverage =",expected_value_of_fault_coverage)


class FC_fault_simulation(fault_coverage):
    def __init__(self, circuit):
        super().__init__(circuit)
        self.fc_type = 'fs'
