#!/usr/bin/env python

'''

- This script goes in the PMOD folder

This script faciliates compiling binaries from source files 
within the source folder ('src'), this is accomplished by 
formatting and running a shell script.
and moving those binaries to the binaries folder ('bin').

A graphical example is shown below: this script is run within 'Main'

         |-- 'bin'----|---'run.sh'
'Main' --|            |
         |-- 'src'-|  |---''  <----------<-------|
                   |                             |
                   |--'aux'     <--------|-->|   |
                   |                     |   |-->|  The script moves the binaries 'aux' and 'xeb_server'
                   |--'xeb_server'   <---|-->|      into the 'bin' folder from the 'src' folder
                   |                     |
                   |--'compile.sh'  -->--| 'compile.sh' creates 'aux' and 'xeb_server'


Info:

    - Change 'linux' to 'windows' for the osFormat variable if running on windows


Inputs:

    bin_list : [string or array of strings], The strings corrospond to the names of the binary files

    SRC_SCRIPT : [string] corrosponds to the name of the script which
                          generates the binaries named in 'bin_list

    BIN_SCRIPT : [string] corrosponds to the name of the script which
                          runs the binary files within the binary directory

    DIR_NAME : [string] ("Main"), corrosponds to the name of the program folder

    osFormat : [string] ("linux"), The OS on which the program is ran

    SRC_NAME : [string] ("src"), The name of the source folder

    BIN_NAME : [string] ("bin"), The name of the binary directory

    SPC : [string] ("    "), Indention spaces for more legable printing


Output:

    Boolean: "True" if success, else "False" if failure.

'''

import sys
import os
import subprocess
import time

from pmod import cmdutil as cmu
from pmod import ioparse as iop
from pmod import strlist as strl



class progComp(cmu.cmdUtil):

    def __init__(self,
                bin_list,
                src_script = "compile.sh",
                bin_script = "run.sh",
                dir_name = "Main",
                src_name = "src",
                bin_name = "bin",
                osFormat='linux',
                newPath=None,
                rename=False,
                debug=True,
                shellPrint=False,
                colourPrint=True,
                space='    ',
                endline='\n',
                moduleNameOverride="compile",
                **kwargs):

        super(progComp, self).__init__(osFormat,
                                       newPath,
                                       rename,
                                       debug,
                                       shellPrint,
                                       colourPrint,
                                       space,
                                       endline,
                                       moduleNameOverride,
                                       **kwargs)

        kwargs = self.__update_funcNameHeader__("init", **kwargs)

        # Internal Variables

        self.failError = False

        self.DIRPATH = ""
        self.SRCPATH = ""
        self.BINPATH = ""

        self.SRC_SCRIPT  = ""
        self.BIN_SCRIPT  = ""
        self.DIR_NAME    = ""
        self.SRC_NAME    = ""
        self.BIN_NAME    = ""

        self.move_dict = {}

        # Initialization (Any failure will result in 'failError' being set to True
        # If failError evaluates to True upon initialization, fix the errors before
        # attempting to call the compile function, else fatal errors will likely occur

        if(self.__not_strarr_print__(bin_list, varID='bin_list')):
            self.failError = True
        else:
            self.move_dict = dict([(i,False) for i in bin_list])

        self.input_string_list = {'SRC_SCRIPT':src_script,
                                  'BIN_SCRIPT':bin_script,
                                  'DIR_NAME':dir_name,
                                  'SRC_NAME':src_name,
                                  'BIN_NAME':bin_name}

        for entry in self.input_string_list:
            if(self.__not_str_print__(self.input_string_list[entry], varID=entry, **kwargs)):
                self.failError = True
            else:
                exec("self."+entry+"="+repr(self.input_string_list[entry]))

        if(len(self.varPath_List) > 0 and self.DIR_NAME != '' and isinstance(self.DIR_NAME, str)):
            if(self.varPath_List[-1] != self.DIR_NAME):
                self.__err_print__("this current directory is not the same as the input directory name...", **kwargs)
                self.failError = True
        else:
            self.__err_print__("current directory name could not be resolved", **kwargs)
            self.failError = True


    def compileFunc(self, safety_bool=True, **kwargs):

        kwargs = self.__update_funcNameHeader__("compileFunc", **kwargs)

        if(self.failError or safety_bool):
            return self.__err_print__("was detected; the compile function will now exit...", varID='failError')

        print(" ")
        print("The compiler is now starting...runtime messesges will be printed below:\n")

        # Moving into the binary folder (bin)
        success, value = self.cmd("cd "+self.BIN_NAME)
        if(not success):
            errmsg = ["the binary folder, could not be accessed",
                      "binary folder name : '"+self.BIN_NAME+"'",
                      "check to see in the binary folder is present under the current name"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Set binary directory (bin) pathway
        success, value = self.cmd("pwd")
        if(not success):
            errmsg = ["the binary folder pathway, could not be accessed",
                      "binary folder name : '"+self.BIN_NAME+"'",
                      "check to see that the binary folder is present under the current name"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)
        else:
            self.BINPATH = value

        # Get list of content of Bin directory
        success, value = self.cmd("ls")
        if(not success):
            errmsg = ["the binary folder content, could not be accessed",
                      "binary folder name : '"+self.BIN_NAME+"'",
                      "check to see that the binary folder is present under the current name"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)
        binarylist = value

        # Check for pre-existing binary files and remove any if the exist
        for entry in self.move_dict:
            if(entry in binarylist):
                errmsg = ["An already existing file is present in the binary folder",
                          "Attempting to overwrite this file : '"+entry+"'"]
                self.__err_print__(errmsg, heading='Warning', parSpace=False, blankLine=False)
                success, value = self.cmd("rm "+entry)
                if(not success):
                    errmsg = ["failure to delete file","newly compiled binary '"+entry+"' may be placed in the '"+DIR_NAME+"' folder"]
                    self.__err_print__(errmsg, parSpace=False, blankLine=False)
    
        # Return to 'Main' directory
        success, value = self.cmd("cd ..")
        if(not success):
            errmsg = ["the program folder, could not be reaccessed",
                      "program folder name : '"+self.DIR_NAME+"'",
                      "check to ensure all folders are properly named"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Ensure that the compiling shell script has UNIX endline characters
        success = self.filesEndlineConvert(self.SRC_SCRIPT, foldName=self.SRC_NAME, **kwargs)
        if(success == False):
            self.__err_print__("not properly formatted: errors may result...", varID=self.SRC_SCRIPT, heading='Warning', parSpace=False) 
    
        # Moving into the source folder (src)
        success, value = self.cmd("cd "+self.SRC_NAME)    
        if(not success):
            errmsg = ["the source folder, could not be accessed",
                      "binary folder name : '"+self.SRC_NAME+"'",
                      "check to see that the source folder is present under the current name"]
            return self.__err_print__(errmsg, heading='ExitError')

        # Get source folder (src) pathway
        success, value = self.cmd("pwd")
        if(not success):
            errmsg = ["the source folder pathway, could not be accessed",
                      "source folder name : '"+self.SRC_NAME+"'",
                      "check to see that the source folder is present under the current name"]
            return self.__err_print__(errmsg, heading='ExitError')
        else:
            self.SRCPATH = value

        # Get content of source folder (src)
        success, value = self.cmd("ls")
        if(not success):
            errmsg = ["the source folder content, could not be accessed",
                      "source folder name : '"+self.SRC_NAME+"'",
                      "check to see that the source folder is present under the current name"]
            return self.__err_print__(errmsg, heading='ExitError')

        if(self.__not_strarr_print__(value, varID='value', **kwargs)):
            errmsg = ["Source folder content could not be accessed",
                      "Source folder : "+SRC_NAME,
                      "Check to ensure that the source directory is properly formatted"]
            return self.__err_print__(errmsg, heading='ExitError')
        else:
            if(len(value) > 0):
                check_list = [entry.rstrip() for entry in value]

                # Check for pre-existing binary files in the source folder (src) and remove any that are found
                for entry in self.move_dict:
                    if(entry in check_list):
                        errmsg = ["An already existing file is present in the binary folder",
                                  "Attempting to delete this file : '"+entry+"'"]
                        self.__err_print__(errmsg, heading='Warning', parSpace=False, blankLine=False)
                        success, value = self.cmd("rm "+entry)
                        if(not success):
                            errmsg = ["Failure to delete existing file : '"+entry+"'",
                                      "Conflict may occur when attempting to recompile this binary file"]
                            self.__err_print__(errmsg, heading='Warning', parSpace=False, blankLine=False)
            else:
                errmsg = ["the source folder is empty",
                          "source folder name : '"+self.SRC_NAME+"'",
                          "add the files to be compiled to the source folder and try again"]
                return self.__err_print__(errmsg, heading='ExitError', blankLine=False)
    
        # Move system directory to source folder (src)
        try:
            os.chdir(self.SRCPATH)
        except:
            errmsg = ["Failure to set the shell pathway to the source folder",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False) 
    
        # Change the mode on the shell script to an exceutable
        try:
            subprocess.call("chmod +x "+self.SRC_SCRIPT, shell=True)
        except:
            errmsg = ["Failure to set the shell script to an exceutable",
                      "Shell script name : '"+self.SRC_SCRIPT+"'",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Run the compiling shell script
        try:
            subprocess.call("./"+self.SRC_SCRIPT, shell=True)
        except:
            errmsg = ["Failure to exceute the shell script",
                      "Shell script name : '"+self.SRC_SCRIPT+"'",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Get content of source folder (src) after running compiling script
        success, value = self.cmd("ls")
        if(not success):
            errmsg = ["The source folder content could not be accessed after compiling shell script",
                      "Shell script name : '"+self.SRC_SCRIPT+"'",
                      "Source folder name : '"+self.SRC_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)
    
        # check contents of source folder (src) for binary(ies)

        if(self.__not_strarr_print__(value, varID='value', **kwargs)):
            errmsg = ["Source folder content could not be accessed after compiling shell script",
                      "Shell script name : '"+self.SRC_SCRIPT+"'",
                      "Source folder name : '"+self.SRC_NAME+"'",
                      "Check to ensure that the source directory is properly formatted"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)
        else:
            if(len(value) > 0):
                for entry in self.move_dict:
                    if(entry in value):
                        self.__err_print__("binary file, has been found after compiling", varID=entry, heading="Success", parSpace=False)
                        self.move_dict[entry] = True
                    else:
                        self.__err_print__("binary file, was not found upon compilation", varID=entry, heading="Failure", parSpace=False)
            else:
                errmsg = ["For some reason the source folder is now empty",
                          "Source folder name : '"+self.SRC_NAME+"'",
                          "Shell script name : '"+self.SRC_SCRIPT+"'",
                          "Replace source code and shell script and try again"]
                return self.__err_print__(errmsg, heading='ExitError', blankLine=False)
    
        # Move binaries to the main directory
        for entry in self.move_dict:
            if(self.move_dict[entry]):
                success, value = self.cmd("mv "+entry+" ..")
                if(not success):
                    self.__err_print__("was not successfully moved into the '"+self.DIR_NAME+"' directory", varID=entry, parSpace=False)
                    self.move_dict[entry] = False

        # Move pathway back to the main directory
        success, value = self.cmd("cd ..")
        if(not success):
            return self.__err_print__("could not be reaccessed", varID=self.DIR_NAME, heading='ExitError')

        # Move binaries into the binary directory
        for entry in self.move_dict:
            if(self.move_dict[entry]):
                success, value = self.cmd("mv "+entry+" "+self.BIN_NAME)
                if(not success):
                    self.__err_print__("was not successfully moved into the '"+self.BIN_NAME+"' directory", varID=entry)
                    self.move_dict[entry] = False

        # Ensure that the running shell script has UNIX endline characters
        success = self.filesEndlineConvert(self.BIN_SCRIPT, foldName=self.BIN_NAME, **kwargs)
        if(success == False):
            self.__err_print__("not properly formatted: errors may result...", varID=self.BIN_SCRIPT, heading='Warning',parSpace=False)

        # Move pathway back into the binary directory
        success, value = self.cmd("cd "+self.BIN_NAME)
        if(not success):
            errmsg = ["the program folder, could not be reaccessed",
                      "program folder name : '"+self.DIR_NAME+"'",
                      "check to ensure all folders are properly named"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Move system directory to binary directory (bin)
        try:
            os.chdir(self.BINPATH)
        except:
            errmsg = ["Failure to set the shell pathway back to the program folder",
                      "Program folder name : '"+self.BIN_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Change the mode on the shell script to an exceutable
        try:
            subprocess.call("chmod +x "+self.BIN_SCRIPT,shell=True)
        except:
            errmsg = ["Failure to set the binary script to an exceutable",
                      "Shell script name : '"+self.BIN_SCRIPT+"'",
                      "Binary folder name : '"+self.BIN_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Get content of binary folder (bin) after moving binaries
        success, value = self.cmd("ls")
        if(not success):
            errmsg = ["The binary folder content could not be accessed after compiling shell script",
                      "Shell script name : '"+self.BIN_SCRIPT+"'",
                      "Binary folder name : '"+self.BIN_NAME+"'"]
            return self.__err_print__(errmsg, heading='ExitError', blankLine=False)

        # Move binaries into the binary directory
        bin_fail = False
        mb = 0
        for entry in self.move_dict:
            if(entry in value):
                self.__err_print__("The '"+entry+"' binary is accounted for in the binary folder", heading="Success", parSpace=False)
            elif(self.move_dict[entry] == False):
                self.__err_print__("The '"+entry+"' binary was not moved into the binary folder", heading="Failure", parSpace=False)
                bin_fail = True
                mb += 1
            else:
                self.__err_print__("The '"+entry+"' binary could not be accounted for", heading="Failure", parSpace=False)
                bin_fail = True
                mb += 1
        if(bin_fail):
            self.__err_print__(str(mb)+" missing binary files...program will not work as intended!", heading="Failure", parSpace=False)
        return True