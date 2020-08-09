
from scipy.interpolate import interp1d as __spln__
from scipy.interpolate import splrep as __bspln__
from scipy.interpolate import splev as __deriv__
from scipy.interpolate import splint as __integ__

from scipy.integrate import quad as __definteg__

import pmod.tcheck as check
import pmod.strlist as strl

'''
Functions useful for mathmatical operations and plotting, emphasis on parsing floating point variables
'''

#################################################################
# Error Printing Helper functions-------------------------------#
#################################################################

printer = check.imprimer()

def __err_print__(errmsg, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    printer.errPrint(errmsg, **pkwargs)

def __not_str_print__(var, varID=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.strCheck(var, **pkwargs)

def __not_arr_print__(var, varID=None, style=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.arrCheck(var, style, **pkwargs)

def __not_num_print__(var, varID=None, style=None, **pkwargs):
    if(isinstance(varID, str)):
        pkwargs["varName"] = varID
    return not printer.numCheck(var, style, **pkwargs)

def __update_funcName__(newFuncName, **pkwargs):
    pkwargs = printer.update_funcName(newFuncName, **pkwargs)
    return pkwargs


#################################################################
# Rounding functions -------------------------------------------#
#################################################################


def round_decimal(value, decimal, string=True, **pkwargs):
    '''
    round_decimal(30.112, 1, True)

        value: input file string
        decimal: non-zero integer
        string: (bool)[True] if True, returns String. Else, returns Float
    '''

    __update_funcName__("round_decimal", **pkwargs)

    try:
        value = float(value)
    except:
        __err_print__("must be castable to a float value", varID='value', heading="ValueError", **pkwargs)
        return False

    if(__not_num_print__(decimal, style='int', **pkwargs)):
        return False

    if(decimal < 0):
        __err_print__("should be an integer greater than zero", varID="decimal", **pkwargs)
        return False

    value = float(value)                
    fm = '%.' + str(int(decimal)) + 'f'
    rnum = fm % value

    if(string):
        if(decimal > 0):
            output = str(rnum)
            return output
        else:
            output = str(int(rnum))+'.'
            return output          
    else:
        if(decimal > 0):
            output = float(rnum)
            return output
        else:
            output = int(rnum)
            return output                  


def round_scientific(value, digits, pyver = '2.7', string=True, **pkwargs):
    '''
    Description:

        Takes as inputs a numeric value and the number of significant digits
        to which the the value is rounded when the value is converted to 
        scientific notation

    round_scientific(30.112, 1)

        value: input file string

        decimal: non-zero integer

        digits: a non-negative integer signifying the number of significant digits

        string: (bool)[True] if True, returns String. Else, returns Float
    '''

    # round_scientific(30.112, 1, True)
    # value: input file string

    __update_funcName__("round_scientific", **pkwargs)

    if(__not_num_print__(value, varID='number', heading="warning", **pkwargs)):
        try:
            value = float(value)
        except:
            return False

    if(__not_num_print__(value, varID='digits', style='int', **pkwargs)):
        return False
    else:
        if(digits <= 0):
            __err_print__("should be an integer greater than zero", varID="digits", **pkwargs)

    if(pyver == '2.7' or pyver == 2.7):
        fm = "{:." + str(int(digits)-1) + "e}"
        rnum = fm.format(value)
    elif(pyver == '2.6' or pyver == 2.6):
        fm = "{0:." + str(int(digits)-1) + "e}"
        rnum = fm.format(value)
    else:
        __err_print__("supported vaules are either '2.7' or '2.6'; '"+str(pyver)+"' not recognized", varID="pyver", **pkwargs)
        return False

    if(string):
        return str(rnum)
    else:
        return float(rnum)


def round_uniform(value, pyver = '2.7', **pkwargs):

    __update_funcName__("round_uniform", **pkwargs)

    if(isinstance(value, str)):
        try:
            value = float(value)
        except:
            __err_print__("could not be coerced to a string", varID="value", **pkwargs)
            return False
    elif(__not_num_print__(value, varID='number', heading="error", **pkwargs)):
        return False
    else:
        pass

    pos_bool = (value > 0.0)
    neg_bool = (value < 0.0)
    nul_bool = (value == 0.0)

    if(pos_bool):
        if(value < 10000000):
            output = round_decimal(value, 6, **pkwargs)
            for i in range(6):
                if(value > 10.0**(i+1)):
                    output = round_decimal(value, 6-(i+1), **pkwargs)
                    if(i == 6):
                        output = output+'.'
            if(value < 0.000001):
                output = round_scientific(value, 3, pyver, **pkwargs)
        else:
            output = round_scientific(value, 3, pyver, **pkwargs)
    elif(neg_bool):
        if(value > -1000000):
            output = round_decimal(value, 5, **pkwargs)
            for i in range(5):
                if(value < -10.0**(i+1)):
                    output = round_decimal(value, 5-(i+1), **pkwargs)   
                    if(i == 5):
                        output = output+'.'
            if(value > -0.000001):
                output = round_scientific(value, 2, pyver, **pkwargs)
        else:
            output = round_scientific(value, 2, pyver, **pkwargs)
    else:
        output = '0.000000'
    return output


def round_format(num, dec, **pkwargs):     
    ''' 

    '''

    __update_funcName__("round_format", **pkwargs)

    if(not isinstance(dec,int)):
        return False 
    else:
        if(dec < 0):
            return False 
        else:
            pass

    if(check.numeric_test(num)):
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
                    __err_print__("could not be coerced into a numeric type", varID="num", **pkwargs)
                    return False
        except:
            __err_print__("must be castable as a numeric type", varID="num", **pkwargs)
            return False

    f = "{0:."+str(dec)+"f}"

    out_String = f.format(num) 
    return out_String    


def space_format(num, spc, adjust = 'left', **pkwargs):

    __update_funcName__("round_format", **pkwargs)

    def __extra_spaces__(string, extra_Spaces, adjust):
        out_Str = ''
        adjust = adjust.lower()
        if(adjust == 'left'):
            out_Str = extra_Spaces*' '+string
            return out_Str
        if(adjust == 'right'):
            out_Str = string+extra_Spaces*' '
            return out_Str
        if(adjust == 'split'):
            extra_Spaces_Right = extra_Spaces/2
            extra_Spaces_Left = extra_Spaces - extra_Spaces_Right
            out_Str = extra_Spaces_Left*' '+string+extra_Spaces_Right*' '
            return out_Str
        return False

    __update_funcName__("space_format", **pkwargs)

    sci_notation = False
    decimal = False
    negative = False

    output_String = ''
    required_String = ''

    if(not isinstance(num, str)):
        try:
            num = str(num)
        except:
            __err_print__("should be a string, or castable to a string", varID="num")
            return False

    num = num.lower()

    n = len(num)

    if('e' in num or 'd' in num):
        sci_notation = True
    if('.' in num):
        decimal = True
    if('-' in num):
        negative = True

    if(spc > n):
        output_String = __extra_spaces__(num, (spc-len(num)), adjust)
        return output_String
    elif(n > spc):
        numlist = [j for i,j in enumerate(num) if i < spc]
        output_String = strl.array_to_str(numlist, spc='')

        if(sci_notation and ('e' not in output_String or 'd' not in output_String)):
            __err_print__("lost scientific notation markers when parsed thorugh spacer", varID="num", **pkwargs)
            return False
        if(decimal and '.' not in output_String):
            __err_print__("lost decimal place when parsed thorugh spacer", varID="num", **pkwargs)
            return False
        if(negative and '-' not in output_String):
            __err_print__("lost negative sign when parsed thorugh spacer", varID="num", **pkwargs)
            return False

        return output_String
    else:
        return num


def sci_space_format(num, digi, spacing=3, adjust='left', pyver='2.6', **pkwargs):

    __update_funcName__("sci_space_format", **pkwargs)

    def to_float(num, **pkwargs):

        if(not isinstance(num, (float,int))):
            try:
                num = float(num)
                return num
            except:
                __err_print__("could not be coerced to numeric", varID="num", **pkwargs)
                return None
        else:
            return num

    space='    '
    if(not isinstance(digi, int)):
        print(space+"[sci_space_format] Error: input 'digi' must be an integer, not a "+str(type(digit)))
    else:
        if(digi < 1):
            print(space+"[sci_space_format] Warning: the lowest number of digits allowed is 1")
            digi = 1

    value_array = []

    if(isinstance(num,(list,tuple))):
        for i,entry in enumerate(num):
            value = to_float(entry)
            if(value == None):
                print(space+"[sci_space_format] Error: 'num' entry, "+str(i)+", cannot be converted to numeric")
                continue
            else:
                value_array.append(value)
    elif(isinstance(num,str)):
        value = to_float(num)
        if(value == None):
            print(space+"[sci_space_format] Error: 'num' entry, "+str(num)+", cannot be converted to numeric")
            return False
        else:
            value_array.append(value)
    elif(isinstance(num,(float,int))):
        value_array.append(num)
    else:
        print(space+"[sci_space_format] Error: 'num', "+str(num)+", not a recognized type")

    if(len(value_array) == 0):
        print(space+"[sci_space_format] Error: no values found after parsing values into array")
        return False

    for i,entry in enumerate(value_array):
#        try:
        if(abs(value_array[i]) < 10e100):
            spacing_value = digi+5+spacing
        else:
            spacing_value = digi+6+spacing
        value_array[i] = round_scientific(entry, digi, pyver=pyver)
        if(value_array[i] == False):
            print(space+"[sci_space_format] Error: could not parse, "+str(value_array[i]))
        value_array[i] = space_format(value_array[i], spacing_value, adjust=adjust)
#        except:
#            print(space+"[sci_space_format] Error: terminal error, could not parse value number "+str(i))
#            return False
    
    return value_array


def span_vec(xvec, nspan, **pkwargs):
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

    test = check.array_test(xvec)
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
     
    test = check.numeric_test(xl) and check.numeric_test(xu)
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

    def pass_newx_vec(self, xarray, der=None):
        self.xarray = xarray       
        self.der    = der

    def pass_int_lim(self, a, b):
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

        test = check.type_test_print(spline,__spln__,'spline','spln_val') 
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

        test = check.type_test_print(bspline,__bspln__,'spline','spln_der') 
        if(not test):
            return test 
        test = check.type_test_print(xvals_arr,'arr','xvals_arr','spln_der') 
        if(not test):
            return test 
        test = check.type_test_print(der,int,'der','spln_der') 
        if(not test):
            return test 

        try:    
            der_vals = __deriv__(xvals_arr, bspline, der)
            return(der_vals) 
        except: 
            return False 


    def spln_integ(self, bspline, a, b):

        test = check.type_test_print(bspline,__bspln__,'spline','spln_integ') 
        if(not test):
            return test 
        test = check.type_test_print(a,'num','a','spln_integ')
        if(not test):
            return test 
        test = check.type_test_print(b,'num','b','spln_integ') 
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
                if(not check.numeric_test(a) or not check.numeric_test(b,'')):
                    print("[get_integ] Error: check that the limits of integration are numeric types")
                    return False    
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
   
 
    def spline_integ_scos(self, x_arr, y_arr, a, b, tol=0.000001, nlim=1000):
        
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
            bspline_obj = __bspln__(x_arr, y_arr)
            int_spline_val = __integ__(a, b, bspline_obj)
        except:
            int_spline_val = False 
            print("[spline_integ] Error: integral evaluation error")   

        return(int_spline_val)

    # Utility Functions 




