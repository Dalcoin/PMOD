import os    
import sys   
import shutil

import ioparse as iop
import strlist as strl

'''
---------------
| Description |
---------------

   Consists of 'path_parse', which is a class to call commands within python 
scripts, allowing functionality in the image of Linux command-line inputs.  
Performing manipulations of the locations of files and directories from 
within python scripts. 

   The main function in the class is 'cmd' : path_parse.cmd(). This 
function allows commands to be passed which, among other things, return the 
contents of the current stored directory string, change the current stored 
directory string, move files between directories and delete files and 
directories. The class allows for pathway information to be stored and 
returned as string objects. 

'''

class path_parse:
    
    '''
    path_parse(osFormat, newPath=None, debug=False, colourPrint=True)    
    
    -----------
    | Inputs: |
    -----------
    
    osFormat = 'windows' or 'linux' 
    newPath = None (by default), else [string] 

        if [string] : the input string becomes the default .path variable
        if [None]   : the directory from which the script is run becomes the 
                      default .path variable.  

    debug = False (by default) : If True, debug info is printed to console, else nothing is printed 
    colourPrint = False (by default)  : If True, directory variable names are denoted by color when printing 
        
    '''
    
    def __init__(self, osFormat, newPath=None, debug=True, shellPrint=False, colourPrint=True):
        
        '''
        --------
        | init |
        --------
        
        Inputs :

            osFormat : 'windows' or 'linux'/'unix'
            newPath = None    (by default)
            debug = False (by default)
            colourPrint  = True  (by default)
            
        Path : 

            .varPath          : A string of the path in which the script is run
            .varPath_list     : A list of strings with values of the directory hiearchy in .path
            .varPath_head     : A string containing the primary (home) directory
            .varPath_contain  : A list of strings with values of the contents of .path
            .varPath_files    : A list of strings with values of the files found in the current directory.
            .varPath_folders  : A list os strings with values of the subdirectories in the current directory. 
            
            .varOS      :  A string to specify the operating system, this determines the path file format 
            .var_col     : True for color Escape code when printing, False by default
        
        '''
        
        self.cd_list = ['ls', 'pwd', 'dir', 'cd', 'chdir', 'mv', 'rm', 'cp', 'mkdir',
                        'rmdir', 'find', 'match', 'help', 'vi']

        self.single_command_list = ['ls', 'pwd'] 
        self.single_path_list_nogroup = ['cd','chdir','vi','help']
        self.single_path_list_group = ['rm','rmdir','mkdir','dir','find','match']
        self.double_path_list = ['mv', 'cp', 'cpdir']

        self.debug = bool(debug)                        
        self.varOS = str(osFormat).lower()
        
        if(self.varOS == 'windows'):
            self.delim = '\\'
        elif(self.varOS == 'linux'):
            self.delim = '/'
        else:
            self.delim = ':'
            
        self.var_col = colourPrint

        if(newPath == None):
            self.varPath = os.getcwd()
        else:            
            self.varPath = newPath
            
        self.varPath_List = self.Str2Arr(newPath)
        self.varPath_Head = self.varPath_List[0]
        self.varPath_Dir  = self.varPath_List[-1]
        self.varPath_Contains = self.contentPath('all')
        self.varPath_Files = self.contentPath('files')
        self.varPath_Folders = self.contentPath('folders')

    
    def documentation(self, string):
        """        	    
        ---------------
        | guidelines: |
        ---------------
	    
        1) "" functions read and modify from the class stored internal variables
        2) "Path" functions take full pathways and perform file and pathway manipulations 
           from these complete, input pathways.
        3) Path functions contain the word 'Path' in the name, Non-Path functions do not.
        4) Non-Path functions should not rely on the class pathway nor on any path class variables.
        5) Path functions should return a boolean value dependent on the success of the operation,
           any values they modify should be self variables, eliminating the need for returning values.
        6) Non-Path functions should return a boolean value when their operation does not 
           require a value to be returned (e.g. moving, copying or deleting objects) which is 
           dependent on the success of the operation. 
        7) For each Path operation available through the 'cmd' function, there should be a corrosponding
           means of accomplishing the same take through a Non-Path function. 
	    
        Function guideline summary:
	    
        1) Complete interdependence for Path functions
        2) Complete independence for Non-Path functions 
        3) Strict naming scheme to distinguish Path from Non-Path functions
        4) Path Variable restrictions 
        5) Return restrictions on Path functions (Boolean only) 
        6) Return restrictions on Non-Path functions 
        7) Corrospondance in operation between Path and Non-Path functionality      
	    

        Naming Convention: 

        1) 
            * path_ : designates a function which modifies the path variables
            * pw_ : designates a function which modifies an input path, does not affect path variables. 

        2)  
            * Non-Dundar self. variables must be denoted by starting with 'var_'
            * Non-Dundar self. functions must not start with 'var_'

        3) 
            * functions which exclusively modify file objects must contain the string, 'file', in their name 
            * functions which exclusively modify directory objects must contain the string, 'dir', in their 
              name
            * functions which exclusively modify file objects must not contain the string, 'dir', in their 
              name     
            * functions which exclusively modify directory objects must not contain the string, 'file', in 
              their name        

	    """

        action_list = ["Usage: ['ls',..,..] , returns a list of strings corrosponding to content of path directory",
                       
                       "Usage: ['pwd',..,..] , returns a string corrosponding to the pathway for path directory",
                       
                       "Usage: ['dir',['file1.file','file2.file'],..] , returns list of strings corrosponding "+
                       "to pathways of grouped files",
                       
                       "Usage: ['cd',..,pathway] , returns None, modifies the path variables to move from the "+ 
                       "path directory to that specified in the pathway. The value for pathway may be either "+
                       "{'..' to move up one directory, '~' to move to home, or a name of a subdirectory}",
                       
                       "Usage: [chdir,..,full_pathway] , returns None, moves path variables to move from the "+
                       "current directory to that specified by full_pathway, full_pathway must be a full pathway",
                       
                       "Usage: [mv,['file1.file','file2.file'],destination] , returns None, moves files in path "+
                       "directory to the destination directory.",
                       
                       "Usage: [rm,['file1.file','file2.file'],..] , returns None, removes files in path directory", 

                       "Usage: [mv,['file1.file','file2.file'],destination], copies files to destination, renames "+
                       "copied files according to numeric naming convention",
                       
                       "Usage: [mkdir,['fold1','fold2'],..] , returns None, creates folders in path directory",
                       
                       "Usage: [rmdir,['fold1','fold2'],..] , returns None, deletes folders and content in path directory",                             
                       "Usage: [find,['file1.file','file2.file'],..] , returns dictionary, searches for files by name, "+
                       " and returns a dictionary with boolean values for the existance of the files",
                          
                       "Usage: [match,['file1.file','file2.file'],..] , returns dictionary, searches for fragments, "+
                       " and returns a dictionary with boolean values for the files containing searched fragments",

                       "Usage: [help,['command'],..] , returns either a list or string, "+
                       "if no command is specified, 'help' returns a list of possible commands, else if a "+
                       "command is specified a string describing the commands usage is returned",
                         
                      ]   

#        help_dict = {k: v for k, v in zip(cd_list,action_list)}        
                                 
        if(string == 'help'):
            help_dict = dict(zip(cd_list,action_list))  # Added for backward compatability
            return help_dict
        else:
            return None 
         
                 
    def __cmd_input_parse__(self, string):
        '''
        -----------------------
        | __cmd_input_parse__ |
        -----------------------
        
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
                            if(count<len(array)-len(ignore)-1):
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
                        if(count<len(abridged_list)-1):
                            out_string = out_string+i+' '
                        else:
                            out_string = out_string+i                        
                    else:  
                        out_string = out_string + i
                    count+=1
                return out_string
                
        # Function Start
        if(not isinstance(string,str)): 
            if(self.debug):
                print("Error: input must be a string, not a "+str(type(string)))
            return ('',[],'')
                                                                   
        inputList = filter(lambda entry: entry != '',string.split(" "))           
        cmdInst = inputList[0]
        
        if(cmdInst in self.single_command_list):
            outInst = (cmdInst,[],'')
            return outInst
    
        if(cmdInst in self.single_path_list_nogroup):               
            outInst_str = combine_list_str(inputList,[1,'End'],space=True)
            if(cmdInst != 'vi'):
                outInst = (cmdInst,[],outInst_str)
            else:
                outInst = (cmdInst,[outInst_str],'')
            return outInst                     
        
        if(cmdInst in self.single_path_list_group):
            if(';' in string):
                inst_str = combine_list_str(inputList,[1,'End'],space=True)
                outInst_list = inst_str.split(';')
                outInst_list = filter(lambda l: l != '',outInst_list)
                outInst = (cmdInst,outInst_list,'')
                return outInst
            else:
                outInst_str = combine_list_str(inputList,[1,'End'],space=True)
                outInst = (cmdInst,[outInst_str],'')
                return outInst 
    
        if(cmdInst in self.double_path_list):
            if(';' in string):
                dest_list = []
                while(';' not in inputList[-1]):
                    dest_list.append(inputList.pop(-1))
                dest_list = dest_list[::-1]
                destStr = combine_list_str(dest_list,[0,'End'],space=True)
                inst_str = combine_list_str(inputList,[1,'End'],space=True)
                outInst_list = inst_str.split(';')
                outInst_list = filter(lambda l: l != '',outInst_list)
                outInst = (cmdInst,outInst_list,destStr)
                return outInst
            else:
                if(len(inputList) == 3):
                    outInst = (cmdInst,[inputList[1]],inputList[2])
                elif('.' in string):
                    dest_list = []
                    while('.' not in inputList[-1]):
                        dest_list.append(inputList.pop(-1))
                    print(inputList)
                    dest_list = dest_list[::-1]
                    destStr = combine_list_str(dest_list,[0,'End'],space=True)
                    inst_str = combine_list_str(inputList,[1,'End'],space=True)
                    outInst = (cmdInst,[inst_str],destStr)              
                else:
                    print("Error: The input spaceing or object style created ambiguity for the indexer: ")
                    print("The following is an echo of the input string which caused the issue: '"+string+"'")
                    outInst = (cmdInst,[],'')
                    return outInst
                
                return outInst
          
        if(self.debug):
            print("Error: command +'"+cmdInst+"' not recognized, use 'help' to view available functions")
        return None 
    
                             
    def joinNode(self,oldPath,newNode):
        '''
        Description: Adds a new node onto a pathway

        Input :

            oldPath : [string], pathway formatted string 
            newPath : [string], node 

        Output : [string], pathway formatted string
        '''

        if(not isinstance(oldPath,str)):
            if(self.debug):
                print(self.space+"[joinNode] Error: 'oldPath' must be a string\n") 
            return False        

        if(not isinstance(newNode,str)):
            if(self.debug):
                print(self.space+"[joinNode] Error: 'newNode' must be a string\n") 
            return False     

        newPath = oldPath+self.delim+newNode
        return newPath


    def delNode(self, oldPath, node):
          
        if(not isinstance(inPath,str):
            if(self.debug):
                print(self.space+"[Str2Arr] Error: input 'inPath' must be a string\n")
            return False  
        else: 
            arrPath = self.Str2Arr(oldPath)
            if(node == -1 and len(arrPath) > 1)
                return self.Arr2Str(arrPath[:-1])
            elif(isinstance(node,str)):
                node = node.lower()
                if(node == 'end' and len(arrPath)):
                    return self.Arr2Str(arrPath[:-1])
                elif(node in arrPath):          
                    listPath = []      
                    for entry in arrPath:
                        if(entry != node):
                            listPath.append(entry)
                        else:
                            break 
                    return self.Arr2Str(listPath)
                else:
                    print(self.space+"[delNode] Error: input 'node' not recognized")
            else:
                if(self.debug):
                    print(self.space+"[delNode] Error: input, 'node', could not be removed from input pathway, 'oldPath'\n")
                return False                  
        return False 


    def Arr2Str(self, inPath)

        if(not isinstance(inPath,(list,tuple)):
            if(self.debug):
                print(self.space+"[Arr2Str] Error: input 'path' must be a python array")
            return False  
        else:
            inPath = filter(None,inPath)
           
        for dir in inPath:
            if(count == 0):
                outPath = str(dir) 
            else:
                outPath = self.joinNode(outPath,dir)
                if(outPath == False):
                    if(self.debug):
                        errMSG = self.space+"[Arr2Str] Error: could not join the "
                        errMSG = errMSG+strl.print_ordinal(count+1)
                        errMSG = errMSG+" entry of input, 'inPath'"
                        print(errMSG)
                    return False 
            count+=1
        
        if(self.varOS == 'linux'):
            outPath = '/'+outPath
        if(self.varOS == 'windows'):
            if(outPath == self.winHead):
                outPath = outPath+"\\"
         
        return outPath
  

    def Str2Arr(self, inPath):

        if(not isinstance(inPath,str):
            if(self.debug):
                print(self.space+"[Str2Arr] Error: input 'inPath' must be a string")
            return False  
        else: 
            outPath = filter(None,inPath.split(self.delim))
            return outPath
        return False 
            
        
    def convertPath(self, inPath, inType='list', outType='str'):        
        '''        
        --------------
        | convertPath |  :  Convert Pathway 
        --------------

        description : converts between list formatted pathways and str formatted pathways

        Inputs :

            inPath : a pathway (formatted as either a string or array)
            inType  : [string] (Default value : 'list'), corrosponding to a python data-type
            outType : [string] (Default value : 'str'), corrosponding to a python data-type      

        Output : Path formatted list or string                                 
        '''      
        outPath = ''
        count = 0

        if(not isinstance(inType,str)):
            if(self.debug):
                print(self.space+"[convertPath] Error: 'inType' must be a string") 
            return False        
        else:
            inType = inType.lower()

        if(not isinstance(outType,str)):
            if(self.debug):
                print(self.space+"[convertPath] Error: 'outType' must be a string") 
            return False    
            outType = outType.lower() 
         
        typeList = ['arr','array','list','tup','tuple']
        typeStr = ['str','string']
              
        if(inType in typeList):                                                    
            if(outType in typeList):
                if(outType == 'arr' or outType == 'array'):                                 
                    return inPath
                elif(outType == 'list'):
                    return list(inPath)
                else:
                    return tuple(inPath)
            elif(outType in typeStr):
                return self.Arr2Str(inPath)                
            else:
                if(self.debug):
                    print(self.space+"[convertPath] Error: input 'outType' not recognized")
                return False
             
        elif(inType == 'str'):
            if(outType in typeStr):
                return inPath
            elif(outType in typeList):
                if(outType == 'arr' or outType == 'array' or outType == 'list'):
                    return self.Str2Arr(inPath)
                else:
                    return tuple(self.Str2Arr(inPath)) 
            else:
                if(self.debug):
                    print(self.space+"[convertPath] Error: input 'outType' not recognized")
                return False
        else:
            if(self.debug):
                print(self.space+"[convertPath] Error: input 'inType' not recognized")
            return False      
        if(self.debug):
            print(self.space+"[convertPath] Error: path conversion failed; cause unknown")             
        return False            
        
        
    def contentPath(self, inPath, objType = 'all', style = None):
        ''' 
        --------------
        | contentPath |
        --------------

        Description: Returns a list of strings corrosponding to the file names in 
                     the current (path) directory, option for selecting only a 
                     specific file extension. 
        
        Input: 
        
            'style': [string], (default value: None), A string corrosponding to 
                                                      a file extension type.
        
        Return:
         
            'file_list': [list], A list of strings corrosponding to all the files
                                 in the current (path) directory matching the 
                                 'style' extension, if 'style' == None, then all
                                 file names are included in 'file_list'                    
        '''
        
        folder_Names = ['dir', 'dirs', 'directory', 'directories', 'folder', 'folders']
        file_Names = ['file', 'files']

        if(isinstance(objType,str)):
            objType = objType.lower() 
        else:
            if(self.debug):
                print(self.space+"[convertPath] Error: 'objType' must be a string") 
            return False  
 
                   
        if(isinstance(inPath,str)): 
            path = inPath
        else:
            path = self.varPath
               
        pathContents = os.listdir(path)
            
        if(objType.lower() == 'all'):
            output = pathContents
        elif(objType.lower() in file_Names):              
            if(style == None):
                output = [entry for entry in pathContents if os.path.isfile(self.joinNode(self.varPath,entry))]
            else:
                file_List = []
                for entry in pathContents:
                    file_type = '.'+str(style)
                    if(file_type in entry):
                        file_List.append(entry)
                output = file_List             
        elif(objType.lower() in folder_Names):              
            output = [entry for entry in pathContents if os.path.isdir(self.joinNode(self.varPath,entry))]
        else:
            output = False
                           
        return output
       

    def __updatePath__(self, newPath, inType = 'str'):        
        '''
        -------------------
        | __updatePath__ |
        -------------------
                    
        Description: Formats a path-formatted list into a path-formatted string,
                     the new path then replaces the old path directory along with 
                     replacing the old path variables with those of the new path.

        Input: 
        
            'newPath': [list,tuple], A path-formatted list 
            'inType'        : [string], corrosponding to a python data-type

        Output : [Bool], success
        '''
          
        typeList = ['arr','array','list','tup','tuple']
        typeStr = ['str','string']  
          
        if(inType in typeList):
            self.varPath = self.convertPath(newPath)             
            self.varPath_List = list(newPath)
            self.varPath_Head = self.varPath_List[0]
            self.varPath_Dir  = self.varPath_List[-1]
            self.varPath_Contains = self.contentPath('all')
            self.varPath_Files = self.contentPath('files')
            self.varPath_Folders = self.contentPath('folders')                        
        elif(inType in typeStr):   
            self.varPath = newPath          
            self.varPath_List = self.Str2Arr(newPath)
            self.varPath_Head = self.varPath_List[0]
            self.varPath_Dir  = self.varPath_List[-1]
            self.varPath_Contains = self.contentPath('all')
            self.varPath_Files = self.contentPath('files')
            self.varPath_Folders = self.contentPath('folders')
        else:
            print("[__updatePath__] Error: 'inType' not a recognized type")
            return False 
        
        
    def __climbPath__(self, node, inType = 'str'):
        '''
        Description : if 'node' is a node in the default (current) pathway 
                      that the default (current) pathway directory is moved to
            
        Input:
         
            'inType' : [string] (Default value : 'str'), corrosponding to a python data-type
      
        The overhead and updating of class path info is taken care of with this function  
        '''        

        typeList = ['arr','array','list','tup','tuple']
        typeStr = ['str','string']     
           
        if(node in self.varPath_List):
            
            for entry in self.varPath_List:
                if(entry != node):
                    newPath_list.append(entry)
                else:
                    break
            newPath_list.append(node)

            if(inType in typeList):
                output = newPath_list
            elif(inType in typeStr):
                output = self.convertPath(newPath_list)
            elif(inType == 'update'):                
                output = self.__updatePath__(newPath_list,'list')
            else:
                if(self.debug):
                    print(self.space+"[__climbPath__] Error: 'inType' command: '"+str(inType)+"' not recongized")
                output = False
            return output
        else: 
            if(self.debug):
                print(self.space+"[__climbPath__] Error: Directory "+node+" not found in current (path) hierarchy")
            return False
        return False
        
    #############################
    # File and Folder Functions # 
    #############################
         
    def move(self, objPath, newPath, inType = 'str', update = False):
        '''
        Description : Moves and renames file and directory objects

        Input : 

            objPath : [string], A complete object pathway, the final node may be either a file or directory 
            newPath : [string], A complete directory pathway, the final node must be a directory 
            inType  : [string] (Default value : 'str'), corrosponding to a python data-type
            update  : [Bool] (Default value : False), option to update the current path variables

        Output : [Bool], success
        '''

        typeList = ['arr','array','list','tup','tuple']

        if(inType in typeList):
            newPath = self.convertPath(newPath)                
            objPath = self.convertPath(objPath)
                                         
        try: 
            shutil.move(objPath,newPath) 
        except: 
            if(self.debug):
                print("[move] Error: object could not be moved.")
                print("File pathway: "+objPath)
                print("Destination pathway: "+newPath+"\n")
            return False
        
        if(update):
            output = self.__updatePath__(self.varPath,'str')
        else:
            output = True
        return output

    
    def delFile(self, file_loc, inType = 'str', update=False):           
        '''
        Description : Attempts to delete the content at the location of the input pathway 
            
        Input:
      
            file_loc : A complete pathway string pointing to a file 
            inType: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables

        Output : [Bool], success
        '''  
        if(inType == 'list' or inType == 'arr'):
            file_loc = self.convertPath(file_loc)

        try:
            os.remove(file_loc)
        except:
            if(self.debug):
                print("[delFile] Error: File could not be deleted.")
                print("File pathway: "+file_loc+"\n")
            return False
            
        if(update):            
            utest = self.__updatePath__(self.varPath,'str')
            if(utest):
                return utest
            else:
                print("[delFile] Error: path not updated")     
                return False
        else:
            return True


    def copyFile(self, old_file_dir, new_file_dir, new_file_name = None, inType = 'str', update = False):
        '''
        Description : Attempts to copy a file from the 'old_file_dir' full pathway 
                      to the full directory pathway 'new_file_dir', with a name 
                      given by 'new_file_name'   

        Input : 
          
            new_file_name : [string], corrosponds to only the name of the copy  
            old_file_dir  : [string], corrosponds to the full pathway of the copied file
            new_file_dir  : [string] (Default : None), corrosponds to full pathway of the location of the copy
            inType: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables

        Output : [Bool], success
        '''

        if(inType == 'list' or inType == 'arr'):
            old_file_dir = self.convertPath(old_file_dir)
            new_file_dir = self.convertPath(new_file_dir)
            
        if(new_file_name != None and isinstance(new_file_name,str)):
            file_dup_loc = self.joinNode(new_file_dir, new_file_name)
        else: 
            new_file_name = self.convertPath(old_file_dir, inType = 'str', outType = 'list')
            new_file_name = new_file_name[-1].split('.')
            if(len(new_file_name) == 2):
                new_file_name = new_file_name[0]+'_copy.'+new_file_name[1] 
            else:
                new_file = new_file_name[0]+'_copy.'
                for i in range(len(new_file_name)-1):
                    new_file = new_file+'.'+new_file_name[i+1] 
                new_file_name = new_file
            file_dup_loc = self.joinNode(new_file_dir, new_file_name)

        try: 
            shutil.copyfile(old_file_dir, file_dup_loc)
        except:
            print("[copyFile] Error: failure create copy: '"+str(new_file_name))
            return False

        if(update):            
            utest = self.__updatePath__(self.varPath,'str')
            if(utest):
                return utest
            else:
                print("[copyFile] Error: path not updated")     
                return False
        else:
            return True
      
      
    def makeDir(self, newPath, inType='str', update=False):
        '''
        Description : creates a directory with the pathway given by 'newPath'
                
        Input : 
                   
            newPath : [string], pathway string corrosponding to a directory 
            inType: [string] (Default value : 'str'), corrosponding to a python data-type
        
        Output : [Bool], success   
        '''
        if(inType == 'str'):
            pathway = newPath
        elif(inType == 'list'):
            pathway = self.convertPath(newPath)
        else:
            print("[makeDir] Error: inType value: '"+str(inType)+"' not recognized")
            return False
            
        try:
            os.mkdir(pathway)
            if(update):
                utest = self.__updatePath__(self.varPath,'str')
                return utest     
            else:
                return True      
        except:           
            print("[makeDir] Error: a directory could not be created at this pathway")
            print("Pathway : "+pathway)     
            return False 
 
        
    def delDir(self, fold_loc, inType='str', update=False):
        '''
        Description : Recursively removes content and directory at pathway 'fold_loc'
               
        Input : 
                
            fold_loc : [string], corrosponds to  
            inType: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables 
               
        Output : [Bool], success
        '''   
        verif = False

        if(inType == 'str'):
            foldtype = isinstance(fold_loc, str)
            if(not foldtype):
                print("[delDir] Error: input pathway must be a string")
                return False
        elif(inType == 'list' or inType == 'arr'):
            try: 
                fold_loc = self.convertPath(fold_loc)
            except: 
                print("[delDir] Error: input pathway could not be parsed into a string")
                return False
        else:
            print("[delDir] Error: 'inType' is not a valid data type")
            return False
        
        try: 
            content = self.pw_contain(fold_loc)
        except:
            print("[delDir] Error: The pathway "+fold_loc+" did not yield a folder whose content could be accessed")
            return False
        
        for i in content:
            file_path = self.joinNode(fold_loc,i)
            if(os.path.isdir(file_path)):
                try:
                    verif = self.delDir(file_path)
                    if(verif == False):
                        print("[delDir] Error: the folder at pathway "+file_path+" could not be deleted")
                except: 
                    print("[delDir] Error: the folder at pathway "+file_path+" could not be deleted")             
            else:
                try:                
                    verif = self.delFile(file_path)
                    if(verif == False):
                        print("[delDir] Error: the file at pathway "+file_path+" could not be deleted")
                except: 
                    print("[delDir] Error: the folder at pathway "+file_path+" could not be deleted")  
        try:  
            verif = os.rmdir(fold_loc)
            if(verif == False):
                print("[delDir] Error: the file at pathway "+fold_loc+" could not be deleted")
        except: 
            print("[delDir] Error: the folder at pathway "+fold_loc+" could not be deleted") 

        if(update):
            utest = self.__updatePath__(self.varPath, 'str')
            return utest
 
        return verif
            
        
    def copyDir(self, old_fold_loc, new_fold_dir, new_fold_name = None, inType = 'str', update = False):
        '''
        Description : Copy directory (including contents) to new location
               
        Input : 
                          
            old_fold_loc  : [string], 
            new_fold_dir  : [string], 
            new_fold_name : [string] (Default : 'None'),  
            inType: [string] (Default : 'str'), corrosponding to a python data-type
            update : [Bool] (Default : False), option to update the current path variables    

        Output : [Bool], success           
        '''

        if(inType == 'list' or inType == 'arr'):
            old_fold_loc = self.convertPath(old_fold_loc)
            new_fold_dir = self.convertPath(new_fold_dir)

        if(new_fold_name != None and isinstance(new_fold_name,str)):
            fold_dup_loc = self.joinNode(new_fold_dir, new_fold_name)
        else: 
            new_fold_name = self.convertPath(old_fold_loc, inType = 'str', outType = 'list')
            new_fold_name = str(new_fold_name[-1])+'_copy'
            fold_dup_loc = self.joinNode(new_fold_dir, new_fold_name)
        
        try: 
            shutil.copytree(old_fold_loc, fold_dup_loc)
        except (WindowsError, OSError):
            print("[copyDir] Error: Folder already exists, file pathway: '"+fold_dup_loc+"' already occupied")
            return False
        except PermissionError:
            print("[copyDir] Error: 'PermissionError', access to file pathway: '"+new_fold_dir+"' is restricted")
            return False
        except:
            print("[copyDir] Error: failure to create copy file: '"+str(new_fold_name)+"'")
            return False

        if(update):            
            utest = self.__updatePath__(self.varPath,'str')
            if(utest):
                return utest
            else:
                print("[copyDir] Error: path not updated")     
                return False
        else:
            return True

                    
    def find(self, obj_name, foldPath, genre='all', inType='str'):
        '''
        Description : Searches an input directory for an object name

        Input :

            obj_name : [string], Name of file to be searched 
            foldPath : [string], pathway of folder in which 'obj_name' is searched
            genre     : [string] (Default : 'all'), type of object to be searched for 
            inType: [string] (Default : 'str'), corrosponding to a python data-type 

        Output : [Bool], success         
        '''  
        if(inType == 'list' or inType == 'arr'):
            foldPath = self.convertPath(foldPath)
        
        if(isinstance(genre,str) and isinstance(inType,str)):
            genre = genre.lower()
            inType = inType.lower()
                
        if(genre == 'files'):
            spf = self.pw_contain(foldPath, rtrn='files')
        elif(genre == 'folders'):     
            spf = self.pw_contain(foldPath, rtrn='folders') 
        else:
            spf = self.pw_contain(foldPath)

        if(obj_name in spf):
            return True
        else:
            return False            
        

    def match(self, fragment, foldPath, genre='files', inType='str'):
        '''
        Description : Searches an input directory for any object containing a specific string

        Input :

            fragment : [string], string to be matched 
            foldPath : [string], pathway of folder in which 'obj_name' is searched
            genre     : [string] (Default : 'all'), type of object to be searched for 
            inType: [string] (Default : 'str'), corrosponding to a python data-type 

        Output : [Bool], success         
        ''' 
 
        if(inType == 'list' or inType == 'arr'):
            foldPath = self.convertPath(foldPath)
        
        if(isinstance(genre,str) and isinstance(inType,str)):
            genre = genre.lower()
            inType = inType.lower()
                
        if(genre == 'files'):
            spf = self.pw_contain(foldPath, rtrn='files')
        elif(genre == 'folders'):     
            spf = self.pw_contain(foldPath, rtrn='folders') 
        else:
            spf = self.pw_contain(foldPath)
              
        for i in spf:
            if(fragment in i):
                match_list.append(i)
        return match_list
        
        
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
        if(self.debug):
            try:
                ecrive = self.__fancyPrint__(self.var_col)         
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
        return None
        

    ####################################################    
    # cmd Function: String-to-Command Parsing Function #
    ####################################################
    
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
                if(self.debug):                        
                    print("Warning: No remaining parent directories left")
                return True
            else:
                return False

        def printFunc(test):
            success = True
            if(test):
                ptest = self.__runFancyPrint__()
                if(not ptest):
                    success = False 
                    print("Error: An unknown error was raised while attempting to print...")
            else:
                print("Error: Failure while updating current path")
                success = False
            return success
            

        def updater(newPath, inType, success, value):
            utest = self.__updatePath__(newPath, inType)                 
            success = printFunc(utest)
            result = (success,value)
            return result

                
        def cmd_pwd(tup):
            success = True
            cmdInst, file_list, destStr = tup
                        
            try:
                value = self.varPath 
            except: 
                value = None
                success = False
                print("Error: current (path) directory pathway not found")

            success = printFunc(success)               
            result = (success,value)                                       
            return result
            
             
        def cmd_ls(tup):
            success = True
            cmdInst, file_list, destStr = tup 

            result = updater(self.varPath_List,'list',True,'')

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
                                       
            for i in file_list:
                verify = self.find(i, self.varPath)
                if(verify):
                    new_file_list.append(self.joinNode(self.varPath,i))
                else:
                    success = False
                    print("Warning Error: file name, '"+i+"' not found in current (path) directory")
            
            value = new_file_list

            if(self.debug):
                ptest_1 = self.__runFancyPrint__()                
                print("Pathway string(s): " )
                ptest_2 = self.__fancyPrintList__(new_file_list)
                if(not ptest_1 or not ptest_2):
                    success = False
                    print("Error: An unknown error was raised while attempting to print...")
            
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
                result = updater(up_path_list,'list',success,value)
                return result
            
            elif(destStr in self.varPath_Contains):
                dest_loc = self.joinNode(self.varPath,destStr)
                if(os.path.isdir(dest_loc)): 
                    newPath_list = list(self.varPath_List)
                    newPath_list.append(destStr)
                else:
                    success = False 
                    print("Error: '"+dest_loc+"not a valid folder in current (path) directory")
                    print("It appears that '"+dest_loc+"' is a file object or is corrupted")    
                    result = (success,value)
                    return result 
                result = updater(newPath_list,'list',success,value)
                return result
            
            elif(destStr[0] == '/' or destStr[0] == '\\'):
                ndir_inst = destStr[1:]
                ctest = self.__climbPath__(ndir_inst,'update')
                success = printFunc(ctest)  
                result = (success,value)
                return result
                    
            elif(destStr == '~'):                
                ctest = self.__climbPath__(self.varPath_Head,'update')
                success = printFunc(ctest)  
                result = (success,value)
                return result
                
            else:
                print("Error: '"+destStr+"' not a valid destination")
                success = False
            
            result = (success,value)
            return result
            
            
        def cmd_chdir(tup):
            success = True            
            value = None
            cmdInst, file_list, destStr = tup 
            
            try: 
                utest = self.__updatePath__(destStr,'str')
                success = printFunc(utest)              
            except:
                print('Error: pathway '+destStr+' could not be reached')
                success = False 
            
            result = (success,value)
            return result 
            
                
        def cmd_mv(tup):
            
            success = True            
            value = None
            cmdInst, file_list, destStr = tup      
             
            mv_file_list = file_list 
            
            for i in range(len(mv_file_list)):
                mv_file_list[i] = self.joinNode(self.varPath,mv_file_list[i])
                         
            # Move File                                     
            if(destStr == '..'):                  
                if(headCheck()):
                    result = (success,value)
                    return result  
                else:
                    up_path_list = list(self.varPath_List)[:-1]

                up_path_str = self.convertPath(up_path_list)   
                up_path_has = self.pw_contain(up_path_str)
                for i in mv_file_list: 
                    if(i in up_path_has):
                        print("Warning: '"+i+"' already exists in the namespace of the target directory, no action taken")
                        continue                     
                    mtest = self.move(i,up_path_str)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")

                result = updater(self.varPath_List,'list',success,value)
                return result     
            
            elif(destStr in self.varPath_Contains and destStr not in self.varPath_Files):                
                dest_path_list = list(self.varPath_List)
                dest_path_list.append(destStr)  
                     
                path_str = self.convertPath(dest_path_list)   
                path_has = self.pw_contain(path_str)
                for i in mv_file_list:           
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue     
                    mtest = self.move(i,path_str)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.varPath_List,'list',success,value)
                return result  
            
            elif(destStr[0] == '/' or destStr[0] == '\\'):
                destStr = destStr[1:]
                dest_path_list = self.__climbPath__(destStr,'list')

                path_str = self.convertPath(dest_path_list)   
                path_has = self.pw_contain(path_str)
                for i in mv_file_list:   
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue            
                    mtest = self.move(i,dest_path_list,str,list)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.varPath_List,'list',success,value)
                return result  
                                      
            elif(destStr == '~'):                
                dest_path_list = self.__climbPath__(self.varPath_Head,'list')

                path_str = self.convertPath(dest_path_list)   
                path_has = self.pw_contain(path_str)
                for i in mv_file_list:       
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue         
                    mtest = self.move(i,dest_path_list,str,list)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.varPath_List,'list',success,value)
                return result  

            elif(destStr not in self.varPath_Contains and len(mv_file_list) == 1):  
                destStr = self.joinNode(self.varPath,destStr)           
                mtest = self.move(mv_file_list[0],destStr,str,str)
                if(not mtest):
                    success = False 
                    print("Error: contents of this path: '"+i+"' could not be moved")                                 
                result = updater(self.varPath_List,'list',success,value)
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
                    dtest = self.delFile(file_path_str, update = True)
                    if(not dtest):
                        success = False 
                        print("Error: contents of the path: '"+i+"' could not be deleted")
                else: 
                    print("Error: '"+i+"' not found within the current (path) directory")
            
            result = updater(self.varPath_List,'list',success,value)
            return result


        def cmd_cp(tup):

            def __cp_help_func__(file_list, path_str):  
                  
                success = True            
                value = None

                path_has = self.pw_contain(path_str, rtrn = 'files')
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
                                                                    
                result = updater(self.varPath_List,'list',success,value)
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
                path_str = self.joinNode(self.varPath,destStr)  
                result = __cp_help_func__(file_list, path_str)
                return result
            
            elif(destStr[0] == '/' or destStr[0] == '\\'):
                ndir_inst = destStr[1:]
                path_str = self.__climbPath__(ndir_inst,'str')
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(ndir_inst)+"' could not be found in the root pathway")
                    return (success,value)
                    
                result = __cp_help_func__(file_list, path_str)
                return result
                    
            elif(destStr == '~'):           
                path_str = self.varPath_Head 
                try:                   
                    path_has = self.pw_contain(path_str, rtrn = 'files')
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
                    print("Error: contents of this path: '"+i+"' could not be moved")
                                     
            result = updater(self.varPath_List,'list',success,value)
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

            result = updater(self.varPath_List,'list',success,value)
            return result        


        def cmd_cpdir(tup):                   

            def __cpdir_help_func__(file_list, path_str):  

                success = True
                value = None

                path_has = self.pw_contain(path_str, rtrn = 'folders')
                for i in file_list:                    
                    inc = 1
                    old_inst = self.joinNode(self.varPath,i)
                    cp_inst = i+"_copy"
                    while(cp_inst in path_has):
                        inc+=1
                        cp_inst = cp_inst + '_' + str(inc)
                    ctest = self.copyDir(old_inst, path_str, new_fold_name = cp_inst)
                    if(not ctest):
                        success = False 
                        print("Error: contents of the path: '"+str(i)+"' could not be copied")
                                                                    
                result = updater(self.varPath_List,'list',success,value)
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
                path_str = self.__climbPath__(ndir_inst,'str')
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
                                 
            result = updater(self.varPath_List,'list',success,value)
            return result
                     
                            
        def cmd_help(tup):

            success = True            
            value = None
            cmdInst, file_list, destStr = tup 
            
            help_dict = self.documentation('help')
               
            if(destStr == ''):
                if(self.debug):
                    print('Below is a list of valid input commands:\n')
                    self.__fancyPrintList__(cd_list)
                    value = cd_list
                    help_text = "Place command name after 'help' for more info on that command"

            else:
                cmd_val = destStr
                if(cmd_val in cd_list):
                    help_dict = self.documentation('help')
                    help_text = help_dict[cmd_val]
                else:
                    success = False
                    help_text = "Error: the command '"+cmd_val+"' not recognized"

            if(self.debug):                   
                print(help_text)
                print('\n')

            value = help_text                                      
            result = (success,value)
            return result   
                
                
            
        ##################
        # Function: Main #
        ##################

        result = (False,None)

        # Dummy test
        if(not isinstance(cmd_string,str)):
            if(self.debug):
                print("Warning: Input must be a properly formated string ")
                print("Warning: No action taken, see help for more info on proper 'cmd' formatting ")    
            return result     
        if(cmd_string == '' or cmd_string.isspace()):
            if(self.debug):
                print("Warning: Input must be a properly formated string ")
                print("Warning: No action taken, see help for more info on proper 'cmd' formatting ")    
            return result    

        cmd_tuple = self.__cmd_input_parse__(cmd_string)   
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
            spc = '     '
            tup_str = str(cmd_tuple)
            if(self.debug or self.shellPrint)
                print("Error: Input '"+cmd_string+"' not resolved")
            if(self.shellPrint):
                print("It appears that either 'cmd_string' was not recognized")
                print("or that, the operand with which it was combined was not properly parsed")
                print("Below is a summary of the output:")
                print("\n")
                print(spc+"'cmdInst' = '"+cmdInst+"'")
                print(spc+"'cmd_tuple' = '"+tup_str+"'") 
                print('\n')
         
        return result 