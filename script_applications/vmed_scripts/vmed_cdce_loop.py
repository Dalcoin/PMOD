import subprocess as subp
import sys
import math as mt

from pmod import strlist as strl
from pmod import ioparse as iop 
from pmod import vmed as vmd
from pmod import opti as opt

def eos_match(input_ea, test_ea):

    tsum = 0.0
    if(len(input_ea) == len(test_ea)):
        for i in xrange(len(input_ea)):
            tsum += abs(float(input_ea[i])-float(test_ea[i]))
        tsum=tsum/len(input_ea)
        return tsum 
    else:
        print("Error: input_ea needs to be the same length as test_ea")
        print("exiting script...")
        sys.exit() 


def cdce_min(cdce):

        cd, ce = cdce
        iop.flat_file_write("check_Eos.don",["Run..."],par=True,ptype='a+')
        iop.flat_file_write("check_Eos.don",["cd : "+str(cd),"ce : "+str(ce)],par=True,ptype='a+')
         
        input_lines = iop.flat_file_grab("sample_input.txt",scrub = True)
        parline_Dict, numline_Dict = vmd.mat_parline_parse(input_lines)    
        parline_Dict = vmd.mat_parline_dict(auto_Load = parline_Dict, cde = [cd,ce])
        parlines, numlines = vmd.mat_parline_dict_to_lines(parline_Dict,numline_Dict) 
        iop.flat_file_replace("sample_input.txt",numlines,parlines)  
          
        run_matter = "./xtest"
        subp.call(run_matter,shell=True)
            
        input_Eos = iop.flat_file_intable("matched_Eos.don")
        test_Eos = iop.flat_file_intable("test.txt")


        input_ea = input_Eos[1]
        test_ea = test_Eos[1]

        iop.flat_file_write("check_Eos.don",[str(ea) for ea in test_ea],par=True,ptype='a+')

        outval = eos_match(input_ea,test_ea)
        return outval


minimize = opt.minimize()
res = minimize.Minimize([1.25,0.60],cdce_min)
