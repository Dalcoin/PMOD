#  parsing_lib
# 
#  Version 0.5 Contruct
#
#
# List of functions contained in this file: number = 7
#
# __dup_check__
# __text_file_replace__
# __text_file_grab__
# __list_file_grab__
# __int_list__
# __convert_time__
# __list_matrix_trans__
#
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
#
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
#
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
#
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
#
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
#
#
# __list_matrix_trans__
#
# list_matrix_trans('list')
# list_matrix_trans(n)
#
# e.g. : convert list_matrix_trans([[1,2,3],[4,5,6]])
#
# n: list of numbers, float and integers allowed. Other data types work but not recommended
# 
# Directions: Place list of lists which form a matrix into n.
#
# Purpose: Transform an NxM matrix 
#
# Returns: List of lists

import numpy as np
import scipy as sp
import math as mt


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

    
    assert str(type(list_to_check)) == "<type 'list'>" , "Error: 'list_to_check' is not a list"
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
#            print(x,i+x+1)
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



def text_file_replace(file_name,file_make,grab_list,change_list):
    
#   Cette fonction contient beaucoup des lines qui sont exclures par des commentaires
#   Un jour, je vais les supprimer

    # text_file_replace('file.in','file.out',[6,7],["nint, mint  0 1","pint, oint  1 1"])
    # file_name: input file string
    # file_make: output file string
    # grab_list: list of integers with the line to be stored or changed
    # change_list: list of strings to replace the lines from grab_list

    assert str(type(file_name)) == "<type 'str'>" , "Error: 'file_name' is not a string"
    assert str(type(file_make)) == "<type 'str'>" , "Error: 'file_make' is not a string"
    assert str(type(grab_list)) == "<type 'list'>" , "Error: 'grab_list' is not an list"
    for i in range(len(grab_list)):
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: 'grab_list' is not a list of integers"
    assert str(type(change_list)) == "<type 'list'>" , "Error: 'change_list' is not an list"
    for i in range(len(change_list)):
        assert str(type(change_list[i])) == "<type 'str'>" , "Error: 'grab_list' is not a list of strings"    
    assert len(grab_list) == len(change_list) , "Error: the length of grab_list must be the same as that of change_list"
    
    with open(file_name,'r') as file_in:
        file_lines = file_in.readlines()
            
#    Ce bloc des codes est demode: n'en utilisez pas!
#    Je l'ai garde pour reference 

#    file_in = open(file_name,'r')
#    file_lines = file_in.readlines()
#    file_in.close()

#   Il faut que 'key' egale un. Si vous le change le fonction rendra rien
    key = 1
    
    length = len(file_lines)
    lines_list = []
    
#   Ce block ne sert a rien 
#    for i in range(length):
#        file_line = file_lines[i].strip("\n").strip("\r").split(" ")
#        if(key != 0):
#            lines_list.append(file_line)
    
    if (key == 1):
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
        
        with open(file_make,'w') as file_out:
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

#    Ce bloc des codes est demode: n'en utilisez pas!
#    Je l'ai garde pour information                 
                
#        file_out = open(file_make,'w')
#        for i in range(n):
#            for j in range(m):
#                if(i == int(replace_list[j][0])):
#                    gellig = j
#                    nonzero=1+nonzero                
#            if(nonzero > 0):      
#                file_out.write(replace_list[gellig][1]+"\n")
#            else:
#                file_out.write(file_lines[i])
#            nonzero=0

            

#--------------------------------------------------------------------------------------------------
            
            
def text_file_grab(file_in,file_out,grab_list,repeat,group):
    
    # text_file_grab('file.in','file.out',[6,7],False,0)
    
    # file_name: input file string
    # file_make: output file string
    # grab_list: list of integers with the lines to be parsed and printed
    # repeat:    boolean, true for option to repeat; if true then the repetition
    #            value is the first value in the grab_list, the middle values are 
    #            the shifted repeated indicies, and the last value is number of cycles
    # group:     Integer number for lines to be grouped by paragraph, 0 if no grouping

    assert str(type(file_in)) == "<type 'str'>" , "Error: 'file_in' is not a string"
    assert str(type(file_out)) == "<type 'str'>" , "Error: 'file_out' is not a string"
    assert str(type(grab_list)) == "<type 'list'>" , "Error: 'grab_list' is not an list"
    for i in range(len(grab_list)):
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: 'grab_list' is not a list of integers"     
    assert str(type(repeat)) == "<type 'bool'>" , "Error: 'repeat' is not a boolean"
    assert str(type(group)) == "<type 'int'>" , "Error: 'groupe' is not an integer"
    assert group >= 0 , "Error: 'group' is negative, group should be non-negative"
        
#    file_in_r = open(file_in,'r')
#    file_lines = file_in_r.readlines()
#    file_in_r.close()
    
    with open(file_name,'r') as file_in:
        file_lines = file_in.readlines()
    
    if(len(grab_list) == 0):
        n=len(file_lines) 
        with open(file_out,'w') as fileout:
            for i in range(n):
                fileout.write(file_lines[i])
#        fileout = open(file_out,'w')
#        for i in range(n):
#            fileout.write(file_lines[i])    
#        fileout.close()    
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
        
#        fileout = open(file_out,'w')
#        if (group > 0):
#            for i in range(n):
#                fileout.write(raw_lines[i])
#                if(i > 0 and (i+1)%group == 0):
#                    fileout.write("\n")
#        else:
#            for i in range(n):
#                fileout.write(raw_lines[i])                       
                
    if(repeat == True):  
        bnd = grab_list[0]+1
        saut = grab_list[1:-1]
        n = grab_list[-1]
        for i in range(n):
            for j in range(len(saut)):
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
                    
#        fileout = open(file_out,'w')
#        if (group > 0):
#            for i in range(n*len(saut)):
#                fileout.write(raw_lines[i])
#                if(i>0 and (i+1)%group == 0):
#                    fileout.write("\n")    
#        else:
#            for i in range(n*len(saut)):
#                fileout.write(raw_lines[i])       
        
#    fileout.close()        
    

#--------------------------------------------------------------------------------------------------
    
def list_file_grab(file_in,grab_list,repeat,formater):
    
    # list_file_grab('file.in',[6,7],False,True)
    
    # file_name: input file string
    # grab_list: list of integers with the lines to be parsed and printed
    #            input [] for the entire file to be grabed.
    # repeat:    boolean, true for option to repeat; if true then the repetition
    #            value is the first value in the grab_list, the middle values are 
    #            the shifted repeated indicies, and the last value is number of cycles
    # formater:  Boolean, True if returned as scrubbed list, else a raw list is returned  
    
    assert str(type(file_in)) == "<type 'str'>" , "Error: 'file_in' is not a string"
    assert str(type(grab_list)) == "<type 'list'>" , "Error: 'grab_list' is not an list"
    assert str(type(repeat)) == "<type 'bool'>" , "Error: 'repeat' is not a boolean"
    assert str(type(formater)) == "<type 'bool'>" , "Error: 'formater' is not a boolean"

#    file_in_r = open(file_in,'r')
#    file_lines = file_in_r.readlines()
#    file_in_r.close() 
    
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
        n = grab_list[-1]
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
        
def int_list(n):return [x+1 for x in range(n)]

#--------------------------------------------------------------------------------------------------

def convert_time(tt,numeric_bool):
    import math as mt
    
    global secs_counter
    global mins_counter
    global hrs_counter
    global days_counter
    
    def secs_counter(tt,numeric_bool):
        if(numeric_bool == False):
            if(tt == 1.):
                return str(str(int(tt))+' sec')
            else:
                return str(str(tt)+' secs')        
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
        
    assert str(type(tt)) == "<type 'int'>" or str(type(tt)) == "<type 'float'>"  or \
                                                  str(type(tt)) == "<type 'long'>", "Error: 'time' is not a number"
    assert str(type(numeric_bool)) == "<type 'bool'>" , "Error: 'numeric_bool' is not a boolean"
        
    tt = float(tt)
    if(tt < 0):
        tt=-1.*tt

    if (tt < 1.):
        return str(str(tt)+" secs")
    elif (tt< 60.):
        return secs_counter(tt,numeric_bool)
    elif (tt < 3600):
        return mins_counter(tt,numeric_bool)
    elif (tt < 86400):
        return hrs_counter(tt,numeric_bool)        
    else:
        return days_counter(tt,numeric_bool)

#--------------------------------------------------------------------------------------------------

def list_matrix_trans(n):
    
    assert str(type(n)) == "<type 'list'>" , "Error: 'n' is not a list"
    
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
    
