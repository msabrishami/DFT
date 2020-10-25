#AND gate

import pdb



def GOR_m(val_list):
    return 1 if (1 in val_list) else 0

def GNOR_m(val_list):
    return 0 if (1 in val_list) else 1

def GNAND_m(val_list):
    return 1 if (0 in val_list) else 0

def GAND_m(val_list):
    return 0 if (0 in val_list) else 1

def GXOR_m(val_list):
    ''' XOR gate with multiple inputs'''
    return 1 if (sum(val_list)%2 == 1) else 0


def GAND(a, b):
    if a == 1:
        if b == 1:
            out = 1
        elif (b == 0):
            out = 0
    elif a == 0:
        out = 0
    return out


def GOR(a, b):
    ''' OR gate with 2 inputs'''
    if a == 1:
        out = 1
    elif a == 0:
        if b == 1:
            out = 1
        elif (b == 0):
            out = 0
    return out


def GXOR(a, b):
    ''' XOR gate with 2 inputs'''
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

def GNOT(a):
    '''NOT gate'''
    if a == 1:
        out = 0
    elif a == 0:
        out = 1
    return out
