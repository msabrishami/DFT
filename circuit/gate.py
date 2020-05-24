#AND gate

import pdb

def GAND(a, b):
    if a == 1:
        if b == 1:
            out = 1
        elif (b == 0):
            out = 0
    elif a == 0:
        out = 0
    return out

#OR gate
def GOR(a, b):
    if a == 1:
        out = 1
    elif a == 0:
        if b == 1:
            out = 1
        elif (b == 0):
            out = 0
    return out

#XOR gate
def GXOR(a, b):
    if a == 1:
        if b == 1:
            out = 0
        elif (b == 0):
            out = 1
    elif a == 0:
        if b == 1:
            out = 1
        elif (b == 0):
            out = 0
    return out

#NOT gate
def GNOT(a):
    if a == 1:
        out = 0
    elif a == 0:
        out = 1
    return out
