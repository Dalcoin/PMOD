import cmdline as cl
#import phelp as ph
import ioparse as iop 
import mathops as mops 
import pinax   as pnx 
import strlist as strl
import tcheck  as check 
import zkparse as zkp

'''

Welcome to the PMOD package, use the 'pmod_help' function for more info on each of the modules 

Class list:
 
    module  | class
    _______ | ___________  
    cmdline | path_parse
    mathops | spline
    zkparse | clock

'''

def pmod_help(string = ''):
    __module_list__ = ['help','cmdline','ioparse','mathops','phelp','pinax','strlist','tcheck','zkparse']

    __doc_list__ = ["'help' returns the modules in the pmod package",
                    "'cmdline' contains the 'path_parse' class which enables shell command line "+
                    "values to be passed to the '.cmd()' function, resulting in pathway and file "+
                    "management functionality",
                    "'ioparse' contains functions for file input/output, options include reading, "+
                    "writing, appending and modifying the content of flat (text) files",
                    "'mathops' contains functions for rounding numerical values as well as the "+
                    "'spline' class for performing spline and calculus operations on 1D functions",
                    "'phelp' contains functions for easy plotting using matplotlib",
                    "'pinax' class contains functions for tabulating data",
                    "'strlist' contains miscellaneous functions for parsing strings and lists",
                    "'tcheck' contains functions for 'TypeError' testing and printing",
                    "'zkparse' contains functions for time and calandar functionality, also "+
                    "contains the 'clock' class which improves time and date dependent automation"  
                   ]

    __module_doc_list__ = dict(zip(__module_list__,__doc_list__))
    
    try:      
        test_string = strl.str_space_clean(string)
    except:
        test_string = ''
     
    if(test_string in __module_list__):
        out_string = __module_doc_list__[strl.str_space_clean(string)]
    else:
        out_string = "Input string not recognized, input the name of a module in pmod for additional info"
    return out_string


# Universal Info
__version__ = '1.2'
__author__  = 'Randy Millerson'


