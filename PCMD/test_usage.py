from PCMD import path_parse as pp
cmv = pp(os_form='Linux',path_print=True,print_col=True)     # Use on Coscompile
#cmv = pp(os_form='Windows',path_print=True,print_col=True)  # Use on Windows


cdlist = cmv.cmd('ls') 
cdpath = cmv.cmd('pwd') 
first_file_path = cmv.cmd('dir '+cdlist[0])

