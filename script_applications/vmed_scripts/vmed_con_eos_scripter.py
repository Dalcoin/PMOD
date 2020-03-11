import subprocess as subp
import time 
import sys

from pmod import ioparse as iop
from pmod import cmdline as cl 
from pmod import strlist as strl
from pmod import vmed as vf

def exit_func():
    print("[vmed_con_eos_scripter] Exit: Error detected, see previous msg for details...exiting script")
    sys.exit()   

tstart = time.time()

cml = cl.path_parse('Linux')

if('vincp' not in cml.var_path_contain):
    cml.cmd('mkdir vincp')
    exist = False
else:
    cml.cmd('rmdir vincp')
    cml.cmd('mkdir vincp')
    exist = True

### Group V contribs 
vlist = vf.v_lines()
if(vlist == False or vlist == []):
    if(vlist == []):
        print("[vmed_con_eos_scripter] Error: no contributions could be parsed from 'contribs.txt'")
    exit_func()
    
    
# Go back to working directory and grab input file data
success, in_path_list = cml.cmd("dir sample_input.txt")
if(success == False):
    print("[vmed_con_eos_scripter] Error: 'sample_input.txt' could not be accessed")
    exit_func()

in_path = in_path_list[0]

lines_list = iop.flat_file_grab(in_path, [])
demark = lines_list[-1]

if(strl.str_space_clean(demark.strip('\n').strip('\r')) == ''):
    j = 0
    while(strl.str_space_clean(lines_list[-1+j].strip('\n').strip('\r')) == ''):
        j+=-1
    demark = lines_list[-1+j]
    lines_list = lines_list[:j]

if(demark != "end param."):
    print("[vmed_con_eos_scripter] Warning: the end line in 'sample_input.txt' is not 'end param.'")
    
sum_failure = False     
    

lines_list = lines_list[:-1]

### Cycle through running each new contrib and storing the result

n = len(vlist)

output_lines = []

output_lines.append("\n")
output_lines.append("         Basic   Part    Tot      Final e   vspread  f    V     t    n\n")
output_lines.append("\n")

for i in range(n):

    # Generate new input 
    new_lines = list(lines_list)
    for j in vlist[i]:
        val = j+'\n'
        new_lines.append(val)
    new_lines.append(demark)

    force = vf.ventry("force",vlist[i])
    if(len(force) == 1):
        force=force+' '
    vnum  = vf.ventry("v",vlist[i])
    if(len(vnum)==2):
        vnum = vnum+' '
    tensor= vf.ventry("tensor",vlist[i])

    # Write the new output and run the program
    iop.flat_file_write(in_path,new_lines)
    subp.call('./xtest',shell=True)

    # 
    iop.flat_file_grab('test1.txt', scrub=True) 
    values = vf.partial_eos(file_name = 'test1.txt')
    for j in range(len(values)):
        values[j] = strl.str_to_list(values[j], filtre = True)

    try:

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
                         force,
                         vnum,
                         tensor,
                         str(i)+'\n']

    except:
        sum_failure = True
        print("[vmed_con_eos_scripter] Error: error occured when attempting to perform convergence tests")
        test_line_seq = ["   ","Failed","Failed","Failed","Failed","Failed",str(i)+"\n"]      

    output_lines.append(strl.array_to_str(test_line_seq, spc = '   '))   


    # Consolidating Files
    cml.cmd('mv test.txt;test1.txt vincp')
    cml.cmd('cd vincp')
    new_fold_name = 'run_'+str(i)
    cml.cmd('mkdir '+new_fold_name)
    cml.cmd('mv test.txt;test1.txt '+new_fold_name)
    cml.cmd('cd ..')

lines_list.append(demark)              
iop.flat_file_write(in_path,lines_list)

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
     