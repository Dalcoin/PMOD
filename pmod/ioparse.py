import tcheck as check
import pinax as px
import strlist as strl


'''

Description: A class for performing basic IO functions on flat (text) files. 


Below is a list of the functions this class offers (w/ input):

   flat_file_read(file_in, ptype='r')

   flat_file_write(file_out, add_list, par=False, ptype='w+')

   flat_file_replace(file_out, grab_list, change_list, count_offset=True, par=True, ptype='w') 

   flat_file_grab(file_in,grab_list,scrub=False,repeat=False,count_offset=True,ptype='r')        

   flat_file_copy(file_in,file_out,grab_list,repeat=False,group=0,ptype='w')  

   flat_file_intable(file_in, header = False)
        
'''

# Variable intialization

global ptype_list, ptype_read, ptype_write

ptype_list = ['r','r+','rb','w','w+','wb','wb+','a','ab','a+','ab+']
ptype_read = ['r','r+','rb']
ptype_write = ['w','w+','wb','wb+','a','ab','a+','ab+']
          

#################################################################
# Helper functions----------------------------------------------#
#################################################################

def __dup_check__(array):
    '''If there is a duplicate in array-like object, True is returned, else False'''    
    s = set()
    for i in array:
        if i in s:
            return True
        else:
            s.add(i)         
    return False        


def __attempt_path_print__(filepath, path_name=None, func_name=None):       
    try:
        if(path_name != None):
            if(func_name != None):
                print("["+func_name+"] Error")
            print("Given pathway '"+path_name+"': "+str(filepath))
            return True                
        else:
            print("Given pathway: "+str(filepath))
            return True
    except:
        print("Pathway could not be parsed")  
        return False       


def __io_opt_test__(ptype, io, par=False, count_offset=False):
    
    success = True

    if(ptype not in ptype_list):
        success = False
        try:            
            print("[__io_opt_test__] Error: 'ptype', '"+str(ptype)+"' is not a valid 'ptype' option")
        except:
            print("[__io_opt_test__] Error: 'ptype', could not be parsed as a valid 'ptype' option string")   

    if(io == 'read'):
        if(ptype not in ptype_read):
            success = False                            
            print("[__io_opt_test__] Error: ptype, '"+str(ptype)+"' is not a valid read option")
    elif(io == 'write'):
        if(ptype not in ptype_write):   
            success = False                         
            print("[__io_opt_test__] Error: ptype, '"+str(ptype)+"' is not a valid write option")      
    else:
        success = False
        print("[__io_opt_test__] Error: option 'io' must be either 'read' or 'write'")
    
    test = check.type_test_print(par,bool,'par','__io_opt_test__') 
    if(not test):
        success = False 
         
    test = check.type_test_print(count_offset,bool,'count_offset','__io_opt_test__') 
    if(not test):
        success = False 
              
    return success


def __grab_list_test__(grab_list, n, m,repeat = False, change_list = None):

    test = check.type_test_print(grab_list,list,'grab_list','__grab_list_test__')
    if(not test):
        return False

    if(n>0):
        for i in range(n):
            test = check.type_test_print(grab_list[i],int,'grab_list['+str(i)+']','__grab_list_test__') 
            if(not test):
                return False 

    if(repeat):
        saut = grab_list[1:-1]
        test = __dup_check__(saut)
        if(test):
            print("[__grab_list_test__] Error: 'saut' values must be unique")
            return False            
    else:
        test = __dup_check__(grab_list)
        if(test):
            print("[__grab_list_test__] Error: 'grab_list' values must be unique")
            return False

        
    if(n>m):
        print("[__grab_list_test__] Error: 'grab_list' is longer than the number of file lines")
        return False
    if(m < (max(grab_list)+1)):
        print("[__grab_list_test__] Error: replacement line number greater than the max number of files lines")
        return False

    if(change_list != None):
        if(len(grab_list) != len(change_list)):  
            print("[__grab_list_test__] Error: 'grab_list' and 'change_list' must have the same length")
            return False
  
        for i in range(len(change_list)):
            test = check.type_test_print(change_list[i],str,'change_list['+str(i)+']','flat_file_replace') 
            if(not test):
                return False        
    return True


def __list_repeat__(grab_list,file_lines,scrub):
    '''   
    
    variables:

    grab_list : list (int), list of ints for formatting according to 'repeat'
    file_lines : list (str), list of strs which are selected according to 'repeat'
    scrub : True to remove end line and carriage return
    
    rules for the 'repeat' format for 'grab_list':

    1) The first value of the grab_list is 'bnd' (bind): corrosponding 
       to the spacing (binding) the grouped lines togeather: grab_list[0]
    
    2) The next values of the grab_list are 'saut' (sauter): the first repeat 
       instances to be selected from, according to line number: grab_list[1:-1] 

    3) The last value of grab_list is 'n' (number): the number of groups to be 
       generated. Spacing between groups corrosponds to 'bnd', while 
       the grouped values start from the 'saut' line values.  

    ''' 
    if(len(grab_list)<3):
        print("[__list_repeat__] Error: 'grab_list' must have at least 3 entries when 'repeat' is True")
        return False        

    raw_lines = []          
    
    lim = len(file_lines)        

    bnd = grab_list[0]+1        
    saut = grab_list[1:-1]
    n = grab_list[-1]+1
     
    if(bnd < 1):
        print("[__list_repeat__] Error: 'bnd' (first value of 'grab_list') must be 1 or greater") 
        return False 
    if(len(saut)> lim):
        print("[__list_repeat__] IndexError: there are more lines to be grabed than file_lines")
        return False 
    for i in saut:
        if(i<0):
            print("[__list_repeat__] Error: 'saut' (grab_list[1:-1]) value should not be negative")
    if(lim < max(saut)+bnd*(n-1)):
        print("[__list_repeat__] IndexError: grab_list evaluation exceeds length of file_lines") 
        return False

    for i in range(n):
        for j in range(len(saut)):
            line_tag = saut[j]+bnd*i
            if(scrub):
                file_lines[line_tag] = file_lines[line_tag].strip("\n").strip("\r")  
            raw_lines.append(file_lines[line_tag])    
    return raw_lines


#########################
#---IOParse functions---#
#########################

def flat_file_read(file_in, ptype='r'):
    '''
    flat_file_read(file_in, ptype='r')

    Description: Writes a list of strings (1 line per string) from an input file, various options for parsing

    (e.g.) :

        flat_file_read('file.in', ptype='r')

    Variables:

        'file_in': file string pathway, if only a single node is given, current (path) directory is assumed

        'ptype': [*] a string in found in the 'ptype_read list'.

    Output: List of Strings; Output: Success Boolean

    '''

    test = __io_opt_test__(ptype, 'read')
    if(not test):
        return False

    test = check.type_test_print(file_in, str, 'file_in', 'flat_file_read')
    if(not test):
        return False

    try:
        with open(file_in, ptype) as file_in:
            file_lines = file_in.readlines()
        return file_lines
    except:
        print("[flat_file_read] Error: File could not be read")
        __attempt_path_print__(file_in)
        return False


def flat_file_write(file_out, add_list=[], par=False, ptype='w+'):
    '''
    flat_file_write(file_out, add_list=[], par=False, ptype='w')

    Description: Writes a list of strings to an output file, various options for parsing

    (e.g.)

        flat_file_write('file.in', ["This is the first line!","This is line #2!"])

    Variables:

        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'add_list': [*] list of strings, each string is a separate line, order denoted by the index.
                    if the 'add_list' is empty then an empty file is created

        'ptype': [*] a string in found in the ptype_write list.

        'par': [*] True if endline character is to be added to each output string, else False.

    Output: Success Boolean
    ''' 

    # Testing proper variable types
    test = __io_opt_test__(ptype,'write', par=par)
    if(not test):
        return False         

    test = check.type_test_print(file_out, str, 'file_out', 'flat_file_write') 
    if(not test):
        return False
    test = check.type_test_print(add_list, list, 'add_list', 'flat_file_write') 
    if(not test):
        return False

    n=len(add_list)
    for i in xrange(n):
        test = check.type_test_print(add_list[i], str, 'add_list['+str(i)+']', 'flat_file_write')
        if(not test):
            return False

    # Print content to file
    try:
        with open(file_out, ptype) as fout:
            for i in add_list:
                if(par):
                    fout.write(i+"\n")
                else:
                    fout.write(i)
        return True
    except:
        print("[flat_file_write] Error: 'add_list' lines could not be printed to file")
        __attempt_path_print__(file_out,'file_out')
        return False


def flat_file_append(file_out, add_list, par=False):
    '''
    flat_file_append(file_out, add_list, par=False)

    Description: Appends a list of strings to an output file

    (e.g.)

        flat_file_write('file.in',["\n","This is the second to last line!","This is the last line!"])

    Variables:
    
        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'add_list': list of strings, each string is a separate line, order denoted by the index. 

        'ptype': [*] a string in found in the ptype_write list.         

        'par': [*] True if endline character is to be added to each output string, else False. 

    Output: Success Boolean         

    ''' 

    ptype = 'a+'
    # Testing proper variable types
    test = check.type_test_print(file_out,str,'file_out','flat_file_append') 
    if(not test):
        return False
    test = check.type_test_print(add_list,'arr','add_list','flat_file_append') 
    if(not test):
        return False
    
    n=len(add_list)
    for i in range(n):
        test = check.type_test_print(add_list[i],str,'add_list['+str(i)+']','flat_file_append')
        if(not test):
            return False           
        
    # Print content to file   
    try: 
        with open(file_out,ptype) as fout:
            for i in add_list: 
                if(par):
                    fout.write(i+"\n")
                else:
                    fout.write(i) 
        return True 
    except: 
        print("[flat_file_write] Error: 'add_list' lines could not be printed to file")
        __attempt_path_print__(file_out,'file_out')
        return False         
     
     
def flat_file_replace(file_out, grab_list , change_list, count_offset=True, par=False, ptype='w'):
    '''
    Description: In the file 'file_out', the lines in 'grab_list' are replaced with the strings in 'change_list'

   (e.g.) 
   
       flat_file_replace('file.in', [1,2], ["This is the first line!","This is line #2!"])

    Variables:
    
        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start 

        'change_list': list of strings, each string is a separate line

        'par': [*] True if endline character is to be added to each output string, else False. 

        'count_offset': [*] True if values in grab_list corrospond to line numbers, else values corrospond to list index

        'ptype': [*] a string in found in the ptype_write list.         

    Output: Success Boolean   
    '''
    
    # Testing proper variable types
    test = __io_opt_test__(ptype, 'write', par=par, count_offset=count_offset)
    if(not test):
        return False
    test = check.type_test_print(file_out,str,'file_out','flat_file_replace') 
    if(not test):
        return False

    # Accounts for the difference between line number (starting at 1) and python indexing (starting at 0)
    if(count_offset):      
        grab_list = [x-1 for x in grab_list]

    # Read in file
    file_lines = flat_file_read(file_out)
    m = len(file_lines)   
    
    # Testing the lengths of variable arrays 
    n = len(grab_list)
    test = __grab_list_test__(grab_list, n, m,repeat = False, change_list = change_list)
    if(not test):
        return False
        
    # Make modifications 
    for i in grab_list:
        j = grab_list.index(i)
        if(par):
            file_lines[i] = change_list[j]+"\n"
        else:
            file_lines[i] = change_list[j]
    
    # Print modifications to file 
    result = flat_file_write(file_out,file_lines,ptype=ptype)
    return result
    
    
def flat_file_grab(file_in, grab_list = [], scrub=False, repeat=False, count_offset=True, ptype='r'):
    '''
    Description: Grabs the lines in 'grab_list' as strings from the file 'file_in'

   (e.g.) 
   
       flat_file_replace('file.in', [1,2], ["This is the first line!","This is line #2!"])

    Variables:
    
        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start 

        'scrub': [bool] (False), Removes end and return line characters from each grabbed string  

        'repeat': [bool] (False), if True, then 'grouping' formatting is used

        'count_offset': [bool] (True), shifts 'grab_list' values by 1 to align line numbers with python indices

        'ptype': [string] ('r'), reading mode          

    Output: List of Strings; Output: Success Boolean  
    '''
            
    # Testing proper variable types
    test = __io_opt_test__(ptype,'read',count_offset=count_offset)
    if(not test):
        return False
    test = check.type_test_print(file_in,str,'file_in','flat_file_grab') 
    if(not test):
        return False

    # Accounts for the difference between line number (starting at 1) and python indexing (starting at 0)
    if(count_offset):      
        grab_list = [x-1 for x in grab_list]
    n = len(grab_list)

    # Read in file
    file_lines = flat_file_read(file_in)
    if(n == 0):
        if(scrub == True):
            for i in range(len(file_lines)):
                file_lines[i] = file_lines[i].strip('\n').strip('\r')
            return file_lines   
        else:
            return file_lines     
    m = len(file_lines)  
    
    # Testing the grab_list                
    test = __grab_list_test__(grab_list, n, m, repeat = repeat)
    if(not test):
        return False
    
    # Parse and return file_lines through 'repeat' option:                
    out_lines = [] 
                                                         
    if(repeat):  
        out_lines = __list_repeat__(grab_list,file_lines,scrub)  
        if(out_lines == False):
            return False
    else:                
        for i in range(n):
            out_lines.append(file_lines[grab_list[i]])     
            if(scrub == True):
                out_lines[i] = out_lines[i].strip("\n").strip("\r")
    return out_lines                  


def flat_file_copy(file_in, file_out, grab_list, repeat=False, group=0, ptype='w'):
    '''
    Description: Grabs the lines in 'grab_list' as strings from the file 'file_in'
                 the lines in grab_list are then printed to file_out 

   (e.g.) 
   
       flat_file_replace('file.in', [1,2], ["This is the first line!","This is line #2!"])

    Variables:
    
        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed

        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start 

        'scrub': [bool] (False), Removes end and return line characters from each grabbed string  

        'repeat': [bool] (False), if True, then 'grouping' formatting is used

        'count_offset': [bool] (True), shifts 'grab_list' values by 1 to align line numbers with python indices

        'ptype': [string] ('r'), reading mode          

    Output: List of Strings; Output: Success Boolean  
    '''

    # basic dummy check of variables 'file_out' and 'group'
    test = check.type_test_print(file_out,str,'file_out','flat_file_copy') 
    if(not test):
        return False         
    test = check.type_test_print(group,int,'group','flat_file_copy') 
    if(not test):
        return False  
    if(group < 0):
        print("[] Error: 'group' must be a non-negative integer")
        return False
     
    # Grab appropriate lines (as specified from grab_list and repeat) from 'file_in' 
    lines = flat_file_grab(file_in,grab_list,scrub=False,repeat=repeat)
    if(lines == False):
        print("[flat_file_copy] Error: retrieving data from 'file_in' failed")
        try: 
            print("'file_in' pathway: "+file_in)
            return False
        except:
            print("'file_in' pathway could not be parsed, check the pathway for errors")
            return False 

    # Parse and return 'out_list' through 'repeat' and 'group' options  
    if(repeat):
        nlines = len(lines)
        out_list = []

        if(group>0):
            for i in range(nlines):
                out_list.append(lines[i])
                if(i>0 and (i+1)%group == 0):
                    out_list.append("\n")
    else:
        if(group>0):
            out_list.append(lines[i])
            if(i>0 and (i+1)%group == 0):
                out_list.append("\n")
     
    result = flat_file_write(file_out, out_list, ptype=ptype) 
    return result
     
     
def flat_file_intable(file_in, header=False, entete=False, columns=True, genre=float):
    ''' 

    Purpose: To read in a well constrained table from a text file. 


    Inputs:

        file_in : python string, corrosponding to a file pathway
        
        header  : If True, the first string in the file is treated as a header string 
          
        entete  : If True and header is True, then the header values are included in the output 
        
        columns : If True, lists of the data value are returned by column, else data values are returned by row
     
    '''  
    table_lines = flat_file_grab(file_in, scrub = True)
    table_num = px.table_str_to_numeric(table_lines, header=header, entete=entete, columns=columns, genre=genre)
    return table_num


def flat_file_skewtable(file_in, 
                        space = '    ', 
                        fill='NULL', 
                        nval = False,
                        numeric = True,
                        header = False, 
                        entete = False, 
                        columns = True, 
                        nanopt = True, 
                        nantup = (True,True,True),
                        spc = ' ',
                        genre = float,
                        debug = True):
    '''
    Purpose: To read in a skewed table from a text file. 

    Inputs:

        file_in : python string, corrosponding to a file pathway

        see 'table_str_to_fill_numeric' in the pinax.py file for details on the options
    '''

    table_lines = flat_file_grab(file_in, scrub = True)
    table_num = px.table_str_to_fill_numeric(table_lines, 
                                             space = space,
                                             fill = fill, 
                                             nval = nval,
                                             header = header, 
                                             entete = entete, 
                                             columns = columns, 
                                             nanopt = nanopt, 
                                             nantup = nantup,
                                             spc = spc, 
                                             genre = genre,
                                             debug = True)
    return table_num
     

def iop_help(string):
    '''
    
    '''
    if(not isinstance(string,str)):
        print("Error: Input must be a string, to view a list of valid inputs, input 'help'") 
        return None

    string = string.lower()
    string = strl.str_filter(string,' ')
       
    help_list = ['help',
                 'flat_file_read',
                 'flat_file_write',
                 'flat_file_replace',
                 'flat_file_grab',
                 'flat_file_copy',  
                 'flat_file_intable',
                 'flat_file_skewtable',
                 'repeat',
                ]

    help_action = [None,
                   "(Input: path string, output: list) Reads the content of a \n"+
                   "flat (text) file line-by-line, each entry in output list\n"+
                   " corrosponds to a line in the file",

                   "(Input: path string; list of strs, output: bool) Writes the\n"+ 
                   "contents of a list of strings to a file line-by-line so that\n"+
                   "the string index (+1) corrosponds to the file line at the\n"+    
                   "path string.\n",  

                   "(Input: path string; list of ints; list of strs, output: bool)\n" 
                   "Replaces lines at line numbers found in grab_list with entries\n"
                   "found in change_list.\n",    

                   "(Input: path string; list of ints, output: list of strs)\n"+     
                   "Grabs the line numbers as text strings as specified in the grab_list\n"+
                   "and returns them as a list of strings. Option 'repeat' for advanced\n"+  
                   "selection of repeating group of lines spaced by a constant\n"+  
                   "number of lines.\n",
  
                   "(Input: path_string; path_string; list of ints, output: bool)\n"+
                   "copies lines from 'file_in' to 'file_out'. The lines which are\n"+ 
                   "copied are deterined by 'grab_list' and 'repeat' options. An\n"+ 
                   "empty grab_list list results in the entire 'file_in' being copied.\n",

                   "(Input: file_in; header = False)\n"+                        
                   "Reads in values from a text file, attempts to formate the results\n"+
                   "as a 'pinax' table.\n"
                   ]         
    
    help_dict = dict(zip(help_list, help_action))

    if(string == 'help'):
        strl.print_fancy(help_list, header = "Valid 'help' strings: ")
        return None
    else:
        try: 
            strl.print_fancy(help_dict[string], header = string+" documentation:")
            return None 
        except:
            print("Error : input string '"+string+"' could not be evaluated, use 'help' for input suggestions")
            return None
            
        