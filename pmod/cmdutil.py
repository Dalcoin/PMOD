import os
import sys
import subprocess

import pmod.ioparse as iop
from pmod.cmdline import PathParse


# File Utility Functions
#
#def convert_endline(file, style='dos2unix', space='    '):
#
#    lines = iop.flat_file_read(file)
#    if(lines == False):
#        print("could not read input 'file' : "+str(file))
#        return False
#
#    if(style == 'dos2unix'):
#        end_Line = "\n"
#    elif(style == 'unix2dos'):
#        end_Line = "\r\n"
#    elif(style == None):
#        end_Line = ""
#    else:
#        print(space+"[convert_endline] Error: 'style' not reconginzed")
#        return False  
#     
#    out_Lines = [i.rstrip()+end_Line for i in lines]  
#    return out_Lines



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


    ############################################################33##
                                                                   #
    ### File Functions                                             #
                                                                   # 
    ############################################################33##

    # Changing the endline character of text files

    def endlineConvert(self, lines, style='dos2unix', **kwargs):

        kwargs = self.__update_funcNameHeader__("endlineConvert", **kwargs)

        if(self.__not_strarr_print__(lines, varID='lines', firstError=True, **kwargs)):
            return False

        if(style == 'dos2unix'):
            endLine = b"\n"
        elif(style == 'unix2dos'):
            endLine = b"\r\n"
        elif(style == None):
            endLine = ""
        else:
            return self.__err_print__("not reconginzed: use 'dos2unix' or 'unix2dos'", varID='style', **kwargs)

        out_Lines = [line.rstrip()+endLine for line in lines]
        return out_Lines


    def filesEndlineConvert(self, files, style='dos2unix', foldName=None, **kwargs):

        kwargs = self.__update_funcNameHeader__("filesEndlineConvert", **kwargs)

        # checking 'files' input for proper formatting
        if(isinstance(files,str)):
            files = [files]
        elif(isinstance(files, (list,tuple))):
            if(self.__not_strarr_print__(files, varID='files', firstError=True, **kwargs)):
                return False
        else:
            return self.__err_print__("type must be either string or list of strings: "+str(type(files)), varID='files', **kwargs)

        # checking 'style' variable
        if(style != None and not isinstance(style, str)):
            return self.__err_print__("must be either a string or None type : "+str(type(style)), varID='style', **kwargs)
        else:
            if(isinstance(style, str)):
                if(style not in ['dos2unix', 'unix2dos']):
                    self.__err_print__("must be either 'dos2unix' or 'unix2dos' if a string : '"+style+"'", varID='style', **kwargs)

        # actions based upon 'foldName' input
        if(foldName == None):
            for file in files:
                if(file in self.varPath_Files):
                    pathway = self.joinNode(self.varPath, file, **kwargs)
                    if(pathway == False):
                        self.__err_print__("could not be joined to the current pathway", varID=str(file), **kwargs)
                        continue
                    lines = iop.flat_file_read(pathway, **kwargs)
                    if(lines == False):
                        self.__err_print__("lines could not be joined to the current pathway", varID=str(file), **kwargs)
                        continue
                    newlines = self.endlineConvert(lines, style, **kwargs)
                    if(newlines == False):
                        self.__err_print__("endlines could not be converted", varID=str(file), **kwargs)
                        continue
                    success = iop.flat_file_write(pathway, add_list=newlines, ptype='wb', **kwargs)
                    if(success == False):
                        self.__err_print__("converted lines could not be rewritten to file", varID=str(file), **kwargs)
                        continue
            return True
        elif(foldName in self.varPath_Folders):
            fold_node = self.joinNode(self.varPath, foldName)
            if(fold_node == False):
                return self.__err_print__("could not be joined to current pathway", varID=str(foldName), **kwargs)
            fold_contents = self.contentPath(fold_node, objType='file')
            if(fold_contents == False):
                return self.__err_print__("content could not be retrieved", varID=str(foldName), **kwargs)

            for file in files:
                if(file in fold_contents):
                    pathway = self.joinNode(fold_node, file, **kwargs)
                    if(pathway == False):
                        self.__err_print__("could not be joined to the '"+fold_node+"' pathway", varID=str(file), **kwargs)
                        continue
                    lines = iop.flat_file_read(pathway, **kwargs)
                    if(lines == False):
                        self.__err_print__("lines could not be joined to the '"+fold_node+"' pathway", varID=str(file), **kwargs)
                        continue
                    newlines = self.endlineConvert(lines, style, **kwargs)
                    if(newlines == False):
                        self.__err_print__("endlines could not be converted", varID=str(file), **kwargs)
                        continue
                    success = iop.flat_file_write(pathway, add_list=newlines, ptype='wb', **kwargs)
                    if(success == False):
                        self.__err_print__("converted lines could not be rewritten to file", varID=str(file), **kwargs)
                        continue
            return True
        else:
            return self.__err_print__("not reconginzed: '"+str(foldName)+"'", varID='foldName', **kwargs)

    # Generating a complimentary string for file name

    def name_compliment(self, name, comp_dict, **kwargs):

        kwargs = self.__update_funcNameHeader__("name_compliment", **kwargs)

        if(self.__not_str_print__(name, varID='name', **kwargs)):
            return False

        if(not isinstance(comp_dict, dict)):
            return self.__err_print__("should be a dictionary type : "+str(type(comp_dict)), varID='comp_dict', **kwargs)

        name_compliments = []
        for entry in comp_dict:
            if(len(name.split(str(entry)))==2):
                add_val = str(comp_dict[entry])
                base_val = name.split(str(entry))
                if(base_val[0] == ''):
                    new_name = add_val+base_val[1]
                    base_id = (base_val[1],)
                else:
                    new_name = base_val[0]+add_val+base_val[1]
                    base_id = (base_val[0], base_val[1])
                name_compliments.append((new_name, base_id),)

        return name_compliments

    ############################################################33##
                                                                   #
    ### Directory Functions                                        #
                                                                   #
    ############################################################33##


    def clearDir(self, dirs, select='all', style=None, **kwargs):
        '''
        Notes:

            Action: Deletes the contents of a directory accessible from 
                    the current pathway. The directory is preserved in the 
                    process. 

            Variables:

                dirs : string, corresponding to a file name
                select : (string), narrows files to be deleted
                style : string or (None), selects objects to be deleted by name or file type

            Valid 'select' values:

                'all'
                'file'
                'files'
                'directory'
                'directories'
                'dir'
                'dirs'
                'folder'
                'folders'

        '''
        select_array = ['all']+self.dirNames+self.fileNames

        kwargs = self.__update_funcNameHeader__("clearDir", **kwargs)

        if(self.__not_str_print__(select, varID='select', **kwargs)):
            return False
        else:
            select = select.rstrip().lower()
            if(select not in select_array):
                errmsg = ["should be in a valid object name:", "Files : "+str(self.fileNames), "Directory : "+str(self.dirNames), "Both : 'all'"]
                return self.__err_print__(errmsg, varID='select', **kwargs)

        # dirs parsed as a array of string(s)
        if(self.strarrCheck(dirs, varName='dirs', heading='Warning', **kwargs)):
            pass
        elif(isinstance(dirs, str)):
            dirs = [dirs]
        else:
            return self.__err_print__("should be either a string or array of strings, not "+str(type(dirs)), varID='dirs', **kwargs)

        # delete items according to 'select'
        dirs_to_empty = []
        not_dirs = []
        for dir in dirs:
            if(dir in self.varPath_Folders):
                dirs_to_empty.append(dir)
            else:
                not_dirs.append(dir)

        if(len(not_dirs) > 0):
            self.__err_print__(["The following entries are not directories in the current pathway:"]+not_dirs, **kwargs)

        # Delete files from directories
        fail_dirs = []
        for dir in dirs_to_empty:
            dirPath = self.joinNode(self.varPath, dir, **kwargs)
            if(select == 'all'):
                if(isinstance(style, str)):
                    contents = self.contentPath(dirPath, **kwargs)
                    if(contents == False):
                        fail_dirs.append(dir)
                        continue
                    for obj in contents:
                        if(style in obj):
                            pass
                        else:
                            continue
                        objPath = self.joinNode(dirPath, obj, **kwargs)
                        if(objPath == False):
                            fail_dirs.append(dir+self.delim+obj)
                            continue
                        if(os.path.isfile(objPath)):
                            os.remove(objPath)
                        elif(os.path.isdir(objPath)):
                            shutil.rmtree(objPath)
                        else:
                            fail_dirs.append(dir+self.delim+obj)
                else:
                    success = self.delDir(dirPath, **kwargs)
                    if(success):
                        success = self.makeDir(dirPath, **kwargs)
                    if(not success):
                        fail_dirs.append(dir)
            elif(select in self.fileNames):
                contents = self.contentPath(dirPath, objType='file', **kwargs)
                if(contents == False):
                    fail_dirs.append(dir)
                    continue
                if(isinstance(style, str)):
                    for obj in contents:
                        if(style in obj):
                            pass
                        else:
                            continue
                        objPath = self.joinNode(dirPath, obj, **kwargs)
                        if(objPath == False):
                            fail_dirs.append(dir+self.delim+obj)
                            continue
                        success = self.delFile(objPath, **kwargs)
                        if(success == False):
                            fail_dirs.append(dir+self.delim+obj)
                else:
                    for obj in contents:
                        objPath = self.joinNode(dirPath, obj, **kwargs)
                        if(objPath == False):
                            fail_dirs.append(dir+self.delim+obj)
                            continue
                        success = self.delFile(objPath, **kwargs)
                        if(success == False):
                            fail_dirs.append(dir+self.delim+obj)
            elif(select in self.dirNames):
                contents = self.contentPath(dirPath, objType='dir', **kwargs)
                if(contents == False):
                    fail_dirs.append(dir)
                    continue
                if(isinstance(style, str)):
                    for obj in contents:
                        if(style in obj):
                            pass
                        else:
                            continue
                        objPath = self.joinNode(dirPath, obj, **kwargs)
                        if(objPath == False):
                            fail_dirs.append(dir+self.delim+obj)
                            continue
                        success = self.delDir(objPath, **kwargs)
                        if(success == False):
                            fail_dirs.append(dir+self.delim+obj)
                else:
                    for obj in contents:
                        objPath = self.joinNode(dirPath, obj, **kwargs)
                        if(objPath == False):
                            fail_dirs.append(dir+self.delim+obj)
                            continue
                        success = self.delDir(objPath, **kwargs)
                        if(success == False):
                            fail_dirs.append(dir+self.delim+obj)
        if(len(fail_dirs) > 0):
            errmsg = ["The following objects could not be cleared:"]+fail_dirs
            self.__err_print__(errmsg, **kwargs)
        return True

    # def transfer_folder_content():

    # def read_files_from_folder():
