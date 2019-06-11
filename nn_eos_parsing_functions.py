### Scripting Program for the following nucleon-nucleon potential programs:

### Still in progress...

# 2NF + 3NF (T != 0)

#nnsumneutemp.f
#mattemp.f

#nnsumtemp.f
#mattmp.f

# n2lo450new.f
# n2lo500new.f
# n3lo450new.f
# n3lo500new.f
# n4lo450new.f
# n4lo500new.f


# 2NF + 3NF (T = 0)

#nnsumneu.f
#mattemp.f

#nnsum.f
#mattmp.f

# n2lo450new.f
# n2lo500new.f
# n3lo450new.f
# n3lo500new.f
# n4lo450new.f
# n4lo500new.f


#Instructions: 

#If temperature is zero:
#
#   Set temp = False
#
#Else if temperture is nonzero:
#
#   Set temp = True

import subprocess
import time
import numpy as np
import scipy as sp
import math as mt

ti = time.time()
check = nn_eos_scripter(1,1)
tf = time.time()
deltat = tf - ti
time_took = convert_time(deltat,False)

log_file = open('log_file.txt',w)
if(check == True):
    log_file.write("Success!"+str("\n"))
    log_file.write('The process took: '+time_took+' to finish.'+"\n")
else(check == False):
    log_file.write("Failure..."+str("\n"))
    log_file.write('The process took: '+time_took+' to finish.'+"\n")


def nn_eos_scripter(mat,temp):
    
    par_lines = list_file_grab('ins.don',[],False,True)
    par_vals = par_lines[0]
    
    n = int(par_vals[0])
    mat = int(par_vals[1])

    inum=int(12)
    jnum=int(18)

    filegrab = open('tot_out.etr','w')

    for i in range(n): 
        
        lines = list_file_grab('matin.d',[],False,False)
        l13 = par_lines[i+1]
    
        blk5 = str('     ')
        blk4 = str('    ')
        blk3 = str('   ')
        blk2 = str('  ')
        blk10 = str(blk5+blk5)
        
        if(temp != 0):
            if (mat == 1):
                string_13 = str(blk10+str(l13[0])+blk5+str(l13[1])+"   "+str(l13[2])+"    "+str(l13[3])+blk5+str(l13[4])+blk5+" "+str(l13[5])+"\n")
                string_19 = str(str('kfUAWSTmu')+'   '+str(l13[0])+'   '+str(l13[1])+"   "+str(l13[2])+"    "+str(l13[3])+blk5+str(l13[4])+"\n")
            elif (mat == 0):
                string_13 = str(blk10+str(l13[0])+"       "+str(l13[1])+"  "+str(l13[2])+"  "+str(l13[3])+blk10+str(l13[4])+blk4+str(l13[5])+"\n")
                string_19 = str(str('kfUAWSTmu')+'   '+str(l13[0])+'     '+str(l13[1])+"  "+str(l13[2])+"  "+str(l13[3])+blk10+str(l13[4])+"\n")
            else:
                print("mat' must be either 1 or 0!")
                return False        
            text_file_replace('matin.d','matin.d',[13,18],[str(string_13),str(string_18)]) 
        else:
            return False
            
#        subprocess.call("./tnn.sh")
        subprocess.call("./xl",shell=True)

        raw_out = list_file_grab('matout.d',[],False,False)

        for j in range(len(raw_out)):
            filegrab.write(raw_out[j])
        filegrab.write(str("\n"))
    filegrab.close()
    return True

