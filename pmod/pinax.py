import re

import strlist as strl
import tcheck as check

global re_space

global nan_list, inf_list, null_list, truth, nil, truth_dict, match_dict

nan_list = ['nan', 'NaN', 'NAN', '-nan', '-NaN', '-NAN']
inf_list = ['inf', 'Inf', 'INF', '-inf', '-Inf', '-INF']
null_list = ['null', 'Null', 'NULL', '-null', '-Null', '-NULL']

truth = ('nan','inf','null')
nil = (nan_list, inf_list, null_list)

match_dict = dict(zip(truth,nil))

re_space = re.compile("^\s+$")

printer = check.imprimer()

#################################################################
# Helper functions----------------------------------------------#
#################################################################

def __err_print__(errmsg, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    printer.errPrint(errmsg, **kwargs)

def __not_str_print__(var, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    return not printer.strCheck(var, **kwargs)

def __not_arr_print__(var, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    return not printer.arrayCheck(var, **kwargs)

def __not_num_print__(var, varID=None, **kwargs):
    if(isinstance(varID, str)):
        kwargs["varName"] = varID
    return not printer.numCheck(var, **kwargs)

####################                         ####################
#  line functions  ###########################  line functions  #
####################                         ####################

###################
#  NAN functions  #
###################

def __nan_func__(check_list):
    check_type = []
    truth_dict = dict(zip(truth,check_list))
    for i in truth:
        if(truth_dict[i]):
            check_type.append(match_dict[i])
    return check_type


def nan_check(string, nan=True, inf=True, null=True, **pkwargs):

    if(not isinstance(string, str)):
        try:
            string = str(string)
        except:
            pkwargs["varName"] = "string"
            __err_print__("is not castable to a python 'str'", **pkwargs)
            return False

    check_list = (nan, inf, null)
    check_type = __nan_func__(check_list)

    if(string in check_type):
        return True
    else:
        return False


def line_nan_check(array, nan=True, inf=True, null=True, **pkwargs):

    if(__not_arr_print__(array, varID="array", **pkwargs)):
        return False

    check_list = (nan,inf,null)
    check_type = __nan_func__(check_list)

    index_list = []
    for i in range(len(array)):
        if(array[i] in check_type):
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


def ismatrix(n, numeric=False, string=False, matrixName=None, **pkwargs):

    pkwargs = printer.update_funcName("ismatrix", **pkwargs)

    mID=''
    if(isinstance(matrixName, str)):
        mID = matrixName
    else:
        mID = "n"

    if(__not_arr_print__(n, varID=mID, **pkwargs)):
        return False

    lang = 0
    for i,entry in enumerate(n):
        if(__not_arr_print__(entry, varID=mID+" entry with index "+str(i), **pkwargs)):
            err = True
            return False
        else:
            if(i == 0):
                lang = len(entry)

            if(numeric):
                err_arr = [str(j) for j in entry if not check.isNumeric(j)]
            elif(string):
                err_arr = [str(j) for j in entry if not isinstance(j, str)]
            else:
                err_arr = [str(j) for j in entry if not check.isNumeric(j) and not isinstance(j, str)]

            if(len(err_arr)>0):
                __err_print__(["Below is the invalid content in the "+strl.print_ordinal(i+1)+" entry of "+mID+":"]+err_arr, **pkwargs)
                return False
            if(len(entry) != lang):
                errString_p1 = "length of the "+strl.print_ordinal(i+1)+" entry of '"+mID
                __err_print__(errString_p1+"' doesn't match the length of the first entry", **pkwargs)
                return False
    return True


def coerce_to_matrix(n, fill="NULL", matrixName=None, **pkwargs):

    mID=''
    if(isinstance(matrixName, str)):
        mID = matrixName
    else:
        mID = "n"

    pkwargs = printer.update_funcName("coerce_to_matrix", **pkwargs)

    if(__not_arr_print__(n, varID=mID, **pkwargs)):
        return False

    newn = list(n)
    maxl = 0

    for i,entry in enumerate(newn):
        if(__not_arr_print__(entry, varID=strl.print_ordinal(i+1)+" entry of matrix "+mID), **pkwargs):
            return False
        if(len(entry) > maxl):
            maxl = len(entry)

    for i,entry in enumerate(newn):
        if(len(entry) < maxl):
            while(len(newn[i]) < maxl):
                newn[i].append(fill)
    return newn


def table_trans(n, test_matrix=True, coerce=False, numeric=False, string=False, fill='NULL', matrixName=None, **pkwargs):

    pkwargs = printer.update_funcName("coerce_to_matrix", **pkwargs)

    matrix_assert = True
    if(test_matrix):
        if(coerce):
            if(not isinstance(pkwargs.get("failPrint"), bool)):
                pkwargs["failPrint"] = False
                oldval=None
            else:
                pkwargs["failPrint"] = False
                oldval=pkwargs["failPrint"]
        if(not ismatrix(n, numeric=numeric, string=string, matrixName=matrixName, **pkwargs)):
            matrix_assert = False
        if(coerce):
            pkwargs["failPrint"] = oldval

    if(coerce and not matrix_assert):
        n = coerce_to_matrix(n, fill=fill, matrixName=matrixName, **pkwargs)
        if(n == False):
            return False
    elif(not matrix_assert):
        return False
    else:
        pass

    nrow = len(n[0])
    new_matrix, new_row = [],[]

    for k in range(nrow):
        for i in n:
            new_row.append(i[k])
        new_matrix.append(new_row)
        new_row=[]

    return new_matrix


def table_str_to_numeric(table_list,
                         header=False,
                         entete=False ,
                         transpose=True,
                         nanopt=True,
                         nantup=(True,True,True),
                         spc=' '     ,
                         genre=float,
                         tableName=None,
                         debug=True,
                         **pkwargs):
    '''
    Input Variables:

        table_list : A python array (list or tuple) of strings which form a numeric table (header option allowed)
        header    : If True, treats the first line in the input array as a header and not with the data
        entete    : If header, attempts to return the header with the output numeric table
        transpose : If True, attempts to return transposed data parsed from 'table_list'
        nanopt    : If True, 'NaN' values do not return error values 
        nantup    : A tuple in the form (nan,inf,null), each value is true if it is allowed
        spc       : string, seperator for numeric values in the input table (',' for CSV, space ' ' is default)
        genre     : A python object function: attempts to coerce object type to 'genre', float is default (str, int)
        debug     : If True, checks performs dummy-check on input data, returns printing of point or location of failure

    Purpose:
    
        Takes a list of strings and attempts to convert into a table of numeric values 
        Useful if working with formatted data tables
    '''

    pkwargs = printer.update_funcName("table_str_to_numeric", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    tableName = ''
    if(isinstance(table_name, str)):
        tableID = table_name
    else:
        tableID = "table_list"

    try:
        nan,inf,null = nantup
    except:
        __err_print__("incorrectly formatted; should be a tuple of three bools", varID="nantup", **pkwargs)
        return False

    if(debug):
        if(__not_arr_print__(table_list, varID=tableID, **pkwargs)):
            return False

        for i,entry in table_list:
            if(__not_str_print__(entry, varID=strl.print_ordinal(i)+" entry of "+tableID, **pkwargs)):
                return False

        if(not isinstance(genre, type)):
            genre = float

    new_table_list = strl.array_filter_spaces(table_list)
    if(new_table_list == False):
        __err_print__("couldn't be filtered", varID=tableID, **pkwargs)
        return False

    n = len(new_table_list)

    if(header):
        head = new_table_list[0]
        new_table_list = new_table_list[1:]
        n = len(new_table_list)
        try:
            head = strl.str_to_list(head, spc=spc, filtre=True)
            nhead = len(head)
        except:
            __err_print__("couldn't be parsed with a header (first) entry; failure to convert to 'list'", varID=tableID, **pkwargs)
            return False

    nanopt_test = False
    for i,entry in new_table_list:
        new_table_list[i] = strl.str_to_list(entry, spc=spc, filtre=True)
        if(new_table_list[i] == False):
            __err_print__(strl.print_ordinal(i)+" table entry; couldn't be converted to list", varID=tableID, **pkwargs)
            return False
        for j,value in enumerate(new_table_list[i]):
            try:
                if(nanopt):
                    nanopt_test = nan_check(value, nan, inf, null)
                if((genre == int or genre == long) and not nanopt_test):
                    new_table_list[i][j] = genre(float(value))
                if((genre == float or genre == str) and not nanopt_test):
                    new_table_list[i][j] = genre(value)
            except:
                ordi = strl.print_ordinal(i)
                ordj = strl.print_ordinal(j)
                __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                return False

    if(header and entete):
        try:
            new_table_list.insert(0, head)
        except:
            __err_print__("failure to incorporate header...", varID=tableID, **pkwargs)

    if(transpose):
        output = table_trans(new_table_list, test_matrix=False, matrixName=tableID, **pkwargs)
        if(output == False):
            return False
        else:
            return output 
    else:
        return new_table_list


def table_str_to_fill_numeric(table_list,
                              space = '    ',
                              fill  = 'NULL',
                              nval  = False ,
                              header=False  ,
                              entete=True   ,
                              transpose=True  ,
                              nanopt=True  ,
                              nantup=(True,True,True),
                              spc=' '       ,
                              genre=float   ,
                              tableName=None,
                              debug=True   ):

    '''

    Input Variables:

        table_list : A array (list or tuple) of strings which form a numeric table (header option allowed)

        space     : A string of spaces, corrosponds to the number of spaces required for an empty entry

        fill      : A string, corrosponds to the value which will be added in the place of an empty entry

        nval      : An integer, corrosponds to the number of values in a row, to which the table will be coerced
                    If False, the table is read according to parsed spaces

        header    : If True, treats the first line in the input array as a header and not with the data

        entete    : If header is True, attempts to return the header with the output numeric table

        transpose : If True, attempts to return lists of each transpose of data, rather than each rows as found in 'table_list'

        nanopt    : If True, NaN style strings values do not return error values as specified in nantup

        nantup    : A tuple in the form (nan,inf,null), each value is true if it is allowed

        sep       : A string, seperator for numeric values in the input table (',' for CSV, space ' ' is default)

        genre     : A python object function: attempts to coerce object type to 'genre', float is default

        debug     : If True, checks performs dummy-check on input data, returns printing of point or location of failure


    Purpose:

        Takes a list of strings and attempts to convert into a table of numeric values
        Useful if working with formatted data tables

    '''
    pkwargs = printer.update_funcName("table_str_to_fill_numeric", **pkwargs)
    pkwargs = printer.setstop_funcName(**pkwargs)

    tableName = ''
    if(isinstance(table_name, str)):
        tableID = table_name
    else:
        tableID = "table_list"

    try:
        nan,inf,null = nantup
    except:
        __err_print__("incorrectly formatted; should be a tuple of three bools", varID="nantup", **pkwargs)
        return False
    null = True

    if(debug):
        if(__not_arr_print__(table_list, varID=tableID, **pkwargs)):
            return False

        for i,entry in table_list:
            if(__not_str_print__(entry, varID=strl.print_ordinal(i)+" entry of "+tableID, **pkwargs)):
                return False

        if(not isinstance(genre, type)):
            genre = float

    if(header):
        head = table_list[0]
        new_table_list = table_list[1:]
        try:
            head = strl.str_to_list(head, spc=spc, filtre=True)
        except:
            __err_print__("couldn't be parsed with a header (first) entry; failure to convert to 'list'", varID=tableID, **pkwargs)
            return False
    else:
        new_table_list = list(table_list)

    # Parsing list of lines
    for i,entry in enumerate(new_table_list):
        string = entry
        temp = strl.str_to_fill_list(string, lngspc=space, fill=fill, nval=nval, spc=spc, numeric=False)

        # Parsing numeric values found in each list
        if(nanopt):
            nan_list = line_nan_check(temp,nan=nan,inf=inf,null=null)
            if(nan_list > 0):
                for j,value in enumerate(temp):
                    if(value not in nan_list and value != fill):
                        try:
                            temp[j] = genre(temp[j])    
                        except:
                            ordi = strl.print_ordinal(i)
                            ordj = strl.print_ordinal(j)
                            __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                            return False
        else:
            nan_list = line_nan_check(temp, False, False, True)
            if(nan_list > 0):
                for j,value in enumerate(temp):
                    if(value not in nan_list and value != fill):
                        try:
                            temp[j] = genre(temp[j])    
                        except:
                            ordi = strl.print_ordinal(i)
                            ordj = strl.print_ordinal(j)
                            __err_print__(ordi+" table entry, "+ordj+" column; failure to parse", varID=tableID, **pkwargs)
                            return False
        new_table_list[i] = temp

    if(header and entete):
        try:
            new_table_list.insert(0, head)
        except:
            __err_print__("failure to incorporate header...", varID=tableID, **pkwargs)

    if(transpose):
        output = table_trans(new_table_list, test_matrix=True, coerce=True, matrixName=tableID, **pkwargs)
        if(output == False):
            return False
        else:
            return output
    else:
        return new_table_list


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
 
        