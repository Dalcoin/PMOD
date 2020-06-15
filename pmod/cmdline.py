#!/usr/bin/env python
'''

0---------0
| Summary |
0---------0

A module containing a class which allows for linux command-line inspired
strings to be passed as commands to a class-function. Options for moving
copying, deleting, creating and modifying files and directories.

The following modules are dependent on 'cmdline':

    cmdutil


0--------------0
| Dependencies |
0--------------0

This module is dependent on the following internal dependencies:

    os     : Retrieving/Resolving/Parsing System Pathways
    shutil : Moving/Coping/Deleting Files and Directories

This module is dependent on the following PMOD dependencies:

    ioparse : used for file reading/writing
    strlist : used for parsing strings and arrays


0-------------0
| Description |
0-------------0

       Consists of 'PathParse', which is a class to call commands within python
    scripts, allowing functionality in the image of Linux command-line inputs.
    Perform manipulations on the location of files and directories from within
    python scripts.
    
       The main function in the class is 'cmd' : PathParse.cmd(). This
    function allows commands to be passed which, among other things, return the
    contents of the current stored directory string, change the current stored
    directory string, move files between directories and delete files and
    directories. The class allows for pathway information to be stored and
    returned as string objects.

'''

import os
import shutil

import pmod.ioparse as iop
import pmod.strlist as strl

class PathParse(object):

    '''
    PathParse(osFormat, newPath=None, debug=False, colourPrint=True)

    -----------
    | Inputs: |
    -----------

    osFormat = 'windows' or 'linux'
    newPath = None (by default), else [string]

        if [None]   : the directory from which the script is run becomes the
                      default .path variable.
        if [string] : the input string becomes the default .path variable

    debug       = True [default] :
                  If True, debug info is printed to console, else nothing is printed

    colourPrint = True [default] :
                  If True, directory variable names are denoted by color when printed


    *Style note: ``Camel'' style names are used for this class
                 The style dictates that first or only words in
                 variable names are all lower-case, all proceeding
                 other words start with a capital letter.

    varPath : corrosponds to the string pointing to the current (path) directory
              *Style note: all addition current (path) pathway information is
              indicated by the addition of and underscore and a descriptive word
              starting with a capital letter (e.g. files in the current (path) 
              directory are stored as a list of strings with the variable: varPath_Files)
    '''

    def __init__(self,
                 osFormat,
                 newPath=None,
                 rename=False,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    '
                ):

        '''
        --------
        | init |
        --------

        Inputs :

            osFormat    = 'windows' or 'linux'
            newPath     = None  (by default)
            debug       = False (by default)
            colourPrint = True  (by default)

        Path :

            .varPath          : A string of the path in which the script is run
            .varPath_List     : A list of strings with values of the directory hiearchy in .path
            .varPath_Head     : A string containing the primary (home) directory
            .varPath_Contains : A list of strings with values of the contents of .path
            .varPath_Files    : A list of strings with values of the files found in the current directory.
            .varPath_Folders  : A list os strings with values of the subdirectories in the current directory.

        Other:

            .varOS      :  A string to specify the operating system, this determines the path file format
            .varCol     :  True for color Escape code when printing, False by default
        '''

        self.SET_INIT_PATH = False
        self.HELP_DICT_INIT = False

        self.cdList = ['ls', 'pwd', 'dir', 'cd', 'chdir', 'mv', 'rm', 'cp',
                       'mkdir','rmdir', 'find', 'match', 'help', 'vi']

        self.singleCommandList = ['ls', 'pwd']
        self.singlePathListNoGroup = ['cd', 'chdir', 'vi', 'help']
        self.singlePathListGroup = ['rm', 'rmdir', 'mkdir', 'dir', 'find', 'match']
        self.doublePathList = ['mv', 'cp', 'cpdir']

        self.dirNames = ['dir', 'dirs', 'directory', 'directories', 'folder', 'folders']
        self.fileNames = ['file', 'files']

        self.typeList = ['arr','array','list','tup','tuple']
        self.typeStr = ['str','string']

        self.space = space
        self.rename = rename
        self.debug = bool(debug)
        self.varOS = str(osFormat).lower()
        self.shellPrint = shellPrint
        self.varCol = colourPrint

        if(self.varOS == 'windows' or self.varOS == 'web'):
            self.delim = '\\'
        elif(self.varOS == 'linux'):
            self.delim = '/'
        elif(self.varOS == 'other'):
            self.delim = ':'
        else:
            if(self.debug):
                print(self.space+"[PathParse] Error: 'varOS', "+str(self.varOS)+" not recognized\n")
            self.SET_INIT_PATH = False

        if(newPath == None):
            try:
                self.varPath = os.getcwd()
                success = True
            except:
                print(self.space+"[PathParse] Error: failure to get current pathway from OS..")
                self.SET_INIT_PATH = False
                success = False
        else:
            self.varPath = newPath
            success = True

        if(success):
            updateTest = self.__updatePath__(self.varPath)
            if(updateTest == False):
                self.SET_INIT_PATH = False
            else:
                self.SET_INIT_PATH = True

        if(self.SET_INIT_PATH == False):
            if(self.debug):
                print(self.space+"[PathParse] Error: Initialization failed!\n")



    def documentation(self, string):
        """
        ---------------
        | guidelines: |
        ---------------

        1) Dundar functions use the internal pathway, non-Dundar functions do not.
        2) Functions performing file and pathway manipulations take full pathways.
        3) Path functions contain the word 'Path' and modify and manipulate the form of a pathway.
        4) Node functions modify and manipulate the nodes within a pathway.
        5) Non-Path functions should return a boolean value when their operation does not 
           require a value to be returned (e.g. moving, copying or deleting objects) which is 
           dependent on the success of the operation. 
        6) For each Path operation available through the 'cmd' function,
           there should be a corrosponding means of accomplishing the same
           task through non-Dundar function.



        Naming Convention: Variables

        1)
            * Internal pathways variables start with 'var'
            * Internal non-pathway variables must not start with 'var'

	    """

        action_list = ["Usage: ['ls',..,..] , returns a list of strings corrosponding to content of path directory\n",
                       
                       "Usage: ['pwd',..,..] , returns a string corrosponding to the pathway for path directory\n",
                       
                       "Usage: ['dir',['file1.file','file2.file'],..] , returns list of strings corrosponding "+
                       "to pathways of grouped files\n",
                       
                       "Usage: ['cd',..,pathway], returns None, modifies the path variables to move from the "+ 
                       "path directory to that specified in the pathway. The value for pathway may be either "+
                       "{'..' to move up one directory, '~' to move to home, or a name of a subdirectory}\n",
                       
                       "Usage: [chdir,..,full_pathway] , returns None, moves path variables to move from the "+
                       "current directory to that specified by full_pathway, full_pathway must be a full pathway\n",
                       
                       "Usage: [mv,['file1.file','file2.file'],destination] , returns None, moves files in path "+
                       "directory to the destination directory.\n",
                       
                       "Usage: [rm,['file1.file','file2.file'],..] , returns None, removes files in path directory\n", 

                       "Usage: [mv,['file1.file','file2.file'],destination], copies files to destination, renames "+
                       "copied files according to numeric naming convention\n",
                       
                       "Usage: [mkdir,['fold1','fold2'],..] , returns None, creates folders in path directory\n",
                       
                       "Usage: [rmdir,['fold1','fold2'],..] , returns None, deletes content in path directory\n",

                       "Usage: [find,['file1.file','file2.file'],..] , returns dictionary, searches for files by name, "+
                       " and returns a dictionary with boolean values for the existance of the files\n",
                          
                       "Usage: [match,['file1.file','file2.file'],..] , returns dictionary, searches for fragments, "+
                       " and returns a dictionary with boolean values for the files containing searched fragments\n",

                       "Usage: [help,['command'],..] , returns either a list or string, "+
                       "if no command is specified, 'help' returns a list of possible commands, else if a "+
                       "command is specified a string describing the commands usage is returned\n",

                       "Usage: [vi,['file1.file',file2.file',...],..], returns a dictionary. The dictionary "+ 
                       " has keys corrosponding to the names of the files as strings and values corrosponding "+
                       " to the lists of strings with each line being one string\n"  
                      ]   

#        self.helpDict = {k: v for k, v in zip(self.cdList,action_list)}

        if(self.HELP_DICT_INIT):
            pass
        else:
            self.HELP_DICT_INIT = True
            self.helpDict = dict(zip(self.cdList,action_list))

        if(string in self.cdList):
            if(self.debug):
                print(self.space+string+":\n")
                print(helpDict[string])
            return self.helpDict
        else:
            return None


    def errPrint(self, errMsg, input=False, funcAdd=None):
        '''
        Description: Checks if input is, or evaulates to, False
                     and then returns and error message, if True
                     returns True

        '''
        if(input):
            return False
        else:
            if(self.debug):
                funcStr = ''
                if(isinstance(funcAdd,str)):
                    funcStr = "[PP]["+funcAdd+"]"
                else:
                    funcStr = "[PP]"
                print(self.space+funcStr+errMsg+"\n")
            return True


    def __cmdInputParse__(self, string):
        '''
        ---------------------
        | __cmdInputParse__ |
        ---------------------
        
        Input:

            string : a string, formatted for use in the .cmd() function
         
        output:

            outInst : a tuple formatted for parsing in the .cmd() function
                       takes the form: (cmdInst, [objStrs], destStr)
            cmdInst : a string, corrosponding to a valid cmd command
            objStrs: one or more strings, corrosponding to instances
                        upon which the cmdInst acts
            destStr : a string, corrosponding to a valid destination
                       (used only when applicable)

        '''

        def combine_list_str(array, span, ignore=None, space=False):

            out_string = ''
            count = 0
            if(ignore != None):
                for i in array:
                    if(count not in ignore):
                        if(space):
                            if(count < len(array)-len(ignore)-1):
                                out_string = out_string+i+' '
                            else:
                                out_string = out_string+i
                        else:
                            out_string = out_string+i
                    count+=1
                return out_string
            else:
                if(span[1] == 'End' or span[1] == 'end' or span[1] == '' or span[1] == -1):
                    abridged_list = array[span[0]:]
                else:
                    abridged_list = array[span[0]:span[1]]

                count = 0
                for i in abridged_list:
                    if(space):
                        if(count < len(abridged_list)-1):
                            out_string = out_string+i+' '
                        else:
                            out_string = out_string+i
                    else:
                        out_string = out_string + i
                    count += 1
                return out_string

        # Function Start
        if(not isinstance(string, str)):
            if(self.debug):
                print("Error: input must be a string, not a "+str(type(string)))
            return ('', [], '')

        inputList = filter(lambda entry: entry != '',string.split(" "))
        cmdInst = inputList[0]

        if(cmdInst in self.singleCommandList):
            outInst = (cmdInst, [], '')
            return outInst

        if(cmdInst in self.singlePathListNoGroup):
            outInst_str = combine_list_str(inputList,[1,'End'],space=True)
            if(cmdInst != 'vi'):
                outInst = (cmdInst, [], outInst_str)
            else:
                outInst = (cmdInst, [outInst_str], '')
            return outInst

        if(cmdInst in self.singlePathListGroup):
            if(';' in string):
                inst_str = combine_list_str(inputList, [1,'End'], space=True)
                outInst_list = inst_str.split(';')
                outInst_list = filter(lambda l: l != '', outInst_list)
                outInst = (cmdInst, outInst_list, '')
                return outInst
            else:
                outInst_str = combine_list_str(inputList, [1,'End'], space=True)
                outInst = (cmdInst, [outInst_str], '')
                return outInst

        if(cmdInst in self.doublePathList):
            if(';' in string):
                dest_list = []
                while(';' not in inputList[-1]):
                    dest_list.append(inputList.pop(-1))
                dest_list = dest_list[::-1]
                destStr = combine_list_str(dest_list, [0,'End'], space=True)
                inst_str = combine_list_str(inputList, [1,'End'], space=True)
                outInst_list = inst_str.split(';')
                outInst_list = filter(lambda l: l != '', outInst_list)
                outInst = (cmdInst, outInst_list, destStr)
                return outInst
            else:
                if(len(inputList) == 3):
                    outInst = (cmdInst, [inputList[1]], inputList[2])
                elif('.' in string):
                    dest_list = []
                    while('.' not in inputList[-1]):
                        dest_list.append(inputList.pop(-1))
                    print(inputList)
                    dest_list = dest_list[::-1]
                    destStr = combine_list_str(dest_list,[0,'End'], space=True)
                    inst_str = combine_list_str(inputList,[1,'End'], space=True)
                    outInst = (cmdInst, [inst_str], destStr)
                else:
                    print("Error: The input spaceing or object style created ambiguity for the indexer: ")
                    print("The following is an echo of the input string which caused the issue: '"+string+"'")
                    outInst = (cmdInst, [], '')
                    return outInst

                return outInst

        if(self.debug):
            print("Error: command +'"+cmdInst+"' not recognized, use 'help' to view available functions")
        return None


    def uniqueName(self, destPath, objName, uniqueNameLimit = 500):
        '''
        Description: 

        Inputs: 

            destPath : [string], [array],
                       A pathway formatted string or array

            objName  : [string]
                       A string corrosponding to an object,
                       The string will be checked against
                       the names of objects in the destPath
                       directory, if there is overlap the
                       a indexer number will be added until
                       there is no overlap or index limit
                       number is exceeded.

        output: A string if no error is detected, else False
        '''

        contents = self.contentPath(destPath)
        if(self.errPrint("[uniqueName] Error: input 'destPath' must be a directory",contents)): 
            return False

        nameList = strl.str_to_list(objName, spc='.')
        name = ''

        # Checks if there is a file ending on 'objName', if there isn't one unique name is determined
        if(len(nameList) > 1):
            pass
        elif(len(nameList) == 1):
            name = nameList[0]
            if(len(name) > 0):
                count = 1
                outName = name
                while(outName in contents):
                    if(count > uniqueNameLimit):
                        self.errPrint("[uniqueName] Error: iteration overflow, exiting function...")
                        return False                    
                    outName = name+"_"+str(count)
                    count += 1
                return outName
            else:
                self.errPrint("[uniqueName] Error: 'objName' is empty")
        else:
            self.errPrint("[uniqueName] Error: 'objName' is empty")
            return False

        # If there is a file ending attached to 'objName', the unique name is generated
        count = 1
        name = objName
        pad = newList[-2]
        while(name in contents):
            if(count > uniqueNameLimit):
                self.errPrint("[uniqueName] Error: iteration overflow, exiting function...")
                return False
            newList[-2] = pad+"_"+str(count)
            name = strl.array_to_str(newList, spc='.')
            count+=1
        return name


    def joinNode(self, oldPath, newNode):
        '''
        Description: Adds a new node onto a string Pathway

        Input :

            oldPath : [string], pathway formatted string
            newPath : [string], node

        Output : [string], pathway formatted string
        '''

        if(not isinstance(oldPath, str)):
            self.errPrint("[joinNode] Error: 'oldPath' must be a string, 'oldPath' : '"+str(oldPath)+"'")
            return False

        if(not isinstance(newNode, str)):
            self.errPrint("[joinNode] Error: 'newNode' must be a string, 'newNode' : '"+str(newNode)+"'")
            return False

        newPath = oldPath+self.delim+newNode
        return newPath


    def delNode(self, oldPath, nodeID=None):
        '''
        Description: deletes node onto a pathway, starting at the end

        Input :

            oldPath : [string], pathway formatted string
            nodeID  : [None or Int], nodes to be deleted from end

        Output : [string], pathway formatted string
        '''

        oldPath = self.convertPath(oldPath, outType="list")
        if(oldPath == False):
            self.errPrint("[delNode] Error: input 'oldPath' must be a string")
            return False

        n = len(oldPath)

        if(n < 1):
            self.errPrint("[delNode] Error: pathway is empty")
            return False
        elif(n == 1):
            self.errPrint("[delNode] Error: home directory reached, cannot delete home node")
            return self.convertPath(oldPath)
        else:
            pass

        if(nodeID == -1 or nodeID == None):
            newPath = oldPath[:-1]
            strPath = self.Arr2Str(newPath)
            return strPath
        elif(isinstance(nodeID, int)):
            try:
                if(nodeID != 0):
                    newPath = oldPath[:nodeID]
                else:
                    newPath = oldPath
                strPath = self.Arr2Str(newPath)
            except:
                self.errPrint("[delNode] Error: 'nodeID' : "+str(nodeID)+" out of range")
                strPath = False
            return strPath
        else:
            self.errPrint("[delNode] Error: 'nodeID' not recognized")
            return False
        return False


    def getNode(self, inPath, nodeID=None):

        pathList = self.convertPath(inPath, outType='list')
        if(pathList == False):
            self.errPrint("[getNode] Error: input 'path' could not be converted to a pathway list")
            return False

        if(nodeID == None or nodeID == -1):
            if(len(pathList) > 0):
                return pathList[-1]
            else:
                self.errPrint("[getNode] Error: pathway is empty")
                return False
        elif(isinstance(nodeID, int)):
            try:
                nodeValue = pathList[nodeID]
                return nodeValue
            except:
                self.errPrint("[getNode] Error: node id: "+str(nodeID)+" not found")
                return False
        else:
            self.errPrint("[getNode] Error: 'nodeID' not recognized : '"+str(nodeID)+"'")
            return False
        return False


    def Arr2Str(self, inPath):

        if(not isinstance(inPath, (list, tuple))):
            self.errPrint("[Arr2Str] Error: input 'path' must be a python array")
            return False
        else:
            inPath = filter(None, inPath)
            if(len(inPath) < 1):
                self.errPrint("[Arr2Str] Error: 'inPath' must contain at least one pathway entry")
                return False

        for i,dir in enumerate(inPath):
            if(i == 0):
                outPath = str(dir)
                if(self.varOS == 'linux'):
                    outPath = '/'+outPath
            else:
                outPath = self.joinNode(outPath, str(dir))
                if(outPath == False):
                    if(self.debug):
                        errMSG = self.space+"[Arr2Str] Error: could not join the "
                        errMSG = errMSG+strl.print_ordinal(i+1)
                        errMSG = errMSG+" entry of input, 'inPath'\n"
                        print(errMSG)
                    return False

        if(self.varOS == 'windows' and len(inPath)==1):
            outPath = outPath+"\\"

        return outPath


    def Str2Arr(self, inPath):

        if(not isinstance(inPath,str)):
            self.errPrint("[Str2Arr] Error: input 'inPath' must be a string")
            return False
        else:
            try:
                outPath = filter(None,inPath.split(self.delim))
            except:
                outPath = False
            return outPath
        return False


    def convertPath(self, inPath, outType='str'):
        '''
        --------------
        | convertPath |  :  Convert Pathway
        --------------

        description : converts between list formatted pathways and str formatted pathways

        Inputs :

            inPath : a pathway (formatted as either a string or array)
            outType : [string] (Default value : 'str'), corrosponding to a python data-type

        Output : Path formatted list or string
        '''

        if(not isinstance(outType, str)):
            self.errPrint("[convertPath] Error: 'outType' must be a string")
            return False
        else:
            outType = outType.lower()

        if(isinstance(inPath, (list, tuple))):
            if(outType in self.typeList):
                if(outType == 'arr' or outType == 'array'):
                    return inPath
                elif(outType == 'list'):
                    return list(inPath)
                else:
                    return tuple(inPath)
            elif(outType in self.typeStr):
                return self.Arr2Str(inPath)
            else:
                self.errPrint("[convertPath] Error: input 'outType' not recognized")
                return False

        elif(isinstance(inPath, str)):
            if(outType in self.typeStr):
                return inPath
            elif(outType in self.typeList):
                if(outType == 'arr' or outType == 'array' or outType == 'list'):
                    return self.Str2Arr(inPath)
                else:
                    return tuple(self.Str2Arr(inPath))
            else:
                self.errPrint("[convertPath] Error: input 'outType' not recognized")
                return False
        else:
            self.errPrint("[convertPath] Error: input 'inPath' not a recognized type")
            return False
        self.errPrint("[convertPath] Error: path conversion failed; cause unknown")
        return False


    def contentPath(self, inPath, objType = 'all', fileStyle = None):
        '''
        ---------------
        | contentPath |
        ---------------

        Description: Returns a list of strings corrosponding to the contents of
                     the an input path's directory. Option for selecting only a
                     specific object (folder, file or file extension). 

        Input:

            'inPath'   : A Pathway; may be in either string or array format.

            'objType'  : Type of object, may be 'all', 'file' or 'folder'. Note
                         that 'objType' takes precedent over 'fileStyle'.

            'fileStyle': [string], (None), A string corrosponding to a file extension
                                           type. Note that 'objType' must be set to 'file'
                                           for 'fileStyle' to take effect.

        Return:

            'file_list': [list], A list of strings corrosponding to all the files
                                 in the current (path) directory matching the
                                 'fileStyle' extension, if 'fileStyle' == None, then all
                                 file names are included in 'file_list'.
        '''

        if(isinstance(inPath,str)):
            path = inPath
        elif(isinstance(inPath,(list,tuple))):
            path = self.Arr2Str(inPath)
        else:
            self.errPrint("[contentPath] Error: input 'inpath' must be either an Array or Str type")
            return False
        if(os.path.isdir(path) == False):
            if(self.debug):
                print(self.space+"[contentPath] Error: pathway 'inpath' does corrospond to a directory")
                print(self.space+"Pathway : "+str(path)+"\n")
            return False

        if(isinstance(objType,str)):
            objType = objType.lower()
        else:
            self.errPrint("[convertPath] Error: 'objType' must be a string")
            return False

        try:
            pathContents = os.listdir(path)
        except:
            if(self.debug):
                print(self.space+"[contentPath] Error: could not retrieve contents of path")
                print(self.space+"path: "+path+"\n")
            return False

        if(objType.lower() == 'all'):
            output = pathContents
        elif(objType.lower() in self.fileNames):
            if(fileStyle == None or not isinstance(fileStyle,(str,tuple,list))):
                output = [entry for entry in pathContents if os.path.isfile(self.joinNode(path,entry))]
            else:
                file_List = []
                if(isinstance(fileStyle,str)):
                    fileType = '.'+fileStyle
                    for entry in pathContents:
                        if(fileType in entry):
                            file_List.append(entry)
                    output = file_List
                else:
                    for ending in fileStyle:
                        fileType = '.'+str(ending)
                        for entry in pathContents:
                            if(fileType in entry):
                                file_List.append(entry)
                    output = file_List
        elif(objType.lower() in self.dirNames):
            output = [entry for entry in pathContents if os.path.isdir(self.joinNode(path,entry))]
        else:
            output = False

        return output


    def __updatePath__(self, newPath):
        '''
        ------------------
        | __updatePath__ |
        ------------------
                    
        Description: Formats a path-formatted list into a path-formatted string,
                     the new path then replaces the old path directory along with
                     replacing the old path variables with those of the new path.

        Input:

            'newPath': [list,tuple], A path-formatted list

        Output : [Bool], success
        '''

        if(isinstance(newPath,str)):
            self.varPath = newPath
            self.varPath_List = self.Str2Arr(newPath)
            if(self.varPath_List == False):
                self.errPrint("[__updatePath__] Error: failure to convert 'newPath' to a list")
                return False
        elif(isinstance(newPath,(list,tuple))):
            self.varPath = self.Arr2Str(newPath)
            if(self.varPath == False):
                self.errPrint("[__updatePath__] Error: failure to convert 'newPath' to a str")
                return False
            self.varPath_List = list(newPath)
        else:
            self.errPrint("[__updatePath__] Error: 'newPath' not a recognized type")
            return False

        self.varPath_Head = self.varPath_List[0]
        if(self.varOS == 'windows'):
            self.varPath_Head = self.varPath_Head+"\\"
        self.varPath_Dir  = self.varPath_List[-1]

        self.varPath_Contains = self.contentPath(self.varPath,'all')
        if(self.varPath_Contains == False):
            self.errPrint("[__updatePath__] Error: failure to get contents from current pathway")
            return False

        self.varPath_Files = self.contentPath(self.varPath,'files')
        if(self.varPath_Files == False):
            self.errPrint("[__updatePath__] Error: failure to get files found in current pathway")
            return False

        self.varPath_Folders = self.contentPath(self.varPath,'folders')
        if(self.varPath_Contains == False):
            self.errPrint("[__updatePath__] Error: failure to get directories found in current pathway")
            return False

        return True


    def __climbPath__(self, node):
        '''
        Description : if 'node' is a node in the default (current) pathway
                      that the default (current) pathway directory is moved to

        Input:

            'node' : [string], corrosponding to a node within the current pathway

        The overhead and updating of class path info is taken care of with this function
        '''
        newPath_list = []
        if(node in self.varPath_List):

            for entry in self.varPath_List:
                if(entry != node):
                    newPath_list.append(entry)
                else:
                    break
            newPath_list.append(node)
            output = self.__updatePath__(newPath_list)
            return output
        else:
            self.errPrint("[__climbPath__] Warning: Directory "+node+" not found in current (path) hierarchy")
            return False
        return True


    def renamePath(self, originPath, destPath, objName=None, climbPath=False):
        '''
        Description : Takes an input pathway and an destination pathway along 
                      options for the object's name and climbing pathway if
                      destination path terminates with a non-folder object.

                      The final node of the input pathway determines the original
                      name of the object. If 'objName' is a string then the new
                      path of the object will replace the object's original name

        Usage: This function is useful when working with the pathways of objects
               to be moved or copied between directories; ensures that the no
               error will occured due to duplicated file names

        Input :

            originPath : [string], A complete object pathway, the final node may be either a file or directory
            destPath   : [string], A directory pathway for the destination, the final node must be a directory
            objName    : [string] (None), If a string, this string will be the final node in 'newPath' output
            climbPath  : [bool] (False), If true then if 'destPath' does have a directory as the final node,
                                         the node will be climbed unitil a directory is found or the home
                                         directory is reached

        Output : [Bool], success
        '''

        def __create_path__(novPath, novName):

            dNode = self.uniqueName(novPath, novName)
            if(dNode == False):
                errPrint("[renamePath][__create_path__] Error: Failure to generate a unique name from input path")
                return False
            return self.joinNode(novPath, dNode)


        destNode = self.getNode(originPath)
        originPath = self.convertPath(originPath)
        destPath = self.convertPath(destPath)

        if(destNode == False):
            self.errPrint("[renamePath] Error: could not get terminating node from 'originPath'")
            return False

        # If the objName variable is changed to a string 
        if(isinstance(objName,str)):
            if(os.path.isdir(destPath)):
                pass
            else:
                if(self.debug):
                    print(self.space+"[PP][renamePath] Error: 'destPath' does not point to a directory")
                    print(self.space+"If 'objName' is set, then the 'destPath' pathway must point to a directory")
                    print(self.space+"'destPath': "+str(destPath)+'\n')
                return False

            newPath = __create_path__(destPath, objName)
            if(newPath == False):
                self.errPrint("[renamePath] Error: new pathway could not be established")
            return newPath

        # Default method: will attempt to establish a unique pathway 
        else:
            if(os.path.isdir(destPath)):
                newPath = __create_path__(destPath, destNode)
                if(newPath == False):
                    self.errPrint("[renamePath] Error: new pathway could not be established")
                return newPath

            # climbPath option----
            if(climbPath):
                parentPath = self.delNode(destPath)

                while(self.convertPath(parentPath) != self.varPath_Head):
			    
                    if(parentPath == False):
                        self.errPrint("[renamePath] Error: could not move up the 'destPath' pathway")
                        return False
			        
                    if(os.path.isdir(parentPath)):
                        destNode = self.uniqueName(parentPath,destNode)
                        newPath = self.joinNode(parentPath,destNode)
                        if(newPath == False):
                            self.errPrint("[renamePath] Error: could add directory name node to 'destPath'")
                            return False
                        return newPath
                    else:
                        if(self.debug):
                            print(self.space+"[PP][renamePath] Error: 'destPath' does not point to a valid pathway destination")
                            print(self.space+"'destPath': "+str(destPath)+'\n')

                    parentPath = self.delNode(parentPath)

                self.errPrint("[renamePath] Error: couldn't find valid destination before 'home' directory")

            self.errPrint("[renamePath] Error: 'destPath' does not point to a valid pathway destination")

        return False


    ###########################################################
    # Move File and Directories from one Directory to another #
    ###########################################################

    def moveObj(self, objPath, destPath, objName=None, renameOverride=None):
        '''
        Description : Moves and renames file and directory objects

        Input :

            objPath  : [string] [array], 
                       A complete object pathway, either string or array. 
                       The final node may be either a file or directory.

            destPath : [string] [array], 
                       A complete directory pathway, either string or array.
                       The final node must be a directory.

            objName  : [string] [None by default], 
                       If a string, then the object will be renamed to the string.

            renameOverride : [Bool] [None by default], 
                             If a boolean then will override the 'self.rename' option.

        Output : [Bool], success
        '''

        #Parse object pathway into the string format
        if(isinstance(objPath,(list,tuple))):
            objPath = self.convertPath(objPath)
            if(objPath == False):
                self.errPrint("[moveObj] Error: failure to convert input 'objPath' to a string")
                return False
        elif(isinstance(objPath,str)):
            pass
        else:
            self.errPrint("[moveObj] Error: 'objPath' must be either a pathway formatted string or array")
            return False

        #Parse destination pathway into the string format
        if(isinstance(destPath,(list,tuple))):
            destPath = self.convertPath(destPath)
            if(destPath == False):
                self.errPrint("[moveObj] Error: failure to convert input 'destPath' to a string")
                return False
        elif(isinstance(destPath,str)):
            pass
        else:
            self.errPrint("[moveObj] Error: 'destPath' must be either a pathway formatted string or array")
            return False

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(objPath, destPath, objType = 'all', objName = objName)
            if(destPath == False):
                self.errPrint("[moveObj] Error: failure to generate 'destPath' destination pathway")
                return False
        else:
            if(isinstance(objName,str)):
                destPath = self.joinNode(destPath,objName)
            else:
                destPath = destPath

        #Move contents of 'objPath' to the 'destPath' destination
        try:
            shutil.move(objPath,destPath)
            success = True
        except:
            if(self.debug):
                print(self.space+"[moveObj] Error: object could not be moved.")
                print(self.space+"File pathway: "+str(objPath))
                print(self.space+"Destination pathway: "+str(destPath)+"\n")
            success = False

        # return success boolean
        return success


    def __moveObj__(self, objPath, newPath, objName=None, renameOverride=None):

        success = self.moveObj(objPath, newPath, objName=objName, renameOverride=renameOverride)
        if(not success):
            self.errPrint("[__moveObj__] Error: failure to perform move operation")
            return success

        try:
            startDir = self.convertPath(objPath,"list")[-2]
        except:
            self.errPrint("[__moveObj__] Error: failure to find folder for object pathway")
            startDir = False
        try:
            finalDir = self.convertPath(newPath,"list")[-1]
        except:
            self.errPrint("[__moveObj__] Error: failure to find folder for new pathway")
            finalDir = False

        if(startDir == self.varPath_Dir or finalDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath)
            if(not success):
                self.errPrint("[__moveObj__] Error: failure to update pathway")
        else:
            success = False

        return success

    ############################
    # Delete File from Pathway #
    ############################

    def delFile(self, delPath):
        '''
        Description : Attempts to delete the content at the location of the input pathway

        Input:

            delPath : A complete pathway string pointing to a file

        Output : [Bool], success
        '''

        if(isinstance(delPath,(list,tuple))):
            delPath = self.convertPath(delPath)
            if(delPath == False):
                self.errPrint("[delFile] Error: failure to convert input 'delPath' to a string")
                return False
        elif(isinstance(delPath,str)):
            pass
        else:
            self.errPrint("[delFile] Error: 'delPath' must be either a pathway formatted string or array")
            return False

        if(os.path.isfile(delPath)):
            pass
        else:
            print(self.space+"[delFile] Error: 'delPath' does not point to a file")
            print(self.space+"File pathway: "+str(delPath)+'\n')
            return False

        try:
            os.remove(delPath)
        except:
            if(self.debug):
                print("[delFile] Error: Failure to delete file")
                print("File pathway: "+delPath+"\n")
            return False

        return True


    def __delFile__(self, delPath):

        success = self.delFile(delPath)
        if(not success):
            self.errPrint("[__delFile__] Error: failure to perform move operation")
            return success

        try:
            startDir = self.convertPath(delPath,"list")[-2]
        except:
            self.errPrint("[__delFile__] Error: failure to find folder for object pathway")
            startDir = False

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath)
            if(not success):
                self.errPrint("[__delFile__] Error: failure to update pathway")
        else:
            success = False

        return success

    #############################################
    # Copy object from one directory to another #
    #############################################

    def copyFile(self, filePath, destPath, objName=None, renameOverride=None):
        '''
        Description : Attempts to copy a file from the 'filePath' full pathway
                      to the full directory pathway 'destPath', with a name
                      given by 'objName'

        Input :

            filePath : [string] corrosponds to full pathway of the location of the file to be copied
            destPath : [string], corrosponds to the pathway of the copied file
            objName  : [string] (Default : None), corrosponds to full pathway of the location of the copy             

        Output : [Bool], success
        '''

        if(isinstance(filePath,(list,tuple))):
            filePath = self.convertPath(filePath)
            if(filePath == False):
                self.errPrint("[copyFile] Error: failure to convert input 'filePath' to a string")
                return False
        elif(isinstance(filePath,str)):
            pass
        else:
            self.errPrint("[copyFile] Error: 'filePath' must be either a pathway formatted string or array")
            return False

        if(isinstance(destPath, (list, tuple))):
            destPath = self.convertPath(destPath)
            if(destPath == False):
                self.errPrint("[copyFile] Error: failure to convert input 'destPath' to a string")
                return False
        elif(isinstance(destPath,str)):                                                                                 
            pass
        else:
            self.errPrint("[copyFile] Error: 'destPath' must be either a pathway formatted string or array")
            return False

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(filePath, destPath, objType='file', objName=objName)
            if(destPath == False):
                self.errPrint("[copyFile] Error: failure to generate 'destPath' destination pathway")
                return False
        else:
            if(isinstance(objName,str)):
                destPath = self.joinNode(destPath,objName)
            else:
                destPath = destPath  

        try:
            shutil.copyfile(filePath, destPath)
        except:
            if(self.debug):                               
                print(self.space+"[copyFile] Error: file could not be copied.")
                print(self.space+"File pathway: "+str(filePath))
                print(self.space+"Destination pathway: "+str(destPath)+"\n")
            return False

        return True


    def __copyFile__(self, objPath, newPath, objName=None, renameOverride=None):

        success = self.copyFile(objPath, newPath, objName=objName, renameOverride=renameOverride)
        if(not success):
            self.errPrint("[__copyFile__] Error: failure to perform move operation")
            return success

        try:
            if(isinstance(objName,str)):
                startDir = self.convertPath(objPath, "list")[-1]
            else:
                startDir = self.convertPath(objPath, "list")[-2]
        except:
            self.errPrint("[__copyFile__] Error: failure to find folder for object pathway")
            startDir = False

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath)
            if(not success):
                self.errPrint("[__copyFile__] Error: failure to update pathway")
        else:
            success = False

        return success

    ######################
    # Make new directory #
    ######################
 
    def makeDir(self, dirPath, dirName=None, renameOverride=None):
        '''
        Description : Attempts to create a folder at the full pathway string, 'dirPath'.
                      If 'dirName' is a a string, then this string will be appended onto
                      the pathway and used as the new folder name

        Input :

            dirPath : [string] corrosponds to full pathway of the location of the file to be copied
            fileName  : [string] (Default : None), corrosponds to full pathway of the location of the copy

        Output : [Bool], success
        '''

        if(isinstance(dirPath,(list,tuple))):
            dirPath = self.convertPath(dirPath)
            if(dirPath == False):
                if(self.debug):
                    print(self.space+"[makeDir] Error: failure to convert input 'dirPath' to a string\n")
                    print(self.space+"[makeDir] 'dirPath' : '"+str(dirPath)+"'\n")
                return False
        elif(isinstance(dirPath,str)):
            pass
        else:
            if(self.debug):
                print(self.space+"[makeDir] Error: 'dirPath' must be either a pathway formatted string or array\n")
                print(self.space+"[makeDir] 'dirPath' : '"+str(dirPath)+"'\n")
            return False

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(dirPath, dirPath, objType = 'directory', objName = dirName)
            if(destPath == False):
                if(self.debug):
                    print(self.space+"[makeDir] Error: failure to generate 'destPath' destination pathway\n")
                    print(self.space+"[makeDir] 'dirPath' : '"+str(dirPath)+"'\n")
                return False
        else:
            if(isinstance(dirName,str)):
                destPath = self.joinNode(dirPath,dirName)
            else:
                destPath = dirPath  

        try:
            os.mkdir(destPath)
        except:
            print(self.space+"[makeDir] Error: directory could not be created")
            print("Pathway : "+destPath+'\n')
            return False

        return True 


    def __makeDir__(self, dirPath, dirName=None, renameOverride=None):

        success = self.makeDir(self, dirPath, dirName=dirName, renameOverride=renameOverride)
        if(not success):
            self.errPrint("[__makeDir__] Error: failure to perform move operation")
            return success

        try:
            if(isinstance(dirName,str)):
                newDir = dirName
            else:
                newDir = self.convertPath(dirPath,"list")[-2]
        except:
            self.errPrint("[__makeDir__] Error: failure to find new pathway directory")
            success = False
            newDir = False

        if(newDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath)
            if(not success):
                self.errPrint("[__makeDir__] Error: failure to update pathway")
        else:
            success = True

        return success


    ##############################
    # Delete directory from path #
    ##############################

    def delDir(self, delPath):
        '''
        Description : Recursively removes content and directory at pathway 'delPath'

        Input : 

            delPath : [string], corrosponds to path containing directory to be deleted

        Output : [Bool], success
        '''
        if(isinstance(delPath,(list,tuple))):
            delPath = self.convertPath(delPath)
            if(delPath == False):
                self.errPrint("[delDir] Error: failure to convert input 'delPath' to a string")
                return False
        elif(isinstance(delPath,str)):
            pass
        else:
            self.errPrint("[delDir] Error: 'delPath' must be either a pathway formatted string or array")
            return False

        if(os.path.isdir(delPath)):
            pass
        else:
            if(self.debug):
                print(self.space+"[delDir] Error: 'delPath' does not point to a folder")
                print(self.space+"File pathway: "+str(delPath)+'\n')
            return False

        try:
            shutil.rmtree(delPath)
        except:
            if(self.debug):
                print(self.space+"[delDir] Error: directory could not be deleted")
                print(self.space+"File pathway: "+str(delPath)+'\n')
            return False

        return True


    def __delDir__(self, delPath):

        success = self.delFile(delPath)
        if(not success):
            if(self.debug):
                print(self.space+"[__delDir__] Error: failure to perform move operation")
            return success

        try:
            startDir = self.convertPath(delPath,"list")[-2]
        except:
            self.errPrint("[__delDir__] Error: failure to find folder for object pathway")
            startDir = False

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath)
            if(not success):
                self.errPrint("[__delDir__] Error: failure to update pathway")
        else:
            success = False

        return success

    ##########################################
    # Copy directory from path to a new path #
    ##########################################


    def copyDir(self, dirPath, destPath, dirName=None, renameOverride=None):
        '''
        Description : Attempts to copy contents from 'dirPath' full pathway
                      to the full directory pathway 'destPath', optional, the
                      string found in 'dirName' will be the name of the new
                      directory, else the new directory will have the same
                      name as the old one.

        Input :

            dirPath : [string] corrosponds to full pathway of the location of the file to be copied
            destPath  : [string], corrosponds to the pathway of the copied file
            dirName  : [string] (Default : None), corrosponds to full pathway of the location of the copy

        Output : [Bool], success
        '''

        if(isinstance(dirPath,(list, tuple))):
            dirPath = self.convertPath(dirPath)
            if(dirPath == False):
                self.errPrint("[copyFile] Error: failure to convert input 'dirPath' to a string")
                return False
        elif(isinstance(dirPath,str)):
            pass
        else:
            self.errPrint("[copyFile] Error: 'dirPath' must be either a pathway formatted string or array")
            return False

        if(isinstance(destPath, (list, tuple))):
            destPath = self.convertPath(destPath)
            if(destPath == False):
                self.errPrint("[copyFile] Error: failure to convert input 'destPath' to a string")
                return False
        elif(isinstance(destPath, str)):
            pass
        else:
            self.errPrint("[copyFile] Error: 'destPath' must be either a pathway formatted string or array")
            return False

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(dirPath, destPath, objType='all', objName=dirName)
            if(destPath == False):
                self.errPrint("[PP][moveObj] Error: failure to generate 'destPath' destination pathway")
                return False

        try:
            shutil.copyfile(dirPath, destPath)
        except:
            if(self.debug):
                print(self.space+"[PP][copyDir] Error: directory could not be copied.")
                print(self.space+"Directory pathway, 'dirPath': "+str(dirPath))
                print(self.space+"Destination pathway, 'destPath': "+str(destPath)+"\n")
            return False
        return True


    def __copyDir__(self, dirPath, destPath, dirName=None, renameOverride=None):

        success = self.copyDir(dirPath, destPath, dirName=dirName, renameOverride=renameOverride)
        if(not success):
            self.errPrint("[__copyDir__] Error: failure to perform move operation")
            return success

        try:
            if(isinstance(dirName,str)):
                startDir = self.convertPath(destPath, "list")[-1]
            else:
                startDir = self.convertPath(destPath, "list")[-2]
        except:
            self.errPrint("[__copyDir__] Error: failure to find folder for object pathway")
            startDir = False

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath)
            if(not success):
                self.errPrint("[__copyDir__] Error: failure to update pathway")
        else:
            success = False

        return success


    #############################
    # find object(s) in pathway #
    #############################

    def find(self, objName, dirPath, objType='all'):
        '''
        Description : Searches an input directory for an object name

        Input :

            objName : [string or list of strings], Name of file(s) to be searched for
            dirPath : [string], pathway of directory for which 'objName' is to be searched
            objType : [string] (Default : 'all'), type of object to be searched for

        Output : False if error occurs, else a dictionary 
                 The output dictionary contains the input object names as keys and 
                 the truth value of their existance in the input directory as values 
        '''

        contents = self.contentPath(dirPath, objType=objType)
        if(contents == False):
            self.errPrint("[find] Error: failure to get contents of pathway 'dirPath'")
            return False

        if(isinstance(objName, str)):
            if(objName in contents):
                within = True
            else:
                within = False
            return {objName:within}
        elif(isinstance(objName,(list, tuple))):
            outDict = {}
            for obj in objName:
                if(obj in contents):
                    within = True
                else:
                    within = False
                outDict[obj] = within
            return outDict
        else:
            self.errPrint("[find] Error: input 'objName' must be either a string or an array")
            return False
        return False

    def __find__(self, objName, objType='all'):

        outDict = self.find(objName, self.varPath, objType=objType)
        if(outDict == False):
            self.errPrint("[__find__] Error: failure to perform internal 'find' operation")
            return False
        else:
            return outDict


    #################################################
    # find object(s) containing fragment in pathway #
    #################################################

    def match(self, fragment, dirPath, objType='all'):
        '''
        Description : Searches an input directory for any object containing a specific string 

        Input :

            fragment : [string or list of strings], string fragment to be matched
            dirPath : [string], pathway of directory for which 'fragment' is to be searched
            objType : [string] (Default : 'all'), type of object to be searched for

        Output : [Bool], success
        '''

        contents = self.contentPath(dirPath, objType=objType)
        if(contents == False):
            self.errPrint("[match] Error: failure to get contents of pathway 'dirPath'")
            return False

        if(isinstance(fragment, str)):
            capList = []
            for entry in contents:
                if(fragment in entry):
                    capList.append(entry)
            return {fragment:capList}
        elif(isinstance(fragment, (list, tuple))):
            outDict = {}
            for frag in fragment:
                capList = []
                for entry in contents:
                    if(fragment in entry):
                        capList.append(entry)
                outDict[frag] = capList
            return outDict
        else:
            self.errPrint("[match] Error: input 'fragment' must be either a string or an array")
            return False
        return False

    def __match__(self, fragment, objType='all'):

        outDict = self.match(fragment, self.varPath, objType=objType)
        if(outDict == False):
            self.errPrint("[__match__] Error: failure to perform internal 'match' operation")
            return False
        else:
            return outDict


    ######################
    # printing functions #
    ######################

    def __fancyPrint__(self, colour=False):
        '''
        Description : Stylized printing of path information

        Input :
            colour : [Bool], color option for distinguishing folders from files

        Output : [Bool], success
        '''
        if(colour):
            blue = '\033[38;5;4m'
            black = '\033[38;5;0m'
            if(self.varOS == 'unix' or self.varOS == 'linux'):
                black = '\033[38;5;2m'
        else:
            blue,black=('','')

        nl = '\n'
        atsp = '   '
        headln = nl+'The current pathway is: '+nl
        bodyln = nl+'The content of the current directory is as follows: '+nl

        print(headln)
        print(atsp+self.varPath)

        try:
            spc = self.varPath_Contains
            spf = self.varPath_Files

            print(bodyln)
            for i in spc:
                if(i in spf):
                    print(black+atsp+i)
                else:
                    print(blue+atsp+i)
            print(black)
            return True

        except:
            return False


    def __runFancyPrint__(self):
        if(self.shellPrint and self.debug):
            try:
                ecrive = self.__fancyPrint__(self.varCol)
                return ecrive
            except:
                return False
        else:
            return True


    def __fancyPrintList__(self,array):

        nl = '\n'
        atsp = '   '

        print(nl)
        for i in array:
            print(atsp+str(i))
        print(nl)
        return True


    ############################################################
    #                                                          #
    #   ####################################################   #   
    #   # cmd Function: String-to-Command Parsing Function #   #
    #   ####################################################   #
    #                                                          #
    ############################################################

    def cmd(self,cmd_string):

        '''
        -------
        | cmd |
        -------
        
        Input: 

            cmd_string : a string, must be formated according to the specifications below.
        
        Valid Commands: 
        
            'ls' : returns list of strings containing the contents of the present directory
		    
            'dir': returns pathway for file in the current directory
		    
            'pwd'  : Returns current directory pathway as string; equivalent to 'self.varPath'
		    
            'cd' : moves into the input directory, note: input directory must be in current directory
                   ('..' to move upwards) ('\\' or '/' to specify directory in root directory)
                   ('~' moves to home directory)
		    
            'chdir' : moves to the directory input, input must be full directory pathway 
		    
            'mv' : moves file(s) from current directory into another directory 
                   which is accessible to the current path
                   (format note: 'mv file_path.file Directory_Name') [file extension must be included]
		    
            'rm' : remove input file(s) from current directory
		    
            'cp' : copies file(s) to destination
		    
            'mkdir' : make new director(y)ies with name equalivalent to input string
		    
            'rmdir' : delete subdirector(y)ies (equiv. to 'rm -rf Directory_Name')
		    
            'cpdir' : copy directory from current directory
		    
            'find' : Searches the current directory for the input file(s) string and returns boolean
		    
            'match' : Searches the current directory for the input pattern and returns list of matches
		    
            'help' : Returns list of valid commands
		    
            'vi'   : Returns a list of strings corrosponding to the contents of a file
        
        '''

        ##################
        #  Subfunctions  #
        ##################

        def headCheck():                  
            if(len(self.varPath_List) == 1):
                self.errPrint("[headCheck] Warning: No remaining parent directories left", funcAdd = 'cmd')
                return True
            else:
                return False

        def printFunc(test):
            success = True
            if(test):
                ptest = self.__runFancyPrint__()
                if(not ptest):
                    success = False
                    self.errPrint("[printFunc] Error occured while attempting to print...", funcAdd = 'cmd')
            else:
                self.errPrint("[printFunc] Error: Failure while updating current path", funcAdd = 'cmd')
                success = False
            return success

        def updater(newPath, value):
            utest = self.__updatePath__(newPath)                 
            success = printFunc(utest)
            result = (success, (value))
            return result


        def cmd_pwd(tup):
            success = True
            cmdInst, file_list, destStr = tup # allows for expanding functionality

            try:
                value = self.varPath 
            except: 
                value = None
                success = False
                self.errPrint("[cmd_pwd] Error: current (path) directory pathway not found", funcAdd = 'cmd')

            success = printFunc(success)               
            result = (success,(value))                                       
            return result


        def cmd_ls(tup):
            success = True
            cmdInst, file_list, destStr = tup # allows for expanding functionality

            result = updater(self.varPath_List,'')

            try:
                value = self.varPath_Contains
            except:
                value = None 
                success = False
                print("Error: current (path) directory contents not found")

            success = printFunc(success)            
            result = (success,value)
            return result


        def cmd_dir(tup):
            success = True            
            cmdInst, file_list, destStr = tup
                   
            new_file_list = []

            values = self.__find__(file_list)
            if(values == False):
                if(self.debug):
                    msg = "[dir] Error: occured when attempting to check current (path) directory for input files\n"
                    print(self.space+msg)
                return (False,None) 
                                       
            for entry in file_list:
                if(values[entry]):
                    new_file_list.append(self.joinNode(self.varPath,entry))
                else:
                    if(self.debug):
                        msg = "[dir] Warning: file name, '"+str(entry)+"' not found in current (path) directory\n"
                        print(self.space+msg)
            value = new_file_list

            ptest_1 = self.__runFancyPrint__()
            if(self.shellPrint):
                print(self.space+"Pathway string(s): \n")
                ptest_2 = self.__fancyPrintList__(new_file_list)
            else:
                ptest_2 = True

            if(not ptest_1 or not ptest_2):
                success = False
                print(self.space+"Error: An unknown error was raised while attempting to print...\n")

            result = (success,value)                
            return result


        def cmd_cd(tup):
            success = True            
            value = None
            cmdInst, file_list, destStr = tup
                                    
            if(destStr == '..'):                  
                if(headCheck()):
                    result = (success,value)
                    return result 
                else:
                    up_path_list = list(self.varPath_List)[:-1]                 
                result = updater(up_path_list,value)
                return result
            
            elif(destStr in self.varPath_Contains):
                dest_loc = self.joinNode(self.varPath, destStr)
                if(os.path.isdir(dest_loc)): 
                    newPath_list = list(self.varPath_List)
                    newPath_list.append(destStr)
                else:
                    success = False 
                    print("Error: '"+dest_loc+"not a valid folder in current (path) directory")
                    print("It appears that '"+dest_loc+"' is a file object or is corrupted")    
                    result = (success, value)
                    return result 
                result = updater(newPath_list,value)
                return result
            
            elif(destStr[0] == '/' or destStr[0] == '\\'):
                ndir_inst = destStr[1:]
                ctest = self.__climbPath__(-1)
                success = printFunc(ctest)  
                result = (success,value)
                return result
                    
            elif(destStr == '~'):                
                ctest = self.__climbPath__(-1)
                success = printFunc(ctest)  
                result = (success,value)
                return result
                
            else:
                print("Error: '"+destStr+"' not a valid destination")
                success = False
            
            result = (success,value)
            return result
            
            
        def cmd_chdir(tup):
            cmdInst, file_list, destStr = tup

            utest = self.__updatePath__(destStr)
            success = printFunc(utest)
            result = (success,None)
            return result

        def cmd_mv(tup):
            
            success = True            
            value = None
            cmdInst, file_list, destStr = tup      
             
            mv_file_list = file_list 
            
            for i in range(len(mv_file_list)):
                mv_file_list[i] = self.joinNode(self.varPath, mv_file_list[i])
                         
            # Move File                                     
            if(destStr == '..'):                  
                if(headCheck()):
                    result = (success, value)
                    return result  
                else:
                    up_path_list = list(self.varPath_List)[:-1]

                up_path_str = self.convertPath(up_path_list)   
                up_path_has = self.contentPath(up_path_str)
                for i in mv_file_list: 
                    if(i in up_path_has):
                        print("Warning: '"+i+"' already exists in the namespace of the target directory, no action taken")
                        continue                     
                    mtest = self.moveObj(i,up_path_str)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")

                result = updater(self.varPath_List,value)
                return result     
            
            elif(destStr in self.varPath_Contains and destStr not in self.varPath_Files):                
                dest_path_list = list(self.varPath_List)
                dest_path_list.append(destStr)  
                     
                path_str = self.convertPath(dest_path_list)   
                path_has = self.contentPath(path_str)
                for i in mv_file_list:           
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue     
                    mtest = self.moveObj(i,path_str)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.varPath_List, value)
                return result  
            
            elif(destStr[0] == '/' or destStr[0] == '\\'):
                destStr = destStr[1:]
                dest_path_list = self.__climbPath__(-1)

                path_str = self.convertPath(dest_path_list)   
                path_has = self.contentPath(path_str)
                for i in mv_file_list:   
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue            
                    mtest = self.moveObj(i, dest_path_list)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")

                result = updater(self.varPath_List, value)
                return result

            elif(destStr == '~'):
                dest_path_str = self.convertPath(self.varPath_Head)
                path_has = self.contentPath(dest_path_str)
                for i in mv_file_list:
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue
                    mtest = self.moveObj(i, dest_path_list)
                    if(not mtest):
                        success = False
                        print("Error: contents of this path: '"+i+"' could not be moved")

                result = updater(self.varPath_List, value)
                return result

            elif(destStr not in self.varPath_Contains and len(mv_file_list) == 1):          
                mtest = self.moveObj(mv_file_list[0], destStr)
                if(not mtest):
                    success = False
                    print("Error: contents of this path: '"+str(mv_file_list[0])+"' could not be moved")                                 
                result = updater(self.varPath_List, value)
                return result  
            
            else:
                print("Error: Invalid formatting; the input object(s) could not be moved...")
                return None                 
            
            
        def cmd_rm(tup):
                      
            success = True            
            value = None
            cmdInst, file_list, destStr = tup 
            
            # Format
            
            for i in file_list:   
                if(i in self.varPath_Files):
                    file_path_str = self.joinNode(self.varPath,i)
                    dtest = self.delFile(file_path_str)
                    if(not dtest):
                        success = False 
                        print("Error: contents of the path: '"+str(i)+"' could not be deleted")
                else: 
                    print("Error: '"+str(i)+"' not found within the current (path) directory")
            
            result = updater(self.varPath_List, value)
            return result


        def cmd_cp(tup):

            def __cp_help_func__(file_list, path_str):  
                  
                success = True            
                value = None

                path_has = self.contentPath(path_str, objType='files')
                for i in file_list:                    
                    inc = 1
                    file_inst_list = i.split(".")
                    if(len(file_inst_list)>2):
                        print("Warning: file '"+str(i)+"' does not match proper naming conventions")
                    old_inst = self.joinNode(self.varPath,i)
                    cp_inst = file_inst_list[0]+"_copy_"+str(inc)+"."+file_inst_list[1] 
                    while(cp_inst in path_has):
                        inc+=1
                        cp_inst = file_inst_list[0]+"_copy_"+str(inc)+"."+file_inst_list[1] 
                    ctest = self.copyFile(old_inst,path_str,cp_inst)
                    if(not ctest):
                        success = False 
                        print("Error: contents of the path: '"+str(i)+"' could not be copied")
                                                                    
                result = updater(self.varPath_List, value)
                return result
                                
            success = True            
            value = None
            cmdInst, file_list, destStr = tup 
          
            if(destStr == '.'):

                result = __cp_help_func__(file_list, self.varPath)
                return result

            elif(destStr == '..'):

                if(headCheck()):
                    result = (success,value)
                    return result
                else:
                    up_path_list = list(self.varPath_List)[:-1]

                up_path_str = self.convertPath(up_path_list)
                result = __cp_help_func__(file_list, up_path_str)
                return result

            elif(destStr in self.varPath_Contains):
                path_str = self.joinNode(self.varPath, destStr)
                result = __cp_help_func__(file_list, path_str)
                return result

            elif(destStr[0] == '/' or destStr[0] == '\\'):
                ndir_inst = destStr[1:]
                path_str = self.__climbPath__(-1)
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(ndir_inst)+"' could not be found in the root pathway")
                    return (success,value)

                result = __cp_help_func__(file_list, path_str)
                return result
                    
            elif(destStr == '~'):           
                path_str = self.varPath_Head 
                try:                   
                    path_has = self.contentPath(path_str, objType='files')
                except:
                    print("Error: 'home' directory cannot be accessed")
                    return (False,None)
                    
                result = __cp_help_func__(file_list, path_str)
                return result
              
            else:
                print("Error: '"+str(destStr)+"' not a valid destination")
                success = False            
            result = (success,value)
            return result 
            

        def cmd_mkdir(tup):
            
            success = True            
            value = None
            cmdInst, file_list, destStr = tup      
            
            for i in file_list:
                file_path_str = self.joinNode(self.varPath,i)
                ctest = self.makeDir(file_path_str)  
                if(not ctest):
                    success = False 
                    print(self.space+"Error: contents of this path: '"+str(i)+"' could not be moved\n")
                                     
            result = updater(self.varPath_List,value)
            return result  

        
        def cmd_rmdir(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup   
            
            for i in file_list: 
                if(i in self.varPath_Contains):
                    file_path_str = self.joinNode(self.varPath,i)
                    output = self.delDir(file_path_str)
                    if(output == False):
                        success = False
                        print(self.space+"Error: contents of this folder: '"+str(i)+"' could not be deleted\n")

            result = updater(self.varPath_List,value)
            return result        


        def cmd_cpdir(tup):                   

            def __cpdir_help_func__(file_list, path_str):  

                success = True
                value = None

                path_has = self.contentPath(path_str, objType='folders')
                for i in file_list:                    
                    inc = 1
                    old_inst = self.joinNode(self.varPath,i)
                    cp_inst = i+"_copy"
                    while(cp_inst in path_has):
                        inc+=1
                        cp_inst = cp_inst + '_' + str(inc)
                    ctest = self.copyDir(old_inst, path_str, dirName=cp_inst)
                    if(not ctest):
                        success = False 
                        print("Error: contents of the path: '"+str(i)+"' could not be copied")
                                                                    
                result = updater(self.varPath_List,value)
                return result

                             
            # cmd_cpdir MAIN   
            success = True            
            value = None
            cmdInst, file_list, destStr = tup 
          
            if(destStr == '.'):
                        
                result = __cpdir_help_func__(file_list, self.varPath) 
                return result                                  
                       
            elif(destStr == '..'):                  

                if(headCheck()):
                    result = (success,value)
                    return result 
                else:
                    up_path_list = list(self.varPath_List)[:-1]

                up_path_str = self.convertPath(up_path_list)   
                result = __cpdir_help_func__(file_list, up_path_str)
                return result
            
            elif(destStr in self.varPath_Contains):
                path_str = self.joinNode(self.varPath,destStr)  
                result = __cpdir_help_func__(file_list, path_str)
                return result
            
            elif(destStr[0] == '/' or destStr[0] == '\\'):
                ndir_inst = destStr[1:]
                path_str = self.__climbPath__(-1)
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(ndir_inst)+"' could not be found in the root pathway")
                    return (success,value)
                    
                result = __cpdir_help_func__(file_list, path_str)
                return result
                    
            elif(destStr == '~'):           
                path_str = self.varPath_Head                     
                result = __cpdir_help_func__(file_list, path_str)
                return result
              
            else:
                print("Error: '"+str(destStr)+"' not a valid destination")
                success = False            
            result = (success,value)
            return result 
        
        
        def cmd_find(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup   
            
            found_list = []
            for i in file_list:            
                ftest = self.find(i, self.varPath)
                found_list.append(ftest)

#            found_dict = {k: v for k, v in zip(file_list, found_list)}   
            found_dict = dict(zip(file_list,found_list))
                
            if(self.debug):
                if(all(i == True for i in found_list)):
                    print("All Files have been found in the current directory!")
                else:
                    for j in found_dict:
                        if(found_dict[j] == False):
                            print("No file named '"+j+"' found in current directory.")
            
            value = found_dict
            result = (success,value)
            return result
          
        
        def cmd_match(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup   
            
            match_list = []
            for i in file_list:
                gtest = self.match(self.varPath, i)
                match_list.append(gtest)

#            match_dict = {k: v for k, v in zip(file_list, match_list)} 
            match_dict = dict(zip(file_list,match_list))
             
            if(self.debug):
                for i in file_list:
                    if(len(match_dict[i]) == 0):
                        print("No matches found for the string, '"+i+"' ")
                    else:
                        print("The following matches were found for the string, '"+i+"' :")
                        self.__fancyPrintList__(match_dict[i])
                        
            value = match_dict
            result = (success,value)                       
            return result           


        def cmd_vi(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup 

            if(len(file_list) > 1):
                if(self.debug):
                    print("Warning: Only one file can be grabbed at a time")         
                value = None 
                success = False

            file_name = file_list[0] 
            file_path_str = self.joinNode(self.varPath,file_name)            
                   
            if(file_name in self.varPath_Files):
                try: 
                    value = iop.flat_file_grab(file_path_str)
                except:
                    if(self.debug):
                        print("Error: Could not retrieve the contents of '"+file_name+"'")         
                    value = None
                    success = False
            elif(file_name not in self.varPath_Contains):
                try:
                    value = iop.flat_file_write(file_path_str)
                except:
                    if(self.debug):
                        print("Error: The file '"+file_name+"' could not be opened")
                    value = None
                    success = False
            else:
                if(self.debug):
                    print("Error: '"+file_name+"' not a file found in current (path) directory")         
                value = None 
                success = False

            result = updater(self.varPath_List,value)
            return result


        def cmd_help(tup):

            success = True
            value = None
            cmdInst, file_list, destStr = tup

            self.helpDict = self.documentation('help')

            if(destStr == ''):
                if(self.debug):
                    print(self.space+'Below is a list of valid input commands:\n')
                    self.__fancyPrintList__(self.cdList)
                    helpText = "Place command name after 'help' for more info on that command"

            else:
                cmd_val = destStr
                if(cmd_val in self.cdList):
                    self.helpDict = self.documentation('help')
                    helpText = self.helpDict[cmd_val]
                else:
                    success = False
                    helpText = "Error: the command '"+cmd_val+"' not recognized"

            if(self.debug):
                print(helpText)
                print('\n')

            value = helpText
            result = (success,value)
            return result


        ##################
        # Function: Main #
        ##################

        result = (False,None)

        # Dummy test
        if(not isinstance(cmd_string,str)):
            if(self.debug):
                print(self.space+"Warning: Input must be a properly formated string ")
                print(self.space+"Warning: No action taken, see help for more info on proper 'cmd' formatting\n")
            return result
        if(cmd_string == '' or cmd_string.isspace()):
            if(self.debug):
                print(self.space+"Warning: Input must be a properly formated string ")
                print(self.space+"Warning: No action taken, see help for more info on proper 'cmd' formatting\n")
            return result

        cmd_tuple = self.__cmdInputParse__(cmd_string)
        cmdInst = cmd_tuple[0]

        if(cmdInst == 'pwd'):               # print working directory 
            result = cmd_pwd(cmd_tuple)

        elif(cmdInst == 'ls'):              # list (content of working directory)
            result = cmd_ls(cmd_tuple)        

        elif(cmdInst == 'dir'):             # directory (pathway)
            result = cmd_dir(cmd_tuple)   

        elif(cmdInst == 'cd'):              # change directory 
            result = cmd_cd(cmd_tuple)

        elif(cmdInst == 'chdir'):           # change directory (with pathway)
            result = cmd_chdir(cmd_tuple)

        elif(cmdInst == 'mv'):              # move and rename (files and directories)
            result = cmd_mv(cmd_tuple)  
 
        elif(cmdInst == 'rm'):              # remove (files) 
            result = cmd_rm(cmd_tuple)      

        elif(cmdInst == 'cp'):              # copy (files)
            result = cmd_cp(cmd_tuple)

        elif(cmdInst == 'mkdir'):           # make directory 
            result = cmd_mkdir(cmd_tuple) 

        elif(cmdInst == 'rmdir'):           # remove directory
            result = cmd_rmdir(cmd_tuple)

        elif(cmdInst == 'cpdir'):           # copy directory 
            result = cmd_cpdir(cmd_tuple)          

        elif(cmdInst == 'find'):            # find (exact file)
            result  = cmd_find(cmd_tuple)

        elif(cmdInst == 'match'):           # match (file names) 
            result = cmd_match(cmd_tuple)

        elif(cmdInst == 'vi'):              # visual interface (read text files)
            result = cmd_vi(cmd_tuple)

        elif(cmdInst == 'help'):            # help (display)
            result = cmd_help(cmd_tuple)

        else:
            tup_str = str(cmd_tuple)
            if(self.debug or self.shellPrint):
                print(self.space+"[cmd] Error: Input '"+cmd_string+"' not resolved\n")
            if(self.shellPrint):
                print(self.space+"It appears that either 'cmd_string' was not recognized")
                print(self.space+"or that, the operand with which it was combined was not properly parsed")
                print(self.space+"Below is a summary of the output:")
                print(self.space+"\n")
                print(self.space+"'cmdInst' = '"+cmdInst+"'")
                print(self.space+"'cmd_tuple' = '"+tup_str+"'")
                print(self.space+'\n')

        return result