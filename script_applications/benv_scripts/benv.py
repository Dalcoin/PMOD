import sys
import os
import subprocess
import re
import time

import ioparse as iop 
import strlist as strl 
import cmdline as cml 
#import cmdutil as cmu
import mathops as mops


class benv(object):

    def __init__(self, initialize = True, kernel = 'linux'):

        # Constants
        self.s4 = "    "

        # File and folder names  

        self.INITIAL_DIR = 'BENV'
        self.INITIAL_PATH = ''
  
        self.PAR_FILE_NAME = 'par.don'
        self.VAL_FILE_NAME = 'nucleus.don'
             
        self.BINFILE = 'bin' 
        self.SRCFILE = 'src' 
        self.DATFILE = 'dat'
        self.binpath = ''
              
        self.PARSFILE = 'parameters.don'
        self.parspath = ''

        self.SKVLFILE = 'skval.don'
        self.skvlpath = ''
           
        self.EOSDIR = 'eos'
        self.eospath = ''

        self.OPTPARS = 'opt_par.etr'
        self.SKINVAL = 'skin.srt'

        # Regex codes
        DIGIT    = "(\d+)"
        DIGITSPC = DIGIT+"\s+"
        FLOATER  = "(\d+.+\d*)\s*"

        # Compiling regex code
        self.INCLOOP = re.compile("\s*INCloop\s*:\s*([T,F,t,f]\D+)") 
        self.AZPAIRS = re.compile("\s*AZpairs\s*:\s*([T,F,t,f]\D+)")
        self.MIRRORS = re.compile("\s*Mirrors\s*:\s*([T,F,t,f]\D+)")
        self.INITPAR = re.compile("\s*Initpar\s*:\s*([T,F,t,f]\D+)")
        self.EOSPARS = re.compile("\s*EOSpars\s*:\s*([T,F,t,f]\D+)") 
        self.EOSGRUP = re.compile("\s*EOSgrup\s*:\s*([T,F,t,f]\D+)")    
           
        self.PAIRS = re.compile("\s*(\d+),(\d+)")
        self.LOOPS = re.compile("\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)")
        self.PARCM = re.compile("\s*"+9*DIGITSPC+FLOATER+DIGIT)      
        self.PARGP = re.compile("\s*"+5*DIGITSPC+FLOATER+DIGIT)    
 
        # debug-----------------
        self.time_Start = time.time()
         
        # Initialization
        self.INITIALIZATION = False

        # Initial Pathway Errors
        self.PARSFILE_PATH_ERROR = False
        self.SKVLFILE_PATH_ERROR = False
        self.EOSDIR_PATH_ERROR = False
        self.BINDIR_PATH_ERROR = False

        # Set Pathways

        self.INTERNAL_CML_SET = False
        self.PARSFILE_PATH_SET = False
        self.SKVLFILE_PATH_SET = False 
        self.EOSDIR_PATH_SET = False 
        self.BINDIR_PATH_SET = False 
        self.SUBPROCESS_PATH_SET = False
        self.INITIAL_PAR_SET = False

        # Other intial task errors
        self.INTERNAL_CML_ERROR = False
        self.SUBPROCESS_PATH_ERROR = False
        self.PAR_FORMAT_ERROR = False

        # Skval errors
        self.SKVAL_FORMAT_ERROR = False 
        self.SKVAL_CONTROL_ERROR = False

        # EoS errors 
        self.EOS_SPLIT_FILE_ERROR = False
        self.EOS_FILE_FORMAT_ERROR = False 
        self.EOS_SPLIT_PARSE_ERROR = False
        self.EOS_PASS_ERROR = False
        self.INITIAL_PARS_ERROR = False

        # Execution Errors
        self.EXIT_ERROR = False

        # BENV objects and variables---------------|
          
        # initial data 
        self.initial_pars = ''
        self.initial_a = 0
        self.initial_z = 0           

        # skval functionality
        self.incloop = False  
        self.azpairs = False
        self.mirrors = False 
        self.initpar = False
        self.eospars = False        
        self.eosgrup = False

        # internal shell command line
        self.cmv = object()   
        self.cmvutil = object()

        # variables
        self.run_time = 0

        #initialization (optional)            
        if(initialize):
            self.INITIALIZATION = True

            print(" ")
            print("Initialization option detected")
            print("Error messages and test results shown below")
            print("Initialization sequence will now begin...\n")

            try:
                self.cmv = cml.PathParse(kernel)
#                self.cmvutil = cmu.cmdUtil(self.cmv)
                self.INITIAL_PATH = self.cmv.varPath
                self.INTERNAL_CML_SET = True
            except:
                print("[benv] Error: internal shell command object 'cmv' could not be created\n")
                self.INTERNAL_CML_ERROR = True

            self.set_par_path()
            self.set_skvl_path()
            self.set_eos_path()
            self.set_bin_dir()

            if(self.PARSFILE_PATH_ERROR):
                print("[benv] Error: no path found for the 'PARSFILE' file")
                print("No attempt will be made to get values from 'PARSFILE'\n")
            else:
                self.initial_pars, self.initial_vals = self.data_from_pars()
                if((self.initial_pars, self.initial_vals) == ('','')):
                    print("[benv] Error: 'PARSFILE' file contains invalid formatting\n")
                    self.PAR_FORMAT_ERROR = True
                else:
                    self.initial_pars = self.initial_pars[0]

            try: 
                self.initial_a, self.initial_z = strl.str_to_list(self.initial_vals[-1], filtre=True) 
                self.initial_a = int(float(strl.str_clean(self.initial_a)))
                self.initial_z = int(float(strl.str_clean(self.initial_z)))     
                self.INITIAL_PAR_SET = True           
            except:
                print("[benv] Error: failure to parse isotope values A and Z to integers (the last parameter line)\n")
                self.PAR_FORMAT_ERROR = True
         
            self.assess_initialization() 
            print("Initialization sequence complete.\n")
            if(self.EXIT_ERROR):
                print("A fatal error was detected in the initialization sequence...the script will now terminate\n")
                self.exit_function("during initalization...see E-level error checks for details")         
            else: 
                print("Runtime warnings and errors printed below: \n")
          
    def exit_function(self, action_msg, failure=True):
        if(failure):
            print("ExitError: 'BENV' failed "+action_msg)
        print("Run Number upon exit:  "+str(self.run_time))
        print("Script run-time :  "+str(time.time()-self.time_Start))
        print("   ")
        sys.exit()

    def assess_initialization(self):
             
        err0 = self.INTERNAL_CML_ERROR
        err1 = self.PARSFILE_PATH_ERROR 
        err2 = self.SKVLFILE_PATH_ERROR
        err3 = self.EOSDIR_PATH_ERROR
        err4 = self.BINDIR_PATH_ERROR 
        err5 = self.SUBPROCESS_PATH_ERROR 
        err6 = self.PAR_FORMAT_ERROR

        path0 = self.INTERNAL_CML_SET 
        path1 = self.PARSFILE_PATH_SET 
        path2 = self.SKVLFILE_PATH_SET 
        path3 = self.EOSDIR_PATH_SET  
        path4 = self.BINDIR_PATH_SET 
        path5 = self.SUBPROCESS_PATH_SET
        path6 = self.INITIAL_PAR_SET
             
        time.sleep(0.5)
        print(" ")
        if(err0):
            print(self.s4+"E0 Internal Command Line Test :          Failed")
        else:
            if(path0):
                print(self.s4+"E0 Internal Command Line Test :          Succeeded") 
            else:
                print(self.s4+"E0 Internal Command Line Test :          ...command line not set")     
        time.sleep(0.5)             
           
        if(err1):
            print(self.s4+"E1 Parameter File Path Test :            Failed")
        else:   
            if(path1):         
                print(self.s4+"E1 Parameter File Path Test :            Succeeded") 
            else:
                print(self.s4+"E1 Parameter File Path Test :            ...path not found")      
        time.sleep(0.5)          

        if(err2):
            print(self.s4+"E2 SKVAL File Path Test :                Failed")
        else:
            if(path2):
                print(self.s4+"E2 SKVAL File Path Test :                Succeeded") 
            else:
                print(self.s4+"E2 SKVAL File Path Test :                ...path not found") 
        time.sleep(0.5)

        if(err3):
            print(self.s4+"E3 EoS Directory Pathway Test :          Failed")
        else:
            if(path3):
                print(self.s4+"E3 Eos Directory Pathway Test :          Succeeded") 
            else:
                print(self.s4+"E3 Eos Directory Pathway Test :          ...path not found") 
        time.sleep(0.5)

        if(err4):
            print(self.s4+"E4 Binary Directory Path Test :          Failed")
        else:
            if(path4):
                print(self.s4+"E4 Binary Directory Path Test :          Succeeded") 
            else:
                print(self.s4+"E4 Binary Directory Path Test :          ...path not found")             
        time.sleep(0.5)

        if(err5):
            print(self.s4+"E5 Setting Binary Directory as default : Failed")
        else:
            if(path5):
                print(self.s4+"E5 Setting Binary Directory as default : Succeeded") 
            else:
                print(self.s4+"E5 Setting Binary Directory as default : Skipped")                 
        time.sleep(0.5)

        if(not err1):
            if(err6):
                print(self.s4+"E6 Parsing inital parameter values :     Failed")
            else:
                if(path6):
                    print(self.s4+"E6 Parsing inital parameter values :     Succeeded")  
                else:
                    print(self.s4+"E6 Parsing inital parameter values :     Skipped")                         
        time.sleep(0.5)                      

        print(" ")
        if(err0 or err1 or err4):
            print(self.s4+"Fatal Error Test: Failed")
            self.EXIT_ERROR = True
        else:
            print(self.s4+"Fatal Error Test: Succeeded")
        print(" ")
        time.sleep(0.5)
        
        return True

    def exit_error_check(self):
        pass    
             
    def clear_data_folder(self):
        if(not self.INTERNAL_CML_SET):
            print(self.s4+"[clear_data_folder] Error: internal CMD line has not yet been initialized\n")
            return False 
         
        success, value = self.cmv.cmd("cd "+self.DATFILE)
        if(not success):
            print(self.s4+"[clear_data_folder] Error: Could not access data folder\n")
            return False 
          
        if(self.cmv.varPath_Dir == self.DATFILE):
            if(len(self.cmv.varPath_Contains) > 0):
                print(self.s4+"[clear_data_folder] Warning: files were found in the data file, the files will be cleared\n")
            while(len(self.cmv.varPath_Contains) > 0):
                self.cmv.cmd("rm "+self.cmv.varPath_Contains[0])

        success, value = self.cmv.cmd("cd ..")
        return success

   
    def move_results_to_data_folder(self, move_List = ['Pars.srt','Vals.srt']):
        if(not self.INTERNAL_CML_SET):
            print(self.s4+"[clear_data_folder] Error: internal CMD line has not yet been initialized\n")
            return False          

        n = len(move_List)
        
        move_String = '' 
        if(self.DATFILE in self.cmv.varPath_Contains):
            
            self.cmv.cmd("cd "+self.BINFILE)
            for i,file in enumerate(move_List):
                if(i == n-1):
                    move_String = move_String+file
                else:
                    move_String = move_String+file+';'
            self.cmv.cmd("mv "+move_String+" ..")
            self.cmv.cmd("cd ..")
            move_String = '' 
            for i,file in enumerate(move_List):
                if(i == n-1):
                    move_String = move_String+file
                else:
                    move_String = move_String+file+';'
            self.cmv.cmd("mv "+move_String+" "+self.DATFILE)
        else:
            print(self.s4+"[clear_data_folder] Error: data folder could not be accessed\n")
            return False                 
        
        return True


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


    ##############################################################
    # functions to set the internal pathway strings used in BENV #
    ############################################################## 

    def set_par_path(self):
        success, data = self.cmv.cmd("dir "+self.PARSFILE)
        if(not success):
            print(self.s4+"[set_par_path] Error: failure to get path for file named: " )
            print(self.s4+"'"+self.PARSFILE+"'\n")
            self.PARSFILE_PATH_ERROR = True 
            return False         
        self.parspath = data[0]
        self.PARSFILE_PATH_SET = True
        return True
     
    def set_skvl_path(self):
        success, data = self.cmv.cmd("dir "+self.SKVLFILE)
        if(not success):
            print(self.s4+"[set_skvl_path] Warning: failure to get path for file named: ")
            print(self.s4+"'"+self.SKVLFILE+"'\n")
            self.SKVLFILE_PATH_ERROR = True
            return False
        self.skvlpath = data[0]
        self.SKVLFILE_PATH_SET = True
        return True       

    def set_eos_path(self):
        success, data = self.cmv.cmd("dir "+self.EOSDIR)
        if(not success):
            print(self.s4+"[set_eos_path] Warning: failure to get path for file named: ")
            print(self.s4+"'"+self.SKVLFILE+"'\n")
            self.EOSDIR_PATH_ERROR = True
            return False
        self.eospath = data[0]      
        self.EOSDIR_PATH_SET = True       
        return True

    def set_bin_dir(self):
        success, output = self.cmv.cmd("cd "+self.BINFILE)
        if(not success):
            print(self.s4+"[set_bin_dir] Error: failure to access "+self.BINFILE+"\n")
            self.BINDIR_PATH_ERROR = True
            return False
        
        success, output = self.cmv.cmd("pwd")
        if(not success):
            print(self.s4+"[set_bin_dir] Error: failure to access "+self.BINFILE+" pathway\n")
            self.BINDIR_PATH_ERROR = True
            return False
        else:
            binpath = output 
        self.BINDIR_PATH_SET = True

        self.binpath = binpath  # the pathway for the bin directory is loaded    
        try:  
            os.chdir(binpath)       # commands executed with subprocess will run in the bin directory
            self.SUBPROCESS_PATH_SET = True
        except:
            print(self.s4+"[set_bin_dir] Error: could not change script directory to '"+str(binpath)+"'\n")
            self.SUBPROCESS_PATH_ERROR = True
            return False            
  
        success, output = self.cmv.cmd("cd ..")   
        if(not success):
            print(self.s4+"[set_bin_dir] ExitError: failure to reaccess "+self.BINFILE+"\n")
            return False

        return True


    ##################################################################################################
    # functions dealing with the 'parameters.don', 'par.don' and 'nucleus.don' (or equivalent) files #
    ##################################################################################################      
    
    def data_from_pars(self, raw = False):        
        try:
            lines = iop.flat_file_grab(self.parspath)
        except:
            print(self.s4+"[data_from_pars] Error: could not get parameters from 'parspath'")
            print(self.s4+"Error occured in the ioparse function [flat_file_grab]")
            print(self.s4+"Pathway: '"+str(self.parspath)+"'\n")
            return ('','')

        if(lines == False):
            print(self.s4+"[data_from_pars] Error: could not get parameters from 'parspath'")
            print(self.s4+"Pathway: '"+str(self.parspath)+"'\n")
            return ('','')

        try:
            par = [lines[0]]
            val = lines[1:4]
        except:
            print(self.s4+"[data_from_pars] Error: check formatting of the file found at 'parspath'")
            print(self.s4+"attempted to format lines of the file found at: '"+str(self.parspath)+"'\n")
            return ('','') 
             
        if(raw):
            return lines
        else:
            return (par, val)


    def parline_style_convert(self, parline):
    
        if(isinstance(parline,str)):
            try:
                outpar = filter(None,[i.rstrip() for i in strl.str_to_list(parline)])
            except:
                print(self.s4+"[parline_style_convert] Error: could not convert 'parline' string to list\n")
                outpar = False
        elif(isinstance(parline,(list,tuple))):
            try:
                outpar = strl.array_to_str(filter(None,parline))
            except: 
                print(self.s4+"[parline_style_convert] Error: could not format 'parline' array to list\n")
                outpar = False
        else:
            print(self.s4+"[parline_style_convert] Error: input 'parline' must be either an array or string")
            print(self.s4+"Attempt to convert 'par' parameter line has failed\n")
            outpar = False 
        return outpar  

    
    def create_pars_line(self, eos, 
                         density = 2,
                         microscopic = True, 
                         e0_rho0 = True,
                         phenom_esym = False,
                         k0 = 220, 
                         rho0 = 0.16,
                         fff = 65,
                         *lengths):

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

        pos_9  = k0
        pos_10 = rho0
        pos_11 = fff

        lens = [n for n in lengths] 
        n = len(lens) 
        
        if(n == 0 and mic == 1):
            print(self.s4+"[create_pars_line] Error: if a microscopic eos is chosen, file length(s) must be defined")
            return False  
        if(mic == 1 and pos_3 == 0 and n < 1):
            print(self.s4+"[create_pars_line] Error: if a combined eos is chosen, the file length must be defined")
            return False         
        elif(mic == 1 and pos_3 == 1 and n < 2):
            print(self.s4+"[create_pars_line] Error: if a seperate eos is chosen, file lengths must be defined (e0 first then e1)")
            return False                  
        elif(mic == 1 and pos_3 == 2 and n < 1):
            print(self.s4+"[create_pars_line] Error: if a symmetric eos is chosen, the file length must be defined")
            return False     
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
        outline = strl.array_to_str(outlist)
               
        return outline      
        

    def format_pars_data(self, parline, a, z, parform = 'str'):
        '''
        Takes a valid 'par.don' string and nucleus denoted by integers (A,Z)
        '''
        
        if(parform == 'array' or parform == 'list' or parform == 'tuple'):
            parline = array_to_str(parline, endline=True)
        else:
            if(isinstance(parline,str)):
                if('\n' in parline):
                    pass 
                else:
                    parline = parline + '\n'
            else:
                print(self.s4+"[format_pars_data] TypeError: 'parline' type does not match 'parform' \n")
                return False
         
        divs = "64 64 64\n"
        lims = "0.0 20.0\n" 
        az = str(a)+'  '+str(z)+'\n'
        return [parline, divs, lims, az] 

    def data_to_pars(self, dataline):        
        success = iop.flat_file_write(self.parspath, dataline)
        if(not success):
            print(self.s4+"[data_to_pars] Errors: failure to write 'dataline'")
            print(self.s4+"Pathway: '"+str(self.parspath)+"'\n")
        return success

    def pass_pars(self, pars):
        '''
        Passes benv parameters to 'par.don' file located in 'bin'
        
        pars takes the form: [see read-me for details]

            n  nden nread n0 n1 mic isnm k0  rho0 fff
            11 2    0     19 19 0   1 0  220 0.16 65  

        '''
          
        #check on 'pars'
        if(isinstance(pars,(list,tuple))):
            parslist = pars
        elif(isinstance(pars,str)):
            parslist = [pars]
        else:
            print(self.s4+"[pass_pars] Error: 'pars' must be an array or string")
            self.exit_function("running checks on 'pars'")
                 
        par_file_path = self.cmv.joinNode(self.binpath,self.PAR_FILE_NAME)   
        success = iop.flat_file_write(par_file_path,parslist) 
        if(not success):
            print(self.s4+"[pass_pars] ExitError: failure when writing the string(s): \n")
            for i in parslist:
                print(self.s4+self.s4+"'"+str(i)+"'")
            print(" ")
            print(self.s4+"to the path: ")
            print(self.s4+str(par_file_path)+"'\n") 
            return False
        return True
             

    def pass_vals(self, val_list): 
         
        #check on 'val_list'
        if(not isinstance(val_list,(list,tuple))):
            print(self.s4+"[pass_vals] Error: 'val_list' must be an array")
         
        val_file_path = self.cmv.joinNode(self.binpath,self.VAL_FILE_NAME)  

        success = iop.flat_file_write(val_file_path,val_list) 
        if(not success):
            print(self.s4+"ExitError: failure when writing the string: \n")
            for i in val_list:
                print(self.s4+self.s4+str(i)+"'")
            print(" ")
            print(self.s4+"to the path: ")
            print(self.s4+"    '"+str(val_file_path)+"'\n") 
            return False
        return True     
            

    #########################################
    # functions dealing with the skval loop #
    #########################################                               
              
    def get_skval_data(self):
        '''
        Gets skval data from the internal pathway (which must be set prior)
        
        Do not call this function unless the skval data file will be available in your script   
        '''     
        if(self.SKVLFILE_PATH_SET == False):
            print(self.s4+"[get_skval_data] Error: skval file pathway not set\n")
            return False
              
        try:
            lines = iop.flat_file_grab(self.skvlpath, scrub = True)
        except:
            lines = False 
        if(lines == False):
            print(self.s4+"[get_skval_data] IOPError: failure to access file")
            print(self.s4+"Pathway:  '"+str(self.skvlpath)+"'\n") 
         
        return lines 
       
         
    def format_skval_data(self, lines):
          
        try:
            skval_lines = list(lines)          
        except: 
            print(self.s4+"[format_skval_data] Error: input 'lines' should be a python array")
            return False
         
        
        # variables   
        incloop, azpairs, mirrors, initpar, eospars, eosgrup  = False, False, False, False, False, False
        incb, azpb, mirb, intp, newb, eosg = True, True, True, True, True, True  
          
        n = len(skval_lines)
        npreamble = -1

        # Parsing Options from SKVAL             
        for i in xrange(n):
            if(not isinstance(skval_lines[i],str)):
                print_Text = " entry of 'skval_lines' is not a string\n"
                print(self.s4+"[format_skval_data] Warning: the "+strl.print_ordinal(str(i+1))+print_Text)             
                continue 
            if(incb):
                incloop = self.INCLOOP.findall(skval_lines[i])
                if(incloop != []):
                    self.incloop = (incloop[0].lower() == 'true')
                    incb = False             
            if(azpb):
                azpairs = self.AZPAIRS.findall(skval_lines[i])
                if(azpairs != []):
                    self.azpairs = (azpairs[0].lower() == 'true')
                    azpb = False                
            if(mirb):
                mirrors = self.MIRRORS.findall(skval_lines[i])  
                if(mirrors != []):
                    self.mirrors = (mirrors[0].lower() == 'true')
                    mirb = False 
            if(intp):
                initpar = self.INITPAR.findall(skval_lines[i])  
                if(initpar != []):
                    self.initpar = (initpar[0].lower() == 'true')
                    intp = False 
            if(newb):
                eospars = self.EOSPARS.findall(skval_lines[i])  
                if(eospars != []):
                    self.eospars = (eospars[0].lower() == 'true')
                    newb = False 
            if(eosg):
                eosgrup = self.EOSGRUP.findall(skval_lines[i])  
                if(eosgrup != []):
                    self.eosgrup = (eosgrup[0].lower() == 'true')
                    eosg = False 


                 
            if(i+1 == n and not all([not incb, not azpb, not mirb, not newb])):
                if(incb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'INCloop' in 'skval_lines'\n")  
                if(azpb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'AZpairs' in 'skval_lines'\n")
                if(mirb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'Mirrors' in 'skval_lines'\n")  
                if(intp):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'Initpar' in 'skval_lines'\n")  
                if(newb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'EOSpars' in 'skval_lines'\n")  
                if(eosg):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'EOSgrup' in 'skval_lines'\n")   
            elif(all([not incb, not azpb, not mirb, not intp, not newb, not eosg])): 
                npreamble = i    
                break    
            else:
                pass
         
        if(n > npreamble >= 0):
            skval_lines = skval_lines[npreamble:] 
          
        pars = []
        doubles = []
        loop = []
        output = ()
                  
           
        if(self.incloop and self.azpairs):
            print(self.s4+"[format_skval_data] Warning: both skval looping and nuclei pairs detected")
            print(self.s4+"                             skval looping takes precedent over paring\n")
            self.SKVAL_CONTROL_ERROR = True
         
        if(self.incloop):
            for i in xrange(len(skval_lines)):

                if(not isinstance(skval_lines[i],str)):
                    print_Text = " entry of 'skval_lines' is not a string\n"
                    print(self.s4+"[format_skval_data] Warning: the "+strl.print_ordinal(str(i+1))+print_Text)             
                    continue                     
                   
                looplist = self.LOOPS.findall(skval_lines[i])
                if(len(looplist) > 0):
                    loop.append(looplist[0])
                if(self.eospars):
                    looplist = self.EOSPARS.findall(skval_lines[i])
                    if(len(looplist)>0):
                        pars.append(looplist[0])
                        
            if(len(loop) > 0):
                if(len(loop) > 1):
                    print(self.s4+"[format_skval_data] Warning: Multiple loop options detected, only the first one will be exectued\n")
                loop_data = loop[0]                     
                loop_type = "loop"
                self.azpairs = False 
            else:                    
                print(self.s4+"[format_skval_data] Warning: Loop option selected; no loops detected, defaulting to a pair-wise search\n")
                self.SKVAL_FORMAT_ERROR = True   
                self.azpairs = True 
                self.incloop = False             
              
        if(self.azpairs and self.incloop == False):
            for i in xrange(len(skval_lines)):

                if(not isinstance(skval_lines[i],str)):
                    print_Text = " entry of 'skval_lines' is not a string\n"
                    print(self.s4+"[format_skval_data] Warning: the "+strl.print_ordinal(str(i+1))+print_Text)             
                    continue    
                    
                double = self.PAIRS.findall(skval_lines[i])
                if(len(double)>0):
                    if(len(double)>1): 
                        print(self.s4+"[format_skval_data] Warning: More than one 'pair' value found in the string: ")
                        print(self.s4+"'"+str(skval_lines[i])+"'")
                        print(self.s4+"Only the first pair will be appended to the stack\n")
                    var = double[0]
                    var = map(lambda x: float(strl.str_clean(x)), var)
                    doubles.append(var)

                if(self.eospars):
                    looplist = self.EOSPARS.findall(skval_lines[i])
                    if(len(looplist)>0):
                        pars.append(looplist[0])

            if(len(doubles) > 0):
                loop_data = doubles
                loop_type = "pair"
            else:                    
                self.SKVAL_FORMAT_ERROR = True
                print(self.s4+"[format_skval_data] Error: No 'pair' values could be found\n")
                return False
                 
        if(not self.incloop and not self.azpairs):
            print(self.s4+"[format_skval_data] Warning: No skval functionality detected...\n") 
            return False
        
        output = (loop_data,loop_type,pars)                           
        return output  


    def skval_loop_line_parse(self, line):

        
        if(isinstance(line,str)):      
            loop = strl.str_to_list(line, filtre=True)
            if(loop == False or len(loop) < 4):
                print(self.s4+"[skval_loop_line_parse] Error: couldn't coerce input string, 'line' into array of at least 4 values\n")
                return False
        elif(isinstance(line,(list,tuple))):
            if(len(line) < 4):
                print(self.s4+"[skval_loop_line_parse] Error: if input 'line' is an array it must be at least 4 values long\n")
                return False
            else:
                loop = line 
        else:
            print(self.s4+"[skval_loop_line_parse] Error: input 'line' must either be a string or an array\n")
            return False
             
        try:
#            output_list = [int(loop[0]), int(loop[1]), int(loop[2]), bool(int(loop[3])), bool(int(loop[4])), bool(int(loop[5]))]
            output_list = [int(loop[0]), int(loop[1]), int(loop[2]), bool(int(loop[3]))]
        except:
            print(self.s4+"[skval_loop_line_parse] Error: could not coerce 'loop' list into a skval-loop list\n")
            return False
             
        return output_list


    ###################################################################################
    # functions dealing with the 'eoses.don', e[x,0,1]_nxlo.don (or equivalent) files #
    ################################################################################### 

    def collect_eos(self):
        '''
        Notes: 
        
            Collects EoS from 'eos' directory 
            This function should only be called once per BENV run 
        
        ''' 

        eos_dir_path = self.cmv.joinNode(self.INITIAL_PATH,self.EOSDIR)
        eos_file_list = self.cmv.contentPath(eos_dir_path)

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
                    

    def format_skval_benv_vals(self, benvals, split = True):
         
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
        
        optpars  = self.data_from_bin(self.OPTPARS,True)
        if(optpars == False):
            self.OPTPARS_ERROR = True                   
         
        skinvals = self.data_from_bin(self.SKINVAL,True)
        if(skinvals == False):
            self.SKINVAL_ERROR = True 
         
        if(clean_Run):
            subprocess.call("rm "+self.OPTPARS, shell = True)
            subprocess.call("rm "+self.SKINVAL, shell = True)

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

                    success = self.data_to_pars(parlines)
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
                 
                success = self.data_to_pars(parlines)
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
             

    def benv_eos_loop(self, reset = True):
    
        benvals_group = []
        benvals_cohort= [] 

        #Get EoS from 'eos' folder 
        eoslist = self.collect_eos()
        if(eoslist == False):
            print(self.s4+"[benv_eos_loop] Error: could not format skval lines from skval file\n")
            return False       

        # Get line strings from 'skval.don' file 
        skval_lines = self.get_skval_data()
        if(skval_lines == False):
            print(self.s4+"[benv_eos_loop] Error: failure to retrieve data from skval file\n")
            return False
           
        # Format skval lines into data list, type string and pars list
        packed_format_skval_data = self.format_skval_data(skval_lines)
        if(packed_format_skval_data == False):
            print(self.s4+"[benv_eos_loop] Error: could not format skval lines from skval file\n")
            return False            
        data, type, pars = packed_format_skval_data  

        # Get parameters par 'Parameter.don' file
        initial_pars = self.initial_pars
        if(initial_pars == ''):
            self.INITIAL_PARS_ERROR = True
            print(self.s4+"[benv_eos_loop] Warning: 'inital_pars' have not been set\n")
         
        # Convert parameters from string to list of floats, assign list to plst 
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
                    formatted_benvals = self.format_skval_benv_vals(benvals)
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
             
            if(self.eosgrup):
                out_Iter = pars   
                inn_Iter = eoslist 
            else: 
                out_Iter = eoslist 
                inn_Iter = pars
             
            for i,out_entry in enumerate(out_Iter):
                for j,inn_entry in enumerate(inn_Iter):

                    if(self.eosgrup):
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
                    formatted_benvals = self.format_skval_benv_vals(benvals)
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

                if(self.eosgrup):
                    benvals_group.append((formatted_benvals,"eos_grup_"+str(jth_entry)+"_"+eosid))
                else:
                    benvals_group.append((formatted_benvals,"par_var_"+str(ith_entry)+"_"+eosid))

            benvals_cohort.append(benvals_group)
            benvals_group = []

        if(reset):
            self.data_to_pars(self.format_pars_data(self.initial_pars, self.initial_a, self.initial_z, parform = 'str'))

        return benvals_cohort