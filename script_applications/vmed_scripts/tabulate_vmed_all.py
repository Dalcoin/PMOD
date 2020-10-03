import re

import pmod.vmed as vf
import pmod.ioparse as iop
import pmod.strlist as strl
import pmod.cmdline as cmd
import pmod.mathops as mops


vmed_index_finder = re.compile('\d+\d*')

def tabulate_vmed_all(jv_list,
                      group_by_vindex=True,
                      momenta=None,
                      print_lines=True,
                      momenta_units='invfm',
                      pot_units='invmev2',
                      round_value=None,
                      digits=3,
                      espace=3,
                      pyver='2.6'):

    '''
    Inputs:

        jv_list : 'jv' formatted list

        group_by_vindex : (True) If True, output table automatically arranged by vmed number (lowest to highest)

        momenta : (None), if momenta is an array of integers, these momenta values used in jsl search

        print_lines : (True), If true, outlines are printed to a file, either way the list of strings is returned

        momenta_units : ('invfm'), options are 'invfm' or 'mev' corrosponding to Inverse Fermi and MeV^2 respectively

        pot_units : ('fm'), options are 'fm' or 'invmev2' corrosponding to Fermi and MeV respectively

    '''

    #Initialize internal command-line
    print("")
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

    if(isinstance(momenta_units,str)):
        if(momenta_units.lower() == 'invfm'):
            plist = map(lambda x: str(round(float(x)/vf.hc,2)), plist)

    pstring = ''
    for entry in plist:
        pstring = pstring + mops.space_format(entry, 12, adjust='right')
    pline = mops.space_format('p', 14, adjust='right')

    heading = pline+pstring+'\n'
    outlines.append(heading)
    outlines.append('\n')

    for entry in vincp_content:
        vval = entry[0]
        filename = entry[1]
        filepath = cml.joinNode(vincp_path,filename)
        filetext = iop.flat_file_grab(filepath)
        matching_values = vf.grab_jsl(filetext, jsl_list, round_form = 1)
        if(isinstance(matching_values,(list,tuple)) and isinstance(pot_units,str)):
            if(pot_units.lower() == 'invmev2'):
                pass
            else:
                if(not isinstance(round_value,int)):
                    matching_values = map(lambda x: str(float(x)*vf.vmhc), matching_values)
                else:
                    if(round_value > 2):
                        matching_values = map(lambda x: str(round(float(x)*vf.vmhc,round_value)), matching_values)
            matching_values = mops.sci_space_format(matching_values, digi=digits, spacing=espace, pyver=pyver)
            outline = strl.array_to_str(matching_values, spc = ' ')
            out_heading = 'vmed '+str(vval)
            out_heading = mops.space_format(out_heading, 9, adjust='right')
            outline = out_heading+"  "+outline+'\n'
            outlines.append(outline)
        elif(matching_values == False or matching_values == None):
            print('    '+"Error: parsing partial wave value failed\n")
            continue
        else:
            print('    '+"Error: unknown error when parsing partial wave\n")
            continue

    if(print_lines):
        iop.flat_file_write('table_vincp',outlines)
    return outlines

# Add or modify selected 'jv' values 
jv_list = [('0','singlet'),('0','V++'),('1','singlet'),('1','triplet'),('1','V++')]
#jv_list = [('0','singlet')]

# Note you can also call : vf.partial_wave_dict 
# This dictionary translates partial waves to their corrosponding 'jv' values: e.g. 
# vf.partial_wave_dict['3p1'] = ('0','V++')


# Add or modify the selected momenta values: 'momenta = ...' 
# A list of possible values are shown below
# [19, 39, 59, 78, 98, 118, 138, 157, 177, 197, 217, 236, 256, 276, 295, 315, 335, 355, 374, 394]
# select_momenta = [19, 197, 335]
# use 'momenta=strl.array_nth_index(vf.pf_vals_20,n)' to select every nth index value; this is the default

# Future updates: function to iterate over partial wave list to generate a unique table for each wave

tabulate_vmed_all(jv_list, group_by_vindex=True, momenta=None, round_value=4)

