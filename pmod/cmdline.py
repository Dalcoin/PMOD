import os    
import sys   
import shutil

import ioparse as iop

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
    path_parse(os_form, new_path=None, path_print=False, print_col=True)    
    
    -----------
    | Inputs: |
    -----------
    
    os_form = 'windows' or 'linux' 
    new_path = None (by default), else [string] 

        if [string] : the input string becomes the default .path variable
        if [None]   : the directory from which the script is run becomes the 
                      default .path variable.  

    path_print = False (by default) : If True, debug info is printed to console, else nothing is printed 
    print_col = False (by default)  : If True, directory variable names are denoted by color when printing 
        
    '''
    
    def __init__(self, os_form, new_path=None, path_print=False, print_col=True):
        
        '''
        --------
        | init |
        --------
        
        Inputs :

            os_form : 'windows' or 'linux'/'unix'
            new_path = None    (by default)
            path_print = False (by default)
            print_col  = True  (by default)
            
        Path : 

            .var_path : A string of the path in which the script is run
            .var_path_list : A list of strings with values of the directory hiearchy in .path
            .var_path_head : A string containing the primary (home) directory
            .var_path_contain : A list of strings with values of the contents of .path
            .var_path_files : A list of string with values of the file (names with file type) in .path   
            
            .var_os:  A string to specify the operating system, this determines the path file format 
            .var_col: True for color Escape code when printing, False by default
        
        '''
        
        global delim
        global cd_list, single_command_list, single_path_list_group
        global single_path_list_nogroup, double_path_list

        cd_list = ['ls', 'pwd', 'dir', 'cd', 'chdir', 'mv', 'rm', 'cp', 'mkdir',
                   'rmdir', 'find', 'match', 'help', 'vi']

        lx_distro = ['ubuntu','xubutnu','redhat','debian','fedora','mintos']
        os_list = ['windows','linux','unix']

        single_command_list = ['ls', 'pwd'] 
        single_path_list_nogroup = ['cd','chdir','vi','help']
        single_path_list_group = ['rm','rmdir','mkdir','dir','find','match']
        double_path_list = ['mv', 'cp', 'cpdir']
        
        self.var_os = str(os_form).lower()

        if(self.var_os in lx_distro):
            self.var_os = 'linux'
        
        if(self.var_os == 'windows'):
            delim = '\\'
        elif(self.var_os == 'linux' or self.var_os == 'unix'):
            delim = '/'
        else:
            delim = '.'
            
        self.var_col = print_col
        
        if(new_path != None):            
            self.var_path = new_path
            if(self.var_os == 'windows'):
                self.var_path_list = self.var_path.split(delim)
                self.var_path_head = self.var_path.split(delim)[0]
            else:
                self.var_path_list = self.var_path.split(delim)
                self.var_path_list = self.var_path_list[1:]
                self.var_path_head = self.var_path_list[0]
            self.var_path_contain = os.listdir(self.var_path)
            self.var_path_files = self.__path_files__()
            self.var_path_print = path_print
        else:
            self.var_path = os.getcwd()
            if(self.var_os == 'windows'):
                self.var_path_list = self.var_path.split(delim)
                self.var_path_head = self.var_path.split(delim)[0]
            else:
                self.var_path_list = self.var_path.split(delim)
                self.var_path_list = self.var_path_list[1:]
                self.var_path_head = self.var_path_list[0]
            self.var_path_contain = os.listdir(self.var_path)
            self.var_path_files = self.__path_files__()
            self.var_path_print = path_print
    
    def documentation(self, string):
        """        	    
        ---------------
        | guidelines: |
        ---------------
	    
        1) Path functions read and modify from the class stored path variables
        2) Non-Path functions take full pathways and perform file and pathway manipulations 
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
         
            out_inst : a tuple formatted for parsing in the .cmd() function
                       takes the form: (cmd_inst, [inst_strs], dest_str)
            cmd_inst : a string, corrosponding to a valid cmd command
            inst_strs: one or more strings, corrosponding to instances 
                        upon which the cmd_inst acts
            dest_str : a string, corrosponding to a valid destination 
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
                
        if(not isinstance(string,str)): 
            print("Error: input must be a string, not a "+str(type(string)))
            return ('',[],'')
                                                                   
        string_list = string.split(" ")
        string_list = filter(lambda l: l != '',string_list)            
        cmd_inst = string_list[0]
        nstr = len(string_list)
        
        if(cmd_inst in single_command_list):
            out_inst = (cmd_inst,[],'')
            return out_inst
    
        if(cmd_inst in single_path_list_nogroup):               
            out_inst_str = combine_list_str(string_list,[1,'End'],space=True)
            if(cmd_inst != 'vi'):
                out_inst = (cmd_inst,[],out_inst_str)
            else:
                out_inst = (cmd_inst,[out_inst_str],'')
            return out_inst                     
        
        if(cmd_inst in single_path_list_group):
            if(';' in string):
                inst_str = combine_list_str(string_list,[1,'End'],space=True)
                out_inst_list = inst_str.split(';')
                out_inst_list = filter(lambda l: l != '',out_inst_list)
                out_inst = (cmd_inst,out_inst_list,'')
                return out_inst
            else:
                out_inst_str = combine_list_str(string_list,[1,'End'],space=True)
                out_inst = (cmd_inst,[out_inst_str],'')
                return out_inst 
    
        if(cmd_inst in double_path_list):
            if(';' in string):
                dest_list = []
                while(';' not in string_list[-1]):
                    dest_list.append(string_list.pop(-1))
                dest_list = dest_list[::-1]
                dest_str = combine_list_str(dest_list,[0,'End'],space=True)
                inst_str = combine_list_str(string_list,[1,'End'],space=True)
                out_inst_list = inst_str.split(';')
                out_inst_list = filter(lambda l: l != '',out_inst_list)
                out_inst = (cmd_inst,out_inst_list,dest_str)
                return out_inst
            else:
                if(len(string_list) == 3):
                    out_inst = (cmd_inst,[string_list[1]],string_list[2])
                elif('.' in string):
                    dest_list = []
                    while('.' not in string_list[-1]):
                        dest_list.append(string_list.pop(-1))
                    print(string_list)
                    dest_list = dest_list[::-1]
                    dest_str = combine_list_str(dest_list,[0,'End'],space=True)
                    inst_str = combine_list_str(string_list,[1,'End'],space=True)
                    out_inst = (cmd_inst,[inst_str],dest_str)              
                else:
                    print("Error: The input spaceing or object style created ambiguity for the indexer: ")
                    print("The following is an echo of the input string which caused the issue: '"+string+"'")
                    out_inst = (cmd_inst,[],'')
                    return out_inst
                
                return out_inst
          
        print("Error: command +'"+cmd_inst+"' not recognized, use 'help' to view available functions")
        return None 
    
                             
    def pw_join(self,old_path,new_node):
        '''
        Description: Adds a new node onto a pathway

        Input :

            old_path : [string], pathway formatted string 
            new_path : [string], node 

        Output : [string], pathway formatted string
        '''
        output = old_path+delim+new_node
        return output
            
        
    def pw_convert(self, trac_in, insort='list', outsort='str'):        
        '''        
        --------------
        | pw_convert |  :  Convert Pathway 
        --------------

        description : converts between list formatted pathways and str formatted pathways

        Inputs :

            trac_in : a pathway (formatted as either a string or array)
            insort  : [string] (Default value : 'list'), corrosponding to a python data-type
            outsort : [string] (Default value : 'str'), corrosponding to a python data-type      

        Output : Path formatted list or string                                 
        '''      
        trac_out = ''
        count = 0
              
        if(insort == 'list' or insort == 'arr'):
            if(insort == 'arr'):
                trac_in = list(trac_in)               
            while('' in trac_in):
                trac_in.remove('')
            for i in trac_in:
                if(count == 0):
                    trac_out = str(i) 
                else:
                    trac_out = self.pw_join(trac_out,i)
                count+=1
            
            if(self.var_os == 'unix' or self.var_os == 'linux'):
                trac_out = '/'+trac_out
             
            if(outsort == 'list' or outsort == 'arr'):
                trac_out = trac_out.split(delim)
                trac_out = filter(lambda l: l != '',trac_out)                 
             
        elif(insort == 'str'):
            if(outsort == 'list' or outsort == 'arr'):
                trac_out = trac_out.split(delim)
                trac_out = filter(lambda l: l != '',trac_out)     
            else: 
                trac_out = trac_in                    

        return trac_out            
        
        
    def __path_files__(self, style = None):
        '''
        ------------------
        | __path_files__ |
        ------------------

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
        current_folder_content = list(self.var_path_contain)
        file_list = []
        if(style == None):
            for i in current_folder_content:
                if(os.path.isfile(self.pw_join(self.var_path,i))):
                    file_list.append(i)
        else:
            for i in current_folder_content:
                file_type = '.'+str(style)
                if(file_type in i):
                    file_list.append(i)
        return file_list
    

    def __update_path__(self, path_updater, sort):        
        '''
        -------------------
        | __update_path__ |
        -------------------
                    
        Description: Formats a path-formatted list into a path-formatted string,
                     the new path then replaces the old path directory along with 
                     replacing the old path variables with those of the new path.

        Input: 
        
            'path_updater': [list,tuple], A path-formatted list 
            'sort'        : [string], corrosponding to a python data-type

        Output : [Bool], success
        '''
        if(sort == 'list' or sort == 'arr'):
            if(sort == 'arr'):
                path_updater = list(path_updater)
            self.var_path_list = path_updater
            self.var_path = self.pw_convert(path_updater)
            if(self.var_os == 'windows'):                    
                if(self.var_path == self.var_path_head):
                    self.var_path = self.var_path+'//'
            self.var_path_contain = os.listdir(self.var_path)
            self.var_path_files = self.__path_files__()   
            return True
        elif(sort == 'str'):
            self.var_path = path_updater
            self.var_path_list = self.var_path.split(delim)
            if(self.var_os == 'windows'):                    
                if(self.var_path == self.var_path_head):
                    self.var_path = self.var_path+'//'
            self.var_path_contain = os.listdir(self.var_path)
            self.var_path_files = self.__path_files__() 
            return True
        else:
            print("[__update_path__] Error: 'sort' must be string corrosponding to a compatible python type")
            return False 
        
        
    def __climb_path__(self, up_dir_inst, sort = 'str'):
        '''
        Description : if 'up_dir_inst' is a node in the default (current) pathway 
                      then the default (current) pathway is moved to corrospond to that node 

        Input:
         
            'sort' : [string] (Default value : 'str'), corrosponding to a python data-type
      
        The overhead and updating of class path info is taken care of with this function  
        '''        
        if(up_dir_inst in self.var_path_list):
            spl_copy = list(self.var_path_list)
            new_path_list = []
            switch = True
            for i in spl_copy:
                if(i != up_dir_inst and switch == True):
                    new_path_list.append(i)
                else:
                    switch = False
            new_path_list.append(up_dir_inst)
            if(sort == 'list' or sort == 'arr'):
                output = new_path_list
                return output
            elif(sort == 'str'):
                output = self.pw_convert(new_path_list)
                return output
            elif(sort == 'update'):                
                output = self.__update_path__(new_path_list,'list')
                return output
            else:
                print("[__climb_path__] Error: 'sort' command: '"+str(sort)+"' not recongized")
        else: 
            print("[__climb_path__] Error: Directory "+up_dir_inst+" not found in current (path) hierarchy")
            return False
        
    
    def pw_contain(self, path, sort = 'str', rtrn = 'all'):
        '''
        Description : Takes a pathway input,
                      returns either a string formatted pathway or list formatted pathway

        Input :

            'path' : [string] or [array], a pathway formatted string or array 
            'sort' : [string] (Default value : 'str'), corrosponding to a python data-type
            'rtrn' : [string], valid entries:
                'all' : returns all contents found at 'path'
                'files' : returns only string names of the files found at 'path'
                'folders' : returns only string names of the folders found at 'path'

        Output : 
         
            output : [string] or [list], a pathway formatted string or list
        ''' 
        if(sort == 'str'):
            new_path = path
        elif(sort == 'list' or sort == 'arr'):
            new_path = self.pw_convert(path)
        else:
            print("[pw_contain] Error: 'sort' option must be either 'str' or 'list'; '"
                  +str(sort)+"' is invalid")
            return False
        
        try: 
            content = os.listdir(new_path)
        except:
            return False
        
        if(rtrn == 'all'):
            return content
        elif(rtrn == 'files'):
            output = []
            for i in content: 
                if('.' in i): output.append(i)
            return output
        elif(rtrn == 'folders'):
            output = []
            for i in content: 
                if('.' not in i): output.append(i)
            return output            
        else:
            print("[pw_contain] Error: 'rtrn' input; '"+rtrn+"' , not valid")
            
             
    
    def move(self, obj_loc, new_loc, sort = 'str', update = False):
        '''
        Description : Moves and renames file and directory objects

        Input : 

            obj_loc : [string], A complete object pathway, the final node may be either a file or directory 
            new_loc : [string], A complete directory pathway, the final node must be a directory 
            sort: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables

        Output : [Bool], success
        '''
        if(sort == 'list' or sort == 'arr'):
            new_loc = self.pw_convert(new_loc)                
            obj_loc = self.pw_convert(obj_loc)
                      
        if(self.var_os == 'windows'):                    
            if(new_loc == self.var_path_head):
                new_loc = new_loc+'//'
                   
        try: 
            shutil.move(obj_loc,new_loc) 
        except: 
            print("[move] Error: object could not be moved.")
            print("File pathway: "+obj_loc)
            print("Destination pathway: "+new_loc)
            return False
        
        if(update):
            output = self.__update_path__(self.var_path,'str')
        else:
            output = True
        return output

    
    def del_file(self, file_loc, sort = 'str', update=False):           
        '''
        Description : Attempts to delete the content at the location of the input pathway 
            
        Input:
      
            file_loc : A complete pathway string pointing to a file 
            sort: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables

        Output : [Bool], success
        '''  
        if(sort == 'list' or sort == 'arr'):
            file_loc = self.pw_convert(file_loc)

        try:
            os.remove(file_loc)
        except:
            print("[del_file] Error: File could not be deleted.")
            print("File pathway: "+file_loc)
            return False
            
        if(update):            
            utest = self.__update_path__(self.var_path,'str')
            if(utest):
                return utest
            else:
                print("[del_file] Error: path not updated")     
                return False
        else:
            return True


    def copy_file(self, old_file_dir, new_file_dir, new_file_name = None, sort = 'str', update = False):
        '''
        Description : Attempts to copy a file from the 'old_file_dir' full pathway 
                      to the full directory pathway 'new_file_dir', with a name 
                      given by 'new_file_name'   

        Input : 
          
            new_file_name : [string], corrosponds to only the name of the copy  
            old_file_dir  : [string], corrosponds to the full pathway of the copied file
            new_file_dir  : [string] (Default : None), corrosponds to full pathway of the location of the copy
            sort: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables

        Output : [Bool], success
        '''

        if(sort == 'list' or sort == 'arr'):
            old_file_dir = self.pw_convert(old_file_dir)
            new_file_dir = self.pw_convert(new_file_dir)
            
        if(new_file_name != None and isinstance(new_file_name,str)):
            file_dup_loc = self.pw_join(new_file_dir, new_file_name)
        else: 
            new_file_name = self.pw_convert(old_file_dir, insort = 'str', outsort = 'list')
            new_file_name = new_file_name[-1].split('.')
            if(len(new_file_name) == 2):
                new_file_name = new_file_name[0]+'_copy.'+new_file_name[1] 
            else:
                new_file = new_file_name[0]+'_copy.'
                for i in range(len(new_file_name)-1):
                    new_file = new_file+'.'+new_file_name[i+1] 
                new_file_name = new_file
            file_dup_loc = self.pw_join(new_file_dir, new_file_name)

        try: 
            shutil.copyfile(old_file_dir, file_dup_loc)
        except:
            print("[copy_file] Error: failure create copy: '"+str(new_file_name))
            return False

        if(update):            
            utest = self.__update_path__(self.var_path,'str')
            if(utest):
                return utest
            else:
                print("[copy_file] Error: path not updated")     
                return False
        else:
            return True
      
      
    def create_dir(self, new_path, sort='str', update=False):
        '''
        Description : creates a directory with the pathway given by 'new_path'
                
        Input : 
                   
            new_path : [string], pathway string corrosponding to a directory 
            sort: [string] (Default value : 'str'), corrosponding to a python data-type
        
        Output : [Bool], success   
        '''
        if(sort == 'str'):
            pathway = new_path
        elif(sort == 'list'):
            pathway = self.pw_convert(new_path)
        else:
            print("[create_dir] Error: sort value: '"+str(sort)+"' not recognized")
            return False
            
        try:
            os.mkdir(pathway)
            if(update):
                utest = self.__update_path__(self.var_path,'str')
                return utest     
            else:
                return True      
        except:           
            print("[create_dir] Error: a directory could not be created at this pathway")
            print("Pathway : "+pathway)     
            return False 
 
        
    def del_dir(self, fold_loc, sort='str', update=False):
        '''
        Description : Recursively removes content and directory at pathway 'fold_loc'
               
        Input : 
                
            fold_loc : [string], corrosponds to  
            sort: [string] (Default value : 'str'), corrosponding to a python data-type
            update : [Bool] (Default value : False), option to update the current path variables 
               
        Output : [Bool], success
        '''   
        verif = False

        if(sort == 'str'):
            foldtype = isinstance(fold_loc, str)
            if(not foldtype):
                print("[del_dir] Error: input pathway must be a string")
                return False
        elif(sort == 'list' or sort == 'arr'):
            try: 
                fold_loc = self.pw_convert(fold_loc)
            except: 
                print("[del_dir] Error: input pathway could not be parsed into a string")
                return False
        else:
            print("[del_dir] Error: 'sort' is not a valid data type")
            return False
        
        try: 
            content = self.pw_contain(fold_loc)
        except:
            print("[del_dir] Error: The pathway "+fold_loc+" did not yield a folder whose content could be accessed")
            return False
        
        for i in content:
            file_path = self.pw_join(fold_loc,i)
            if(os.path.isdir(file_path)):
                try:
                    verif = self.del_dir(file_path)
                    if(verif == False):
                        print("[del_dir] Error: the folder at pathway "+file_path+" could not be deleted")
                except: 
                    print("[del_dir] Error: the folder at pathway "+file_path+" could not be deleted")             
            else:
                try:                
                    verif = self.del_file(file_path)
                    if(verif == False):
                        print("[del_dir] Error: the file at pathway "+file_path+" could not be deleted")
                except: 
                    print("[del_dir] Error: the folder at pathway "+file_path+" could not be deleted")  
        try:  
            verif = os.rmdir(fold_loc)
            if(verif == False):
                print("[del_dir] Error: the file at pathway "+fold_loc+" could not be deleted")
        except: 
            print("[del_dir] Error: the folder at pathway "+fold_loc+" could not be deleted") 

        if(update):
            utest = self.__update_path__(self.var_path, 'str')
            return utest
 
        return verif
            
        
    def copy_dir(self, old_fold_loc, new_fold_dir, new_fold_name = None, sort = 'str', update = False):
        '''
        Description : Copy directory (including contents) to new location
               
        Input : 
                          
            old_fold_loc  : [string], 
            new_fold_dir  : [string], 
            new_fold_name : [string] (Default : 'None'),  
            sort: [string] (Default : 'str'), corrosponding to a python data-type
            update : [Bool] (Default : False), option to update the current path variables    

        Output : [Bool], success           
        '''

        if(sort == 'list' or sort == 'arr'):
            old_fold_loc = self.pw_convert(old_fold_loc)
            new_fold_dir = self.pw_convert(new_fold_dir)

        if(new_fold_name != None and isinstance(new_fold_name,str)):
            fold_dup_loc = self.pw_join(new_fold_dir, new_fold_name)
        else: 
            new_fold_name = self.pw_convert(old_fold_loc, insort = 'str', outsort = 'list')
            new_fold_name = str(new_fold_name[-1])+'_copy'
            fold_dup_loc = self.pw_join(new_fold_dir, new_fold_name)
        
        try: 
            shutil.copytree(old_fold_loc, fold_dup_loc)
        except (WindowsError, OSError):
            print("[copy_dir] Error: Folder already exists, file pathway: '"+fold_dup_loc+"' already occupied")
            return False
        except PermissionError:
            print("[copy_dir] Error: 'PermissionError', access to file pathway: '"+new_fold_dir+"' is restricted")
            return False
        except:
            print("[copy_dir] Error: failure to create copy file: '"+str(new_fold_name)+"'")
            return False

        if(update):            
            utest = self.__update_path__(self.var_path,'str')
            if(utest):
                return utest
            else:
                print("[copy_dir] Error: path not updated")     
                return False
        else:
            return True

                    
    def find(self, obj_name, fold_path, genre='all', sort='str'):
        '''
        Description : Searches an input directory for an object name

        Input :

            obj_name : [string], Name of file to be searched 
            fold_path : [string], pathway of folder in which 'obj_name' is searched
            genre     : [string] (Default : 'all'), type of object to be searched for 
            sort: [string] (Default : 'str'), corrosponding to a python data-type 

        Output : [Bool], success         
        '''  
        if(sort == 'list' or sort == 'arr'):
            fold_path = self.pw_convert(fold_path)
        
        if(isinstance(genre,str) and isinstance(sort,str)):
            genre = genre.lower()
            sort = sort.lower()
                
        if(genre == 'files'):
            spf = self.pw_contain(fold_path, rtrn='files')
        elif(genre == 'folders'):     
            spf = self.pw_contain(fold_path, rtrn='folders') 
        else:
            spf = self.pw_contain(fold_path)

        if(obj_name in spf):
            return True
        else:
            return False            
        

    def match(self, fragment, fold_path, genre='files', sort='str'):
        '''
        Description : Searches an input directory for any object containing a specific string

        Input :

            fragment : [string], string to be matched 
            fold_path : [string], pathway of folder in which 'obj_name' is searched
            genre     : [string] (Default : 'all'), type of object to be searched for 
            sort: [string] (Default : 'str'), corrosponding to a python data-type 

        Output : [Bool], success         
        ''' 
 
        if(sort == 'list' or sort == 'arr'):
            fold_path = self.pw_convert(fold_path)
        
        if(isinstance(genre,str) and isinstance(sort,str)):
            genre = genre.lower()
            sort = sort.lower()
                
        if(genre == 'files'):
            spf = self.pw_contain(fold_path, rtrn='files')
        elif(genre == 'folders'):     
            spf = self.pw_contain(fold_path, rtrn='folders') 
        else:
            spf = self.pw_contain(fold_path)
              
        for i in spf:
            if(fragment in i):
                match_list.append(i)
        return match_list
        
        
    def __fancy_print__(self,col=False):
        '''
        Description : Stylized printing of path information

        Input : 

            col : [Bool], color option for distinguishing folders from files

        Output : [Bool], success 
        '''
        if(col):
            blue = '\033[38;5;4m'
            black = '\033[38;5;0m'
            if(self.var_os == 'unix' or self.var_os == 'linux'):
                black = '\033[38;5;2m'
        else:
            blue,black=('','')
        
        nl = '\n'
        atsp = '   '
        headln = nl+'The current pathway is: '+nl
        bodyln = nl+'The content of the current directory is as follows: '+nl 
        
        print(headln)
        print(atsp+self.var_path)
        
        try: 
            spc = self.var_path_contain
            spf = self.var_path_files
        
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

    
    def __run_fancy_print__(self):
        if(self.var_path_print):
            try:
                ecrive = self.__fancy_print__(self.var_col)         
                return ecrive
            except:
                return False
        else:                        
            return True   
        
            
    def __fancy_print_list__(self,array):

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

        'pwd'  : Returns current directory pathway as string; equivalent to 'self.var_path'

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

        def head_check():                  
            if(len(self.var_path_list) == 1):
                if(self.var_path_print):                        
                    print("Warning: No remaining parent directories left")
                return True
            else:
                return False

        def print_func(test):
            success = True
            if(test):
                ptest = self.__run_fancy_print__()
                if(not ptest):
                    success = False 
                    print("Error: An unknown error was raised while attempting to print...")
            else:
                print("Error: Failure while updating current path")
                success = False
            return success
            

        def updater(new_path, sort, success, value):
            utest = self.__update_path__(new_path, sort)                 
            success = print_func(utest)
            result = (success,value)
            return result

                
        def cmd_pwd(tup):
            success = True
            cmd_inst, file_list, dest_str = tup
                        
            try:
                value = self.var_path 
            except: 
                value = None
                success = False
                print("Error: current (path) directory pathway not found")

            success = print_func(success)               
            result = (success,value)                                       
            return result
            
             
        def cmd_ls(tup):
            success = True
            cmd_inst, file_list, dest_str = tup 

            try:
                value = self.var_path_contain
            except:
                value = None 
                success = False
                print("Error: current (path) directory contents not found")

            success = print_func(success)            
            result = (success,value)
            return result
            
             
        def cmd_dir(tup):
            success = True            
            cmd_inst, file_list, dest_str = tup
                   
            new_file_list = []
                                       
            for i in file_list:
                verify = self.find(i, self.var_path)
                if(verify):
                    new_file_list.append(self.pw_join(self.var_path,i))
                else:
                    success = False
                    print("Warning Error: file name, '"+i+"' not found in current (path) directory")
            
            value = new_file_list

            if(self.var_path_print):
                ptest_1 = self.__run_fancy_print__()                
                print("Pathway string(s): " )
                ptest_2 = self.__fancy_print_list__(new_file_list)
                if(not ptest_1 or not ptest_2):
                    success = False
                    print("Error: An unknown error was raised while attempting to print...")
            
            result = (success,value)                
            return result
             
                     
        def cmd_cd(tup):
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup
                                    
            if(dest_str == '..'):                  
                if(head_check()):
                    result = (success,value)
                    return result 
                else:
                    up_path_list = list(self.var_path_list)[:-1]                 
                result = updater(up_path_list,'list',success,value)
                return result
            
            elif(dest_str in self.var_path_contain):
                dest_loc = self.pw_join(self.var_path,dest_str)
                if(os.path.isdir(dest_loc)): 
                    new_path_list = list(self.var_path_list)
                    new_path_list.append(dest_str)
                else:
                    success = False 
                    print("Error: '"+dest_loc+"not a valid folder in current (path) directory")
                    print("It appears that '"+dest_loc+"' is a file object or is corrupted")    
                    result = (success,value)
                    return result 
                result = updater(new_path_list,'list',success,value)
                return result
            
            elif(dest_str[0] == '/' or dest_str[0] == '\\'):
                ndir_inst = dest_str[1:]
                ctest = self.__climb_path__(ndir_inst,'update')
                success = print_func(ctest)  
                result = (success,value)
                return result
                    
            elif(dest_str == '~'):                
                ctest = self.__climb_path__(self.var_path_head,'update')
                success = print_func(ctest)  
                result = (success,value)
                return result
                
            else:
                print("Error: '"+dest_str+"' not a valid destination")
                success = False
            
            result = (success,value)
            return result
            
            
        def cmd_chdir(tup):
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 
            
            try: 
                utest = self.__update_path__(dest_str,'str')
                success = print_func(utest)              
            except:
                print('Error: pathway '+dest_str+' could not be reached')
                success = False 
            
            result = (success,value)
            return result 
            
                
        def cmd_mv(tup):
            
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup      
             
            mv_file_list = file_list 
            
            for i in range(len(mv_file_list)):
                mv_file_list[i] = self.pw_join(self.var_path,mv_file_list[i])
                         
            # Move File                                     
            if(dest_str == '..'):                  
                if(head_check()):
                    result = (success,value)
                    return result  
                else:
                    up_path_list = list(self.var_path_list)[:-1]

                up_path_str = self.pw_convert(up_path_list)   
                up_path_has = self.pw_contain(up_path_str)
                for i in mv_file_list: 
                    if(i in up_path_has):
                        print("Warning: '"+i+"' already exists in the namespace of the target directory, no action taken")
                        continue                     
                    mtest = self.move(i,up_path_str)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")

                result = updater(self.var_path_list,'list',success,value)
                return result     
            
            elif(dest_str in self.var_path_contain and dest_str not in self.var_path_files):                
                dest_path_list = list(self.var_path_list)
                dest_path_list.append(dest_str)  
                     
                path_str = self.pw_convert(dest_path_list)   
                path_has = self.pw_contain(path_str)
                for i in mv_file_list:           
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue     
                    mtest = self.move(i,path_str)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.var_path_list,'list',success,value)
                return result  
            
            elif(dest_str[0] == '/' or dest_str[0] == '\\'):
                dest_str = dest_str[1:]
                dest_path_list = self.__climb_path__(dest_str,'list')

                path_str = self.pw_convert(dest_path_list)   
                path_has = self.pw_contain(path_str)
                for i in mv_file_list:   
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue            
                    mtest = self.move(i,dest_path_list,str,list)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.var_path_list,'list',success,value)
                return result  
                                      
            elif(dest_str == '~'):                
                dest_path_list = self.__climb_path__(self.var_path_head,'list')

                path_str = self.pw_convert(dest_path_list)   
                path_has = self.pw_contain(path_str)
                for i in mv_file_list:       
                    if(i in path_has):
                        print("Warning: '"+i+"' already exists in target directory, no action taken")
                        continue         
                    mtest = self.move(i,dest_path_list,str,list)
                    if(not mtest):
                        success = False 
                        print("Error: contents of this path: '"+i+"' could not be moved")
                                     
                result = updater(self.var_path_list,'list',success,value)
                return result  

            elif(dest_str not in self.var_path_contain and len(mv_file_list) == 1):  
                dest_str = self.pw_join(self.var_path,dest_str)           
                mtest = self.move(mv_file_list[0],dest_str,str,str)
                if(not mtest):
                    success = False 
                    print("Error: contents of this path: '"+i+"' could not be moved")                                 
                result = updater(self.var_path_list,'list',success,value)
                return result  
            
            else:
                print("Error: Invalid formatting; the input object(s) could not be moved...")
                return None                 
            
            
        def cmd_rm(tup):
                      
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 
            
            # Format
            
            for i in file_list:   
                if(i in self.var_path_files):
                    file_path_str = self.pw_join(self.var_path,i)
                    dtest = self.del_file(file_path_str, update = True)
                    if(not dtest):
                        success = False 
                        print("Error: contents of the path: '"+i+"' could not be deleted")
                else: 
                    print("Error: '"+i+"' not found within the current (path) directory")
            
            result = updater(self.var_path_list,'list',success,value)
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
                    old_inst = self.pw_join(self.var_path,i)
                    cp_inst = file_inst_list[0]+"_copy_"+str(inc)+"."+file_inst_list[1] 
                    while(cp_inst in path_has):
                        inc+=1
                        cp_inst = file_inst_list[0]+"_copy_"+str(inc)+"."+file_inst_list[1] 
                    ctest = self.copy_file(old_inst,path_str,cp_inst)
                    if(not ctest):
                        success = False 
                        print("Error: contents of the path: '"+str(i)+"' could not be copied")
                                                                    
                result = updater(self.var_path_list,'list',success,value)
                return result
                                
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 
          
            if(dest_str == '.'):

                result = __cp_help_func__(file_list, self.var_path) 
                return result                                  
                       
            elif(dest_str == '..'):                  

                if(head_check()):
                    result = (success,value)
                    return result 
                else:
                    up_path_list = list(self.var_path_list)[:-1]

                up_path_str = self.pw_convert(up_path_list)   
                result = __cp_help_func__(file_list, up_path_str)
                return result
            
            elif(dest_str in self.var_path_contain):
                path_str = self.pw_join(self.var_path,dest_str)  
                result = __cp_help_func__(file_list, path_str)
                return result
            
            elif(dest_str[0] == '/' or dest_str[0] == '\\'):
                ndir_inst = dest_str[1:]
                path_str = self.__climb_path__(ndir_inst,'str')
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(ndir_inst)+"' could not be found in the root pathway")
                    return (success,value)
                    
                result = __cp_help_func__(file_list, path_str)
                return result
                    
            elif(dest_str == '~'):           
                path_str = self.var_path_head 
                try:                   
                    path_has = self.pw_contain(path_str, rtrn = 'files')
                except:
                    print("Error: 'home' directory cannot be accessed")
                    return (False,None)
                    
                result = __cp_help_func__(file_list, path_str)
                return result
              
            else:
                print("Error: '"+str(dest_str)+"' not a valid destination")
                success = False            
            result = (success,value)
            return result 
            

        def cmd_mkdir(tup):
            
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup      
            
            for i in file_list:
                file_path_str = self.pw_join(self.var_path,i)
                ctest = self.create_dir(file_path_str)  
                if(not ctest):
                    success = False 
                    print("Error: contents of this path: '"+i+"' could not be moved")
                                     
            result = updater(self.var_path_list,'list',success,value)
            return result  

        
        def cmd_rmdir(tup):

            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup   
            
            for i in file_list: 
                if(i in self.var_path_contain):
                    file_path_str = self.pw_join(self.var_path,i)
                    output = self.del_dir(file_path_str)
                    if(output == False):
                        success = False

            result = updater(self.var_path_list,'list',success,value)
            return result        


        def cmd_cpdir(tup):                   

            def __cpdir_help_func__(file_list, path_str):  

                success = True
                value = None

                path_has = self.pw_contain(path_str, rtrn = 'folders')
                for i in file_list:                    
                    inc = 1
                    old_inst = self.pw_join(self.var_path,i)
                    cp_inst = i+"_copy"
                    while(cp_inst in path_has):
                        inc+=1
                        cp_inst = cp_inst + '_' + str(inc)
                    ctest = self.copy_dir(old_inst, path_str, new_fold_name = cp_inst)
                    if(not ctest):
                        success = False 
                        print("Error: contents of the path: '"+str(i)+"' could not be copied")
                                                                    
                result = updater(self.var_path_list,'list',success,value)
                return result

                             
            # cmd_cpdir MAIN   
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 
          
            if(dest_str == '.'):
                        
                result = __cpdir_help_func__(file_list, self.var_path) 
                return result                                  
                       
            elif(dest_str == '..'):                  

                if(head_check()):
                    result = (success,value)
                    return result 
                else:
                    up_path_list = list(self.var_path_list)[:-1]

                up_path_str = self.pw_convert(up_path_list)   
                result = __cpdir_help_func__(file_list, up_path_str)
                return result
            
            elif(dest_str in self.var_path_contain):
                path_str = self.pw_join(self.var_path,dest_str)  
                result = __cpdir_help_func__(file_list, path_str)
                return result
            
            elif(dest_str[0] == '/' or dest_str[0] == '\\'):
                ndir_inst = dest_str[1:]
                path_str = self.__climb_path__(ndir_inst,'str')
                if(path_str == False):
                    success = False
                    print("Error: the folder: '"+str(ndir_inst)+"' could not be found in the root pathway")
                    return (success,value)
                    
                result = __cpdir_help_func__(file_list, path_str)
                return result
                    
            elif(dest_str == '~'):           
                path_str = self.var_path_head                     
                result = __cpdir_help_func__(file_list, path_str)
                return result
              
            else:
                print("Error: '"+str(dest_str)+"' not a valid destination")
                success = False            
            result = (success,value)
            return result 
        
        
        def cmd_find(tup):

            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup   
            
            found_list = []
            for i in file_list:            
                ftest = self.find(i, self.var_path)
                found_list.append(ftest)

#            found_dict = {k: v for k, v in zip(file_list, found_list)}   
            found_dict = dict(zip(file_list,found_list))
                
            if(self.var_path_print):
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
            cmd_inst, file_list, dest_str = tup   
            
            match_list = []
            for i in file_list:
                gtest = self.match(self.var_path, i)
                match_list.append(gtest)

#            match_dict = {k: v for k, v in zip(file_list, match_list)} 
            match_dict = dict(zip(file_list,match_list))
             
            if(self.var_path_print):
                for i in file_list:
                    if(len(match_dict[i]) == 0):
                        print("No matches found for the string, '"+i+"' ")
                    else:
                        print("The following matches were found for the string, '"+i+"' :")
                        self.__fancy_print_list__(match_dict[i])
                        
            value = match_dict
            result = (success,value)                       
            return result           


        def cmd_vi(tup):

            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 

            if(len(file_list) > 1):
                    if(self.var_path_print):
                        print("Warning: Only one file can be grabbed at a time")         
                    value = None 
                    success = False
               
            file_name = file_list[0] 
            file_path_str = self.pw_join(self.var_path,file_name)            
                   
            if(file_name in self.var_path_files):
                try: 
                    value = iop.flat_file_grab(file_path_str)
                except:
                    if(self.var_path_print):
                        print("Error: Could not retrieve the contents of '"+file_name+"'")         
                    value = None 
                    success = False
            elif(file_name not in self.var_path_contain):
                try: 
                    value = iop.flat_file_write(file_path_str) 
                except:
                    if(self.var_path_print):
                        print("Error: The file '"+file_name+"' could not be opened")         
                    value = None 
                    success = False    
            else:
                if(self.var_path_print):
                    print("Error: '"+file_name+"' not a file found in current (path) directory")         
                value = None 
                success = False
                                 
            result = updater(self.var_path_list,'list',success,value)
            return result
                     
                            
        def cmd_help(tup):

            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 
            
            help_dict = self.documentation('help')
               
            if(dest_str == ''):
                if(self.var_path_print):
                    print('Below is a list of valid input commands:\n')
                    self.__fancy_print_list__(cd_list)
                    value = cd_list
                    help_text = "Place command name after 'help' for more info on that command"

            else:
                cmd_val = dest_str
                if(cmd_val in cd_list):
                    help_dict = self.documentation('help')
                    help_text = help_dict[cmd_val]
                else:
                    success = False
                    help_text = "Error: the command '"+cmd_val+"' not recognized"

            if(self.var_path_print):                   
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
            if(self.var_path_print):
                print("Warning: Input must be a properly formated string ")
                print("Warning: No action taken, see help for more info on proper 'cmd' formatting ")    
            return result     
        if(cmd_string == '' or cmd_string.isspace()):
            if(self.var_path_print):
                print("Warning: Input must be a properly formated string ")
                print("Warning: No action taken, see help for more info on proper 'cmd' formatting ")    
            return result    

        cmd_tuple = self.__cmd_input_parse__(cmd_string)   
        cmd_inst = cmd_tuple[0]        
                                
        if(cmd_inst == 'pwd'):               # print working directory 
            result = cmd_pwd(cmd_tuple)

        elif(cmd_inst == 'ls'):              # list (content of working directory)
            result = cmd_ls(cmd_tuple)        

        elif(cmd_inst == 'dir'):             # directory (pathway)
            result = cmd_dir(cmd_tuple)   
          
        elif(cmd_inst == 'cd'):              # change directory 
            result = cmd_cd(cmd_tuple)

        elif(cmd_inst == 'chdir'):           # change directory (with pathway)
            result = cmd_chdir(cmd_tuple)

        elif(cmd_inst == 'mv'):              # move and rename (files and directories)
            result = cmd_mv(cmd_tuple)  
 
        elif(cmd_inst == 'rm'):              # remove (files) 
            result = cmd_rm(cmd_tuple)      

        elif(cmd_inst == 'cp'):              # copy (files)
            result = cmd_cp(cmd_tuple)

        elif(cmd_inst == 'mkdir'):           # make directory 
            result = cmd_mkdir(cmd_tuple) 

        elif(cmd_inst == 'rmdir'):           # remove directory
            result = cmd_rmdir(cmd_tuple)

        elif(cmd_inst == 'cpdir'):           # copy directory 
            result = cmd_cpdir(cmd_tuple)          

        elif(cmd_inst == 'find'):            # find (exact file)
            result  = cmd_find(cmd_tuple)

        elif(cmd_inst == 'match'):           # match (file names) 
            result = cmd_match(cmd_tuple)

        elif(cmd_inst == 'vi'):              # visual interface (read text files)
            result = cmd_vi(cmd_tuple)

        elif(cmd_inst == 'help'):            # help (display)
            result = cmd_help(cmd_tuple)
              
        else:
            spc = '     '
            tup_str = str(cmd_tuple)
            print("Error: Input '"+cmd_string+"' not resolved")
            if(self.var_path_print):
                print("It appears that either 'cmd_string' was not recognized")
                print("or that, the operand with which it was combined was not properly parsed")
                print("Below is a summary of the output:")
                print("\n")
                print(spc+"'cmd_inst' = '"+cmd_inst+"'")
                print(spc+"'cmd_tuple' = '"+tup_str+"'") 
                print('\n')
            return result
         
        return result 