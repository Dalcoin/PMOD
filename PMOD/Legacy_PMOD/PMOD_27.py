# PMOD.py
# 
# Version 1.0 Construct
#
# Author: Randy Millerson
#
# Contains functions for formatting, input/output and numeric tasks
#
# Dependencies: Numpy, Scipy, Math, Time
#
# Compatibilities: Python 2.7 
#
# List of functions contained in this file: 24
#
# __type_test__
# __numeric_test__
# __numeric_assert__
# __int_assert__
# __string_assert__
# __list_assert__
# __bool_assert__
# __int_list__
# __empty_lists__
# __dup_check__
# __list_matrix_trans__
# __list_irr_matrix_trans__
# __convert_time__
# __text_file_replace__
# __text_file_grab__
# __list_file_grab__
# __table_file_parse__
# __table_err_gen_file__
# __round_decimal__
# __round_decimal_sci__
# __numeric_uni_format__
# __list_to_string__
# __spline_vals__
# __spline_int__
#
#------------------------------------------------------------------------------------------------------------
#
# __type_test__
#
# type_test('object','type')
# type_test(object_input,test_type)
#
# e.g. : type_test(10.035,float)
#
# object_input: python 'object'
# test_type: python 'type'
#
# Directions: put object to be checked in object_input, put type to be tested in test_type.
#
# Purpose: Returns bool, True if the objecthas a type equal to test_type, else False.
#
# Returns: Boolean
#
#------------------------------------------------------------------------------------------------------------
#
# __numeric_test__
#
# numeric_test('object')
# numeric_test(x)
#
# e.g. : type_test(10.035)
#
# x: python 'object'
#
# Directions: put object to be checked in x
#
# Purpose: Returns bool, True if the object is a numeric type, else False.
#
# Returns: Boolean
#
#------------------------------------------------------------------------------------------------------------
#
# __numeric_assert__
#
# numeric_assert('int','str')
# numeric_assert(n,string)
#
# e.g. : numeric_assert(10.035,'x')
#
# n: Any type
# string: 'string' type, used to indicate the variable to be checked for error
#
# Directions: put value to be checked in n, put values name in string.
#
# Purpose: Returns error if 'n' is not a numeric type as well as 
#          a string designation of variable 'n', else nothing is returned
#
# Returns: Assertion Error, None
#
#------------------------------------------------------------------------------------------------------------
#
# __int_assert__
#
# int_assert('int','str')
# int_assert(n,string)
#
# e.g. : int_assert('string','x')
#
# n: Any type
# string: 'string' type, used to indicate the variable to be checked for error
#
# Directions: put value to be checked in n, put values name in string.
#
# Purpose: Returns error if 'n' is not an integer type as well as 
#          a string designation of variable 'n', else nothing is returned
#
# Returns: Assertion Error, None
#
#------------------------------------------------------------------------------------------------------------
#
# __string_assert__
#
# string_assert('str','str')
# string_assert(n,string)
#
# e.g. : string_assert('string','x')
#
# n: Any type
# string: 'string' type, used to indicate the variable to be checked for error
#
# Directions: put value to be checked in n, put values name in string.
#
# Purpose: Returns error if 'n' is not a string type as well as 
#          a string designation of variable 'n', else nothing is returned
#
# Returns: Assertion Error, None
#
#------------------------------------------------------------------------------------------------------------
#
# __list_assert__
#
# list_assert('list','str')
# list_assert(n,string)
#
# e.g. : list_assert([1,2,3],'x')
#
# n: Any type
# string: 'string' type, used to indicate the variable to be checked for error
#
# Directions: put value to be checked in n, put values name in string.
#
# Purpose: Returns error if 'n' is not a list type as well as 
#          a string designation of variable 'n', else nothing is returned
#
# Returns: Assertion Error, None
#
#------------------------------------------------------------------------------------------------------------
#
# __bool_assert__
#
# bool_assert('bool','str')
# bool_assert(n,string)
#
# e.g. : bool_assert(True,'x')
#
# n: Any type
# string: 'string' type, used to indicate the variable to be checked for error
#
# Directions: put value to be checked in n, put values name in string.
#
# Purpose: Returns error if 'n' is not a boolean type as well as 
#          a string designation of variable 'n', else nothing is returned
#
# Returns: Assertion Error, None
#
#--------------------------------------------------------------------------------------------------
#
# __int_list__
#
# int_list('int')
# int_list(n)
#
# e.g. : int_list(10)
#
# n: non-negative integer
#
# Directions: put integer you wish to generate list of integers upto, starting from one 
#
# Purpose: Generates a sequential list of integers starting from 1, for use in other functions in this series
#
# Returns: a list of sequential integers
#
#--------------------------------------------------------------------------------------------------
#
# __empty_lists__
#
# empty_lists('int')
# int_list(n)
#
# e.g. : lista, listb, listc, listd = empty_list(4)
#
# n: non-negative, non-zero integer
# 
# Directions: put integer number of empty lists you want to generate into n, set equal
#             to the names of the corrosponding empty lists, there must be the same
#             number of lists as the values of the integer 'n'
#
# Purpose: Generates empty lists in a conscise way
#
# Returns: n number of empty lists
#
#--------------------------------------------------------------------------------------------------
#
# __dup_check__
#
# dup_check('list')
# dub_check(list_to_check)
#
# e.g. : dub_check([1,1,2,3,4,4])
#
# list_to_check: List of integers to be check for duplication: 'list' of 'int'
#
# Directions: Input a list of integers
# 
# Purpose: Checks for duplicates in a python list. 
#
#          Note that dup_check(n) starting from integer 1 and incrementing by 1 will
#          generate a list of the triangle numbers, also given by the 
#          binomial coefficient formula: (n+1 
#                                          2)
#
# Returns: A list with two entries: the first is a boolean indicating whether a duplicate occurs,
#                                   the second is an integer of pair-wise number of duplicate.
#
#--------------------------------------------------------------------------------------------------
#
# __list_matrix_trans__
#
# list_matrix_trans('list')
# list_matrix_trans(n)
#
# e.g. : convert list_matrix_trans([[1,2,3],[4,5,6],[7,8,9]])
#
# n: list of lists 
# 
# Directions: Place list of lists which form a matrix into n.
#
# Purpose: Transform an NxN matrix 
#
# Returns: List of lists
#
#--------------------------------------------------------------------------------------------------
#
# __list_irr_matrix_trans__
#
# list_irr_matrix_trans('list')
# list_irr_matrix_trans(n)
#
# e.g. : list_irr_matrix_trans([[1,2,3],[4,5,6]])
#
# n : list of lists
#
# Directions: Place list of lists which from a matrix into n
#
# Purpose: Transform NxM matrix
#
# Returns: List of lists
#
#--------------------------------------------------------------------------------------------------
#
# __convert_time__
#
# convert_time('int','bool')
# convert_time(tt,numeric_bool)
#  
# e.g. : convert_time(144000,False)
#
# tt: integer of seconds, float allowed but accurent only to an integer unit of time.
# numeric_bool: Boolean, 'True' for a string of time in the form [days, hours, minutes, seconds]
#                   else 'False' for a stylized, highly readable, but non parsable string format
# 
# Directions: place integer of seconds in tt, set formatting boolean
#
# Purpose: Converts seconds into more comprehensible time scale
#
# Returns: string, or list of int
#
#--------------------------------------------------------------------------------------------------
#
# __text_file_replace__
#
# text_file_replace('string','string','list' of 'int','list' of 'strings')
# tet_file_replace(file_name,file_make,grab_list,change_list)
#
# e.g. : text_file_replace('file.in','file.out',[6,7],["nint, mint  0 1","pint, oint  1 1"])
#
# file_name: Input file string : 'file.in'
# file_make: Output file string : 'file.out'
# grab_list: List of integers with the line to be stored or changed : [6,7]
# change_list: List of strings to replace the lines from grab_list: ["nint, mint  0 1","pint, oint  1 1"]
#
# Directions: put the name of the file whose lines you want to replace in 'file.in' 
#             put the name of the file which will be output as the replacement file in 'file.out'
#             Note: 'file.in' may be the same as 'file.out'
#             put the a list of integers, corrosponding to the lines to be changed, into grab_list
#             put list of strings to replace the lines from 'grab_list' in change_list
#             note: grab_list must be the same length as change_list.
#
# Purpose: Replace specific lines in a file with a list of new lines as specified by line number
#
# Returns: None
#
#--------------------------------------------------------------------------------------------------
#
# __text_file_grab__
#
# text_file_grab('string','string','list' of 'int','bool','int')
# text_file_grab(file_name,file_make,grab_list,repeat,group)
#
# e.g. : text_file_grab('file.in','file.out',[6,7],False,0)
#
# file_name: Input file string : 'file.in'
# file_make: Output file string : 'file.out'
# grab_list: list of integers with the lines to be parsed and printed : 'list' of 'int'
# repeat:    Boolean, true for option to repeat; if true then the repetition : 'bool'
#            value is the first value in the grab_list, the middle values are  
#            the shifted repeated indicies, and the last value is number of cycles
# group:     Integer number for lines to be grouped by paragraph, 0 if no grouping : positive 'int'
# 
# Directions: put the name of the file whose lines you want to grab in 'file.in'
#             put the name of the file which will be output as the grabbed file in 'file.out'
#             put the a list of integers, corrosponding to the lines to be grabbed, into 'grab_list'
#
# Purpose: Grab specific lines in an input file and print them to an output file, repeat options are available
#
# Returns: None
#             
#--------------------------------------------------------------------------------------------------
#
# __list_file_grab__
#
# list_file_grab('string','list' of 'int','bool',bool)
# list_file_grab(file_in,grab_list,repeat,formater)
#
# e.g. : list_file_grab('file.in',[6,7],False,True)
#    
# file_name: Input file string
# grab_list: List of integers with the lines to be parsed and printed,
#            input '[]' for the entire file to be grabed.
# repeat:    Boolean, true for option to repeat; if true then the repetition
#            value is the first value in the grab_list, the middle values are 
#            the shifted repeated indicies, and the last value is number of cycles
# formater:  Boolean, True if returned as scrubbed list, else a raw list is returned 
#
# Directions: put the name of the file whose lines you want to grab in 'file.in'
#             put the a list of integers, corrosponding to the lines to be grabbed, into 'grab_list'
#             set repeat to 'True' if repeat format is to be used (see 'repeat'), else set to 'False'
#             set formater to 'True' if you want a scrubbed list of lines, else set to 'False'
#
# Purpose: Grab a list of strings corrosponding to the lines from the input file. 
#
# Returns: List of strings, or list of list of strings
#
#--------------------------------------------------------------------------------------------------
#
# __table_file_parse__
#
# table_file_parse('string',[])
# table_file_parse(file_in,group)
#
# e.g. : table_file_parse('file.in',[6,7])
#    
# file_name: Input file string
# group: list, must either be empty or contain exactly two integers 
#
# Directions: put the name of the file whose lines you want to grab in 'file.in'
#             put either an empty list or a list of the shape of the matrix to be 
#             parsed, containing exactly two non-negative integers, into group
#
# Purpose: Parse a file into a matrix table, with controls for the shape of the matrix
#
# Returns: List of lists
#
#--------------------------------------------------------------------------------------------------
#
# __round_decimal__
#
# round_decimal('numeric','int','bool')
# round_decimal(x,d,string)
# 
# e.g. : round_decimal(42.425,2,True)
# 
# x: Input numeric
# d: Non-zero integer: number of decimal places to be rounded
# string: Boolean, If True then a string is returned, else a numeric is returned 
#
# Directions: put the number to be rounded into x, put the number of decimal places into d,
#             put a boolean to determined (True) if a string should be returned, or (False)
#             for a numeric to be returned
#
# Purpose: A simple function which rounds a number according to a number of decimal places.
#          Options are provided for string or numeric return, a float is returned if 'd' is
#          non-zero and 'string' is False, if 'd' is zero, then a integer is returned. If 
#          'string' is True, a string is always retured. 
#
# Returns: Either a string or numeric 
#
#--------------------------------------------------------------------------------------------------
#
# __round_decimal_sci__
#
# round_decimal_sci('numeric','int','bool')
# round_decimal_sci(x,d,string)
# 
# e.g. : round_decimal_sci(42.425,2,True)
# 
# x: Input numeric
# d: Non-zero integer: number of significant places to be rounded
# string: Boolean, If True then a string is returned, else a numeric is returned 
#
# Directions: put the number to be rounded into x, put the number of significant figures into d,
#             put a boolean to determined (True) if a string should be returned, or (False)
#             for a numeric to be returned. 
#
# Purpose: A simple function which returns a number according to significant figures.
#          Options are provided for string or numeric return. A numeric return results
#          in a float return. Note that for values greater than 10^15, scientific 
#          notation is used for string returns. 
#
# Returns: Either a string or float 
#
#--------------------------------------------------------------------------------------------------
#
# __numeric_uni_format__
#
# numeric_uni_format('numeric')
# numeric_uni_format(x)
# 
# e.g. : numeric_uni_format(2342.42528)
# 
# x: Input numeric
#
# Directions: put the number to be specially formatted into x
#
# Purpose: A simple function which returns a number to be returned as a string  
#          formatted to exactly 8 characters in length, for values greater than 
#          10^15, scientfic notation is used. 
#
# Returns: Either a string of exactly 8 character spaces
#
#--------------------------------------------------------------------------------------------------
#
# __spline_vals__
#
# spline_vals('list','list','list',int)
# spline_vals(xnew,x,y,der)
#
# spline_vals([2.7,3.14],[1,2,3,4,5,6],[0.12,1.26,3.42,7.20,17.77,42.33],1)
#
# xnew: list of numeric values to be to be evaluated
# x:    list of numeric x-values for function f(x) -> y
# y:    list of numeric y-values for function f(x) -> y
#
# Directions: place list of the values to be evaluated from a cubic spline in xnew,
#             place list of x-values from 1-D function into x, place list of y-values
#             from the same 1-D function, x and y should have the following relationship:
#             f(x) -> y, where the mapping is at least surjective. Place integer level of 
#             derivative to be evaluated into der, 0 is jno derivative.
# 
# Purpose: Provide a quick and relable function to evaluate splined values from an input
#          of discrete x and y points alone. Support for derivatives. 
#
# Returns: a list of numeric values
#
#--------------------------------------------------------------------------------------------------
# 
# __spline_int__
#
# spline_int('list','list','numeric','numeric')
# spline_int(x,y,a,b)
#
# spline_vals([1,2,3,4,5,6],[0.12,1.26,3.42,7.20,17.77,42.33],1,2)
#
# Directions: place list of x-values from 1-D function into x, place list of y-values
#             from the same 1-D function, x and y should have the following relationship:
#             f(x) -> y, where the mapping is at least surjective. Place numeric values 
#             into a and b, corrosponding to the lower and upper limits of integration. 
# 
# Purpose: Provide a quick and relable function to evaluate definite integral values from
#          an input of discrete x and y points alone.
#
# Returns: a list of numeric values 

import numpy as np
import scipy as sp
import math as mt
import time

#--------------------------------------------------------------------------------------------------

def type_test(object_input,test_type):
    return type(object_input) is test_type

#--------------------------------------------------------------------------------------------------

def numeric_test(x):
    bool_sum=False
    bool_sum = type_test(x,int)+bool_sum
    bool_sum = type_test(x,float)+bool_sum
    bool_sum = type_test(x,long)+bool_sum
    bool_sum = type_test(x,complex)+bool_sum
    bool_sum = bool(bool_sum)
    return bool_sum

#--------------------------------------------------------------------------------------------------

def numeric_assert(n,string):
    assert str(type(string)) == "<type 'str'>", "Error in numeric_assert(), 'string' is not a string"
    assert str(type(n)) == "<type 'int'>" or str(type(n)) == "<type 'float'>"  or \
                            str(type(n)) == "<type 'long'>", "Error: Input "+string+" is not a number"
    
#--------------------------------------------------------------------------------------------------

def int_assert(n,string):
    assert str(type(string)) == "<type 'str'>", "Error in numeric_assert(), 'string' is not a string"
    assert str(type(n)) == "<type 'int'>" , "Error: Input "+string+" is not an interger"   
    
#--------------------------------------------------------------------------------------------------

def string_assert(n,string):
    assert str(type(string)) == "<type 'str'>", "Error in numeric_assert(), 'string' is not a string"
    assert str(type(n)) == "<type 'str'>" , "Error: Input "+string+" is not a string"   
    
#--------------------------------------------------------------------------------------------------

def list_assert(n,string):
    assert str(type(string)) == "<type 'str'>", "Error in numeric_assert(), 'string' is not a string"
    assert str(type(n)) == "<type 'list'>" , "Error: Input "+string+" is not a list"    

#--------------------------------------------------------------------------------------------------

def bool_assert(n,string):
    assert str(type(string)) == "<type 'str'>", "Error in numeric_assert(), 'string' is not a string"
    assert str(type(n)) == "<type 'bool'>" , "Error: Input "+string+" is not a boolean"        
    
#--------------------------------------------------------------------------------------------------
        
def int_list(n):return [x+1 for x in range(n)]

def empty_lists(n):return ([] for i in range(n))

#--------------------------------------------------------------------------------------------------

def dup_check(list_to_check):
    
    #dup_check([1,1,2,3,4])
    #list_to_check must be a python 'list'
    #Checks to see if a list contains duplicates 
    #Output is a list containing an indicator of duplicaticity 
    #and the pair-wise number of duplicates 
    
# Note that dup_check(n) starting from integer 1 and incrementing by 1 will
# generate a list of the triangle numbers, also given by the binomial coefficient formula:
# (n+1)
#  (2)

    list_assert(list_to_check,'list_to_check')
    
    n = len(list_to_check)
    m = 0
    for i in range(n):
        m = m + (n - i)
    dup_count = 0
    dup_list = []
    dup_val = []
    x=0
    while(x < n):
        for i in range(n-x-1):
            check_res = list_to_check[x] == list_to_check[i+x+1]
            if(check_res == True):
                dup_count = dup_count+1
                dup_list.append(x)
        x=x+1
    if(dup_count > 0):
        dup_bool = True
    else: dup_bool = False
    return_collection = [dup_bool,dup_count]
    return return_collection


#--------------------------------------------------------------------------------------------------

def list_matrix_trans(n):
    
    list_assert(n,'n')
    
    len_vals=[]
    for i in range(len(n)):
        len_vals.append(len(n[i]))
    if(len(len_vals) > 1):
        x = len(len_vals)
        assert int(dup_check(len_vals)[1]) == int((x)*(x-1)/2), "Error: 'n' is not a proper matrix"
    old_row_len = len(n[0])
    old_col_len = len(n)
    new_row_set=[]
    new_row=[]
    for i in range(old_row_len):
        for j in range(old_col_len):
            new_row.append(n[j][i])
        new_row_set.append(new_row)
        new_row = []
    return new_row_set

#--------------------------------------------------------------------------------------------------
    
def list_irr_matrix_trans(n):
    
    list_assert(n,'n')
    
    len_vals=[]
    for i in range(len(n)):
        len_vals.append(len(n[i]))
        if(i>0):
            assert len_vals[i] <= len_vals[i-1], "Error: The input list is incompatible with this function"
    old_col_len = len(n)
    old_row_len = len(n[0])
    m = len(n[0])
    new_row_set=[]
    new_row=[]
    x = 0
    j = 0
    for i in range(old_row_len):
        for j in range(old_col_len):
            if(len_vals[j]-1 >= i ):
                new_row.append(n[j][i])
        new_row_set.append(new_row)
        new_row=[]
    return new_row_set      

#--------------------------------------------------------------------------------------------------

def convert_time(tt,numeric_bool):
    
#   convert_time(204235,True)    
#   tt = numeric type, number of seconds to be converted
#   numeric_bool: boolean type, controls if the output is a 
#   string (when False), or a list of floats (when True)
 
    global secs_counter
    global mins_counter
    global hrs_counter
    global days_counter
    
    def secs_counter(tt,numeric_bool):
        if(numeric_bool == False):
            if(tt == 1.):
                return str(str(int(tt))+' sec')
            else:
                tt = round_decimal(tt,3,True)
                return str(tt+' secs')        
        else:
            return [tt]
        
    def mins_counter(tt,numeric_bool):        
        mins = mt.floor(tt/60.) 
        secs = tt - mins*60
        secs = secs_counter(secs,numeric_bool)
        if(numeric_bool == False):    
            if(mins == 1):
                return str(str(int(mins))+' min'+' & '+str(secs))
            else:
                return str(str(int(mins))+' mins'+' & '+str(secs))
        else:
            return [mins,secs[0]]

    def hrs_counter(tt,numeric_bool):           
        hrs = mt.floor(tt/(3600))
        secs_left = tt - hrs*3600
        mins = mins_counter(secs_left,numeric_bool)
        if(numeric_bool == False): 
            if(hrs == 1):
                return str(str(int(hrs))+' hr, ' + str(mins))
            else:
                return str(str(int(hrs))+' hrs, ' + str(mins))
        else: 
            return [hrs,mins[0],mins[1]]
        
        
    def days_counter(tt,numeric_bool):
        days = mt.floor(tt/86400)
        secs_left = tt - days*86400
        hrs=hrs_counter(secs_left,numeric_bool)
        if(numeric_bool == False):
            if(days == 1):
                return str(str(int(days))+' day, ' + str(hrs))
            else:
                return str(str(int(days))+' days, ' + str(hrs)) 
        else:
            return [days,hrs[0],hrs[1],hrs[2]]        
    
    numeric_assert(tt,'tt')
    bool_assert(numeric_bool,'numeric_bool')
        
    tt = float(tt)
    if(tt < 0):
        tt=-1.*tt

    if (tt < 1.):
        return secs_counter(tt,numeric_bool)
    elif (tt< 60.):
        return secs_counter(tt,numeric_bool)
    elif (tt < 3600):
        return mins_counter(tt,numeric_bool)
    elif (tt < 86400):
        return hrs_counter(tt,numeric_bool)        
    else:
        return days_counter(tt,numeric_bool)

#--------------------------------------------------------------------------------------------------

def text_file_print(file_name,add_list):
    
    # text_file_replace('file.in',["line_1: 0 1","line_2: 1 1"])
    # file_name: output file string
    # add_list: list of strings, each string is a separate line, order denoted by the index. 
    
    string_assert(file_name,'file_name')
    list_assert(add_list,'add_list')
    
    n=len(add_list)
    for i in range(n):
        string_assert(add_list[i],str('add_list line #: '+str(i)))
            
    with open(file_name,'w') as file_out:
        for i in range(n): 
            file_out.write(add_list[i]+"\n")  

#--------------------------------------------------------------------------------------------------

def text_file_replace(file_name,grab_list,change_list):
    
    # text_file_replace('file.in','file.out',[6,7],["nint, mint  0 1","pint, oint  1 1"])
    # file_name: input file string
    # file_make: output file string
    # grab_list: list of integers with the line to be stored or changed
    # change_list: list of strings to replace the lines from grab_list
    
    string_assert(file_name,'file_name')
    list_assert(grab_list,'grab_list')

    for i in range(len(grab_list)):        
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: 'grab_list' is not a list of integers"
    list_assert(change_list,'change_list')
    for i in range(len(change_list)):
        assert str(type(change_list[i])) == "<type 'str'>" , "Error: 'grab_list' is not a list of strings"    
    assert len(grab_list) == len(change_list) , "Error: the length of grab_list must be the same as that of change_list"
    
    with open(file_name,'r') as file_in:
        file_lines = file_in.readlines()
        
    length = len(file_lines)
    lines_list = []
    
    for i in range(len(grab_list)):
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: grab_list must be a list of integers"
        dup_test = dup_check(grab_list)[0]
        assert dup_test == False , "Error: grab_list values must be unique"
    
    grab_list = [x-1 for x in grab_list]
    n = len(file_lines)
    m = len(grab_list)
    replace_list=[]
    j=0
    
    for i in range(m):
        if(grab_list[i] < n):
            replace_list.append([grab_list[i],str(change_list[i])])
    nonzero = 0
        
    assert n>=m , "Error: The number of replacement lines is greater than the number of file lines"
    assert n >= (max(grab_list)+1) , "Error: A replacement line is greater than the largest file line"
    
    with open(file_name,'w') as file_out:
        for i in range(n):
            for j in range(m):                
                if(i == int(replace_list[j][0])):
                    gellig = j
                    nonzero=1+nonzero         
            if(nonzero > 0):      
                file_out.write(replace_list[gellig][1]+"\n")
            else:
                file_out.write(file_lines[i])
            nonzero=0
            
#--------------------------------------------------------------------------------------------------
            
def text_file_grab(file_in,file_out,grab_list,repeat, ):
    
    # text_file_grab('file.in','file.out',[6,7],False,0)    
    # file_name: input file string
    # file_make: output file string
    # grab_list: list of integers with the lines to be parsed and printed
    #            the entire file is grabbed if grab_list is empty
    # repeat:    boolean, true for option to repeat; if true then the repetition
    #            value is the first value in the grab_list, the middle values are 
    #            the shifted repeated indicies, and the last value is number of cycles
    # group:     Integer number for lines to be grouped by paragraph, 0 if no grouping
    
    string_assert(file_in,'file_in')
    string_assert(file_out,'file_out')
    list_assert(grab_list,'grab_list')
    assert file_in != file_out , "Error: file_in must be different than file_out"
    for i in range(len(grab_list)):
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: 'grab_list' is not a list of integers"     
    bool_assert(repeat,'repeat')
    int_assert(group,'group')
    assert group >= 0 , "Error: 'group' is negative, group should be non-negative"
    
    with open(file_in,'r') as file_in_open:
        file_lines = file_in_open.readlines()
    
    if(len(grab_list) == 0):
        n=len(file_lines) 
        with open(file_out,'w') as fileout:
            for i in range(n):
                fileout.write(file_lines[i])
        return
        
    grab_list = [x-1 for x in grab_list]
        
    n = len(grab_list)
    raw_lines = []
    form_lines = []
    
    if(repeat == False):
        grab_list_check = grab_list
    else:
        grab_list_check = grab_list[1:-1]
    
    for i in range(len(grab_list_check)):
        assert str(type(grab_list_check[i])) == "<type 'int'>" , "Error: grab_list must be a list of integers"
        dup_test = dup_check(grab_list_check)[0]
        assert dup_test == False , "Error: grab_list values must be unique"
        
    if(repeat == False):
        assert len(file_lines) >= max(grab_list)+1 , "Error: a line value in grab_list exceeds the number of lines file_in"
        for i in range(n):
            raw_lines.append(file_lines[grab_list[i]])
            lines = file_lines[grab_list[i]].strip("\n").strip("\r").split(" ")            
            lines = [x for x in lines if x != ''] 
            form_lines.append(lines)
        
        with open(file_out,'w') as fileout:
            if(group>0):
                fileout.write(raw_lines[i])
                if(i>0 and (i+1)%group == 0):
                    fileout.write("\n")
            else:
                for i in range(n):
                    fileout.write(raw_lines[i])                 
                
    if(repeat == True):  
        
        bnd = grab_list[0]+1
        saut = grab_list[1:-1]
        len_saut = len(saut)
        n = grab_list[-1]+1
        
        max_line = len(file_lines)        
        line_end = grab_list[-2]+(n-1)*bnd+1
        assert max_line >= line_end , "Error: Your max line grabbed exceeds total file lines"           
        
        for i in range(n):
            for j in range(len_saut):
                line_tag = saut[j]+bnd*i
                raw_lines.append(file_lines[line_tag])
                lines = file_lines[line_tag].strip("\n").strip("\r").split(" ")            
                lines = [x for x in lines if x != '']                 
                form_lines.append(lines)
        with open(file_out,'w') as fileout:
            if(group>0):
                for i in range(n*len(saut)):
                    fileout.write(raw_lines[i])
                    if(i>0 and (i+1)%group == 0):
                        fileout.write("\n")
            else: 
                for i in range(n*len(saut)):
                    fileout.write(raw_lines[i])

#--------------------------------------------------------------------------------------------------
    
def list_file_grab(file_in,grab_list,repeat,formater):
    
    # list_file_grab('file.in',[6,7],False,True)    
    # file_in: input file string
    # grab_list: list of integers with the lines to be parsed and printed
    #            input [] for the entire file to be grabed.
    # repeat:    boolean, true for option to repeat; if true then the repetition
    #            value is the first value in the grab_list, the middle values are 
    #            the shifted repeated indicies, and the last value is number of cycles
    # formater:  Boolean, True if returned as scrubbed list, else a raw list is returned  
    
    string_assert(file_in,'file_in')
    list_assert(grab_list,'grab_list')
    bool_assert(repeat,'repeat')
    bool_assert(formater,'formater')
    
    with open(file_in,'r') as file_in_r:
        file_lines = file_in_r.readlines()    
    
    raw_lines = []
    form_lines = []   

    if(len(grab_list) == 0):
        n=len(file_lines)    
        if(formater == True):
            for i in range(n):
                lines = file_lines[i].strip("\n").strip("\r").split(" ")            
                lines = filter(None,lines) 
                form_lines.append(lines)
            return form_lines
        else:
            for i in range(n):
                raw_lines.append(file_lines[i])    
            return raw_lines       
        
    grab_list = [x-1 for x in grab_list]    
    n = len(grab_list)
    
    if(repeat == False):
        grab_list_check = grab_list
    else:
        grab_list_check = grab_list[1:-1]
    
    for i in range(len(grab_list_check)):
        assert str(type(grab_list_check[i])) == "<type 'int'>" , "Error: grab_list must be a list of integers"
        dup_test = dup_check(grab_list_check)[0]
        assert dup_test == False , "Error: grab_list values must be unique"
    
    if(repeat == False):
        for i in range(n):
            raw_lines.append(file_lines[grab_list[i]])
            lines = file_lines[grab_list[i]].strip("\n").strip("\r").split(" ")            
            lines = filter(None,lines) 
            form_lines.append(lines)
        if(formater == True):
            return form_lines
        else:
            return raw_lines                               
                
    if(repeat == True):  
        assert len(grab_list) > 2, "Error: grab_list must take at least three values"
        bnd = grab_list[0]+1
        saut = grab_list[1:-1]
        n = grab_list[-1]+1
        for i in range(n):
            for j in range(len(saut)):
                line_tag = saut[j]+bnd*i
                raw_lines.append(file_lines[line_tag])
                lines = file_lines[line_tag].strip("\n").strip("\r").split(" ")            
                lines = filter(None,lines)          
                form_lines.append(lines)            
        if(formater == True):
            return form_lines
        else:
            return raw_lines           
        
#--------------------------------------------------------------------------------------------------

def table_file_parse(file_in,group):
    
    # table_file_parse('file.in',True)
    
    # file_in: input file string
    # group: an empty list, or a list of two integers
    
    string_assert(file_in,'file_in')
    list_assert(group,'group')
    
    with open(file_in,'r') as file_in_r:
        file_lines = file_in_r.readlines()    
        
    n = len(file_lines)
                  
    grab_table = []    
    head_list = []
    
    if(len(group) != 0):
        assert str(type(group[0])) == "<type 'int'>" , "Error: first entry in 'group' is not an integer"
        assert str(type(group[1])) == "<type 'bool'>" , "Error: second entry in 'group' is not a boolean"
        grouping = group[0]
        first_skip = group[1]
        cont = True
    else:
        cont = False

    for i in range(n):
        lines = file_lines[i].strip("\n").strip("\r").split(" ")            
        lines = filter(None,lines) 
        grab_table.append(lines)
    
    table_trans = list_irr_matrix_trans(grab_table)
    m = len(table_trans)
    
    if(cont == False):
        return table_trans
    else:
        grouped_table = []
        temp_list = []
        if(first_skip == False):
            assert m%grouping == 0, "Error: There is/are column(s) that cannot be grouped"  
            temp_list=[]
            for i in range(m/grouping):
                for j in range(grouping):
                    temp_list.append(table_trans[j+i*grouping])
                grouped_table.append(temp_list)
                temp_list = []
            return grouped_table
        if(first_skip == True):
            assert (m-1)%grouping == 0, "Error: There is/are column(s) that cannot be grouped"  
            temp_list=[]
            for i in range((m-1)/grouping):
                for j in range(grouping):
                    temp_list.append(table_trans[j+i*grouping+1])
                grouped_table.append(temp_list)
                temp_list = []
            return grouped_table

#--------------------------------------------------------------------------------------------------                
        
def table_err_gen_file(file_1,file_2,file_out,header,out_header):
    
    string_assert(file_1,'file_1')
    string_assert(file_2,'file_2')
    string_assert(file_out,'file_out')
    bool_assert(header,'header')
    list_assert(out_header,'out_header')

    order_1 = table_file_parse(file_1,[])
    order_2 = table_file_parse(file_2,[])
    
    n = len(order_1)       
    assert len(order_1) == len(order_2), "Error: The number of variables differ between files"
    for i in range(n):
        assert len(order_1[i]) == len(order_1[i]), "Error: The length of variable %i differ between files" %i
    m = len(order_1[0]) 

    temp_list = []
    hold_list = []
    out_list = []

    if(header == True):        
        if(len(out_header) != n):
            assert len(out_header) == 0, "Error: 'out_header' is not a valid length, set to [] to reuse native header."
        if(len(out_header) == 0):
            for i in range(n):
                out_header.append(order_1[i][0])        
        for i in range(n):
            temp_list.append(out_header[i])
            for j in range(1,len(order_1[i])):
                err = abs(float(order_2[i][j])-float(order_1[i][j]))
                temp_list.append(numeric_uni_format(err))
            hold_list.append(temp_list)
            temp_list=[]
        out_lists = list_irr_matrix_trans(hold_list)
        for i in range(m):
            out_list.append(list_to_string(out_lists[i])) 
        text_file_print(file_out,out_list)
    else:
        for i in range(n):
            for j in range(0,len(order_1[i])):
                err = abs(float(order_2[i][j])-float(order_1[i][j]))
                temp_list.append(numeric_uni_format(err))
            hold_list.append(temp_list)
            temp_list=[]
        out_lists = list_irr_matrix_trans(hold_list)
        for i in range(m):
            out_list.append(list_to_string(out_lists[i])) 
        text_file_print(file_out,out_list)
                                            
#--------------------------------------------------------------------------------------------------
            
def round_decimal(x,d,string):
    
    # round_decimal(30.112,1,True)
    
    # x: input file string
    # d: non-zero integer
    # string: boolean, String if True, Float if false

    numeric_assert(x,'x')
    int_assert(d,'d')
    bool_assert(string,'string')
    
    assert d >= 0 , "Error: 'd' must be a non-negative integer"
    
    x = float(x)
    fm = '%.' + str(int(d)) + 'f'
    x = fm % x
    if(string == True and d>0):
        return str(x)
    elif(string == False and d > 0):
        return float(x)
    elif(string == True and d == 0):
        return(str(int(x))+".")
    elif(string == False and d == 0):
        return(int(x))
    else:
        return x
    
#--------------------------------------------------------------------------------------------------
    
def round_decimal_sci(x,d,string):
    
    # round_decimal_sci(30.112,1,True)    
    # x: input file string
    # d: a non-negative integer signifying the number of significant digits

    numeric_assert(x,'x')
    int_assert(d,'d')
    bool_assert(string,'string')
    
    assert d >= 0 , "Error: 'd' must be a non-negative integer"
    
    x = float(x)
    fm = "{:." + str(int(d)-1) + "e}"
    x = fm.format(x)
    if(string == True):
        return str(x)
    else:
        return float(x)    

#--------------------------------------------------------------------------------------------------
    
def numeric_uni_format(x):
    
    numeric_assert(x,'x')

    if(np.isnan(x) == True):
        x = 0.0
    
    pos_bool = (x > 0.0)
    neg_bool = (x < 0.0)
    nul_bool = (x == 0.0)

    if(pos_bool is True):
        if(x < 10000000):
            outpt = round_decimal(x,6,True)
            for i in range(6):
                if(x > 10.0**(i+1)):
                    outpt = round_decimal(x,6-(i+1),True)
                    if(i == 6):
                        outpt = outpt+'.'
        if(x >= 10000000):
            outpt = round_decimal_sci(x,3,True)
        if(x < 0.000001):
            outpt = round_decimal_sci(x,3,True)
    elif(neg_bool is True):
        if(x > -1000000):
            outpt = round_decimal(x,5,True)
            for i in range(5):
                if(x < -10.0**(i+1)):
                    outpt = round_decimal(x,5-(i+1),True)   
                    if(i == 5):
                        outpt = outpt+'.'
        if(x <= -1000000):
            outpt = round_decimal_sci(x,2,True)
        if(x > -0.000001):
            outpt = round_decimal_sci(x,2,True)
    else:
        outpt = '0.000000'
    return outpt

#--------------------------------------------------------------------------------------------------

def list_to_string(n):
    list_assert(n,'n')
    return_string = ''
    for i in range(len(n)):
        if(numeric_test(n[i])):
            prex = n[i]
            return_string = return_string + numeric_uni_format(prex) + " "
        else:
            prex = str(n[i])
            return_string = return_string + prex + " "
    return return_string

#--------------------------------------------------------------------------------------------------

def spline_vals(xnew,x,y,der):
    from scipy.interpolate import interp1d as spln    
    from scipy.interpolate import splrep as bspline
    from scipy.interpolate import splev as deriv
    
    list_assert(xnew,'xnew')
    list_assert(x,'x')
    list_assert(y,'y')
    int_assert(der,'der')
    assert der >= 0, "Error: 'der' must be an integer greater than or equal to zero"

    spline = spln(x,y,kind='cubic')
    spline_vals = spline(xnew)
    if(der == 0):
        return(spline_vals)
    if(der > 0):
        bspline_obj = bspline(x,y)
        der_spline_vals = deriv(xnew,bspline_obj,der)
        return(der_spline_vals)
    
#--------------------------------------------------------------------------------------------------

def spline_int(x,y,a,b):
    from scipy.interpolate import splrep as bspline
    from scipy.interpolate import splint as integ
    
    list_assert(x,'x')
    list_assert(y,'y')
    numeric_assert(a,'a')
    numeric_assert(b,'b')
    
    bspline_obj = bspline(x,y)
    int_spline_val = integ(a,b,bspline_obj)
    return(int_spline_val)
