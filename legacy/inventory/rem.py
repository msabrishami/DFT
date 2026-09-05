def get_inp_plus_one(tp):
    # for t in reversed[tp]:
    i = len(tp)-1
    success = False
    while tp[i]>=0:
        if tp[i] == 0:
            tp[i] = 1
            success = True
            break
        else:
            tp[i] = 0
            i-=1
            print(i)
            print
            if i == -1:
                success = False
                break

    return success, tp

print(get_inp_plus_one([1,1,0,0]))