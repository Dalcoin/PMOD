import subprocess as subp
import re

from pmod import strlist as strl
from pmod import ioparse as iop
from pmod import mathops as mops
from pmod import pinax   as px
from pmod import cmdline as cl


def grab_jsl(file_text, list_jsl_match, round_form, round_length=None):
    '''
    file_text      : String; name of the 'pot.d' file
    list_jsl_match : List  ; list of formated tuples
    round_form     : Int   ; 1 = True, anything else = False 
    round_length   : None by default (else an integer greater than 7)        

    Description :
    
        Extracts V matrix values from a 'pot.d' formated file according to 
        the standard output, for a given J and momenta pair (Q1,Q2): 
      
            singlet  triplet  V++  V--  V+-  V-+

        The values are returned as a list of floats
    ''' 
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


def v_group():

    cmv = cl.path_parse('linux')
    
    # Get path of file storing the contribs
    success, file_path_list = cmv.cmd("dir contribs.txt")
    lines_list = iop.flat_file_grab(file_path_list[0], [], scrub = True)
    
    # Pair up V line with fun. line 
    main = strl.array_nth_index(lines_list, 2)
    comp = strl.array_nth_index(lines_list, 2, True)
    paired = map(lambda x,y: [x,y], main,comp)
        
    ### Group V contribs by number
    ngroup = []
    lngroup = []
    numgroup = []
    setn = -1
    for i in paired:
        get = i[0]
        vn = strl.str_to_list(get,filtre=True)[1]
        num = int(vn[1:])
        if(setn == num):
            lngroup.append(i)
        else:
            numgroup.append(num)
            ngroup.append(lngroup)
            lngroup = []
            lngroup.append(i)
            setn = num        
    ngroup = filter(None,ngroup)
    
    for i in range(len(ngroup)):
        ngroup[i] = strl.array_flatten(ngroup[i],safety=False)    

    return numgroup, ngroup
    

def p_run_loop(qf_pair):

    total_vals_list_1 = []
    total_vals_list_2 = []

    n = len(qf_pair)
    
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
        subp.call("f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL", shell=True)
        subp.call("./xl", shell=True)
        
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
    
    return val_table_1, val_table_2   


########
# MAIN #
########  

# Set-up regex match for parsing V-values
match = '(-?\d\.\d*D.\d{2})'
v_line = re.compile(match)  

# Constants  

hc = 197.33            # Standard Nuclear Conversion Constant
vmhc = 345845.245781   # ??? V MeV^-2 Conversion Constant

# Set-up P values 
kf_vals = [i*0.1 for i in xrange(1,21)]
qf_vals = [hc*float(i) for i in kf_vals]
qf_pair = zip(strl.array_nth_index(qf_vals,2),strl.array_nth_index(qf_vals,2,inverse_filter=True))
    

# Get V groupings
numgroup, ngroup = v_group()

cmv = cl.path_parse('linux')

success, in_path_list = cmv.cmd("dir dpot1.d")
in_path = in_path_list[0]
lines_list = iop.flat_file_grab(in_path, [])
demark = lines_list[-1]
lines_list = lines_list[:-1]

# Run P loop 
for i in range(len(ngroup)):
    
    # Add new V-vals generator
    new_lines = list(lines_list)
    for j in ngroup[i]:
        val = j+'\n'
        new_lines.append(val)
    new_lines.append(demark)   
    iop.flat_file_write(in_path,new_lines) 

    table_12, table_13 = p_run_loop(qf_pair)

    twelve_name = 'fig12_v'+str(numgroup[i])+'.txt'
    thirteen_name = 'fig13_v'+str(numgroup[i])+'.txt'
     
    iop.flat_file_write(twelve_name, table_12, par = True)
    iop.flat_file_write(thirteen_name, table_13, par = True)

    if('vincp' not in cmv.path_contain):
        cmv.cmd('mkdir vincp')
    cmv.cmd('mv '+twelve_name+';'+thirteen_name+' vincp')

print("Finished!\n")
