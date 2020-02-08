import subprocess as subp
import re

from pmod import strlist as strl
from pmod import ioparse as iop
from pmod import mathops as mops
from pmod import pinax   as px
from pmod import cmdline as cl

from pmod import vmed as vf


    
# Get V groupings
numgroup, ngroup = vf.v_group()

cmv = cl.path_parse('linux')
success, in_path_list = cmv.cmd("dir dpot1.d")
in_path = in_path_list[0]

lines_list = iop.flat_file_grab(in_path, [])
demark = lines_list[-1]
lines_list = lines_list[:-1]

cmd = "f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL"   
subprocess.call(cmd, shell=True)    # Comment out if already compiled 

# Run P loop 
for i in range(len(ngroup)):
     
    # Add new V-vals generator
    new_lines = list(lines_list)
    for j in ngroup[i]:
        val = j+'\n'
        new_lines.append(val)
    new_lines.append(demark)   
    iop.flat_file_write(in_path,new_lines) 

    subprocess.call("./xl", shell=True) 
    flines = iop.flat_file_grab('pot.d')
        
    table_12, table_13 = vf.gen_table_12_13(flines)
      
    twelve_name = 'fig12_v'+str(numgroup[i])+'.txt'
    thirteen_name = 'fig13_v'+str(numgroup[i])+'.txt'
     
    iop.flat_file_write(twelve_name, table_12, par = True)
    iop.flat_file_write(thirteen_name, table_13, par = True)
        
    if('vincp' not in cmv.path_contain):
        cmv.cmd('mkdir vincp')
    cmv.cmd('mv '+twelve_name+';'+thirteen_name+' vincp')

print("Finished!\n")
