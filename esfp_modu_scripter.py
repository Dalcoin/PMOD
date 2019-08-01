import subprocess
import time
import numpy as np
import scipy as sp
import math as mt

# Dependencies: __list_file_grab__

def esfp_modul_scripter():
    subprocess.call("f90 $F90FLAGS -o run -s -w sfp.f temp_eos_modules.f $LINK_FNL",shell=True)
    subprocess.call("./run",shell=True)
    subprocess.call("rm run",shell=True)
    
    lines_out = list_file_grab("values_sfp.srt",[],False,True)
    pars = list_file_grab("par.don",[],False,True)
    pars = pars[0]
    
    n = int(pars[0])
    mat = int(pars[1])
    ti = float(pars[2])
    tinc = float(pars[3])
    numt = int(pars[4])
    
    s = "  "
    ts=[]
    for i in range(numt):ts.append(float(ti+i*tinc))
    for i in range(numt):
        kf, den, tgroup, ea, sa, fa, prs= ([] for i in range(7))
        for j in range(n):             
            kf.append('%.4f' % float(lines_out[j+i*(2*n)][0]))
            den.append('%.4f' % float(lines_out[j+i*(2*n)][1]))
            tgroup.append(lines_out[j+i*(2*n)][2])
            ea.append('%.3f' % float(lines_out[j+i*(2*n)][3]))
            sa.append('%.3f' % float(lines_out[j+i*(2*n)][4]))
            fa.append('%.3f' % float(lines_out[j+i*(2*n)][5]))
            prs.append('%.3f' % float(lines_out[j+(2*i+1)*(n)][0]))
        with open('esfp_values.don','a+') as fileout:
            fileout.write("Kf      Den     EA      SA     FA      PRS\n")  
            fileout.write("\n")
            fileout.write("T = " + str(ts[i]) + "\n")        
            for k in range(n):
                line_str = str(kf[k])+s+str(den[k])+s+str(ea[k])+s
                line_str = line_str + str(sa[k])+s+str(fa[k])+s+str(prs[k])
                line_str = line_str+"\n"
                fileout.write(line_str)
            fileout.write("\n")
    subprocess.call("rm values_sfp.srt",shell=True) 
    print("Sequence Finished: look in 'esfp_values.don' for the results.")

                      
# Main Program

esfp_modul_scripter()
