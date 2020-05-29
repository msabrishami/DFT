##input format(cin, a0, b0, a1, b1)
##output format(sum0, sum1, sum2)



def full_adder(carry_in, a, b):
    sum = a ^ b ^ carry_in
    carry = (a and b) or (carry_in and (a or b))
    return carry,sum

def add2_sim(in_vector):
    cin = in_vector['1']
    a0 = in_vector['2'] 
    b0 = in_vector['3']  
    a1 = in_vector['4'] 
    b1 = in_vector['5']

    cout0, sum0 = full_adder(cin, a0, b0)
    sum2, sum1 = full_adder(cout0, a1, b1)
    out_vector = {'50':sum0, '51':sum1, '52':sum2}   

    return out_vector

