#__________________________________________________#
#_____________________levelization_________________#
#__________________________________________________#
def lev (nodelist, Nnodes):
    # Nnodes is number of nodes
    count = Nnodes
    max = 0
    for i in nodelist:
        if i.gtype == 'IPT':
            i.lev = 0
            count -= 1
        else:
            i.lev = -1

    while count:
        for i in nodelist:
            if i.lev == -1:
                for k in range(0, i.fin):
                    flag = 0
                    if i.unodes[k].lev == -1:
                        flag = 1
                        break
                
                if flag == 0:
                    for j in range(0, i.fin):
                        if i.unodes[j].lev >= max:
                            max = i.unodes[j].lev
                    i.lev = max + 1
                    count -= 1
    a = nodelist.copy()
    a.sort(key=lambda x: x.lev)
    return a