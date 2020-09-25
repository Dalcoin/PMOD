import sys
import os
import subprocess
import re
import time

from progLib.programStructure import progStruct

from progLib.pmod import ioparse as iop
from progLib.pmod import strlist as strl
from progLib.pmod import mathops as mops


class benv(progStruct):

    def __init__(self,
                 eos_fold_name='eos',
                 par_file_name='par.don',
                 val_file_name='nucleus.don',
                 vrb_file_name='opt_par.etr',
                 skn_file_name='skin.srt',
                 xeb_bin_name='xeb_server',
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

        # EOS-BIN FILE
        self.EXFILE = 'ex_nxlo.don'
        self.E0FILE = 'e0_nxlo.don'
        self.E1FILE = 'e1_nxlo.don'

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
        self.RESETIT = re.compile(r"\s*Resetit\s*:\s*(TRUE|True|true|FALSE|False|false)")

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
        self.initial_parline = ''
        self.initial_vallist = []
        self.initial_nucs = []
        self.initial_a = 0
        self.initial_z = 0

        # skval functionality
        self.skval_dict = {'INCloop':False,
                           'AZpairs':False,
                           'Initpar':False,
                           'Mirrors':False,
                           'EOSpars':False,
                           'EOSgrup':False,
                           'Resetit':False}

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
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.VALFILE, **kwargs)

        if(self.AUXFILE in self.BIN_DICT):
            self.AUXPATH = self.BIN_DICT[self.AUXFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.AUXFILE, **kwargs)

        if(self.XEBFILE in self.BIN_DICT):
            self.XEBPATH = self.BIN_DICT[self.XEBFILE]
        else:
            success = self.__err_print__("not found in '"+self.BINFOLD+"'", varID=self.XEBFILE, **kwargs)

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
                    'EOSgrup':self.EOSGRUP,
                    'Resetit':self.RESETIT}

        test_list = ['INCloop',
                     'AZpairs',
                     'Initpar',
                     'Mirrors',
                     'EOSpars',
                     'EOSgrup',
                     'Resetit']

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
                if(resh == 'loop' or resh == 'special'):
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

        if(len(parlist) >= 4):
            self.initial_parline = parlist[0]
            self.initial_vallist = parlist[1:]

        # Parse the nuclist
        if(len(nuclist) > 0):
            if(pairs):
                try:
                    nuclist = map(lambda lam: (int(lam[0]), int(lam[1])), nuclist)
                except:
                    return self.__err_print__("failure to retrieve 'pair' values as integers", varID='nuclist', **kwargs)
            else:
                try:
                    nuclist = map(lambda lam: (int(lam[0]), int(lam[1]), int(lam[2]), bool(lam[3])), nuclist)
                except:
                    return self.__err_print__("failure to retrieve 'loop' values as integers", varID='nuclist', **kwargs)
            self.initial_nucs = nuclist

        if(self.skval_dict["INCLOOP"] and self.skval_dict["AZPAIRS"]):
            self.__err_print__("INCLOOP takes precedent over AZPAIRS", heading="warning", **kwargs)

        doubles = []
        loop = []

        if(pairs):
            loop_type = 'pairs'
        else:
            loop_type  = 'loop'

        output = (loop_type, nuclist, parlist)
        return output


    ##############
    # Parameters #
    ##############

    def create_parline(self, eos, n, n0, n1,
                         density = 2,
                         microscopic = True,
                         e0_rho0 = True,
                         phenom_esym = False,
                         k0 = 220,
                         rho0 = 0.16,
                         fff = 65,
                         addn=True,
                         **kwargs):

        '''
        A function which creates a 'par' formatted string

        The input consists of an eos identifier variable and optional
        variables corrosponding to each possible 'par' modifier

        pars takes the form: [see read-me for details]

            n  nden nread n0 n1 mic isnm iemp k0  rho0 fff
            11 2    0     19 19 1   1    0    220 0.16 65

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

        if(all([n==0,n0==0,n1==0]) and mic == 1):
            return self.__err_print__("if a microscopic eos is chosen, file length(s) must be defined", **kwargs)
        if(mic == 1 and pos_3 == 0 and n == 0):
            return self.__err_print__("if a combined eos is chosen, the file length must be defined", **kwargs)
        elif(mic == 1 and pos_3 == 1 and n < 2):
            return self.__err_print__("if a seperated eos is chosen, file lengths must be defined (e0 first, then e1)", **kwargs)
        elif(mic == 1 and pos_3 == 2 and n < 1):
            return self.__err_print__("if a SNM eos only is chosen, the file length must be defined", **kwargs)
        else:
            if(mic == 1 and (pos_3 == 0 or pos_3 == 2)):
                pos_1 = n
                pos_4 = 0
                pos_5 = 0
            elif(mic == 1 and pos_3 == 1):
                pos_1 = 0
                pos_4 = n0
                pos_5 = n1
            else:
                pos_1 = 0
                pos_4 = 0
                pos_5 = 0

        outlist = [pos_1,pos_2,pos_3,pos_4,pos_5,pos_6,pos_7,pos_8,pos_9,pos_10,pos_11]
        parline = strl.array_to_str(outlist)

        if(addn):
            parline += '\n'

        return parline

    def parse_parline(self, parline, **kwargs):
        '''
            n  nden nread n0 n1 mic isnm iemp k0  rho0 fff
            11 2    0     19 19 1   1    0    220 0.16 65
        '''

        if(self.__not_str_print__(parline, varID='parline', **kwargs)):
            return False

        pl = strl.str_to_list(parline, filtre=True, **kwargs)
        if(self.__not_arr_print__(pl, varID='parlist', **kwargs)):
            return False

        n = len(pl)
        if(n != 11):
            return self.__err_print__("length should be 11 values. Length : "+str(n), varID='parline', **kwargs)

        try:
            parlist = [int(pl[0]),
                       int(pl[1]),
                       int(pl[2]),
                       int(pl[3]),
                       int(pl[4]),
                       int(pl[5]),
                       int(pl[6]),
                       int(pl[7]),
                       int(pl[8]),
                       float(pl[9]),
                       int(pl[10])]
            return parlist
        except:
            return self.__err_print__("could not be coerced into appropriate parline values", varID='parlist', **kwargs)

    def update_parline(self, val, pos, parline, **kwargs):

        parsed_parline = self.parse_parline(parline, **kwargs)
        if(parsed_parline == False):
            return False

        if(self.__not_num_print__(val, varID='val', style='int', **kwargs)):
            return False

        if(isinstance(pos, (str, int))):
            try:
                pos = int(pos)
            except:
                return self.__err_print__("should be an integer ranging between 0-10", varID='pos', **kwargs)
            if(pos < 0 or pos > 10):
                return self.__err_print__("should be an integer ranging between 0-10", varID='pos', **kwargs)
        elif(isinstance(val, (list,tuple)) and isinstance(pos, (list,tuple))):
            if(not (len(val) == len(pos))):
                msg = ["'val' and 'pos' should be the same length","'pos' length : "+str(len(val)),"'pos' length : "+str(len(pos))]
                return self.__err_print__(msg, **kwargs)
            try:
                pos = [int(entry) for entry in pos]
            except:
                return self.__err_print__("entries should be convertable to integers", varID='pos', **kwargs)
            if(min(pos) < 0 or max(pos) > 10):
                return self.__err_print__("should contain integers ranging between 0-10", varID='pos', **kwargs)
            ward = 'list'

        if(ward == 'list'):
            for i,entry in enumerate(pos):
                parsed_parline[entry] = val[i]
        else:
            parsed_parline[pos] = val

        return strl.array_to_str(parsed_parline, **kwargs)


    def create_vallist(self, a, z, divs='64 64 64', lims='0.0 20.0', addn=True, **kwargs):
        '''
        Description : Creats a list compatible with the 'nucleus.don' file.
                      Takes a 'parline' string along with an 'A' string, 'Z' string,
                      'divs' string and 'lims' string. 'addn' add the endline character
                      to each string.
        '''

        if(__not_str_print__(divs, varID='divs', **kwargs)):
            try:
                if(isinstance(divs, (list, tuple))):
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

        if(__not_str_print__(lims, varID='lims', **kwargs)):
            try:
                if(isinstance(lims, (list, tuple))):
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


    def parse_valline(self, valline, **kwargs):
        '''
        64 64 64
        0.0 20.0
        208 82
        '''

        if(self.__not_strarr_print__(valline, varID='valline', **kwargs)):
            return False
        if(len(valline) != 3):
            return self.__err_print__("length should contain be 3 strings. Length : "+str(len(valline)), varID='valline', **kwargs)
        divs, lims, anz = valline

        vallist = []

        dv = strl.str_to_list(divs, filtre=True, **kwargs)
        if(self.__not_arr_print__(dv, varID='divs', **kwargs)):
            return False
        n = len(dv)
        if(n != 3):
            return self.__err_print__("length should be 3 values. Length : "+str(n), varID='divs', **kwargs)
        try:
            dvlist = [int(dv[0]),
                      int(dv[1]),
                      int(dv[2])]
            vallist.append(dvlist)
        except:
            return self.__err_print__("could not be coerced into appropriate valline values", varID='divs', **kwargs)

        lm = strl.str_to_list(lims, filtre=True, **kwargs)
        if(self.__not_arr_print__(lm, varID='lims', **kwargs)):
            return False
        n = len(lm)
        if(n != 2):
            return self.__err_print__("length should be 2 values. Length : "+str(n), varID='lims', **kwargs)
        try:
            lmlist = [float(dv[0]),
                      float(dv[1])]
            vallist.append(lmlist)
        except:
            return self.__err_print__("could not be coerced into appropriate valline values", varID='lims', **kwargs)

        az = strl.str_to_list(anz, filtre=True, **kwargs)
        if(self.__not_arr_print__(az, varID='anz', **kwargs)):
            return False
        n = len(az)
        if(n != 2):
            return self.__err_print__("length should be 2 values. Length : "+str(n), varID='anz', **kwargs)
        try:
            azlist = [int(dv[0]),
                      int(dv[1])]
            vallist.append(azlist)
        except:
            return self.__err_print__("could not be coerced into appropriate valline values", varID='anz', **kwargs)

        return vallist


    def write_parline(self, parline):
        '''
        Passes benv parameters to 'par.don' file located in 'bin'

        pars takes the form: [see read-me for details]

            n  nden nread n0 n1 mic isnm iemp k0  rho0 fff
            11 2    0     19 19 0   1    0    220 0.16 65

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

    def format_benv_data(self, data, eospars=False, eosgrup=False, style=None, coerce_to_style=False, **kwargs):

        par_Strings = []
        val_Strings = []

        val_Strings.append("NR      PR      NS    CHR      BE      SEC   A   Z\n")
        val_Strings.append("\n")

        for cohort in data:
            for i,group in enumerate(cohort):
                try:
                    entry, eosid = group
                except:
                    msg = ["Data format invalid : ", "Data : "+str(group), "Failure for the "+strl.print_ordinal(i+1)+" EoS input"]
                    self.__err_print__(msg, varID=eosid, **kwargs)
                    continue
                if(entry == False):
                    msg = ["EoS could not be evaluated, check EoS file", "Failure for the "+strl.print_ordinal(i+1)+" EoS input"]
                    self.__err_print__(msg, varID=eosid, **kwargs)
                    continue

                par_Strings.append(str(eosid)+'\n')
                val_Strings.append(str(eosid)+'\n')

                try:
                    par_String, val_String, nucleus = entry
                except:
                    msg = ["EoS entry could not be evaluated...", "Failure for the "+strl.print_ordinal(i+1)+" EoS input"]
                    self.__err_print__(msg, varID=eosid, **kwargs)
                    continue
                nucleus = ["  "+strl.array_to_str(az ,spc = '  ')+'\n' for az in nucleus]

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

        eos_file_list = self.contentPath(self.EOSPATH)

        if(eos_file_list == None or eos_file_list == False):
            self.EOS_COLLECT_ERROR = True
            return self.__err_print__("folder contents could not be retrieved", varID='eos', **kwargs)

        exfiles = []
        e1files = []
        e0files = []
        eafail = []
        eoslist = []

        for i in eos_file_list:
            if('ex' in i.lower() and (('e0' not in i.lower()) and ('e1' not in i.lower()))):
                exfiles.append(i)
            elif('e1' in i.lower() and (('e0' not in i.lower()) and ('ex' not in i.lower()))):
                e1files.append(i) 
            elif('e0' in i.lower() and (('ex' not in i.lower()) and ('e1' not in i.lower()))):
                e0files.append(i)
            else:
                eafail.append(i)

        if(len(eafail) > 0):
            msg = ["The following files are not valid 'eos' files:"]+eafail
            self.__err_print__(msg, **kwargs)

        improper_format = []
        for file in exfiles:
            file_path = self.joinNode(eos_dir_path, file, **kwargs)
            ex = iop.flat_file_intable(file_path, **kwargs)
            if(ex != False):
                if(len(ex) != 3):
                    improper_format.append(ex)
                    continue
                eoslist.append((ex, file))
            else:
                continue
        self.__err_print__(["The following 'ex' files were improperly formatted:"]+improper_format, **kwargs)

        for file in e0files:

            e1pack = False
            e1name = ''

            comp_name = self.name_compliment(file, {'e0':'e1', 'E0':'E1'}, **kwargs)
            if(comp_name == False):
                self.__err_print__("could not be converted to a name compliment", varID=file, **kwargs)
            else:
                if(len(comp_name) > 0):
                    if(len(comp_name) > 2):
                        self.__err_print__("has more than one file compliment", varID=file, heading='Warning', **kwargs)
                    e1name = comp_name[0][0]
                    idbaseline = comp_name[0][1]
                else:
                    self.__err_print__("could not be converted to a name compliment", varID=file, **kwargs)

            e1data = False

            e0_file_path = self.joinNode(self.EOSPATH, file, **kwargs)
            e0data = iop.flat_file_intable(e0_file_path, **kwargs)
            if(e1name in e1files):
                e1pack = True
                e1_file_path = self.joinNode(eos_dir_path, e1name, **kwargs)
                e1data = iop.flat_file_intable(e1_file_path, **kwargs)

            if(not e0data):
                print("[collect_eos] Error: could not parse the file at path '"+str(e0_file_path)+"' into a table")
                continue
            if(e1data == False and e1pack):
                print("[collect_eos] Error: could not parse the file at path '"+str(e1_file_path)+"' into a table")
                continue

            if(e1pack):
                e10 = []
                try:
                    e10 = [e0data[0], e0data[1], e1data[0], e1data[1]]
                    eoslist.append((e10,idbaseline))
                except:
                    msg = ["failure to coerce data into four arrays, check pathways:", e0_file_path, e1_file_path]
                    self.__err_print__(msg, **kwargs)
                    continue
            else:
                e0 = []
                try:
                    e0 = [e0data[0], e0data[1]]
                    eoslist.append((e0,idbaseline))
                except:
                    msg = ["failure to coerce data into two arrays, check pathway:", e0_file_path]
                    self.__err_print__(msg, **kwargs)
                    continue

        return eoslist


    def format_eos_data(self, eos_obj, parline, **kwargs):

        try:
            eoslist, eosid = eos_obj
        except:
            return self.__err_print__("should be an array of length two", varID='eos_obj',  **kwargs)

        output = ()
        exgp = []
        e0gp = []
        e1gp = []

        m = len(eoslist)

        if(m == 3):
            type = 0
            kf = eoslist[0]
            e0 = eoslist[1]
            e1 = eoslist[2]
            if(len(kf) == len(e0) and len(e0) == len(e1)):
                n = len(kf)
            else:
                return self.__err_print__("eos arrays should all be the same length", varID='eos_obj', **kwargs)
            exgp = map(lambda x,y,z: strl.array_to_str([x,y,z], spc='  ', endline=True), kf,e0,e1)
            eval = [exgp]
            neid = 'ex'+eosid
            parline = self.update_parline([n,0], [0,2], parline, **kwargs)

        elif(m == 4):
            type = 1
            kf0 = eoslist[0]
            e0  = eoslist[1]
            kf1 = eoslist[2]
            e1  = eoslist[3]

            if(len(kf0) == len(e0)):
                n0 = len(kf0)
            else:
                return self.__err_print__("and the corrosponding kfs should be arrays with the same length", varID='e0', **kwargs)

            if(len(kf1) == len(e1)):
                n1 = len(kf1)
            else:
                return self.__err_print__("and the corrosponding kfs should be arrays with the same length", varID='e0', **kwargs)

            e0gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf0,e0)
            e1gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True),kf1,e1)
            eval = [e0gp, e1gp]
            neid = 'e10'+eosid
            parline = self.update_parline([1, n0, n1], [2, 3, 4], parline, **kwargs)

        elif(m == 2):
            type = 2
            kf = eoslist[0]
            e0 = eoslist[1]

            if(len(kf) == len(e0)):
                n = len(kf)
            else:
                return self.__err_print__("and the corrosponding kf should be arrays of the same length", varID='e0', **kwargs)

            e0gp = map(lambda x,y: strl.array_to_str([x,y],spc='  ',endline=True), kf,e0)
            eval = [e0gp]
            neid = 'e0'+eosid
            parline = self.update_parline([n, 2], [0, 2], parline, **kwargs)

        else:
            return self.__err_print__("must a numeric array of length 2, 3 or 4", varID='eoslist', **kwargs)

        output = (type, eval, parline, neid)

        return output


    def write_eos(self, formatted_eos, **kwargs):

        ealist = []
        e0list = []
        e1list = []

        try:
            elist, type = formatted_eos
            try:
                if(type == 0):
                    ealist = elist[0]
                elif(type == 1):
                    e0list = elist[0]
                    e1list = elist[1]
                elif(type == 2):
                    e0list = elist[0]
            except:
                msg = "has an eos component which is not properly formatted"
                return self.__err_print__(msg, varID='formatted_eos', **kwargs)
        except:
            return self.__err_print__("should be an array of length three", varID='formatted_eos', **kwargs)

        if(type == 0):
            eos_path = self.joinNode(self.BINPATH, self.EXFILE, **kwargs)
            if(eos_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.EXFILE, **kwargs)
            success = iop.flat_file_write(eos_path, ealist, **kwargs)
            if(success == False):
                return False
        elif(type == 1):
            e0_path = self.joinNode(self.BINPATH, self.E0FILE, **kwargs)
            if(e0_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.E0FILE, **kwargs)
            success = iop.flat_file_write(e0_path, e0list, **kwargs)
            if(success == False):
                return False
            e1_path = self.joinNode(self.BINPATH, self.E1FILE, **kwargs)
            if(e1_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.E1FILE, **kwargs)
            success = iop.flat_file_write(e1_path, e1list, **kwargs)
            if(success == False):
                return False
        elif(type == 2):
            e0_path = self.joinNode(self.BINPATH, self.E0FILE, **kwargs)
            if(e0_path == False):
                return self.__err_print__(["could not be added to the 'bin' pathway:", self.BINPATH], varID=self.E0FILE, **kwargs)
            success = iop.flat_file_write(e0_path, e0list, **kwargs)
            if(success == False):
                return False
        else:
            return self.__err_print__("not properly formatted", varID='formatted_eos', **kwargs)

        return True


    #######################################
    # functions dealing with benv looping #------------------------------------------------------------|
    #######################################

    def clean_up(self):
        
        self.exit_error_check()
        print("")
        print("No fatal Errors detected")
        print("Run Number upon exit:  "+str(self.run_time))
        print("Script run-time :  "+str(round(time.time()-self.time_Start,3))+" seconds")
        print("   ")

        return True

    # Running and Looping functions

    def single_run(self, parline=None, vallist=None, run_cmd='run.sh', clean_Run=True, **kwargs):

        if(isinstance(parline, str)):
            pass_parline = self.write_parline(parline, **kwargs)
            if(pass_parline == False):
                msg = ["failure to create and write parline", "parline : "+str(parline)]
                return self.__err_print__(msg, **kwargs)
        if(isinstance(vallist, (tuple, list))):
            pass_vallist = self.write_vallist(vallist, **kwargs)
            if(pass_vallist == False):
                msg = ["failure to create and write vallist", "vallist : "+str(vallist)]
                return self.__err_print__(msg, **kwargs)

        self.set_osdir(self.EOSPATH, **kwargs)
        self.run_commands(run_cmd, **kwargs)
        self.set_osdir(**kwargs)

        values_dict = self.read_files_from_folder('bin', [self.VRBFILE, self.SKNFILE], clean=True, **kwargs)

        optpars = values_dict.get(self.VRBFILE)
        skinvals = values_dict.get(self.SKNFILE)

        if(clean_Run):
            self.clearDir(['eos'], select=[self.VRBFILE, self.SKNFILE], **kwargs)

        self.cycle+=1
        return (optpars, skinvals)


    def skval_loop(self, skval, mirrors=False, **kwargs):
        '''
        Notes:

        '''

        try:
            nuclist, loop_type, parlist = skval
        except:
            return self.__err_print__("should be an array of two values", varID='skval', **kwargs)

        if(self.__not_str_print__(loop_type, varID='loop_type', **kwargs)):
            return False
        else:
            loop_type = loop_type.lower()
            loop_type = loop_type.rstrip()
            if(loop_type != 'loop' and loop_type != 'pair'):
                return self.__err_print__("should be equal to either, 'loop' or 'pair'", varID='loop_type', **kwargs)

        if(self.__not_arr_print__(nuclist, varID='nuclist', **kwargs)):
            return False

        output = []

        # 'loop_type' determines if BENV values are computed by a skval loop or individual nuclei
        if(loop_type == 'loop'):

            for loop in nuclist:

                biga = loop[0]
                bigz = loop[1]
                inc =  loop[2]
                inv =  loop[3]

                if(inv):
                    inv = -1
                else:
                    inv = 1
                for i in xrange(biga):
                    ax = self.initial_a+inv*inc*i
                    for j in xrange(bigz):
                        zx = self.initial_z+inv*inc*j

                        new_vallist = self.create_vallist(ax, zx, **kwargs)
                        pass_vallist = self.write_vallist(new_vallist, **kwargs)
                        if(pass_vallist == False):
                            msg = ["failure to create and write vallist", "vallist : "+str(new_vallist)]
                            return self.__err_print__(msg, **kwargs)

                        results = self.single_run()
                        if(results == False):
                            msg = ["failure to create complete run", "A,Z : "+str(ax)+","+str(zx)]
                            return self.__err_print__(msg, **kwargs)
                        output.append((results,(ax,zx)))

                        if(mirrors and ax-zx!=zx):
                            zx = ax-zx

                            new_vallist = self.create_vallist(ax, zx, **kwargs)
                            pass_vallist = self.write_vallist(new_vallist, **kwargs)
                            if(pass_vallist == False):
                                msg = ["failure to create and write vallist", "vallist : "+str(new_vallist)]
                                return self.__err_print__(msg, **kwargs)

                            results = self.single_run()
                            if(results == False):
                                msg = ["failure to create complete run", "A,Z : "+str(ax)+","+str(zx)]
                                return self.__err_print__(msg, **kwargs)
                            output.append((results,(ax,zx)))
            return output

        if(loop_type == 'pair'):

            for pair in nuclist:

                ax = pair[0]
                zx = pair[1]

                new_vallist = self.create_vallist(ax, zx, **kwargs)
                pass_vallist = self.write_vallist(new_vallist, **kwargs)
                if(pass_vallist == False):
                    msg = ["failure to create and write vallist", "vallist : "+str(new_vallist), ""]
                    return self.__err_print__(msg, **kwargs)

                results = self.single_run()
                if(results == False):
                    msg = ["failure to create complete run", "A,Z : "+str(ax)+","+str(zx)]
                    return self.__err_print__(msg, **kwargs)
                output.append((results,(ax,zx)))
            return output


    def eos_loop(self, eoslist,
                       skval,
                       parline=None,
                       initpar=False,
                       mirrors=False,
                       reset=True,
                       **kwargs):
        '''
        reset : [bool] (True), resets data files to pre-run values
        '''

        benvals_group = []

        if(not isinstance(parline ,str)):
            if(isinstance(self.parline, str)):
                parline = self.parline
            else:
                self.__err_print__("could not be properly parsed", varID='parline', **kwargs)

        # cycle through each EoS
        for i,eos in enumerate(eoslist):

            # Convert each EoS object into eos data (eos_inst) and eos id (eosid)
            formdat = self.format_eos_data(eos, parline **kwargs)
            if(formdat == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS could not be formatted, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue
            # Set eos data (eos_instance) and 'par.don' line (parline)
            type, eos_instance, parline, eosid = formdat

            # Pass the eos data to the appropriate file
            success = self.write_eos(eos_instance)
            if(success == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" EoS could not be passed to 'bin', cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

            if(initpar):
                new_vallist = self.create_vallist(self.initial_a, self.initial_z, **kwargs)
                pass_vallist = self.write_vallist(new_vallist, **kwargs)
                initrun = self.single_run(self, parline=None, vallist=None, run_cmd='run.sh', clean_Run=True, **kwargs)
                if(init_run == False):
                    self.__err_print__("run failed", varID='initpar', **kwargs)
                else:
                    formated_initrun = self.parse_skval_benv_vals(initrun, (self.initial_a, self.initial_z))
                    if(formated_initrun == False):
                        self.__err_print__("failure to execute 'initpar'", **kwargs)
                    else:
                        benvals_group.append((formated_initrun, eosid))

            # Initiate skval loop for given 'parline', 'data' and 'type' and 'parline'
            benvals = self.skval_loop(skval, mirrors, **kwargs)
            if(benvals == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" failed the 'skval_loop' routine, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue

            # Format data returned by skavl loop routine
            formatted_benvals = self.parse_skval_benv_vals(benvals)
            if(formatted_benvals == False):
                ith_entry = strl.print_ordinal(str(i+1), **kwargs)
                msg = "The "+ith_entry+" failed the 'skval_loop' formatting routine, cycling to the next eos..."
                self.__err_print__(msg, **kwargs)
                continue
            benvals_group.append((formatted_benvals,eosid))

        if(reset):
            self.write_parline(self.initial_parline, **kwargs)
            self.write_vallist(self.initial_vallist, **kwargs)

        return benvals_group


    def benv_run(self, reset=True, **kwargs):
        '''
        !Function which runs the BENV program!
        '''

        # Get SKVAL from 'skval.don' file
        skval_lines = self.get_options(**kwargs)
        if(skval_lines == False):
            return self.__err_print__("could not collect 'skval' data from 'skval.don' file", **kwargs)

        # Format skval lines into skval data
        skval = self.parse_skval(skval_lines, **kwargs)
        if(skval == False):
            return self.__err_print__("failure to format 'skval' data", **kwargs)

        # Get EoS from 'eos' folder
        eoslist = self.collect_eos()
        if(eoslist == False):
            return self.__err_print__("could not collect EoS data from 'eos' folder", **kwargs)

        # Put EoS and skval data in EoS loop
        benval_data = self.eos_loop(eoslist, skval,
                                    parline=self.initial_parline,
                                    initpar=self.skval_dict['Initpar'],
                                    mirrors=self.skval_dict['Mirrors'],
                                    reset  =self.skval_dict['Resetit'],
                                    **kwargs)

        formatted_benval_data = self.format_benv_data(benval_data,
                                                      self.skval_dict['EOSpars'],
                                                      self.skval_dict['EOSgrup'],
                                                      **kwargs)
        return formatted_benval_data

