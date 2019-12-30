
import math as mt 
from scipy.interpolate import interp1d as spln    
from scipy.interpolate import splrep as bspln
from scipy.interpolate import splev as deriv
from scipy.interpolate import splint as integ

import tcheck as check

'''
functions for rounding numbers

The version of python must be passed for relevent functions:

   For all rounding functions: 

   | Inputs must be numeric |

   pyver : '26' or '27' are supported

   str_bool : True for a string return, else False for a numeric return.
              Warning: the returned value will be cast to the type of the original input object.
     
''' 
            

def round_decimal(num, deci, str_bool=True):
    
    # round_decimal(30.112,1,True)
    
    # x: input file string
    # d: non-zero integer
    # string: boolean, String if True, Float if false

    test = check.type_test_print(num,'num','num','round_decimal')
    if(not test):
        return test 
    test = check.type_test_print(deci,int,'deci','round_decimal')
    if(not test):
        return test 
    test = check.type_test_print(str_bool,bool,'str_bool','round_decimal') 
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
    # x: input file string
    # d: a non-negative integer signifying the number of significant digits

    test = check.type_test_print(num,'num','num','round_scientific') 
    if(not test):
        return test 
    test = check.type_test_print(deci,int,'deci','round_scientific')
    if(not test):
        return test 
    test = check.type_test_print(str_bool,bool,'str_bool','round_scientific') 
    if(not test):
        return test 
    
    if(deci < 0):
        print("[round_scientific] Error: 'digi' decimal value must be non-negative")
        return False

    num = float(num)
    if(pyver == '27'):        
        fm = "{:." + str(int(digi)-1) + "e}"
        rnum = fm.format(x)
    elif(pyver == '26'):
        fm = "{0:." + str(int(digi)-1) + "e}"
        rnum = fm.format(x)             
    else:
        print("[round_scientific] Error: 'pyver' not recognized'")
        return False        
         
    if(str_bool):
        return str(rnum)
    else:
        return float(rnum)    


def round_uniform(num, pyver = '27'):
    
    test = check.type_test_print(num,'num','num','round_uniform') 
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


    def pass_vals(self, x_vec, y_vec, xarray = None):
        self.x_vec = x_vec 
        self.y_vec = y_vec 
        self.xarray = xarray  

    def pass_xarr(self,xarray):
        self.xarray = xarray       

    def pass_int_lim(self,a,b):
        self.a = a 
        self.b = b  


    def spln_obj(self, x_arr, y_arr, type = 'spline', sort = 'cubic'):

        test = check.type_test_print(x_arr,'arr','x_arr','spln_obj')
        if(not test):
            return test 
        test = check.type_test_print(y_arr,'arr','y_arr','spln_obj')
        if(not test):
            return test 
        test = check.type_test_print(type,str,'type','spln_obj')   
        if(not test):
            return test 
        test = check.type_test_print(sort,str,'sort','spln_obj')  
        if(not test):
            return test 

        if(type == 'spline'):

            try: 
                spline = spln(x_arr,y_arr,kind=sort)
                return spline
            except: 
                spline = False 
                print("[spln_obj] Error: spline object generation failed") 
                return spline

        elif(type == 'bspline'):

            try: 
                bspline = bspln(x,y)
                return bspline
            except: 
                bspline = False 
                print("[spln_obj] Error: bspline object generation failed") 
                return bspline

        else: 
            print("[spln_obj] Error: 'type' not recognized")
            return False


    def pass_spline(self, x_arr, y_arr, type = 'spline', sort = 'cubic'):
        try:
            self.spline_inst = spln_obj(x_arr, y_arr, type = 'spline', sort = 'cubic')
            return True
        except:
            return False       

    def pass_bspline():
        try:
            self.spline_inst = spln_obj(x_arr, y_arr, type = 'bspline', sort = 'cubic')
            return True
        except:
            return False

    def spln_val(self, spline, xvals_arr):

        test = check.type_test_print(spline,spln,'spline','spln_val') 
        if(not test):
            return test 
        test = check.type_test_print(xvals_arr,'arr','xvals_arr','spln_val') 
        if(not test):
            return test 

        try:
            spline_vals = spline(xvals_arr)
            return(spline_vals)
        except: 
            return False 


    def spln_der(self, bspline, xvals_arr, der = 1):

        test = check.type_test_print(bspline,bspln,'spline','spln_der') 
        if(not test):
            return test 
        test = check.type_test_print(xvals_arr,'arr','xvals_arr','spln_der') 
        if(not test):
            return test 
        test = check.type_test_print(der,int,'der','spln_der') 
        if(not test):
            return test 

        try:    
            der_vals = deriv(xvals_arr,bspline,der)
            return(der_vals) 
        except: 
            return False 


    def spln_integ(self, bspline, a, b):

        test = check.type_test_print(bspline,bspln,'spline','spln_integ') 
        if(not test):
            return test 
        test = check.type_test_print(a,'num','a','spln_integ')
        if(not test):
            return test 
        test = check.type_test_print(b,'num','b','spln_integ') 
        if(not test):
            return test 

        try:    
            int_vals = integ(a,b,bspline)
            return(der_vals)
        except: 
            return False 

    ### Functions for performing 1-D splines, derivatives and integrals

    def get_spline(self):
        try: 
            result = self.spln_val(self.spline_inst, self.xarray)
            self.spln_array = (result, self.xarray) 
            return result  
        except:
            return False

    def get_der(self):
        try: 
            result = self.spln_der(self.bspline_inst, self.xarray, der = self.der)
            self.der_array = (result, self.der) 
            return result  
        except:
            return False

    def get_int(self):
        try: 
            result = self.spln_integ(self, self.bspline_inst, self.a, self.b)
            self.int_inst = (result, self.a, self.b) 
            return result  
        except:
            return False
             
     
    # SCOS (Self-Contained One-Shot: does not use class variables) 

    def spline_val_scos(self, xvals_arr, x_arr, y_arr, der = 0 , type = 'cubic'):

        test = check.type_test_print(xvals_arr,'arr','xvals_arr','spline_val_scon')     
        if(not test):
            return test 
        test = check.type_test_print(der,int,'der','spline_val_scon')    
        if(not test):
            return test 
        
        if(der < 0):
            print("[spline_val_scon] Error: 'der' must be non-negative")
            return False

        if(der == 0):    
            try:
                spline = spln(x_arr,y_arr,kind=type)
                spline_vals = spline(xvals_arr)
                return(spline_vals)
            except:
                print("[spline_val_scon] Error: spline function(s) failed")
                return False
        if(der > 0):
            try:
                bspline_obj = bspln(x,y)
                der_spline_vals = deriv(xvals_arr,bspline_obj,der)
                return(der_spline_vals)
            except:
                print("[spline_val_scon] Error: bspline function(s) failed")
                return False
   
 
    def spline_integ_scos(self, x_arr, y_arr, a, b, tol = 0.000000001, nlim = 1000):
        
        test = check.type_test_print(x_arr,'arr','x_arr','spline_integ')
        if(not test):
            return test 
        test = check.type_test_print(y_arr,'arr','y_arr','spline_integ')            
        if(not test):
            return test 
        test = check.type_test_print(a,'num','a','spline_integ')
        if(not test):
            return test 
        test = check.type_test_print(b,'num','b','spline_integ')          
        if(not test):
            return test 
        test = check.type_test_print(tol,float,'tol','spline_integ')
        if(not test):
            return test 
        test = check.type_test_print(nlim,int,'nlim','spline_integ') 
        if(not test):
            return test         

        try: 
            bspline_obj = bspln(x_arr,y_arr)
            int_spline_val = integ(a,b,bspline_obj)
        except:
            int_spline_val = False 
            print("[spline_integ] Error: integral evaluation error")   

        return(int_spline_val)


