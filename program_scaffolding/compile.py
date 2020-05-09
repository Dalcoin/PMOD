import sys
import os
import subprocess
import time

import pmod.cmdline as cml
import pmod.cmdutil as cmu
import pmod.ioparse as iop
import pmod.strlist as strl

'''

- This script goes in the PMOD folder

This script faciliates compiling binaries from source files 
within the source folder ('src'), this is accomplished by 
formatting and running a shell script.
and moving those binaries to the binaries folder ('bin').

A graphical example is shown below: this script is run within 'Main'

         |-- 'bin'----|---'run.sh'
'Main' --|            |
         |-- 'src'-|  |---''  <----------<------|
                   |                            |
                   |--'aux'   <----------|-->|  |
                   |                     |   |--| The script moves the binaries 'aux' and 'xeb_server'
                   |--'xeb_server'  <----|-->|    into the 'bin' folder from the 'src' folder
                   |                     |
                   |--'compile.sh'  -->--| 'compile.sh' creates 'aux' and 'xeb_server'


Info:

    - Change 'linux' to 'windows' for the OS_INST variable if running on windows


Inputs:

    bin_list : [string or array of strings], The strings corrospond to the names of the binary files

    src_script : [string] corrosponds to the name of the script which
                          generates the binaries named in 'bin_list

    bin_script : [string] corrosponds to the name of the script which
                          runs the binary files within the binary directory

    DIR_NAME : [string] ("Main"), corrosponds to the name of the program folder

    OS_INST : [string] ("linux"), The OS on which the program is ran

    SRC_DIR : [string] ("src"), The name of the source folder

    BIN_DIR : [string] ("bin"), The name of the binary directory

    SPC : [string] ("    "), Indention spaces for more legable printing


Output:

    Boolean: "True" if success, else "False" if failure.

'''

def compileFunc(bin_list,
                src_script = "compile.sh",
                bin_script = "run.sh",
                DIR_NAME = "Main",
                OS_INST = "linux",
                SRC_DIR = "src",
                BIN_DIR = "bin",
                SPC="    "):

    # Setting the stage

    # Pathway variables, these should always be strings
    DIRPATH = ""
    SRCPATH = ""
    BINPATH = ""

    # Check input variable 'bin_list' for TypeError
    if(isinstance(bin_list,(list,tuple))):
        if(not all([isinstance(entry,str) for entry in bin_list])):
            print(SPC+"[compileFunc] ExitError: if input 'bin_list' is an array, it must contain only strings\n")
            return False
    elif(isinstance(bin_list,str)):
        bin_list = [bin_list]
    else:
        print(SPC+"[compileFunc] ExitError: input 'bin_list' must be either an array or a string\n")
        return False

    # Set-up debug variables
    movexeb = False # Delete
    moveaux = False # Delete
    move_dict = {}
    for entry in bin_list:
        move_dict[entry] = False
    exefail = False

    #------------------
    # Compile actions |
    #------------------

    print(" ")
    print("The 'compileFunc' routine is now starting...runtime messesges will be printed below:\n")

    # Set internal command line and command line utility
    try:
        cmv = cml.PathParse(OS_INST)
        cmt = cmu.cmdUtil(cmv)
        if(cmt.CML_INIT == False):
            print(SPC+"Error: 'cmdUtil' could not be initialized\n")
            return False
        print(SPC+"Success: Internal pathway routine has been successfully initialized")
    except:
        print(SPC+"Error: an error occured while initializing internal pathway routine")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Set start pathway
    success, value = cmv.cmd("pwd")
    if(not success):
        print(SPC+"Error: It looks like the '"+DIR_NAME+"' folder pathway could not be accessed")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False
    else:
        DIRPATH = value

    # Moving into the binary folder (bin)
    success, value = cmv.cmd("cd "+BIN_DIR)
    if(not success):
        print(SPC+"Error: It looks like the binary folder, '"+BIN_DIR+"', could not be accessed")
        print(SPC+"       Check to see if the binary folder is present")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Set binary directory (bin) pathway
    success, value = cmv.cmd("pwd")
    if(not success):
        print(SPC+"Error: It looks like the binary folder, '"+BIN_DIR+"', pathway could not be accessed")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed")
        return False
    else:
        BINPATH = value

    # Get list of content of Bin directory
    success, value = cmv.cmd("ls")
    if(not success):
        print(SPC+"Error: It looks like the binary folder, '"+BIN_DIR+"', content could not be accessed")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False
    binarylist = value

    # Check for pre-existing binary files and remove any if the exist
    for entry in bin_list:
        if(entry in binarylist):
            print(SPC+"Warning: An already existing '"+entry+"' file is present in the binary folder")
            print(SPC+"         An attempt will be made to overwrite this file...")
            success, value = cmv.cmd("rm "+entry)
            if(not success):
                print(SPC+"Error: failure to delete existing file, '"+entry+"'")
                print(SPC+"The newly compiled version of this binary may end up in the '"+DIR_NAME+"' folder\n")

    # Return to 'Main' directory
    success, value = cmv.cmd("cd ..")
    if(not success):
        print(SPC+"Error: It looks like the program folder, '"+DIR_NAME+"', could not be accessed")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Moving into the source folder (src)
    cmv = cml.PathParse(OS_INST)
    success, value = cmv.cmd("cd "+SRC_DIR)    
    if(not success):
        print(SPC+"Error: It looks like the source folder, '"+SRC_DIR+"', could not be accessed")
        print(SPC+"       Check to see if the source folder is present")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Get source folder (src) pathway
    success, value = cmv.cmd("pwd")
    if(not success):
        print(SPC+"Error: It looks like the source folder, '"+SRC_DIR+"', pathway could not be accessed")
        print(SPC+"       Check to see if the source folder is present")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False
    else:
        SRCPATH = value

    # Get content of source folder (src)
    success, value = cmv.cmd("ls")
    if(not success):
        print(SPC+"Error: It looks like the source folder, '"+SRC_DIR+"', content could not be accessed")
        print(SPC+"       Check to see if the source file properly formatted")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    if(isinstance(value,(list,tuple))):
        if(len(value) > 0):
            check_list = [i.rstrip() for i in value]

            # Check for pre-existing binary files in the source folder (src) and remove any that are found
            for entry in bin_list:
                if(entry in check_list):
                    print(SPC+"Warning: An already existing '"+entry+"' file is present in the binary folder")
                    print(SPC+"         An attempt will be made to overwrite this file...")
                    success, value = cmv.cmd("rm "+entry)
                    if(not success):
                        print(SPC+"Error: failure to delete existing file, '"+entry+"'")
                        print(SPC+"There may be a failure when attempting to overwrite this binary during compilation\n")
        else:
            print("Error: It looks like the source folder, '"+SRC_DIR+"', is empty")      
            print("ExitError: fatal error; 'compileFunc' could not be completed\n")
            return False
    else:
        print(SPC+"Error: It looks like the source folder, '"+SRC_DIR+"', content could not be accessed")
        print(SPC+"       Check to ensure that the source directory is properly formatted")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False
    
    # Move system directory to source folder (src)
    try:
        os.chdir(SRCPATH)
    except:
        print(SPC+"Error: failure to set the shell pathway to the source folder")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False     

    # Ensure that the compiling shell script has UNIX endline characters
    success = cmt.convert_file_endline(src_script, foldName = SRC_DIR)
    if(success == False):
        print(SPC+"Warning: '"+src_script+"'shell script not formatted, errors may result from improper formatting\n")

    # Change the mode on the shell script to an exceutable
    try:
        subprocess.call("chmod +x "+src_script,shell=True)
    except:
        print(SPC+"Error: failure to set the 'compileFunc' shell script to an executable")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Run the compiling shell script
    try:
        subprocess.call("./"+src_script,shell=True)
    except:
        print(SPC+"Error: failure to run the 'compileFunc' shell script")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Get content of source folder (src) after running compiling script
    success, value = cmv.cmd("ls")
    if(not success):
        print(SPC+"Error: It looks like the source folder, '"+SRC_DIR+"', content could not be accessed after compiling")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # check contents of source folder (src) for binary(ies)
    if(isinstance(value,(list,tuple))):
        if(len(value) > 0):
            for entry in bin_list:
                if(entry in value):
                    print(SPC+"Success: The binary file, '"+entry+"', has been found after compiling")
                    move_dict[entry] = True
                else:
                    print(SPC+"Error: it looks like the binary file, '"+entry+"' wasn't created upon compilation")
        else:
            print("Error: It looks like the source folder, '"+SRC_DIR+"', is empty")
            print("ExitError: fatal error; 'compileFunc' could not be completed\n")
            return False
    else:
        print(SPC+"Error: It looks like the source folder, '"+SRC_DIR+"', content could not be accessed after compiling")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Move binaries to the main directory
    for entry in bin_list:
        if(move_dict[entry]):
            success, value = cmv.cmd("mv "+entry+" ..")
            if(not success):
                print(SPC+"Error: '"+entry+"' was not successfully moved into the '"+DIR_NAME+"' directory")
                move_dict[entry] = False

    # Move pathway back to the main directory
    success, value = cmv.cmd("cd ..")
    if(not success):
        print(SPC+"Error: It looks like the program folder, '"+DIR_NAME+"', could not be reaccessed")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Move binaries into the binary directory
    for entry in bin_list:
        if(move_dict[entry]):
            success, value = cmv.cmd("mv "+entry+" "+BIN_DIR)
            if(not success):
                print(SPC+"Error: '"+entry+"' was not successfully moved into the '"+BIN_DIR+"' directory")
                move_dict[entry] = False

    # Move pathway back into the binary directory
    success, value = cmv.cmd("cd "+BIN_DIR)
    if(not success):
        print(SPC+"Error: It looks like the binary folder, '"+BIN_DIR+"', could not be accessed")
        print(SPC+"       Check to see if the binary folder is present")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Move system directory to binary directory (bin)
    try:
        os.chdir(BINPATH)
    except:
        print(SPC+"Error: failure to set the shell pathway to the binary folder")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Ensure that the running shell script has UNIX endline characters
    success = cmt.convert_file_endline(bin_script, foldName=BIN_DIR)
    if(success == False):
        print(SPC+"Warning: "+bin_script+" shell script not formatted, errors may result from improper formatting\n")

    # Change the mode on the shell script to an exceutable
    try:
        subprocess.call("chmod +x "+bin_script,shell=True)
    except:
        print(SPC+"Error: failure to set the '"+bin_script+"' shell script to an executable")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed\n")
        return False

    # Get content of binary folder (bin) after moving binaries
    success, value = cmv.cmd("ls")
    if(not success):
        print(SPC+"Error: It looks like the binary folder, '"+BIN_DIR+"', content could not be accessed")
        print(SPC+"ExitError: fatal error; 'compileFunc' could not be completed")
        return False

    # Move binaries into the binary directory
    bin_fail = False
    for entry in bin_list:
        if(entry in value):
            print(SPC+"Success: The '"+entry+"' binary is accounted for in the binary folder")
        elif(move_dict[entry] == False):
            print(SPC+"Error: The '"+entry+"' binary is not accounted for in the binary folder")
            bin_fail = True
        else:
            bin_fail = True

    if(bin_fail):
        print(SPC+"Error: compileFunc failed, binary(ies) missing; program will not work as intended\n")

    return True


#----------
# example |
#----------

# Main program: test example, change "False" to "True" to actually run

#---------------------------------------------------------------------|

#bin_list = ("xeb_server","aux")
#src_script = "compile.sh"
#bin_script = "run.sh"
#
#if(False):
#    success = compileFunc(bin_list, src_script = src_script, bin_script = bin_script)
#else:
#    success = True
#
#print(" ")
#if(success):
#    print("No fatal errors detected, see above for runtime messesges")
#else:
#    print("Fatal error detected! See above for runtime errors")
#print(" ")
