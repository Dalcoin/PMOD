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

    tcheck  : PathParse is a super class of 'imprimerTemplate'
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

from pmod.tcheck import imprimerTemplate
import pmod.ioparse as iop
import pmod.strlist as strl

class PathParse(imprimerTemplate):

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
                 space='    ',
                 endline='\n',
                 moduleNameOverride=None,
                 **kwargs
                ):

        '''
        --------
        | init |
        --------

        Inputs :

            osFormat    = 'windows' or 'linux'
            newPath     = None    (by default)
            debug       = True    (by default)
            colourPrint = True    (by default)
            space       = '    '  (by default)
            endline     = '\n'    (by default)

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

        # initilize imprimerTemplate class
        super(PathParse, self).__init__(space, endline, debug, **kwargs)

        # Set debug info for __init__
        if(isinstance(moduleNameOverride, str)):
            self.__set_funcNameHeader__(moduleNameOverride, **kwargs)
        else:
            self.__set_funcNameHeader__("PathParse", **kwargs)
        kwargs = self.__update_funcNameHeader__("init", **kwargs)

        # initilize class variables
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

        self.varPath          = None
        self.varPath_List     = None
        self.varPath_Head     = None
        self.varPath_Contains = None
        self.varPath_Files    = None
        self.varPath_Folders  = None

        self.helpDict = None

        if(self.varOS in ('windows', 'web', 'net', 'internet')):
            self.delim = '\\'
        elif(self.varOS in ('linux', 'unix'):
            self.delim = '/'
        elif(self.varOS == 'classic'):
            self.delim = ':'
        elif(self.varOS in ('tcl', 'tacl')):
            self.delim = '.'
        else:
            self.__err_print__(": "str(self.varOS)+", is not recognized", varID='varOS', **kwargs)
            self.SET_INIT_PATH = False

        if(isinstance(newPath, str)):
            self.varPath = newPath
            success = True
        else:
            try:
                self.varPath = os.getcwd()
                success = True
            except:
                self.__err_print__("failure to resolve current pathway", **kwargs)
                self.SET_INIT_PATH = False
                success = False

        if(success):
            updateTest = self.__updatePath__(self.varPath)
            if(updateTest == False):
                self.SET_INIT_PATH = False
            else:
                self.SET_INIT_PATH = True

        if(self.SET_INIT_PATH == False):
            self.__err_print__("initilization failed!")


    def documentation(self, string, **kwargs):
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
                print(self.helpDict[string])
            return self.helpDict
        else:
            return None


    def __cmdInputParse__(self, string, **kwargs):
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
        if(self.__not_str_print__(string, varID="string", **kwargs)):
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
                    errArray = ["The input spaceing or object style created ambiguity for the indexer:"]
                    errArray.append("The following is an echo of the input string which caused the issue: ")
                    errArray.append("'"+string+"'")
                    __err_print__(errArray, **kwargs)
                    outInst = (cmdInst, [], '')

                return outInst

        __err_print__("not recognized, use 'help' to view available functions", varID=str(cmdInst), **kwargs)
        return ('',[],'')


    def Arr2Str(self, inPath, **kwargs):

        kwargs = self.__update_funcNameHeader__("Arr2Str", **kwargs)

        if(not isinstance(inPath, (list, tuple))):
            return self.__err_print__("must be a python array", varID='inPath', **kwargs)
        else:
            inPath = filter(None, inPath)
            if(len(inPath) < 1):
                return self.__err_print__("must contain at least one pathway entry", varID='inPath', **kwargs)

        for i,dir in enumerate(inPath):
            if(i == 0):
                outPath = str(dir)
                if(self.varOS == 'linux'):
                    outPath = '/'+outPath
            else:
                outPath = self.joinNode(outPath, str(dir), **kwargs)
                if(outPath == False):
                    errmsg = ": could not join the"+strl.print_ordinal(i+1)+" entry"
                    return self.__err_print__(errmsg, varID='inPath', **kwargs)

        if(self.varOS == 'windows' and len(inPath)==1):
            outPath = outPath+"\\"

        return outPath


    def Str2Arr(self, inPath, **kwargs):

        kwargs = self.__update_funcNameHeader__("Str2Arr", **kwargs)

        if(self.__not_str_print__(inPath, varID='inPath', **kwargs)):
            return False
        else:
            try:
                return outPath = filter(None, inPath.split(self.delim))
            except:
                return self.__err_print__("could not be converted to a list", varID='inPath', **kwargs)


    def convertPath(self, inPath, outType='str', **kwargs):
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

        kwargs = self.__update_funcNameHeader__("convertPath", **kwargs)

        if(__not_str_print__(outType, varID='outType', **kwargs)):
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
                return self.Arr2Str(inPath, **kwargs)
            else:
                return self.__err_print__("not recognized", varID='outType', **kwargs)
        elif(isinstance(inPath, str)):
            if(outType in self.typeStr):
                return inPath
            elif(outType in self.typeList):
                if(outType == 'arr' or outType == 'array' or outType == 'list'):
                    return self.Str2Arr(inPath, **kwargs)
                else:
                    return tuple(self.Str2Arr(inPath, **kwargs))
            else:
                return self.__err_print__("not recognized", varID='outType', **kwargs)
        else:
            return self.__err_print__("not of a recognized type, should be a 'Str' or an 'Array'", varID='inPath', **kwargs)
        return self.errPrint("path conversion failed", **kwargs)


    def uniqueName(self, destPath, objName, uniqueNameLimit=500, **kwargs):
        '''
        Description: 

        Inputs: 

            destPath : [string], [array],
                       A pathway formatted string or array which points to a directory

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

        kwargs = self.__update_funcNameHeader__("uniqueName", **kwargs)

        contents = self.contentPath(destPath, **kwargs)
        if(contents == False):
            return self.__err_print__("must be a valid directory pathway", varID='destPath', **kwargs)

        nameList = strl.str_to_list(objName, spc='.')
        if(nameList == False):
            return self.__err_print__("was not properly parsed", varID='objName', **kwargs)

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
                        return self.__err_print__("name ID overflow; too many files with the same name ID", **kwargs)                   
                    outName = name+"_"+str(count)
                    count += 1
                return outName
            else:
                return self.__err_print__("is empty; should be string corrosponding to new object name", varID='objName', **kwargs)
        else:
            return self.__err_print__("is empty; should be string corrosponding to the new object name", varID='objName', **kwargs)

        # If there is a file ending attached to 'objName', the unique name is generated
        count = 1
        name = objName
        pad = nameList[-2]
        while(name in contents):
            if(count > uniqueNameLimit):
                return self.__err_print__("name ID overflow; too many files with the same name ID", **kwargs)
            nameList[-2] = pad+"_"+str(count)
            name = strl.array_to_str(nameList, spc='.')
            count+=1
        return name


    def joinNode(self, oldPath, newNode, **kwargs):
        '''
        Description: Adds a new node onto a string Pathway

        Input :

            oldPath : [string], pathway formatted string
            newPath : [string], node

        Output : [string], pathway formatted string
        '''

        kwargs = self.__update_funcNameHeader__("joinNode", **kwargs)
        if(self.__not_str_print__(oldPath, varID='oldPath', **kwargs)):
            return False
        if(self.__not_str_print__(newNode, varID='newNode', **kwargs)):
            return False

        newPath = oldPath+self.delim+newNode
        return newPath


    def delNode(self, oldPath, nodeID=None, **kwargs):
        '''
        Description: deletes node onto a pathway, starting at the end

        Input :

            oldPath : [string], pathway formatted string
            nodeID  : [None or Int], nodes to be deleted from end

        Output : [string], pathway formatted string
        '''

        kwargs = self.__update_funcNameHeader__("delNode", **kwargs)

        oldPath = self.convertPath(oldPath, outType="list", **kwargs)
        if(oldPath == False):
            return False

        n = len(oldPath)

        if(n < 1):
            return self.__err_print__("does not contain a valid pathway", varID='oldPath', **kwargs)
        elif(n == 1):
            self.__err_print__("home directory reached, cannot delete home node", heading='warning', **kwargs)
            return self.convertPath(oldPath, **kwargs)
        else:
            pass

        if(nodeID == -1 or nodeID == None):
            newPath = oldPath[:-1]
            strPath = self.Arr2Str(newPath, **kwargs)
            return strPath
        elif(isinstance(nodeID, int)):
            try:
                if(nodeID != 0):
                    newPath = oldPath[:nodeID]
                else:
                    newPath = oldPath
                strPath = self.Arr2Str(newPath)
            except:
                strPath = self.__err_print__("is out of range", varID='nodeID', **kwargs)
            return strPath
        else:
            return self.__err_print__("is not recognized", varID='nodeID', **kwargs)
        return False


    def getNode(self, inPath, nodeID=None, **kwargs):

        kwargs = self.__update_funcNameHeader__("getNode", **kwargs)

        pathList = self.convertPath(inPath, outType='list')
        if(pathList == False):
            return False

        if(nodeID == None or nodeID == -1):
            if(len(pathList) > 0):
                return pathList[-1]
            else:
                return self.__err_print__("does not contain a valid pathway", varID='inPath', **kwargs)
        elif(isinstance(nodeID, int)):
            try:
                nodeValue = pathList[nodeID]
                return nodeValue
            except:
                return self.__err_print__("is out of range", varID='nodeID', **kwargs)
        else:
            return self.__err_print__("is not recognized: '"+str(nodeID)+"'", varID='nodeID', **kwargs)
        return False


    def contentPath(self, inPath, objType='all', fileStyle=None, **kwargs):
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

            'output': [list], A list of strings corrosponding to all the files
                              in the current (path) directory matching the
                              'fileStyle' extension, if 'fileStyle' == None, then all
                              file names are included in 'file_list'.
        '''

        kwargs = self.__update_funcNameHeader__("contentPath", **kwargs)

        if(isinstance(inPath, str)):
            path = inPath
        elif(isinstance(inPath, (list,tuple))):
            path = self.Arr2Str(inPath, **kwargs)
            if(path == False):
                return False
        else:
            return self.__err_print__("must be either an 'Array' or 'Str' type", varID='inpath', **kwargs)

        if(os.path.isdir(path) == False):
            errmsg = ["does not corrospond to a directory", "Pathway : "+str(path)]
            return self.__err_print__(errmsg, varID = 'inPath', **kwargs)

        if(self.__not_str_print__(objType, varID='objType', heading='Warning', **kwargs)):
            self.__err_print__("will be defaulted to a value of : 'all'", varID='objType', **kwargs)
            objType = 'all'
        else:
            objType = objType.lower()

        try:
            pathContents = os.listdir(path)
        except:
            return self.__err_print__(["content is irretrievable","pathway: "+path])

        if(objType.lower() == 'all'):
            output = pathContents
        elif(objType.lower() in self.fileNames):
            if(fileStyle == None or not isinstance(fileStyle,(str,tuple,list))):
                output = [entry for entry in pathContents if os.path.isfile(self.joinNode(path, entry, **kwargs))]
            else:
                file_List = []
                if(isinstance(fileStyle, str)):
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
            output = [entry for entry in pathContents if os.path.isdir(self.joinNode(path, entry, **kwargs))]
        else:
            output = False

        return output


    def __updatePath__(self, newPath, **kwargs):
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
        kwargs = self.__update_funcNameHeader__("__updatePath__", **kwargs)

        if(isinstance(newPath, str)):
            if(newPath == ''):
                return self.__err_print__("is an empty string and not a pathway", varID='newPath', **kwargs)
            __oldval__ = self.varPath_List
            self.varPath_List = self.Str2Arr(newPath, **kwargs)
            if(self.varPath_List == False):
                self.varPath_List = __oldval__
                return self.__err_print__("failed to convert to a list", varID='newPath', **kwargs)
            self.varPath = newPath
        elif(isinstance(newPath,(list,tuple))):
            if(len(newPath) < 1):
                return self.__err_print__("is an empty array", varID='newPath', **kwargs)
            __oldval__ = self.varPath
            self.varPath = self.Arr2Str(newPath)
            if(self.varPath == False):
                self.varPath = __oldval__
                return self.__err_print__("failed to convert to a string", varID='newPath', **kwargs)
            self.varPath_List = list(newPath)
        else:
            return self.__err_print__("not a recognized type", varID='newPath', **kwargs)

        self.varPath_Head = self.varPath_List[0]
        if(self.varOS == 'windows'):
            self.varPath_Head = self.varPath_Head+"\\"
        self.varPath_Dir  = self.varPath_List[-1]

        self.varPath_Contains = self.contentPath(self.varPath, 'all', **kwargs)
        if(self.varPath_Contains == False):
            self.varPath_Contains = None
            self.varPath_Files = None
            self.varPath_Folders = None
            return self.__err_print__("failure to get contents from current pathway", **kwargs)

        self.varPath_Files = self.contentPath(self.varPath, 'files', **kwargs)
        if(self.varPath_Files == False):
            self.varPath_Files = None
            self.varPath_Folders = None
            return self.__err_print__("failure to get files from current pathway")

        self.varPath_Folders = self.contentPath(self.varPath, 'folders', **kwargs)
        if(self.varPath_Folders == False):
            self.varPath_Folders = None
            return self.__err_print__("failure to get directories from current pathway", **kwargs)

        return True


    def climbPath(self, oldpath, node, **kwargs):
        '''
        Description : if 'node' is a node in the default (current) pathway
                      that the default (current) pathway directory is moved
                      up to that node, else False is returned

        Input:

            'node' : [string], corrosponding to a node within the current pathway

        The overhead and updating of class path info is taken care of with this function
        '''

        kwargs = self.__update_funcNameHeader__("climbPath", **kwargs)

        if(isinstance(oldpath, str)):
            path = self.convertPath(oldpath, outType='list', **kwargs)
            if(path == False):
                return self.__err_print__(["failed to convert to a list", "pathway : '"+oldpath+"'"], varID='oldpath', **kwargs)
        elif(isinstance(oldpath, (list, tuple))):
            path = list(oldpath)
        else:
            return self.__err_print__("must be a path string or path array", varID='oldPath', **kwargs)

        newPath_List = []
        if(node in path):
            for entry in path:
                if(entry != node):
                    newPath_List.append(entry)
                else:
                    break
            newPath_List.append(node)
            return newPath_List
        else:
            return self.__err_print__(["not found in 'path' hierarchy '", "pathway : "+str(node)], varID='node', **kwargs)


    def __climbPath__(self, node, **kwargs):
        '''
        Description : if 'node' is a node in the default (current) pathway
                      that the default (current) pathway directory is moved to

        Input:

            'node' : [string], corrosponding to a node within the current pathway

        The overhead and updating of class path info is taken care of with this function
        '''

        newPath_List = self.climbPath(self.varPath_List, node, **kwargs)
        if(newPath_List == False):
            return False

        output = self.__updatePath__(newPath_List, **kwargs)
        return output


    def renamePath(self, originPath, destPath, objName=None, climbPath_Opt=True, **kwargs):
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
            climbPath_Opt  : [bool] (False), If true then if 'destPath' does have a directory as the final node,
                                         the node will be climbed unitil a directory is found or the home
                                         directory is reached

        Output : [Bool], success
        '''

        def __create_path__(novPath, novName, **kwargs):

            dNode = self.uniqueName(novPath, novName, **kwargs)
            if(dNode == False):
                return self.__err_print__("Failure to generate a unique name from input path", **kwargs)
            return self.joinNode(novPath, dNode, **kwargs)

        kwargs = self.__update_funcNameHeader__("renamePath", **kwargs)

        destNode = self.getNode(originPath, **kwargs)
        originPath = self.convertPath(originPath, **kwargs)
        destPath = self.convertPath(destPath, **kwargs)

        if(destNode == False):
            return self.__err_print__("failed to yield terminating node", varID='originPath', **kwargs)

        # If the objName variable is changed to a string
        if(isinstance(objName,str)):
            if(os.path.isdir(destPath)):
                pass
            else:
                errmsg = ["does not point to a directory"]
                errmsg.append("If 'objName' is set, then the 'destPath' pathway must point to a directory")
                errmsg.append("'destPath' : "+str(destPath))
                return self.__err_print__(errmsg, varID='destPath', **kwargs)
            newPath = __create_path__(destPath, objName, **kwargs)
            if(newPath == False):
                self.__err_print__("new pathway could not be established", **kwargs)
            return newPath

        # Default method: will attempt to establish a unique pathway
        else:
            if(os.path.isdir(destPath)):
                newPath = __create_path__(destPath, destNode, **kwargs)
                if(newPath == False):
                    self.__err_print__("new pathway could not be established", **kwargs)
                return newPath

            # climbPath_Opt ----option----
            if(climbPath_Opt):
                parentPath = self.delNode(destPath, **kwargs)
                while(self.convertPath(parentPath, **kwargs) != self.varPath_Head):
                    if(parentPath == False):
                        return self.__err_print__("pathway could not be climbed", varID='destPath', **kwargs)
                    if(os.path.isdir(parentPath)):
                        destNode = self.uniqueName(parentPath, destNode, **kwargs)
                        newPath = self.joinNode(parentPath, destNode, **kwargs)
                        if(newPath == False):
                            return self.__err_print__("could not accept directory name node", varID='destPath', **kwargs)
                        return newPath
                    else:
                        return self.__err_print__(["is not a valid destination pathway", "'destPath': "+str(destPath)], varID='destPath', **kwargs)
                    parentPath = self.delNode(parentPath)
                self.__err_print__("couldn't find valid destination before reaching the 'home' directory", **kwargs)
            self.__err_print__("is not a valid pathway destination", varID='destPath', **kwargs)
        return False


    ###########################################################
    # Move File and Directories from one Directory to another #
    ###########################################################

    def moveObj(self, objPath, destPath, objName=None, renameOverride=None, **kwargs):
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

        kwargs = self.__update_funcNameHeader__("moveObj", **kwargs)

        #Parse object pathway into the string format
        if(isinstance(objPath, (list,tuple))):
            objPath = self.convertPath(objPath, **kwargs)
            if(objPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID='objPath', **kwargs)
        elif(isinstance(objPath, str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='objPath', **kwargs)

        #Parse destination pathway into the string format
        if(isinstance(destPath, (list,tuple))):
            destPath = self.convertPath(destPath, **kwargs)
            if(destPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID='destPath', **kwargs)
        elif(isinstance(destPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='destPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(objPath, destPath, objName=objName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(objName,str)):
                destPath = self.joinNode(destPath, objName, **kwargs)
            else:
                destPath = destPath

        #Move contents of 'objPath' to the 'destPath' destination
        try:
            shutil.move(objPath, destPath)
            success = True
        except:
            errmsg = ["object could not be moved:", "File pathway: "+str(objPath), "Destination pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, **kwargs)

        return success


    def __moveObj__(self, objPath, newPath, objName=None, renameOverride=None, **kwargs):

        success = self.moveObj(objPath, newPath, objName=objName, renameOverride=renameOverride, **kwargs)
        if(not success):
            return self.errPrint("failure to perform move operation", **kwargs)

        try:
            startDir = self.convertPath(objPath, "list", **kwargs)[-2]
        except:
            return self.__err_print__("failure to parse object folder from 'objPath'", **kwargs)

        try:
            finalDir = self.convertPath(newPath,"list")[-1]
        except:
            return self.__err_print__("failure to find folder for the new pathway", **kwargs)

        if(startDir == self.varPath_Dir or finalDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                self.__err_print__("failure to update pathway", **kwargs)
        else:
            success = False
        return success


    ############################
    # Delete File from Pathway #
    ############################

    def delFile(self, delPath, **kwargs):
        '''
        Description : Attempts to delete the content at the location of the input pathway

        Input:

            delPath : A complete pathway string pointing to a file

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("delFile", **kwargs)

        if(isinstance(delPath, (list,tuple))):
            delPath = self.convertPath(delPath, **kwargs)
            if(delPath == False):
                return self.__err_print__("could not be converted to a pathway string", varID= 'delPath', **kwargs)
        elif(isinstance(delPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='delPath', **kwargs)

        if(os.path.isfile(delPath)):
            pass
        else:
            errmsg = ["is not a file pathway", "Pathway: "+str(delPath)]
            return self.__err_print__(errmsg, varID='delPath', **kwargs)

        try:
            os.remove(delPath)
        except:
            errmsg = ["Failure to delete file", "File pathway: "+str(delPath)]
            return self.__err_print__(errmsg, **kwargs)
        return True


    def __delFile__(self, delPath, **kwargs):

        success = self.delFile(delPath, **kwargs)
        if(not success):
            return self.errPrint(["failure to perform file delete operation"], **kwargs)

        try:
            startDir = self.convertPath(delPath, "list", **kwargs)[-2]
        except:
            return self.__err_print__("failure to find the folder containing the object in 'delPath' pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return False

    #############################################
    # Copy object from one directory to another #
    #############################################

    def copyFile(self, filePath, destPath, objName=None, renameOverride=None, **kwargs):
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

        kwargs = self.__update_funcNameHeader__("copyFile", **kwargs)

        if(isinstance(filePath,(list,tuple))):
            filePath = self.convertPath(filePath, **kwargs)
            if(filePath == False):
                return self.errPrint("could not be converted to a pathway string", varID= 'filePath', **kwargs)
        elif(isinstance(filePath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='filePath', **kwargs)

        if(isinstance(destPath,(list,tuple))):
            destPath = self.convertPath(destPath, **kwargs)
            if(destPath == False):
                return self.errPrint("could not be converted to a pathway string", varID= 'destPath', **kwargs)
        elif(isinstance(destPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='destPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(filePath, destPath, objName=objName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(objName, str)):
                destPath = self.joinNode(destPath, objName, **kwargs)
            else:
                destPath = destPath

        try:
            shutil.copyfile(filePath, destPath)
            success = True
        except:
            errmsg = ["file could not be copied", "File pathway: "+str(filePath), "Destination pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, **kwargs)
        return success


    def __copyFile__(self, objPath, newPath, objName=None, renameOverride=None, **kwargs):

        success = self.copyFile(objPath, newPath, objName, renameOverride, **kwargs)
        if(not success):
            return self.__err_print__("failure to perform copy operation", **kwargs)

        try:
            if(isinstance(objName, str)):
                startDir = self.convertPath(objPath, "list")[-1]
            else:
                startDir = self.convertPath(objPath, "list")[-2]
        except:
            return self.__err_print__("failure to find folder for object pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return False


    ######################
    # Make new directory #
    ######################
 
    def makeDir(self, dirPath, dirName=None, renameOverride=None, **kwargs):
        '''
        Description : Attempts to create a folder at the full pathway string, 'dirPath'.
                      If 'dirName' is a a string, then this string will be appended onto
                      the pathway and used as the new folder name

        Input :

            dirPath : [string] corrosponds to full pathway of the location of the file to be copied
            fileName  : [string] (Default : None), corrosponds to full pathway of the location of the copy

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("makeDir", **kwargs)

        if(isinstance(dirPath,(list,tuple))):
            dirPath = self.convertPath(dirPath, **kwargs)
            if(dirPath == False):
                return self.errPrint("could not be converted to a pathway string", varID= 'dirPath', **kwargs)
        elif(isinstance(dirPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='dirPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(filePath, destPath, objName=dirName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(dirName, str)):
                destPath = self.joinNode(destPath, dirName, **kwargs)
            else:
                destPath = destPath

        try:
            os.mkdir(destPath)
            success = True
        except:
            errmsg = ["directory could not be created", "Directory pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, **kwargs)
        return success


    def __makeDir__(self, dirPath, dirName=None, renameOverride=None, **kwargs):

        success = self.makeDir(self, dirPath, dirName, renameOverride, **kwargs)
        if(not success):
            return self.__err_print__("failure to perform move operation")

        try:
            if(isinstance(dirName,str)):
                newDir = dirName
            else:
                newDir = self.convertPath(dirPath,"list")[-2]
        except:
            return self.__err_print__("failure to find new pathway directory")

        if(newDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return True


    ##############################
    # Delete directory from path #
    ##############################

    def delDir(self, delPath, **kwargs):
        '''
        Description : Recursively removes content and directory at pathway 'delPath'

        Input : 

            delPath : [string], corrosponds to path containing directory to be deleted

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("delDir", **kwargs)

        if(isinstance(delPath, (list,tuple))):
            delPath = self.convertPath(delPath, **kwargs)
            if(delPath == False):
                return self.errPrint("could not be converted to a pathway string", varID= 'delPath', **kwargs)
        elif(isinstance(delPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='delPath', **kwargs)

        if(os.path.isdir(delPath)):
            pass
        else:
            errmsg = ["is not a directory pathway", "pathway: "+str(delPath)]
            return self.__err_print__(errmsg, varID='delPath', **kwargs)

        try:
            shutil.rmtree(delPath)
            success = True
        except:
            errmsg = ["directory could not be deleted", "pathway: "+str(delPath)]
            success = self.__err_print__(errmsg, varID='delPath', **kwargs)
        return success


    def __delDir__(self, delPath, **kwargs):

        success = self.delFile(delPath, **kwargs)
        if(not success):
            if(self.debug):
                print(self.space+"[__delDir__] Error: failure to perform move operation")
            return success

        try:
            startDir = self.convertPath(delPath,"list")[-2]
        except:
            return self.__err_print__("failure to find folder for object pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return True


    ##########################################
    # Copy directory from path to a new path #
    ##########################################

    def copyDir(self, dirPath, destPath, dirName=None, renameOverride=None, **kwargs):
        '''
        Description : Attempts to copy contents from 'dirPath' full pathway
                      to the full directory pathway 'destPath', optional, the
                      string found in 'dirName' will be the name of the new
                      directory, else the new directory will have the same
                      name as the old one.

        Input :

            dirPath : [string] corrosponds to full pathway of the location of the file to be copied
            destPath  : [string], corrosponds to the pathway of the newly created copy directory
            dirName  : [string] (Default : None), corrosponds to full pathway of the location of the copy

        Output : [Bool], success
        '''

        kwargs = self.__update_funcNameHeader__("copyDir", **kwargs)

        if(isinstance(dirPath, (list,tuple))):
            dirPath = self.convertPath(dirPath, **kwargs)
            if(dirPath == False):
                return self.errPrint("could not be converted to a pathway string", varID= 'dirPath', **kwargs)
        elif(isinstance(dirPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='dirPath', **kwargs)

        if(isinstance(destPath, (list,tuple))):
            destPath = self.convertPath(destPath, **kwargs)
            if(destPath == False):
                return self.errPrint("could not be converted to a pathway string", varID= 'destPath', **kwargs)
        elif(isinstance(destPath,str)):
            pass
        else:
            return self.__err_print__("must be either a pathway formatted string or array", varID='destPath', **kwargs)

        #If 'renameOption', perform 'renamePath' operation
        if(renameOverride != None):
            if(renameOverride):
                renameOption = True
            else:
                renameOption = False
        else:
            renameOption = self.rename

        if(renameOption):
            destPath = self.renamePath(dirPath, destPath, objName=dirName, **kwargs)
            if(destPath == False):
                return self.__err_print__("failure to generate renamed object at destination pathway", **kwargs)
        else:
            if(isinstance(dirName, str)):
                destPath = self.joinNode(destPath, dirName, **kwargs)
            else:
                destPath = destPath

        try:
            shutil.copytree(dirPath, destPath)
            success = True
        except:
            errmsg = ["directory could not be copied", "Directory pathway: "+str(dirPath), "Destination pathway: "+str(destPath)]
            success = self.__err_print__(errmsg, varID='dirPath', **kwargs)
        return success


    def __copyDir__(self, dirPath, destPath, dirName=None, renameOverride=None, **kwargs):

        success = self.copyDir(dirPath, destPath, dirName, renameOverride)
        if(not success):
            return self.__err_print__("failure to perform move operation", **kwargs)

        try:
            if(isinstance(dirName, str)):
                startDir = self.convertPath(destPath, "list")[-1]
            else:
                startDir = self.convertPath(destPath, "list")[-2]
        except:
            return self.__err_print__("failure to find folder for object pathway", **kwargs)

        if(startDir == self.varPath_Dir):
            success = self.__updatePath__(self.varPath, **kwargs)
            if(not success):
                return self.__err_print__("failure to update pathway", **kwargs)
            else:
                return success
        else:
            return True


    #############################
    # find object(s) in pathway #
    #############################

    def find(self, objName, dirPath, objType='all', **kwargs):
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

        kwargs = self.__update_funcNameHeader__("find", **kwargs)

        contents = self.contentPath(dirPath, objType, **kwargs)
        if(contents == False):
            return self.__err_print__("pathway contents could not be resolved", varID='dirPath', **kwargs)

        if(isinstance(objName, str)):
            if(objName in contents):
                within = True
            else:
                within = False
            return {objName:within}
        elif(isinstance(objName, (list, tuple))):
            outDict = {}
            for obj in objName:
                if(obj in contents):
                    within = True
                else:
                    within = False
                outDict[obj] = within
            return outDict
        else:
            return self.__err_print__("must be either a string or an array", varID='objName', **kwargs)
        return False


    def __find__(self, objName, objType='all', **kwargs):

        outDict = self.find(objName, self.varPath, objType)
        if(outDict == False):
            return self.__err_print__("failure to complete 'find' operation")
        else:
            return outDict


    #################################################
    # find object(s) containing fragment in pathway #
    #################################################

    def match(self, fragment, dirPath, objType='all', **kwargs):
        '''
        Description : Searches an input directory for any object containing a specific string 

        Input :

            fragment : [string or list of strings], string fragment to be matched
            dirPath : [string], pathway of directory for which 'fragment' is to be searched
            objType : [string] (Default : 'all'), type of object to be searched for

        Output : [Bool], success
        '''

        contents = self.contentPath(dirPath, objType, **kwargs)
        if(contents == False):
            return self.__err_print__("pathway contents could not be resolved", varID='dirPath', **kwargs)

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
                    if(frag in entry):
                        capList.append(entry)
                outDict[frag] = capList
            return outDict
        else:
            return self.__err_print__("must be either a string or an array", varID='fragment', **kwargs)
        return False

    def __match__(self, fragment, objType='all', **kwargs):

        outDict = self.match(fragment, self.varPath, objType, **kwargs)
        if(outDict == False):
            return self.__err_print__("failure to complete 'match' operation", **kwargs)
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

        def files_present(fileList, cmdInst=None, funcName=None):
            outfiles = []

            if(fileList == []):
                return []

            for file in fileList:
                if(file not in self.varPath_Files and cmdInst not in self.singlePathListGroup and cmdInst not in self.singlePathListNoGroup):
                    if(isinstance(funcName,str)):
                        self.errPrint("["+funcName+"]"+"[files_present] Error: '"+str(file)+"' not found in current directory", funcAdd='cmd')
                    else:
                        self.errPrint("[files_present] Error: '"+str(file)+"' not found in current directory", funcAdd='cmd')
                else:
                    outfiles.append(file)
            if(len(outfiles) == 0):
                if(isinstance(funcName,str)):
                    self.errPrint("["+funcName+"]"+"[files_present] Warning: none of the files were found in the current directory", funcAdd='cmd')
                else:
                    self.errPrint("[files_present] Warning: The file(s) was not found in the current directory", funcAdd='cmd')
            return outfiles

        def cmd_pwd(tup):
            success = True
            cmdInst, file_list, destStr = tup # allows for expanding functionality

            try:
                value = self.varPath 
                if(value == False):
                    self.errPrint("[cmd_pwd] Error: 'varPath' not set...", funcAdd='cmd')
            except:
                self.errPrint("[cmd_pwd] Error: 'varPath' not set...", funcAdd='cmd')

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

            result = (success,value)
            return result


        def cmd_dir(tup):
            success = True
            cmdInst, file_list, destStr = tup

            self.__updatePath__(self.varPath)
            new_file_list = []

            values = self.__find__(file_list)
            if(values == False):
                self.errPrint("[cmd_dir] Error: occured when attempting to find input files in the current directory", funcAdd = 'cmd')
                return (False,None)

            for entry in file_list:
                if(values[entry]):
                    new_file_list.append(self.joinNode(self.varPath,entry))
                else:
                    self.errPrint("[cmd_dir] Warning: file name, '"+str(entry)+"' not found in current directory", funcAdd = 'cmd')
            value = new_file_list

            ptest_1 = self.__runFancyPrint__()
            if(self.shellPrint):
                print(self.space+"Pathway string(s): \n")
                ptest_2 = self.__fancyPrintList__(new_file_list)
            else:
                ptest_2 = True

            if(not ptest_1 or not ptest_2):
                success = False
                self.errPrint("[cmd_dir] Error: An unknown error was raised during printing", funcAdd = 'cmd')

            result = (success,value)
            return result


        def cmd_cd(tup):
            success = True
            value = None
            cmdInst, file_list, destStr = tup
            self.__updatePath__(self.varPath)

            if(destStr == '..'):
                if(headCheck()):
                    result = (success,value)
                    return result
                else:
                    up_path_list = list(self.varPath_List)[:-1]
                result = updater(up_path_list,value)

            elif(destStr in self.varPath_Contains):
                dest_loc = self.joinNode(self.varPath, destStr)
                if(os.path.isdir(dest_loc)):
                    newPath_list = list(self.varPath_List)
                    newPath_list.append(destStr)
                else:
                    self.errPrint("[cmd_cd] Error: '"+str(dest_loc)+"' is not a valid folder in current directory", funcAdd = 'cmd')
                    result = (False, value)
                    return result
                result = updater(newPath_list,value)

            elif(destStr[0] == '/' or destStr[0] == '\\'):
                destStr = destStr[1:]
                ctest = self.__climbPath__(destStr)
                if(ctest == False):
                    self.errPrint("[cmd_cd] Error: failure to climb pathway", funcAdd='cmd')
                result = (ctest, value)

            elif(destStr == '~'):
                result = updater(self.varPath_Head, value)

            else:
                self.errPrint("Error: '"+str(destStr)+"' not a valid destination", funcAdd = 'cmd')
                result = (False, value)

            return result


        def cmd_chdir(tup):
            cmdInst, file_list, destStr = tup

            utest = self.__updatePath__(destStr)
            if(utest == False):
                self.errPrint("[cmd_chdir] Error: failure to change path directory", funcAdd='cmd')
            result = (utest,None)
            return result


        def cmd_mv(tup):

            def __move_object_2_path__(dest_path_list, move_file_list, rename=False):
                success = True

                dest_path_str = self.convertPath(dest_path_list)
                newname = dest_path_list[-1]

                if(rename):
                    path_has = self.contentPath(self.varPath)
                else:
                    path_has = self.contentPath(dest_path_str)

                if(newname in path_has and self.rename == False):
                    self.errPrint("[cmd_mv] Error: '"+str(newname)+"' already exists in target directory", funcAdd = 'cmd')
                    return False

                for entry in move_file_list:
                    init_path = self.joinNode(self.varPath, entry)
                    if(rename):
                        mtest = self.__moveObj__(init_path, self.varPath, objName=newname)
                    else:
                        mtest = self.__moveObj__(init_path, dest_path_str)
                    if(not mtest):
                        success = False
                        self.errPrint("[cmd_mv] Error: contents of this path: '"+str(init_path)+"' could not be moved", funcAdd = 'cmd')
                return success

            success = True
            value = None
            rename = False

            dpath_list = []

            cmdInst, file_list, destStr = tup
            self.__updatePath__(self.varPath)

            # parsing destination in list format
            if(destStr == '..'):
                if(headCheck()):
                    self.errPrint("[cmd_mv] Warning: 'home' directory reached, no action taken", funcAdd='cmd')
                    return (success, value)
                else:
                    dpath_list = list(self.varPath_List)
                    dpath_list = dpath_list[:-1]

            elif(destStr == '~'):
                dpath_list = [self.varPath_Head]

            elif(destStr[0] == '/' or destStr[0] == '\\'):
                destStr = destStr[1:]
                dpath_list = self.climbPath(self.varPath, destStr)
                if(dpath_list == False):
                    errPrint("[cmd_mv] Error: failure while climbing path to find folder, '"+str(destStr)+"'", funcAdd='cmd')
                    return (climb_check, value)

            elif(destStr in self.varPath_Folders):
                dpath_list = list(self.varPath_List)
                dpath_list.append(destStr)

            elif(len(file_list) == 1 and destStr not in self.varPath_Folders):
                dpath_list = list(self.varPath_List)
                dpath_list.append(destStr)
                rename = True

            else:
                errPrint("[cmd_mv] Error: Invalid formatting; the input object(s) could not be moved", funcAdd='cmd')
                result = (success, value)
                return result

            # Move file(s) to destination
            if(len(dpath_list) == 0):
                self.errPrint("[cmd_mv] Error: destination pathway list could not be parsed", funcAdd='cmd')
                return False
            __move_object_2_path__(dpath_list, file_list, rename=rename)

            # Update 
            result = updater(self.varPath_List, value)
            return result


        def cmd_rm(tup):
                      
            success = True            
            value = None
            cmdInst, file_list, destStr = tup
            self.__updatePath__(self.varPath)
            
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
            self.__updatePath__(self.varPath)

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
                node_inst = destStr[1:]
                path_str = self.__climbPath__(node_inst)
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(node_inst)+"' could not be found in the root pathway")
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
            self.__updatePath__(self.varPath)
            
            for i in file_list:
                file_path_str = self.joinNode(self.varPath,i)
                ctest = self.makeDir(file_path_str)  
                if(not ctest):
                    success = False 
                    print(self.space+"Error: contents of this path: '"+str(i)+"' could not be moved\n")
                                     
            result = updater(self.varPath_List, value)
            return result  

        
        def cmd_rmdir(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup
            self.__updatePath__(self.varPath)
            
            for i in file_list: 
                if(i in self.varPath_Contains):
                    file_path_str = self.joinNode(self.varPath,i)
                    output = self.delDir(file_path_str)
                    if(output == False):
                        success = False
                        self.errPrint("[cmd_rmdir] Error: folder, '"+str(i)+"', could not be deleted", funcAdd='cmd')

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
            self.__updatePath__(self.varPath)
          
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
                node_inst = destStr[1:]
                path_str = self.__climbPath__(node_inst)
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(node_inst)+"' could not be found in the root pathway")
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
            self.__updatePath__(self.varPath)

            found_dict = self.__find__(file_list)
            if(found_dict == False):
                self.errPrint("[cmd_find] Error: failure to parse 'find' values", funcAdd='cmd')
                return (False, None)

            if(self.debug):
                if(all(i == True for i in found_dict)):
                    print(self.space+"All searched objects have been found in the current directory!\n")
                else:
                    for found in found_dict:
                        if(found_dict[found] == False):
                            print(self.space+"No object named '"+str(found)+"' found in current directory.")

            result = (success, found_dict)
            return result


        def cmd_match(tup):

            success = True
            value = None
            cmdInst, file_list, destStr = tup
            self.__updatePath__(self.varPath)

            match_dict = self.__match__(file_list)
            if(match_dict == False):
                self.errPrint("[cmd_match] Error: failure to parse 'match' values", funcAdd='cmd')
                return (False, None)

            if(self.debug):
                if(len(match_dict) == 0):
                    print(self.space+"No matches found for the string, '"+str(frag)+"' \n")
                else:
                    for frag in match_dict:
                        print(self.space+"The following matches were found for the string, '"+str(frag)+"' :")
                        self.__fancyPrintList__(match_dict[frag])

            result = (success, match_dict)
            return result


        def cmd_vi(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup
            self.__updatePath__(self.varPath)

            if(len(file_list) > 1):
                if(self.debug):
                    self.errPrint("Warning: Only one file can be grabbed at a time", funcAdd='cmd')         
                value = None 
                success = False

            file_name = file_list[0] 
            file_path_str = self.joinNode(self.varPath,file_name)            
                   
            if(file_name in self.varPath_Files):
                try: 
                    value = iop.flat_file_grab(file_path_str)
                except:
                    if(self.debug):
                        errPrint("[cmd_vi] Error: Could not retrieve the contents of '"+file_name+"'", funcAdd='cmd')         
                    value = None
                    success = False
            elif(file_name not in self.varPath_Contains):
                try:
                    value = iop.flat_file_write(file_path_str)
                except:
                    if(self.debug):
                        errPrint("[cmd_vi] Error: The file '"+file_name+"' could not be opened", funcAdd='cmd')
                    value = None
                    success = False
            else:
                if(self.debug):
                    errPrint("[cmd_vi] Error: '"+file_name+"' not a file found in current (path) directory", funcAdd='cmd')         
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
        print("")

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

        cmdInst, fileList, destStr = cmd_tuple
        fileList = files_present(fileList, cmdInst=cmdInst)
        cmd_tuple = (cmdInst, fileList, destStr)

        if(cmdInst == 'pwd'):               # print working directory 
            result = cmd_pwd(cmd_tuple)

        elif(cmdInst == 'ls'):              # list (content of working directory)
            result = cmd_ls(cmd_tuple)        

        elif(cmdInst == 'dir'):             # return directory (pathway) of object in cwd
            result = cmd_dir(cmd_tuple)   

        elif(cmdInst == 'cd'):              # change directory (pathway)
            result = cmd_cd(cmd_tuple)

        elif(cmdInst == 'chdir'):           # change directory (with new pathway)
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

        elif(cmdInst == 'vi'):              # visual interface (read\create flat files)
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