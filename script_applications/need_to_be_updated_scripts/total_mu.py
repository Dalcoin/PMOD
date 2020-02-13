import subprocess
import time

from pmod import ioparse as iop
from pmod import mathops as mops
from pmod import pinax as px

# MAIN PROGRAM----------------------------------------------------------------------------------------------------------


reset=1
counter = 0

temp_list=[]
mu_list=[]
T = []

i_list=[1]
j_list=[1]

tstart = time.time()

par_grab = iop.flat_file_grab("par.don")
par_grab = par_grab[0]

par_str = ""
for i in range(len(par_grab)-2): par_str = par_str+str(par_grab[i])+" "

m = int(par_grab[0])
n = int(par_grab[3])
mat = int(par_grab[1])

ti = float(par_grab[4])
tf = float(par_grab[5])

for i in range(n):
    t_val = ti + float(i)*tf
    T.append(t_val)

p=n*m

subprocess.call("make",shell=True)

for j in range(0,n):
    for i in range(0,m):
        loop_grab = iop.flat_file_grab("par.don")
        loop_grab = loop_grab[0]

        inum=int(loop_grab[-2])
        ival=inum
        jnum=int(loop_grab[-1])
        jval=jnum
        
        if(counter == 0):
            i_rst = inum
            j_rst = jnum
            i_reset = str(inum) + " "
            j_reset = str(jnum) 
            input_reset = i_reset + j_reset
            input_reset = [str(par_str + input_reset)]

#   Bash
        subprocess.call("python serv.py",shell=True)
          
        file_mu = iop.flat_file_grab("mu.don",[],False,True)        
        mu = file_mu[0]
        mu_f = float(mu[0])

        print(mu_f, i, j)        
        temp_list.append(mu_f)
#        print(temp_list)
#        print(ival,jval)

        ival+=1
        i_list.append(ival-1)
        chempot_redux=str(ival)+" "+str(jval)

        cl = [par_str+chempot_redux]
        iop.flat_file_replace("par.don","par.don",[1],cl)    
        counter = counter + 1
        
    jval+=1
    ival=1
    j_list.append(jval)
    chempot_redux=str(ival)+" "+str(jval)
    cl = [par_str+chempot_redux]
    file_out = iop.flat_file_replace("par.don","par.don",[1],cl)    

    mu_list.append(temp_list)
    temp_list=[]


kf_vals = iop.flat_file_grab('kf.don',[],False,True)
xkf = []
xkfo = []
den = []
for i in range(m):
    xkfo_val = ('%.1f' % float(kf_vals[i][0]))
    xkfo.append(xkfo_val)
    kfo3 = float(xkfo[i])*float(xkfo[i])*float(xkfo[i])
    den_val = 2.0*kfo3/(3.0*mt.pi*mt.pi)
    den_val = ('%.6f' % den_val)
    den.append(den_val)

if(mat == 0):
    for i in range(m):
        xkf_val = ('%.4f' % float(kf_vals[i][0]))
        xkf.append(xkf_val)
elif(mat == 1):
    for i in range(m):
        xkf_val = (3.0*mt.pi*mt.pi*float(den[i]))**(1./3.)
        xkf_val = ('%.4f' % xkf_val)         
        xkf.append(xkf_val)    

title_str = "den       kf      kfo  "
for i in range(n):
    title_str = title_str + "mu"+str(int(T[i]))+"     "
title_str = title_str + "\n"
mu_form = px.table_trans(mu_list)
with open('out_mu.srt','w') as file_muo:
    file_muo.write(title_str)
    for i in range(m):
        str_outpt = str(den[i]) + "  " 
        str_outpt = str_outpt + str(xkf[i]) + "  " 
        str_outpt = str_outpt + str(xkfo[i]) + "  "
        for j in range(n):
            mu_val = float(mu_form[i][j])
            mu_bool = (mu_val > 0.0)
            if(mu_bool is True):
                mu_ecr = mops.round_scientific(mu_val,5)
                if(mu_val >= 10.0):
                   mu_ecr = mops.round_scientific(mu_val,4)
                if(mu_val >= 100.0):
                   mu_ecr = mops.round_scientific(mu_val,3)
                if(mu_val >= 1000.0):
                   mu_ecr = mops.round_scientific(mu_val,2)                
            else:
                mu_ecr = mops.round_scientific(mu_val,4)
                if(mu_val <= -10.0):
                   mu_ecr = mops.round_scientific(mu_val,3)
                if(mu_val <= -100.0):
                   mu_ecr = mops.round_scientific(mu_val,2) 
                if(mu_val <= -1000.0):
                   mu_ecr = mops.round_scientific(mu_val,1) 
            str_outpt = str_outpt + mu_ecr + "  "  
        str_outpt = str_outpt+"\n"          
        file_muo.write(str_outpt)
        

#file_muo = open('out_mu.srt','w')
#for k in range(0,n):
#    chem_group=mu_list[k]
#    for kk in range(0,m):
#        chemp=chem_group[kk]
#        chempo=str(chemp)+"\n"
#        file_muo.write(chempo)
#    file_muo.write(str(" \n"))
#file_muo.close()
    
if(reset == 1):
    iop.flat_file_replace("par.don","par.don",[1],input_reset)

subprocess.call("clear", shell=True)
subprocess.call("rm mu.don", shell=True)

tend = time.time()
deltat = tend - tstart
time_took = convert_time(deltat,False)

spc = '    ' 
print(spc+"Success!"+str("\n"))
print(spc+'The process took '+str(time_took)+' to finish.')
print(spc+'Check the file "out_mu.srt" for the outputs\n')

