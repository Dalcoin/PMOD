import tcheck 

class ioparse:

    def __init__(self, file_in=None, file_out=None, pyver='27'):
        global check
        self.file_in = file_in 
        self.file_out = file_out
        
        self.pyver = pyver
         
        check = tcheck.tcheck()
         
        self.ptype_list = ['r','r+','rb','w','w+','wb','wb+','a','ab','a+','ab+']
        self.ptype_read = ['r','r+','rb']
        self.ptype_write = ['w','w+','wb','wb+','a','ab','a+','ab+']
              
    
    def set_file(self,file_in,file_out):
        self.file_in = file_in 
        self.file_out = file_out  

    def dup_check(self,array):
        '''If there is a duplicate in array-like object, True is returned, else False'''    
        s = set()
        for i in array:
            if i in s:
                return True
            else:
                s.add(i)         
        return False        


    def attempt_path_print(self,filepath):
        try:
            print("Given pathway: "+str(filepath))
        except:
            print("Pathway could not be parsed") 


    def io_opt_test(self, ptype,io,par=False,count_offset=False):
        
        success = True

        if(ptype not in self.ptype_list):
            success = False
            try:            
                print("[io_opt_test] Error: 'ptype', '"+str(ptype)+"' is not a valid 'ptype' option")
            except:
                print("[io_opt_test] Error: 'ptype', could not be parsed as a valid 'ptype' option string")   

        if(io == 'read'):
            if(ptype not in self.ptype_read):
                success = False                            
                print("[io_opt_test] Error: ptype, '"+str(ptype)+"' is not a valid read option")
        elif(io == 'write'):
            if(ptype not in self.ptype_write):   
                success = False                         
                print("[io_opt_test] Error: ptype, '"+str(ptype)+"' is not a valid write option")      
        else:
            success = False
            print("[io_opt_test] Error: option 'io' must be either 'read' or 'write'")
        
        test = check.type_test_print(par,bool,'par','io_opt_test') 
        if(not test):
            success = False 
             
        test = check.type_test_print(count_offset,bool,'count_offset','io_opt_test') 
        if(not test):
            success = False 
                  
        return success


    def grab_list_test(self, grab_list, change_list = None, n, m):

        test = check.type_test_print(grab_list,list,'grab_list','grab_list_test')
        if(not test):
            return False

        if(n>0):
            for i in range(n):
                test = check.type_test_print(grab_list[i],int,'grab_list['+str(i)+']','grab_list_test') 
                if(not test):
                    return False 

        if(repeat == False):
            test = self.dup_check(grab_list)
            if(test):
                print("[grab_list_test] Error: 'grab_list' values must be unique")
            return False

        if(change_list != None):
            if(len(grab_list) != len(change_list)):  
                print("[grab_list_test] Error: 'grab_list' and 'change_list' must have the same length")
                return False
		    
            for i in range(len(change_list)):
                test = check.type_test_print(change_list[i],str,'change_list['+str(i)+']','flat_file_replace') 
                if(not test):
                    return False
            
        if(n>m):
            print("[grab_list_test] Error: 'grab_list' is longer than the number of file lines")
            return False
        if(m < (max(grab_list)+1)):
            print("[grab_list_test] Error: replacement line number greater than the max number of files lines")
            return False
        
        return True


    def list_repeat(self,grab_list,file_lines,scrub):
        if(len(grab_list)<3):
            print("[list_repeat] Error: 'grab_list' must have at least 3 entries when 'repeat' is True"
            return False

        raw_lines = []          
        
        bnd = grab_list[0]+1
        saut = grab_list[1:-1]
        n = grab_list[-1]+1
        for i in range(n):
            for j in range(len(saut)):
                line_tag = saut[j]+bnd*i
                raw_lines.append(file_lines[line_tag])
                if(scrub):
                    raw_lines[j] = raw_input[i].strip("\n").strip("\r")         
        return raw_lines
  
    
    def flat_file_read(self,file_in,ptype='r'):
        '''
        flat_file_read(self,file_in,ptype='r')

        Description: Writes a list of strings (1 line per string) from an input file, various options for parsing
          
        (e.g.)
        flat_file_read('file.in',ptype='rb')   

        Variables:
        
        'file_in': file string pathway, if only a single node is given, current (path) directory is assumed
        'ptype': [*] a string in found in the self.ptype_read list.         

        Output: List of Strings; else Boolean if failure           
         
        '''    

        test = self.io_opt_test(ptype,'read')
        if(not test):
            return False            

        test = check.type_test_print(file_in,str,'file_in','flat_file_read') 
        if(not test):
            return False
      
        try:
            with open(file_in,ptype) as file_in:
                file_lines = file_in.readlines()
            return file_lines 
        except:
            print("[flat_file_read] Error: File could not be read")
            self.attempt_path_print(file_in)
            return False             
        

    def flat_file_write(self,file_out,add_list,par=False,ptype='w'):
        '''
        flat_file_write(self,file_out,add_list,ptype='w',par=False)

        Description: Writes a list of strings to an output file, various options for parsing

        (e.g.)
        flat_file_write('file.in',["This is the first line!","This is line #2!"])

        Variables:
        
        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed
        'add_list': list of strings, each string is a separate line, order denoted by the index. 
        'ptype': [*] a string in found in the self.ptype_write list.         
        'par': [*] True if endline character is to be added to each output string, else False. 

        Output: Boolean      

        ''' 

        # Testing proper variable types
        test = self.io_opt_test(ptype,'write',par=par)
        if(not test):
            return False         

        test = check.type_test_print(file_out,str,'file_out','flat_file_write') 
        if(not test):
            return False
        test = check.type_test_print(add_list,list,'add_list','flat_file_write') 
        if(not test):
            return False
        
        n=len(add_list)
        for i in range(n):
            test = check.type_test_print(add_list[i],str,'add_list['+str(i)+']','flat_file_write')
            if(not test):
                return False           
            
        # Print content to file   
        try: 
            with open(file_out,ptype) as fout:
                for i in add_list: 
                    if(par):
                        fout.write(i+"\n")
                    else:
                        fout.write(i) 
            return True 
        except: 
            print("[flat_file_write] Error: 'add_list' lines could not be printed to file")
            self.attempt_path_print(file_out)
            return False



    def flat_file_replace(self,file_out,grab_list,change_list,count_offset=True,par=True,ptype='w'):
        '''
        flat_file_replace(file_out,grab_list,change_list,par=True,count_offset=True,ptype='w')

        Description: In the file 'file_out', the lines in 'grab_list' are replaced with the strings in 'change_list'

        (e.g.)
        flat_file_replace('file.in',[1,2],["This is the first line!","This is line #2!"])

        Variables:
        
        'file_out': file string pathway, if only a single node is given, current (path) directory is assumed
        'grab_list': list of integers, each integer corrosponds to a line number, options for 0 or 1 index start 
        'change_list': list of strings, each string is a separate line
        'par': [*] True if endline character is to be added to each output string, else False. 
        'count_offset': [*] True if values in grab_list corrospond to line numbers, else values corrospond to list index
        'ptype': [*] a string in found in the self.ptype_write list.         

        Output: Boolean   
        '''
        
        # Testing proper variable types
        test = self.io_opt_test(ptype,io,par=par,count_offset=count_offset)
        if(not test):
            return False
        test = check.type_test_print(file_out,str,'file_out','flat_file_replace') 
        if(not test):
            return False

        if(count_offset):      
            grab_list = [x-1 for x in grab_list]

        # Read in file
        file_lines = self.flat_file_read(file_out)
        m = len(file_lines)   
        
        # Testing the lengths of variable arrays 
        n = len(grab_list)

        test = check.type_test_print(grab_list,list,'grab_list','flat_file_replace')
        if(not test):
            return False

        for i in range(len(grab_list)):
            test = check.type_test_print(grab_list[i],int,'grab_list['+str(i)+']','flat_file_replace') 
            if(not test):
                return False 
        for i in range(len(change_list)):
            test = check.type_test_print(change_list[i],str,'change_list['+str(i)+']','flat_file_replace') 
            if(not test):
                return False 

        test = self.dup_check(grab_list)
        if(test):
            print("[flat_file_replace] Error: 'grab_list' values must be unique")


        if(len(grab_list) != len(change_list)):  
            print("[flat_file_replace] Error: 'grab_list' and 'change_list' must have the same length")
            return False

        if(n>m):
            print("[flat_file_replace] Error: 'grab_list' is longer than the number of file lines")
            return False
        if(m < (max(grab_list)+1)):
            print("[flat_file_replace] Error: replacement line number greater than the max number of files lines")
            return False
            
        # Make modifications 
        for i in grab_list:
            j = grab_list.index(i)
            if(par):
                file_lines[i] = change_list[j]+"\n"
            else:
                file_lines[i] = change_list[j]
        
        # Print modifications to file 
        result = self.flat_file_write(file_out,file_lines,ptype=ptype)
        return result
        
        
    def flat_file_grab(file_in,grab_list,scrub=False,repeat=False,count_offset=True,ptype='w'):
                
        # Testing proper variable types
        test = self.io_opt_test(ptype,'read',count_offset=count_offset)
        if(not test):
            return False
        test = check.type_test_print(file_in,str,'file_in','flat_file_grab') 
        if(not test):
            return False

        if(count_offset):      
            grab_list = [x-1 for x in grab_list]
        n = len(grab_list)

        # Read in file
        file_lines = self.flat_file_read(file_in)
        if(n == 0):
            if(scrub == True):
                for i in range(len(file_lines)):
                    file_lines[i] = file_lines[i].strip('\n').strip('\r')
                return file_lines   
            else:
                return file_lines     
        m = len(file_lines)  
        
        # Testing the grab_list 
               
        test = self.grab_list_test(grab_list, n, m)
        if(not test):
            return False
        
        # parse file_lines through repeat options:
                
        out_lines = [] 
                                                             
        if(repeat):  
            out_lines = self.list_repeat(self,grab_list,file_lines,scrub)  
        else:                
            for i in range(n):
                out_lines.append(file_lines[grab_list[i]])     
                if(scrub == True):
                    out_lines[i] = out_lines[i].strip("\n").strip("\r")
        return out_lines                  
