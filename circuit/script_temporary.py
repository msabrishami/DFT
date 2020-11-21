

import os
import subprocess

netlists_EPFL_ALL = ["arbiter", "ctrl",  "i2c",  "mem_ctrl", "sin", "bar","dec", "int2float", "multiplier", "sqrt", "cavlc", "div", "log2", "router", "square", "adder", "hyp", "max", "priority", "voter"]
# removed because of size issue: mem_ctrl, hyp, div, sqrt, square, log2 
# removed because other issues "ctrl",  "i2c", router 
netlists_EPFL_EZ = ["arbiter", "sin", "bar","dec", "int2float", "multiplier", "cavlc", "adder", "max", "priority", "voter"]

netlists_ISCAS = ["c17","c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]

all_netlists = netlists_ISCAS
all_netlists.extend(netlists_EPFL_EZ)

tps = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]


########################################
###  STEP1: GENERATE GOLDEN TPs
########################################
# all_netlists.extend([x+"_syn" for x in netlists_EPFL_EZ])
# tps [100000]
# script = "python3 main_saeed.py -ckt \t$CKT$ -tp $TP$ -func genTP \t&"
# for ckt in all_netlists:
#     for tp in tps:
#         # if os.path.exists("../data/stafan-data/" + ckt[2:] + "-stafan-TP" + str(tp) + ".log"):
#         #     print("file exists for ckt: {} tp: {}, skipped".format(ckt, tp))
#         #     continue
#         sc = script.replace("$CKT$", ckt)
#         sc = sc.replace("$TP$", str(tp))
#         print(sc)



########################################
###  STEP1.5: GENERATE STIL 
########################################




#######################################
### STEP2: GENERATE STAFAN LOAD VALUES
#######################################
all_netlists = netlists_EPFL_EZ
tps = [1000, 2000] #, 5000, 10000, 20000, 50000, 100000]
script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-tp \t$TP$ \t-tpLoad 100000 -func saveStatTP & " 

for ckt in all_netlists:
    for version in ["synV0"]:
        for tp in tps:
            if os.path.exists("../data/stafan-data/{}_{}-TP{}.stafan".format(ckt, version, tp)):
                # print("file exists for ckt: {} version {} tp: {}!".format(ckt, version, tp))
                continue
            else:
                sc = script.replace("$CKT$", ckt)
                sc = sc.replace("$VER$", version)
                sc = sc.replace("$TP$", str(tp))
                print(sc)

exit()
#######################################
### STEP3: LIST OBSERVATION (B) VALUES OF ALL NODES 
### FOR SEPARATE TPs IN SEPERATE FILES
#######################################
# script = "python3 main_saeed.py -ckt\t$CKT$ -synv \t $VER$ \t-tpLoad \t$TP$ \t-func writeOB & "
# for ckt in all_netlists:
#     for version in ["synV0", "synV1", "synV2"]:
#         for tp in tps:
#             
#             if os.path.exists("../data/stafan-data/{}_{}-TP{}.stafan".format(ckt, version, tp)):
#                 if os.path.exists("../data/ob_stat/{}_{}_TP{}.obs".format(ckt, version, tp)):
#                     # print("{} {} {} exists".format(ckt, version, tp))
#                     continue
#                 sc = script.replace("$CKT$", ckt)
#                 sc = sc.replace("$VER$", version)
#                 sc = sc.replace("$TP$", str(tp))
#                 print(sc)
#             else:
#                 # print("{} {} {} stafan not found".format(ckt, version, tp))
#                 continue

#######################################
# STEP4: COLLECT THE REPORT OF STAFAN VALUES
#######################################
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-func analysisOB &"
# 
# for ckt in all_netlists:
#     for version in ["synV0", "synV1", "synV2"]:
#         sc = script.replace("$CKT$", ckt)
#         sc = sc.replace("$VER$", version)
#         print(sc)

#######################################
# STEP5: Get the histogram of B values in a circuit
# script = "python3 main_saeed.py -func histOB -ckt $CKT$ -syn $VER$ -tpLoad $TP$"


#######################################
# STEP6: Find HTO points with deltaHTO
# all_netlists = ["c432"]
# tps = [10000]
# script = "python3 main_saeed.py -func deltaHTO -ckt $CKT$ -syn $VER$ -tpLoad $TP$ -opCount 20 -Bth 0.05 -HTO_th 0.2 -HTC_th 0.2"
# for ckt in all_netlists:
#     for version in ["synV0", "synV1", "synV2"]:
#         for tp in tps:
# 
#             if os.path.exists("../data/stafan-data/{}_{}-TP{}.stafan".format(ckt, version, tp)):
#                 sc = script.replace("$CKT$", ckt)
#                 sc = sc.replace("$VER$", version)
#                 sc = sc.replace("$TP$", str(tp))
#                 print(sc)
#             else:
#                 print("STAFAN not found")
#                 continue
# 


# STEP7: Find HTO points with deltaP
#script = "python3 main_saeed.py -func deltaP -ckt $CKT$ -syn $VER$ -tpLoad $TP$ -opCount 20 -Bth 0.05"

#   for ckt in all_netlists:
#       for version in ["synV0", "synV1", "synV2"]:
#           for tp in tps:
#               
#               if os.path.exists("../data/stafan-data/{}_{}-TP{}.stafan".format(ckt, version, tp)):
#                   if os.path.exists("../data/ob_stat/{}_{}_TP{}.obs".format(ckt, version, tp)):
#                       print("{} {} {} exists".format(ckt, version, tp))
#                       continue
#                   sc = script.replace("$CKT$", ckt)
#                   sc = sc.replace("$VER$", version)
#                   sc = sc.replace("$TP$", str(tp))
#                   print(sc)
#               else:
#                   print("STAFAN not found")
#                   continue


### STEP UNKNOWN:
### CREATE VERILOG FILE BASED ON OPS OF TMAX
# script = "python3 main_saeed.py -func genV_TMAXOP -ckt $CKT$ -syn $VER$ -tpLoad 10000"
# all_netlists = netlists_EPFL_EZ 
# 
# for ckt in all_netlists:
#     for version in ["synV0", "synV1", "synV2"]:
#         sc = script.replace("$CKT$", ckt)
#         sc = sc.replace("$VER$", version)
#         print(sc)
# 
# 

