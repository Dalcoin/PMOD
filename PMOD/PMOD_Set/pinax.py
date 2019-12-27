import re 

#import tcheck as check #enable for tcheck functionality 

global re_space
 

re_space = re.compile("^\s+$")


def __func_eprint__(msg):
    if(True):
        print(msg)
    return False

####################                         #################### 
# action functions ########################### action functions #
####################                         #################### 

# Action functions 
# These functions are meant to be called on list arrays

def get_shape_matrix(table):
    shape = False
    n = len(table)
    m = len(table[-1])
    for i in table[:-1]:            
        if(len(i) != m):
            err = __func_eprint__("[get_shape_matrix] Error: Table does not have a rectangular shape")
            return err
    shape = (n,m)
    return shape

def coerce_to_matrix(n):
    l = max(len(i) for i in n)    
    for i in n:
        if(len(i) < l):
            while(len(i) < l): 
                i.append(None)
    return n

def check_str_allspace(string):    
    try:
        sarray = re_space.findall(string)
        if(len(sarray) == 1):
            return True
        else:
            return False
    except:
        return False 
   
def array_to_string(array, spc = '  ', print_bool = True):
    ''' 
    Input: 
        array   : A Python array (list or tuple) object  
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


def array_of_arrays_to_string(array, spc = '  '):
    ''' 
    Input: 
        array   : A Python array (list or tuple) object  
        spc [*] : A string object, usually spacing

    Return:
        out_str : A string if success, A False if failure 
    '''
    out_str = ''
    n = len(array)
    try: 
        for i in range(n):
            array[i] = array_to_string(array[i],spc)
    except:
        return False 
     
            
###################                           ################### 
# table functions ############################# table functions #
###################                           ################### 

# Table (pinax) functions 
# These functions are the main function to be used on list arrays.

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


def table_numeric(line_list,sep=' ',header=False,sort=str):
    
    new_line_list = list(line_list)
    n = len(new_line_list)
    
    if(header):
        new_line_list = table_trans(new_line_list)
        new_line_list = new_line_list[1:-1]
        head = new_line_list[0]
        new_line_list = table_trans(new_line_list)
    
    for i in range(n):
        new_line_list[i] = new_line_list[i].split(sep)
        new_line_list[i] = filter(None,new_line_list[i])
        if(sort != str):
            for j in range(len(new_line_list[i])):
                try:
                    if(sort == int or sort == long):
                        new_line_list[i][j] = sort(float(new_line_list[i][j]))
                    else:
                        new_line_list[i][j] = sort(new_line_list[i][j])
                except:
                    success = False 
                    return success
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
 
    
    
    
    
    
    
    


