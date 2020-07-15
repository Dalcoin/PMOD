'''
This program is for use with the following program pipeline:

    matter.f
    nxloyyynew.f (x = 2,3,4 ; y = 450,500)
    nnsum.f\nnsum_2015_opti.f

Computes and stores EoS files generated from selected 3NF contributions at specified chiral order
'''

import subprocess as subp
import time
import sys

import pmod.vmed as vf
import pmod.ioparse as iop
import pmod.cmdline as cmv
import pmod.strlist as strl


def exit_func():
    print("[vmed_con_eos_scripter] Exit: Error detected, see previous msg for details...exiting script")
    sys.exit()

################
#              #
#   Controls   #
#              #
################

group_by_vmeds = False
group_by_vgrps = False

run_timeout = False

if(group_by_vmeds and group_by_vgrps):
    print("Warning: both v-lines and v-groups have been selected, v-group takes precedent")

if(not group_by_vmeds and not group_by_vgrps):
    print("Error: neither v-lines, nor v-groups have been selected, exiting now...")
    exit_func

if(isinstance(run_timeout, bool)):
    if(run_timeout):
        run_timeout = 100000
    else:
        run_timeout = False
elif(isinstance(run_timeout, int)):
    if(run_timeout > 0):
        pass
    else:
        run_timeout = 100000
else:
    run_timeout = False
  
########################
#                      #
#   Ends of Controls   #
#                      #
########################

tstart = time.time()

cml = cmv.PathParse('Linux')

# Make empty 'vincp' folder, clear folder if it already exists
if('vincp' not in cml.varPath_Contains):
    cml.cmd('mkdir vincp')
    exist = False
else:
    cml.cmd('rmdir vincp')
    cml.cmd('mkdir vincp')
    exist = True

### Group V contribs
if(group_by_vgrps):
    numgroup, ngroup = vf.v_group()
elif(group_by_vmeds):
    numgroup, ngroup = vf.v_lines(True)
else:
    exit_func()

if(isinstance(ngroup,(list,tuple))):
    n = len(ngroup)
    if(n == 0):
        print("[vmed_con_eos_scripter] Error: no contributions could be parsed from 'contribs.txt'")
        exit_func()
else:
    print("[vmed_con_eos_scripter] Error: failure to parse contributions from 'contribs.txt'")
    exit_func()

# Go back to working directory and grab input file data
success, in_path_list = cml.cmd("dir sample_input.txt")
if(success == False):
    print("[vmed_con_eos_scripter] Error: 'sample_input.txt' could not be accessed")
    exit_func()

in_path = in_path_list[0]
lines_list = iop.flat_file_grab(in_path)

# set the demarcation line, removes empty lines at end of file
demarc = lines_list[-1]
if(demarc.rstrip() == ''):
    j = 0
    while(lines_list[-1+j].rstrip() == ''):
        j+=-1
    demarc = lines_list[-1+j]
    lines_list = lines_list[:j]

if(demarc.rstrip() != "end param."):
    print("[vmed_con_eos_scripter] Warning: the end line in 'sample_input.txt' is not 'end param.'")

sum_failure = False

lines_list = lines_list[:-1]

### Cycle through running each new contrib and storing the result

output_lines = []

output_lines.append("\n")
output_lines.append("         Basic   Part    Tot      Final e   vspread  n\n")
output_lines.append("\n")

for i,entry in enumerate(ngroup):

    # Add new V-vals generator
    new_lines = list(lines_list)

    if(group_by_vgrps):
        for ventry in entry:
            for vm in ventry:
                val = vm+'\n'
                new_lines.append(val)
    elif(group_by_vmeds):
        for ventry in entry:
            new_lines.append(ventry+"\n")
    else:
        exit_func()

    new_lines.append(demarc)
    iop.flat_file_write(in_path, new_lines)

    if(isinstance(run_timeout, int) and not isinstance(run_timeout, bool)):
        try:
            subp.call("./xtest", shell=True, timeout=run_timeout)
        except subp.TimeoutExpired:
            print("[vmed_con_eos_scripter] Error: run number "+str(1+i)+" runtime exceeded timeout, cycling to next run...")
            cml.cmd('rm test.txt;test1.txt')
            continue
    else:
        subp.call("./xtest", shell=True)
#    subp.call("./xtest", shell=True)

    # Get select E/A values generated from the partial waves 
    values = vf.partial_eos(file_name = 'test1.txt')

    try:

        for j in range(len(values)):
            values[j] = strl.str_to_list(values[j], filtre = True)

        v1 = values[-1][-1]
        v2 = values[-2][-1]
        v3 = values[-3][-1]
        v5 = values[-5][-1]
        v8 = values[-8][-1]

        v12 = abs(float(v1)-float(v2))
        v13 = abs(float(v2)-float(v3))
        v15 = abs(float(v3)-float(v5))
        v18 = abs(float(v5)-float(v8))

        vspread = round((v12+v13+v15)/3.0,4)

        if(v18 >= v15 and v15 >= v13 and v13 >= v12):
            totconv = 'True '
        else:
            totconv = 'False'

        if(v18 >= v15 and v15 >= v12):
            partconv = 'True '
        else:
            partconv = 'False'

        if(v18 >= v12):
            basconv = 'True '
        else:
            basconv = 'False'

        test_line_seq = ["   ",
                         str(basconv),
                         str(partconv),
                         str(totconv),
                         str(v1),
                         str(vspread),
                         str(numgroup[i])+'\n']

    except:
        sum_failure = True
        print("[vmed_con_eos_scripter] Error: error occured when attempting to perform convergence tests")
        test_line_seq = ["   ","Failed","Failed","Failed","Failed","Failed",str(i)+"\n"]

    output_lines.append(strl.array_to_str(test_line_seq, spc = '   '))

    # Consolidating Files
    cml.cmd('ls')
    cml.cmd('mv test.txt;test1.txt vincp')
    cml.cmd('cd vincp')
    new_fold_name = 'run_'+str(numgroup[i])
    cml.cmd('mkdir '+new_fold_name)
    cml.cmd('mv test.txt;test1.txt '+new_fold_name)
    cml.cmd('cd ..')

lines_list.append(demarc)
iop.flat_file_write(in_path, lines_list)

try:
    iop.flat_file_write('sum_test.txt', output_lines)
except:
    sum_failure = True
    line1 = "[vmed_con_eos_scripter] Error: an error occured when attempting "
    line2 = "to write convergence tests results to 'sum_test.txt'"
    print(line1+line2)

tend = time.time()

print('')
spc = '    '

if(sum_failure):
    print("Finished, Error(s) reported (see above for error msg(s)), see below for run details:\n")   
else:
    print("Finished! No Errors reported, see below for run details:\n")
print(spc+"The script took approx. "+str(round(tend-tstart,1))+" secs to run")
print(spc+"The script found "+str(n)+" contributions")
if(exist):
    print(spc+"The script found an existing 'vincp' directory and overwrote it\n")
else:
    print(spc+"The script did not find an existing 'vincp' directory; one was created\n")
