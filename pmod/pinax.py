import re 

import strlist as __strl__ 
import tcheck as __check__ 

global re_space
 

re_space = re.compile("^\s+$")


#######################
#  General Functions  #
#######################


def __func_eprint__(msg):
    if(True):
        print(msg)
    return False

####################                         #################### 
#  line functions  ###########################  line functions  #
####################                         ####################

###################
#  NAN functions  #
###################


def __bool_tester__(obj, array_of_arrays):
    bul = False 
    for i in array_of_arrays:
        bul = bul or (obj in i)
    return bul  

def __nan_func__(check):
    
    nan_list = ['nan','NaN','NAN','-nan','-NaN','-NAN']
    inf_list = ['inf','Inf','INF','-inf','-Inf','-INF']
    null_list = ['null', 'Null', 'NULL', '-null', '-Null', '-NULL']

    truth = ('nan','inf','null')

    nil = (nan_list,inf_list,null_list)

    truth_dict = dict(zip(truth,check))
    match_dict = dict(zip(truth,nil))

    check_type = []
    
    for i in truth:
        if(truth_dict[i]):
            check_type.append(match_dict[i]) 

    return check_type

def nan_check(string, nan = True, inf = True, null = True):

    if(not isinstance(string,str)):
        try:
            string = str(string)
        except:
            print("[nan_check] TypeError: 'string' is not castable to a python 'str'")
            return False  

    check = (nan,inf,null) 
    check_type = __nan_func__(check)

    if(__bool_tester__(string,check_type)):
        return True 
    else:
        return False
     
def line_nan_check(array, nan = True, inf = True, null = True):

    if(not __check__.array_test(array)):
        print("[line_nan_check] TypeError: 'array' is not a python array")
        return False  

    check = (nan,inf,null) 
    check_type = __nan_func__(check)
            
    index_list = []
    for i in range(len(array)):
        if(__bool_tester__(array[i],check_type)):
            index_list.append(i)
        else:
            pass

    if(len(index_list) > 0):
        return index_list
    else:
        return False
          
            
###################                           ################### 
# table functions ############################# table functions #
###################                           ################### 

# Table (pinax) functions 
# These functions are the main function to be used on matrix arrays.

# Format:
#
# The format for tables takes the following basic form: [[],[]]
# 
# Functions: 
# 
# table_trans  ([[1,2,3],[4,5,6]])  =>  [[1,4],[2,5],[3,6]]  


def ismatrix(n, numeric = False):

    p1 = 'Below is invalid content found in the '
    p2 = " entry of 'n'" 

    if(not __check__.array_test(n)):
        return __func_eprint__("[ismatrix] Error: input 'n' is not a python array")
      
    index_err = []
    err = False
    length_err = False
    lang = 0

    for i in range(len(n)):
        if(not __check__.array_test(n[i])):
            print("[ismatrix] Error: the "+__strl__.print_ordinal(i+1)+" entry in 'n' is not a python array")
            err = True
        else:      
            if(i == 0):
                lang = len(n[i])
            if(numeric):
                err_arr = [j for j in n[i] if not __check__.numeric_test(j)]
            else:
                err_arr = [j for j in n[i] if not __check__.numeric_test(j) and not isinstance(j,str)]
            if(len(err_arr)>0):
                err = True
                __strl__.format_fancy(err_arr,header=p1+__strl__.print_ordinal(i+1)+p2)            
            if(len(n[i]) != lang):
                err = True
                length_err = True
    if(err):
        if(length_err):
            print("[ismatrix] Error: lengths of the enteries of 'n' are not all equal")
        return False 
    else:
        return True


def coerce_to_matrix(n, fill = 'NULL'):
     
    if(not __check__.array_test(n)):
        text = "[coerce_to_matrix] Error: input 'n' is not a python array; could not coerce to matrix"
        return __func_eprint__(text)             
        
    newn = list(n)
     
    maxl = 0
    for i in range(len(newn)):
        if(not __check__.array_test(newn[i])):
            text = "[coerce_to_matrix] Error: the "+__strl__.print_ordinal(i+1)+" entry in 'n' is not a python array"
            return __func_eprint__(text)        
        if(len(newn[i])>maxl):
            maxl = len(newn[i])
         
    for i in range(len(newn)):
        if(len(newn[i]) < maxl):
            while(len(newn[i]) < maxl):
                newn[i].append(fill)
    return newn
                 
                 
                

def table_trans(n, test_table=True, coerce=False, numeric=False, fill = 'NULL', cleanup = False):

    matrix_value = True
    if(test_table):
        matrix_value = ismatrix(n, numeric = numeric)   
    
    if(coerce and matrix_value == False):
        try:
            n = coerce_to_matrix(n, fill = fill)
            if(n == False):
                return __func_eprint__("[table_trans] Error: attempt to coerce 'n' to a matrix failed")
            contrive = True
        except:
            return __func_eprint__("[table_trans] Error: error occured while attempting to coerce 'n' into a matrix")
            return False
    elif(matrix_value == False):
        print("[table_trans] Error: 'n' did not pass the matrix test")
        return False
    else:
        pass

    nrow = len(n[0])
    new_matrix, new_row = [],[]
    
    try:           
        for k in range(nrow):
            for i in n:
                new_row.append(i[k])
            new_matrix.append(new_row)
            new_row=[]
    except: 
        err = __func_eprint__("[table_trans] Error: input could not be cast into a translated matrix")
        return err           

    if(cleanup):
        pass

    return new_matrix


def table_str_to_numeric(line_list   , 
                         header=False, 
                         entete=False , 
                         columns=True,
                         nanopt=True,
                         nantup=(True,True,True),
                         sep=' '     , 
                         genre=float , 
                         debug=True   ):
    '''

    Input Variables:

        line_list : A python array (list or tuple) of strings which form a numeric table (header option allowed)
        header    : If True, treats the first line in the input array as a header and not with the data
        entete    : If header, attempts to return the header with the output numeric table
        columns   : If True, attempts to return each columns of data, rather than input rows found in 'line_list'
        nanopt    : If True, 'NaN' values do not return error values 
        nantup    : A tuple in the form (nan,inf,null), each value is true if it is allowed
        sep       : string, seperator for numeric values in the input table (',' for CSV, space ' ' is default)
        genre     : A python object function: attempts to coerce object type to 'genre', float is default (str, int)
        debug     : If True, checks performs dummy-check on input data, returns printing of point or location of failure

    Purpose:
    
        Takes a list of strings and attempts to convert into a table of numeric values 
        Useful if working with formatted data tables
    '''

    nan,inf,null = nantup
    

    if(debug):    
        fail_test = not __check__.array_test(line_list) # True if failed array test
        if(fail_test):
            print("[table_str_to_numeric] TypeError: input 'line_list' is not a python array")
            return False
	    
        for i in range(len(line_list)):   # checking if each object in 'line_list' is a string
            fail_test = not isinstance(line_list[i],str)  # True if failed string test
            if(fail_test):
                print("[table_str_to_numeric] TypeError: non-string object at line "+str(i+1)+"of 'line_list'")        
                return False

    new_line_list = __strl__.array_filter_spaces(list(line_list))
    n = len(new_line_list)

    if(header):
        head = new_line_list[0]
        new_line_list = new_line_list[1:-1]
        n = len(new_line_list)
        try:
            head = __strl__.str_to_list(head, spc = sep, filtre = True)
            nhead = len(head)
        except:
            print("[table_str_to_numeric] Error: header could not be parsed]")
            return False
    
    nanopt_test = False
    for i in range(n):
        new_line_list[i] = __strl__.str_to_list(new_line_list[i], spc = sep, filtre = True)
        for j in range(len(new_line_list[i])):
            try:
                if(nanopt):
                    nanopt_test = nan_check(new_line_list[i][j],nan,inf,null) 
                if((genre == int or genre == long) and nanopt_test == False):
                    new_line_list[i][j] = genre(float(new_line_list[i][j]))
                if((genre == float or genre == str) and nanopt_test == False):
                    new_line_list[i][j] = genre(new_line_list[i][j])
            except:
                print("[table_str_to_numeric] Error: failed attempting to parsing table as numeric array")
                return False

    if(header and entete):
        try:
            new_line_list.insert(0,head)
        except:
            print("[table_str_to_numeric] Warning: error occured when adding header, returning table without it")
            pass
  
    if(columns):
        output = table_trans(new_line_list)  
        if(output == False):
            print("[table_str_to_numeric] Warning: could not translate table, returning as is")
            return new_line_list
        else:
            return output 
    else:
        return new_line_list


def table_str_to_fill_numeric(line_list     , 
                              space = '    ',
                              fill  = 'NULL',
                              nval  = False ,
                              header=False  , 
                              entete=True   , 
                              columns=True  ,
                              nanopt=True  , 
                              nantup=(True,True,True),
                              spc=' '       , 
                              genre=float   , 
                              debug=True   ):

    '''

    Input Variables:

        line_list : A array (list or tuple) of strings which form a numeric table (header option allowed)

        space     : A string of spaces, corrosponds to the number of spaces required for an empty entry

        fill      : A string, corrosponds to the value which will be added in the place of an empty entry 

        nval      : An integer, corrosponds to the number of values in a row, to which the table will be coerced
                    If False, the table is read according to parsed spaces

        header    : If True, treats the first line in the input array as a header and not with the data

        entete    : If header is True, attempts to return the header with the output numeric table

        columns   : If True, attempts to return lists of each columns of data, rather than each rows as found in 'line_list'

        nanopt    : If True, NaN style strings values do not return error values as specified in nantup 

        nantup    : A tuple in the form (nan,inf,null), each value is true if it is allowed

        sep       : A string, seperator for numeric values in the input table (',' for CSV, space ' ' is default)

        genre     : A python object function: attempts to coerce object type to 'genre', float is default 

        debug     : If True, checks performs dummy-check on input data, returns printing of point or location of failure


    Purpose:
    
        Takes a list of strings and attempts to convert into a table of numeric values 
        Useful if working with formatted data tables

    '''

    nan,inf,null = nantup
    null = True

    if(debug):    
        fail_test = not __check__.array_test(line_list) # True if failed array test
        if(fail_test):
            print("[table_str_to_numeric] TypeError: input 'line_list' is not a python array")
            return False
	    
        for i in range(len(line_list)):   # checking if each object in 'line_list' is a string
            fail_test = not isinstance(line_list[i],str)  # True if failed string test
            if(fail_test):
                print("[table_str_to_numeric] TypeError: non-string object at line "+str(i+1)+"of 'line_list'")        
                return False    

    if(header):
        head = line_list[0]
        op_list = line_list[1:-1]
        n = len(op_list)
        try:
            head = __strl__.str_to_list(head, spc = spc, filtre = True)
            nhead = len(head)
        except:
            print("[table_str_to_fill_numeric] Warning: header could not be parsed")
            header = False
    else:
        op_list = list(line_list)
    
    # Parsing list of lines 
    for i in range(len(op_list)):
        string = op_list[i]        
        temp = __strl__.str_to_fill_list(string, lngspc = space, fill = fill, nval = nval, spc = spc, numeric = False)
          
        # Parsing numeric values found in each list
        if(nanopt): 
            nan_list = line_nan_check(temp,nan=nan,inf=inf,null=null)
            if(nan_list > 0):
                for j in range(len(temp)):
                    if(temp[j] not in nan_list and temp[j] != fill):
                        try:
                            temp[j] = genre(temp[j])    
                        except:
                            temp[j] = float(temp[j])
        else:
            nan_list = line_nan_check(temp,False,False,True)
            if(nan_list > 0):
                for j in range(len(temp)):
                    if(temp[j] not in nan_list and temp[j] != fill):
                        try:
                            temp[j] = genre(temp[j])    
                        except:
                            temp[j] = float(temp[j])

        op_list[i] = temp 

    if(header and entete):
        op_list.insert(0,head)
         
    if(columns):
        output = table_trans(op_list, coerce=True, fill = fill)
        if(output == False):
            print("[table_str_to_numeric] Warning: could not transpose table; returning as is")
            return op_list
        else:
            return output 
    else:
        return op_list      



def table_array_str(list_lines, split_str = '  ', row=True):
 
    lines = list(list_lines)

    for i in range(len(lines)):
        lines[i] = filter(None,lines[i].split(split_str))

    n = len(lines)
    for i in range(n):
        if(len(lines[i]) == 0):
            del lines[i]
            n=n-1
        if(len(lines[i]) == 1 and lines[i][0].isspace()):
            del lines[i]
            n=n-1     
       
    if(row):
        return lines 
    else:
        return table_trans(lines)
     

def skew_str_table_to_matrix(array, header = False, split_str = '  '):

    new_list = list(array)
    for i in range(len(new_list)):
        new_list[i] = new_list[i].split(split_str)
    
    if(header):
        header = new_list[0]
        new_list = new_list[1:-1]
    
    for i in range(len(new_list)):
        for j in range(len(new_list[i])):
            if(new_list[i][j] == ''):
                new_list[i][j] = None
 
        