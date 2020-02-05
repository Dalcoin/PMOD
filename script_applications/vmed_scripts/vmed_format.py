### Program needs to be updated to reflect changes to PMOD package

import re 
import sys 

from pmod import cmdline as cmv  
from pmod import strlist as strl 

class pot_format:

    def __init__(self, os_val, py_version):
         
        self.os = os_val         
        self.pyval = py_version
        
    # head function: 
    
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
    
    
    
    # jsl function: parsing content of 'pot.d' files 
    
    def grab_jsl(self,file_text,list_jsl_match,round_form,round_length=None):
        j_codes = [0,1,2,3]
        #xy_codes = {0:'(100,100)', 1:'(100,300)', 2:'(300,100)', 3:'(300,300)'}
        jsl_codes = {0:'singlet',1:'triplet',2:'V++',3:'V--',4:'V+-',5:'V-+'}
    
        match = '(-?\d\.\d*D.\d{2})'
        v_line = re.compile(match)
        
        Total_Out_List = []
        nos_jsl = []
    
        for i in file_text:
            if(i!='\n'):
                split = i.split()
                try:
                    test = int([j for j in split if j][0])
                except:
                    test = -1
                if(test in j_codes):
                    j = int(float(split[0].replace('D','E')))
                    x = int(float(split[1].replace('D','E')))
                    y = int(float(split[2].replace('D','E')))
                    xy_val = str('('+str(x)+','+str(y)+')')
                    j_val  = str(j)
                else:
                    line = i
                    temp=v_line.findall(line)
                    temp=[k.replace('D','E') for k in temp]
                    for k in range(len(temp)):           
                        jsl_val = jsl_codes[k]
                        if((j_val,xy_val,jsl_val) in list_jsl_match):
                            if(round_form == 1):
                                if(round_length==None or round_length<7):  
                                    if(self.pyval == '27'):     
                                        sticky = parse27.numeric_sci_format(float(temp[k]),9)
                                    if(self.pyval == '26'):     
                                        sticky = parse26.numeric_sci_format(float(temp[k]),9)
                                else:
                                    if(self.pyval == '27'):
                                        sticky = parse27.numeric_sci_format(float(temp[k]),round_length)
                                    if(self.pyval == '26'):
                                        sticky = parse26.numeric_sci_format(float(temp[k]),round_length)
                            else:
                                sticky = temp[k]
                            nos_jsl.append((j_val,xy_val,jsl_val))
                            Total_Out_List.append(sticky)
        return Total_Out_List, nos_jsl
    
    
    # Main 

    def pot_format_func(self,cust_in):
        
        #eff_file_form = 'lrt_pot_eq_4.txt' # testing purposes
        
        # Read par file:
        
        expd = '    '
        jsl_expd = ['V++','V--','V+-','V-+']
        
        pars_name = 'par.txt'
        pot_name = 'pot_list.txt'
        jsl_name = 'jsl_list.txt' 
        
        cmv_pars = cmv.path_parse(os_form=self.os,path_print=False)
        cmv_pars.cmd('cd par_files')
        par_path = cmv_pars.cmd('dir '+pars_name)
        pot_path = cmv_pars.cmd('dir '+pot_name) 
        jsl_path = cmv_pars.cmd('dir '+jsl_name)

        par_path = par_path[1][0]
        pot_path = pot_path[1][0]
        jsl_path = jsl_path[1][0]
        
        cmv_pot = cmv.path_parse(os_form=self.os,path_print=False)
        cmv_pot.cmd('cd pot_files')
                                   
        if(self.pyval == '27'):
            par_text = parse27.list_file_grab(par_path,[],False,True)
        if(self.pyval == '26'):
            par_text = parse26.list_file_grab(par_path,[],False,True)
        pars=par_text[1]
        
        multi_file = int(pars[0])
        custom_jsl = int(pars[1])
        round_form = int(pars[2])
        latex_form = int(pars[3])
        if(latex_form == 1):
            round_length = int(pars[4])
        else:
            round_length = None
        
        mf = (multi_file == 1)
        lf = (latex_form == 1)
        
        # par implement
        
        if(multi_file == 1):
            if(cust_in):
                if(self.pyval == '27'):
                    eff_file_list_text = parse27.list_file_grab(pot_path,[],False,False)
                if(self.pyval == '26'):
                    eff_file_list_text = parse26.list_file_grab(pot_path,[],False,False)
                eff_file_list_text = map(lambda x: x.strip('\n').strip('\r').strip(' '), eff_file_list_text)          
            else:
                try:
                    head_match = '\d\d*'
                    head_compile = re.compile(head_match)
                    eff_file_list_text = cmv_pot.cmd('ls')
                    eff_file_list_text = eff_file_list_text[1]
                    eff_file_list_text.sort(key = lambda y: int(head_compile.findall(y)[0]))    
                except:
                    eff_file_list_text = cmv_pot.cmd('ls')
                    eff_file_list_text = eff_file_list_text[1]
            nfile = len(eff_file_list_text)
        else:
            eff_file_list_text = [par_text[2][0].strip(' ').strip('\n').strip('\r')]  
            eff3nf_file_form = eff_file_list_text[0]
            nfile = len(eff_file_list_text)
            
        # jsl implement
            
        if(custom_jsl == 1):
            if(self.pyval == '27'):
                jsl_file_list_text = parse27.list_file_grab(jsl_path,[],False,True)
            if(self.pyval == '26'):
                jsl_file_list_text = parse26.list_file_grab(jsl_path,[],False,True)      
            jsl_file_list_text = map(lambda x: tuple(x), jsl_file_list_text)
            list_jsl_match = jsl_file_list_text
        else:
            list_jsl_match = [
            ('0','(100,100)','singlet' ),   
            ('0','(100,300)','V++' ),
            ('0','(300,300)','V++' ),
            ('1','(100,100)','singlet' ),
            ('1','(300,100)','triplet' ),  
            ('1','(300,300)','V+-' ),
            ('2','(100,300)','triplet' ),
            ('2','(300,100)','V--' ),
            ('2','(300,300)','V-+' ),
            ('3','(100,300)','singlet' ),
            ('3','(100,300)','V--' ),
            ('3','(100,300)','V+-' )]    
            
        # fin-list construction    
        
        list_of_lists = []
        for i in eff_file_list_text:
            
            # Read file eff3nfn3lo file(s):
            pot_file_pathway = 'dir '+i
            ftg = cmv_pot.cmd(pot_file_pathway)
            ftg = ftg[1][0]
            if(self.pyval == '27'):
                file_text = parse27.list_file_grab(ftg,[],False,False)
            if(self.pyval == '26'):
                file_text = parse26.list_file_grab(ftg,[],False,False)
            file_text = file_text[32:]
            tot_list,nos = self.grab_jsl(file_text,list_jsl_match,round_form,round_length)
            list_jsl_match = nos                    
            list_of_lists.append(tot_list)
        
        ds = '  '        
        jbunda = []
        jvals = map(lambda x: x[0], list_jsl_match)
        
        # Aligned spacing for pretty output
        count_c = 0
        switch = False
        for i in jvals:
            if(count_c == 0):
                keeprun = i 
                jbunda.append(str(keeprun)+' ')
            else:
                if(i == keeprun):
                    jbunda.append(ds)
                else:
                    jbunda.append(str(i)+' ')
                    keeprun = i
            count_c+=1
        
        # Vectorizing space for output 
        xy_list = map(lambda x: x[1],list_jsl_match)
        state_list = map(lambda x: x[2],list_jsl_match)
        for i in range(len(state_list)):
            if(state_list[i] in jsl_expd):
                state_list[i] = state_list[i]+expd
        
        # Output data list (needs to be transformed)
        list_to_trans = []        
        list_to_trans.append(jbunda)
        list_to_trans.append(xy_list)
        list_to_trans.append(state_list)
        for i in list_of_lists:
            list_to_trans.append(i)
         
        #Finialized list (transformed data set)   
        if(self.pyval == '27'):
            fin_list = parse27.list_irr_matrix_trans(list_to_trans)
        if(self.pyval == '26'):
            fin_list = parse26.list_irr_matrix_trans(list_to_trans)        
            
        #print list construction    
        print_list = []                
        head = self.head_construct(eff_file_list_text,latex_form,nfile)
        print_list.append(head)                    
        if(head != '' and lf):            
            print_list.append('\\hline')
        
        if(lf):
            spc = ' & '
        else:
            spc = '  '
        
        for i in fin_list:
            fin_str = ''
            count = 0
            temp_len = len(i)
            for j in i:
                if(count < temp_len-1):
                    fin_str = fin_str+str(j)+spc
                else:
                    if(lf):
                        fin_str = fin_str+str(j)+' \\\\'
                    else:
                        fin_str = fin_str+str(j)
                count +=1
            print_list.append(fin_str)

        return print_list


def print_potd_format(os_choice, py_version):
    '''
    os_choice = 'windows' or 'linux'
    '''

    if(py_version != '26' and py_version != '27'):
        raise ValueError

    formater = pot_format(os_choice,py_version)      
    list_to_print = formater.pot_format_func(False)
    if(py_version == '27'):
        parse27.text_file_print('table_pot.txt',list_to_print,True)
    if(py_version == '26'):
        parse26.text_file_print('table_pot.txt',list_to_print,True)
    print("Formatting completed")
