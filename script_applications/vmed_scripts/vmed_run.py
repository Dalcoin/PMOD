import subprocess
import re

from pmod import ioparse as iop

from pmod import vmed as vf      # not a standard pmod file; must be added for compatability with all vmed scripts 

    
cmd = "f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL"
subprocess.call(cmd, shell=True)    # Comment out if already compiled  
subprocess.call("./xl", shell=True) # Comment out if already excecuted

flines = iop.flat_file_grab('pot.d')

val_table_12, val_table_13 = vf.gen_table_12_13(flines)
    
iop.flat_file_write('fig_12_vals.txt',val_table_12,par = True)
iop.flat_file_write('fig_13_vals.txt',val_table_13,par = True)
