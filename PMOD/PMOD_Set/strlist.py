import itertools

import tcheck as check

'''
A python module which faciliates working with list, lists of strings and strings


'''

### array functions


# checking and modifying arrays by content:  



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


def array_filter_yield(array, match, reverse = False):
    if(reverse):
        for i in array:
            if(i != match):
                continue
            else:
                yield i
    else:
        for i in array:
            if(i == match):
                continue
            else:
                yield i

            
def array_filter(array, match, reverse = False):
    return [i for i in array_filter_yield(array, match, reverse)]


def array_filter_spaces(array, filter_none = True):
    def space_filter(array):
        for i in array:     
            if(str(i).isspace() or i == ''):
                continue
            else:
                yield i
    if(filter_none):
        return filter(None,[i for i in space_filter(array)])
    else:
        return [i for i in space_filter(array)]
            
    


# array to string         
       

def array_to_string(array, spc = ' ', print_bool = True):
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
                print("[array_to_string] TypeError: element of 'array' or 'spc' not castable to a string")
            return False        
             

def array_matrix_to_array_str(array, spc = '  '):
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


# modifying array by index 

def array_nth_index(array, n, inverse_filter = False,list_form = True):
    try:
        if(inverse_filter):
            out_object = itertools.ifilter(lambda x: array.index(x)%n, array)
        else:
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


def array_flatten(array, safety = True, out_type = list):
    try:
        if(safety):
            out_list = [item for subarray in array for item in subarray if check.array_test(item)]    
        else:
            out_list = [item for subarray in array for item in subarray]
    except:
        return False 
    if(out_type == list):
        return out_list 
    elif(out_type == tuple):
        return tuple(out_list)
    elif(out_type == set):
        return set(out_list)
    else:
        try:
            print("[array_flatten] Error: invalid 'out_type' : "+str(out_type)) 
        except:
            print("[array_flatten] Error: invalid 'out_type'")
        return False 


### string functions 

# string content

def str_space_check(string, none_bool = False):
    if(none_bool): 
        checker = string.isspace() or string == '' or string == None
    else:
        checker = string.isspace() or string == ''
    return checker

#

def str_to_list(string, split_val = ' ', filt = False, cut = None):
    try:
        if(filt):
            return filter(cut,string.split(split_val))
        else:
            return string.split(split_val)
    except:
        print("[str_to_list] Error: input could not be split")
        return False









