

import sys
import os
sys.path.insert(1, "../circuit/")
import config

def load_data(dataset_name, dataset_format=None):
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
