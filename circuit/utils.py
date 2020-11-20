

import config


def ckt_type(cname):
    print("FIX ME LATER -- CKT TYPE AUTOMATIC DETECTION")
    return "EPFL"
    if cname in config.ALL_ISCAS85:
        return "ISCAS85"
    elif cname in config.ALL_EPFL:
        return "EPFL"
    else:
        raise NameError("Circuit is not known")
