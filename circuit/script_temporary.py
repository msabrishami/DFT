

import os
import subprocess

netlists = ["arbiter", "ctrl",  "i2c",  "mem_ctrl", "sin", "bar","dec", "int2float", "multiplier", "sqrt", "cavlc", "div", "log2", "router", "square", "adder", "hyp", "max", "priority", "voter"]
# removed because of size issue: mem_ctrl, hyp, div, sqrt, square, log2 
# removed because other issues "ctrl",  "i2c", router 
netlists_EPFL = ["arbiter", "sin", "bar","dec", "int2float", "multiplier", "cavlc", "adder", "max", "priority", "voter"]

netlists_ISCAS = ["c17","c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]

all_netlists = []
for ckt in netlists_ISCAS:
    all_netlists.append("$$" + ckt)
#for ckt in netlists_EPFL:
#    all_netlists.append(ckt)


tps = [50, 100, 200, 500, 1000, 2000, 5000] # , 10000]
# all_netlists = ["$$c3540"]
# all_netlists = netlists_ISCAS
# script = "python3 main_personal.py -ckt $CKT$ -tp $TP$ -op writeInfo > ./temp_results/$CKT$_info_$TP$.log & "
script = "python3 main_saeed.py -ckt $CKT$ -tp $TP$ -func saveStat"

for ckt in all_netlists:
    for tp in tps:
        if os.path.exists("../data/stafan-data/" + ckt[2:] + "-stafan-" + str(tp) + ".log"):
            # print("file exists for ckt: {} tp: {}, skipped".format(ckt, tp))
            continue
        if "$$" in ckt:
            sc = script.replace("$CKT$", ckt[2:]).replace("$TP$", str(tp))
        else:
            sc = script.replace("$CKT$", ckt+"_syn").replace("$TP$", str(tp))
        sc = sc.replace("$TP$", str(tp))
        print(sc)
        # subprocess.check_call(sc, shell=True)
        #print("Done with " + ckt + " tp: " + str(tp))
