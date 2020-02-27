import subprocess as subp
import re
import sys
import time


from pmod import strlist as strl
from pmod import ioparse as iop
from pmod import mathops as mops
from pmod import pinax   as px
from pmod import cmdline as cl

from pmod import vmed as vf

# 
tstart = time.time()

f12n = 'fig12_v'
f13n = 'fig13_v'
    
# Get V groupings
numgroup, ngroup = vf.v_group()

cmv = cl.path_parse('linux')
success, in_path_list = cmv.cmd("dir dpot1.d")
in_path = in_path_list[0]

lines_list = iop.flat_file_grab(in_path, [])
demark = lines_list[-1]
lines_list = lines_list[:-1]

cmd = "f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL"   
subp.call(cmd, shell=True)    # Comment out if already compiled 

# Run P loop 

if('vincp' not in cmv.var_path_contain):
    cmv.cmd('mkdir vincp')
    exist = False
else:
    cmv.cmd('rmdir vincp')
    cmv.cmd('mkdir vincp')
    exist = True

for i in range(len(ngroup)):
     
    # Add new V-vals generator
    new_lines = list(lines_list)
    for j in ngroup[i]:
        val = j+'\n'
        new_lines.append(val)
    new_lines.append(demark)   
    iop.flat_file_write(in_path,new_lines) 

    subp.call("./xl", shell=True) 
    flines = iop.flat_file_grab('pot.d')
        
    table_12, table_13 = vf.gen_table_12_13(flines)
      
    twelve_name = f12n+str(numgroup[i])+'.txt'
    thirteen_name = f13n+str(numgroup[i])+'.txt'
     
    iop.flat_file_write(twelve_name, table_12, par = True)
    iop.flat_file_write(thirteen_name, table_13, par = True)
        
    cmv.cmd('mv '+twelve_name+';'+thirteen_name+' vincp')

plist = [0.1,0.5,1.0,1.3]

cmv.cmd('cd vincp')
p1s0, t1s0 = [], []

t1s0.append("p       0.1        0.5        1.0        1.3        1.5        2.0  ")
t1s0.append(" ")

for i in xrange(len(numgroup)):
    success, filename = cmv.cmd('dir '+f13n+str(numgroup[i])+'.txt')  
    filename = filename[0]
    filetable = iop.flat_file_intable(filename)    
    oneszero = filetable[1]
    p1s0.append(str(mops.round_uniform(float(oneszero[0]), pyver='26')))   # 0.1
    p1s0.append(str(mops.round_uniform(float(oneszero[4]), pyver='26')))   # 0.5
    p1s0.append(str(mops.round_uniform(float(oneszero[9]), pyver='26')))   # 1.0
    p1s0.append(str(mops.round_uniform(float(oneszero[12]), pyver='26')))  # 1.3 
    p1s0.append(str(mops.round_uniform(float(oneszero[14]), pyver='26')))  # 1.5
    p1s0.append(str(mops.round_uniform(float(oneszero[19]), pyver='26')))  # 2.0   
    p1s0.append('v'+str(numgroup[i]))
    t1s0.append(strl.array_to_str(p1s0, spc = '   ')) 
    p1s0 = []

output_list = strl.format_fancy(t1s0, list_return = True)
iop.flat_file_write('all_3p0.txt',output_list)

tend = time.time()

print('')
spc = '    '
print("Finished! No Errors reported, see below for run details:\n")
print(spc+"The script took approx. "+str(round(tend-tstart,1))+" secs to run")
print(spc+"The script found "+str(len(numgroup))+" groupings")
if(exist):
    print(spc+"The script found an existing 'vincp' directory and overwrote it\n")
else:
    print(spc+"The script did not find an existing 'vincp' directory; one was created\n")

