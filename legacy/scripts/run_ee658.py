import os
import glob

MAIN_DIR = "/home/msabrishami/workspace/ee658-github-classroom-repos"
AUTO_DIR = f"{MAIN_DIR}/phase2/auto-tests-phase2"

def check_files(ckts):
    for ckt in ckts:
        os.system(f"find {AUTO_DIR}/ -name *{ckt}* | grep -v rtpg | grep -v rfl")


def delete_all():
    paths = ["cmds/dfs/*", "cmds/pfs/*", "cmds/logicsim/*", 
            "golden_results/pfs/*", "golden_results/dfs/*", "golden_results/logicsim/*", 
            "inputs/logicsim/*", "inputs/pfs/tps/*", "inputs/pfs/faults/*", "inputs/dfs/*", 
            "outputs/dfs/*", "outputs/pfs/*", "outputs/logicsim/*"]
    for path in paths:
        os.system(f"rm {AUTO_DIR}/{path} 2> /dev/null")


ckts = glob.glob("../data/ckt/*.ckt")
ckts = [x.split("/")[-1][:-4] for x in ckts]
# delete_all()
# check_files(ckts)
print(ckts)
for ckt in ckts:
    if "_" in ckt:
        continue
    if ckt not in ["c1", "c2", "c3", "c4", "c17", "x3mult", "add2", "c432", "c499", "c880"]:
        continue
    cmd = f"python3 main_saeed.py -ckt ../data/ckt/{ckt}.ckt -func ee658-p2 -tp 10 -fault 10"
    os.system(cmd)


