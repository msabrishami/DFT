

import os
import subprocess

netlists_EPFL_ALL = ["arbiter", "ctrl",  "i2c",  "mem_ctrl", "sin", "bar","dec", "int2float", "multiplier", "sqrt", "cavlc", "div", "log2", "router", "square", "adder", "hyp", "max", "priority", "voter"]
# removed because of size issue: mem_ctrl, hyp, div, sqrt, square, log2 
# removed because other issues "ctrl",  "i2c", router 
netlists_EPFL_EZ = ["arbiter", "sin", "bar","dec", "int2float", "multiplier", "cavlc", "adder", "max", "priority", "voter"]

netlists_ISCAS = ["c17","c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]
netlists_ISCAS = ["c17","c432","c499","c880", "c1908","c3540","c5315","c6288","c7552"]
netlists_ISCAS = ["c499","c880", "c1908","c3540","c5315","c6288","c7552"]

all_netlists = netlists_ISCAS

tps = [50, 100, 200, 500, 1000]# , 2000, 5000, 10000]



#TODO: make this steps as arguments


# STEP1: GENERATE GOLDEN TPs
# script = "python3 main_saeed.py -ckt \t$CKT$ -tp $TP$ -func genTP"

# STEP2: GENERATE STAFAN LOAD VALUES
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-tp \t$TP$ \t-tpLoad 10000 -func saveStatTP & " 

# STEP3: LIST OBSERVATION (B) VALUES OF ALL NODES FOR SEPARATE TPs IN SEPERATE FILES
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-tpLoad \t$TP$ \t-func writeOB & "

# STEP5: Get the histogram of B values in a circuit
# script = "python3 main_saeed.py -func histOB -ckt $CKT$ -syn $VER$ -tpLoad $TP$"


# STEP6: Find HTO points with deltaHTO
# script = "python3 main_saeed.py -func deltaHTO -ckt $CKT$ -syn $VER$ -tpLoad $TP$ -opCount 20 -Bth 0.05"


# STEP7: Find HTO points with deltaP
script = "python3 main_saeed.py -func deltaP -ckt $CKT$ -syn $VER$ -tpLoad $TP$ -opCount 20 -Bth 0.05"

for ckt in all_netlists[0:2]:
    for version in ["synV0", "synV1", "synV2"]:
        for tp in tps:
            # if os.path.exists("../data/stafan-data/" + ckt[2:] + "-stafan-TP" + str(tp) + ".log"):
            #     print("file exists for ckt: {} tp: {}, skipped".format(ckt, tp))
            #     continue
            sc = script.replace("$CKT$", ckt)
            sc = sc.replace("$VER$", version)
            sc = sc.replace("$TP$", str(tp))
            print(sc)


# STEP4: COLLECT THE REPORT OF STAFAN VALUES
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-func analysisOB &"
# 
# for ckt in all_netlists:
#     for version in ["synV0", "synV1", "synV2"]:
#         sc = script.replace("$CKT$", ckt)
#         sc = sc.replace("$VER$", version)
#         print(sc)
# 
