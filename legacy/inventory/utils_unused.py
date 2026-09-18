"""Helpers removed from pycad.utils because the library does not use them.

bcolors, ckt_type, not_gate and the binary printing helpers were only needed by
the experiment scripts and old checkers. Kept for reference only.
"""
from pycad import config as cfg


class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'


def not_gate(a):
    return 1 - a


def ckt_type(cname):
    print("FIX ME LATER -- CKT TYPE AUTOMATIC DETECTION")
    return "EPFL"
    if cname in cfg.ALL_ISCAS85:
        return "ISCAS85"
    elif cname in cfg.ALL_EPFL:
        return "EPFL"
    else:
        raise NameError("Circuit is not known")


def bin2int(bin_arr):
    """ Its the other way around ... """
    int_val = 0
    print(bin_arr)
    for idx, val in enumerate(bin_arr):
        int_val += (val * (2**idx))
    print(int_val)
    return int_val


def int2binList(val, bitwidth):
    res = []
    for k in range(bitwidth):
        res.append(val % 2)
        val = int(val/2)
    return res


def print_out_bin(Z):
    for k in Z:
        print(k + "\t" + "{:064b}".format(Z[k]))
