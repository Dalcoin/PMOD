import subprocess as subp
import sys
import time

import pmod.ioparse as iop
import pmod.cmdline as cml
import pmod.strlist as strl

import pmod.vmed as vf

# Get V groupings
tstart = time.time()
numgroup, ngroup = vf.v_group()

cmv = cml.PathParse('linux')
success, in_path_list = cmv.cmd("dir dpot1.d")
if(not success):
    print("CMDError: an error occured when searching for 'dpot1.d' file pathway")
    sys.exit("The python script 'vmed_all.py' has been terminated.")

in_path = in_path_list[0]

lines_list = iop.flat_file_grab(in_path)
original_lines = list(lines_list)
if(lines_list == False):
    print("CMDError: an error occured when reading file at pathway: str(in_path)")
    sys.exit("The python script 'vmed_all.py' has been terminated.")

demark = lines_list[-1]
lines_list = lines_list[:-1]

cmd = "f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL"
try:
    subp.call(cmd, shell=True)    # Comment out if already compiled
except:
    print("SHELLError: an error occured when compiling 'eff3nfn3lo.f' and 'cpot.f'")
    sys.exit("The python script 'vmed_all.py' has been terminated.")

# Run P loop 

if('vincp' not in cmv.varPath_Folders):
    cmv.cmd('mkdir vincp')
    exist = False
else:
    cmv.cmd('rmdir vincp')
    cmv.cmd('mkdir vincp')
    exist = True

for i, entry in enumerate(ngroup):

    # Add new V-vals generator
    new_lines = list(lines_list)
    for ventry in entry:
        print(ventry[0])
        for vm in ventry:
            val = vm+'\n'
            new_lines.append(val)
    new_lines.append(demark)
    iop.flat_file_write(in_path, new_lines)

    subp.call("./xl", shell=True)
    success, value = cmv.cmd('mv pot.d pot'+str(numgroup[i])+'.txt')
    if(success == False):
        print(spc+"Error: failure to rename 'pot' file for the "+strl.print_ordinal(i)+" run")
    success, value = cmv.cmd('mv '+'pot'+str(numgroup[i])+'.txt'+' vincp')
    if(success == False):
        print(spc+"Error: failure to move 'pot' file into 'vincp' for the "+strl.print_ordinal(i)+" run")

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

iop.flat_file_write(in_path, original_lines)