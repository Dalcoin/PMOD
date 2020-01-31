
import numpy as __np__
import math as __mt__ 

from matplotlib import pyplot as __plt__

from scipy.interpolate import interp1d as __spln__    
from scipy.interpolate import splrep as __bspln__
from scipy.interpolate import splev as __deriv__
from scipy.interpolate import splint as __integ__

from scipy.integrate import quad as __definteg__

import tcheck as __check__

'''
functions for rounding numbers

The version of python must be passed for relevent functions:

   * rounding functions: 

   | Inputs must be numeric |

   pyver : '26' or '27' are supported

   str_bool : True for a string return, else False for a numeric return.
              Warning: the returned value will be cast to the type of the original input object.
     
''' 
            

# Rounding functions 

def round_decimal(num, deci, str_bool=True):
    
    # round_decimal(30.112,1,True)
    
    # x: input file string
    # d: non-zero integer
    # string: boolean, String if True, Float if false

    test = __check__.type_test_print(num,'num','num','round_decimal')
    if(not test):
        return test 
    test = __check__.type_test_print(deci,int,'deci','round_decimal')
    if(not test):
        return test 
    test = __check__.type_test_print(str_bool,bool,'str_bool','round_decimal') 
    if(not test):
        return test 
    
    if(deci < 0):
        print("[round_decimal] Error: 'deci' decimal value must be non-negative")
        return False
    
    num = float(num)                
    fm = '%.' + str(int(deci)) + 'f'
    rnum = fm % num

    if(str_bool):
        if(deci > 0):
            output = str(rnum)
            return output
        else:
            output = str(int(rnum))+'.'
            return output          
    else:
        if(deci > 0):
            output = float(rnum)
            return output
        else:
            output = int(rnum)
            return output                  


def round_scientific(num, digi, pyver = '27', str_bool = True):
    
    # round_scientific(30.112,1,True)    
    # num: input file string
    # d: a non-negative integer signifying the number of significant digits

    test = __check__.type_test_print(num,'num','num','round_scientific') 
    if(not test):
        return test 
    test = __check__.type_test_print(digi,int,'digi','round_scientific')
    if(not test):
        return test 
    test = __check__.type_test_print(str_bool,bool,'str_bool','round_scientific') 
    if(not test):
        return test 
    
    if(digi < 0):
        print("[round_scientific] Error: 'digi' decimal value must be non-negative")
        return False

    num = float(num)
    if(pyver == '27'):        
        fm = "{:." + str(int(digi)-1) + "e}"
        rnum = fm.format(num)
    elif(pyver == '26'):
        fm = "{0:." + str(int(digi)-1) + "e}"
        rnum = fm.format(num)             
    else:
        print("[round_scientific] Error: 'pyver' not recognized'")
        return False        
         
    if(str_bool):
        return str(rnum)
    else:
        return float(rnum)    


def round_uniform(num, pyver = '27'):
    
    test = __check__.type_test_print(num,'num','num','round_uniform') 
    if(not test):
        return test 

    num = float(num)
        
    pos_bool = (num > 0.0)
    neg_bool = (num < 0.0)
    nul_bool = (num == 0.0)
     
    if(pos_bool):
        if(num < 10000000):
            output = round_decimal(num,6)
            for i in range(6):
                if(num > 10.0**(i+1)):
                    output = round_decimal(num,6-(i+1))
                    if(i == 6):
                        output = output+'.'
        if(num >= 10000000):
            output = round_scientific(num,3,pyver)
        if(num < 0.000001):
            output = round_scientific(num,3,pyver)
    elif(neg_bool):
        if(num > -1000000):
            output = round_decimal(num,5)
            for i in range(5):
                if(num < -10.0**(i+1)):
                    output = round_decimal(num,5-(i+1))   
                    if(i == 5):
                        output = output+'.'
        if(num <= -1000000):
            output = round_scientific(num,2,pyver)
        if(num > -0.000001):
            output = round_scientific(num,2,pyver)
    else:
        output = '0.000000'
    return output



def span_vec(xvec, nspan):
    '''
    Description: generates a list which spans the range of numerical 
                 array 'xvec' with 'nspan' number of equally spaced floats

    Inputs: 
     
        'xvec' : A python array containing numeric values 
        'nspan': The length of the generated spanning array 
        
    Output: 
       
        'span_list' : A list of equally spaced floats spanning the range of 'xvec'
        False       : if an error is detected  
    '''

    test = __check__.array_test(xvec)
    if(not test):
        print("[span_vec] TypeError: 'xvec' must be a python array")
        return False 
    else:
        if(not isinstance(xvec,list)):
            xvec = list(xvec)
    test = isinstance(nspan, int) and nspan > 2 
    if(not test):
        print("[span_vec] Error: 'nspan' must be an integer at least equal to 3")
        return False      
     
    xl = min(xvec)
    xu = max(xvec)
     
    test = __check__.numeric_test(xl) and __check__.numeric_test(xu)
    if(not test or xl == xu): 
        print("[span_vec] TypeError: 'xvec' should be an array of unique numeric values")
     
    inc = (float(xu) - float(xl))/float((nspan-1))
    span_list = [float(xl)]
    for i in range(nspan-1):
        val = xl+float(i+1)*(inc)
        span_list.append(val) 
    return span_list    

   

class spline:
    '''
    class spline:

        spline(x_array, y_array, x_array = x_points_array)

        A class for performing 1-D spline and calculus operations on 
        discreet arrays of points. 

        A note on usage: this class is only meant to be used as a quick
                         means to estimate splined values or the derivatives
                         and integrals of two sets of data with the relationship,
                         f(X) = Y. This module is not meant to be used when 
                         accuracy is important, nor is it meant to be scalable and 
                         used for a large number of operations. 
    '''

    def __init__(self, x_vec = None, y_vec = None, xarray = None):
        self.x_vec = x_vec
        self.y_vec = y_vec 

        #Values to be passed 
        self.spline_inst = None
        self.bspline_inst = None 
        self.xarray = xarray 
        
        #Values to get 
        self.spln_array = None
        self.der_array = None
        self.int = None     

        #Values for variables
        self.a = None 
        self.b = None 
        self.der = None   
    

    def pass_vecs(self, x_vec, y_vec, xarray = None):
        self.x_vec = x_vec  
        self.y_vec = y_vec  
        self.xarray = xarray  

    def pass_newx_vec(self, xarray, der = None):
        self.xarray = xarray       
        self.der    = der

    def pass_int_lim(self,a,b):
        self.a = a 
        self.b = b  


    def spln_obj(self, x_arr, y_arr, type = 'spline', sort = 'cubic'):

        test = __check__.type_test_print(x_arr,'arr','x_arr','spln_obj')
        if(not test):
            return test 
        test = __check__.type_test_print(y_arr,'arr','y_arr','spln_obj')
        if(not test):
            return test 
        test = __check__.type_test_print(type,str,'type','spln_obj')   
        if(not test):
            return test 
        test = __check__.type_test_print(sort,str,'sort','spln_obj')  
        if(not test):
            return test 

        if(type == 'spline'):

            try: 
                spline = __spln__(x_arr, y_arr, kind=sort)
                return spline
            except: 
                spline = False 
                print("[spln_obj] Error: spline object generation failed") 
                return spline

        elif(type == 'bspline'):

            try: 
                bspline = __bspln__(x_arr, y_arr)
                return bspline
            except: 
                bspline = False 
                print("[spln_obj] Error: bspline object generation failed") 
                return bspline

        else: 
            print("[spln_obj] Error: input variable 'type' is not recognized string")
            return False


    def pass_spline(self, x_arr = None, y_arr = None, sort = 'cubic'):
        try:
            if(x_arr != None and y_arr != None):
                self.x_vec = x_arr 
                self.y_vec = y_arr
            self.spline_inst = self.spln_obj(self.x_vec, self.y_vec, type = 'spline', sort = 'cubic')
            return True
        except:
            return False       

    def pass_bspline(self, x_arr = None, y_arr = None):
        try:
            if(x_arr != None and y_arr != None):
                self.x_vec = x_arr 
                self.y_vec = y_arr
            self.bspline_inst = self.spln_obj(x_arr, y_arr, type = 'bspline', sort = 'cubic')
            return True
        except:
            return False

    def spln_val(self, spline, xvals_arr):

        test = __check__.type_test_print(spline,__spln__,'spline','spln_val') 
        if(not test):
            return test 
        test = __check__.type_test_print(xvals_arr,'arr','xvals_arr','spln_val') 
        if(not test):
            return test 

        try:
            spline_vals = spline(xvals_arr)
            return(spline_vals)
        except: 
            return False 


    def spln_der(self, bspline, xvals_arr, der = 1):

        test = __check__.type_test_print(bspline,__bspln__,'spline','spln_der') 
        if(not test):
            return test 
        test = __check__.type_test_print(xvals_arr,'arr','xvals_arr','spln_der') 
        if(not test):
            return test 
        test = __check__.type_test_print(der,int,'der','spln_der') 
        if(not test):
            return test 

        try:    
            der_vals = __deriv__(xvals_arr, bspline, der)
            return(der_vals) 
        except: 
            return False 


    def spln_integ(self, bspline, a, b):

        test = __check__.type_test_print(bspline,__bspln__,'spline','spln_integ') 
        if(not test):
            return test 
        test = __check__.type_test_print(a,'num','a','spln_integ')
        if(not test):
            return test 
        test = __check__.type_test_print(b,'num','b','spln_integ') 
        if(not test):
            return test 

        try:    
            int_vals = __integ__(a,b,bspline)
            return(der_vals)
        except: 
            return False 

    ### Functions for performing 1-D splines, derivatives and integrals

    def get_spline(self, in_xarray = None):
        if(self.spline_inst != None and in_xarray == None):  
            try:
                result = self.spln_val(self.spline_inst, self.xarray)
                self.spln_array = (self.xarray, result) 
                return result
            except:
                print("[get_spline] Error 0: unknown error occured when trying to create spline") 
                return False               
        elif(self.spline_inst == None):
            print("Error: No spline instance found, initialize a spline instance and try again") 
            return False
        elif(self.xarray == None):
            if(in_xarray == None):
                print("Error: No xspline vector found, input an xspline vector and try again") 
                return False
            else:
                try:
                    self.xarray = in_xarray
                    result = self.spln_val(self.spline_inst, self.xarray)
                    self.spln_array = (self.xarray, result) 
                    return result                        
                except:           
                    print("[get_spline] Error 1: unknown error occured when trying to create spline") 
                    return False   
        else:           
            print("[get_spline] Error 2: unknown error occured when trying to create spline") 
            return False                                            

    def get_deriv(self, in_xarray, der = 1):
        if(in_xarray == None):
            try: 
                result = self.spln_der(self.bspline_inst, self.xarray, der = self.der)
                self.der_array = (self.xarray, result, self.der) 
                return result  
            except:
                return False
        else:
            try: 
                self.xarray = in_xarray
                self.der = der
                result = self.spln_der(self.bspline_inst, self.xarray, der = self.der)
                self.der_array = (self.xarray, result, self.der) 
                return result  
            except:
                return False

    def get_integ(self, a = None, b = None):
        if(a == None and b == None): 
            try: 
                result = self.spln_integ(self, self.bspline_inst, self.a, self.b)
                self.int_inst = (result, self.a, self.b) 
                return result  
            except:
                return False
        else:
            try: 
                self.a = a 
                self.b = b 
                if(not __check__.numeric_test(a) or not __check__.numeric_test(b,'')):
                    print("[get_integ] Error: check that the limits of integration are numeric types")
                    return False    
                result = self.spln_integ(self, self.bspline_inst, self.a, self.b)
                self.int_inst = (result, self.a, self.b) 
                return result  
            except:
                return False
        
             
     
    # SCOS (Self-Contained One-Shot: does not use class variables) 

    def spline_val_scos(self, xvals_arr, x_arr, y_arr, der = 0 , type = 'cubic'):

        test = __check__.type_test_print(xvals_arr,'arr','xvals_arr','spline_val_scon')     
        if(not test):
            return test 
        test = __check__.type_test_print(der,int,'der','spline_val_scon')    
        if(not test):
            return test 
        
        if(der < 0):
            print("[spline_val_scon] Error: 'der' must be non-negative")
            return False

        if(der == 0):    
            try:
                spline = __spln__(x_arr,y_arr,kind=type)
                spline_vals = spline(xvals_arr)
                return(spline_vals)
            except:
                print("[spline_val_scon] Error: spline function(s) failed")
                return False
        if(der > 0):
            try:
                bspline_obj = __bspln__(x,y)
                der_spline_vals = __deriv__(xvals_arr,bspline_obj,der)
                return(der_spline_vals)
            except:
                print("[spline_val_scon] Error: bspline function(s) failed")
                return False
   
 
    def spline_integ_scos(self, x_arr, y_arr, a, b, tol = 0.000001, nlim = 1000):
        
        test = __check__.type_test_print(x_arr,'arr','x_arr','spline_integ')
        if(not test):
            return test 
        test = __check__.type_test_print(y_arr,'arr','y_arr','spline_integ')            
        if(not test):
            return test 
        test = __check__.type_test_print(a,'num','a','spline_integ')
        if(not test):
            return test 
        test = __check__.type_test_print(b,'num','b','spline_integ')          
        if(not test):
            return test 
        test = __check__.type_test_print(tol,float,'tol','spline_integ')
        if(not test):
            return test 
        test = __check__.type_test_print(nlim,int,'nlim','spline_integ') 
        if(not test):
            return test         

        try: 
            bspline_obj = __bspln__(x_arr,y_arr)
            int_spline_val = __integ__(a,b,bspline_obj)
        except:
            int_spline_val = False 
            print("[spline_integ] Error: integral evaluation error")   

        return(int_spline_val)


    # Utility Functions 




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

    spln_inst = spline()
                   
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
