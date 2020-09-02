import os 
import sys 
import subprocess

import pmod.ioparse as iop
from pmod.cmdline import PathParse


# File Utility Functions

def convert_endline(file, style = 'dos2unix', space = '    '):

    lines = iop.flat_file_read(file)
    if(lines == False):
        print("    [convert_endline] Error: could not read input 'file' : "+str(file))
        return False

    if(style == 'dos2unix'):
        end_Line = "\n"
    elif(style == 'unix2dos'):
        end_Line = "\r\n"
    elif(style == None):
        end_Line = ""
    else:
        print(space+"[convert_endline] Error: 'style' not reconginzed")
        return False  
     
    out_Lines = [i.rstrip()+end_Line for i in lines]  
    return out_Lines
 


class cmdUtil(PathParse):
      
    def __init__(self,
                 osFormat,
                 newPath=None,
                 rename=False,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    ',
                 endline='\n',
                 moduleNameOverride="cmdUtil",
                 **kwargs):

        super(cmdUtil, self).__init__(osFormat,
                                      newPath,
                                      rename,
                                      debug,
                                      shellPrint,
                                      colourPrint,
                                      space,
                                      endline,
                                      moduleNameOverride,
                                      **kwargs)

    ############################################################33##


    ### CMD Functions

    ### File Functions

    def convert_endline(self, lines, style='dos2unix', **kwargs):
        if(self.__not_strarr_print__(lines, varID='lines', firstError=True, **pkwargs)):
            return False

        if(style == 'dos2unix'):
            end_Line = "\n"
        elif(style == 'unix2dos'):
            end_Line = "\r\n"
        elif(style == None):
            end_Line = ""
        else:
            return self.__err_print__("not reconginzed: use 'dos2unix' or 'unix2dos'", varID='style', **kwargs)

        out_Lines = [line.rstrip()+end_Line for line in lines]  
        return out_Lines


    ############################################################33##


    def empty_folder(self, dir, select='all'):
        '''
        Notes: 

            Action: Deletes the contents of a directory accessible from 
                    the current pathway. The directory is preserved in the 
                    process. 
          
            Variables:
	    
                dir : string, corresponding to a file name
                select : string, narrows files to be deleted  
        '''

        if(not isinstance(select, str)):
            if(self.debug):
                print(self.space+"[empty_folder] Error: 'select' must be a string\n")
            return False 
        else:
            select = select.lower()
             
        success = self.enter_dir(fiche)
        if(not success):
            return success

        if(select == 'all'):
            delete_List_Files = self.cml.varPath_Files
            delete_List_Folders = self.cml.varPath_Folders

            if(not isinstance(delete_List_Files, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir()
                return False
            for i,entry in enumerate(delete_List_Files):
                success, value = self.cml.cmd("rm "+entry)
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")

            if(not isinstance(delete_List_Folders, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir()
                return False
            for i,entry in enumerate(delete_List_Folders):
                success, value = self.cml.cmd("rmdir "+entry)
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")

        elif(select in file_Names):
            delete_List = self.cml.var_path_files
            if(not isinstance(delete_List, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir() 
                return False                
            for i,entry in enumerate(delete_List):
                success, value = self.cml.cmd("rm "+entry)  
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")

        elif(select in folder_Names):    
            delete_List = self.cml.var_path_folders
            if(not isinstance(delete_List, (list,tuple))):
                if(self.debug):
                    print(self.space+"[empty_folder] Error: could not retrieve a list of files to delete\n")
                self.moveup_dir()
                return False
            for i,entry in enumerate(delete_List):
                success, value = self.cml.cmd("rmdir "+entry)
                if(success == False):
                    if(self.debug):
                        print(self.space+"[empty_folder] Error: file entry "+str(i)+" in delete list couldn't be deleted\n")
        else:
            if(self.debug):
                print(self.space+"[empty_folder] Error: input 'select' not reconginzed\n")
            self.moveup_dir()
            return False

        self.moveup_dir()
        return True


    def convert_file_endline(self, fileNames, style='dos2unix', foldName=None, **kwargs):

        # checking 'fileNames' input for proper formatting
        if(isinstance(fileNames,str)):
            fileNames = [fileNames]
        elif(isinstance(fileNames, (list,tuple))):
            if(self.__not_strarr_print__(fileNames, firstError=True, **kwargs)):
                return False
        else:
            return self.__err_print__("type must be either string or list of strings: "+str(type(fileNames)), varID='fileNames', **kwargs)

        # actions based upon 'foldName' input
        if(foldName == None):
            for entry in fileNames:
                if(entry in self.varPath_Files):
                    pathway = self.joinNode(self.varPath, entry, **kwargs)
                    if(pathway == False):
                        self.__err_print__("could not be joined to the current pathway", varID=str(entry), **kwargs)
                        continue
                    lines = iop.flat_file_read(pathway, **kwargs)
                    if(lines == False):
                        self.__err_print__("lines could not be joined to the current pathway", varID=str(entry), **kwargs)
                        continue
                    newlines = self.convert_endline(lines, style, **kwargs)
                    if(newlines == False):
                        self.__err_print__("endlines could not be converted", varID=str(entry), **kwargs)
                        continue
                    success = iop.flat_file_write(pathway, add_list=newlines, **kwargs)
                    if(success == False):
                        self.__err_print__("converted lines could not be written to file", varID=str(entry), **kwargs)
                        continue
            return True
        elif(foldName in self.varPath_Folders):
            fold_node = self.cml.joinNode(self.varPath, foldName)
            if(fold_node == False):
                return self.__err_print__("could not be joined to current pathway", varID=str(foldName), **kwargs)
            fold_contents = self.contentPath(fold_node, objType='file')
            if(fold_contents == False):
                return self.__err_print__("content could not be retrieved", varID=str(foldName), **kwargs)

            for entry in fileNames:
                if(entry in fold_contents):
                    pathway = self.joinNode(fold_node, entry, **kwargs)
                    if(pathway == False):
                        self.__err_print__("could not be joined to the '"+fold_node+"' pathway", varID=str(entry), **kwargs)
                        continue
                    lines = iop.flat_file_read(pathway, **kwargs)
                    if(lines == False):
                        self.__err_print__("lines could not be joined to the '"+fold_node+"' pathway", varID=str(entry), **kwargs)
                        continue
                    newlines = self.convert_endline(lines, style, **kwargs)
                    if(newlines == False):
                        self.__err_print__("endlines could not be converted", varID=str(entry), **kwargs)
                        continue
                    success = iop.flat_file_write(pathway, add_list=newlines, **kwargs)
                    if(success == False):
                        self.__err_print__("converted lines could not be rewritten to file", varID=str(entry), **kwargs)
                        continue
            return True
        else:
            return self.__err_print__("not reconginzed: "+str(foldName), varID='foldName', **kwargs)
