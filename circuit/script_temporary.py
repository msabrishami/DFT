

import os
import subprocess

netlists = ["c17", "c432", "c499", "adder_syn", "arbiter_syn"]
tps = [22, 23]

script = "python3 main_personal.py -ckt $CKT$ -tp $TP$ -op saveStat"

for ckt in netlists:
    for tp in tps:
        sc = script.replace("$CKT$", ckt)
        sc = sc.replace("$TP$", str(tp))
        subprocess.check_call(sc, shell=True)
        print("Done with " + ckt + " tp: " + str(tp))

