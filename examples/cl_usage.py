from pmod import tcheck as check
from pmod import cmdline as cl


# Generating example for utility

def run(cmdin, clinst, output=True):

    input_check = check.type_test_print(cmdin, str, var_name='cmdin', func_name='run')    
   
    indt = '   '
    
    success,value = clinst.cmd(cmdin)
   
    if(output):
        print("Output:")
        print(indt+"Success: "+str(success))
        print(indt+"Value: "+repr(value))  
        
    return (success,value)

# Examples

winnp = cl.path_parse(os_form='Windows')                                  # No print on Windows
winpp = cl.path_parse(os_form='Windows',path_print=True,print_col=True)   # Print on Windows  
#linnp = cl.path_parse(os_form='Linux')                                    # No print on Linux
#linpp = cl.path_parse(os_form='Linux',path_print=True,print_col=True)     # Print on Linux

# Running Example
run('ls',winpp)
run('pwd',winnp)


