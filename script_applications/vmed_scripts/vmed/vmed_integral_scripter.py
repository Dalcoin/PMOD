import subprocess as subp

from pmod import ioparse as iop 
from pmod import strlist as strl
from pmod import mathops as mops

from pmod import vmed as vf      # not a standard pmod file; must be added for compatability with all vmed scripts

'''
vmed_integral_scripter : a script for performing rapid integral tests on the effective three-body interaction
                         pipeline developed for in-medium chiral effective field theory interactions at the 
                         fourth order of the chiral expansion. 

Note: The 'vmed.py' module must be added to the standard pmod library for compatability 

This script is to be attached in conjunction with the following file(s) and package(s):

    files:

        eff3nfn3lo1.f 
        cpot.f 
        dpot.f 
        pot.f 

    packages:
    
        pmod (python modules)

The following file(s) and directory(ies) are produced from this script:

    files:

        integral_results.txt 

    directory(ies):

'''

# jsl values 

jsls = [('0','(19,19)','singlet'),    # 0.1 
        ('0','(59,59)','singlet'),    # 0.3 
        ('0','(98,98)','singlet'),    # 0.5 
        ('0','(138,138)','singlet'),  # 0.7 
        ('0','(197,197)','singlet'),  # 1.0 
        ('0','(256,256)','singlet'),  # 1.3 
        ('0','(315,315)','singlet'),  # 1.6 
        ('0','(374,374)','singlet')]  # 1.9 

# jsls = [vf.jsl_entry('0',i,i,'singlet') for i in vf.pf_vals_20] # all jsls

# Integral values to loop over
cqfi_list = ['5.d0','10.d0','20.d0','40.d0','80.d0','120.d0']
nqftest_list = [24,32,48,64,80,96]

# overhead for replaced code
cqfi_txt = '      cqfi = '
nqftest_txt = '      nqftest = '
 

gp_vals = []
mx_vals = []

nlines = [2896, 2897]   # Lines in eff3nfn3lo1.f which contain the control values for integration, subject to change

getsf = True # Set to False for non-finite integration

for i in xrange(len(nqftest_list)):
    if(getsf):
        for j in xrange(len(cqfi_list)):
            clist = [cqfi_txt+cqfi_list[j]+'\n',nqftest_txt+str(nqftest_list[i])+'\n']
                                    
            iop.flat_file_replace('eff3nfn3lo1.f', nlines, clist)
            subp.call("f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL", shell=True)
            subp.call("./xl", shell=True)
                                         
            lines = iop.flat_file_grab('pot.d', scrub=True)        
            vals = vf.grab_jsl(lines,jsls,1)     
            for k in xrange(len(vals)):
                vals[k] = str(mops.round_uniform(float(vals[k])*vf.vmhc, pyver = '26')) 
            gp_vals.append(str(cqfi_list[j])+'  '+strl.array_to_str(vals, spc = '  '))   
        mx_vals.append(gp_vals)                  
        gp_vals = []                 
    else:
        clist = [nqftest_txt+str(nqftest_list[i])+'\n']
                                
        iop.flat_file_replace('eff3nfn3lo1.f', [nlines[1]], clist)
        subp.call("f90 $F90FLAGS -o xl -s -w cpot.f eff3nfn3lo1.f $LINK_FNL", shell=True)
        subp.call("./xl", shell=True)
                                     
        lines = iop.flat_file_grab('pot.d', scrub=True)        
        vals = vf.grab_jsl(lines,jsls,1)   
        for k in xrange(len(vals)):
            vals[k] = str(mops.round_uniform(float(vals[k])*vf.vmhc, pyver = '26')) 
        mx_vals.append(str(nqftest_list[i])+'  '+strl.array_to_str(vals, spc = '  '))         
           
for i in xrange(len(mx_vals)):    
    if(getsf): 
        out_list = strl.format_fancy(mx_vals[i], header = 'Number of Points: '+str(nqftest_list[i]), list_return = True)
        iop.flat_file_append('integral_results.txt', out_list)
    else:
        out_list = strl.format_fancy(mx_vals[i], header = 'Number of Points: '+str(nqftest_list[i]), list_return = True)
        iop.flat_file_append('integral_results.txt', out_list)
