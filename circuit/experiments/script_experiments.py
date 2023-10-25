

import os
import glob

netlists_EPFL_ALL = ["arbiter", "ctrl",  "i2c",  "mem_ctrl", "sin", "bar","dec", "int2float", "multiplier", "sqrt", "cavlc", "div", "log2", "router", "square", "adder", "hyp", "max", "priority", "voter"]
# removed because of size issue: mem_ctrl, hyp, div, sqrt, square, log2 
# removed because other issues "ctrl",  "i2c", router 
netlists_EPFL_EZ = ["arbiter", "sin", "bar","dec", "int2float", "multiplier", "cavlc", "adder", "max", "priority", "voter"]

netlists_ISCAS = ["c17","c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]
netlists_ISCAS = ["c432","c499","c880","c1355","c1908","c3540","c5315","c6288","c7552"]

# all_netlists = netlists_ISCAS
# all_netlists.extend(netlists_EPFL_EZ)

# netlists_ISCAS = ["c432","c3540","c5315","c6288"] # 1K patterns
# netlists_ISCAS = ["c432","c499","c880","c1355","c1908","c3540","c5315","c6288"] # 5K patterns

all_netlists = netlists_ISCAS
# all_netlists = ["priority_syn", "int2float_syn", "dec_syn", "cavlc_syn", "adder_syn"] 
tps = [1000, 10000, 100000]


########################################
###  STEP0:SIMPLE TEST OF DFT PACKAGE 
########################################
# all_netlists.extend([x+"_syn" for x in netlists_EPFL_EZ])
# all_netlists = [x + ".v" for x in all_netlists]
# script = "python3 main_saeed.py -ckt \t$CKT$ -tp $TP$ -func genTP \t&"
# script = "python3  main_saeed.py -ckt ../data/verilog/$CKT$ -tp $TP$ -func test4 "
# script = "python3 main_saeed.py -ckt ../data/verilog/{} -func stafan-save-coded -tp {} -cpu 10 -code 20"
# script = "python3 main_saeed.py -ckt ../data/verilog/{} -func stafan-save -tp {} -cpu 10"
# script = "python3 main_saeed.py -ckt ../data/verilog/{} -func ppsf_parallel -cpu  50"
# script = "python3 main_saeed.py -ckt ../data/verilog/{} -func stafan-load -tpLoad 1000000"
script = "python3 main_saeed.py -ckt ../data/verilog/{} -func ppsf_vs_stafan -tpLoad {} -cpu 50"
# script = "scp viterbi2:/home/viterbi/00/abri442/workspace/DFT/data/fault_sim/{}/*step* ../data/fault_sim/{}/"
script = "python3 main_saeed.py -ckt ../data/verilog/{} -func ppsf_vs_stafan -cpu 50 -tpLoad 100000"
script = "python3 main_saeed.py -ckt ../data/verilog/{} -func fc-sta-fs -cpu 50 -tpLoad 100000 -opCount 100 -ci 2"
script = "python3 g-experiments.py -ckt ../data/verilog/{} -func ppsf-error -cpu 100"
# script = "python3 g-experiments.py -ckt ../data/verilog/{} -func PD_PPSF -cpu 80 -ci 1"
script = "python3 main_saeed.py -ckt ../data/verilog/{} \t -func ppsf-vs-stafan -tpLoad 100000 -ci 3 -cpu 50"
script = "python3 g-experiments.py -ckt ../data/verilog/{} \t -func  compare-tpfc -tpLoad 100000 -tp 1000 -cpu 50 -ci 10 -times 50"
#script = "python3 g-experiments.py  -ckt ../data/verilog/{}   -func tpfc-pfs -cpu 10 -tp 1000 -times 10"
#script = "python3 g-experiments.py  -ckt ../data/verilog/{}   -func tpfc-ppsf -cpu 10 -tp 5000 -times 10"
script = "python3 g-experiments.py -ckt ../data/verilog/{} -func stafan"
script = "python3 main_saeed.py -ckt ../data/verilog/{} \t -func  deltaFCP -tpLoad 1000000 -tp 1000 -cpu 50 -ci 1 -opCount 10000 -depth 10"
script = "python3 main_saeed.py -ckt ../data/verilog/{} \t -func  fanin-analysis"
script = "python3 main_saeed.py -ckt ../data/verilog/{} -func simple-stafan -tp {} -cpu 100"
script = "python3 g-experiments.py  -ckt ../data/verilog/{}   -func tpfc-pfs -cpu 40 -tp 1000 -times 20"

# All TPs used for STAFAN on Jan 11th 
STAFAN_TPs = [200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000]
STAFAN_TPs = [1000000, 2000000, 5000000, 10000000]
# os.chdir("../data/stafan-data/")
os.chdir("./results/fc_pfs/")

for tp in [1]: # STAFAN_TPs:
    for ckt in all_netlists:
        for ver in [0, 1, 2]:
            not_found = []
            ckt_name = ckt + "_synV" + str(ver) + ".v" 
            print(script.format(ckt_name, tp))
            continue
            # exit()
            #         continue
            # fnames = glob.glob(f"{ckt_name}/*00.stafan")
            ckt_name = ckt + "_synV" + str(ver) 
            fnames = glob.glob(f"tpfc-pfs-{ckt_name}-tp*-part*.csv")
            max_tps = list(set([fname.split("-")[-2][2:] for fname in fnames]))
            if len(max_tps) > 1:
                for tp in max_tps:
                    print(ckt_name, tp, len(glob.glob(f"tpfc-pfs-{ckt_name}-tp{tp}-part*.csv")))
            if len(max_tps) == 0:
                print(ckt_name, "Empty")
                continue
            print(f"{ckt_name} \t {max_tps[0]}")
            continue

            for tp in STAFAN_TPs:
                if f"{ckt_name}/{ckt_name}-tp{tp}.stafan" not in fnames:
                    not_found.append(str(tp))
            if len(not_found) == 0:
                print(f"{ckt_name} DONE!")
            else:
                print(f"{ckt_name} not found: " + str(not_found))
        # if os.path.exists("../data/stafan-data/" + ckt[2:] + "-stafan-TP" + str(tp) + ".log"):
        #     print("file exists for ckt: {} tp: {}, skipped".format(ckt, tp))
        #     continue
    exit()
        # sc = script.format(ckt_name, tp)
        # os.system(sc)
        # print(sc)
        # print("date \'+%F   %H:%M:%S\'")
exit()


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
# all_netlists = ["arbiter", "max", "priority"] 
# # all_netlists = [x + "_synV1" for x in all_netlists]
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv synV1 -tpLoad 100000 -tp 20000 -func gen_stil \t&"
# for ckt in all_netlists:
#     sc = script.replace("$CKT$", ckt)
#     print(sc)
# 



#######################################
### STEP2: GENERATE STAFAN LOAD VALUES
#######################################
# all_netlists = netlists_EPFL_EZ
# tps = [1000, 2000] #, 5000, 10000, 20000, 50000, 100000]
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-tp \t$TP$ \t-tpLoad 100000 -func saveStatTP & " 
# 
# for ckt in all_netlists:
#     for version in ["synV0"]:
#         for tp in tps:
#             if os.path.exists("../data/stafan-data/{}_{}-tp{}.stafan".format(ckt, version, tp)):
#                 # print("file exists for ckt: {} version {} tp: {}!".format(ckt, version, tp))
#                 continue
#             else:
#                 sc = script.replace("$CKT$", ckt)
#                 sc = sc.replace("$VER$", version)
#                 sc = sc.replace("$TP$", str(tp))
#                 print(sc)



#######################################
### STEP3: LIST OBSERVATION (B) VALUES OF ALL NODES 
### FOR SEPARATE TPs IN SEPERATE FILES
#######################################
# script = "python3 main_saeed.py -ckt\t$CKT$ -synv \t $VER$ \t-tpLoad \t$TP$ \t-func writeOB & "
# all_netlists = ["sin"]
# versions = ["synV1"]
# tps = [1000, 10000, 20000]
# for ckt in all_netlists:
#     for version in versions:
#         for tp in tps:
#             if os.path.exists("../data/stafan-data/{}_{}-tp{}.stafan".format(ckt, version, tp)):
#                 if os.path.exists("../data/ob_stat/{}_{}_tp{}.obs".format(ckt, version, tp)):
#                     print("{} {} {} exists".format(ckt, version, tp))
#                     continue
#                 sc = script.replace("$CKT$", ckt)
#                 sc = sc.replace("$VER$", version)
#                 sc = sc.replace("$TP$", str(tp))
#                 print(sc)
#             else:
#                 print("{} {} {} stafan not found".format(ckt, version, tp))
#                 continue
# exit()

#######################################
# STEP4: COLLECT THE REPORT OF STAFAN VALUES
#######################################
# script = "python3 main_saeed.py -ckt \t$CKT$ -synv \t $VER$ \t-func analysisOB &"
# all_netlists = ["sin"]
# versions = ["synV1"]
# tps = [1000, 10000, 20000]

# for ckt in all_netlists:
#     for version in versions:
#         sc = script.replace("$CKT$", ckt)
#         sc = sc.replace("$VER$", version)
#         print(sc)
# exit()
# #######################################
# STEP5: Get the histogram of B values in a circuit
# script = "python3 main_saeed.py -func histOB -ckt $CKT$ -syn $VER$ -tpLoad $TP$"


#######################################
# STEP6: Find HTO points with deltaHTO
# all_netlists = ["sin"]

# tps = [10000]
# script = "python3 main_saeed.py -func deltaHTO -ckt $CKT$ -syn $VER$ -tpLoad $TP$ -opCount $OPCNT$ -Bth 0.05 -HTO_th 0.2 -HTC_th 0.2 -Bth $BTH$"
# ckt = "c3540"
# # bth = [0.15, 0.2]
# bth = [0.2]
# count = [11, 20, 40]

# # count = [65]
# f = "deltaHTO"
# htoth = "0.2"
# htcth = "0.05"
# tp = 100000
# version = "synV1"
# for cnt in count:
#     for b in bth:            
#         if os.path.exists(f"../data/stafan-data/{ckt}_{version}-tp{tp}.stafan"):
#             if os.path.exists(f"../data/observations/{ckt}_{version}_{f}_B-{b}_Count-{cnt}.op"):
#                 print(f"{ckt}_{version}_{f}_B-{b}_Count-{cnt}.op exists")
#                 continue
#             sc = f"python3 main_saeed.py -func {f} -ckt {ckt} -syn {version} -tpLoad {tp} -opCount {cnt} -Bth {b} -HTO_th {htoth} -HTC_th {htcth} > {ckt}_{version}_{f}_opcnt_{cnt}_Bth_{b}_HTO_th_{htoth}_HTC_th_{htcth}.log &"
#             print(sc)
#         else:
#             print("STAFAN not found")
#             continue

# for ckt in all_netlists:
#     # for version in ["synV0", "synV1", "synV2"]:
#     for version in ["synV1"]
#         for tp in tps:
# 
#             if os.path.exists("../data/stafan-data/{}_{}-tp{}.stafan".format(ckt, version, tp)):
#                 sc = script.replace("$CKT$", ckt)
#                 sc = sc.replace("$VER$", version)
#                 sc = sc.replace("$TP$", str(tp))
#                 print(sc)
#             else:
#                 print("STAFAN not found")
#                 continue
# 


# # STEP7: Find HTO points with deltaP
# script = "python3 main_saeed.py -func deltaP -ckt $CKT$ -syn $VER$ -tpLoad $TP$ -opCount $OPCNT$ -Bth $BTH$"
# all_netlists = ["sin"]
# ckt = "c3540"
# # bth = [0.1, 0.15, 0.2]
# bth = [0.2]
# # count = [13, 26, 39, 52, 65, 78, 91, 104, 117, 130, 143, 156, 169, 182]
# count = [11, 20, 40]
# # count = [104, 117, 130, 143, 156]
# tp = 100000
# f = "deltaP"
# version = "synV1"
# for cnt in count:
#     for b in bth:            
#         if os.path.exists(f"../data/stafan-data/{ckt}_{version}-tp{tp}.stafan"):
#             if os.path.exists(f"../data/observations/{ckt}_{version}_{f}_B-{b}_Count-{cnt}.op"):
#                 print(f"{ckt}_{version}_{f}_B-{b}_Count-{cnt}.op exists")
#                 continue
#             sc = f"python3 main_saeed.py -func {f} -ckt {ckt} -syn {version} -tpLoad {tp} -opCount {cnt} -Bth {b} > {ckt}_{version}_{f}_opcnt_{cnt}_Bth{b}.log &"
#             print(sc)
#         else:
#             print("STAFAN not found")
#             continue
# 

### STEP 8: generate genv_TMAXOP which is verilog and stil of OP added
### CREATE VERILOG FILE BASED ON OPS OF TMAX
# script = "python3 main_saeed.py -func genV_TMAXOP -ckt c3540 -op_fname $OPFNAME$ -syn synV1 -Bth $BTH$ -tpLoad 100000 -tp 1000 &"
# ckt = "c3540"
# # bth = "0.1"
# bth = [0.2]
# # count = [13, 26, 39, 52, 65]
# count = [11, 20, 40]
# tp = 10000
# f = "deltaP"
# version = "synV1"
# for cnt in count:
#     for b in bth:
#         sc = script.replace("$OPFNAME$", f"{ckt}_synV1_{f}_B-{b}_Count-{cnt}")
#         sc = sc.replace("$BTH$", str(b))
#         print (sc)


# for i in range(1, 10):
#     for ver in ["beta"]:
#         sc = script.replace("$OPFNAME$", f"sin_synV1_TMAX_{ver}_{13 * i}")
#         print (sc)

# sc = script.replace("$OPFNAME$", f"sin_synV1_TMAX_130")
# print (sc)

# for ckt in all_netlists:
#     for version in ["synV1"]:
#         sc = script.replace("$CKT$", ckt)
#         sc = sc.replace("$VER$", version)
#         if ckt in ["arbiter", "max", "priority"]:
#             sc = sc.replace("$TP$", "20000")
#         else:
#             sc = sc.replace("$TP$", "1000")
#         print(sc)

