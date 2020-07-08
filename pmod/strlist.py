import itertools

'''
A python module which faciliates working with list, lists of strings and strings

function list:

    |---helper functions--------------------------

    __isArray__(array)
    __isNumeric__(array)

    |---array functions--------------------------- 

    array_duplicate_check(array)
    array_duplicates(array, inverse = False)

    array_filter(array, match, reverse=False)
    array_filter_spaces(array, filter_none=True)

    array_to_str(array, spc = ' ', print_bool=True)
    array_matrix_to_array_str(array, spc = '  ')

    array_nth_index(array, n, inverse_filter = False,list_form = True)
    array_flatten(array, safety = True, out_type = list)

    |---string functions--------------------------- 

    str_space_check(string, none_bool = False)
    str_to_list(string, split_val = ' ', filt = False, cut = None)

'''

### Internal Helper Functions

def __isArray__(array):
    return isinstance(array, (tuple, list))

def __isNumeric__(num):
    return isinstance(num, (int,float,long))

#######################
### array functions ###
#######################

# checking and modifying arrays by content:

def array_duplicate_check(array):
    '''
    Description: Checks for duplicates in an array-like object
                 If duplicates are found, True is returned
                 Else, False is returned
                 If input is not an array, None is returned

    Inputs:

        'array' : a list or tuple to be checked for duplicates

    '''
    if(not __isArray__(array)):
        return None
    s = []
    for i in array:
        if i in s:
            return True
        else:
            s.append(i)
    return False


def array_duplicates(array, inverse=False, count=False, index=False):
    '''
    Description: Checks for duplicates in an array-like object
                 If duplicates are found, a list of the duplicate values is returned
                 Else an empty list is returned

    Inputs:

        array : (list or tuple), The array which is to be checked for duplicates

        inverese : (bool) [False], Returns the non-duplicated values in the array

        count : (bool) [False], Returns a dictionary with each key index corrosponding
                                to each value in 'array' and the corrosponding value
                                index equal to the number of times that that key appears

        index : (bool) [False], Returns a dictionary with each key index corrosponding
                                to each value in 'array' and the corrosponding value
                                index equal to a list of integer indicies for which the
                                'array' entry appears within the array

    Returns:

        (ci, dup_list)

        ci : (tuple), a tuple containing index and/or count dictionary, else an empty tuple

        dup_list : (list), a list of duplicate objects in 'array', else an empty list

        False, if an error is detected

    |--------------------|
    |---exampli gratia---|
    |--------------------|

    array = [1,2,2,4,3,3,3]

    ci, dup_list = array_duplicates(array, count=True, index=True)
    indicies, counts = ci

    ---

    dup_list = [2,3]

    indicies = {1: [0],
                2: [1, 2],
                3: [4, 5, 6],
                4: [3]}

    counts = {1: 1,
              2: 2,
              3: 3,
              4: 1}
    '''
    if(not __isArray__(array)):
        return False

    s = []
    dupList = []
    inv = []

    countDict = {}
    indexDict = {}

    for i,entry in enumerate(array):
        if entry in s:
            if(entry not in dupList):
                dupList.append(entry)
            if(count and inverse==False):
                countDict[entry] = countDict[entry]+1
            if(index and inverse==False):
                indexDict[entry] = indexDict[entry]+[i]
        else:
            s.append(entry)
            if(count and inverse==False):
                countDict[entry] = 1
            if(index and inverse==False):
                indexDict[entry] = [i]
    if(inverse):
        for i,entry in enumerate(array):
            if(entry in s and entry not in dupList):
                inv.append(entry)
                if(count):
                    countDict[entry] = 1
                if(index):
                    indexDict[entry] = [i]
        if(count or index):
            if(count and not index):
                return (countDict, inv)
            elif(index and not count):
                return (indexDict, inv)
            else:
                return ((indexDict, countDict), inv)
        else:
            return ((), inv)
    else:
        if(count or index):
            if(count and not index):
                return (countDict, dupList)
            elif(index and not count):
                return (indexDict, dupList)
            else:
                return ((indexDict, countDict), dupList)
        else:
            return ((), dupList)


def array_filter(array, match, inverse=False):
    '''
    Description: returns input array filtered of any values found in 'match'

    Inputs:

        array : (tuple or list), an array to be filtered of 'match' entries

        match : (tuple, list or entry value), if 'match' is an array the
                entry of the arrays are filtered from 'array', else 'match'
                value is filtered from the array

        inverse : (bool) [False], if True every entry not equivalent to 'match'
                  is filtered from the array
    '''

    if(not __isArray__(array)):
        return False

    outArray = []
    if(inverse):
        for entry in array:
            if(__isArray__(match)):
                if(entry not in match):
                    continue
                else:
                    outArray.append(entry)
            else:
                if(entry != match):
                    continue
                else:
                    outArray.append(entry)
    else:
        for entry in array:
            if(__isArray__(match)):
                if(entry in match):
                    continue
                else:
                    outArray.append(entry)
            else:
                if(entry == match):
                    continue
                else:
                    outArray.append(entry)
    return outArray


def array_filter_spaces(array, none_filter=True, inverse=False):
    '''
    Description: Returns non-space string elements of 'array', in 'inverse'
                 is True, only space-string elements of 'array' are returned
    '''

    if(not __isArray__(array)):
        return False

    nonSpaceList = []
    spaceList = []

    for entry in array:
        if(str(entry).isspace() or entry == ''):
            if(inverse):
                spaceList.append(entry)
        else:
            if(not inverse):
                nonSpaceList.append(entry)
    if(none_filter):
        if(inverse):
            return filter(None, SpaceList)
        else:
            return filter(None, nonSpaceList)
    else:
        if(inverse):
            return SpaceList
        else:
            return nonSpaceList


def array_to_str(array, spc=' ', endline=False, front_spacing='', print_bool=True):
    '''
    Description: Turns array of string elements into a single string
                 each entry is space by 'spc' spacing value. If
                 'endline' is True then '\n' is added to the end of
                 the output string. If 'print_bool' is True, any
                 error's that are raised will print an error message
                 to the console. 

    Input:

        array : (list or tuple), A 1-D Python array object

        spc : (string) [' '],  A string object, usually spacing

        endline : (bool) [False], If True, a endline character is added to the output string

        print_bool : (bool) [True], If True, any errors that are raised will print an error
                      message to the console.

    Return:

        out_str : A string if success, False if failure
    '''

    if(not __isArray__(array)):
        if(print_bool):
            print("[array_to_str] TypeError: 'array' is not an array : "+str(type(array)))
        return False

    out_str = ''

    for i, entry in enumerate(array):
        if(i == 0):
            out_str = out_str+str(entry)
        else:
            out_str = out_str+str(spc)+str(entry)

    if(endline):
        out_str = out_str+"\n"
    if(front_spacing != '' and isinstance(front_spacing, str)):
        out_str = front_spacing+out_str

    return out_str


def array_matrix_to_array_str(array, spc='  ', endline=False, front_spacing='', print_bool=True, string_safety=True):
    '''
    Description: Takes a matrix (2-D array of arrays) and returns a 1-D array; 'outArray'
                 Each entry in 'outArray' is a string corrosponding to the original entry
                 in 'array' parsed through the function 'array_to_str'

    Input:
        array   : A 2-D Python array (list or tuple) object
        spc [*] : A string object, usually spacing

    Return:
        out_array : A list of strs if success, False if failure
    '''
    if(not __isArray__(array)):
        if(print_bool):
            print("[array_matrix_to_array_str] TypeError: 'array' is not an array : "+str(type(array)))
        return False
    outArray = []

    for i,entry in enumerate(array):
        if(string_safety):
            if(isinstance(array, str)):
                outArray.append(string)
            else:
                string = array_to_str(entry, spc, endline, front_spacing, print_bool)
                if(string == False):
                    if(print_bool):
                        msg = "[array_matrix_to_array_str] Warning: the "
                        print(msg+print_ordinal(i)+" entry is not an array or string: "+str(type(array)))
                    continue
                outArray.append(string)
        else:
            string = array_to_str(entry, spc, endline, front_spacing, print_bool)
            if(string == False):
                if(print_bool):
                    msg = "[array_matrix_to_array_str] Warning: the "
                    print(msg+print_ordinal(i)+" entry is not an array : "+str(type(array)))
                continue
            outArray.append(string)
    return outArray


def array_nth_index(array, n, inverse=False, print_bool=True, space='    '):
    '''
    Description: Takes an input array and outputs a list corrosponding 
                 to the value found at every nth index of input array

    Input:

        array : (list or tuple), the array for entries to be selected by index

        n : (int), the integer corrosponding to the modulus determining which
            index values are selected from 'array'

        inverese : (bool) [False], If true then the all values of 'array' are
                   returned except for those at each 'n'th value of the index.

    Return:
        out_array : A list of strs if success, False if failure
    '''
    if(not __isArray__(array)):
        if(print_bool):
            print(space+"[array_nth_index] Error: input 'array' must be an array: '"+str(type(array))+"'\n")
        return False
    array_len = len(array)

    if(not isinstance(n, int)):
        if(print_bool):
            print(space+"[array_nth_index] Error: input 'n' must be an integer: '"+str(type(n))+"'\n")
        return False
    else:
        if(n <= 1 or n>(array_len/2)):
            if(print_bool):
                print(space+"[array_nth_index] Error: input 'n' is only valid for 1 < n <= (len('array')/2): "+str(n)+"'\n")
            return False

    try:
        if(inverse):
            out_object = itertools.ifilter(lambda x: array.index(x)%n, array)
        else:
            out_object = itertools.ifilterfalse(lambda x: array.index(x)%n, array)
    except:
        if(print_bool):
            print(space+"[array_nth_index] Error: failure to filter array\n")
        return False

    out_list = [entry for entry in out_object]
    return out_list


def array_flatten(array, safety=True):
    '''
    Warning: this function uses 'exec' and is inherently insecure if input is allowed from the user.

    Description: Attempts to flatten (reduce dimension by one) input array.

    Inputs:

        safety   : Boolean, if True then all arrays are compatable, else array must be 2D
        out_type : Type, type of output, must be an iterable
    '''
    if(not __isArray__(array)):
        return False

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

    return out_list


### string functions 

# string content

def str_space_check(string, none_bool=False, print_bool=True, space='    '):
    '''
    Description: checks if a string is all empty spaces (endline characters included)
    '''
    if(not isinstance(string, (str, type(None)))):
        if(print_bool):
            print("[str_space_check] Error: input 'string', is not a string\n")
        return False
    else:
        if(none_bool and string==None):
            return True

    try:
        checker = string.isspace() or string == ''
        return checker
    except:
        if(print_bool):
            print("[str_space_check] Error: internal error\n")
        return False


def str_to_list(string, spc = ' ', filtre = False, cut = None, print_bool=True):
    '''
    Description: parses input string into a list, default demarcation is by single spacing
    '''
    if(not isinstance(string, str)):
        mod_string = str(string)
    else:
        mod_string = string

    try:
        if(filtre):
            return filter(cut, mod_string.split(spc))
        else:
            return mod_string.split(spc)
    except:
        if(print_bool):
            print("[str_to_list] Error: input could not be split")
        return False


def str_to_fill_list(string, 
                     lngspc='    ',
                     fill='NaN',
                     nval=False,
                     spc=' ',
                     numeric=False):
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


def str_filter(string, filtre, inverse=False, print_bool=True):
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
            if(__isArray__(filtre)):
                if(i in filtre):
                    out_list.append(i)
            else:
                if(i == filtre):
                    out_list.append(i)       
    else:
        for i in string:
            if(__isArray__(filtre)):
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
    if(not isinstance(string, str)):
        s4 = '    '
        try:
            print(s4+"[str_clean] Error: 'string' input is not a string: "+str(string)+"\n")
        except:
            print(s4+"[str_clean] Error: 'string' input is not a string\n")
        return False

    array = str_to_list(string.rstrip(), filtre=True)
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

    if(__isArray__(obj)):
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

    if(__isNumeric__(n)):
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









