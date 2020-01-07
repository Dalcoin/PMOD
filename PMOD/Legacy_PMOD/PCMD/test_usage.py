from PCMD import path_parse as pp


# Generating example for utility

def run(cmdin,pp_inst,output=True):
   
    indt = '   '
    
    success,value = pp_inst.cmd(cmdin)
   
    if(output):
        print("Output:")
        print(indt+"Success: "+str(success))
        print(indt+"Value: "+repr(value))  
        
    return (success,value)

# Examples

winnp = pp(os_form='Windows')                                  # No print on Windows
winpp = pp(os_form='Windows',path_print=True,print_col=True)   # Print on Windows  
linnp = pp(os_form='Linux')                                    # No print on Linux
linpp = pp(os_form='Linux',path_print=True,print_col=True)     # Print on Linux

# Running Example
run('ls',winpp)


