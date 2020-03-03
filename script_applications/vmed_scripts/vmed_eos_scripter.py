import subprocess as subp
import time 

from pmod import ioparse as iop
from pmod import cmdline as cl 
from pmod import strlist as strl
from pmod import vmed as vf

tstart = time.time()

cml = cl.path_parse('Linux')

if('vincp' not in cml.var_path_contain):
    cml.cmd('mkdir vincp')
    exist = False
else:
    cml.cmd('rmdir vincp')
    cml.cmd('mkdir vincp')
    exist = True

### Group V contribs by number
numgroup, ngroup = vf.v_group()
    
# Go back to working directory and grab input file data
success, in_path_list = cml.cmd("dir sample_input.txt")
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
    print("Warning: the end line in 'sample_input.txt' is not 'end param.'")
    
sum_failure = False     
    

lines_list = lines_list[:-1]

### Cycle through running each new contrib and storing the result

n = len(ngroup)

output_lines = []

output_lines.append("\n")
output_lines.append("     Basic  Part   Tot     Final e   V\n")
output_lines.append("\n")

for i in range(n):

    # Generate new input 
    new_lines = list(lines_list)
    for j in ngroup[i]:
        val = j+'\n'
        new_lines.append(val)
    new_lines.append(demark)

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
              
        if(v18 >= v15 and v15 >= v13 and v13 >= v12):
            totconv = True
        else: 
            totconv = False
	    
        if(v18 >= v15 and v15 >= v12):
            partconv = True
        else:
            partconv = False
	    
        if(v18 >= v12):
            basconv = True
        else:
            basconv = False   

        test_line_seq = ["   ",
                         str(basconv),
                         str(partconv),
                         str(totconv),
                         str(v1),
                         "v"+str(numgroup[i])+'\n']

    except:
        sum_failure = True
        test_line_seq = ["   ","Failed","Failed","Failed","Failed","v"+str(numgroup[i])+'\n']      

    output_lines.append(strl.array_to_str(test_line_seq, spc = '   '))   


    # Consolidating Files
    cml.cmd('mv test.txt;test1.txt vincp')
    cml.cmd('cd vincp')
    new_fold_name = 'run_v'+str(numgroup[i])
    cml.cmd('mkdir '+new_fold_name)
    cml.cmd('mv test.txt;test1.txt '+new_fold_name)
    cml.cmd('cd ..')

lines_list.append(demark)              
iop.flat_file_write(in_path,lines_list)

iop.flat_file_write('sum_test.txt', output_lines) 

tend = time.time()

print('')
spc = '    '

if(sum_failure):
    print("Finished, 1 Error reported, see below for run details:\n")   
else:
    print("Finished! No Errors reported, see below for run details:\n")
print(spc+"The script took approx. "+str(round(tend-tstart,1))+" secs to run")
print(spc+"The script found "+str(len(numgroup))+" groupings")
if(exist):
    print(spc+"The script found an existing 'vincp' directory and overwrote it\n")
else:
    print(spc+"The script did not find an existing 'vincp' directory; one was created\n")
     