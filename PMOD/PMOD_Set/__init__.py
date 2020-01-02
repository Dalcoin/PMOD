import cmdline # as cml
import ioparse # as iop 
import mathops # as mops 
import pinax   # as pnx 
import strlist # as strl
import tcheck  # as check 
import zkparse # as zkp

'''
Class list:

    ______    _____ 
    module  : class
   
    cmdline : path_parse
    mathops : spline
    zkparse : clock

'''

def doc(string = ''):
    __module_list__ = ['cmdline','ioparse','mathops','pinax','strlist','tcheck','zkparse']

    __doc_list__ = ["'cmdline' contains the 'path_parse' class which enables shell command line "+
                    "values to be passed to the '.cmd()' function, resulting in pathway and file "+
                    "management functionality",
                    "'ioparse' contains functions for file input/output, options include reading, "+
                    "writing, appending and modifying the content of flat (text) files",
                    "'mathops' contains functions for rounding numerical values as well as the "+
                    "'spline' class for performing spline and calculus operations on 1D functions",
                    "'pinax' class contains functions for tabulating data",
                    "'strlist' contains miscellaneous functions for parsing strings and lists",
                    "'tcheck' contains functions for 'TypeError' testing and printing",
                    "'zkparse' contains functions for time and calandar functionality, also "+
                    "contains the 'clock' class which improves time and date dependent automation"  
                   ]

    __module_doc_list__ = dict(zip(__module_list__,__doc_list__))
    
    try:      
        test_string = strlist.str_space_clean(string)
    except:
        test_string = ''
     
    if(test_string in __module_list__):
        out_string = __module_doc_list__[strlist.str_space_clean(string)]
    else:
        out_string = "'doc' input string not recognized, input the name of a module in pmod for additional info"
    return out_string


__version__ = '1.0'
__author__  = 'Randy Millerson'


