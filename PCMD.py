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
        .path_list : A list of strings with values of the folders in .path
        .path_head : A string containing the primary directory
        .path_contain : A list of strings with values of the contents in .path
        .path_files : A list of string with values of the file names in .path   
        
        .os:  A string to specify the operating system path file format 
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
            self.path_list = new_path.split(delim)
            self.path_head = new_path.split(delim)[0]
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            self.path_print = path_print
        else:
            self.path = os.getcwd()
            self.path_list = self.path.split(delim)
            self.path_head = self.path.split(delim)[0]
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            self.path_print = path_print
            
            
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
    
    def move_file(self,file_name,new_location,upbool = False):
        
        if(upbool == True):
            file_pathway = self.path+delim+file_name
            fold_loc = new_location
            try: 
                shutil.move(file_pathway,fold_loc) 
            except: 
                raise OSError
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            return 1
            
        
        file_pathway = self.path+delim+file_name
        fold_loc = self.path+delim+new_location
        
        if(new_location in self.path_contain):
            try: 
                shutil.move(file_pathway,fold_loc) 
            except: 
                raise OSError
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            return 1
        else:
            return None
    
    def del_file(self,file_name):
        file_pathway = self.path+delim+file_name
        if(file_name in self.path_contain):            
            try:
                os.remove(file_pathway)
            except:
                raise OSError
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            return 1
        else:
            return None
                        
    def create_dir(self,dir_name):
        pathway = self.path
        dir_pathway = pathway+delim+dir_name
        try:
            os.mkdir(dir_pathway)
            self.path_contain = os.listdir(self.path)
            self.path_files = self.get_files()
            return 1           
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
        'cd' : moves into the directory input, note: input directory must be in current directory
               ('..' to move upwards)  
        'mv' : moves file from current directory into subdirectory
               (format note: 'mv file_path.file Directory_Name') [file extension must be included]
        'rm' : remove input file from current directory
        'mkdir' : make new directory with name equalivalent to input string
        'rmdir' : delete current directory
        'find' : Searches the current directory for the input file string and returns boolean
        'grep' : Searches the current directory for the input pattern and returns list of matches
        'pwd'  : Returns current directory pathway as string; equivalent to 'self.path'
        'help' : Returns list of valid commands
        
        '''
        
        def cmd_ls():
            self.path_contain = os.listdir(self.path)
            if(self.path_print):
                self.fancy_print(color)
            return self.path_contain
                   
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
                
                del self.path_list[-1]
                     
                self.path = self.create_path(self.path_list)
                self.path_split = self.path.split(delim)
                self.path_list = [i for i in self.path_split]
                if(self.path == 'C:'):
                    self.path = 'C://'
                self.path_contain = os.listdir(self.path)
                self.path_files = self.get_files()                     
                     
                if(self.path_print):
                    self.fancy_print(color)         
                    return 1
                else:                        
                    return 1
            
            elif(dir_inst in self.path_contain):
                motion_test = self.path+delim+dir_inst
                if(os.path.isdir(motion_test)):                
                    self.path_list.append(dir_inst)            
                    self.path = self.create_path(self.path_list)
                    self.path_split = self.path.split(delim)
                    self.path_list = [i for i in self.path_split]
                    self.path_contain = os.listdir(self.path)
                    self.path_files = self.get_files()
                    if(self.path_print):
                        self.fancy_print(color)
                        return 1
                    else:
                        return 1
            else:
                print("Error: '"+dir_inst+"' is not a folder in (path) directory")
                return None   
                    
                
        def cmd_mv(motion,nmot):
            
            point_guard = True
            file_inst = ''
            fold_inst = ''
            move_up = False
            
            if(motion[-1] == '..'):
                move_up = True
            
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
                print('Error: file name is missing type extension')
                return None 
            
            # Move File
            valid_file = file_inst in self.path_files
            valid_fold = fold_inst in self.path_contain
            move_down = not move_up
            move_down_assert = valid_file and valid_fold and move_down
            move_up_assert = valid_file and move_up
                        
            if(move_down_assert):
                verif = self.move_file(file_inst,fold_inst)
                if(self.path_print):
                    self.fancy_print(color)
                return 1
            elif(move_up_assert):
                if(len(self.path_list) == 1):
                    if(self.path_print):                        
                        print("Stop: No remaining parent directories left")
                    return 1
                
                current_path_list = self.path_list
                del current_path_list[-1]
                new_dir = self.create_path(current_path_list)
                
                upbool = True
                verif = self.move_file(file_inst,new_dir,upbool)
                self.path_contain = os.listdir(self.path)
                self.path_files = self.get_files()  
                if(self.path_print):
                    self.fancy_print(color)
                return 1                
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
                print('Error: file name is missing type extension')
                return None     
             
            if(file_inst in self.path_files):
                verif = self.del_file(file_inst) 
                if(self.path_print):
                    self.fancy_print(color)
                return 1     
            else:
                return None
            

        def cmd_mkdir(motion,nmot):
            
            # Format 
            for i in range(nmot-1):                
                if(i < nmot-2):
                    fold_inst = fold_inst+motion[i+1]+' '
                else:
                    fold_inst = fold_inst+motion[i+1]
            if('.' in file_inst):
                print('Error: folder name should not contain type extension')
                return None     
            
            verif = self.create_dir(fold_inst)            
            if(self.path_print):
                self.fancy_print(color)
            return 1          
        
        
        def cmd_find(motion,nmot):

            file_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    file_inst = file_inst+motion[i+1]+' '
                else:
                    file_inst = file_inst+motion[i+1]
            if('.' not in [j for j in file_inst]):
                print('Error: file name is missing type extension')
                return None     
            
            verif = self.find_file(file_inst)
            if(self.path_print):
                if(verif):
                    print("The file '"+file_inst+"' has been found in the current directory!")
                else:
                    print("No file named '"+file_inst+"' found in current directory.")
            return verif
        
        
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
        
        
        def cmd_dir(motion,nmot):

            file_inst = ''
            
            # Format
            for i in range(nmot-1):                
                if(i < nmot-2):
                    file_inst = file_inst+motion[i+1]+' '
                else:
                    file_inst = file_inst+motion[i+1]  
            if('.' not in [j for j in file_inst]):
                print('Error: file name is missing type extension')
                return None     
                    
            verif = self.find_file(file_inst)
            if(verif):
                file_path_list = list(self.path_list)
                file_path_list.append(file_inst)
                file_path_ret = self.create_path(file_path_list)
            else:
                print('Error: file not found in the current directory')
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
        
        def cmd_help(cd_list):
            if(self.path_print):
                print('Below is a list of valid input commands:\n')
                self.fancy_print_list(cd_list)
            return cd_list
                
            
        ##################
        # Function: Main #
        ##################
        
        assert isinstance(motion,str), "Error: input must be a string"
              
        cd_list = ['ls','dir','pwd','cd','mv','rm','mkdir','find','grep','help']
                                                                       
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
        elif(cmd_inst == 'mv'):    
            verif = cmd_mv(motion,nmot)
        elif(cmd_inst == 'rm'):
            verif = cmd_rm(motion,nmot)      
        elif(cmd_inst == 'mkdir'):
            verif = cmd_mkdir(motion,nmot) 
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