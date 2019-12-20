
import math as mt 
from scipy.interpolate import interp1d as spln    
from scipy.interpolate import splrep as bspln
from scipy.interpolate import splev as deriv
from scipy.interpolate import splint as integ

from tcheck import tcheck as check


class rund:

    def __init__(self, pyver = '27', num = None, deci = None, digi = None):
        self.num = num
        self.deci = deci 
        self.digi = digi 
        self.pyver = pyver

    def pass_num(self, num, deci = None, digi = None)
        self.num = num 
        self.deci = deci
        self.digi = digi 
                

    def round_decimal(self, num, deci, str_bool=True):
        
        # round_decimal(30.112,1,True)
        
        # x: input file string
        # d: non-zero integer
        # string: boolean, String if True, Float if false

        check.type_test_print(num,'num','num','round_decimal') 
        check.type_test_print(deci,int,'deci','round_decimal')
        check.type_test_print(str_bool,bool,'str_bool','round_decimal') 
        
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

    
    def round_decimal_sci(self, num, digi, str_bool = True):
        
        # round_decimal_sci(30.112,1,True)    
        # x: input file string
        # d: a non-negative integer signifying the number of significant digits
    
        check.type_test_print(num,'num','num','round_decimal_sci') 
        check.type_test_print(deci,int,'deci','round_decimal_sci')
        check.type_test_print(str_bool,bool,'str_bool','round_decimal_sci') 
        
        if(deci < 0):
            print("[round_decimal_sci] Error: 'digi' decimal value must be non-negative")
            return False

        num = float(num)
        if(self.pyver == '27'):        
            fm = "{:." + str(int(digi)-1) + "e}"
            rnum = fm.format(x)
        elif(self.pyver == '26'):
            fm = "{0:." + str(int(digi)-1) + "e}"
            rnum = fm.format(x)             
        else:
            print("[round_decimal_sci] Error: 'pyver' not recognized'")
            return False        
             
        if(str_bool):
            return str(rnum)
        else:
            return float(rnum)    

    
    def round_uniform(num):
        
        check.type_test_print(num,'num','num','numeric_uni_format') 

        num = float(num)
            
        pos_bool = (num > 0.0)
        neg_bool = (num < 0.0)
        nul_bool = (num == 0.0)
    
        if(pos_bool):
            if(num < 10000000):
                output = self.round_decimal(num,6)
                for i in range(6):
                    if(num > 10.0**(i+1)):
                        output = self.round_decimal(num,6-(i+1))
                        if(i == 6):
                            output = output+'.'
            if(num >= 10000000):
                output = self.round_decimal_sci(num,3)
            if(num < 0.000001):
                output = self.round_decimal_sci(num,3)
        elif(neg_bool):
            if(num > -1000000):
                output = self.round_decimal(num,5)
                for i in range(5):
                    if(num < -10.0**(i+1)):
                        output = self.round_decimal(num,5-(i+1))   
                        if(i == 5):
                            output = output+'.'
            if(num <= -1000000):
                output = self.round_decimal_sci(num,2)
            if(num > -0.000001):
                output = self.round_decimal_sci(num,2)
        else:
            output = '0.000000'
        return output




class spline:

    def __init__(self, x_vec = None, y_vec = None, spln_type=None):
        self.x_vec = x_vec
        self.y_vec = y_vec 
        self.spln_type = spln_type


    def spln_obj(self, x_arr, y_arr, type = 'spline', sort = 'cubic'):

        check.type_test_print(x_arr,'arr','x_arr','spln_obj')
        check.type_test_print(y_arr,'arr','y_arr','spln_obj')
        check.type_test_print(type,str,'type','spln_obj')   
        check.type_test_print(sort,str,'sort','spln_obj')  

        if(type = 'spline'):

            try: 
                spline = spln(x_arr,y_arr,kind=sort)
                return spline
            except: 
                spline = False 
                print("[spln_obj] Error: spline object generation failed" 
                return spline

        elif(type = 'bspline'):

            try: 
                bspline = bspln(x,y)
                return bspline
            except: 
                bspline = False 
                print("[spln_obj] Error: bspline object generation failed" 
                return bspline

        else: 
            print("[spln_obj] Error: 'type' not recognized"
            return False


    def spln_val(self, spline, xvals_arr):

        check.type_test_print(spline,spln,'spline','spln_val') 
        check.type_test_print(xvals_arr,'arr','xvals_arr','spln_val') 
        try:
            spline_vals = spline(xvals_arr)
            return(spline_vals)
        except: 
            return False 


    def spln_der(self, bspline, xvals_arr, der = 1):

        check.type_test_print(bspline,bspln,'spline','spln_der') 
        check.type_test_print(xvals_arr,'arr','xvals_arr','spln_der') 
        check.type_test_print(der,int,'der','spln_der') 
        try:    
            der_vals = deriv(xvals_arr,bspline,der)
            return(der_vals) 
        except: 
            return False 


    def spln_integ(self, bspline, a, b):

        check.type_test_print(bspline,bspln,'spline','spln_integ') 
        check.type_test_print(a,'num','a','spln_integ')
        check.type_test_print(b,'num','b','spln_integ') 
        try:    
            int_vals = integ(a,b,bspline)
            return(der_vals)
        except: 
            return False 
         

    def spline_val_scon(self, xvals_arr, x_arr, y_arr, der = 0 , type = 'cubic'):

        check.type_test_print(xvals_arr,'arr','xvals_arr','spline_val_scon')     
        check.type_test_print(der,int,'der','spline_val_scon')    
        
        if(der < 0):
            print("[spline_val_scon] Error: 'der' must be non-negative")
            return False

        if(der == 0):    
            try:
                spline = spln(x_arr,y_arr,kind=type)
                spline_vals = spline(xnew_arr)
                return(spline_vals)
            except:
                print("[spline_val_scon] Error: spline function(s) failed")
                return False
        if(der > 0):
            try:
                bspline_obj = bspln(x,y)
                der_spline_vals = deriv(xnew_arr,bspline_obj,der)
                return(der_spline_vals)
            except:
                print("[spline_val_scon] Error: bspline function(s) failed")
                return False
   
 
    def spline_integ_scon(self, x_arr, y_arr, a, b, tol = 0.000000001, nlim = 1000):
        
        check.type_test_print(x_arr,'arr','x_arr','spline_integ')
        check.type_test_print(y_arr,'arr','y_arr','spline_integ') 
           
        check.type_test_print(a,'num','a','spline_integ')
        check.type_test_print(b,'num','b','spline_integ')          

        check.type_test_print(tol,float,'tol','spline_integ')
        check.type_test_print(nlim,int,'nlim','spline_integ') 
        
        try: 
            bspline_obj = bspln(x_arr,y_arr)
            int_spline_val = integ(a,b,bspline_obj)
        except:
            int_spline_val = False 
            print("[spline_integ] Error: integral evaluation error")   

        return(int_spline_val)

