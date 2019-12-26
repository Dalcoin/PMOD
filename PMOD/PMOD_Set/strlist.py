import itertools
import tcheck as check

'''
A python module which deals with list, lists of strings and strings
'''

# array functions 

def array_duplicate_check(array):
    '''
    Checks for duplicates in an array-like object 

        If duplicates are found, True is returned 
        Else False is returned
    '''    
    test = check.type_test_print(array, 'arr', var_name='array', func_name='array_duplicate_check')  
    if(not test):
        return False
    s = set()
    for i in array:
        if i in s:
            return True
        else:
            s.add(i)         
    return False      
     

def array_duplicate_return(array, inverse = False): 
    '''
    Checks for duplicates in an array-like object 

        If duplicates are found, a list of the duplicate values is returned 
        Else an empty list is returned
    '''   
    test = check.type_test_print(array, 'arr', var_name='array', func_name='array_duplicate_check')  
    if(not test):
        return False  
    s = set()                        
    list_dup = []                   
    for i in array:                      
        if i in s:                 
            if(i not in list_dup):
                list_dup.append(i)
        else:                    
            s.add(i)                
    if(inverse):
        output = s-set(list_dup)
        return list(output)        
    else:           
        return list_dup          
       

def array_to_string(array, spc = '  ', print_bool = True):
    ''' 
    Input: 
        array   : A 1-D Python array (list or tuple) object  
        spc [*] : A string object, usually spacing

    Return:
        out_str : A string if success, A False if failure 
    '''
    out_str = ''                          
    for i in array:                        
        try:                            
            out_str = out_str+str(spc)+str(i)
        except:
            if(print_bool):
                print("[array_to_string] TypeError: element of 'array' or 'spc' not castable to a string"
            return False        
             

def array_2d_to_string(array, spc = '  ')
    ''' 
    Input: 
        array   : A 2-D Python array (list or tuple) object  
        spc [*] : A string object, usually spacing

    Return:
        out_str : A string if success, A False if failure 
    '''
    out_str = ''
    n = len(array)
    out_array = []
    try: 
        for i in range(n):
            out_array.append(array_to_string(array[i],spc))
        return out_array
    except:
        return False 


def array_select(array, n, list_form = False):
    try:
        out_object = itertools.ifilterfalse(lambda x: array.index(x)%n, array)
        if(list_form):
            out_list = []
            for i in out_object:
                out_list.append(i)
            return out_list
        else:
            return out_object
    except:
        return False


# string functions 

def str_to_list(string, split_val = ' ', cut = None):
    try:
        return filter(cut,string.split(split_val))
    except:
        return False






