
'''             
tcheck        
               
Description: A selection of functions for aiding with error checking 
             by searching for TypeError, each function returns either 
             a None type or Bool type. 

function list:

    numeric_test(obj)
    array_test(obj)
    flat_array_test(obj)
    type_test(var,sort) 
    type_test_print(var, sort, var_name=None, func_name='', print_bool=True)

'''

### Helper functions:
    
def numeric_test(obj):
    '''
    Description: A 'numeric' type is defined as an object which evaluates to a python number

    obj: input, any python object
    '''
    int_inst = isinstance(obj, int)
    float_inst = isinstance(obj, float)                     
    long_inst = isinstance(obj, long)                       
                                                           
    numeric_bool = int_inst or float_inst or long_inst            
    return numeric_bool                                           

                   
def array_test(obj):
    '''
    Description: An array is defined as a iterable and numerically indexed object: lists and tuples

    obj: input, any python object
    '''
    list_inst = isinstance(obj, list)
    tuple_inst = isinstance(obj, tuple)                  
    array_bool = list_inst or tuple_inst 
    return array_bool 


def flat_array_test(obj): 
    '''
    Description: Tests an array for flatness (each object within the array has a dimensionality of zero)

    obj: input, any python object    
    ''' 
    if(array_test(obj)):
        for i in obj:
            try:
                n = len(i)
                if(isinstance(i,str)):
                    continue
                else:
                    return False
            except:
                continue
        return True
    else:
        return False

         
               
def __fail_print__(success, var_name=None, correct_type="valid type", func_name='', print_bool = True):
    '''
    Dunder printing function for internal error correction and checking
    '''
    if(print_bool):
        if(isinstance(correct_type,str)):
            correct_type = correct_type 
        else:
            try:
                correct_type = str(correct_type)
            except:
                print("[__fail_print__] Error: 'correct_type' must be a string or type object")
                return False
        if(not success and var_name != None):
            if(func_name == ''): 
                print("TypeError: the variable '"+var_name+"' is not a "+correct_type)
            else:
                print("["+func_name+"]"+" TypeError: the variable '"+var_name+"' is not a "+correct_type)
            return False
        if(not success and var_name == None):
            if(func_name == ''):
                print("TypeError: input variable is not a "+correct_type)
            else:
                print("["+func_name+"]"+" TypeError: input variable is not a "+correct_type)
            return False 
        return True       
    else:
        return None   

### Main functions 

def type_test(var,sort):
    '''
    Description: This function returns a boolean, 'var' is tested for equivalence to 
                 'sort', 'sort' may a 'type' object.  

    Inputs:
    
        var  : input object 
        sort : sort is either a type, class object or module object against which 'var' is tested
                
    '''
     
    if(sort == None):
        type_bool = (var == sort)
    elif(sort == 'num'):
        type_bool = numeric_test(var)  
    elif(sort == 'arr'):
        type_bool = array_test(var)
    elif(isinstance(sort,type) or type(sort) == "<type 'classobj'>" or type(sort) == "<type 'module'>"):        
        type_bool = isinstance(var, sort)
    else:
        type_bool = False        
    return type_bool 

         
def type_test_print(var, sort, var_name=None, func_name='', print_bool=True):
    '''
    Description: This function returns a boolean, 'var' is tested for equivalence to 
                 'sort', 'sort' may a 'type', 'classobj' or 'module' object. The main 
                 difference between this function and 'type_test' is that this function 
                 is optimized for printing out error functions    

    Inputs:
    
        'var'  : python object, input object 
        'sort' : sort is either a type, class object or module object against which 'var' is tested
        'var_name' : string, The name of variable 'var', to be used when printing error messages.
        'func_name' : string,  The name of a function, to be used when printing error messages.
        'print_bool' : boolean, printing option, useful when printing to the console would interfere with threading       
                
    '''
    type_bool = type_test(var,sort)
    test = __fail_print__(type_bool, var_name, correct_type=sort, func_name=func_name, print_bool = print_bool)
    return test