### Scripting Program for repeated runs of the following nucleon-nucleon potential programs:

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


import subprocess
import time
import numpy as np
import scipy as sp
import math as mt

def nn_eos_scripter():
    
    # 'par_ins.don' e.g. 
    par_values = list_file_grab('par_ins.txt',[1],False,True)  
    val_line = par_values[0]
    
    assert len(val_line) > 2, "Error: two few parameters in 'par_ins.don' "
    assert len(val_line) < 4, "Error: two many parameters in 'par_ins.don' "
    
    #Universal Parameter Values
    mat = int(val_line[0])
    temp = int(val_line[1])
    test_bool = bool(int(val_line[2]))
    
    #----------------------If the Test Boolean is True:----------------------#
    
    if(test_bool == True):
        
        test_lines = list_file_grab('test_ins.txt',[],False,False)
        
        # Testing parameters
        test_lines_pars = test_lines[0].strip("\n").strip("\r").split(" ")  
        group = int(test_lines_pars[0])
        num_groups = int(test_lines_pars[1])
        
        # Testing line replacment lists
        test_lines_nums = test_lines[1].strip("\n").strip("\r").split(" ")  
        g_list = []
        
        c_list = []
        c_list_in = []
        
        assert len(test_lines_nums) == group, "Error: replacment group number is not equal to the number of test lines"
        for i in range(group):
            g_list.append(int(test_lines_nums[i]))
                        
        for i in range(num_groups):
            for j in range(group):
                c_list_in.append(test_lines[j+2+(i*group)].strip("\n").strip("\r"))
            c_list.append(c_list_in)
            c_list_in = []
            
                        
        for i in range(num_groups):
            
            text_file_replace('matin.d','matin.d',g_list,c_list[i])
            subprocess.call("./xl",shell=True)
            raw_out = list_file_grab('matout.d',[],False,False)

            with open('tot_out.etr','a+') as filegrab:
                for j in range(len(raw_out)):
                    filegrab.write(raw_out[j])
                filegrab.write(str("\n"))
                
        return True
    
    #----------------------If the Test Boolean is False:----------------------#
            
    val_lines = list_file_grab('val_ins.txt',[],False,True)
    val_vals = val_lines[0]
    
    n = int(val_vals[0])

    for i in range(n): 
        
        lines = list_file_grab('matin.d',[],False,False)
        l13 = val_lines[i+1]
    
        blk5 = str('     ')
        blk4 = str('    ')
        blk3 = str('   ')
        blk2 = str('  ')
        blk10 = str(blk5+blk5) 
        
        if(temp == 0):
            if (mat == 1):
                nmass = str(939.5654)
                string_13 = str(blk10+str(l13[0])+blk5+str(l13[1])+"  "+str(l13[2]))                
                string_18 = str(str('Nmass,kf')+'  '+nmass+'   '+str(l13[0]))                
                text_file_replace('matin.d','matin.d',[13,18],[str(string_13),str(string_18)]) 
            elif (mat == 0):
                nmass = str(938.918)
                string_13 = str(blk10+str(l13[0])+"       "+str(l13[1])+"  "+str(l13[2]))                
                string_18 = str(str('Nmass,kf')+'  '+nmass+'   '+str(l13[0]))       
                text_file_replace('matin.d','matin.d',[13,18],[str(string_13),str(string_18)])  
            else:
                print("mat' must be either 1 or 0!")
                return False                                                                      
        elif(temp == 1):
            if (mat == 1):
                string_13 = str(blk10+str(l13[0])+blk5+str(l13[1])+"   "+str(l13[2])+
                                "    "+str(l13[3])+blk5+str(l13[4])+blk5+" "+str(l13[5]))
                
                string_19 = str(str('kfUAWSTmu')+'   '+str(l13[0])+'   '+str(l13[1])+"   "+
                                str(l13[2])+"    "+str(l13[3])+blk5+str(l13[4]))
                text_file_replace('matin.d','matin.d',[13,19],[str(string_13),str(string_19)])
            elif (mat == 0):
                string_13 = str(blk10+str(l13[0])+"       "+str(l13[1])+"  "+str(l13[2])+
                                "  "+str(l13[3])+blk10+str(l13[4])+blk4+str(l13[5]))
                
                string_19 = str(str('kfUAWSTmu')+'   '+str(l13[0])+'     '+str(l13[1])+"  "+
                                str(l13[2])+"  "+str(l13[3])+blk10+str(l13[4]))
                text_file_replace('matin.d','matin.d',[13,19],[str(string_13),str(string_19)])
            else:
                print("'mat' must be either 1 or 0!")
                return False                     
        else:
            print("'temp' must be either a 1 or 0!")
            return False
            
#        subprocess.call("./xl",shell=True)

        raw_out = list_file_grab('matout.d',[],False,False)

        with open('tot_out.etr','a+') as filegrab:
            for j in range(len(raw_out)):
                filegrab.write(raw_out[j])
            filegrab.write(str("\n"))    
    return True


# Main Program

ti = time.time()
check = nn_eos_scripter()
tf = time.time()
deltat = tf - ti
time_took = convert_time(deltat,False)

with open('log_file.txt','w') as log_file:
    if(check == True):
        log_file.write("Success!"+str("\n"))
        log_file.write('The process took '+time_took+' to finish.'+"\n")
        log_file.write('Check the file "tot_out.etr" for the outputs\n')
        log_file.write('\n')
        log_file.write('Koreet ahe barrit, geigh ay lech ek Skorem ek kort!\n')
        log_file.write('Shair, Shairee gal rieatem!\n')
        log_file.write('\n')        
    else: 
        log_file.write("Failure..."+str("\n"))
        log_file.write('The process took: '+time_took+' to finish.'+"\n")
