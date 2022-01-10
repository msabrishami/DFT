
import sys
import pandas as pd
import matplotlib.pyplot as plt
import pdb
sys.path.insert(1, "../../")
import config 
CKTs = config.AUTO_TP.keys()

def deltaFC_FS_ST(df, remove_half=False):
    all_TPs = []
    for col in df.columns:
        if "FC-ST-tp" in col:
            all_TPs.append(int(col.split("-")[-1][2:]))
    TPs = [] 
    for tp in all_TPs:
        if tp < 500 and tp%100==0:
            TPs.append(tp)
        elif tp < 2000 and tp%500==0:
            TPs.append(tp)
        elif tp < 10000 and tp%1000==0:
            TPs.append(tp)
        elif tp%5000==0:
            TPs.append(tp)
    print(TPs)
    fig, axs = plt.subplots(len(TPs), 2, figsize=(20, 40))
    for i in range(len(TPs)):
        col1 = "FC-FS-tp{:04d}".format(TPs[i])
        col2 = "FC-ST-tp{:04d}".format(TPs[i])
        mid = df[col2].median()
        axs[i][0].scatter(
                df[df[col2] > mid][col1],
                df[df[col2] > mid][col2])
        axs[i][1].scatter(df[col1], df[col2])
        for j in [0,1]:
            axs[i][j].set_xscale("log")
            axs[i][j].set_yscale("log")
            axs[i][j].set_xlabel("E[delta-FC] using PPSF probs.")
            axs[i][j].set_ylabel("E[delta-FC] using STAFAN probs.")
        axs[i][0].set_title("{}\nFC{:04d}-ST{:04d}\nHigher half nodes".format(ckt, TPs[i], TPs[i]))
        axs[i][1].set_title("{}\nFC{:04d}-ST{:04d}\nAll nodes".format(ckt, TPs[i], TPs[i]))
    
    fig.tight_layout()
    fname = "deltaFC-scatter-{}-FC-ST.png".format(ckt)
    plt.savefig(fname)
    print(f"Saved figure in {fname}")
    plt.close()


def compare_depth(ckt_name, CI, opCount, depth, quantile=0.8):
    fname_all = "OPI-deltaFC-{}-ci{}-op{}-0.csv".format(ckt, CI, opCount)
    fname_depth = "OPI-deltaFC-{}-ci{}-op{}-depth{}-0.csv".format(ckt, CI, opCount, depth)
    df_all = pd.read_csv(fname_all)
    df_depth = pd.read_csv(fname_depth)
    all_TPs = []
    for col in df_all.columns:
        if "FC-ST-tp" in col:
            all_TPs.append(int(col.split("-")[-1][2:]))
    TPs = [] 
    for tp in all_TPs:
        if tp < 500 and tp%100==0:
            TPs.append(tp)
        elif tp < 2000 and tp%500==0:
            TPs.append(tp)
        elif tp < 10000 and tp%1000==0:
            TPs.append(tp)
        elif tp%5000==0:
            TPs.append(tp)
    fig, axs = plt.subplots(len(TPs), 2, figsize=(20, 40))
    for i in range(len(TPs)):
        col = "FC-FS-tp{:04d}".format(TPs[i])
        # mid = df_all[col].median()
        mid = df_all[col].quantile(0.8) # TODO: change the name
        axs[i][0].scatter(
                df_all[df_all[col] > mid][col],
                df_depth[df_all[col] > mid][col])
        axs[i][1].scatter(df_all[col], df_depth[col])
        for j in [0,1]:
            axs[i][j].set_xscale("log")
            axs[i][j].set_yscale("log")
            axs[i][j].set_xlabel("E[delta-FC] using all nodes in fanin-cone")
            axs[i][j].set_ylabel(f"E[delta-FC] using limited depth = {depth}")
        axs[i][0].set_title("{}\nTP={}\n\
                Higher {} quantile nodes".format(ckt, TPs[i], quantile))
        axs[i][1].set_title("{}\nTP={}\nAll nodes".format(ckt, TPs[i]))
    
    fig.tight_layout()
    fname = "deltaFC-fanin-{}-ci{}-depth{}.png".format(ckt, CI, depth)
    plt.savefig(fname)
    print(f"Saved figure in {fname}")
    plt.close()


import glob
# CKTs = ["c3540_synV0"]
os.chdir("./results/deltaFC")
for ckt in CKTs:
    print("------------------------------------")
    print(ckt)
    # files = glob.glob(f"./OPI-deltaFC-{ckt}-ci2-*.csv")
    # max_nodes = max([int(x.split("-")[-2][2:]) for x in files])
    # fname = "OPI-deltaFC-{}-ci2-op{}-0.csv".format(ckt, max_nodes)
    # print("Reading deltaFC csv file from {}".format(fname))
    # df = pd.read_csv(fname)
    # deltaFC_FS_ST(df, remove_half=False)

    CI = 1
    depth = 5
    files = glob.glob(f"./OPI-deltaFC-{ckt}-ci{CI}-op*-0.csv")
    max_nodes = max([int(x.split("-")[-2][2:]) for x in files if "depth" not in x])    
    compare_depth(ckt, CI, max_nodes, depth)
