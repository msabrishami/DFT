def c17_sim(in_vector):
    a1 = in_vector['1']
    a2 = in_vector['2']
    a3 = in_vector['3']
    a6 = in_vector['6']
    a7 = in_vector['7']

    a10 = not(a1 and a3)
    a11 = not(a3 and a6)
    a16 = not(a2 and a11)
    a19 = not(a11 and a7)
    a22 = not(a10 and a16)
    a23 = not(a16 and a19)


    out_vec = {'22': int(a22), '23' : int(a23)}

    return out_vec

