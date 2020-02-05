import subprocess
import re

from pmod import strlist as strl
from pmod import ioparse as iop
from pmod import mathops as mops
from pmod import pinax   as px

from pmod import vmed as vf


n = len(vf.pf_vals_20)

vals_list = []

for i in range(n):
    

    cmd = "f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL"
    subprocess.call(cmd, shell=True)    # Comment out if already compiled  
    subprocess.call("./xl", shell=True) # Comment out if already excecuted
    
    flines = iop.flat_file_grab('pot.d')
    lines = strl.array_filter_spaces(flines[-70:])
    
    run_vals = grab_jsl(lines, [vf.holt_jsl_20(vf.pf_vals_20[i])], round_form = 1)
    vals_list.append(run_vals)

    
val_table = px.table_trans(vals_list)

for i in range(len(val_table)):
    val_table[i] = [float(j)*vf.vmhc for j in val_table[i]]

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
