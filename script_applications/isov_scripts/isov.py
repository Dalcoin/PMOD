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


class isov(object):

    def __init__(self, initialize = True, kernel = 'linux'):

        # Constants
        self.s4 = "    "

        # File and folder names

        self.INITIAL_DIR = 'ISOV'
        self.INITIAL_PATH = ''

        self.PAR_FILE_NAME = 'par.don'
        self.VAL_FILE_NAME = 'nucleus.don'

        self.SRCFILE = 'src'
        self.srcpath = ''

        self.BINFILE = 'bin'
        self.binpath = ''

        self.DATFILE = 'dat'
        self.datpath = ''

        self.EOSDIR = 'eos'
        self.eospath = ''

        self.PARFILE = 'parameters.don'
        self.parpath = ''

        self.options = 'options.don'
        self.optpath = ''

        self.OPTPARS = 'opt_par.etr'
        self.SKINVAL = 'skin.srt'

        # Regex codes
        DIGIT    = "(\d+)"
        DIGITSPC = DIGIT+"\s+"
        FLOATER  = "(\d+.+\d*)\s*"

        # Compiling regex code
#        self.AZPAIRS = re.compile("\s*AZpairs\s*:\s*([T,F,t,f]\D+)")

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
