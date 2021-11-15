
import sys
import os
sys.path.insert(1, "../circuit/")
import config
import pdb

WEBADDR = "https://sportlab.usc.edu/~tegramax/files/"

def download_primitive(dataset, dataset_format=None):
    if dataset not in config.CKTS:
        print("dataset {} not available".format(dataset))
        return 
    
    if not os.path.exists("./verilog"):
        os.system("mkdir verilog")
    
    for ckt in config.CKTS[dataset]:
        if os.path.exists("./verilog/" + ckt + ".v"):
            print("{} already exists!".format(ckt))
            continue
        sc = "wget {}verilog/{}/{}.v -P ./verilog/".format(WEBADDR, dataset, ckt)
        os.system(sc)

def download_syn(dataset, syn_version):
    """ downloading synthesized datasets uploaded on personal sport-lab page
    The netlists are synthesized with NanGate15nm: 
    dataset_name should be within [ISCAS85, EPFL]
    syn_version should be a list
    V0: any AND, NAND, OR, NOR, INV, BUF, XOR, XNOR 
    V1: only AND2, OR2, INV, BUF 
    V2: only AND, OR, INV, BUF, with no limitation on fan-in is accepted """ 

    assert type(syn_version) == list, "synthesize version should be a list"
 
    if dataset not in config.CKTS:
        print("dataset {} not available".format(dataset))
        return 
    
    if not os.path.exists("./verilog"):
        os.system("mkdir verilog")
    
    for version in versions:
        for ckt in config.CKTS[dataset]:
            cname = ckt + "_syn" + version + ".v"
            if os.path.exists("./verilog/" + cname):
                print("{} already exists!".format(cname))
                continue
            sc = "wget {}verilog_syn/{}/{}/{} -P ./verilog/".format(
                    WEBADDR, dataset, version, cname)
            os.system(sc)


if __name__ == '__main__':
    print("Available benchmarks are EPFL, ISCAS85, and ISCAS89")
    print("Select what you want to download: ")
    print("1) Original design files") 
    print("2) Synthesized files (gate level verilog)") 
    tmp = input() 
    if tmp == "1":
        print("Write down the names of the datasets separated with space")
        print("\t(EPFL, ISCAS85, ISCAS89)")
        datasets = input().split(" ")
        print(datasets)
        for dataset in datasets: 
            download_primitive(dataset, "v")
    elif tmp == "2":
        print("Write down the names of the datasets separated with space")
        print("\t(EPFL, ISCAS85)")
        datasets = input().split(" ")
        print("Write down the synthesis versions separated with space\n")
        print("\tV0: AND, NAND, OR, NOR, XOR, XNOR, INV, BUFF, no limit on gate inputs")
        print("\tV1: AND, NAND, OR, NOR, INV, BUFF, gate inputs limited to two")
        print("\tV2: AND, NAND, OR, NOR, INV, BUFF, no limites on gate inputs")
        versions = input().split(" ")
        for dataset in datasets:
            download_syn(dataset, versions)

    else:
        print("Argument not accepted")
