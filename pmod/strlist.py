import itertools

import tcheck as __check__

'''
A python module which faciliates working with list, lists of strings and strings

function list:

    |---array functions--------------------------- 

    array_duplicate_check(array)
    array_duplicate_return(array, inverse = False)

    array_filter_yield(array, match, reverse = False)
    array_filter(array, match, reverse = False)
    array_filter_spaces(array, filter_none = True)

    array_to_str(array, spc = ' ', print_bool = True)
    array_matrix_to_array_str(array, spc = '  ')

    array_nth_index(array, n, inverse_filter = False,list_form = True)
    array_flatten(array, safety = True, out_type = list)

    |---string functions--------------------------- 

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
    test = __check__.type_test_print(array, 'arr', var_name='array', func_name='array_duplicate_check')  
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
    test = __check__.type_test_print(array, 'arr', var_name='array', func_name='array_duplicate_check')  
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
            if(__check__.array_test(match)):
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
            if(__check__.array_test(match)):
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
       

def array_to_str(array, spc = ' ', endline = False, print_bool = True):
    ''' 
    Input: 
        array   : A 1-D Python array (list or tuple) object  
        spc [*] : A string object, usually spacing

    Return:
        out_str : A string if success, A False if failure 
    '''
    out_str = ''                          
    for i,entry in enumerate(array):                        
        try:
            if(i == 0):
                out_str = out_str+str(entry)
            else: 
                out_str = out_str+str(spc)+str(entry)
        except:
            if(print_bool):
                print("[array_to_str] TypeError: the "+print_ordinal(i)+" element of 'array' is not castable to a string")
            return False
    if(endline):
        out_str = out_str+"\n"     
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

    if(isinstance(out_type,str)):
        out_type = out_type.lower()

    if(out_type == list or out_type == 'list'):
        return out_list 
    elif(out_type == tuple or out_type == 'tuple'):
        return tuple(out_list)
    elif(out_type == set or out_type == 'set'):
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
        
      
def str_to_list(string, spc = ' ', filtre = False, cut = None):
    '''
    Description: parses input string into a list, default demarkation is by single spacing
    '''
    mod_string = str(string)
    try:
        if(filtre):
            return filter(cut,mod_string.split(spc))
        else:
            return mod_string.split(spc)
    except:
        print("[str_to_list] Error: input could not be split")
        return False


def str_to_fill_list(string, lngspc = '    ', fill = 'NaN', nval = False, spc = ' ', numeric = False):
    '''
    Purpose : To turn python string, 'string', into a list of numeric characters, with support 
              for blank entries, input options allow for compatability with multiple 
              formatting situations and scenarios  

    Inputs: 

        string : a python 'str' object 

        lngspc : a python 'str' object, intended to be the number of blank spaces denoting a blank entry
                 default : '    ', 4 blank spaces

        fill   : a python 'str' object, intended to be the filler value for blank entries 
                 default : 'NaN', Not a Number string 
         
        nval   : either boolean False, or an integer greater than zero, intended to be 
                 the number of numeric and blank entries in 'string', also the length of the 
                 array into which the function will attempt to coerce the string
                 default : False, boolean False 

        spc    : a python string object, intended to be the value for which the seperated entries within  
                 'string' are determined, possibly a delimiter character, note that non-entry empty spaces 
                 are deleted upon splitting 'string'
                 default : ' ', a single space character 

        numeric: a python 'bool' or python 'str' object, If True then non-filled spaces are mapped to floats 
                 If 'numeric' is a string, it must corrospond to the type to which non-filled entries are 
                 coerced into, valid options are 'str', 'int' and 'float'
                 default : False 
    '''

    def __cut__(arr, n, fill):

        cut = True 
        while(cut):
            if(arr[-1] == fill and len(arr) > n):
                del arr[-1]
            else:
                cut = False 
        if(len(arr)>n):
            cut = True 
            while(cut):
                if(arr[0] == fill and len(arr) > n):
                    del arr[0]
                else:
                    cut = False                 
        if(len(arr) == n):
            return arr 
        else:
            print("Warning, output array could not be coerced into 'nval' number of entries")
            return arr
 
    # Function start
    spc1 = ' ' 

    if(not isinstance(string,str)):
        print("[str_to_spc_fill_array] Error: input 'string' is not a python 'str' type")
        return False

    # Where all the machinery is
    newline = string.replace(lngspc,spc1+fill+spc1)  
    newarr = filter(None,newline.split(spc))         
    flatarr = array_flatten(newarr)

    if(not isinstance(flatarr,list)):
        print("[str_to_spc_fill_array] Error: error occured when flattening output array")
        return flatarr

    if(isinstance(nval,int)):
        if(nval > 0 and len(flatarr) > nval):
            flatarr = __cut__(flatarr,nval,fill) 

    # conditions bound by the numeric formatter
    if(numeric):
        try:
            flatarr = map(lambda x: float(x) if x != fill else x, flatarr)
        except:
            print("Warning: Could not coerce output array into a numeric array")
    elif(isinstance(numeric,str)):
        if(numeric.lower() == 'float'):
            try:
                flatarr = map(lambda x: float(x), flatarr)
            except:
                print("Warning: Could not coerce output array into a numeric array")
        elif(numeric.lower() == 'int'):
            try:
                flatarr = map(lambda x: int(x), flatarr)
            except:
                print("Warning: Could not coerce output array into a numeric array")

    return flatarr


def str_filter(string, filtre, inverse = False, print_bool = True):
    '''
    Description: Filters 'filtre' string out of 'string' string, if 
                 'inverse' then the instances of 'filtre' are returned
                 else the entries not equivalent to 'filtre' are returned
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
            if(__check__.array_test(filtre)):
                if(i in filtre):
                    out_list.append(i)
            else:
                if(i == filtre):
                    out_list.append(i)       
    else:
        for i in string:
            if(__check__.array_test(filtre)):
                if(i not in filtre):
                    out_list.append(i)
            else:
                if(i != filtre):
                    out_list.append(i)
    
    out_str = array_to_str(out_list, spc = '', print_bool = print_bool)
    return out_str
       
       
def str_clean(string):
    '''
    Description : Removes all spaces, endline characters and newline characters from string 
    '''
    array = str_to_list(string.rstrip(), filtre = True)
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
              
                           


### Formatting and Printing Functions

def format_fancy(obj, header = None, newln = True, indt = 4, err = True, list_return = False):

    if(newln):
        nl = '\n'
    else:
        nl = ''

    spc = indt*' '

    stylized_list = []
    
    if(__check__.array_test(obj)):
        if(list_return):
            stylized_list.append(' \n')       
        else:
            print(' ')
        if(isinstance(header,str)):
            out_val = header+nl 
            if(list_return):
                stylized_list.append(out_val)  
            else:        
                print(out_val)
        for i in obj:
            out_val = spc+str(i)+nl 
            if(list_return):
                stylized_list.append(out_val)
            else:  
                print(out_val)
        if(list_return):
            stylized_list.append(' \n')
            return stylized_list
        else:
            print(' ')
            return None
    
    elif(isinstance(obj,str)):
        if(list_return):
            stylized_list.append(' \n')
        else:
            print(' ')
        if(isinstance(header,str)):
            out_val = spc+header+nl 
            if(list_return):
                stylized_list.append(out_val)
            else:
                print(out_val)
        out_val = obj+nl 
        if(list_return):
            stylized_list.append(out_val)
            return stylized_list
        else:
            print(out_val)
            return None
             
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
    

def print_ordinal(n):
    chg = ['1','2','3']
    dictn = {'1':'st','2':'nd','3':'rd'}
    
    if(__check__.numeric_test(n)):
        if(not isinstance(n,int)):
            n = int(n)
    elif(isinstance(n,str)):
        try:
            n = int(float(n))
        except:
            print("[print_ordinal] Error: input '"+n+"' could not be cast to an integer")
            return False
    else:
        print("[print_ordinal] Error: input 'n' could not be cast to an integer")
        return False        

    if(str(n) in chg):
        return str(n)+dictn[str(n)]
    else:
        return str(n)+'th'    
    








