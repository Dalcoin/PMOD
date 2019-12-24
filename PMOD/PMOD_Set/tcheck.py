
'''
tcheck

Description: A selection of functions for aiding with error checking 
             by searching for TypeError, each function returns either 
             a None type or Bool type. 
'''

### Helper functions:
    
def numeric_test(var):
    '''
    A numeric is defined as a value which evaluates to a python number
    '''
    int_inst = isinstance(var, int)
    float_inst = isinstance(var, float)
    long_inst = isinstance(var, long)

    numeric_bool = int_inst or float_inst or long_inst
    return numeric_bool

                   
def array_test(var):
    '''
    An array is defined as a iterable object which contains discreetly ordered values: lists and tuples
    '''
    list_inst = isinstance(var, list)
    tuple_inst = isinstance(var, tuple)                  
    array_bool = list_inst or tuple_inst
    return array_bool 
         
               
def __fail_print__(success, var_name=None, correct_type="valid type", func_name='', print_bool = True):
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
    Inputs:
    
        var  : input object 
        sort : sort is either a type or object against which 'var' is tested

    Description: 
            
        This function returns a boolean, 'var' is tested for equivalence to 
        'sort', 'sort' may a 'type' object.                  
    '''
     
    if(sort == None):
        type_bool = (var == sort)
    elif(isinstance(sort,type) or isinstance(sort,object)):        
        type_bool = isinstance(var, sort)
    elif(sort == 'num'):
        type_bool = numeric_test(var)  
    elif(sort == 'arr'):
        type_bool = array_test(var)
    else:
        type_bool = False        
    return type_bool 

         
def type_test_print(var, sort, var_name=None, func_name='', print_bool=True):
    type_bool = type_test(var,sort)
    test = __fail_print__(type_bool, var_name, correct_type=sort, func_name=func_name, print_bool = print_bool)
    return test