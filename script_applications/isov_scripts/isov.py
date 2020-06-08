import subprocess
import os

import ioparse as iop
import strlist as strl
import pmod.program_scaffolding.program_structure as pstruct


class isov(pstruct.progStruct):

    def __init__(self, **kwargs):

        self.EOSFOLD = 'eos'
        self.EOSPATH = ''
        self.EOSPATH_SET = False
        self.EOSPATH_ERROR = False

        self.E0FILE = 'e0_nxlo.don'
        self.E1FILE = 'e1_nxlo.don'
        self.EXFILE = 'ex_nxlo.don'

        self.E0FILE_PATH = ''
        self.E1FILE_PATH = ''
        self.ExFILE_PATH = ''

        self.PARFILE = 'par.don'

        valid_keys = [ 'dir_fold_name',
                       'src_fold_name',
                       'bin_fold_name',
                       'dat_fold_name',
                       'opt_file_name',
                       'initialize',
                       'kernel']

        # Printing available functions with corrosponding commands here...
        iso_lines = [self.s4+"\n",
                     self.s4+"Please input a command from the list below:\n",
                     2*self.s4+"Isoscalar/Isovector values from EoS found in 'eos' file        : iso",
                     2*self.s4+"To generate parabolic progression for EoS found in 'eos' file  : parab",
                     2*self.s4+"To generate working set of phenomenological EoS                : phenom",
                     2*self.s4+"To generate chiral cutoff error for data files in 'dat'        : error",
                     "\n"
                    ]

        # Adding available functions with corrosponding commands here...
        self.action_dict = {'iso':self.run_iso,
                            'parab':self.run_parab,
                            'phenom':self.run_phenom
                            'error':self.chiral_cutoff_error
                           }

        # Checking intialized class inputs for availability
        for key in kwargs:
            if(key not in valid_keys):
                del kwargs[key]

        # Initializing parent class
        super(isov, self).__init__(kwargs)

        # Setting-up additional requirements for ISOV class
        self.eos_check()
        self.init_fold_in_main(self.EOSFOLD)
        self.set_eos_file_paths()

        self.set_option_menu(iso_lines)


    #-----------------#
    #  Par functions  #
    #-----------------#

    def create_parline(self, eosinfo, **phenom_pars):

        idbase, nread, n = eosinfo
        if(nread == 1):
            n0, n1 = n
            n = 0
        else:
            n0, n1 = 0, 0

        mic = phenom_pars.get('mic')
        isym_emp = phenom_pars.get('isym_emp')
        isnm = phenom_pars.get('isnm')
        k0 = phenom_pars.get('k0')
        rho0 = phenom_pars.get('rho0')

        array = (n, 2, nread, n0, n1, mic, isnm, isym_emp, k0, rho0 , 65)
        parline = strl.array_to_str(array)
        return parline


    def pass_parline(parline):
        if(not isinstance(parline,str)):
            if(self.debug):
                print(self.s4+"[pass_parline] Error: input, 'parline', must be a string\n")
            return False

        if(self.BINPATH_SET):
            parpath = self.cmv.joinNode(self.BINPATH, self.PARFILE)
            success = iop.flat_file_write(parpath, [parline])
            if(success == False):
                if(self.debug):
                    print(self.s4+"[pass_eos] Error: failure to pass the input, 'parline', to the 'par' file\n")
            return success
        else:
            if(self.debug):
                print(self.s4+"[pass_parline] Error: The path to the 'bin' folder has not yet been set\n")
        return None


    #-----------------#
    #  EoS functions  #
    #-----------------#

    def eos_check(self):
        if(self.INTERNAL_CML_SET and self.DIRPATH_PATH):
            if(self.EOSFOLD in self.DIR_FOLDERS):
                self.EOSPATH = self.cmv.joinNode(self.DIRPATH,self.EOSFOLD)
                self.EOSPATH_SET = True
                return True
            else:
                self.EOSPATH_ERROR = True
                return False
        else:
            return False

    def set_eos_file_paths(self):
        if(self.INTERNAL_CML_SET and self.EOSPATH_SET):
            self.E0FILE_PATH = self.cmv.joinNode(self.EOSPATH,self.E0FILE)
            self.E1FILE_PATH = self.cmv.joinNode(self.EOSPATH,self.E0FILE)
            self.ExFILE_PATH = self.cmv.joinNode(self.EOSPATH,self.E0FILE)
        else:
            if(self.debug):
                print(self.s4+"[set_eos_file_paths] Error: check that internal pathways are set\n")
            return False

    def collect_eos(self):
        '''
        Notes:

            Collects EoS from 'eos' directory
            This function should only be called once per run

        '''

        eos_file_list = self.cmv.contentPath(self.EOSPATH)

        if(eos_file_list == None or eos_file_list == False):
            if(self.debug):
                print(self.s4+"[collect_eos] Error: EoS files could not be found\n")
            self.EOS_COLLECT_ERROR = True
            return False

        exfiles = []
        e1files = []
        e1extra = []
        e0files = []
        nafiles = []
        eoslist = []


        for i in eos_file_list:
            if('ex' in i.lower() and (('e0' not in i.lower()) and ('e1' not in i.lower()))):
                exfiles.append(i)
            elif('e1' in i.lower() and (('e0' not in i.lower()) and ('ex' not in i.lower()))):
                e1files.append(i)
            elif('e0' in i.lower() and (('ex' not in i.lower()) and ('e1' not in i.lower()))):
                e0files.append(i)
            else:
                nafiles.append(i)

        if(len(nafiles) > 0):
            head_Text = "The following files are not valid 'eos' files:"
            strl.format_fancy(nafiles,header=head_Text)

        for i in exfiles:
            file_path = self.cmv.joinNode(self.EOSPATH,i)
            ex = iop.flat_file_intable(file_path)
            if(ex != False):
                if(len(ex) != 3):
                    print(self.s4+"[collect_eos] Error: the file '"+str(i)+"' does not have three equal data columns\n")
                    self.EOS_FILE_FORMAT_ERROR = True
                    continue
                if(len(ex[0]) == len(ex[1]) and len(ex[1]) == len(ex[2])):
                    n = len(ex[0])
                eoslist.append((ex,(i,0,n)))
            else:
                print(self.s4+"[collect_eos] Error: could not read table from '"+str(i)+"'\n")
                continue

        for i in e0files:

            e1pack = False
            e1data = False

            e1name, idbaseline = self.name_compliment(i,{'e0':'e1','E0':'E1'})

            e0_file_path = self.cmv.joinNode(self.EOSPATH,i)
            if(e1name in e1files):
                e1pack = True
                e1extra.append(e1name)
                e1_file_path = self.cmv.joinNode(self.EOSPATH,e1name)

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
                n0 = len(e0data[0])
                n1 = len(e1data[1])
                eoslist.append((e10,(i,1,(n0,n1))))
            else:
                e0 = []
                try:
                    e0 = [e0data[0],e0data[1]]
                except:
                    print("[collect_eos] Error: could not parse '"+str(e0_file_path)+"' content into data")
                    self.EOS_SPLIT_PARSE_ERROR = True
                    continue
                eoslist.append((e0,(i,2,n)))

        for i in e1files:
            if(i not in e1extra):
                e1 = []
                e1_file_path = self.cmv.joinNode(self.EOSPATH,i)
                e1data = iop.flat_file_intable(e1_file_path)
                try:
                    e1 = [e1data[0],e1data[1]]
                except:
                    print(self.s4+"[collect_eos] Error: could not parse '"+str(e1_file_path)+"' content into data\n")
                    continue
                eoslist.append((e1,(i,3,n)))

        return eoslist


    def check_eos(self, eosdata, nread):
        if(nread == 0):
            if(len(eosdata) != 3):
                if(self.debug):
                    print(self.s4+"[check_eos] Error: if input eos has 'nread' of '0', there should be three data columns\n")
                return False
            else:
                n = len(eosdata[0])
                if(all([len(col) == n for col in eosdata])):
                    return True
                else:
                    if(self.debug):
                        print(self.s4+"[check_eos] Error: for input, 'eosdata', columns should all be the same length\n")
                    return False
        if(nread == 1):
            if(len(eosdata) != 4):
                if(self.debug):
                    print(self.s4+"[check_eos] Error: if input eos has 'nread' of '1', there should be four data columns\n")
                return False
            else:
                
                if(len(eosdata[0]) == len(eosdata[1]) and len(eosdata[2]) == len(eosdata[3])):
                    return True
                else:
                    if(self.debug):
                        print(self.s4+"[check_eos] Error: for input, 'eosdata', columns pairs should be the same length\n")
                    return False
        if(nread == 2 or nread == 3):
            if(len(eosdata) != 2):
                if(self.debug):
                    print(self.s4+"[check_eos] Error: if input eos has 'nread' of '2' or '3', there should be two data columns\n")
                return False
            else:
                n = len(eosdata[0])
                if(all([len(col) == n for col in eosdata])):
                    return True
                else:
                    if(self.debug):
                        print(self.s4+"[check_eos] Error: for input, 'eosdata', columns should be the same length\n")
                    return False
        else:
            if(self.debug):
                print(self.s4+"[check_eos] Error: 'nread' must be an integer in the following range [0-3]\n")
            return False


    def pass_eos(self, eosdata, eosinfo):

        try:
            idbase, nread, n = eosinfo
        except:
            if(self.debug):
                print(self.s4+"[pass_eos] Error: input, 'eosinfo', not formatted correctly\n")
            return False

        success = self.check_eos(eosdata, nread)
        if(success == False):
            if(self.debug):
                print(self.s4+"[pass_eos] Error: found in input...\n")
            return False

        if(nread == 0):
            ex_lines = map(lambda x,y,z: str(x)+'    '+str(y)'    '+str(z)+'\n', eosdata[0],eosdata[1],eosdata[2])
            success = iop.flat_file_write(self.EXFILE_PATH,ex_lines)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[pass_eos] Error: failure when writing EoS lines to 'ex' eos file\n")
                return False
        elif(nread == 1):
            e0_lines = map(lambda x,y: str(x)+'    '+str(y)+'\n', eosdata[0],eosdata[1])
            success = iop.flat_file_write(self.E0FILE_PATH, e0_lines)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[pass_eos] Error: failure when writing EoS lines to 'e0' eos file\n")
                return False
            e1_lines = map(lambda x,y: str(x)+'    '+str(y)+'\n', eosdata[2],eosdata[3])
            success = iop.flat_file_write(self.E1FILE_PATH, e1_lines)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[pass_eos] Error: failure when writing EoS lines to 'e1' eos file\n")
                return False
        elif(nread == 2 or nread == 3):
            eq_lines = map(lambda x,y: str(x)+'    '+str(y)+'\n', eosdata[0],eosdata[1])
            if(nread == 2):
                success = iop.flat_file_write(self.E0FILE_PATH, eq_lines)
            else:
                success = iop.flat_file_write(self.E1FILE_PATH, eq_lines)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[pass_eos] Error: failure when writing EoS lines to eos file\n")
                return False
        else:
            if(self.debug):
                print(self.s4+"[pass_eos] Error: 'nread' within input, 'eosinfo', not recognized\n")
            return False
        return True


    #----------------#
    # isov functions #
    #----------------#

    def isov_action_function(self, input_action):

        if(self.action_dict.get(input_action) != None):
            self.action_dict[input_action]()
            return True
        else:
            if(self.debug):
                print(self.s4+"Warning: input, 'input_action', is not a recognized value\n")
            return False


    def run_iso_val(self):
        success = True
        eos_content = self.cmv.contentPath(self.BINPATH)
        if('verify_isov.don' in eos_content):
            self.cmv.delfile(self.cmv.joinNode(self.BINPATH,'verify_isov.don'))

        os.chdir(self.BINPATH)
        try:
            zero = subprocess.call("./run.sh", shell=True)
        except:
            if(self.debug):
                print(self.s4+"[run_iso_val] Error: unknown error while attempting to run the 'run.sh' script in 'bin'\n")
        os.chdir(self.DIRPATH)


    def run_parab_val(self):
        success = True
        eos_content = self.cmv.contentPath(self.BINPATH)
        if('verify_parab.don' in eos_content):
            self.cmv.delfile(self.cmv.joinNode(self.BINPATH,'verify_isov.don'))

        os.chdir(self.BINPATH)
        try:
            zero = subprocess.call("./run.sh", shell=True)
        except:
            if(self.debug):
                print(self.s4+"[run_parab_val] Error: unknown error while attempting to run the 'run.sh' script in 'bin'\n")
        os.chdir(self.DIRPATH)
        

    def run_isov_loop(self):
        success = self.program_loop(self.isov_action_function, program_name='ISOV')
        return success

    #----------------#
    # loop functions #
    #----------------#


    def generate_phenom_parline_dict(self):

        mic = None
        isym_emp = None
        isnm = None

        all_sym = None
        err_opt = None

        # Real-Time Input
        print("  ")
        while(True):
            answer = raw_input(self.s4+"Do you want to use only a microscopic EoS [yes/no]? ")
            if(answer.lower() == 'yes'):
                mic = 1
                break
            elif(answer.lower() == 'no'):
                mic = 0
                break
            else:
                print(" ")
                print(self.s4+"Error: '"+answer+"', could not be parsed...")
                print(self.s4+"please try again, answering only with 'yes' or 'no'\n")

        if(mic == 0):
            print("  ")
            while(True):
                answer = raw_input(self.s4+"Is the symmetry energy phenomenological [yes/no]? ")
                if(answer.lower() == 'yes'):
                    isym_emp = 1
                    break
                elif(answer.lower() == 'no'):
                    isym_emp = 0
                    break
                else:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not be parsed...")
                    print(self.s4+"please try again, answering only with 'yes' or 'no'\n")
            print("  ")
            while(True):
                print(self.s4+"Choose a phenomenological EoS for symmetric matter... ")
                answer = raw_input(self.s4+"saturation density dependent or not [sat/nosat]? ")
                if(answer.lower() == 'nosat'):
                    isnm = 1
                    break
                elif(answer.lower() == 'sat'):
                    isnm = 0
                    break
                else:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not be parsed...")
                    print(self.s4+"please try again, answering only with 'yes' or 'no'\n")
            print("  ")
            while(True):
                answer = raw_input(self.s4+"Do you want to override microscopic symmetric EoS [yes/no]? ")
                if(answer.lower() == 'yes'):
                    all_sym = 1
                    break
                elif(answer.lower() == 'no'):
                    all_sym = 0
                    break
                else:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not be parsed...")
                    print(self.s4+"please try again, answering only with 'yes' or 'no'\n")

        if(isnm == 0):
            print("  ")  
            while(True):
                answer = raw_input(self.s4+"Input a curvature value (MeV) as an integer (typically 220 or 260): ")
                try:
                    k0 = int(answer.rstrip())
                    break
                except:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not converted to a float...")
                    print(self.s4+"please try again, answering with only an integer value\n")
            print("  ")
            while(True):
                answer = raw_input(self.s4+"Input a saturation density (fm^-3) as a float (typically 0.16): ")
                try:
                    rho0 = float(answer.rstrip())
                    break
                except:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not converted to a float...")
                    print(self.s4+"please try again, answering with only a float value\n")

        if(mic == 1):
            isym_emp = 0
            isnm = 0
            k0 = 220
            rho0 = 0.16

        phenom_eos_dict = {'mic':mic, 'isym_emp':isym_emp, 'isnm':isnm, 'k0':k0, 'rho0':rho0}
        return (phenom_eos_dict, all_sym)


    def run_iso(self):

        eoslist = self.collect_eos()
        if(eoslist == False):
            if(self.debug):
                print(self.s4+"[run_iso] Error: 'eos' could not be collected\n")
            return False

        err_opt = None

        phenom_eos_dict, all_sym = self.generate_phenom_parline_dict()

        print(" ")
        # Exceute Input
        for i,eos in enumerate(eoslist):

            print(self.s4+"ISOV evaluation for the "+strl.print_ordinal(i)+" EoS :")

            eosdata, eosinfo = eos
            id, nread, n = eosinfo
            parline = self.create_parline(eosinfo, **phenom_eos_dict)

            success = self.pass_parline(parline)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[run_iso] Warning: an error occured when passing 'parline' to the par file in 'bin'\n")
                continue

            success = self.pass_eos(eosdata,eosinfo)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[run_iso] Warning: an error occured when passing EoS to the eos file in 'bin'\n")
                continue

            success = self.run_iso_val()
            if(success == False):
                if(self.debug):
                    print(self.s4+"[run_iso] Warning: an error occured when evaluating ISOV values\n")
                continue

            isov_file_inst = iop.flat_file_grab(self.cmv.joinNode(self.BINPATH,"IsoVals.don"))
            success = iop.flat_file_write(self.cmv.joinNode(self.DATPATH,"isov_"+id),isov_file_inst)
            del isov_file_inst


        print("  ")
        while(True):
            answer = raw_input(self.s4+"Do you want to calculate the chiral cutoff error [yes/no]? ")
                if(answer.lower() == 'yes'):
                    err_opt = True
                    break
                elif(answer.lower() == 'no'):
                    err_opt = False
                    break
                else:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not be parsed...")
                    print(self.s4+"please try again, answering only with 'yes' or 'no'\n")

        if(err_opt):
            self.chiral_cutoff_error()
        return True


    def run_parab(self):

        eoslist = self.collect_eos()
        if(eoslist == False):
            if(self.debug):
                print(self.s4+"[run_iso] Error: 'eos' could not be collected\n")
            return False

        err_opt = None

        phenom_eos_dict, all_sym = self.generate_phenom_parline_dict()

        print(" ")
        # Exceute Input
        for i,eos in enumerate(eoslist):

            print(self.s4+"Parabolic evaluation for the "+strl.print_ordinal(i)+" EoS :")

            eosdata, eosinfo = eos
            id, nread, n = eosinfo
            parline = self.create_parline(eosinfo, **phenom_eos_dict)

            success = self.pass_parline(parline)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[run_iso] Warning: an error occured when passing 'parline' to the par file in 'bin'\n")
                continue

            success = self.pass_eos(eosdata,eosinfo)
            if(success == False):
                if(self.debug):
                    print(self.s4+"[run_iso] Warning: an error occured when passing EoS to the eos file in 'bin'\n")
                continue

            success = self.run_parab_val()
            if(success == False):
                if(self.debug):
                    print(self.s4+"[run_iso] Warning: an error occured when evaluating ISOV values\n")
                continue

            parab_file_inst = iop.flat_file_grab(self.cmv.joinNode(self.BINPATH,"IsoVals.don"))
            success = iop.flat_file_write(self.cmv.joinNode(self.DATPATH,"isov_"+id),parab_file_inst)
            del parab_file_inst


        print("  ")
        while(True):
            answer = raw_input(self.s4+"Do you want to calculate the chiral cutoff error [yes/no]? ")
                if(answer.lower() == 'yes'):
                    err_opt = True
                    break
                elif(answer.lower() == 'no'):
                    err_opt = False
                    break
                else:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not be parsed...")
                    print(self.s4+"please try again, answering only with 'yes' or 'no'\n")

        if(err_opt):
            self.chiral_cutoff_error()
        return True


    def run_phenom(self):

        print(" ")
        print(self.s4+"Phenomenological evaluation\n")

        isym_emp = 0
        isnm = 0
        k0 = 220
        rho0 = 0.16

        id = 'phn.don'
        nread = 0

        lines = flat_file_grab(self.cmv.joinNode(self.BINPATH,'den.don'))
        n = len(lines)

        phenom_eos_dict = {'mic':mic, 'isym_emp':isym_emp, 'isnm':isnm, 'k0':k0, 'rho0':rho0}
        eosinfo = id, nread

        parline = self.create_parline(eosinfo, **phenom_eos_dict)

        success = self.pass_parline(parline)
        if(success == False):
            if(self.debug):
                print(self.s4+"[run_iso] Warning: an error occured when passing 'parline' to the par file in 'bin'\n")
            continue

        success = self.run_phenom_val()
        if(success == False):
            if(self.debug):
                print(self.s4+"[run_iso] Warning: an error occured when evaluating ISOV values\n")
            return False

        phen_file_inst = iop.flat_file_grab(self.cmv.joinNode(self.BINPATH,"IsoVals.don"))
        success = iop.flat_file_write(self.cmv.joinNode(self.DATPATH,"isov_"+id),phen_file_inst)
        del phen_file_inst


        print("  ")
        while(True):
            answer = raw_input(self.s4+"Do you want to calculate the chiral cutoff error [yes/no]? ")
                if(answer.lower() == 'yes'):
                    err_opt = True
                    break
                elif(answer.lower() == 'no'):
                    err_opt = False
                    break
                else:
                    print(" ")
                    print(self.s4+"Error: '"+answer+"', could not be parsed...")
                    print(self.s4+"please try again, answering only with 'yes' or 'no'\n")

        if(err_opt):
            self.chiral_cutoff_error()
        return True















