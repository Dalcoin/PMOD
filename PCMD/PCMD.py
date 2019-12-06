import os 
import sys
import shutil

class path_parse:
    
    '''
    path_parse(os_form,new_path,path_print,print_col)
    
    
    -----------
    | Inputs: |
    -----------
    
    new_path = None (by default)
    path_print = False (by default)
    os_form = 'Windows' or 'Linux' 
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
        
        spc = self.path_contain
        spf = self.path_files
        
        print(bodyln)
        for i in spc:
            if(i in spf):
                print(black+atsp+i)
            else:
                print(blue+atsp+i)
        print(black)
            
    
    def run_fancy_print(self):
        if(self.path_print):
            self.fancy_print(color)         
            return 1
        else:                        
            return 1   
        
            
    def fancy_print_list(self,array):

        nl = '\n'
        atsp = '   '
        
        for i in array:
            print(atsp+str(i))
        

    ####################################################    
    # cmd Function: String-to-Command Parsing Function #
    ####################################################
    
    def cmd(self,motion):
        
        '''
        -------
        | cmd |
        -------
        
        Input: 
        motion: a string, must be formated according to Linux command line.
        
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
        
        def cmd_ls():
            self.path_contain = os.listdir(self.path)
            if(self.path_print):
                self.fancy_print(color)
            return self.path_contain
        
        def cmd_dir(motion,nmot):

            file_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    file_inst = file_inst+motion[i+1]+' '
                else:
                    file_inst = file_inst+motion[i+1]  
            if('.' not in [j for j in file_inst]):
                print('Error: file name '+file_inst+'is missing type extension')
                return None     
                    
            verif = self.find_file(file_inst)
            if(verif):
                file_path_list = list(self.path_list)
                file_path_list.append(file_inst)
                file_path_ret = self.create_path(file_path_list)
            else:
                print('Error: '+file_inst+' not found in the current directory')
                file_path_ret = None
            
            if(self.path_print):
                atsp = '   '
                if(verif):
                    print('The path way for '+file_inst+' is shown below: ')
                    print(' ')
                    print(atsp+file_path_ret)
                else:
                    print('Error: No pathway to display')
            
            return file_path_ret
                   
        def cmd_pwd():
            if(self.path_print):
                self.fancy_print(color)
            return self.path            
        
        def cmd_cd(motion,nmot):
              
            # Format
            dir_inst = ''
            for i in range(nmot-1):
                if(i < nmot-2):
                    dir_inst = dir_inst+motion[i+1]+' '
                else:
                    dir_inst = dir_inst+motion[i+1]    
                       
            if(dir_inst == '..'):                  
                if(len(self.path_list) == 1):
                    if(self.path_print):                        
                        print("Stop: No remaining parent directories left")
                    return 1                
                new_path_list = list(self.path_list)[:-1]
                output = self.update_path(new_path_list,list)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output
                else:
                    print("Error: 'update_path' failed internal check")
                    return None
            
            elif(dir_inst in self.path_contain):
                motion_test = str(self.path)+delim+dir_inst
                if(os.path.isdir(motion_test)): 
                    new_path_list = list(self.path_list)
                    new_path_list.append(dir_inst)
                    output = self.update_path(new_path_list,list)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output
                else:
                    print("Error: 'update_path' failed internal check")
                    return None
            
            elif(dir_inst[0] == '/' or dir_inst[0] == '\\'):
                ndir_inst = dir_inst[1:]
                output = self.climb_path(ndir_inst,'update')
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output                                   
                else:
                    print("Error: Folder "+ndir_inst+" not found within root path")
                    return None
                    
            elif(dir_inst == '~'):                
                output = self.climb_path(self.path_head,'update')
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output                                   
                else:
                    print("Error: Internal conflict, home directory could not be accessed")
                    return None   
                
            else:
                print("Error: '"+dir_inst+"' is not a folder in (path) directory")
                return None   
            
            
        def cmd_chdir(motion,nmot):
            # Format
            dir_inst = ''
            for i in range(nmot-1):
                if(i < nmot-2):
                    dir_inst = dir_inst+motion[i+1]+' '
                else:
                    dir_inst = dir_inst+motion[i+1]   
            
            try: 
                output = self.update_path(dir_inst,str)
                if(bool(output)):
                    output = self.run_fancy_print()
                    return output                                   
                else:
                    print("Error: Internal conflict, new (path) directory could not be accessed")
                    return None                
            except:
                print('Error: pathway '+dir_inst+' not found')
                return None
            
                
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
        
        assert isinstance(motion,str), "Error: input must be a string, not a "+str(type(motion))
              
        cd_list = ['ls','dir','pwd','cd','chdir','mv','rm','mkdir',
                   'rmdir','find','grep','help']
                                                                       
        motion = motion.split(" ")
        nmot = len(motion)            
        cmd_inst = motion[0]
        
        assert cmd_inst in cd_list, "Error: command not recognized, "\
                                    "use 'help' to view available functions"
                    
        if(cmd_inst == 'ls'):
            value = cmd_ls()
            return value
        elif(cmd_inst == 'pwd'):
            value = cmd_pwd()
            return value        
        elif(cmd_inst == 'dir'):
            value = cmd_dir(motion,nmot)
            if(isinstance(value,str)):
                return value
            else:
                verif = None   
        elif(cmd_inst == 'cd'):
            verif = cmd_cd(motion,nmot)
        elif(cmd_inst == 'chdir'):
            verif = cmd_chdir(motion,nmot)
        elif(cmd_inst == 'mv'):    
            verif = cmd_mv(motion,nmot)
        elif(cmd_inst == 'rm'):
            verif = cmd_rm(motion,nmot)      
        elif(cmd_inst == 'mkdir'):
            verif = cmd_mkdir(motion,nmot) 
        elif(cmd_inst == 'rmdir'):
            verif = cmd_rmdir(motion,nmot)
        elif(cmd_inst == 'find'):
            value = cmd_find(motion,nmot)
            if(isinstance(value,bool)):
                return value
            else:
                verif = None
        elif(cmd_inst == 'grep'):
            value = cmd_grep(motion,nmot)
            if(isinstance(value,list)):
                return value
            else:
                verif = None
        elif(cmd_inst == 'help'):
            value = cmd_help(cd_list)
            return value
        else:
            print("Error: Input not resolved")
            return None
         
        if(verif == 1):
            return 1
        else:
            print('Error: Input not resolved')
            return None
              