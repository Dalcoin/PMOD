import subprocess
import numpy as np
import scipy as sp
import math as mt


def dup_check(list_to_check):
    
    #dup_check([1,1,2,3,4])
    #list_to_check must be a python 'list'
    #Checks to see if a list contains duplicates 
    #Output is a list containing an indicator of duplicaticity 
    #and the pair-wise number of duplicates 
    
# Note that dup_check(n) starting from integer 1 and incrementing by 1 will
# generate a list of the triangle numbers, also given by the binomial coefficient formula:
# (n+1)
#  (2)

    
    assert str(type(list_to_check)) == "<type 'list'>" , "Error: 'list_to_check' is not a list"
    n = len(list_to_check)
    m = 0
    for i in range(n):
        m = m + (n - i)
    dup_count = 0
    dup_list = []
    dup_val = []
    x=0
    while(x < n):
        for i in range(n-x-1):
#            print(x,i+x+1)
            check_res = list_to_check[x] == list_to_check[i+x+1]
            if(check_res == True):
                dup_count = dup_count+1
                dup_list.append(x)
        x=x+1
    if(dup_count > 0):
        dup_bool = True
    else: dup_bool = False
    return_collection = [dup_bool,dup_count]
    return return_collection



#--------------------------------------------------------------------------------------------------



def text_file_replace(file_name,file_make,grab_list,change_list):
    
#   Cette fonction contient beaucoup des lines qui sont exclures par des commentaires
#   Un jour, je vais les supprimer

    # text_file_replace('file.in','file.out',[6,7],["nint, mint  0 1","pint, oint  1 1"])
    # file_name: input file string
    # file_make: output file string
    # grab_list: list of integers with the line to be stored or changed
    # change_list: list of strings to replace the lines from grab_list

    assert str(type(file_name)) == "<type 'str'>" , "Error: 'file_name' is not a string"
    assert str(type(file_make)) == "<type 'str'>" , "Error: 'file_make' is not a string"
    assert str(type(grab_list)) == "<type 'list'>" , "Error: 'grab_list' is not an list"
    for i in range(len(grab_list)):
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: 'grab_list' is not a list of integers"
    assert str(type(change_list)) == "<type 'list'>" , "Error: 'change_list' is not an list"
    for i in range(len(change_list)):
        assert str(type(change_list[i])) == "<type 'str'>" , "Error: 'grab_list' is not a list of strings"    
    assert len(grab_list) == len(change_list) , "Error: the length of grab_list must be the same as that of change_list"
    
    with open(file_name,'r') as file_in:
        file_lines = file_in.readlines()
            
#    Ce bloc des codes est demode: n'en utilisez pas!
#    Je l'ai garde pour reference 

#    file_in = open(file_name,'r')
#    file_lines = file_in.readlines()
#    file_in.close()

#   Il faut que 'key' egale un. Si vous le change le fonction rendra rien
    key = 1
    
    length = len(file_lines)
    lines_list = []
    
#   Ce block ne sert a rien 
#    for i in range(length):
#        file_line = file_lines[i].strip("\n").strip("\r").split(" ")
#        if(key != 0):
#            lines_list.append(file_line)
    
    if (key == 1):
        for i in range(len(grab_list)):
            assert str(type(grab_list[i])) == "<type 'int'>" , "Error: grab_list must be a list of integers"
            dup_test = dup_check(grab_list)[0]
            assert dup_test == False , "Error: grab_list values must be unique"

        grab_list = [x-1 for x in grab_list]
        n = len(file_lines)
        m = len(grab_list)
        replace_list=[]
        j=0
        
        for i in range(m):
            if(grab_list[i] < n):
                replace_list.append([grab_list[i],str(change_list[i])])
        nonzero = 0
        
        with open(file_make,'w') as file_out:
            for i in range(n):
                for j in range(m):
                    if(i == int(replace_list[j][0])):
                        gellig = j
                        nonzero=1+nonzero         
                if(nonzero > 0):      
                    file_out.write(replace_list[gellig][1]+"\n")
                else:
                    file_out.write(file_lines[i])
                nonzero=0

#    Ce bloc des codes est demode: n'en utilisez pas!
#    Je l'ai garde pour information                 
                
#        file_out = open(file_make,'w')
#        for i in range(n):
#            for j in range(m):
#                if(i == int(replace_list[j][0])):
#                    gellig = j
#                    nonzero=1+nonzero                
#            if(nonzero > 0):      
#                file_out.write(replace_list[gellig][1]+"\n")
#            else:
#                file_out.write(file_lines[i])
#            nonzero=0

            

#--------------------------------------------------------------------------------------------------
            
            
def text_file_grab(file_in,file_out,grab_list,repeat,group):
    
    # text_file_grab('file.in','file.out',[6,7],False,0)
    
    # file_name: input file string
    # file_make: output file string
    # grab_list: list of integers with the lines to be parsed and printed
    # repeat:    boolean, true for option to repeat; if true then the repetition
    #            value is the first value in the grab_list, the middle values are 
    #            the shifted repeated indicies, and the last value is number of cycles
    # group:     Integer number for lines to be grouped by paragraph, 0 if no grouping

    assert str(type(file_in)) == "<type 'str'>" , "Error: 'file_in' is not a string"
    assert str(type(file_out)) == "<type 'str'>" , "Error: 'file_out' is not a string"
    assert str(type(grab_list)) == "<type 'list'>" , "Error: 'grab_list' is not an list"
    for i in range(len(grab_list)):
        assert str(type(grab_list[i])) == "<type 'int'>" , "Error: 'grab_list' is not a list of integers"     
    assert str(type(repeat)) == "<type 'bool'>" , "Error: 'repeat' is not a boolean"
    assert str(type(group)) == "<type 'int'>" , "Error: 'groupe' is not an integer"
    assert group >= 0 , "Error: 'group' is negative, group should be non-negative"
        
#    file_in_r = open(file_in,'r')
#    file_lines = file_in_r.readlines()
#    file_in_r.close()
    
    with open(file_name,'r') as file_in:
        file_lines = file_in.readlines()
    
    if(len(grab_list) == 0):
        n=len(file_lines) 
        with open(file_out,'w') as fileout:
            for i in range(n):
                fileout.write(file_lines[i])
#        fileout = open(file_out,'w')
#        for i in range(n):
#            fileout.write(file_lines[i])    
#        fileout.close()    
        return
        
    grab_list = [x-1 for x in grab_list]
        
    n = len(grab_list)
    raw_lines = []
    form_lines = []
    
    if(repeat == False):
        grab_list_check = grab_list
    else:
        grab_list_check = grab_list[1:-1]
    
    for i in range(len(grab_list_check)):
        assert str(type(grab_list_check[i])) == "<type 'int'>" , "Error: grab_list must be a list of integers"
        dup_test = dup_check(grab_list_check)[0]
        assert dup_test == False , "Error: grab_list values must be unique"
    
    if(repeat == False):
        for i in range(n):
            raw_lines.append(file_lines[grab_list[i]])
            lines = file_lines[grab_list[i]].strip("\n").strip("\r").split(" ")            
            lines = [x for x in lines if x != ''] 
            form_lines.append(lines)
        
        with open(file_out,'w') as fileout:
            if(group>0):
                fileout.write(raw_lines[i])
                if(i>0 and (i+1)%group == 0):
                    fileout.write("\n")
            else:
                for i in range(n):
                    fileout.write(raw_lines[i])
        
#        fileout = open(file_out,'w')
#        if (group > 0):
#            for i in range(n):
#                fileout.write(raw_lines[i])
#                if(i > 0 and (i+1)%group == 0):
#                    fileout.write("\n")
#        else:
#            for i in range(n):
#                fileout.write(raw_lines[i])                       
                
    if(repeat == True):  
        bnd = grab_list[0]+1
        saut = grab_list[1:-1]
        n = grab_list[-1]+1
        for i in range(n):
            for j in range(len(saut)):
                line_tag = saut[j]+bnd*i
                raw_lines.append(file_lines[line_tag])
                lines = file_lines[line_tag].strip("\n").strip("\r").split(" ")            
                lines = [x for x in lines if x != '']                 
                form_lines.append(lines)
        with open(file_out,'w') as fileout:
            if(group>0):
                for i in range(n*len(saut)):
                    fileout.write(raw_lines[i])
                    if(i>0 and (i+1)%group == 0):
                        fileout.write("\n")
            else: 
                for i in range(n*len(saut)):
                    fileout.write(raw_lines[i])
                    
#        fileout = open(file_out,'w')
#        if (group > 0):
#            for i in range(n*len(saut)):
#                fileout.write(raw_lines[i])
#                if(i>0 and (i+1)%group == 0):
#                    fileout.write("\n")    
#        else:
#            for i in range(n*len(saut)):
#                fileout.write(raw_lines[i])       
        
#    fileout.close()        
    

#--------------------------------------------------------------------------------------------------
    
def list_file_grab(file_in,grab_list,repeat,formater):
    
    # list_file_grab('file.in',[6,7],False,True)
    
    # file_name: input file string
    # grab_list: list of integers with the lines to be parsed and printed
    #            input [] for the entire file to be grabed.
    # repeat:    boolean, true for option to repeat; if true then the repetition
    #            value is the first value in the grab_list, the middle values are 
    #            the shifted repeated indicies, and the last value is number of cycles
    # formater:  Boolean, True if returned as scrubbed list, else a raw list is returned  
    
    assert str(type(file_in)) == "<type 'str'>" , "Error: 'file_in' is not a string"
    assert str(type(grab_list)) == "<type 'list'>" , "Error: 'grab_list' is not an list"
    assert str(type(repeat)) == "<type 'bool'>" , "Error: 'repeat' is not a boolean"
    assert str(type(formater)) == "<type 'bool'>" , "Error: 'formater' is not a boolean"

#    file_in_r = open(file_in,'r')
#    file_lines = file_in_r.readlines()
#    file_in_r.close() 
    
    with open(file_in,'r') as file_in_r:
        file_lines = file_in_r.readlines()    
    
    raw_lines = []
    form_lines = []   

    if(len(grab_list) == 0):
        n=len(file_lines)    
        if(formater == True):
            for i in range(n):
                lines = file_lines[i].strip("\n").strip("\r").split(" ")            
                lines = filter(None,lines) 
                form_lines.append(lines)
            return form_lines
        else:
            for i in range(n):
                raw_lines.append(file_lines[i])    
            return raw_lines       
        
    grab_list = [x-1 for x in grab_list]    
    n = len(grab_list)
    
    if(repeat == False):
        grab_list_check = grab_list
    else:
        grab_list_check = grab_list[1:-1]
    
    for i in range(len(grab_list_check)):
        assert str(type(grab_list_check[i])) == "<type 'int'>" , "Error: grab_list must be a list of integers"
        dup_test = dup_check(grab_list_check)[0]
        assert dup_test == False , "Error: grab_list values must be unique"
    
    if(repeat == False):
        for i in range(n):
            raw_lines.append(file_lines[grab_list[i]])
            lines = file_lines[grab_list[i]].strip("\n").strip("\r").split(" ")            
            lines = filter(None,lines) 
            form_lines.append(lines)
        if(formater == True):
            return form_lines
        else:
            return raw_lines                               
                
    if(repeat == True):  
        assert len(grab_list) > 2, "Error: grab_list must take at least three values"
        bnd = grab_list[0]+1
        saut = grab_list[1:-1]
        n = grab_list[-1]+1
        for i in range(n):
            for j in range(len(saut)):
                line_tag = saut[j]+bnd*i
                raw_lines.append(file_lines[line_tag])
                lines = file_lines[line_tag].strip("\n").strip("\r").split(" ")            
                lines = filter(None,lines)          
                form_lines.append(lines)            
        if(formater == True):
            return form_lines
        else:
            return raw_lines                      

#--------------------------------------------------------------------------------------------------
        
def int_list(n):return [x+1 for x in range(n)]

#--------------------------------------------------------------------------------------------------

def convert_time(tt,numeric_bool):
    import math as mt
    
    global secs_counter
    global mins_counter
    global hrs_counter
    global days_counter
    
    def secs_counter(tt,numeric_bool):
        if(numeric_bool == False):
            if(tt == 1.):
                return str(str(int(tt))+' sec')
            else:
                return str(str(tt)+' secs')        
        else:
            return [tt]
        
    def mins_counter(tt,numeric_bool):        
        mins = mt.floor(tt/60.) 
        secs = tt - mins*60
        secs = secs_counter(secs,numeric_bool)
        if(numeric_bool == False):    
            if(mins == 1):
                return str(str(int(mins))+' min'+' & '+str(secs))
            else:
                return str(str(int(mins))+' mins'+' & '+str(secs))
        else:
            return [mins,secs[0]]

    def hrs_counter(tt,numeric_bool):           
        hrs = mt.floor(tt/(3600))
        secs_left = tt - hrs*3600
        mins = mins_counter(secs_left,numeric_bool)
        if(numeric_bool == False): 
            if(hrs == 1):
                return str(str(int(hrs))+' hr, ' + str(mins))
            else:
                return str(str(int(hrs))+' hrs, ' + str(mins))
        else: 
            return [hrs,mins[0],mins[1]]
        
        
    def days_counter(tt,numeric_bool):
        days = mt.floor(tt/86400)
        secs_left = tt - days*86400
        hrs=hrs_counter(secs_left,numeric_bool)
        if(numeric_bool == False):
            if(days == 1):
                return str(str(int(days))+' day, ' + str(hrs))
            else:
                return str(str(int(days))+' days, ' + str(hrs)) 
        else:
            return [days,hrs[0],hrs[1],hrs[2]]        
        
    assert str(type(tt)) == "<type 'int'>" or str(type(tt)) == "<type 'float'>"  or \
                                                  str(type(tt)) == "<type 'long'>", "Error: 'time' is not a number"
    assert str(type(numeric_bool)) == "<type 'bool'>" , "Error: 'numeric_bool' is not a boolean"
        
    tt = float(tt)
    if(tt < 0):
        tt=-1.*tt

    if (tt < 1.):
        return str(str(tt)+" secs")
    elif (tt< 60.):
        return secs_counter(tt,numeric_bool)
    elif (tt < 3600):
        return mins_counter(tt,numeric_bool)
    elif (tt < 86400):
        return hrs_counter(tt,numeric_bool)        
    else:
        return days_counter(tt,numeric_bool)

#--------------------------------------------------------------------------------------------------

def list_matrix_trans(n):
    
    assert str(type(n)) == "<type 'list'>" , "Error: 'n' is not a list"
    
    len_vals=[]
    for i in range(len(n)):
        len_vals.append(len(n[i]))
    if(len(len_vals) > 1):
        x = len(len_vals)
        assert int(dup_check(len_vals)[1]) == int((x)*(x-1)/2), "Error: 'n' is not a proper matrix"
    old_row_len = len(n[0])
    old_col_len = len(n)
    new_row_set=[]
    new_row=[]
    for i in range(old_row_len):
        for j in range(old_col_len):
            new_row.append(n[j][i])
        new_row_set.append(new_row)
        new_row = []
    return new_row_set

def list_irr_matrix_trans(n):
    
    assert str(type(n)) == "<type 'list'>" , "Error: 'n' is not a list"
    
    len_vals=[]
    for i in range(len(n)):
        len_vals.append(len(n[i]))
        if(i>0):
            assert len_vals[i] <= len_vals[i-1], "Error: The input list is incompatible with this function"
    old_col_len = len(n)
    old_row_len = len(n[0])
    m = len(n[0])
    new_row_set=[]
    new_row=[]
    x = 0
    j = 0
    for i in range(old_row_len):
        for j in range(old_col_len):
            if(len_vals[j]-1 >= i ):
#                print(j,i,len_vals[j])
#                print(n[j][i])
                new_row.append(n[j][i])
        new_row_set.append(new_row)
        new_row=[]
    return new_row_set
    

def odfm(x,d):
    x = float(x)
    fm = '%.' + str(int(d)) + 'f'
    x = fm % x
    return str(x)


# MAIN PROGRAM----------------------------------------------------------------------------------------------------------

import time

reset=1
counter = 0

temp_list=[]
mu_list=[]
T = []

i_list=[1]
j_list=[1]

tstart = time.time()

par_grab = list_file_grab("par.don",[],False,True)
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
        loop_grab = list_file_grab("par.don",[],False,True)
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
#        subprocess.call("make",shell=True)
        subprocess.call("python serv.py",shell=True)
          
        file_mu = list_file_grab("mu.don",[],False,True)        
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
        text_file_replace("par.don","par.don",[1],cl)    
        counter = counter + 1
        
    jval+=1
    ival=1
    j_list.append(jval)
    chempot_redux=str(ival)+" "+str(jval)
    cl = [par_str+chempot_redux]
    file_out = text_file_replace("par.don","par.don",[1],cl)    

    mu_list.append(temp_list)
    temp_list=[]


kf_vals = list_file_grab('kf.don',[],False,True)
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
mu_form = list_irr_matrix_trans(mu_list)
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
                mu_ecr = odfm(mu_val,5)
                if(mu_val >= 10.0):
                   mu_ecr = odfm(mu_val,4)
                if(mu_val >= 100.0):
                   mu_ecr = odfm(mu_val,3)
                if(mu_val >= 1000.0):
                   mu_ecr = odfm(mu_val,2)                
            else:
                mu_ecr = odfm(mu_val,4)
                if(mu_val <= -10.0):
                   mu_ecr = odfm(mu_val,3)
                if(mu_val <= -100.0):
                   mu_ecr = odfm(mu_val,2) 
                if(mu_val <= -1000.0):
                   mu_ecr = odfm(mu_val,1) 
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
    text_file_replace("par.don","par.don",[1],input_reset)

subprocess.call("clear", shell=True)
subprocess.call("rm mu.don", shell=True)

tend = time.time()
deltat = tend - tstart
time_took = convert_time(deltat,False)
print("Success!"+str("\n"))
print('The process took '+time_took+' to finish.'+"\n")
print('Check the file "out_mu.srt" for the outputs\n')

