import subprocess
import re

from pmod import strlist as strl
from pmod import ioparse as iop
from pmod import mathops as mops
from pmod import pinax   as px


def grab_jsl(file_text, list_jsl_match, round_form, round_length=None):
    
    def __parse_tfile__(file_text):
    
        for i in file_text:
            split = i.split()
            try:
                test = float([j for j in split if j][0])
            except:
                test = -1
            if(test in j_codes):
                j = int(float(split[0].replace('D','E')))
                x = int(float(split[1].replace('D','E')))
                y = int(float(split[2].replace('D','E')))
                xy_val = str('('+str(x)+','+str(y)+')')
                j_val  = str(j)
            else:
                temp=v_line.findall(i)
                temp=[k.replace('D','E') for k in temp]
                for k in range(len(temp)):
                    jsl_val = jsl_codes[k]
                    jsl_inst = (j_val,xy_val,jsl_val)
                    yield jsl_inst, float(temp[k])    
        
    j_codes = [0,1,2,3]
    jsl_codes = {0:'singlet',1:'triplet',2:'V++',3:'V--',4:'V+-',5:'V-+'}

    Total_Out_List = []
    nos_jsl = []
    
    finalvals = []
    
    for i in list_jsl_match:
        for j,k in __parse_tfile__(file_text):
            if(i == j):
                finalvals.append(k)

    for i in range(len(finalvals)):
        if(round_form == 1):
            if(round_length == None or round_length < 7):
                sticky = mops.round_scientific(float(finalvals[i]),9,'26')
            else:
                sticky = mops.round_scientific(float(finalvals[i]),round_length,'26')
        else:
            sticky = finalvals[i]
        finalvals[i] = sticky
    
    return finalvals
    
    
        
match = '(-?\d\.\d*D.\d{2})'
v_line = re.compile(match)    

hc = 197.33
vmhc = 345845.245781



kf_vals = [i*0.1 for i in xrange(1,21)]
qf_vals = [hc*float(i) for i in kf_vals]
qf_pair = zip(strl.array_nth_index(qf_vals,2),strl.array_nth_index(qf_vals,2,inverse_filter=True))

n = len(qf_pair)
total_vals_list_1 = []
total_vals_list_2 = []


for i in range(n):

    q1_str = '      q(1)='+str(qf_pair[i][0])+'d0'
    q2_str = '      q(2)='+str(qf_pair[i][1])+'d0'    
    
    double1 = '('+str(int(qf_pair[i][0]))+','+str(int(qf_pair[i][0]))+')'
    double2 = '('+str(int(qf_pair[i][1]))+','+str(int(qf_pair[i][1]))+')'

    
    list_jsl_match = [
        ('0',double1,'singlet'),
        ('1',double1,'V--'),
        ('1',double1,'V++'),
        ('1',double1,'V-+'),
        ('0',double2,'singlet'),
        ('1',double2,'V--'),
        ('1',double2,'V++'),
        ('1',double2,'V-+'),
        ('1',double1,'singlet'),
        ('0',double1,'V++'),
        ('1',double1,'triplet'),
        ('2',double1,'triplet'),
        ('1',double2,'singlet'),
        ('0',double2,'V++'),
        ('1',double2,'triplet'),
        ('2',double2,'triplet'),
    ]
      
    iop.flat_file_replace('cpot.f', [58,59], [q1_str,q2_str])
    subprocess.call("f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL", shell=True)
    subprocess.call("./xl", shell=True)
    
    flines = iop.flat_file_grab('pot.d')
    lines = strl.array_filter_spaces(flines[-70:])
    
    run_vals = grab_jsl(lines, list_jsl_match, round_form = 1)

    part1 = run_vals[:4]
    part2 = run_vals[4:8]
    part3 = run_vals[8:12]
    part4 = run_vals[12:16]

    total_vals_list_1.append(part1)
    total_vals_list_1.append(part2)
    total_vals_list_2.append(part3)
    total_vals_list_2.append(part4)
    
val_table_1 = px.table_trans(total_vals_list_1)
val_table_2 = px.table_trans(total_vals_list_2)


for i in range(len(val_table_1)):
    val_table_1[i] = [float(j)*vmhc for j in val_table_1[i]]
for i in range(len(val_table_2)):
    val_table_2[i] = [float(j)*vmhc for j in val_table_2[i]]

val_table_1.insert(0,kf_vals)
val_table_1 = px.table_trans(val_table_1)

val_table_2.insert(0,kf_vals)
val_table_2 = px.table_trans(val_table_2)

for i in range(len(val_table_1)):
    val_table_1[i] = strl.array_to_str(val_table_1[i], spc = '  ')
for i in range(len(val_table_2)):
    val_table_2[i] = strl.array_to_str(val_table_2[i], spc = '  ')
    
iop.flat_file_write('twelve_run.txt',val_table_1,par = True)
iop.flat_file_write('thirteen_run.txt',val_table_2,par = True)