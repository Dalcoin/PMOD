import re 

import strlist as strl 

#import tcheck as check #enable for tcheck functionality 

global re_space
 

re_space = re.compile("^\s+$")


def __func_eprint__(msg):
    if(True):
        print(msg)
    return False

####################                         #################### 
#  line functions  ###########################  line functions  #
####################                         #################### 

def line_nan_check(array):
    
    nan_list = ['nan','NaN','NAN','-nan','-NaN','-NAN']

    index_list = []
    for i in range(len(array)):
        if(i in nan_list):
            index_list.append(i)
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


def table_trans(n, coerce_rect=False, check_table=False):

    if(check_table):
        shape = get_shape_matrix(n)
        if(shape == False):
            err = __func_eprint__("[table_trans] Error: input is not a rectangular matrix")
            return err                

    nrow = len(n[0])
    new_matrix, new_row = [],[]
    
    if(coerce_rect):
        try:
            n = coerce_to_matrix(n)
        except:
            err = __func_eprint__("[table_trans] Error: input could not be coerced into a rectangular matrix")
            return err
    
    try:           
        for k in range(nrow):
            for i in n:
                new_row.append(i[k])
            new_matrix.append(new_row)
            new_row=[]
        return new_matrix
    except: 
        err = __func_eprint__("[table_trans] Error: input could not be cast into a translated matrix")
        return err           


def table_str_to_numeric(line_list, sep=' ', header=False, safety = False, columns=True, sort=float):
    
    new_line_list = strl.array_filter_spaces(list(line_list))
    n = len(new_line_list)

    if(header):
        head = new_line_list[0]
        new_line_list = new_line_list[1:-1]
        n = len(new_line_list)
        try:
            head = strl.str_to_list(head, split_val = sep, filtre = True)
            nhead = len(head)
        except:
            print("[table_str_to_numeric] Error: header could not be parsed]")
            return False
    
    for i in range(n):
        new_line_list[i] = strl.str_to_list(new_line_list[i], split_val = sep, filtre = True)
        for j in range(len(new_line_list[i])):
            try:
                if(sort == int or sort == long):
                    new_line_list[i][j] = sort(float(new_line_list[i][j]))
                if(sort == float):
                    new_line_list[i][j] = sort(new_line_list[i][j])
            except:
                if(safety):
                    pass 
                else:
                    return False

    if(header):
        try:
            new_line_list.insert(0,head)
        except:
            pass
  
    if(columns):
        output = table_trans(new_line_list)  
        if(output == False):
            return new_line_list
        else:
            return output 
    else:
        return new_line_list



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
 
    
    
    
    
    
    
    


