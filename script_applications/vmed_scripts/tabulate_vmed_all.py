import re

import pmod.vmed as vf
import pmod.ioparse as iop
import pmod.strlist as strl
import pmod.cmdline as cmd


vmed_index_finder = re.compile('\d+\d*')

def tabulate_vmed_all(jv_list, group_by_vindex=True, momenta=None, print_lines=True):

    #Initialize internal command-line
    cml = cmd.PathParse('linux')
    if(cml == False):
        return False

    # Get contents of vincp (contains the eff. potentials in question) Must run 'vmed_all.py' first!
    if('vincp' not in cml.varPath_Folders):
        print("Error: no instance of 'vincp' in current (path) directory")
        return False
    vincp_path = cml.joinNode(cml.varPath,'vincp')
    vincp_content = cml.contentPath(vincp_path, objType = 'file',)

    # group by v# in order, set 'group_by_vindex = False' to ignore this command
    if(group_by_vindex):
        vincp_content = map(lambda x: (vmed_index_finder.findall(x.split('.')[0])[0],x), vincp_content)
        vincp_content.sort(key = lambda x: int(x[0]))

    # Set momenta values 
    if(momenta == None):
        plist = strl.array_nth_index(vf.pf_vals_20,5)
    elif(isinstance(momenta,(list,tuple))):
        plist = momenta
    else:
        print("Error: input variable, 'momenta', not recognized")
        return False

    jsl_list = []
    for jv in jv_list:
        j = str(jv[0])
        t = str(jv[1])
        for p in plist:
            jsl_list.append(vf.jsl_entry(j,p,p,t))

    outlines = []
    
    sp7 = '       '
    heading = 'p'+sp7+strl.array_to_str(momenta,spc='              ')+'\n'
    outlines.append(heading)
    for entry in vincp_content:
        vval = entry[0]
        filename = entry[1]
        filepath = cml.joinNode(vincp_path,filename)
        filetext = iop.flat_file_grab(filepath)
        matching_values = vf.grab_jsl(filetext, jsl_list, round_form = 1)
        outline = strl.array_to_str(matching_values, spc = '  ')
        outline = 'vmed '+str(vval)+'  '+outline+'\n'
        outlines.append(outline)
    
    if(print_lines):
        iop.flat_file_write('table_vincp',outlines)

    return outlines

# Add or modify selected 'jv' values 
#jv_list = [('0','singlet'),('0','V++'),('1','singlet'),('1','triplet'),('1','V++')]
jv_list = [('0','singlet')]

# Note you can also call : vf.partial_wave_dict 
# This dictionary translates partial waves to their corrosponding 'jv' values: e.g. 
# vf.partial_wave_dict['3p1'] = ('0','V++')


# Add or modify the selected momenta values: 'momenta = ...' 
# A list of possible values are shown below
# [19, 39, 59, 78, 98, 118, 138, 157, 177, 197, 217, 236, 256, 276, 295, 315, 335, 355, 374, 394]
# select_momenta = [19, 197, 335]
# use 'momenta=strl.array_nth_index(vf.pf_vals_20,n)' to select every nth index value; this is the default

# Future updates: function to iterate over partial wave list to generate a unique table for each wave

tabulate_vmed_all(jv_list, group_by_vindex=True, momenta=None)

