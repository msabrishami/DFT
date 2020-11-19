



#TODO: if file already exists, it creates a new copy, 
# like circuit.v.1 instead of overwriting on circuit.v

import sys
import os
sys.path.insert(1, "../circuit/")
import config

def load_primitive(dataset_name, dataset_format=None):
    script = "wget  https://sportlab.usc.edu/~msabrishami/files/verilog/$$CKT$$ -P ./verilog/"
    if (dataset_name=="ISCAS85") and (dataset_format=="v"):
        if not os.path.exists("./verilog"):
            print("let's make the directory")
            os.system("mkdir verilog")
        for ckt in config.ALL_ISCAS85:
            if not os.path.exists("./verilog/" + ckt + ".v"):
                sc = script.replace("$$CKT$$", ckt + ".v")
                print(sc)
                os.system(sc)

def load_syn(dataset_name, syn_version):
    """ loading synthesized datasets uploaded on personal sport-lab page
    The netlists are synthesized with NanGate15nm: 
    dataset_name should be within [ISCAS85, EPFL]
    syn_version should be a list
    V0: any AND, NAND, OR, NOR, INV, BUF, XOR, XNOR is accepted
    V1: only AND2, OR2, INV, BUF are accepted
    V2: only AND, OR, INV, BUF, with no limitation on fan-in is accepted """ 

    assert type(syn_version) == list, "synthesize version should be a list"
    url = "https://sportlab.usc.edu/~msabrishami/files/"
    script = "wget {}verilog_syn/$$DS$$/$$V$$/$$CKT$$ -P ./verilog/".format(url)
    script = script.replace("$$DS$$", dataset_name)
    if dataset_name == "ISCAS85":
        netlists = config.ALL_ISCAS85
    elif dataset_name == "EPFL":
        netlists = config.ALL_EPFL_EZ
    else:
        raise NameError("dataset is not valid")

    for ckt in netlists:
        for version in syn_version:
            sc = script.replace("$$V$$", version)
            if version == "VX":
                sc = sc.replace("$$CKT$$", ckt + "_syn.v")
            else:
                sc = sc.replace("$$CKT$$", ckt + "_syn" + version + ".v")
            os.system(sc)
