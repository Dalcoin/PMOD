import os 
import sys
import shutil

class path_parse:
    
    '''
    path_parse(os_form,new_path,path_print,print_col)
    
    
    -----------
    | Inputs: |
    -----------
    
    os_form = 'Windows' or 'Linux' 
    new_path = None (by default)
    path_print = False (by default)
    print_col = False (by default)
    
    ---------------
    | Description |
    ---------------
    
    path_parse is a class to call commands within python scripts allowing 
    functionality in the image of Linux command-line inputs for file and folder
    functions. The main function in the class is 'cmd' : path_parse.cmd(). This 
    function allows commands to be passed which, return the contents of the current 
    stored directory string, change the current stored directory string, move files 
    between directories and delete files and directories. The class allows for 
    pathway information to be stored and returned as string objects. 
    
    ------------------
    | Function List: |
    ------------------
    
    __init__(self,os_form,new_path=None,path_print=False,print_col=False)
    
    create_path(self,path_list) : Creates and returns a pathway string from a pathway list
    
    get_files(self,style = None) : Returns a list of strings corrosponding to the names
                                   of the files, whose names contains file extensions,
                                   in the current (path) directory, option for selection 
                                   by extension.

    move_file(self,file_name,new_location,upbool = False) : Moves 'file_name' to 'new_location', 
                                                            note that 'file_name' must be a file
                                                            with a file extension in the string
                                                            and 'new_location' must be a folder,
                                                            both must be in the current directory.
                                                            if 'upbool' is True, then the file is 
                                                            moved to the higher directory and the
                                                            location in 'new_location' is ignored.
    
    del_file(self,file_name) : Deletes file with a name equal
                               to 'file_name' in the current
                               (path) directory
    
    create_dir(self,dir_name) : Creates a folder with a name 
                                equal to 'dir_name' in the 
                                current (path) directory
    
    find_file(self,file_name) : Checks the current (path) directory for a file with 
                                'file_name' as its identifier. Returns boolean.

    grep_file(self,fragment) : Checks the current (path) directory for any file with
                               'fragment' in its name. The list of matching file names 
                               is returned in string format. 
                                 
    fancy_print(self,col=False) : Prints the current (path) directory pathway in a
                                  stylized format. 

    fancy_print_list(self,array) :  Prints a list, 'array', in a stylized format.
    
    '''
    
    def __init__(self,os_form,new_path=None,path_print=False,print_col=False):
        
        '''
        --------
        | init |
        --------
        
        Inputs:
        os : 'Windows' or 'Linux'/'Unix'
        new_path = None (by default)
        path_print = False (by default)
        print_col  = False (by default)
        
        .path : A string of the path in which the script is run
        .path_list : A list of strings with values of the directory hiearchy in .path
        .path_head : A string containing the primary (home) directory
        .path_contain : A list of strings with values of the contents of .path
        .path_files : A list of string with values of the file (names with file type) in .path   
        
        .os:  A string to specify the operating system, this determines the path file format 
        .col: True for color Escape code when printing, False by default
        
        '''
        
        global delim
        global color
        
        self.os = os_form
        os_list = ['Ubuntu','Xubutnu','Redhat','Debian','Fedora','MintOS']
        if(self.os in os_list):
            self.os = 'Linux'
        
        if(self.os == 'Windows'):
            delim = '\\'
        elif(self.os == 'Unix' or self.os == 'Linux'):
            delim = '/'
        else:
            delim = ':'
            
        self.col = print_col
        color = self.col
        
        if(new_path != None):            
            self.path = new_path
            if(self.os == 'Windows'):
                self.path_list = self.path.split(delim)
                self.path_head = self.path.split(delim)[0]
            else:
                self.path_list = self.path.split(delim)
                self.path_list = self.path_list[1:]
                self.path_head = self.path_list[0]
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            self.path_print = path_print
        else:
            self.path = os.getcwd()
            if(self.os == 'Windows'):
                self.path_list = self.path.split(delim)
                self.path_head = self.path.split(delim)[0]
            else:
                self.path_list = self.path.split(delim)
                self.path_list = self.path_list[1:]
                self.path_head = self.path_list[0]
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            self.path_print = path_print



    def cmd_input_parse(self,string):
        '''
        -------------------
        | cmd_input_parse |
        -------------------
        
        Inputs:

        string : a string, formatted for use in the .cmd() function 
         
        output:
         
        out_inst : a tuple formatted for parsing in the .cmd() function
        
        '''
    
        def combine_list_str(array,span,ignore=None,space=False):
            
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
    
        
        assert isinstance(string,str), "Error: input must be a string, not a "+str(type(string))
          
        cd_list = ['ls','dir','pwd','cd','chdir','mv','rm','mkdir',
                   'rmdir','find','grep','help','vi']
    
        single_command_list = ['ls', 'pwd', 'help'] 
        single_path_list_nogroup = ['cd','chdir','vi']
        single_path_list_group = ['rm','rmdir','mkdir','dir','find','grep']
        double_path_list = ['mv']
    
        mod_list = []
                                                                   
        string_list = string.split(" ")
        string_list = filter(lambda l: l != '',string_list)            
        cmd_inst = string_list[0]
        nstr = len(string_list)
    
        assert cmd_inst in cd_list, "Error: command not recognized, "\
                                    "use 'help' to view available functions"
        
        if(cmd_inst in single_command_list):
            out_inst = (cmd_inst,[],[])
            return out_inst
    
        if(cmd_inst in single_path_list_nogroup):               
            out_inst_str = combine_list_str(string_list,[1,'End'],space=True)
            if(cmd_inst != 'vi'):
                out_inst = (cmd_inst,[],[out_inst_str])
            else:
                out_inst = (cmd_inst,[out_inst_str],[])
            return out_inst                     
        
        if(cmd_inst in single_path_list_group):
            if(';' in string):
                inst_str = combine_list_str(string_list,[1,'End'],space=True)
                out_inst_list = inst_str.split(';')
                out_inst_list = filter(lambda l: l != '',out_inst_list)
                out_inst = (cmd_inst,out_inst_list,[])
                return out_inst
            else:
                out_inst_str = combine_list_str(string_list,[1,'End'],space=True)
                out_inst = (cmd_inst,[out_inst_str],[])
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
                    print("Error: The input spaceing created ambiguity for the indexer: '"+string+"'")
                    raise IndexError  
                
                return out_inst
                 
                

            
    def join_node(self,old_path,new_node):
        output = old_path+delim+new_node
        return output
            
        
    def create_path(self,path_list):        
        '''
        
        ---------------
        | create_path |
        ---------------
        
        Input: 
        
            'path_list': [list,tuple], A path-formatted list 
        
        Return:
         
            'out_path': [string], a path-formatted string
            
        Description: Formats a path-formatted list into a path-formatted string
        
        '''
        out_path = ''
        count = 0
        while('' in path_list):
            path_list.remove('')
        for i in path_list:
            if(count == 0):
                out_path = str(i) 
            else:
                out_path = out_path + delim + str(i)
            count+=1
        if(self.os == 'Unix' or self.os == 'Linux'):
            out_path = '/'+out_path
        return out_path            
        
        
    def get_files(self,style = None):
        '''
        -------------
        | get_files |
        -------------
        
        Input: 
        
            'style': [string], (default value: None), A string corrosponding to 
                                                      a file extension type.
        
        Return:
         
            'file_list': [list], A list of strings corrosponding to all the files
                                 in the current (path) directory matching the 
                                 'style' extension, if 'style' == None, then all
                                 file names are included in 'file_list'
            
        Description: Returns a list of strings corrosponding to the file names in 
                     the current (path) directory, option for selecting only a 
                     specific file extension. 
        
        '''
        current_folder_content = self.path_contain
        file_list = []
        if(style == None):
            for i in current_folder_content:
                if('.' in i):
                    file_list.append(i)
        else:
            for i in current_folder_content:
                file_type = '.'+style
                if(file_type in i):
                    file_list.append(i)
        return file_list
    

    def update_path(self,path_updater,sort):        
        '''
        
        ---------------
        | update_path |
        ---------------
        
        Input: 
        
            'path_updater': [list,tuple], A path-formatted list ]
            'sort'        : [type]      , A python data-type
                    
        Description: Formats a path-formatted list into a path-formatted string
        
                
        '''
        if(sort == list):
            self.path_list = path_updater
            self.path = self.create_path(path_updater)
            if(self.os == 'Windows'):                    
                if(self.path == self.path_head):
                    self.path = self.path+'//'
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()   
            return 1
        elif(sort == str):
            self.path = path_updater
            self.path_list = self.path.split(delim)
            if(self.os == 'Windows'):                    
                if(self.path == self.path_head):
                    self.path = self.path+'//'
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files() 
            return 1
        else:
            print("Error: 'sort' not a valid type")
            return None 
        
        
    def climb_path(self,up_dir_inst,exit):
        if(up_dir_inst in self.path_list):
            spl_copy = list(self.path_list)
            new_path_list = []
            switch = True
            for i in spl_copy:
                if(i != up_dir_inst and switch == True):
                    new_path_list.append(i)
                else:
                    switch = False
            new_path_list.append(up_dir_inst)
            if(exit == 'list'):
                output = new_path_list
                return output
            elif(exit == 'str'):
                output = self.create_path(new_path_list)
                return output
            elif(exit == 'update'):                
                output = self.update_path(new_path_list,list)
                return output
            else:
                print("Error: 'exit' command: '"+str(exit)+"' not recongized")
        else: 
            print("Error: Directory "+up_dir_inst+" not found in current (path) hierarchy")
            return None
        
    
    def get_ctnt(self,path,sort = str,rtrn = 'all'):
        
        if(sort == str):
            new_path = path
        elif(sort == list):
            new_path = self.create_path(path)
        else:
            print("Error: 'sort' option must be either 'str' or 'list'; '"
                  +str(sort)+"' is invalid")
        
        content = os.listdir(new_path)
        
        if(rtrn == 'all'):
            return content
        elif(rtrn == 'files'):
            files = []
            for i in content: 
                if('.' in i): files.append(i)
            return files
        elif(rtrn == 'folders'):
            folders = []
            for i in content: 
                if('.' not in i): folders.append(i)
            return folders            
        else:
            print("Error: 'rtrn' input; '"+rtrn+"' , not valid")
            
             
    
    def move_file(self,file_loc,fold_loc,file_sort,fold_sort):
        
        if(fold_sort == list):
            fold_loc = self.create_path(fold_loc)                
        if(file_sort == list):
            file_loc = self.create_path(file_loc)
                      
        if(self.os == 'Windows'):                    
            if(fold_sort == self.path_head):
                fold_sort = fold_sort+'//'
                   
        try: 
            shutil.move(file_loc,fold_loc) 
        except: 
            raise OSError
            print("Error: File could not be moved.")
        
        output = self.update_path(self.path,str)
        return output

    
    def del_file(self,file_loc,update):           
        try:
            os.remove(file_loc)
        except:
            raise OSError
            
        if(update):            
            output = self.update_path(self.path,str)
        else:
            output = 1
            
        if(output):
            return 1
        else:
            print('Error: current (path) directory information could not be updated')
            return None
        
    def del_all_ctnt(self,fold_loc,warn=False):
        
        if(not os.path.isdir(fold_loc)):
            print("Error: "+fold_loc+" is not a valid directory")
            return None
        
        content = self.get_ctnt(fold_loc)
        
        for i in content:
            file_path = self.join_node(fold_loc,i)
            if(os.path.isdir(file_path)):
                verif = self.del_all_ctnt(file_path)                
            else:                
                verif = self.del_file(file_path,False)
        verif = os.rmdir(fold_loc)
        return 1
            
        
                        
    def create_dir(self,in_dir,dir_name):
        pathway = in_dir
        dir_pathway = pathway+delim+dir_name
        try:
            os.mkdir(dir_pathway)
            output = self.update_path(self.path,str)
            return output           
        except:           
            raise OSError        
            return None  
                
    def find_file(self,file_name):
        spf = self.path_files
        if(file_name in spf):
            return True
        else:
            return False
        
    def grep_file(self,fragment):
        spf = self.path_files
        grep_list = []
        for i in spf:
            if(fragment in i):
                grep_list.append(i)
        return grep_list
        
        
    def fancy_print(self,col=False):
        
        if(col):
            blue = '\033[38;5;4m'
            black = '\033[38;5;0m'
            if(self.os == 'Unix' or self.os == 'Linux'):
                black = '\033[38;5;2m'
        else:
            blue,black=('','')
        
        nl = '\n'
        atsp = '   '
        headln = nl+'The current pathway is: '+nl
        bodyln = nl+'The content of the current directory is as follows: '+nl 
        
        print(headln)
        print(atsp+self.path)
        
        try: 
            spc = self.path_contain
            spf = self.path_files
        
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

    
    def run_fancy_print(self):
        if(self.path_print):
            try:
                ecrive = self.fancy_print(color)         
                return True
            except:
                return False
        else:                        
            return True   
        
            
    def fancy_print_list(self,array):

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
        'pwd'  : Returns current directory pathway as string; equivalent to 'self.path'
        'cd' : moves into the input directory, note: input directory must be in current directory
               ('..' to move upwards) ('\\' or '/' to specify directory in root directory)
               ('~' moves to home directory)
        'chdir' : moves to the directory input, input must be full directory pathway 
        'mv' : moves file from current directory into subdirectory
               (format note: 'mv file_path.file Directory_Name') [file extension must be included]
        'rm' : remove input file from current directory
        'mkdir' : make new directory with name equalivalent to input string
        'rmdir' : delete subdirectory (equiv. to 'rm -rf Directory_Name')
        'find' : Searches the current directory for the input file string and returns boolean
        'grep' : Searches the current directory for the input pattern and returns list of matches
        'help' : Returns list of valid commands
        
        '''

        def cmd_pwd():
            success = True
            cmd_inst, file_list, dest_str = tup
                        
            try:
                value = self.path 
            except: 
                value = None
                success = False
                print("Error: current (path) directory pathway not found")

            ptest = self.run_fancy_print()
            if(not ptest):
                success = False
                print("Error: An unknown error was raised while attempting to print...")
               
            result = (success,value)                                       
            return result
            
             
        def cmd_ls(tup):
            success = True
            cmd_inst, file_list, dest_str = tup 

            try:
               value = self.path_contain
            except:
               value = None 
               success = False
               print("Error: current (path) directory contents not found")

            ptest = self.run_fancy_print()
            if(not ptest):
                success = False
                print("Error: An unknown error was raised while attempting to print...")
            
            result = (success,value)
            return result
            
             
        def cmd_dir(tup):
            success = True            
            cmd_inst, file_list, dest_str = tup

            nlist = len(file_list)
            new_file_list = []

            for i in file_list:
                verify = self.find_file(i)
                if(verify):
                    new_file_list.append(self.join_node(self.path,i))
                else:
                    success = False
                    print("Warning Error: file name, '"+i+"' not found in current (path) directory"
            
            value = new_file_list

            if(self.path_print):
                ptest_1 = self.fancy_print()                
                print("Pathway string(s): " )
                ptest_2 = self.fancy_print_list(new_file_list)
                if(not ptest_1 and not ptest_2):
                    success = False
                    print("Error: An unknown error was raised while attempting to print...")
            
            result = (success,value)                
            return result
             
                     
        def cmd_cd(motion,nmot):
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup
                                    
            if(dest_str == '..'):                  
                if(len(self.path_list) == 1):
                    if(self.path_print):                        
                        print("Warning: No remaining parent directories left")
                    result = (success,value)
                    return result 
               
                up_path_list = list(self.path_list)[:-1]
                utest = self.update_path(up_path_list,list)
                if(utest):
                    ptest = self.run_fancy_print()
                    if(not ptest):
                       success = False 
                       print("Error: An unknown error was raised while attempting to print...")
                else:
                    print("Error: Failed while updating current path")
                    success = False
                result = (success,value)
                return result
            
            elif(dest_str in self.path_contain):
                dest_loc = self.join_node(self.path,dest_str)
                if(os.path.isdir(dest_loc)): 
                    new_path_list = list(self.path_list)
                    new_path_list.append(dir_inst)
                    utest = self.update_path(new_path_list,list)
                else:
                    success = False 
                    print("Error: '"+dest_loc+"not a valid folder in current (path) directory")
                    print("It appears that '"+dest_loc+"' is a file object or is corrupted")    
                    result = (success,value)
                    return result 

                if(utest):
                    ptest = self.run_fancy_print()
                    if(not ptest):
                       success = False 
                       print("Error: An unknown error was raised while attempting to print...")
                else:
                    print("Error: Unknown failure while updating current path")
                    success = False
                result = (success,value)
                return result
            
            elif(dest_str[0] == '/' or dest_str[0] == '\\'):
                ndir_inst = dest_str[1:]
                ctest = self.climb_path(ndir_inst,'update')
                if(ctest):
                    ptest = self.run_fancy_print()
                    if(not ptest):
                       success = False 
                       print("Error: An unknown error was raised while attempting to print.")                                  
                else:
                    success = False 
                    print("Error: An unknown error while attempting to climb the current path.")
                result = (success,value)
                return result
                    
            elif(dest_str == '~'):                
                ctest = self.climb_path(self.path_head,'update')
                if(ctest):
                    ptest = self.run_fancy_print()
                    if(not ptest):
                       success = False 
                       print("Error: An unknown error was raised while attempting to print.")                                  
                else:
                    success = False 
                    print("Error: An unknown error while attempting to climb the current path.")  
                result = (success,value)
                return result
                
            else:
                print("Error: '"+dir_inst+"' not a valid destination")
                success = False
            
            result = (success,value)
            return result
            
            
        def cmd_chdir(motion,nmot):
            success = True            
            value = None
            cmd_inst, file_list, dest_str = tup 
            
            try: 
                utest = self.update_path(dir_inst,str)
                if(utest):
                    ptest = self.run_fancy_print()
                    if(not ptest):
                       success = False 
                       print("Error: An unknown error was raised while attempting to print.")                                
                else:
                    success = False
                    print("Error: Unknown failure while updating current path")               
            except:
                print('Error: pathway '+dir_inst+' could not be reached')
                success = False 
            
            result = (success,value)
            return result 
            
                
        def cmd_mv(motion,nmot):
            
            point_guard = True            
            file_inst = ''
            fold_inst = ''            
             
            # Format 
            for i in range(nmot-1):
                if(point_guard):
                    if('.' not in [j for j in motion[i+1]]):
                        file_inst = file_inst+motion[i+1]+' ' 
                    else:
                        point_guard = False
                        file_inst = file_inst+motion[i+1]                                              
                else:
                    if(i < nmot-2):
                        fold_inst = fold_inst+motion[i+1]+' '
                    else:
                        fold_inst = fold_inst+motion[i+1]  
            if('.' not in file_inst):
                print('Error: '+file_inst+' is missing type extension')
                return None 
            
            # Move File
            file_inst = str(self.path)+delim+file_inst
                                                              
            if(fold_inst == '..'):
                if(len(self.path_list) == 1):
                    if(self.path_print):                        
                        print("Stop: No remaining parent directories left")
                    return 1 
                dest_path_list = list(self.path_list)[:-1]
                output = self.move_file(file_inst,dest_path_list,str,list)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output                                   
                else:
                    print("Error: Internal conflict, new (path) directory could not be accessed")
                    return None      
            
            elif(fold_inst in self.path_contain):                
                dest_path_list = list(self.path_list)
                dest_path_list.append(fold_inst)                
                output = self.move_file(file_inst,dest_path_list,str,list)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output
                else:
                    print("Error: 'update_path' failed internal check")
                    return None 
            
            elif(fold_inst[0] == '/' or fold_inst[0] == '\\'):
                ndir_inst = dir_inst[1:]
                dest_path_list = self.climb_path(ndir_inst,'list')
                output = self.move_file(file_inst,dest_path_list,str,list)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output                                   
                else:
                    print("Error: Internal conflict, "+ndir_inst+" could not be accessed")
                    return None
                      
            elif(fold_inst == '~'):                
                dest_path_list = self.climb_path(self.path_head,'list')
                output = self.move_file(file_inst,dest_path_list,str,list)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output                                   
                else:
                    print("Error: Internal conflict, home directory could not be accessed")
                    return None  
            
            else:
                print("Error: The file couldn't be moved...")
                return None                 
            
            
        def cmd_rm(motion,nmot):
            
            file_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    file_inst = file_inst+motion[i+1]+' '
                else:
                    file_inst = file_inst+motion[i+1]
            if('.' not in [j for j in file_inst]):
                print('Error: '+file_inst+' is missing type extension')
                return None     
             
            if(file_inst in self.path_files):
                file_path_list = list(self.path_list)
                file_path_list.append(file_inst)
                file_path_str = self.create_path(file_path_list)
                output = self.del_file(file_path_str,True)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output
                else:
                    print("Error: 'del_file' failed internal check")
                    return None
            else:
                print("Error: file "+file_inst+" not found in current (path) directory")
            

        def cmd_mkdir(motion,nmot):
            
            fold_inst = ''
            
            # Format 
            for i in range(nmot-1):                
                if(i < nmot-2):
                    fold_inst = fold_inst+motion[i+1]+' '
                else:
                    fold_inst = fold_inst+motion[i+1]     
            
            verif = self.create_dir(self.path,fold_inst)  
            if(verif):                
                if(self.path_print):
                    self.fancy_print(color)
            return verif          
        
        
        def cmd_find(motion,nmot):

            file_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    file_inst = file_inst+motion[i+1]+' '
                else:
                    file_inst = file_inst+motion[i+1]
            if('.' not in [j for j in file_inst]):
                print('Error: '+file_inst+' is missing type extension')
                return None     
            
            verif = self.find_file(file_inst)
            if(self.path_print):
                if(verif):
                    print("The file '"+file_inst+"' has been found in the current directory!")
                else:
                    print("No file named '"+file_inst+"' found in current directory.")
            return verif
        
        
        def cmd_rmdir(motion,nmot):
            
            fold_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    fold_inst = fold_inst+motion[i+1]+' '
                else:
                    fold_inst = fold_inst+motion[i+1]    
             
            if(fold_inst in self.path_contain):
                fold_inst = self.join_node(str(self.path),fold_inst)
                output = self.del_all_ctnt(fold_inst)
                if(bool(output)):
                    output = self.update_path(self.path_list,list)
                    output = self.run_fancy_print()
                    return output
                else:
                    print("Error: 'del_all_ctnt' failed internal check")
                    return None
            else:
                print("Error: file '"+fold_inst+"' not found in current (path) directory")
                return None    
        
        
        def cmd_grep(motion,nmot):

            file_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    file_inst = file_inst+motion[i+1]+' '
                else:
                    file_inst = file_inst+motion[i+1]  
            
            verif = self.grep_file(file_inst)
            if(self.path_print):
                if(len(verif) == 0):
                    print("Match string '"+file_inst+"' does not"+ 
                          "match any files in path directory")
                else:
                    print("Match string '"+file_inst+"' found in the following files:\n")
                    self.fancy_print_list(verif)                          
            return verif        
        
        
        def cmd_help(cd_list):
            if(self.path_print):
                print('Below is a list of valid input commands:\n')
                self.fancy_print_list(cd_list)
            return cd_list
                
            
        ##################
        # Function: Main #
        ##################

        fail_tup = (False,None)
        cmd_tuple = cmd_input_parse(self,cmd_string,checker=False)   
        cmd_inst = cmd_tuple        

        result = fail_tup                    

        if(cmd_inst == 'ls'):
            result = cmd_ls(cmd_tuple)

        elif(cmd_inst == 'pwd'):
            result = cmd_pwd(cmd_tuple)        

        elif(cmd_inst == 'dir'):
            result = cmd_dir(cmd_tuple)   

        elif(cmd_inst == 'cd'):
            result = cmd_cd(cmd_tuple)

        elif(cmd_inst == 'chdir'):
            result = cmd_chdir(cmd_tuple)

        elif(cmd_inst == 'mv'):    
            result = cmd_mv(cmd_tuple)

        elif(cmd_inst == 'rm'):
            result = cmd_rm(cmd_tuple)      

        elif(cmd_inst == 'mkdir'):
            result = cmd_mkdir(cmd_tuple) 

        elif(cmd_inst == 'rmdir'):
            result = cmd_rmdir(cmd_tuple)

        elif(cmd_inst == 'find'):
            result  = cmd_find(cmd_tuple)

        elif(cmd_inst == 'grep'):
            result = cmd_grep(cmd_tuple)

        elif(cmd_inst == 'help'):
            result = cmd_help(cmd_tuple)

        else:
            spc = '     '
            print("Error: Input '"+cmd_string+"' not resolved")
            print("It appears that either 'cmd_string' was not recognized"
            print("Or that, the operand with which it was combined was not properly parsed")
            print("Below is a summary of the output:")
            print("\n")
            print(spc+"'cmd_inst' = '"+cmd_inst+"'")
            print(spc+"'cmd_tuple' = '"+str(cmd_tuple)+"'") 
            print('\n')
            return fail_tup

        (success,value) = result
        if(checker):
            if(success):
                print("cmd evaluation was successful!")
                if(value != None):
                   print("The returned value is: "+str(value))
            else:
                print("cmd evaluation failed...")
                if(value != None):
                   print("The returned value is: "+str(value))                

        return result 
              