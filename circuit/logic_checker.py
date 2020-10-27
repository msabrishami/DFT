

class Checker():
    def __init__(self):
        print("None")
        """ create a circuit and a modelsim simulation
        we have two types of inputs: "gate-level-circuit" and a "verilog"
        verilog can be anything, gate level, behavioral, etc. 
        But gate-level-circuit can only be gate-level ckt or gate-level verilog 
        For now we are only supporting ckt for gate-level-circuit
        It is possible that both are the same, if we have a gate-level-verilog
        Objective: 
        we want to simulate the gate-level-circuit  with methods in class Circuit 
            and compare the results with modelsim simulation of the verilog. 
        Tasks: 
        - Check if the PI/PO of the files are the same -- raise error if not match
        - etc. 




