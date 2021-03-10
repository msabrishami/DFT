
import numpy as np
import config
import matplotlib.pyplot as plt

def ckt_type(cname):
    print("FIX ME LATER -- CKT TYPE AUTOMATIC DETECTION")
    return "EPFL"
    if cname in config.ALL_ISCAS85:
        return "ISCAS85"
    elif cname in config.ALL_EPFL:
        return "EPFL"
    else:
        raise NameError("Circuit is not known")




#### COPIED FROM StatisticsSTA.utils


def smooth_hist(f_T, window=5):
    """ No mathematical background is here, just practical """ 
    hw = int(window/2)
    sm = [0]*len(f_T)
    if len(f_T) < 3*window:
        print("Too small to smooth!")
        return 
    if window%2 == 0:
        print("Window must be odd number")
        return
    for idx in range(len(f_T)):
        if idx < hw or idx > len(f_T)-hw-1:
            sm[idx] = f_T[idx]
        else:
            sm[idx] = np.mean(f_T[idx-hw:idx+hw+1])
    
    return sm


def save_mchist(delays, fname, bins, cut=None, verbose=False):
    Td = list(delays)
    if cut:
        Td.sort()
        low = Td[int(len(delays)*cut)]
        high = Td[-int(len(delays)*cut)]

    freq, T = np.histogram(Td, bins=bins, range=(low, high))
    outfile = open(fname, "w")
    for idx in range(len(freq)):
        outfile.write("{}\t{}\n".format(T[idx], freq[idx]))
    outfile.close()
    if verbose:
        print("PMF saved in {}".format(fname))


def load_mchist(fname):
    fname = "../data/cell_ssta/cell_mchist/MOSFET_16nm_LP_cnand2_vth0-N0.05_lg-N0.05_w-N0.10_toxe-N0.10_ndep-N0.05_MC5000.mchist"
    infile = open(fname)
    T = []
    f_T = []
    for line in infile:
        T.append(float(line.strip().split()[0]))
        f_T.append(float(line.strip().split()[1]))
    
    return np.asarray(T), np.asarray(f_T)


def hist2pmf(T, h_T):
    f_T = np.zeros(len(T))
    tot = np.sum(h_T)
    for idx in range(len(T)-1):
        dT = T[idx+1] - T[idx]
        f_T[idx] = (h_T[idx]/tot) / dT

    f_T[-1] = f_T[-2]
    return (T, f_T)


def plot_pmf(dist):
    x1, y1 = dist.pmf()
    plt.plot(x1, y1, linewidth=2, color='blue', linestyle='--')
    plt.grid()

def get_cmap(n, name='prism'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


