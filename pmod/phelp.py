# phelp (plot help)

from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

from pmod import ioparse as iop






def new_plot(x, y, xlabel = '', ylabel = '', ylim = None, xlim = None, save = False, save_name = 'plot.txt'):
    plt.plot(x, y)
    plt.ylabel(ylabel, fontsize = 20)
    plt.xlabel(xlabel, fontsize = 20)
    if(ylim != None):
        plt.ylim(ylim[0],ylim[1])
    if(xlim != None):
        plt.xlim(xlim[0],xlim[1])
    if(save):
        plt.savefig(save_name)    
    return None     


def new_smooth_plot(x, y, smooth = 300, xlabel = '', ylabel = '', 
                    ylim = None, xlim = None, save = False, save_name = 'plot.txt'):
 
    xnp = np.array(x) 
    ynp = np.array(y)
    xsmooth = np.linspace(xnp.min(), xnp.max(), smooth) 
    spl = make_interp_spline(xnp, ynp, k=3)  # type: BSpline
    ysmooth = spl(xsmooth)

    new_plot(xsmooth, 
             ysmooth, 
             xlabel = xlabel, 
             ylabel = ylabel, 
             ylim = ylim, 
             xlim = xlim, 
             save = save, 
             save_name = save_name)
    return None
