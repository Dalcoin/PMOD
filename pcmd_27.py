import os 
import sys
import shutil

class path_parse:
    
    '''
    path_parse(new_path,path_print)
    
    Inputs:
    
    new_path = None (by default)
    path_print = False (by default)
    
    path_parse is a class to call commands within python scripts allowing 
    functionality in the image of Linux command-line inputs for file and folder
    functions. The main function in the class is 'cmd' : path_parse.cmd(). This 
    function allows commands to be passed which, return the contents of the current 
    stored directory string, change the current stored directory string, move files 
    between directories and delete files and directories. The class allows for 
    pathway information to be stored and returned as string objects. 
    '''
    
    def __init__(self,os_form,new_path=None,path_print=False):
        
        '''
        Inputs:
        os : 'Windows' or 'Linux'/'Unix'
        new_path = None (by default)
        path_print = False (by default)
        
        .path : A string of the path in which the script is run
        .path_list : A list of strings with values of the folders in .path
        .path_head : A string containing the primary directory
        .path_contain : A list of strings with values of the contents in .path
        .path_files : A list of string with values of the file names in .path
        '''
        
        global delim
        
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
        create_path(path_list)

        Does what the name suggests: creates a
        path string from the path_list input
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

    ####################################################    
    # cmd Function: String-to-Command Parsing Function #
    ####################################################
    
    def cmd(self,motion):
        
        '''
        .cmd(motion)
        
        Input: 
        motion: a string, must be formated according to Linux command line.
        
        Valid Commands: 
        
        'ls' : returns list of strings containing the contents of the present directory
        'cd' : moves into the directory input, note: input directory must be in current directory
               ('..' to move upwards)  
        'mv' : moves file from current directory into subdirectory
               (format note: 'mv file_path.file Directory_Name') [file extension must be included]
        'rm' : remove input file from current directory
        'mkdir' : make new directory with name equal to input string
        'rmdir' : delete current directory
               
        '''
        
        def cmd_ls():
            self.path_contain = os.listdir(self.path)
            if(self.path_print):
                print(self.path)
                print(self.path_contain)
            return 1
                   
        
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
                self.path_contain = os.listdir(self.path)
                self.path_files = self.get_files()                     
                     
                if(self.path_print):
                    print(self.path)
                    print(self.path_contain)            
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
                        print(self.path)
                        print(self.path_contain)   
                        return 1
                    else:
                        return 1
            else:
                print("Error: '"+dir_inst+"' is not a directory")
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
            
            print(move_down_assert)
            print(move_up_assert)
            
            if(move_down_assert):
                verif = self.move_file(file_inst,fold_inst)
                if(self.path_print):
                    print(self.path)
                    print(self.path_contain)
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
                    print(self.path)
                    print(self.path_contain)
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
                    print(self.path)
                    print(self.path_contain)
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
                print(self.path_contain)
            return 1          
        
        ##################
        # Function: Main #
        ##################
        
        assert isinstance(motion,str), "Error: input must be a string"
              
        cd_list = ['ls','cd','mv','rm','mkdir']
                                                                       
        motion = motion.split(" ")
        nmot = len(motion)            
        cmd_inst = motion[0]
        
        assert cmd_inst in cd_list, 'Error: command not recognized, \\
                                    use help() to view available functions'
                    
        if(cmd_inst == 'ls'):
            verif = cmd_ls()        
        elif(cmd_inst == 'cd'):
            verif = cmd_cd(motion,nmot)          
        elif(cmd_inst == 'mv'):    
            verif = cmd_mv(motion,nmot)
        elif(cmd_inst == 'rm'):
            verif = cmd_rm(motion,nmot)      
        elif(cmd_inst == 'mkdir'):
            verif = cmd_mkdir(motion,nmot) 
        else:
            print("Error: Input not resolved")
            return None
        
        if(verif == 1):
            return 1
        else:
            print('Error: Input not resolved')
            return None
              