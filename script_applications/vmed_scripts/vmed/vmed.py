import subprocess               
import re                       
                                
import strlist as strl
import ioparse as iop 
import mathops as mops
import pinax   as px  

'''
    --------
    | vmed |
    --------

    Note: 'vmed.py' must be added to the pmod package for 
          vmed scripts to function. 'vmed.py' is not a 
          standard pmod module

    A list of relevent functions and constants to optimize working with 
    the effective 3NF nuclear potential pipeline. Optimized for working 
    at the third order of the chiral expansion.

    list of functions:

        grab_jsl : allows array of texts to be searched for jsl patterns,
                   corrosponding to an input potential matrix in jsl form.

    available constants:

        pi   : standard pi [12-digits]
        hc   : nuclear conversion constant [6-digits] 
        vmhc : nuclear potential conversion from (MeV^-2) to (fm) 
        mnuc : standard nucleon mass energy (MeV) [6-digits]
        mneu : neutron mass energy (MeV) [10-digits]
        mprt : proton mass energy (MeV) [13-digits]
        melc : electron mass energy (MeV) [9-digits]
        mmun : muon mass energy (MeV) [12 -digits]           
        
'''


match = '(-?\d\.\d*D.\d{2})'
v_line = re.compile(match)

def jsl_entry(j,p1,p2,t):
    '''
    jsl_entry
     
    j => {0, 1, 2, 3}
    p1, p2 - A python numeric or string corrosponding to a numeric 
    t => {'singlet', triplet', 'V++', 'V--', 'V+-', 'V-+'}
    '''

    entry = (str(j),'('+str(p1)+','+str(p2)+')',str(t))
    return entry

def grab_jsl(file_text, list_jsl_match, round_form, round_length=None):
    
    def __parse_tfile__(file_text):

        j_codes = [0,1,2,3]
        for i in file_text:
            split = i.split()
            try:
                test = int(float([j for j in split if j][0]))
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
        

    jsl_codes = {0:'singlet',1:'triplet',2:'V++',3:'V--',4:'V+-',5:'V-+'}
      
    Total_Out_List = []
    nos_jsl = []    
    finalvals = []
    
    for i in list_jsl_match:
        for j,k in __parse_tfile__(file_text):
#            print str(i)+" --- "+str(j)    # Debug printing
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


#################################
#   functions for vmed_format   #
#################################

# heading function for vmed_format

def head_construct(self, eflt, latex, nfile):
    
    head_match = '\d\d*'
    head_compile = re.compile(head_match)
    eflt.sort(key = lambda y: int(head_compile.findall(y)[0]))
    sp_7 = '       '
    sp_6 = '      '
    sp_5 = '     '
    sp_4 = '    '
    
    try: 
        if(latex == 1):
            head = 'j & (x,y) & State & '
        else:
            head = 'j    q1  q2    State    '

        count = 0
        for i in eflt:
            head_num = head_compile.findall(i)

            if(latex == 1):  
                if(count<nfile-1):
                    head = head+'Eq.'+str(head_num[0])+' & '
                else:
                    head = head+'Eq.'+str(head_num[0])+'\\\\'
                count += 1
            else:
                if(count<nfile-1):
                    if(int(head_num[0]) < 10):
                        head = head+'Eq.'+str(head_num[0])+sp_7
                    elif(int(head_num[0]) < 100):
                        head = head+'Eq.'+str(head_num[0])+sp_6
                    elif(int(head_num[0]) < 1000):
                        head = head+'Eq.'+str(head_num[0])+sp_5
                    else:
                        head = head+'Eq.'+str(head_num[0])+sp_4
                else:
                    head = head+'Eq.'+str(head_num[0])
                count += 1   
    except:
        head = ''

    return head



# Captures the s (first 4) and p (last 4) waves corrosponding to the ones in the reference paper [*}

def holt_jsl_20(p): 

    jsl_out = [
        ('0','('+str(p)+','+str(p)+')','singlet'),
        ('1','('+str(p)+','+str(p)+')','V--'),
        ('1','('+str(p)+','+str(p)+')','V++'),
        ('1','('+str(p)+','+str(p)+')','V-+'),
        ('1','('+str(p)+','+str(p)+')','singlet'),
        ('0','('+str(p)+','+str(p)+')','V++'),
        ('1','('+str(p)+','+str(p)+')','triplet'),
        ('2','('+str(p)+','+str(p)+')','V--')
    ]
     
    return jsl_out  


# Constants
     
pi = 3.14159265359     # pi - 12 digits 
hc = 197.327           # hc - Standard Nuclear Conversion Constant
                       
mnuc = 938.918         # Nucleon Mass-Energy 
mneu = 939.5656328     # Neutron Mass-Energy   
mprt = 938.2720881629  # Proton Mass-Energy  
melc = 0.51099895      # Electron Mass-Energy 
mmun = 105.658375523   # Muon Mass-Energy    
                       
vmhc = pi*hc*mnuc/2.0  # (pi/2) hc [MeV^-2] -> fm Conversion Constant     
 

kf_vals_20 = [i*0.1 for i in xrange(1,21)]  
qf_vals_20 = [hc*float(i) for i in kf_vals_20]
pf_vals_20 = [int(i) for i in qf_vals_20]
  
