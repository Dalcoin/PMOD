#!/usr/bin/env python

'''

programStructure : 

    - Contains a class progStruct

Purpose :

    This file contains the class progStruct which is a 
    part of the programScaffold package. This package
    is meant to facilitate the creation of consistant
    program structure so as to facilitate automation of
    simple shell based programs

File Structure : 

    The file structure described in the programScaffold
    package is shown graphically below :

    1) Three folders are required : 'src', 'bin' and 
       'dat', additional directories may be included but
       are not required.

    2) Three files are required : 'compile.py', 'exe.py',
       'option.don'.

    3) 'src' must contain at least two files, at least 
       one source code file, 'source.src', and a shell
       script which facilitates scripting, 'compile.sh'

    4) 'bin' must contain at least two files, at least
       one binary code file, 'binaries', and a shell
       script which exceutes the binaries.

    5) 'dat' is the folder where the end results of
       the program end up.

    6) 'compile_main.py' invokes the 'compile' script
       in 'pmod' to compile the source code in 'src'
       and move the binaries to the 'bin' directory

    7) 'exe.py' executes the binaries in 'bin'

    8) 'option.don' provides options for changing the
       operation of the binaries in 'bin'

    9) 'pmod' is the package which facilitates this
       program structuring and internal operation
 
                    |--- 'src' -|--- 'source.src'
                    |           |
                    |           |--- 'compile.sh'
                    |
'Main' Directory ---|--- 'bin' -|--- 'binaries'
                    |           |
                    |           |--- 'run.sh'
                    |
                    |--- 'dat' -|--- ''
                    |
                    |--- 'compile_main.py'
                    |
                    |--- 'exe.py'
                    |
                    |--- 'option.don'
                    |
                    |--- 'pmod' -|---'...'

'''

import sys
import os
import subprocess
import re
import time

import pmod.ioparse as iop 
import pmod.strlist as strl 
import pmod.cmdline as cml 
#import pmod.cmdutil as cmu
import pmod.mathops as mops


class progStruct(object):

    def __init__(self, dir_fold_name='BENV',
                       src_fold_name='src',
                       bin_fold_name='bin',
                       dat_fold_name='dat',
                       opt_file_name='option.don',
                       initialize=True,
                       kernel='linux'
                ):

        # Constants

        self.s4 = "    " # spaceing for print

        # File and folder names  

        self.DIRNAME = dir_fold_name
        self.DIRPATH = ''

        self.SRCFOLD = src_fold_name
        self.SRCPATH = ''

        self.BINFOLD = bin_fold_name
        self.BINPATH = ''

        self.DATFOLD = dat_fold_name
        self.DATPATH = ''

        self.OPTFILE = opt_file_name
        self.OPTPATH = ''

        self.FOLDNAME_LIST = [self.SRCFOLD, self.BINFOLD, self.DATFOLD]
        self.FOLDPATH_LIST = [self.SRCPATH, self.BINPATH, self.DATPATH]
        self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))

        self.FILENAME_LIST = [self.OPTFILE]
        self.FILEPATH_LIST = [self.OPTPATH]
        self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))

        self.DIR_FOLDERS = []
        self.DIR_FILES = []

        self.BIN_DICT = {}

        # Regex codes
        RE_DIGIT    = "(\d+)"
        RE_DIGITSPC = DIGIT+"\s+"
        RE_FLOATER  = "(\d+.+\d*)\s*"
        RE_BOOL     = "([T,F,t,f]\D+)"

        # Compiling regex code
        #self.compiled_regex = re.compile("")

        #-------#----------------#-------#
        # debug #                # debug #
        #-------#----------------#-------#

        self.debug = True

        # Run time
        self.time_start = time.time()
        self.time_end = 0.0

        # Initialization
        self.INITIALIZATION = False

        # Pathway Errors
        self.DIRPATH_ERROR = False
        self.SRCPATH_ERROR = False
        self.BINPATH_ERROR = False
        self.DATPATH_ERROR = False
        self.OPTPATH_ERROR = False

        self.FOLDPATH_ERROR_LIST = [self.SRCPATH_ERROR, self.BINPATH_ERROR, self.DATPATH_ERROR]
        self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))

        self.FILEPATH_ERROR_LIST = [self.OPTPATH_ERROR]
        self.FILEPATH_ERROR_DICT = {zip(self.FILENAME_LIST,FILEPATH_ERROR_LIST)}

        # Set Pathways
        self.INTERNAL_CML_SET = False
        self.CML_UTIL_SET = False

        self.DIRPATH_SET = False
        self.SRCPATH_SET = False
        self.BINPATH_SET = False
        self.DATPATH_SET = False
        self.OPTPATH_SET = False

        self.FOLDPATH_SET_LIST = [self.SRCPATH_SET, self.BINPATH_SET, self.DATPATH_SET]
        self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))

        self.FILEPATH_SET_LIST = [self.OPTPATH_SET]
        self.FILEPATH_SET_DICT = {zip(self.FILENAME_LIST,FILEPATH_SET_LIST)}

        # Other intial task errors
        self.INTERNAL_CML_ERROR = False
        self.CML_UTIL_ERROR = False

        # Execution Errors
        self.EXIT_ERROR = False

        # internal shell command line
        self.cmv = object()   
        self.cmvutil = object()

        # internal variables
        self.cycle = 0

        # looping variables
        self.option_menu_lines = []

        #initialization (optional)            
        if(initialize):
            self.INITIALIZATION = True

            print(" ")
            print("Initialization option detected")
            print("Error messages and test results shown below")
            print("Initialization sequence will now begin...\n")

            self.init_internal_pathway()

            # Checking for folders
            self.src_check()
            self.bin_check()
            self.dat_check()

            # Checking for files
            self.opt_check()

            self.assess_initialization()
            self.update_dicts()
            print("Initialization sequence complete.\n")
            if(self.EXIT_ERROR):
                print("A fatal error was detected in the initialization sequence...the script will now terminate\n")
                self.exit_function("during initalization...see E-level error checks for details")
            else:
                print("Runtime warnings and errors will be printed below: \n")


    #--------------------#----------------#--------------------#
    # Verify Directories #                # Verify Directories #
    #--------------------#----------------#--------------------#


    def init_internal_pathway(self):

        if(self.INTERNAL_CML_SET):
            if(self.debug):
                print(self.s4+"[init_internal_pathway] Error: internal pathway already set\n")
            return False
        else:
            try:
                self.cmv = cml.PathParse(kernel)
                self.INTERNAL_CML_SET = True
            except:
                if(self.debug):
                    print(self.s4+"[init_internal_pathway] Error: internal failure to set internal pathway\n")
                self.INTERNAL_CML_ERROR = True
                self.DIRPATH_ERROR = True
                return False
            self.DIR_FOLDERS = self.cmv.varPath_Folders 
            self.DIR_FILES = self.cmv.varPath_Files
            try:
                self.cmvutil = cmu.cmdUtil(self.cmv)  # not finished yet
                self.CML_UTIL_SET = True
            except:
                if(self.debug):
                    print(self.s4+"[init_internal_pathway] Warning: failure to set internal pathway utility\n")
                self.CML_UTIL_ERROR = True
            self.DIRPATH = self.cmv.varPath
            self.DIRPATH_SET = True
            return True


    def src_check(self):
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.SRCFOLD in self.DIR_FOLDERS):
                self.SRCPATH = self.cmv.joinNode(self.DIRPATH,self.SRCFOLD)
                self.SRCPATH_SET = True
                return True
            else:
                self.SRCPATH_ERROR = True
                return False
        else:
            return False

    def bin_check(self):
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.BINFOLD in self.DIR_FOLDERS):
                self.BINPATH = self.cmv.joinNode(self.DIRPATH,self.BINFOLD)
                self.BINPATH_SET = True
                return True
            else:
                self.BINPATH_ERROR = True

    def dat_check(self):
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.DATFOLD in self.DIR_FOLDERS):
                self.DATPATH = self.cmv.joinNode(self.DIRPATH,self.DATFOLD)
                self.DATPATH_SET = True
                return True
            else:
                self.BINPATH_ERROR = True
                return False
        else:
            return False

    def opt_check(self):
        if(self.INTERNAL_CML_SET and self.DIRPATH_SET):
            if(self.OPTFILE in self.DIR_FILES):
                self.OPTPATH = self.cmv.joinNode(self.DIRPATH,self.OPTFILE)
                self.OPTPATH_SET = True
                return True
            else:
                self.OPTPATH_ERROR = True
                return False
        else:
            return False


    #--------------------------#----------------#--------------------------#
    # Initialize Main Contents #                # Initialize Main Contents #
    #--------------------------#----------------#--------------------------#


    def update_dicts(self, dict_type = 'all'):

        if(dict_type == 'all'):	    
            self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))
            self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))
            self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_ERROR_DICT = {zip(self.FILENAME_LIST,FILEPATH_ERROR_LIST)}
            self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_SET_DICT = {zip(self.FILENAME_LIST,FILEPATH_SET_LIST)}

        elif(dict_type == 'fold'):
            self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))
            self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))

        elif(dict_type == 'file'):
            self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))
            self.FILEPATH_ERROR_DICT = {zip(self.FILENAME_LIST,FILEPATH_ERROR_LIST)}
            self.FILEPATH_SET_DICT = {zip(self.FILENAME_LIST,FILEPATH_SET_LIST)}

        elif(dict_type == 'path'):

            self.FOLDPATH_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_LIST))
            self.FILEPATH_DICT = dict(zip(self.FILENAME_LIST,self.FILEPATH_LIST))

        elif(dict_type == 'error'):
            self.FOLDPATH_ERROR_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_ERROR_DICT = {zip(self.FILENAME_LIST,FILEPATH_ERROR_LIST)}
            self.FOLDPATH_SET_DICT = dict(zip(self.FOLDNAME_LIST,self.FOLDPATH_ERROR_LIST))
            self.FILEPATH_SET_DICT = {zip(self.FILENAME_LIST,FILEPATH_SET_LIST)}

        else:
            if(self.debug):
                print(self.s4+"[update_dicts] Error: input, dict_type, not recognizned\n")
            return False
        return True


    def init_fold_in_main(self, fold_name, auto_check=True):

        if(not isinstance(fold_name,str)):
            if(self.debug):
                print(self.s4+"[add_fold_to_main] Error: input 'fold_name' must be a string\n")
            return False

        self.FOLDNAME_LIST.append(fold_name)
        self.FOLDPATH_SET_DICT[fold_name] = False
        self.FOLDPATH_ERROR_DICT[fold_name] = False

        if(auto_check):
            success = self.fold_check_in_main(fold_name)
            return success
        return True


    def init_file_in_main(self, file_name, auto_check=True):

        if(not isinstance(file_name,str)):
            if(self.debug):
                print(self.s4+"[add_fold_to_main] Error: input 'file_name' must be a string\n")
            return False

        self.FILENAME_LIST.append(file_name)
        self.FILEPATH_SET_DICT[file_name] = False
        self.FILEPATH_ERROR_DICT[file_name] = False

        if(auto_check):
            success = self.file_check_in_main(file_name)
            return success
        return True


    def fold_check_in_main(self, fold_name):
        if(not isinstance(fold_name,str)):
            if(self.debug):
                print(self.s4+"[fold_check_in_main] Error: input variable, 'fold_name', must be a strings\n")
            return False

        if(not isinstance(self.cmv,cml.PathParse)):
            if(self.debug):
                print(self.s4+"[fold_check_in_main] Error: internal pathway has not been set\n")
            return False

        if(fold_name in self.FOLDNAME_LIST):
            self.FOLDPATH_DICT[fold_name] = self.cmv.joinNode(self.cmv.varPath,fold_name)
		    self.FOLDPATH_SET_DICT[fold_name] = True
		    self.PATH_ERROR_DICT[fold_name] = False
            return True
        else:
            self.FOLDPATH_DICT[fold_name] = False
		    self.FOLDPATH_SET_DICT[fold_name] = False
		    self.FOLDPATH_ERROR_DICT[fold_name] = True
            return False


    def file_check_in_main(self, file_name):
        if(not isinstance(file_name,str)):
            if(self.debug):
                print(self.s4+"[file_check_in_main] Error: input variable, 'file_name', must be a strings\n")
            return False

        if(not isinstance(self.cmv,cml.PathParse)):
            if(self.debug):
                print(self.s4+"[file_check_in_main] Error: internal pathway has not been set\n")
            return False

        if(file_name in self.FILENAME_LIST):
            self.FILEPATH_DICT[file_name] = self.cmv.joinNode(self.cmv.varPath,file_name)
		    self.FILEPATH_SET_DICT[file_name] = True
		    self.FILEPATH_ERROR_DICT[file_name] = False
            return True
        else:
            self.FILEPATH_DICT[file_name] = False
		    self.FILEPATH_SET_DICT[file_name] = False
		    self.FILEPATH_ERROR_DICT[file_name] = True
            return False


    def init_binary(self, bin_name):
        '''
        Description:

            Add the name of a binary file with the input 'bin_name'
            The binary will be assumed to be in the binary folder ('bin')
            Be sure to include any file extention (e.g. 'run.sh')

        Input(s):

            bin_name : [array of strings, string], corrosponding to the name(s) of the
                       binary file to be added to the binary file dictionary. It is
                       assumed that this file resides within the 'bin' directory

        Output(s):

            success : [bool], True if successful, else False
        '''

        if(isinstance(bin_name,(array,tuple))):
            if(not all([isinstance(bin,str) for bin in bin_name])):
                if(self.debug):
                    print(self.s4+"[init_binary] Error: input, 'bin_name', should be an array of strings\n")
                return False
        elif(isinstance(bin_name,str)):
            bin_name = [bin_name]
        else:
            if(self.debug):
                print(self.s4+"[init_binary] Error: input, 'bin_name', not a recognizned type\n")
            return False

        for bin in bin_name:
            if(bin in self.cmv.contentPath(self.BINPATH)):
                self.BIN_DICT[bin] = self.cmv.joinNode(self.BINPATH,bin)
            else:
                if(self.debug):
                    print(self.s4+"[init_binary] Warning: binary file, '"+bin+"', not found in 'bin' folder\n")
        return True


    #---------------------------#----------------#---------------------------#
    # Debug and Error Functions #                # Debug and Error Functions #
    #---------------------------#----------------#---------------------------#


    def get_run_time(self, type='str'):
        self.time_end = time.time()
        run_time = self.time_end - self.time_start
        if(type == 'float'):
            return float(run_time)
        elif(type == 'int'):
            return int(run_time)
        else:
            return str(run_time)


    def exit_function(self, action_msg, failure=True):
        if(failure):
            print("ExitError: '"+self.DIRNAME+"' failed "+action_msg)
        print("Run Number upon exit:  "+str(self.cycle))
        print("Script run-time :  "+self.get_run_time(type='str')
        print("   ")
        sys.exit()


    def assess_initialization(self):
             
        err0 = self.INTERNAL_CML_ERROR
        err1 = self.DIRPATH_ERROR
        err2 = self.SRCPATH_ERROR
        err3 = self.BINPATH_ERROR
        err4 = self.DATPATH_ERROR
        err5 = self.OPTPATH_ERROR
        err6 = self.CML_UTIL_ERROR

        path0 = self.INTERNAL_CML_SET 
        path1 = self.DIRPATH_SET
        path2 = self.SRCPATH_SET
        path3 = self.BINPATH_SET
        path4 = self.DATPATH_SET
        path5 = self.OPTPATH_SET
        path6 = self.CML_UTIL_SET
             
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
            print(self.s4+"E1 Main Directory Path Test :            Failed")
        else:   
            if(path1):         
                print(self.s4+"E1 Main Directory Path Test :            Succeeded") 
            else:
                print(self.s4+"E1 Main Directory Path Test :            ...path not found")      
        time.sleep(0.5)          

        if(err2):
            print(self.s4+"E2 Source Directory Path Test :                Failed")
        else:
            if(path2):
                print(self.s4+"E2 Source Directory Path Test :                Succeeded") 
            else:
                print(self.s4+"E2 Source Directory Path Test :                ...path not found") 
        time.sleep(0.5)

        if(err3):
            print(self.s4+"E3 Binary Directory Pathway Test :          Failed")
        else:
            if(path3):
                print(self.s4+"E3 Binary Directory Pathway Test :          Succeeded") 
            else:
                print(self.s4+"E3 Binary Directory Pathway Test :          ...path not found") 
        time.sleep(0.5)

        if(err4):
            print(self.s4+"E4 Data Directory Path Test :          Failed")
        else:
            if(path4):
                print(self.s4+"E4 Data Directory Path Test :          Succeeded") 
            else:
                print(self.s4+"E4 Data Directory Path Test :          ...path not found")             
        time.sleep(0.5)

        if(err5):
            print(self.s4+"E5 Option File Path Test : Failed")
        else:
            if(path5):
                print(self.s4+"E5 Option File Path Test : Succeeded") 
            else:
                print(self.s4+"E5 Option File Path Test : Skipped")                 
        time.sleep(0.5)

        if(err6):
            print(self.s4+"E6 Command Line Utility Test :          Failed")
        else:
            if(path6):
                print(self.s4+"E6 Command Line Utility Test :          Succeeded") 
            else:
                print(self.s4+"E6 Command Line Utility Test :          ...command line utility not set")     
        time.sleep(0.5)              

        print(" ")
        if(err0 or err1 or err3):
            print(self.s4+"Fatal Error Test: Failed")
            self.EXIT_ERROR = True
        else:
            print(self.s4+"Fatal Error Test: Succeeded")
        print(" ")
        time.sleep(0.5)
        
        return True


    #-----------------------#----------------#-----------------------#
    # File/Folder Utilities #                # File/Folder Utilities #
    #-----------------------#----------------#-----------------------#




    #------------------------#----------------#------------------------#
    # Program Loop Functions #                # Program Loop Functions #
    #------------------------#----------------#------------------------#


    def set_option_menu(self, lines):
        '''
            
        '''
        if(isinstance(lines,(array,tuple))):
            if(not all([isinstance(line,str) for line in lines])):
                if(self.debug):
                    print(self.s4+"[set_option_menu] Error: input, 'lines', should be an array of strings\n")
                return False
        elif(isinstance(lines,str)):
            lines = [lines]
        else:
            if(self.debug):
                print(self.s4+"[set_option_menu] Error: input, 'lines', not a recognizned type\n")
            return False
        
        self.option_menu_lines = [self.s4+line+"\n" for line in lines]
        return True


    def print_option_menu(self):
        if(self.option_menu_lines != []):
            try:
                print(" ")
                for line in self.option_menu_lines:
                    print(line)
                print(" ")
                return True
            except:
                if(self.debug):
                    print(self.s4+"[print_option_menu] Error: failure to print menu lines, cause unknown\n")
                return False
        else:
            if(self.debug):
                print(self.s4+"[print_option_menu] Error: 'option_menu_lines' hasn't been set yet\n")
            return False


    def program_loop(self, action_function, program_name='Main'):
        '''
        Description: 

            A simple program loop template

        Input(s): 

            action_function : [function], action_function must take one argument (string)
                              which will result in one action being completed. If 
                              action_function returns the string 'quit' than the program
                              loop terminates. If action_function returns False, then an
                              error message is printed.

        Output(s):

            success : [bool], True if successfully exited, else False
        '''
  
        run = True

        success = self.print_option_menu()
        if(success == False):
            if(self.debug):
                print(s4+"["+program_name+"] Error: input menu not properly formatted\n")
            return False

        while(run):

            action = raw_input(self.s4+"Input a choice from the option menu: ")
            print(' ')

            try:
                formatted_action = action.lower().rstrip()
            except:
                if(self.debug):
                    print(s4+"["+program_name+"] Error: input could not be parsed, please try again\n")
                continue

            if(formatted_action == 'quit' or formatted_action == 'exit'):
                print(" ")
                break 

            success = self.action_function(formatted_action)
            if(success):
                if(self.debug):
                    print(s4+"["+program_name+"] Success: formatted input, '"+formatted_action+"', successfully completed\n")
            else:
                if(self.debug):
                    print(s4+"["+program_name+"] Error: formatted input, "+formatted_action+" is not a valid command\n")
                continue

        return True













