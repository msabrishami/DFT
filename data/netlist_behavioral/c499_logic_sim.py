import sys
from collections import OrderedDict
import re
import numpy as np


def Syndrome(R, IC, ID):
    S = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=bool)
    S[0] = (ID[0] ^ ID[4] ^ ID[8] ^ ID[12]) ^ (ID[16] ^ ID[17] ^ ID[18] ^ ID[19]) ^ (
                ID[20] ^ ID[21] ^ ID[22] ^ ID[23]) ^ (R & IC[0])
    S[1] = (ID[1] ^ ID[5] ^ ID[9] ^ ID[13]) ^ (ID[24] ^ ID[25] ^ ID[26] ^ ID[27]) ^ (
                ID[28] ^ ID[29] ^ ID[30] ^ ID[31]) ^ (R & IC[1])
    S[2] = (ID[2] ^ ID[6] ^ ID[10] ^ ID[14]) ^ (ID[16] ^ ID[17] ^ ID[18] ^ ID[19]) ^ (
                ID[24] ^ ID[25] ^ ID[26] ^ ID[27]) ^ (R & IC[2])
    S[3] = (ID[3] ^ ID[7] ^ ID[11] ^ ID[15]) ^ (ID[20] ^ ID[21] ^ ID[22] ^ ID[23]) ^ (
                ID[28] ^ ID[29] ^ ID[30] ^ ID[31]) ^ (R & IC[3])
    S[4] = (ID[16] ^ ID[20] ^ ID[24] ^ ID[28]) ^ (ID[0] ^ ID[1] ^ ID[2] ^ ID[3]) ^ (ID[4] ^ ID[5] ^ ID[6] ^ ID[7]) ^ (
                R & IC[4])
    S[5] = (ID[17] ^ ID[21] ^ ID[25] ^ ID[29]) ^ (ID[8] ^ ID[9] ^ ID[10] ^ ID[11]) ^ (
                ID[12] ^ ID[13] ^ ID[14] ^ ID[15]) ^ (R & IC[5])
    S[6] = (ID[18] ^ ID[22] ^ ID[26] ^ ID[30]) ^ (ID[0] ^ ID[1] ^ ID[2] ^ ID[3]) ^ (ID[8] ^ ID[9] ^ ID[10] ^ ID[11]) ^ (
                R & IC[6])
    S[7] = (ID[19] ^ ID[23] ^ ID[27] ^ ID[31]) ^ (ID[4] ^ ID[5] ^ ID[6] ^ ID[7]) ^ (
                ID[12] ^ ID[13] ^ ID[14] ^ ID[15]) ^ (R & IC[7])
    return S


def Correction(S, ID):
    OD = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  dtype=bool)
    OD[0] = (S[0] & ~S[1] & ~S[2] & ~S[3] & S[4] & ~S[5] & S[6] & ~S[7]) ^ ID[0]
    OD[1] = (~S[0] & S[1] & ~S[2] & ~S[3] & S[4] & ~S[5] & S[6] & ~S[7]) ^ ID[1]
    OD[2] = (~S[0] & ~S[1] & S[2] & ~S[3] & S[4] & ~S[5] & S[6] & ~S[7]) ^ ID[2]
    OD[3] = (~S[0] & ~S[1] & ~S[2] & S[3] & S[4] & ~S[5] & S[6] & ~S[7]) ^ ID[3]
    OD[4] = (S[0] & ~S[1] & ~S[2] & ~S[3] & S[4] & ~S[5] & ~S[6] & S[7]) ^ ID[4]
    OD[5] = (~S[0] & S[1] & ~S[2] & ~S[3] & S[4] & ~S[5] & ~S[6] & S[7]) ^ ID[5]
    OD[6] = (~S[0] & ~S[1] & S[2] & ~S[3] & S[4] & ~S[5] & ~S[6] & S[7]) ^ ID[6]
    OD[7] = (~S[0] & ~S[1] & ~S[2] & S[3] & S[4] & ~S[5] & ~S[6] & S[7]) ^ ID[7]
    OD[8] = (S[0] & ~S[1] & ~S[2] & ~S[3] & ~S[4] & S[5] & S[6] & ~S[7]) ^ ID[8]
    OD[9] = (~S[0] & S[1] & ~S[2] & ~S[3] & ~S[4] & S[5] & S[6] & ~S[7]) ^ ID[9]
    OD[10] = (~S[0] & ~S[1] & S[2] & ~S[3] & ~S[4] & S[5] & S[6] & ~S[7]) ^ ID[10]
    OD[11] = (~S[0] & ~S[1] & ~S[2] & S[3] & ~S[4] & S[5] & S[6] & ~S[7]) ^ ID[11]
    OD[12] = (S[0] & ~S[1] & ~S[2] & ~S[3] & ~S[4] & S[5] & ~S[6] & S[7]) ^ ID[12]
    OD[13] = (~S[0] & S[1] & ~S[2] & ~S[3] & ~S[4] & S[5] & ~S[6] & S[7]) ^ ID[13]
    OD[14] = (~S[0] & ~S[1] & S[2] & ~S[3] & ~S[4] & S[5] & ~S[6] & S[7]) ^ ID[14]
    OD[15] = (~S[0] & ~S[1] & ~S[2] & S[3] & ~S[4] & S[5] & ~S[6] & S[7]) ^ ID[15]
    OD[16] = (S[4] & ~S[5] & ~S[6] & ~S[7] & S[0] & ~S[1] & S[2] & ~S[3]) ^ ID[16]
    OD[17] = (~S[4] & S[5] & ~S[6] & ~S[7] & S[0] & ~S[1] & S[2] & ~S[3]) ^ ID[17]
    OD[18] = (~S[4] & ~S[5] & S[6] & ~S[7] & S[0] & ~S[1] & S[2] & ~S[3]) ^ ID[18]
    OD[19] = (~S[4] & ~S[5] & ~S[6] & S[7] & S[0] & ~S[1] & S[2] & ~S[3]) ^ ID[19]
    OD[20] = (S[4] & ~S[5] & ~S[6] & ~S[7] & S[0] & ~S[1] & ~S[2] & S[3]) ^ ID[20]
    OD[21] = (~S[4] & S[5] & ~S[6] & ~S[7] & S[0] & ~S[1] & ~S[2] & S[3]) ^ ID[21]
    OD[22] = (~S[4] & ~S[5] & S[6] & ~S[7] & S[0] & ~S[1] & ~S[2] & S[3]) ^ ID[22]
    OD[23] = (~S[4] & ~S[5] & ~S[6] & S[7] & S[0] & ~S[1] & ~S[2] & S[3]) ^ ID[23]
    OD[24] = (S[4] & ~S[5] & ~S[6] & ~S[7] & ~S[0] & S[1] & S[2] & ~S[3]) ^ ID[24]
    OD[25] = (~S[4] & S[5] & ~S[6] & ~S[7] & ~S[0] & S[1] & S[2] & ~S[3]) ^ ID[25]
    OD[26] = (~S[4] & ~S[5] & S[6] & ~S[7] & ~S[0] & S[1] & S[2] & ~S[3]) ^ ID[26]
    OD[27] = (~S[4] & ~S[5] & ~S[6] & S[7] & ~S[0] & S[1] & S[2] & ~S[3]) ^ ID[27]
    OD[28] = (S[4] & ~S[5] & ~S[6] & ~S[7] & ~S[0] & S[1] & ~S[2] & S[3]) ^ ID[28]
    OD[29] = (~S[4] & S[5] & ~S[6] & ~S[7] & ~S[0] & S[1] & ~S[2] & S[3]) ^ ID[29]
    OD[30] = (~S[4] & ~S[5] & S[6] & ~S[7] & ~S[0] & S[1] & ~S[2] & S[3]) ^ ID[30]
    OD[31] = (~S[4] & ~S[5] & ~S[6] & S[7] & ~S[0] & S[1] & ~S[2] & S[3]) ^ ID[31]
    return OD


def c499_sim(in_vec_dict):
    # Create the input and output variables (top level)
    ID = np.array([in_vec_dict['in1'], in_vec_dict['in5'], in_vec_dict['in9'], in_vec_dict['in13'], in_vec_dict['in17'],
                   in_vec_dict['in21'], in_vec_dict['in25'], in_vec_dict['in29'], in_vec_dict['in33'],
                   in_vec_dict['in37'], in_vec_dict['in41'], in_vec_dict['in45'], in_vec_dict['in49'],
                   in_vec_dict['in53'], in_vec_dict['in57'], in_vec_dict['in61'], in_vec_dict['in65'],
                   in_vec_dict['in69'], in_vec_dict['in73'], in_vec_dict['in77'], in_vec_dict['in81'],
                   in_vec_dict['in85'], in_vec_dict['in89'], in_vec_dict['in93'], in_vec_dict['in97'],
                   in_vec_dict['in101'], in_vec_dict['in105'], in_vec_dict['in109'], in_vec_dict['in113'],
                   in_vec_dict['in117'], in_vec_dict['in121'], in_vec_dict['in125']], dtype=bool)
    IC = np.array(
        [in_vec_dict['in129'], in_vec_dict['in130'], in_vec_dict['in131'], in_vec_dict['in132'], in_vec_dict['in133'],
         in_vec_dict['in134'], in_vec_dict['in135'], in_vec_dict['in136']], dtype=bool)
    R = np.array([in_vec_dict['in137']], dtype=bool)

    # Call the modules in order
    S = Syndrome(R, IC, ID)
    OD = Correction(S, ID)

    # Get the output dictionary
    out_vec_dict = OrderedDict()
    out_vec_dict['out724'] = OD[0].astype(int)
    out_vec_dict['out725'] = OD[1].astype(int)
    out_vec_dict['out726'] = OD[2].astype(int)
    out_vec_dict['out727'] = OD[3].astype(int)
    out_vec_dict['out728'] = OD[4].astype(int)
    out_vec_dict['out729'] = OD[5].astype(int)
    out_vec_dict['out730'] = OD[6].astype(int)
    out_vec_dict['out731'] = OD[7].astype(int)
    out_vec_dict['out732'] = OD[8].astype(int)
    out_vec_dict['out733'] = OD[9].astype(int)
    out_vec_dict['out734'] = OD[10].astype(int)
    out_vec_dict['out735'] = OD[11].astype(int)
    out_vec_dict['out736'] = OD[12].astype(int)
    out_vec_dict['out737'] = OD[13].astype(int)
    out_vec_dict['out738'] = OD[14].astype(int)
    out_vec_dict['out739'] = OD[15].astype(int)
    out_vec_dict['out740'] = OD[16].astype(int)
    out_vec_dict['out741'] = OD[17].astype(int)
    out_vec_dict['out742'] = OD[18].astype(int)
    out_vec_dict['out743'] = OD[19].astype(int)
    out_vec_dict['out744'] = OD[20].astype(int)
    out_vec_dict['out745'] = OD[21].astype(int)
    out_vec_dict['out746'] = OD[22].astype(int)
    out_vec_dict['out747'] = OD[23].astype(int)
    out_vec_dict['out748'] = OD[24].astype(int)
    out_vec_dict['out749'] = OD[25].astype(int)
    out_vec_dict['out750'] = OD[26].astype(int)
    out_vec_dict['out751'] = OD[27].astype(int)
    out_vec_dict['out752'] = OD[28].astype(int)
    out_vec_dict['out753'] = OD[29].astype(int)
    out_vec_dict['out754'] = OD[30].astype(int)
    out_vec_dict['out755'] = OD[31].astype(int)

    return out_vec_dict


if __name__ == '__main__':
    if len(sys.argv) != 3:  # Check if the input arguments are enough
        print('Not enough arguments. ')
        exit(1)

    input_file = sys.argv[1]  # This is the path for the input file
    output_file = sys.argv[2]  # This is the path for the output file

    # Read the input vector and create the dictionary
    input_file = open(input_file, 'r')
    in_vec_dict = OrderedDict()
    for line in input_file:
        line = line.strip()
        vector_array = re.split(r',', line)
        in_vec_dict[vector_array[0]] = int(vector_array[1])

    # Simulate c499
    out_vec_dict = c499_sim(in_vec_dict)

    # Write output to file
    output_file = open(output_file, 'w')
    for dict_item in out_vec_dict:
        if out_vec_dict[dict_item].astype(int):
            output_file.write('%s,1\n' % dict_item)
        else:
            output_file.write('%s,0\n' % dict_item)
