
from scipy.interpolate import interp1d as __spln__    
from scipy.interpolate import splrep as __bspln__
from scipy.interpolate import splev as __deriv__
from scipy.interpolate import splint as __integ__

from scipy.integrate import quad as __definteg__

import tcheck as __check__

'''
Functions useful for mathmatical operations and plotting, fills a void found in math and numpy
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


def round_scientific(num, digi, pyver = '2.7', str_bool = True):
    
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
    if(pyver == '2.7'):        
        fm = "{:." + str(int(digi)-1) + "e}"
        rnum = fm.format(num)
    elif(pyver == '2.6'):
        fm = "{0:." + str(int(digi)-1) + "e}"
        rnum = fm.format(num)             
    else:
        print("[round_scientific] Error: 'pyver' not recognized'")
        return False        
         
    if(str_bool):
        return str(rnum)
    else:
        return float(rnum)    


def round_uniform(num, pyver = '2.7'):
    
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
     
      
def round_format(num, dec, pyver = '2.7'):     
    ''' 
         
    '''  

    if(not isinstance(dec,int)):
        return False 
    else:
        if(dec < 0):
            return False 
        else:
            pass
           
    if(__check__.numeric_test(num)):
        pass
    else:
        try:
            if(isinstance(num,str)):
                try:
                    if('.' in num):                    
                        num = float(num)
                    else:
                        num = int(num)
                except:
                    return False
        except:
            return False

    f = "0:."+str(dec)+"f"

    out_String = f.format(num) 
    return out_String    


def space_format(num, spc, adjust = 'left'):

    def __extra_spaces__(string, extra_Spaces, adjust):
        out_Str = ''
        adj = adjust.lower()
        print(adj)
        if(adj == 'left'): 
            print(extra_Spaces)
            out_Str = extra_Spaces*' '+string
            return out_Str
        if(adj == 'right'):
            out_Str = string+extra_Spaces*' ' 
            return out_Str
        if(adj == 'split'):
            extra_Spaces_Right = extra_Spaces/2    
            extra_Spaces_Left = extra_Spaces - extra_Spaces_Right
            out_Str = extra_Spaces_Left*' '+string+extra_Spaces_Right*' '
            return out_Str
        return False 

    sci_Notation = False  
    output_String = ''
    required_String = ''
     
    if(not isinstance(num,str)):
        print("[space_format] Error: 'num' must be a string")
        return False 

    n = len(num)

    if('e' in num or 'd' in num or 'D' in num or 'E' in num):
        sci_Notation = True 
      

    if(len(num) > spc and sci_Notation == False):
        num_List = [i for i in num]
        if('.' in num):
            i = 0
            while(i <= spc-1 and i<n-1):   
                output_String+=num_List[i]
                i+=1              
            if('.' in output_String):                
                output_String = __extra_spaces__(output_String, (spc-len(output_String)), adjust)
                return output_String 
            else:
                print("[space_format] Error: the input 'num' has more characters than spaces")
                return False 
    if(n <= spc and sci_Notation):
        output_String = __extra_spaces__(num, (spc-n), adjust) 
        return output_String
     
     
    
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

    if(xl < 0):
        xl = xl-0.0000000001
    elif(xl > 0):
        xl = xl+0.0000000001
    else:
        pass

    if(xu < 0):
        xu = xu+0.0000000001
    elif(xl > 0):
        xu = xu-0.0000000001
    else:
        pass
     
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

        Warning: Interpolation using fuctions called upon splines generated with 
                 scipy must be within the range of the function, scipy functions 
                 in general do no interpolate beyond the range of the input data
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




