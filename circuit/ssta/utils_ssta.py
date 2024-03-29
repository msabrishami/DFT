import numpy as np
import matplotlib.pyplot as plt

def smooth_hist(vals, window=5):
    """ Average smoothing over a floating point series, it can be a series of 
        PDF values for a distribution, or histogram values. 
    
    Warning: assumption is that both ends of this series converge to zero 
        we pad the data with zero values before smoothing process
        the length of the output is not the same as input if padding added

    Parameters
    ----------
    f_T : list of float 
        value series, both ends are assumed to converge to zero 
    window : int (must be odd)
        smoothing filter length

    Returns
    -------
    sm : list of float
        smoothed series 
    """
    assert len(vals) > 3*window, "Too small to smooth!"
    assert window%2==1, "Window must be odd number"

    hw = int(window/2)
    sm = list(vals) 
        
    for idx in range(len(vals)):
        sm[idx] = np.mean(vals[max(0, idx-hw):min(len(vals)-1, idx+hw+1)])
            
    return sm


def mcraw2mchist(delays, bins, fname=None, cut=None, pad=None, verbose=False):
    """ Gets Monte Carlo raw simulation (mcraw) results and returns 
        Monte Carlo histogram distribution (mchist)

    Parameters
    ----------
    delays : list of float 
        Monte Carlo raw simulation results, unit can vary, usually is ps
    bins :  int
        Number of bins to be used for creating histogram distribution 
    fname : str, optional
        If assigned, stores the results of histogram (mchist)
    cut : tuple of floats, optional
        Histogram resolution drops if outline points are present, if cut is 
        assigned, it cuts the (low, high) percentage of the data. 
    pad : int, optional, must be odd
        If assigned, adds pad number of zero values to both ends of histogram 
        results, also adds extra bin values to equalize lengths of T and f_T

    Returns
    -------
    T, f_T : tuple of Numpy ndarrays, T is bin values, f_T is pdf values

    Warning: using cut can change the distribution drastically! 
    Warning: the name can be missleading, does not return histogram, but a 
        sampling of PDF (refer to np.histogram documentation for density argument)
    """
    Td = delays
    Td.sort()
    # Note: in np.histogram, len(f)=len(T)+1
    if cut:
        low = Td[int(len(delays)*cut)]
        high = Td[-int(len(delays)*cut)]
        f_T, _T = np.histogram(Td, bins=bins, range=cuts, density=True)
    else:
        f_T, _T = np.histogram(Td, bins=bins, density=True)
    
    
    T = np.zeros(len(f_T))
    for idx in range(len(f_T)):
        T[idx] = (_T[idx] + _T[idx+1])/2 # len(T)=len(f_T)
    
    if pad:
        f_T = np.append([0]*pad, f_T)
        f_T = np.append(f_T, [0]*pad)
        T_start = [T[0] - (k+1)*(T[1]-T[0]) for k in reversed(range(pad))]
        T_end = [T[-1] + (k+1)*(T[-1] - T[-2]) for k in range(pad)]
        T = np.append(T_start, T)
        T = np.append(T, T_end)
    
    if fname==None:
        return T, f_T

    outfile = open(fname, "w")
    for idx in range(len(T)):
        # print(idx, T[idx], f_T[idx])
        outfile.write("{}\t{}\n".format(T[idx], f_T[idx]))
    outfile.close()
    if verbose:
        print("PMF saved in {}".format(fname))

    return T, f_T


def load_mcraw(fname):
    """ Loading Monte Carlo simulation results
    A simple file (fname) with delay values in each line 
    The unit for values can vary, usually it is in ps """ 
    lines = open(fname, "r").readlines()
    lines = [float(line) for line in lines]
    print("Loaded {} with {} values".format(fname, len(lines)))
    return lines

def load_mchist(fname):
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


def plot_pmf(dist, fname=None):
    x1, y1 = dist.pmf()
    plt.plot(x1, y1, linewidth=2, color='blue', linestyle='--')
    plt.grid()
    if fname:
        plt.savefig(fname)
    plt.close()

def get_cmap(n, name='prism'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


