import os 
import sys 
import subprocess

import ioparse as iop
from cmdline import path_parse as cmv

 
# File Utility Functions

def convert_Endline(file, style = 'dos2unix', space = '    '):
         
    lines = iop.flat_file_read(file) 
    if(lines == False):
        print("    [convert_Endline] Error: could not read input 'file' : "+str(file)) 
        return False       
     
    if(style == 'dos2unix'):
        end_Line = "\n"
    elif(style == 'unix2dos'):
        end_Line = "\r\n"
    elif(style == None):
        end_Line = ""
    else:
        print(space+"[convert_Endline] Error: 'style' not reconginzed")
        return False  
     
    out_Lines = [i.rstrip()+end_Line for i in lines]  
    return out_Lines
 


# Meta - CMDLine class 

class cmdutil(object):
      
    def __init__(self, system = "linux", initialize = True, cmd_Object = None,  debug = True):

        self.folder_Names = ['dir', 'dirs', 'directory', 'directories', 'folder', 'folders']
        self.file_Names = ['file', 'files']
         
        self._space = '    '          
        self._cml = None                  
        self._debug = None 

        self.system = system

        __errors__ = { 'initialize_Err' : False,
                       'cml_setter_Err' : False,
                       'cml_gen_Err'    : False,
                       'spc_setter_Err' : False,
                       'dbg_setter_Err' : False,
                      }     

        self.CML_SET = False 
        
            
        if(initialize):    

            if(debug):
                self.debug = True  

            if(cmd_Object != None):
                self.cml = cmd_Object         
            else:
                self.cml_Generate()
                 
            if(self.CML_SET):
                success, self.init_Path = self.cml.cmd("pwd") 
                self.init_Name = self.cml.var_path_list[-1]       

    @property
    def cml(self):
        return self._cml

    @cml.setter 
    def cml(self, cmd_Object):

        if(isinstance(self._cml,cmv)):
            self.CML_SET = True
            if(self.debug):   
                print(self.space+"[cml.setter] Warning: property variable 'cml' is already set and cannot be changed\n") 
            else:
                pass
        else:
            if(isinstance(cmd_Object,cmv)): 
                self._cml = cmd_Object    
                self.CML_SET = True            
            else:
                self.CML_SET = False
                if(self.debug):
                    print(self.space+"[cml.setter] Warning: 'cml' must be set to a 'cmdline.path_parse' object\n")                      
                else:
                    pass 


    def cml_Generate(self): 
         
        try: 
            self.cml = cmv(self.system)
        except:
            if(self.debug):
                print(self.space+"[cml_Generate] Error: could not create a local 'cmv' object\n") 
            return False
                 
        
    @property
    def space(self):
        return self._space

    @space.setter 
    def space(self, space_Value):
        if(isinstance(space_Value,str)):
            self._space = space_Value 
        else: 
            if(self.debug):
                print(self.space+"[cml_Generate] Error: 'space' must be a string\n")

    @property
    def debug(self):
        return self._debug

    @debug.setter 
    def debug(self, debug_Value):
        if(isinstance(debug_Value,bool)):
            self._debug = debug_Value 
        else: 
            self._debug = False                         
           
         
    ############################################################33##

      
    def __err_Func__(self, **errs):
        getter = True   
        for errType, err in errs.iteritems():
            getter = False  
            if(__errors__.get(errType,None) != None):
                __errors__[errType] = bool(err)       
                   
        if(getter):
            return __errors__ 
  
    ############################################################33##

    ############################################################33##

    ### CMD Functions 
      
    def pass_CMD(self, cmd):
     
        if(not self.CML_SET):
            if(self.debug):
                print(self.space+"[pass_CMD] Error: 'cml' (internal 'path_parse' class instance) not found")         
          
        success, value = self.cml.cmd(cmd) 
        
        if(success):
            return success, value
        else:
            if(self.debug):
                print(self.space+"[pass_CMD] Error: failure to excute input 'cmd': "+cmd)
            return success

    
    def enter_dir(self, fiche):

        if(not isinstance(fiche, str)):
            if(self.debug):
                print(self.space+"[empty_Folder] Error: 'fiche' must be a string\n")
            return False 

        if(fiche in self.cml.var_path_folders):
            success, value = self.cml.cmd("cd "+fiche)
            if(success == False):
                if(self.debug):
                    err_msg = "Error: 'fiche' was found in the current directory, but could not be accessed\n"
                    print(self.space+"[enter_dir] "+err_msg)
                return False
        else:
            if(self.debug):
                print(self.space+"[empty_Folder] Error: 'fiche' could not be found in the current directory\n")
            return False  
        return True


    def moveup_dir(self):

        if(len(self.cml.var_path_list) > 1):
            success, value = self.cml.cmd("cd ..")
            if(success == False):
                if(self.debug):
                    err_msg = "Error: could not move up the pathway\n"
                    print(self.space+"[moveup_dir] "+err_msg)
                return False
        return True


    ############################################################33##

    # File Functions

    def convert_Endline(self, file, style = 'dos2unix'):
             
        lines = iop.flat_file_read(file) 
        if(lines == False):
            if(self.debug):
                print(self.space+"[convert_Endline] Error: could not read input 'file' : "+str(file)) 
            return False       
         
        if(style == 'dos2unix'):
            end_Line = "\n"
        elif(style == 'unix2dos'):
            end_Line = "\r\n"
        elif(style == None):
            end_Line = ""
        else:
            if(self.debug):
                print(self.space+"[convert_Endline] Error: 'style' not reconginzed")
            return False  
         
        out_Lines = [line.rstrip()+end_Line for line in lines]  
        return out_Lines

 
  
    ############################################################33##

     
    def empty_Folder(self, fiche, select = 'all'):
        '''
        Notes: 
	    
            Action: Deletes the contents of a directory accessible from 
                    the current pathway. The directory is preserved in the 
                    process. 
          
            Variables:
	    
                fiche : string, corresponding to a file name
                select : string, narrows files to be deleted  
        '''
         

        if(not isinstance(select, str)):
            if(self.debug):
                print(self.space+"[empty_Folder] Error: 'select' must be a string\n")
            return False 
        else:
            select = select.lower()
             
        success = self.enter_dir(fiche)
        if(not success):
            return success
        
        if(select == 'all'):
            delete_List_Files = self.cml.var_path_files
            delete_List_Folders = self.cml.var_path_folders

            if(not isinstance(delete_List_Files, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_Folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir() 
                return False         
    
            for i,entry in enumerate(delete_List_Files):
                success, value = self.cml.cmd("rm "+entry)  
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_Folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")

            if(not isinstance(delete_List_Folders, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_Folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir() 
                return False                   
            for i,entry in enumerate(delete_List_Folders):
                success, value = self.cml.cmd("rmdir "+entry)  
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_Folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")
                          
        elif(select in file_Names):    
            delete_List = self.cml.var_path_files
            if(not isinstance(delete_List, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_Folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir() 
                return False                
            for i,entry in enumerate(delete_List):
                success, value = self.cml.cmd("rm "+entry)  
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_Folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")

        elif(select in folder_Names):    
            delete_List = self.cml.var_path_folders
            if(not isinstance(delete_List, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_Folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir() 
                return False                  
            for i,entry in enumerate(delete_List):
                success, value = self.cml.cmd("rmdir "+entry)  
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_Folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")
        else:
            if(self.debug):
                print(self.space+"[empty_Folder] Error: input 'select' not reconginzed\n")
            self.moveup_dir()
            return False    

        self.moveup_dir()            
        return True


     
    def convert_File_Endline(self, fileNames, foldName = None, style):

        # checking 'fileNames' input for proper formatting
        if(isinstance(fileNames,str)):
            fileNames = [fileNames]   
        elif(isinstance(fileNames,(list,tuple))):
            if(all([isinstance(entry,str) for entry in fileNames])):
                pass 
            else:
                if(self.debug):
                    print(self.space+"[convert_File_Endline] Error: all entries in 'fileNames' must be strings")
                else:
                    pass 
                return False      

        # actions based upon 'foldName' input
        if(foldName == None):
            for entry in fileNames:
                if(entry in self.cml.var_path_files):
                    success = self.convert_Endline(entry, style = style)  
        elif(foldName in self.var_path_folders):
            
            for entry in fileNames:
                if(entry in self.cml.var_path_files):
                    success = self.convert_Endline(entry, style = style)  
             




     
 