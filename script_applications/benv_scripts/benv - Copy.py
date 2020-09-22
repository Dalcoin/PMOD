import sys
import os
import subprocess
import re
import time

from pmod.programStructure import progStruc

import pmod.ioparse as iop
import pmod.strlist as strl
import pmod.mathops as mops


class benv(progStruc):

    def __init__(self,
                 eos_fold_name='eos'
                 par_file_name='par.don',
                 val_file_name='nucleus.don',
                 vrb_file_name='opt_par.etr',
                 skn_file_name='skin.srt',
                 xeb_bin_name='xeb_server'
                 aux_bin_name='aux',
                 osFormat='linux',
                 newPath=None,
                 rename=True,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    ',
                 endline='\n',
                 moduleNameOverride="BENV",
                 **kwargs):

        super(benv, self).__init__(osFormat,
                                   'benv',
                                   'src',
                                   'bin',
                                   'dat',
                                   'skval.don',
                                   True,
                                   osFormat,
                                   newPath,
                                   rename,
                                   debug,
                                   shellPrint,
                                   colourPrint,
                                   space,
                                   endline,
                                   moduleNameOverride=moduleNameOverride
                                   **kwargs)

        #########################
        # File and folder names #
        #########################

        # EoS
        self.EOSFOLD = eos_fold_name
        self.EOSPATH = ''

        # Bin Files #

        # Bin Files
        self.AUXNAME = aux_bin_name
        self.AUXPATH = ''

        self.XEBNAME = xeb_bin_name
        self.XEBPATH = ''

        # Input Files
        self.PARFILE = par_file_name
        self.PARPATH = ''

        self.VALFILE = val_file_name
        self.VALPATH = ''

        # Output Files
        self.VRBFILE = vrb_file_name
        self.VRBPATH = ''

        self.SKNFILE = skn_file_name
        self.SKNPATH = ''

        ###############
        # REGEX codes #
        ###############

        # General Regex codes
        self.RE_INT      = re.compile(r'([+-]*\d+)')
        self.RE_DIGITS   = re.compile(r"(\d+)")
        self.RE_DIGITSPC = re.compile(DIGIT+r"\s+")

        self.RE_FLOAT        = re.compile(r'([+-]*\d+\.*\d*)')
        self.RE_SCIFLOAT     = re.compile(r'(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')
        self.RE_CHARFLOAT    = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+')
        self.RE_CHARSCIFLOAT = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')

        self.RE_BOOL = re.compile(r'(?:TRUE|True|true|FALSE|False|false)')
        self.RE_BOOL_FR = re.compile(r'(?:VRAI|Vrai|vrai|FAUX|Faux|faux)')

        # SKVAL regex codes
        self.INCLOOP = re.compile(r"\s*INCloop\s*:\s*(TRUE|True|true|FALSE|False|false)")
        self.AZPAIRS = re.compile(r"\s*AZpairs\s*:\s*(TRUE|True|true|FALSE|False|false)")
        self.MIRRORS = re.compile(r"\s*Mirrors\s*:\s*(TRUE|True|true|FALSE|False|false)")
        self.INITPAR = re.compile(r"\s*Initpar\s*:\s*(TRUE|True|true|FALSE|False|false)")
        self.EOSPARS = re.compile(r"\s*EOSpars\s*:\s*(TRUE|True|true|FALSE|False|false)")
        self.EOSGRUP = re.compile(r"\s*EOSgrup\s*:\s*(TRUE|True|true|FALSE|False|false)")

        self.SKVAL_HEADER = re.compile(r"#\-+([^\-]+)\-+#")
        self.SKVAL_NUCLEI = re.compile(r"\s*(\d+)\s*,\s*(\d+)")
        self.SKVAL_LOOP   = re.compile(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)")

        self.parln1 = re.compile(r"\s*"+9*self.RE_DIGITSPC+"(\d+\.+\d+)\s+(\d+)")
        self.parln2 = re.compile(r"\s*"+2*self.RE_DIGITSPC+self.RE_DIGITS)
        self.parln34= re.compile(r"\s*(\d+\.\d+)\s+(\d+\.\d+)")

        # EoS errors 
        self.EOS_SPLIT_FILE_ERROR = False
        self.EOS_FILE_FORMAT_ERROR = False 
        self.EOS_SPLIT_PARSE_ERROR = False
        self.EOS_PASS_ERROR = False
        self.INITIAL_PARS_ERROR = False

        # BENV Parameters---------------|

        # initial data 
        self.initial_pars = []
        self.initial_nucs = []
        self.initial_a = 0
        self.initial_z = 0

        # skval functionality
        self.skval_dict = {'INCloop':False,
                           'AZpairs':False,
                           'Initpar':False,
                           'Mirrors':False,
                           'EOSpars':False,
                           'EOSgrup':False}

        self.BENV_SET_BINARIES = self.init_binary([self.PARFILE, self.VALFILE, self.AUX, self.XEB])
        self.BENV_SET_PATHWAYS = self.benv_structure(**kwargs)


    ##########################
    # Initiate BENV STRUCTRE #
    ##########################

    def benv_structure(self, **kwargs):

        success = True

        eosset = self.init_fold_in_main(self.EOSFOLD, **kwargs)
        if(eosset == False):
            return False
        self.EOSPATH = self.FOLDPATH_DICT[self.EOSFOLD]

        if(self.PARFILE in self.BIN_DICT):
            self.PARPATH = self.BIN_DICT[self.PARFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.PARFILE, **kwargs)

        if(self.VALFILE in self.BIN_DICT):
            self.VALPATH = self.BIN_DICT[self.VALFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD"'", varID=self.VALFILE, **kwargs)

        if(self.AUXFILE in self.BIN_DICT):
            self.AUXPATH = self.BIN_DICT[self.AUXFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD"'", varID=self.AUXFILE, **kwargs)

        if(self.XEBFILE in self.BIN_DICT):
            self.XEBPATH = self.BIN_DICT[self.XEBFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD"'", varID=self.XEBFILE, **kwargs)

        return success


    #########
    # SKVAL #
    #########

    def parse_skval(self, lines, **kwargs):
        '''
        Converts 'skval' file lines, from 'skval.don' option file, into 'skavl data'
        This function should only be called once.
        '''

        if(self.__not_strarr_print__(lines, **kwargs)):
            return False

        # variables

        reg_dict = {'INCloop':self.INCLOOP,
                    'AZpairs':self.AZPAIRS,
                    'Initpar':self.MIRRORS,
                    'Mirrors':self.INITPAR,
                    'EOSpars':self.EOSPARS,
                    'EOSgrup':self.EOSGRUP}

        test_list = ['INCloop',
                     'AZpairs',
                     'Initpar',
                     'Mirrors',
                     'EOSpars',
                     'EOSgrup']

        line_ids = ['pars', 'loop', 'special', 'nuclei']

        n = len(lines)

        parlist = []
        nuclist = []

        # Parsing Options from SKVAL

        lab_bool = False
        par_bool = False
        nuc_bool = False
        hed_bool = False

        pairs = False

        par_trv = False
        nuc_trv = False

        par_set_dict = {'par_ln1_set' : True, 'par_ln2_set' : True, 'par_ln3_set' : True, 'par_ln4_set' : True}
        par_lgn_dict = {'par_ln1_set' : self.parln1, 
                        'par_ln2_set' : self.parln2, 
                        'par_ln3_set' : self.parln34, 
                        'par_ln4_set' : self.parln34}

        for i,line in enumerate(lines):

            if(self.SKVAL_HEADER.findall(line) != []):
                resh = self.SKVAL_HEADER.findall(line)[0].lower()
                if(resh == 'loop' or resh == 'special')
                    hed_bool = True
                elif(resh == 'nuclei'):
                    nuc_bool = True
                    if(self.skval_dict['INCLOOP']):
                        pairs = False
                    elif(self.skval_dict['AZPAIRS']):
                        pairs = True
                    else:
                        return self.__err_print__("one of the 'Loop' options should be set to 'True'", **kwargs)
                elif(resh == 'pars'):
                    par_bool = True
                else:
                    par_bool, hed_bool, nuc_bool = (False, False, False)
                continue

            if(hed_bool):
                if(any([test in line for test in test_list])):
                    for value in reg_dict:
                        key = reg_dict[value].findall(line)
                        if(key != []):
                            self.skval_dict[value] = (key[0].lower() == 'true')
                            del reg_dict[value]
            elif(par_bool):
                for entry in par_set_dict:
                    key = []
                    if(par_set_dict[entry]):
                        key = par_lgn_dict[entry].findall(line)
                    else:
                        continue
                    if(len(key) > 0):
                        parlist.append(key[0])
                        del par_set_dict[entry]
                        break
            elif(nuc_bool):
                if(pairs):
                    key = self.SKVAL_NUCLEI.findall(line)
                    if(len(key) > 0):
                        nuclist.append(key[0])
                else:
                    key = self.SKVAL_LOOP.findall(line)
                    if(len(key) > 0):
                        nuclist.append(key[0])
                    nuc_bool = False
            else:
                pass

        if(len(parlist) == 4):
            self.initial_pars = parlist

        if(len(nuclist) > 0):
            self.initial_nucs = nuclist

        if(self.skval_dict["INCLOOP"] and self.skval_dict["AZPAIRS"]):
            self.__err_print__("INCLOOP takes precedent over AZPAIRS", heading="warning", **kwargs)

        doubles = []
        loop = []

        if(pairs):
            loop_type = 'pairs'
        else:
            loop_type  = 'loop'

        output = (nuclist, loop_type, parlist)
        return output


    ##############
    # Parameters #
    ##############

    def create_parline(self, eos,
                         density = 2,
                         microscopic = True,
                         e0_rho0 = True,
                         phenom_esym = False,
                         k0 = 220,
                         rho0 = 0.16,
                         fff = 65,
                         addn=True,
                         *lengths,
                         **kwargs):

        '''
        A function which creates a 'par' formatted string

        The input consists of an eos identifier variable and optional
        variables corrosponding to each possible 'par' modifier

        '''

        if(isinstance(eos,str)):
            if(eos == '0' or eos.lower() == 'combined' or eos.lower() == 'com'):
                pos_3 = 0
            elif(eos == '1' or eos.lower() == 'seperate' or eos.lower() == 'sep'):
                pos_3 = 1
            elif(eos == '2' or eos.lower() == 'symmetric' or eos.lower() == 'sym'):
                pos_3 = 2
            else:
                pos_3 = 0
        elif(isinstance(eos,int)):
            if(eos == 0):
                pos_3 = eos
            elif(eos == 1):
                pos_3 = eos
            elif(eos == 2):
                pos_3 = eos
            else:
                pos_3 = 0
        else:
            pos_3 = 0

        if(isinstance(density,str)):
            options_list_2 = ['2pf', 'thomas-fermi', 'fermi', 'tf']
            options_list_3 = ['2py', 'folded-yukawa', 'yukawa', 'fy']
            options_list_4 = ['3pf', 'extended-thomas-fermi', 'extened-fermi','efermi', 'etf']
            if(density == '2' or density.lower() in options_list_2):
                pos_2 = 2
            elif(density == '3' or density.lower() in options_list_3):
                pos_2 = 3
            elif(density == '4' or density.lower() in options_list_4):
                pos_2 = 4
            else:
                pos_2 = 2
        elif(isinstance(density,int)):
            if(eos == 2):
                pos_2 = eos
            elif(eos == 3):
                pos_2 = eos
            elif(eos == 4):
                pos_2 = eos
            else:
                pos_2 = 2
        else:
            pos_2 = 2

        if(microscopic):
            pos_6 = 1
        else:
            pos_6 = 0

        if(e0_rho0):
            pos_7 = 1
        else:
            pos_7 = 0

        if(phenom_esym):
            pos_8 = 1
        else:
            pos_8 = 0

        if(self.__not_num_print__(k0, varID='k0', **kwargs)):
            try:
                k0 = int(k0)
            except:
                msg = "could not be converted to an integer, setting to default: 220"
                self.__err_print__(msg, varID='k0', heading='warning', **kwargs)
                k0 = 220
        else:
            k0 = int(k0)
        pos_9  = k0

        if(self.__not_num_print__(rho0, varID='rho0', **kwargs)):
            try:
                rho0 = float(rho0)
            except:
                msg = "could not be converted to a float, setting to default: 0.16"
                self.__err_print__(msg, varID='rho0', heading='warning', **kwargs)
                rho0 = 0.16
        else:
            rho0 = float(rho0)
        pos_10 = rho0

        if(self.__not_num_print__(fff, varID='fff', heading='warning', **kwargs)):
            try:
                fff = int(fff)
            except:
                msg = "could not be converted to an integer, setting to default: 65"
                self.__err_print__(msg, varID='fff', heading='warning', **kwargs)
                fff = 65
        else:
            fff = int(fff)
        pos_11  = fff

        lens = [n for n in lengths]
        n = len(lens)

        if(n == 0 and mic == 1):
            return self.__err_print__("if a microscopic eos is chosen, file length(s) must be defined", **kwargs)
        if(mic == 1 and pos_3 == 0 and n < 1):
            return self.__err_print__("if a combined eos is chosen, the file length must be defined", **kwargs)
        elif(mic == 1 and pos_3 == 1 and n < 2):
            return self.__err_print__("if a seperated eos is chosen, file lengths must be defined (e0 first, then e1)", **kwargs)
        elif(mic == 1 and pos_3 == 2 and n < 1):
            return self.__err_print__("if a SNM eos only is chosen, the file length must be defined", **kwargs)
        else:
            if(mic == 1 and (pos_3 == 0 or pos_3 == 2)):
                pos_1 = lens[0]
                pos_4 = 0
                pos_5 = 0
            elif(mic == 1 and pos_3 == 1):
                pos_1 = 0
                pos_4 = lens[0]
                pos_5 = lens[0]
            else:
                pos_1 = 0
                pos_4 = 0
                pos_5 = 0

        outlist = [pos_1,pos_2,pos_3,pos_4,pos_5,pos_6,pos_7,pos_8,pos_9,pos_10,pos_11]
        parline = strl.array_to_str(outlist)

        if(addn):
            parline += '\n'

        return parline


    def create_vallist(self, a, z, divs='64 64 64', lims='0.0 20.0', addn=True, **kwargs):
        '''
        Description : Creats a list compatible with the 'nucleus.don' file.
                      Takes a 'parline' string along with an 'A' string, 'Z' string,
                      'divs' string and 'lims' string. 'addn' add the endline character
                      to each string.
        '''

        if(__not_str_print__(divs, varID='divs', **kwargs):
            try:
                if(isinstance(divs, (list, tuple)):
                    if(len(divs) == 3):
                        divs = strl.array_to_str(divs, **kwargs)
                    else:
                        return self.__err_print__("should be a string of three integers", varID='divs', **kwargs)
                else:
                    return self.__err_print__("should be a string of three integers", varID='divs', **kwargs)
                if(divs == False):
                    return divs
            except:
                return self.__err_print__("should be a string of three integers", varID='divs', **kwargs)

        if(__not_str_print__(lims, varID='lims', **kwargs):
            try:
                if(isinstance(lims, (list, tuple)):
                    if(len(lims) == 2):
                        lims = strl.array_to_str(lims, **kwargs)
                    else:
                        return self.__err_print__("should be a string of two floats", varID='lims', **kwargs)
                else:
                    return self.__err_print__("should be a string of two floats", varID='lims', **kwargs) 
                if(lims == False):
                    return lims
            except:
                return self.__err_print__("should be a string of two floats", varID='lims', **kwargs)

        a = str(a)
        z = str(z)

        az = str(a)+'  '+str(z)

        if(addn):
            divs += '\n'
            lims += '\n'
            az += '\n'

        return [divs, lims, az]


    def write_parline(self, parline):
        '''
        Passes benv parameters to 'par.don' file located in 'bin'

        pars takes the form: [see read-me for details]

            n  nden nread n0 n1 mic isnm k0  rho0 fff
            11 2    0     19 19 0   1 0  220 0.16 65

        '''
        success = iop.flat_file_write(self.PARPATH, parline, **kwargs)
        return success


    def write_vallist(self, vallist):
        '''
        Passes benv parameters to 'nucleus.don' file located in 'bin'

        vals take the form: [see read-me for details]

            n0 n1 n2
            vi vf
            na nz

            e.g.

            64 64 64
            0.0 20.0
            208 82
        '''
        success = iop.flat_file_write(self.VALPATH, vallist, **kwargs)
        return success


    #########################
    # Output Data Formatter #
    #########################

    def format_benv_data(self, data, style = None, coerce_to_style = False):

        def __parval_to_string__(parval_obj, coerce_to_style):

            try:
                optpars, skinvals = parval_obj
            except:
                print(self.s4+"[format_benv_data] [__parval_to_string__] Error: could not coerce 'parval_obj' into two objects")
                return False

            if(optpars != False):
                pars_List = strl.str_to_list(optpars)
            else:
                pars_List = ["Error: No density functional parameters found, check convergence"]

            if(skinvals != False):
                vals_List = strl.str_to_list(skinvals)                         
            else:
                vals_List = ["Error: No found 'BENV' values found..."]       

            if(coerce_to_style):
                pass             # Place string style formatting function here
            else:
                par_String = strl.array_to_str(pars_List,spc='  ')
                val_String = strl.array_to_str(vals_List,spc='  ')

            return (par_String, val_String)


        if(isinstance(style,str)):
            style = style.lower()
        else:
            if(style == None):
                pass
            else:
                print(self.s4+"[format_benv_data] Error: input 'style' must be a string\n")
                return False

        if(style == 'os' or style == 'one-shot' or style == 'single' or style == None):
            parval_data = __parval_to_string__(data)
            if(parval_data == False):
                print(self.s4+"[format_benv_data] Error: 'data' could not be coerced into 'parval_data'\n")
                return False
            par_string, val_string = parval_data
            output = ([par_string+'\n'], [val_string+'\n'])

        elif(style == 'skval' or style == 'double' or style == 'skval-loop'):

            par_Strings = []
            val_Strings = []

            for i,entry in enumerate(data):  
                value, nucleus = entry
                             
                nucleus_String = strl.array_to_str(nucleus ,spc = '  ')+'\n'
                parval_data = __parval_to_string__(value)
                if(parval_data == False):
                    print(self.s4+"[format_benv_data] Error: 'value' could not be coerced into 'parval_data'")
                    print(self.s4+"Failure occured for the "+str(strl.print_ordinal(i))+" value of the input data\n")
                    continue
                par_string, val_string = parval_data
                par_Strings.append(par_String+nucleus_String)                            
                val_Strings.append(val_String+nucleus_String)                  

            output = (par_Strings, val_Strings)

        elif(style == 'eos', style == 'triple', style == 'eos-loope'):

            par_Strings = []
            val_Strings = []

            val_Strings.append("NR      PR      NS    CHR      BE      SEC   A   Z\n")
            val_Strings.append("\n")

            for cohort in data:

                for i,group in enumerate(cohort):

                    parval_data = group
                    if(parval_data == False):
                        print(self.s4+"[format_benv_data] Error: 'group' could not be coerced into 'entry' and 'eosid'")
                        print(self.s4+"Failure occured for the "+str(strl.print_ordinal(i))+" value of the input data\n")
                        continue

                    entry, eosid = parval_data
                    if(entry == False):
                        print(self.s4+"[format_benv_data] Error: 'entry' could not be coerced into 'data' and 'nucleus'")
                        print(self.s4+"Failure occured for the "+str(strl.print_ordinal(i))+" value of the input data\n")
                        continue

                    par_Strings.append(str(eosid)+'\n')
                    val_Strings.append(str(eosid)+'\n')   


                    par_String, val_String, nucleus = entry
                    nucleus = ["  "+strl.array_to_str(az ,spc = '  ')+'\n' for az in nucleus]
    
#                    value = (par_String, val_String)                                                               
#                    par_String, val_String = __parval_to_string__(value)
                    
                    par_list = [par for par in map(lambda x,y: x+y, par_String,nucleus)]
                    val_list = [val for val in map(lambda x,y: x+y, val_String,nucleus)]

                    for par in par_list:
                        par_Strings.append(par)
                    for val in val_list:
                        val_Strings.append(val)

                    par_Strings.append(" \n")
                    val_Strings.append(" \n")

            val_Strings.append("\n")
            val_Strings.append("\n")
            val_Strings.append("*Key\n")
            val_Strings.append("\n")
            val_Strings.append("NR  :  Neutron Radius\n")
            val_Strings.append("PR  :  Proton  Radius\n")
            val_Strings.append("NS  :  Neutron Skin\n")
            val_Strings.append("CHR :  Charge  Radius\n")
            val_Strings.append("BE  :  Binding Energy\n")
            val_Strings.append("SEC :  Sym. Eng. Coef\n")
            val_Strings.append("A   :  Mass    number\n")
            val_Strings.append("Z   :  Atomic  number\n")

            output = (par_Strings, val_Strings)

        else:
            print(self.s4+"[format_benv_data] Error: 'style' input variable not reconignized")
            return False

        return output

    #######
    # EOS #
    #######

    def collect_eos(self, **kwargs):
        '''
        Notes:

            Collects EoS from 'eos' directory 
            This function should only be called once per BENV run
        '''

        eos_dir_path = self.joinNode(self.INITIAL_PATH,self.EOSDIR)
        eos_file_list = self.contentPath(eos_dir_path)

        if(eos_file_list == None or eos_file_list == False):
            print("[collect_eos] Error: EoS files could not be found")
            self.EOS_COLLECT_ERROR = True
            return False
    
        exfiles = []
        e1files = []
        e0files = []
        egshock = []
        eoslist = []

        for i in eos_file_list:
            if('ex' in i.lower() and (('e0' not in i.lower()) and ('e1' not in i.lower()))):
                exfiles.append(i)
            elif('e1' in i.lower() and (('e0' not in i.lower()) and ('ex' not in i.lower()))):
                e1files.append(i) 
            elif('e0' in i.lower() and (('ex' not in i.lower()) and ('e1' not in i.lower()))):
                e0files.append(i)        
            else:
                egshock.append(i) 

        if(len(egshock) > 0):
            head_Text = "The following files are not valid 'eos' files:"
            strl.format_fancy(egshock,header=head_Text)                 
            
        for i in exfiles:
            file_path = self.cmv.joinNode(eos_dir_path,i)  
            ex = iop.flat_file_intable(file_path) 
            if(ex != False):
                if(len(ex) != 3):
                    print("[collect_eos] Error: the file '"+str(i)+"' does not have three equal data columns")
                    self.EOS_FILE_FORMAT_ERROR = True
                    continue 
                eoslist.append((ex,i))
            else:
                print("[collect_eos] Error: could not read table from '"+str(i)+"'")
                continue                                     
              
        for i in e0files:
             
            e1pack = False
            e1data = False
            
            if(len(i.split('e0')) == 2):
                e1add = 'e1'
                baselist = i.split('e0') 
            elif(len(i.split('E0')) == 2):
                e1add = 'E1'
                baselist = i.split('E0')                      
            else:         
                self.EOS_SPLIT_PARSE_ERROR = True 
                continue

            if(baselist[0] == ''):
                e1name = e1add+baselist[1]
                idbaseline = baselist[1]
            else:
                e1name = baselist[0]+e1add+baselist[1]
                idbaseline = baselist[0]+baselist[1]

            e0_file_path = self.cmv.joinNode(eos_dir_path,i)
            if(e1name in e1files):
                e1pack = True
                e1_file_path = self.cmv.joinNode(eos_dir_path,e1name)

            e0data = iop.flat_file_intable(e0_file_path)
            if(e1pack):
                e1data = iop.flat_file_intable(e1_file_path)

            if(not e0data):
                print("[collect_eos] Error: could not parse the file at path '"+str(e0_file_path)+"' into a table")
                self.EOS_SPLIT_PARSE_ERROR = True 
                continue 
            if(not e1data and e1pack):
                print("[collect_eos] Error: could not parse the file at path '"+str(e1_file_path)+"' into a table")
                self.EOS_SPLIT_PARSE_ERROR = True 
                continue

            if(e1pack):
                e10 = []
                try:
                    e10 = [e0data[0],e0data[1],e1data[0],e1data[1]]
                except:
                    print("[collect_eos] Error: could not parse '"+str(e0_file_path)+"' and '"+str(e1_file_path)+"' content into data")
                    self.EOS_SPLIT_PARSE_ERROR = True 
                    continue                                     
                eoslist.append((e10,idbaseline)) 
            else:
                e0 = []
                try:
                    e0 = [e0data[0],e0data[1]]
                except:
                    print("[collect_eos] Error: could not parse '"+str(e0_file_path)+"' content into data")
                    self.EOS_SPLIT_PARSE_ERROR = True 
                    continue                                     
                eoslist.append((e0,idbaseline))

        return eoslist         


    def format_eos_data(self, eos_obj, pl=[], set_pars = True):
    
        eoslist_entry, eosid = eos_obj

        output = ()
        exgp = [] 
        e0gp = [] 
        e1gp = []

        if(len(eoslist_entry) == 3):
            type = 0
            kf = eoslist_entry[0]
            e0 = eoslist_entry[1] 
            e1 = eoslist_entry[2]
            exgp = map(lambda x,y,z: strl.array_to_str([x,y,z],spc='  ',endline=True),kf,e0,e1)
            if(len(kf) == len(e0) and len(e0) == len(e1)):
                n = len(kf)
            else: 
                print("[format_eos_data] Warning: It appears that the input eos entry is improperly formatted")
                print("                           Further errors will likely occur down the pipeline")
                n = len(kf)
            if(set_pars and len(pl) == 7):
                pars = strl.array_to_str((n,pl[0],type,0,0,pl[1],pl[2],pl[3],pl[4],pl[5],pl[6]))     
                output = (((type, exgp),pars),eosid)
            else:          
                output = ((type, exgp),eosid)     
   
        elif(len(eoslist_entry) == 4):
            type = 1
            kf0 = eoslist_entry[0]
            e0  = eoslist_entry[1]
            kf1 = eoslist_entry[2]
            e1  = eoslist_entry[3]
            e0gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf0,e0)
            e1gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf1,e1)

            if(len(kf0) == len(e0) and len(kf1) == len(e1)):
                n0 = len(kf0)
                n1 = len(kf1)
            else: 
                print("[format_eos_data] Warning: It appears that the input eos entry is improperly formatted")
                print("                            Further errors will likely occur down the pipeline")
                n0 = len(kf0)
                n1 = len(kf1)
            if(set_pars and len(pl) == 7):
                pars = strl.array_to_str((0,pl[0],type,n0,n1,pl[1],pl[2],pl[3],pl[4],pl[5],pl[6]))     
                output = (((type, e0gp, e1gp),pars),'e10'+eosid)
            else:          
                output = ((type, e0gp, e1gp),'e10'+eosid) 
               
        elif(len(eoslist_entry) == 2): 
            type = 2
            kf = eoslist_entry[0]
            e0 = eoslist_entry[1]             
            e0gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf,e0)

            if(len(kf) == len(e0)):
                n = len(kf)
            else: 
                print("[format_eos_data] Warning: It appears that the input eos entry is improperly formatted")
                print("                           Further errors will likely occur down the pipeline")
                n = len(kf)
            if(set_pars and len(pl) == 7):
                pars = strl.array_to_str((n,pl[0],type,0,0,pl[1],pl[2],pl[3],pl[4],pl[5],pl[6]))     
                output = (((type, e0gp),pars),'e0'+eosid)
            else:          
                output = ((type, e0gp),'e0'+eosid)   
        else:
            print("[format_eos_data] Error: 'eoslist_entry' must be either 2, 3 or 4 numeric lists long")
            output = False          
        return output         


    def pass_eos(self, formatted_eos):

        if(not isinstance(formatted_eos,(list,tuple))):
            print("[pass_eos] Error: 'formatted_eos' must be either a list or tuple")
            self.EOS_PASS_ERROR = True
            return False 
         
        type = formatted_eos[0]  
        if(type == 0):
            eos_path = self.cmv.joinNode(self.binpath,'ex_nxlo.don') 
            success = iop.flat_file_write(eos_path, formatted_eos[1])  
            if(not success): 
                print("[pass_eos] Error: when writing to 'ex_nxlo.don'")          
        elif(type == 1):
            e0_path = self.cmv.joinNode(self.binpath,'e0_nxlo.don') 
            success = iop.flat_file_write(e0_path, formatted_eos[1])
            if(not success): 
                print("[pass_eos] Error: when writing to 'e0_nxlo.don'")   
            e1_path = self.cmv.joinNode(self.binpath,'e1_nxlo.don') 
            success = iop.flat_file_write(e1_path, formatted_eos[2])      
            if(not success): 
                print("[pass_eos] Error: when writing to 'e1_nxlo.don'")   
        elif(type == 2):
            e0_path = self.cmv.joinNode(self.binpath,'e0_nxlo.don') 
            success = iop.flat_file_write(e0_path, formatted_eos[1])  
            if(not success): 
                print("[pass_eos] Error: when writing to 'e0_nxlo.don'")                   
        else:
            print("[pass_eos] Error: 'formatted_eos' is not properly formatted")
            return False

        return True


    #######################################
    # functions dealing with benv looping #------------------------------------------------------------|
    #######################################


    def data_from_bin(self, file_Name, first_Line, number_Lines = 1):

        '''
        Function to get data from files found in the 'binpath' directory 

        '''
                      
        filepath = self.cmv.joinNode(self.binpath,file_Name)
        lines = iop.flat_file_grab(filepath)

        if(lines == False or not isinstance(lines,list)):
            print(self.s4+"[data_from_bin] Error: Failure to get data from file: '"+str(file_Name)+"'")
            print(self.s4+"Pathway: '"+str(filepath))
            print(self.s4+"Run number: "+str(self.run_time)+"'\n")
            return False

        if(len(lines) < number_Lines):
            print(self.s4+"[data_from_bin] Error: the number of lines found in file less than: "+str(number_Lines))
            print(self.s4+"File name: '"+str(file_Name)+"'")
            print(self.s4+"Run number: "+str(self.run_time)+"'\n")
            return False 
                    
        if(first_Line):
            return lines[0] 
        else: 
            return lines   

  
    def run_benv(self, collect = True):

        if(self.SUBPROCESS_PATH_ERROR):
            print("[run_benv] Error: pathway to binary directory has not been set")
            return False

        subprocess.call("./run.sh", shell=True)                   
        return True


    def parse_skval_benv_vals(self, benvals, split = True):

        if(split):
            parlines = [] 
            nuclines = []
            azs      = []
        else:
            outlines = []

        for i in xrange(len(benvals)):
            parline = strl.str_to_list(str(benvals[i][0][0]).rstrip(), filtre=True)
            nucline = strl.str_to_list(str(benvals[i][0][1]).rstrip(), filtre=True)
        
            parline = strl.array_to_str([round(float(j),10) for j in parline], spc = '  ')
            nucline = strl.array_to_str([round(float(j),10) for j in nucline], spc = '  ')

            if(split):
                parlines.append(parline) 
                nuclines.append(nucline)
                azs.append((str(int(float(benvals[i][1][0]))), str(int(float(benvals[i][1][1])))))
            else:            
                isoline = '    '+str(int(float(benvals[i][1][0])))+'  '+str(int(float(benvals[i][1][1])))
                totline = parline+nucline+isoline+'\n'                
                outlines.append(totline)
        
        if(split): 
            return (parlines, nuclines, azs)
        else: 
            return outlines


    def clean_up(self, debug = False):

        if(debug):
            pass
        else:
            if(self.cmv.varPath_Dir != self.BINFILE):          
                success, output = self.cmv.cmd("cd "+self.BINFILE)
                if(not success):
                    print("[clean_up] ExitError: failure to access "+self.BINFILE)
                    self.exit_function("while changing directories")
            else:
                return False            
    
            subprocess.call("rm CONSOLE.txt",shell = True)         
        
        self.exit_error_check()
        print("")
        time.sleep(0.5)
        print("No fatal Errors detected")
        time.sleep(0.5)
        print("Run Number upon exit:  "+str(self.run_time))
        time.sleep(0.5)
        print("Script run-time :  "+str(round(time.time()-self.time_Start,3))+" seconds")
        time.sleep(0.5)
        print("   ")

        return True

    # Running and Looping functions

    def run_once(self, clean_Run = True):
           
        pars, vals = self.data_from_pars() 
        self.pass_pars(pars)
        self.pass_vals(vals)
        self.run_benv()
        
        optpars  = self.data_from_bin(self.VRBFILE,True)
        if(optpars == False):
            self.VRBFILE_ERROR = True                   
         
        skinvals = self.data_from_bin(self.SKNFILE,True)
        if(skinvals == False):
            self.SKNFILE_ERROR = True 
         
        if(clean_Run):
            subprocess.call("rm "+self.VRBFILE, shell = True)
            subprocess.call("rm "+self.SKNFILE, shell = True)

        self.run_time+=1
        return (optpars,skinvals)
        
      
    def skval_loop(self, parline, skval_data, skval_type):
        ''' 
        Notes: 

        '''
    
        benvals = []    
         
        # Parsing data from the skval data file, default : 'skval.don' 
        if(not isinstance(skval_data,(list,tuple)) or not isinstance(skval_type,str)):
            print(self.s4+"[skval_loop] TypeError: check function input variables\n")
            return False
        else:
            data = list(skval_data)            
            type = str(skval_type)              
        
        # 'type' determines if BENV values are computed by a skval loop or individual nuclei   
        if(type == 'loop'):        
            skval_list = self.skval_loop_line_parse(data)
            if(skval_list == False):
                return skval_list
            if(not isinstance(skval_list[0],int) or not isinstance(skval_list[1],int) or not isinstance(skval_list[2],int)):
                return False

            if(skval_list[3]):
                inv = -1 
            else:
                inv = 1                     
            for i in xrange(skval_list[0]):
                ax = self.initial_a+inv*skval_list[2]*(i)
                for j in xrange(skval_list[1]): 
                    zx = self.initial_z+inv*(skval_list[2])*(j)                                    
                    parlines = self.format_pars_data(parline, ax, zx)     
                    if(parlines == False):
                        print(self.s4+"[skval_loop] Error: failure when formatting 'parameters', current run skipped\n")
                        results = ('False','False')
                        benvals.append((results,(ax,zx))) 
                        continue 

                    success = self.write_parlist(parlines)
                    if(not success): 
                        print(self.s4+"[skval_loop] Error: failure when passing 'parameters', current run skipped\n")
                        results = ('False','False')
                    else:
                        results = self.run_once()
                    benvals.append((results,(ax,zx))) 

        elif(type == 'pair'):   
            for i in data: 
                ax = i[0]
                zx = i[1]
                parlines = self.format_pars_data(parline, ax, zx)
                if(parlines == False):
                    print(self.s4+"[skval_loop] Error: failure when formatting 'parameters', current run skipped\n")
                    results = ('False','False')
                    benvals.append((results,(ax,zx))) 
                    continue 
                 
                success = self.write_parlist(parlines)
                if(not success): 
                    print(self.s4+"[skval_loop] Error: failure when passing 'parameters', current run skipped\n")
                    results = ('False','False')
                else:
                    results = self.run_once()
                benvals.append((results,(ax,zx)))                
        else:
            print(self.s4+"[skval_loop] ValueError: 'type' value not reconignized")
            benvals = False     
          
        return benvals


    def benv_eos_loop(self, reset=True):
        '''
        !Function which runs the BENV program!

        reset : [bool] (True), resets data files to pre-run values
        '''

        benvals_group = []
        benvals_cohort= []

        #Get EoS from 'eos' folder
        eoslist = self.collect_eos()
        if(eoslist == False):
            return self.__err_print__("could not collect EoS data from 'eos' folder", heading='Fatal Error', **kwargs)

        #Get SKVAL from 'skval.don' file
        skval_lines = self.get_options(**kwargs)
        if(skval_lines == False):
            return self.__err_print__("could not collect SKVAL data from 'skval.don' file", heading='Fatal Error', **kwargs)

        # Format skval lines into data list, type string and pars list
        skval_data = self.parse_skval(skval_lines, **kwargs)
        if(skval_data == False):
            return self.__err_print__("failure to format skval lines", **kwargs)  
        data, type, pars = skval_data  

        # Get parameters par 'Parameter.don' file
        initial_pars = self.initial_pars
        if(initial_pars == ''):
            self.INITIAL_PARS_ERROR = True
            print(self.s4+"[benv_eos_loop] Warning: 'inital_pars' have not been set\n")
         
        # Convert parameters from (string) to (list of floats), assign list to 'plst'
        if(self.INITIAL_PARS_ERROR):
            pass
        else:
            pl = self.parline_style_convert(initial_pars) 
            if(pl == False):
                self.INITIAL_PARS_ERROR = True
                print(self.s4+"[benv_eos_loop] Error: could not convert 'pars' to list\n")
            else:
                plst = [pl[1],pl[5],pl[6],pl[7],pl[8],pl[9],pl[10]]   
             

        # cycle through each EoS
        if(self.initpar and not self.INITIAL_PARS_ERROR):
            for i,entry in enumerate(eoslist):

                # Convert each EoS object into eos data (eos_obj) and eos id (eosid)  
                packed_format_eos_data = self.format_eos_data(entry, pl=plst)
                ith_entry = strl.print_ordinal(str(i+1)) 
                if(packed_format_eos_data == False):                    
                    print("[benv_eos_loop] Error: the "+ith_entry+" EoS could not be formatted")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue 
                eos_obj,eosid = packed_format_eos_data
            
                # Set eos data (eos_instance) and 'par.don' line (parline) 
                eos_instance, parline = eos_obj
		         
                # Pass the eos data to the appropriate file  
                success = self.pass_eos(eos_instance)
                if(success == False): 
                    print(self.s4+"[benv_eos_loop] RuntimeError: could not pass the "+ith_entry+" EoS to the bin folder")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue 
		    
                # Initiate skval loop for given 'parline', 'data' and 'type' and 'parline'
                benvals = self.skval_loop(parline, data, type)
                if(benvals == False):
                    print(self.s4+"[benv_eos_loop] Error: failure of the 'skval_loop' routine\n")
                    print(self.s4+"'skval_loop' failure occured for the "+ith_entry+" run of the loop")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue 
		    
                # Format data returned by skavl loop routine 
                try:
                    formatted_benvals = self.parse_skval_benv_vals(benvals)
                except:
                    print(self.s4+"[benv_eos_loop] Error: fatal error occured when formating data from 'skval_loop'\n")
                    print(self.s4+"Formating failure occured for the "+ith_entry+" run of the loop")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue 
                    
                if(formatted_benvals == False):
                    print(self.s4+"[benv_eos_loop] Error: failure to properly format data from 'skval_loop'\n")
                    print(self.s4+"Formating failure occured for the "+ith_entry+" run of the loop")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue 
                      
                benvals_group.append((formatted_benvals,eosid))
            benvals_cohort.append(benvals_group)
            benvals_group = []
        else:    
            pass 
           
        if(len(pars)>0):
             
            if(self.egrprup):
                out_Iter = pars   
                inn_Iter = eoslist 
            else: 
                out_Iter = eoslist 
                inn_Iter = pars

            for i,out_entry in enumerate(out_Iter):
                for j,inn_entry in enumerate(inn_Iter):

                    if(self.egrprup):
                        eos_entry = inn_entry 
                        par_entry = out_entry
                        ith_entry = strl.print_ordinal(str(i+1)) 
                        jth_entry = strl.print_ordinal(str(j+1))
                    else:
                        eos_entry = out_entry  
                        par_entry = inn_entry 
                        ith_entry = strl.print_ordinal(str(j+1)) 
                        jth_entry = strl.print_ordinal(str(i+1))

                    # Convert each EoS object into eos data (eos_obj) and eos id (eosid)
                    packed_format_eos_data = self.format_eos_data(eos_entry, pl=par_entry)
                    ith_entry = strl.print_ordinal(str(i+1))
                    jth_entry = strl.print_ordinal(str(j+1))
                    if(packed_format_eos_data == False):
                        cycle_Info_Text = "the "+jth_entry+" EoS, during the "+ith_entry+" par cycle,"
                        print(self.s4+"[benv_eos_loop] Error: "+cycle_Info_Text+" could not be formatted")
                        print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                        continue
                    eos_obj,eosid = packed_format_eos_data
                    eos_instance, parline = eos_obj

                    # Pass the eos data to the appropriate file  
                    success = self.pass_eos(eos_instance)
                    if(success == False):
                        cycle_Info_Text = "the "+jth_entry+" EoS, during the "+jth_entry+" par cycle,"
                        print(self.s4+"[benv_eos_loop] RuntimeError: "+cycle_Info_Text+" could not be passed to the bin folder")
                        print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                        continue

                    # Initiate skval loop for given 'parline', 'data' and 'type' and 'parline'
                    benvals = self.skval_loop(parline, data, type)
                    if(benvals == False):
                        print(self.s4+"[benv_eos_loop] Error: failure of the 'skval_loop' routine\n")
                        print(self.s4+"'skval_loop' failure occured for the "+ith_entry+" run of the loop")
                        print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                        continue

                # Format data returned by skavl loop routine
                try:
                    formatted_benvals = self.parse_skval_benv_vals(benvals)
                except:
                    print(self.s4+"[benv_eos_loop] Error: fatal error occured when formating data from 'skval_loop'\n")
                    print(self.s4+"Formating failure occured for the "+ith_entry+" run of the loop")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue

                if(formatted_benvals == False):
                    print(self.s4+"[benv_eos_loop] Error: failure to properly format data from 'skval_loop'\n")
                    print(self.s4+"Formating failure occured for the "+ith_entry+" run of the loop")
                    print(self.s4+"This execution will be terminated, cycling to the next eos...\n")
                    continue

                if(self.egrprup):
                    benvals_group.append((formatted_benvals,"eos_grup_"+str(jth_entry)+"_"+eosid))
                else:
                    benvals_group.append((formatted_benvals,"par_var_"+str(ith_entry)+"_"+eosid))

            benvals_cohort.append(benvals_group)
            benvals_group = []

        if(reset):
            self.write_parlist(self.format_pars_data(self.initial_pars, self.initial_a, self.initial_z, parform = 'str'))

        return benvals_cohort