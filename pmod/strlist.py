import itertools

import tcheck as check

'''
A python module which faciliates working with list, lists of strings and strings

function list:

    array functions--------------------------- 

    array_duplicate_check(array)
    array_duplicate_return(array, inverse = False)

    array_filter_yield(array, match, reverse = False)
    array_filter(array, match, reverse = False)
    array_filter_spaces(array, filter_none = True)

    array_to_str(array, spc = ' ', print_bool = True)
    array_matrix_to_array_str(array, spc = '  ')

    array_nth_index(array, n, inverse_filter = False,list_form = True)
    array_flatten(array, safety = True, out_type = list)

    string functions--------------------------- 

    str_space_check(string, none_bool = False)
    str_to_list(string, split_val = ' ', filt = False, cut = None)

'''

### array functions


# checking and modifying arrays by content:  



def array_duplicate_check(array):
    '''
    Description: Checks for duplicates in an array-like object 
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
    Description: Checks for duplicates in an array-like object 
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


def array_filter_yield(array, match, inverse = False):
    '''
    Description: yields filtered array, match may either be an individual object or an array
    '''
    if(inverse):
        for i in array:
            if(check.test_array(match)):
                if(i not in match):
                    continue
                else:
                    yield i
            else:
                if(i != match):
                    continue
                else:
                    yield i
    else:
        for i in array:
            if(check.test_array(match)):
                if(i in match):
                    continue
                else:
                    yield i
            else:
                if(i == match):
                    continue
                else:
                    yield i

            
def array_filter(array, match, reverse = False):
    '''
    Description: returns filtered array, match may either be an individual object or an array
    '''
    return [i for i in array_filter_yield(array, match, reverse)]


def array_filter_spaces(array, filter_none = True):
    '''
    Description: Returns non-space string elements of array 
    ''' 
    def __space_filter__(array):
        for i in array:     
            if(str(i).isspace() or i == ''):
                continue
            else:
                yield i
    if(filter_none):
        return filter(None,[i for i in __space_filter__(array)])
    else:
        return [i for i in __space_filter__(array)]
            
    


# array to string         
       

def array_to_str(array, spc = ' ', print_bool = True):
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
                print("[array_to_str] TypeError: element of 'array', or 'spc', not castable to a string")
            return False        
    return out_str
             

def array_matrix_to_array_str(array, spc = '  '):
    ''' 
    Input: 
        array   : A 2-D Python array (list or tuple) object  
        spc [*] : A string object, usually spacing

    Return:
        out_str : A list of strs if success, False if failure 
    '''
    out_str = ''
    n = len(array)
    out_array = []
    try: 
        for i in range(n):
            out_array.append(array_to_str(array[i],spc))
        return out_array
    except:
        return False 


# modifying array by index 

def array_nth_index(array, n, inverse_filter = False, list_form = True):
    '''
    Description: Takes input array and outputs list corrosponding 
                 to every nth value of input array
    '''

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
    '''
    Description: Attempts to flatten (reduce dimension by one) input array.

    Inputs:

        safety   : Boolean, if True then all arrays are compatable, else array must be 2D
        out_type : Type, type of output, must be an iterable 
    '''
    try:             
        if(safety):  
            new_array = str_filter(str(array), [' ','[',']'])
            string_rep = array_to_str(new_array, spc='')
            exec('out_str = '+'['+string_rep+']')
            out_list = out_str              
        else:         
            out_list = [i for j in array for i in j]
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

def str_space_check(string, none_bool = False, print_bool = True):
    ''' 
    Description: checks if a string is all empty spaces (endline characters included)
    '''
    try:
        if(none_bool): 
            checker = string.isspace() or string == '' or string == None
        else:
            checker = string.isspace() or string == ''
        return checker
    except:
        if(print_bool):
            print("[str_space_check] Error: internal error, input may not be a string")      
        
         
      
def str_to_list(string, split_val = ' ', filtre = False, cut = None, print_bool = True):
    '''
    Description: parses input string into a list, default demarkation is by single spacing
    '''
    mod_string = str(string)
    try:
        if(filtre):
            return filter(cut,mod_string.split(split_val))
        else:
            return mod_string.split(split_val)
    except:
        print("[str_to_list] Error: input could not be split")
        return False


def str_filter(string, filtre, inverse = False, print_bool = True):
    '''
    Description: Filters 'filtre' string out of 'string' object, if 
                 'inverse' then the instances of 'filtre' are returned
    '''
    if(not isinstance(string,str)):
        try:
            string = str(string)
        except:
            if(print_bool):
                print("[str_filter] Error: 'string' input could not be cast as a string object")

    out_list = []
    if(inverse):
        for i in string:
            if(check.array_test(filtre)):
                if(i in filtre):
                    out_list.append(i)
            else:
                if(i == filtre):
                    out_list.append(i)       
    else:
        for i in string:
            if(check.array_test(filtre)):
                if(i not in filtre):
                    out_list.append(i)
            else:
                if(i != filtre):
                    out_list.append(i)
    
    out_str = array_to_str(out_list, spc = '', print_bool = print_bool)
    return out_str
       
       
def str_space_clean(string):
    '''
    removes all spaces, endline characters and newline characters from string 
    '''
    array = str_to_list(string, filtre = True)
    out_string = array_to_str(array, spc = '')
    return out_string
     
      
def str_set_spacing(string, space = ' ', print_bool = True):
    ''' 
    Description: spaces non-space substrings by a set amount
        
    (e.g.)  'Hey,        Hello    World'  - becomes -  'Hey, Hello World'   
    '''       
    try:
        array = str_to_list(string, filtre = True)
        output = array_to_str(array, spc = space, print_bool = print_bool)   
        return output  
    except:
        if(print_bool):
            print("[str_to_list] Error: input could not be split")
        return False           
              
                           


### printing functions

def print_fancy(obj, header = None, newln = True, indt = 4, err = True):

    if(newln):
        nl = '\n'
    else:
        nl = ''

    spc = indt*' '

    stylized_list = []
    
    if(check.array_test(obj)):
        print(' ')
        if(isinstance(header,str)):
            out_val = header+nl 
            stylized_list.append(out_val)  
            print(out_val)
        for i in obj:
            out_val = spc+str(i)+nl 
            stylized_list.append(out_val) 
            print(out_val)
        print(' ')
        return None
    
    elif(isinstance(obj,str)):
        print(' ')
        if(isinstance(header,str)):
            out_val = spc+header+nl 
            stylized_list.append(out_val)
            print(out_val)
        out_val = obj+nl 
        stylized_list.append(out_val)
        print(out_val)
    else:
        print("TypeError: 'obj' input object must be either an 'array' or a 'string'")


def print_border(string, style = ('-','|'), newln = True, cushion = 0, indt = 0, comment = None):
    
    n = len(string)
    
    if(newln):
        nl = '\n'
    else:
        nl = ''
    
    spr = 2*cushion+(cushion/1)*2+(cushion/2)*2+(cushion/4)*2     
#    tnb = 4*style[0]+(n+2*cushion)*style[0] 
    blnk= style[1]+(2+spr+n)*' '+style[1]  
    tnb = len(blnk)*style[0]         
    mid = style[1]+(1+spr/2)*' '+string+(1+spr/2)*' '+style[1] 

    if(isinstance(indt,int) and indt >= 0):
        blnk = indt*' '+blnk
        tnb = indt*' '+tnb 
        mid = indt*' '+mid

    if(isinstance(comment,str)):
        blnk = comment+blnk
        tnb = comment+tnb 
        mid = comment+mid
    
    stylized_list = []
    print(tnb)
    stylized_list.append(tnb+nl)
    for i in range(cushion):
        print(blnk)
        stylized_list.append(blnk+nl)
    print(mid)
    stylized_list.append(mid+nl)
    for i in range(cushion):
        print(blnk)
        stylized_list.append(blnk+nl)
    print(tnb)
    stylized_list.append(tnb+nl)

    return stylized_list       
    












