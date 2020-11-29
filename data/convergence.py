#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
import numpy as np
import math

import pdb
## SAEED added these: 
netlists_EPFL_EZ = ["arbiter", "sin", "bar","dec", "int2float", "multiplier", "cavlc", "adder", "max", "priority", "voter"]

netlists_ISCAS = ["c17","c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]
netlists_ISCAS = ["c880","c1355","c1908","c3540","c5315","c6288","c7552"]

all_netlists = netlists_ISCAS
all_netlists.extend(netlists_EPFL_EZ)

circuits =  ["arbiter"]
upper_bound = 3.2e-1
# keys = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
keys = [1000, 10000, 20000]
# synv = ["V0", "V1", "V2"]
synv = ["V1"]
for c in circuits:
    print (f"circuit {c}")
    for v in synv:
        results = {}
        fname = f"ob_stat/{c}_syn{v}_REPORT.obsr"
        if not os.path.exists(fname):
            print("Not found {} {} ".format(c, v))
            continue
        with open(fname, "r") as flog:
            lines = flog.readlines()
            for line in lines:
                pattern_cnt = int(line.strip().split(",")[0])
                stafan = [float(x) for x in line.strip().split(",")[1:-1]]
                results[pattern_cnt] = stafan
        

        for k in keys:
            # Plot the convergence figure 
            if k not in results:
                continue
            plt.figure()
            plt.title(f"{c} {v} {k} Convergence figure")
            plt.xlabel("STAFAN Values")
            plt.ylabel("Points Count")
            x = list(range(len(results[k])))
            # print (x)
            results[k].sort(reverse=True)
            y = results[k]
            y_min = min(y) 
            print("MIN >>", y_min)
            count_zero = 0
            if c == "arbiter":
                y_prime = []
                for yy in y:
                    if yy == 0:
                        count_zero += 1
                    if yy < 0.1:
                        y_prime.append(math.log10(yy + 10e-25))
                y = y_prime
            print(count_zero)
            # print (y)
            # plt.plot(x, y, label=f"{k}")
            plt.hist(y, bins='auto', alpha=0.6, edgecolor="black", label=f"{k}")
            plt.legend()
            plt.savefig(f"figures/{c}_syn{v}_{k}_upper_{upper_bound}_convergence.png")
            plt.close()




        """
        for i in range(0, len(keys) - 1):
            if (keys[i+1] not in results) or (keys[i] not in results):
                continue
            error_rate = [abs((j-k)/j * 100) if j!=0 and j<=upper_bound else None for j,k in zip(results[keys[i]], results[keys[i+1]])]
            esum = 0
            elen = 0
            ebounded = []
            # @Yang, what is this? :-? 
            for e in error_rate:
                if e:
                    ebounded.append(e)
                    esum += e
                    elen += 1
            avg_error_rate = esum / elen
            # avg_error_rate = sum(error_rate)/len(error_rate)

            # np.histogram(enp, bins=[3.2e-6, 1e-5, 3.2e-5, 1e-4, 3.2e-4, 1e-3, 3.2e-3, 1e-2, 3.2e-2, 1e-1, 3.2e-1])
            plt.figure()
            enp = np.array(ebounded)
            # print (enp)
            plt.hist(enp, bins=[0,0.01,0.1,0.2, 0.5, 1, 2,3,4,5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130], facecolor="blue", edgecolor="black", alpha=0.6)
            plt.title(f"circuit {c} {v} error rate histogram: {keys[i]} and {keys[i+1]}")
            plt.xlabel("STAFAN Difference Percentage")
            plt.ylabel("Frequency (Points)")
            plt.text(60, 40, f"upper_bound={upper_bound}\navg_error_rate={avg_error_rate}")
            plt.savefig(f"figures/{c}_syn{v}_upper_{upper_bound}_{keys[i]}_{keys[i+1]}_error_rate.png")
            plt.close()

        print(f"patterns : {keys[i]} and {keys[i+1]}")
        print (avg_error_rate)

        """
        print("Done")


        

