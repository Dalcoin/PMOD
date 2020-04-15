import sys
import os
import subprocess
import re
import time

import ioparse as iop 
import strlist as strl 
import cmdline as cml 
import mathops as mops


class benv:

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
        self.EOSPARS = re.compile("\s*EOSpars\s*:\s*([T,F,t,f]\D+)") 
        self.INITPAR = re.compile("\s*Initpar\s*:\s*([T,F,t,f]\D+)")

           
        self.PAIRS = re.compile("\s*(\d+),(\d+)")
        self.LOOPS = re.compile("\s*(\d+)\s+(\d+)\s+(\d+)\s*")
        self.PARCM = re.compile("\s*"+9*DIGITSPC+FLOATER+DIGIT)      
        self.PARGP = re.compile("\s*"+5*DIGITSPC+FLOATER+DIGIT)    
 
        # debug-----------------
        time_Start = time.time()
         
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
        self.eospars = False        

        # internal shell command line
        self.cmv = object()   
           
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
                self.cmv = cml.path_parse(kernel) 
                self.INITIAL_PATH = self.cmv.var_path
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
             
        print(" ")
        if(err0):
            print(self.s4+"E0 Internal Command Line Test :          Failed")
        else:
            if(path0):
                print(self.s4+"E0 Internal Command Line Test :          Succeeded") 
            else:
                print(self.s4+"E0 Internal Command Line Test :          ...command line not set")                  
           
        if(err1):
            print(self.s4+"E1 Parameter File Path Test :            Failed")
        else:   
            if(path1):         
                print(self.s4+"E1 Parameter File Path Test :            Succeeded") 
            else:
                print(self.s4+"E1 Parameter File Path Test :            ...path not found")                

        if(err2):
            print(self.s4+"E2 SKVAL File Path Test :                Failed")
        else:
            if(path2):
                print(self.s4+"E2 SKVAL File Path Test :                Succeeded") 
            else:
                print(self.s4+"E2 SKVAL File Path Test :                ...path not found") 

        if(err3):
            print(self.s4+"E3 EoS Directory Pathway Test :          Failed")
        else:
            if(path3):
                print(self.s4+"E3 Eos Directory Pathway Test :          Succeeded") 
            else:
                print(self.s4+"E3 Eos Directory Pathway Test :          ...path not found") 

        if(err4):
            print(self.s4+"E4 Binary Directory Path Test :          Failed")
        else:
            if(path4):
                print(self.s4+"E4 Binary Directory Path Test :          Succeeded") 
            else:
                print(self.s4+"E4 Binary Directory Path Test :          ...path not found")             

        if(err5):
            print(self.s4+"E5 Setting Binary Directory as default : Failed")
        else:
            if(path5):
                print(self.s4+"E5 Setting Binary Directory as default : Succeeded") 
            else:
                print(self.s4+"E5 Setting Binary Directory as default : Skipped")                 

        if(not err1):
            if(err6):
                print(self.s4+"E6 Parsing inital parameter values :     Failed")
            else:
                if(path6):
                    print(self.s4+"E6 Parsing inital parameter values :     Succeeded")  
                else:
                    print(self.s4+"E6 Parsing inital parameter values :     Skipped")                         
                      
        print(" ")
        if(err0 or err1 or err4):
            print(self.s4+"Fatal Error Test: Failed")
            self.EXIT_ERROR = True
        else:
            print(self.s4+"Fatal Error Test: Succeeded")
        print(" ")
        
        return True


    def exit_printout(self):
        if(not self.INITIALIZATION):
           print(" ")
           print("Initialization tests: \n")
           self.assess_initialization()
        
        
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
            outpar = filter(None,[i.rstrip() for i in strl.str_to_list(parline)])
        elif(isinstance(parline,(list,tuple))):
            outpar = strl.array_to_str(filter(None,parline))
        else:
            print("[parline_style_convert] Error: input 'parline' must be either an array or string")
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
                print("Error: 'parline' must either be a string or list of strings, set parform to 'list' in the latter case")
                return False
         
        divs = "64 64 64\n"
        lims = "0.0 20.0\n" 
        az = str(a)+'  '+str(z)+'\n'
        return [parline, divs, lims, az] 

    def data_to_pars(self, dataline):        
        success = iop.flat_file_write(self.parspath, dataline)
        if(not success):
            print(self.s4+"[data_to_pars] Errors: failure to write 'dataline' to the following path:")
            print(self.s4+"                       "+str(self.parspath))
        return success

    def get_inital_pars(self):
        return self.initial_pars

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
                 
        par_file_path = self.cmv.pw_join(self.binpath,self.PAR_FILE_NAME)   
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
         
        val_file_path = self.cmv.pw_join(self.binpath,self.VAL_FILE_NAME)  

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
        if(not self.SKVLFILE_PATH_SET):
            print(self.s4+"[get_skval_data] Error: skval file pathway has not yet been set")
            print(self.s4+"                 Set the pathway with the 'set_skval_path' function\n")
            return False
              
        lines = iop.flat_file_grab(self.skvlpath, scrub = True)
        if(not lines):
            print(self.s4+"[get_skval_data] IOPError: failure to access the file '"+str(self.skvlpath)+"'") 
            return False
        return lines 
       
         
    def format_skval_data(self, lines):
          
        skval_lines = list(lines)          
        
        # variables   
        incloop, azpairs, mirrors, eospars, initpar = False, False, False, False, False
        incb, azpb, mirb, newb, intp = True, True, True, True, True  
          
        n = len(skval_lines)
        npreamble = -1

        # Parsing Options from SKVAL             
        for i in xrange(n):
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
            if(newb):
                eospars = self.EOSPARS.findall(skval_lines[i])  
                if(eospars != []):
                    self.eospars = (eospars[0].lower() == 'true')
                    newb = False 
            if(intp):
                initpar = self.INITPAR.findall(skval_lines[i])  
                if(initpar != []):
                    self.initpar = (initpar[0].lower() == 'true')
                    intp = False 

                 
            if(i+1 == n and not all([not incb, not azpb, not mirb, not newb])):
                if(incb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'INCloop' in 'skval_lines'")  
                if(azpb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'AZpairs' in 'skval_lines'")
                if(mirb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'Mirrors' in 'skval_lines'")  
                if(newb):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'EOSpars' in 'skval_lines'")  
                if(intp):
                    print(self.s4+"[format_skval_data] Warning: could not find parameter 'Initpar' in 'skval_lines'")   
            elif(all([not incb, not azpb, not mirb, not newb, not intp])):
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
            print("[format_skval_data] Warning: both skval looping and nuclei pairs detected")
            print("                             skval looping takes precedent over paring\n")
            self.SKVAL_CONTROL_ERROR = True
         
        if(self.incloop):
            for i in skval_lines:
                looplist = self.LOOPS.findall(i)
                if(len(looplist) > 0):
                    loop.append(looplist[0])
                if(self.eospars):
                    looplist = self.EOSPARS.findall(i)
                    if(len(looplist)>0):
                        pars.append(looplist[0])
                        
            if(len(loop) > 0):
                if(len(loop) > 1):
                    print("[format_skval_data] Warning: Multiple loop options detected, only the first one will be exectued")
                loop_data = loop[0]                     
                loop_type = "loop"
                self.azpairs = False 
            else:                    
                print("[format_skval_data] Warning: Loop option selected; no loops detected, defaulting to a pair-wise search")
                self.SKVAL_FORMAT_ERROR = True   
                self.azpairs = True 
                self.incloop = False             
              
        if(self.azpairs and self.incloop == False):
            for i in skval_lines:
                double = self.PAIRS.findall(i)
                if(len(double)>0):
                    if(len(double)>1): 
                        print("[format_skval_data] Warning: More than one 'pair' value found in the string: ")
                        print("                    '"+i+"'")
                        print("            Only the first pair will be appended to the stack")
                    var = double[0]
                    var = map(lambda x: float(strl.str_clean(x)), var)
                    doubles.append(var)
                if(self.eospars):
                    looplist = self.EOSPARS.findall(i)
                    if(len(looplist)>0):
                        pars.append(looplist[0])

            if(len(doubles) > 0):
                loop_data = doubles
                loop_type = "pair"
            else:                    
                self.SKVAL_FORMAT_ERROR = True
                print("[format_skval_data] Error: No 'pair' values could be found")
                 
        else:
            print("[format_skval_data] Error: No skval functionality detected...") 
            loop_data = []
            loop_type = ''
        
        output = (loop_data,loop_type,pars) 
                           
        return output  


    def skval_loop_line_parse(self, line):
        if(not isinstance(line,str)):      
            print("Error: input 'line' must be a string")                  
            self.exit_function("when parsing a skval loop instance")
          
        loop = strl.str_to_list(line, filtre=True)
        if(len(loop) != 6):
            print("[skval_loop_line_parse] Error: there should be exactly 6 entries in 'line'")
            self.exit_function("when parsing a skval loop instance")
            
        try:
            output_list = [int(loop[0]), int(loop[1]), int(loop[2]), bool(int(loop[3])), bool(int(loop[4])), bool(int(loop[5]))]
        except:
            print("[skval_loop_line_parse] Error: could not coerce 'loop' list into a skval-loop list")
            self.exit_function("when parsing a skval loop instance")

        return output_list


    ###################################################################################
    # functions dealing with the 'eoses.don', e[x,0,1]_nxlo.don (or equivalent) files #
    ################################################################################### 

    def collect_eos(self):
        '''
        Collects EoS from 'eos' directory 
        This function should only be called once per BENV run 
        
 
        ''' 

        eos_dir_path = self.cmv.pw_join(self.INITIAL_PATH,self.EOSDIR)
        eos_file_list = self.cmv.pw_contain(eos_dir_path)

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
            head = "The following files are not valid 'eos' files:"
            strl.format_fancy(egshock,header=head)                 
            
        for i in exfiles:
            file_path = self.cmv.pw_join(eos_dir_path,i)  
            ex = iop.flat_file_intable(file_path) 
            if(ex != False):
                if(len(ex) != 3):
                    print("[collect_eos] Error: the file '"+str(i)+"' did not have three equal data columns")
                    self.EOS_FILE_FORMAT_ERROR = True
                    continue 
                eoslist.append((ex,i))
            else:
                print("[collect_eos] Error: could not read the file '"+str(i)+"' as a table")
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
             
            e0_file_path = self.cmv.pw_join(eos_dir_path,i)  
            if(e1name in e1files):
                e1pack = True
                e1_file_path = self.cmv.pw_join(eos_dir_path,e1name)     

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
            eos_path = self.cmv.pw_join(self.binpath,'ex_nxlo.don') 
            success = iop.flat_file_write(eos_path, formatted_eos[1])  
            if(not success): 
                print("[pass_eos] Error: when writing to 'ex_nxlo.don'")          
        elif(type == 1):
            e0_path = self.cmv.pw_join(self.binpath,'e0_nxlo.don') 
            success = iop.flat_file_write(e0_path, formatted_eos[1])
            if(not success): 
                print("[pass_eos] Error: when writing to 'e0_nxlo.don'")   
            e1_path = self.cmv.pw_join(self.binpath,'e1_nxlo.don') 
            success = iop.flat_file_write(e1_path, formatted_eos[2])      
            if(not success): 
                print("[pass_eos] Error: when writing to 'e1_nxlo.don'")   
        elif(type == 2):
            e0_path = self.cmv.pw_join(self.binpath,'e0_nxlo.don') 
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
                      
        filepath = self.cmv.pw_join(self.binpath,file_Name)
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
                    

    def format_skval_benv_vals(self, benvals, split = False):
         
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
            

    def clean_up(self):
        
        if(self.cmv.var_path_list[-1] != self.BINFILE):          
            success, output = self.cmv.cmd("cd "+self.BINFILE)
            if(not success):
                print("[clean_up] ExitError: failure to access "+self.BINFILE)
                self.exit_function("while changing directories")

        subprocess.call("rm CONSOLE.txt",shell = True)         
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
        return ((optpars,skinvals))
        
      
    def skval_loop(self, parline, skval_data, skval_type):
        ''' 
        Notes: 

        '''
    
        benvals = []    
         
        # Parsing data from the skval data file, default : 'skval.don' 
        if(not isinstance(skval_data,(list,tuple)) or not isinstance(skval_type,str)):
            print("[skval_loop] TypeError: check function input variables")
            self.exit_function("while attempting to execute skval looping")  
        else:
            data = list(skval_data)            
            type = skval_type              
        
        # 'type' determines if BENV values are computed by a skval loop or individual nuclei   
        if(type == 'loop'):        
            skval_list = self.skval_loop_line_parse(data)
            if(skval_list[3]):
                inv = -1 
            else:
                inv = 1                     
            for i in xrange(skval_list[0]):
                ax = self.initial_a+inv*skval_list[2]*(j+1)
                for j in xrange(skval_list[1]): 
                    zx = self.initial_z+inv*(skval_list[2])*(j+1)                                    
                    parlines = self.format_pars_data(parline, ax, zx)       
                    self.data_to_pars(parlines)
                    results = self.run_once()
                    benvals.append((results,(ax,zx)))                                                                       
        elif(type == 'pair'):   
            for i in data: 
                parlines = self.format_pars_data(parline, i[0], i[1])
                self.data_to_pars(parlines)
                results = self.run_once()
                benvals.append((results,i))                
        else:
            print("[skval_loop] ValueError: 'type' value not reconignized")
            self.exit_function("while attempting to execute skval looping") 
                
        return benvals
             

    def benv_eos_loop(self, reset = True):
    
        benvals_group = []
        benvals_cohort= [] 

        # Get parameters par 'Parameter.don' file
        initial_pars = self.get_inital_pars()
        # Convert parameters from string to list of floats, assign list to plst 
        pl = self.parline_style_convert(initial_pars) 
        plst = [pl[1],pl[5],pl[6],pl[7],pl[8],pl[9],pl[10]]   
    
        # Get line strings from 'skval.don' file 
        skval_lines = self.get_skval_data()

        # Format skval lines into data list, type string and pars list
        data, type, pars = self.format_skval_data(skval_lines)    
        #Get EoS from 'eos' folder 
        eoslist = self.collect_eos()  

        # cycle through each EoS
        for entry in eoslist:
            # Convert each EoS object into eos data (eos_obj) and eos id (eosid)  
            eos_obj,eosid = self.format_eos_data(entry, pl=plst)            
            # Set eos data (eos_instance) and 'par.don' line (parline) 
            eos_instance, parline = eos_obj

            # Pass the eos data to the appropriate file  
            success = self.pass_eos(eos_instance)
            if(success == False): 
                print(self.s4+"[benv_eos_loop] RuntimeError: error occured when passing EoS to the bin folder")
                print(self.s4+"This occured on run number: "+str(self.run_time))
                print(self.s4+"This exectution will be terminated, cycling to the next eos...\n"
                continue 

            # Initiate skval loop for given 'parline', 'data' and 'type' and 'parline'
            benvals = self.skval_loop(parline, data, type)

            # Format data returned by skavl loop routine 
            formatted_benvals = self.format_skval_benv_vals(benvals)
            benvals_group.append((formatted_benvals,eosid))

        if(len(pars)>0):
            benvals_cohort.append(benvals_group)
            benvals_group = []
            for i,par in enumerate(pars):
                for entry in enumerate(eoslist):
                    eos_obj,eosid = self.format_eos_data(entry,pl=par)
                    eos_instance, parline = eos_obj
                    self.pass_eos(eos_instance)
                    benvals = self.skval_loop(parline, data, type)
                    formatted_benvals = self.format_skval_benv_vals(benvals)
                    benvals_group.append((formatted_benvals,"par_var_"+str(i)+"_"+eosid))
                benvals_cohort.append(benvals_group)
                benvals_group = []
         
        if(reset):
            self.data_to_pars(self.format_pars_data(self.initial_pars, self.initial_a, self.initial_z, parform = 'str'))
    
        return benvals_group 


 
