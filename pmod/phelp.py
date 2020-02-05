from matplotlib import pyplot as __plt__

import tcheck as __check__
import mathops as __mops__

# Graphing functions


def __ecc_plot__(x, y, label = None, lims = None, fontsize = 20, save = False, save_name = 'plot.jpg'):
    # ECC

    # Dummy Check for 'x' and 'y'
    if(not __check__.array_test(x)):
        print("[__ecc_plot__] Error: 'x' must be an array")  
        return False    
    if(not __check__.array_test(y)):
        print("[__ecc_plot__] Error: 'y' must be an array") 
        return False      
            
    # Checking 'x' for proper formating
    xnumeric = True 
    xarray = True
    for i in x:
        if(__check__.numeric_test(i)):
            xarray = False 
        elif(__check__.array_test(i)):
            xnumeric = False 
            for j in i:
                if(not __check__.numeric_test(j)):
                    xarray = False
        else:
            xnumeric, xarray = False, False 
    if(xarray == False and xnumeric == False):
        print("[__ecc_plot__] Error: input 'x' must either be a numeric array or an array of numeric arrays") 
        return False

    # Checking 'y' for proper formating              
    ynumeric = True 
    yarray = True
    for i in y:
        if(__check__.numeric_test(i)):
            yarray = False 
        elif(__check__.array_test(i)):
            ynumeric = False 
            for j in i:
                if(not __check__.numeric_test(j)):
                    yarray = False
        else:
            ynumeric, yarray = False, False 
    if(yarray == False and ynumeric == False):
        print("[__ecc_plot__] Error: input 'y' must either be a numeric array or an array of numeric arrays") 
        return False
    
    # Special check for a set of y arrays   

    if(yarray and not xarray):
        for i in xrange(len(y)):
            if(len(x) != len(y[i])): 
                print("[__ecc_plot__] Warning: 'x' should corrospond 1-to-1 to each array in 'y'")
                print("Will attempt to coerce each array in 'y' to the length of 'x'") 
                return False

    if(xarray and not yarray):
        print("[__ecc_plot__] Error: if 'x' is an array of arrays, then 'y' must be as well")
        return False    
           
    if(xarray):
        if(len(x) != len(y)):
            print("[__ecc_plot__] Error: if 'x' is an array of arrays, then it must have the same length as 'y'")
            return False
        else:
            for i in xrange(len(x)):
                if(len(x[i]) != len(y[i])): 
                    errmsg = "[__ecc_plot__] Warning: each respective entry of 'x' "
                    errmsg = errmsg + "should corrospond 1-to-1 to the 'y' entry"
                    print(errmsg)    
                    return False
     
    # Label checks            
    labre = False
    if(not __check__.array_test(label)):
        if(label != None):
            print("[__ecc_plot__] Warning: input 'label' is not an array and has been deprecated") 
        labre = True  
    else:
        if(len(label) < 2):
            print("[__ecc_plot__] Warning: input 'label' has a length less than 2 and has been deprecated") 
            labre = True
        else:
            xlabel, ylabel = label[0], label[1]
            if(not isinstance(xlabel,str)):
                labre = True        
            if(not isinstance(ylabel,str)):
                labre = True                         
              
    # Limit checks
             
    limre = False
    if(not __check__.array_test(lims)):
        if(lims != None):
            print("[__ecc_plot__] Warning: input 'lims' is not an array and has been deprecated") 
        limre = True  
    else:
        if(len(lims) < 2):
            print("[__ecc_plot__] Warning: input 'lims' has a length less than 2 and has been deprecated") 
            limre = True
        else:
            xlims, ylims = lims[0], lims[1]
            if(__check__.array_test(xlims)):
                if(not __check__.numeric_test(xlims[0]) or not __check__.numeric_test(xlims[1])):
                    limre = True 
            else:
                limre = True 
            if(__check__.array_test(ylims)):
                if(not __check__.numeric_test(ylims[0]) or not __check__.numeric_test(ylims[1])):
                    limre = True      
            else:
                limre = True          
                                   
    # Checking the rest of the input variables
    if(__check__.numeric_test(fontsize)):
        fontsize = int(fontsize)
    else:
        fontsize = 30 
             
    if(not isinstance(save,bool)):
        save = False          

    if(not isinstance(save_name, str)):
        save_name = 'plot.jpg'    
             
    output = (xarray, yarray ,labre, limre, fontsize, save, save_name)
    return output
              

def new_plot(x, y, label = None, lims = None, fontsize = 30, save = False, save_name = 'plot.jpg'):

    test = __ecc_plot__(x, y, label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: input test failed, see preceding error msg for details")
        return False  
    else:
        xarray, yarray ,labre, limre, fontsize, save, save_name = test
        
    xysep, ysep, sep = False, False, False
    if(xarray and yarray): 
        xysep = True 
    elif(yarray):
        ysep = True 
    else:
        sep = True 

    if(labre):
        label = (None, None)
    if(limre):
        lims = (None, None)

    xlab, ylab = label[0], label[1]
    xlim, ylim = lims[0], lims[1]

                   
    __plt__.figure()
    __plt__.rc('xtick',labelsize=16)
    __plt__.rc('ytick',labelsize=16)

    if(sep):
        __plt__.plot(x, y, linewidth = 2.5)
    elif(ysep):
        for i in y:
            __plt__.plot(x, i, linewidth = 2.5)
    elif(xysep):
        for i in xrange(len(x)):
            __plt__.plot(x[i], y[i], linewidth = 2.5)

    if(xlab != None):
        __plt__.ylabel(ylab, fontsize = fontsize, labelpad = 20)
    if(ylab != None):
        __plt__.xlabel(xlab, fontsize = fontsize, labelpad = 20)
    if(xlim != None):
        __plt__.xlim(xlim[0],xlim[1])
    if(ylim != None):
        __plt__.ylim(ylim[0],ylim[1])
             
    __plt__.show()
    if(save):
        __plt__.savefig(save_name)    
    return True  


def new_smooth_plot(x, y, label = None, lims = None, smoothness = 300,
                    fontsize = 30, save = False, save_name = 'plot.jpg'):    

    test = __ecc_plot__(x, y, label, lims, fontsize, save, save_name)
    if(test == False):
        print("[new_plot] Error: input test failed, see preceding error msg for details")
        return False  
    else:
        xarray, yarray ,labre, limre, fontsize, save, save_name = test
        
    xysep, ysep, sep = False, False, False


    if(xarray and yarray): 
        xysep = True 
    elif(yarray):
        ysep = True 
    else:
        sep = True 

    if(labre):
        label = (None, None)
    if(limre):
        lims = (None, None)

    xlab, ylab = label[0], label[1]
    xlim, ylim = lims[0], lims[1]

    spln_inst = __mops__.spline()
                   
    __plt__.figure()
    __plt__.rc('xtick',labelsize=16)
    __plt__.rc('ytick',labelsize=16)

    if(sep):
        xsmooth = span_vec(x, smoothness)  
        spln_inst.pass_vecs(x, y, xsmooth)
              
        spln_inst.pass_spline()
        ysmooth = spln_inst.get_spline()   

        __plt__.plot(xsmooth, ysmooth, linewidth = 2.5)
    elif(ysep):
        for i in y:
            xsmooth = span_vec(x, smoothness)  
            spln_inst.pass_vecs(x, i, xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   

            __plt__.plot(xsmooth, ysmooth, linewidth = 2.5)
    elif(xysep):
        for i in xrange(len(x)):
            xsmooth = span_vec(x[i], smoothness)  
            spln_inst.pass_vecs(x[i], y[i], xsmooth)
                  
            spln_inst.pass_spline()
            ysmooth = spln_inst.get_spline()   

            __plt__.plot(xsmooth, ysmooth, linewidth = 2.5)

    if(xlab != None):
        __plt__.ylabel(ylab, fontsize = fontsize, labelpad = 20)
    if(ylab != None):
        __plt__.xlabel(xlab, fontsize = fontsize, labelpad = 20)
    if(xlim != None):
        __plt__.xlim(xlim[0],xlim[1])
    if(ylim != None):
        __plt__.ylim(ylim[0],ylim[1])
             
    __plt__.show()
    if(save):
        __plt__.savefig(save_name)    
    return True  




def new_four_plot(tl_data, tr_data, bl_data, br_data, label = None, axlabel = None, save = False):

    fig, axs = __plt__.subplots(2, 2, sharex=False, sharey=False)
    
    if(not __check__.array_test(label)):
        label = [' ',' ',' ',' ']        
    else:
        if(len(label) != 4): 
            label = [' ',' ',' ',' ']
        
     
    axs[0, 0].plot(tl_data[0], tl_data[1])
    if(nxlo == 'x'):
        axs[0, 0].plot(tl_data[2], tl_data[3])
    axs[0, 0].set_title(label[0])
    
    axs[0, 1].plot(tr_data[0], tr_data[1])
    if(nxlo == 'x'):    
        axs[0, 1].plot(tr_data[2], tr_data[3])
    axs[0, 1].set_title(label[1])
    
    axs[1, 0].plot(bl_data[0], bl_data[1])
    if(nxlo == 'x'):
        axs[1, 0].plot(bl_data[2], bl_data[3])
    axs[1, 0].set_title(label[2])
    
    axs[1, 1].plot(br_data[0], br_data[1])
    if(nxlo == 'x'):
        axs[1, 1].plot(br_data[2], br_data[3])
    axs[1, 1].set_title(label[3])
    
    for ax in axs.flat:
        ax.set(xlabel='p ($fm^{-1}$)', ylabel='V (fm)')
        
    __plt__.tight_layout()
    __plt__.show()
        
    if(save):
#        print(fig_file(nxlo,fig).split('.')[0])
        fig.savefig(fig_file(nxlo,fig_num).split('.')[0]+'.pdf')
