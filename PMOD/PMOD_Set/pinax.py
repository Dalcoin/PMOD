import numpy
import pandas 

#import tcheck #enable for tcheck functionality
#check = tcheck.check_mod()

'''
Contains:

    class pinax
'''

class pinaxas:

    def __init__(self, table = None, eprint = False):
#        global check #alt. enable for tcheck functionality
#        check = tcheck.check_mod() #alt. enable for tcheck functionality

        self.table = table
        if(table != None):
            self.shape = (len(table),len(table[0]))
        self.eprint = eprint



    ####################                         #################### 
    # helper functions ########################### helper functions #
    ####################                         #################### 

        # functions which began with 'func_' are helper functions 
        # helper functions are not meant to be called outside of the pinax class      

    def __func_eprint__(self, msg):
        if(self.eprint):
            print(msg)
        return False

    ####################                         #################### 
    # action functions ########################### action functions #
    ####################                         #################### 

    # Action functions 
    # These functions are meant to be called on list arrays

    def array_to_str(array,offset='',spacing='  '):        
        out_str = ''
        if(not isinstance(array,list) and not isinstance(array,tuple)):
            self.__func_eprint__('[array_to_str] Error: input must be an array')
            return False
        for i in array:
            out_str = out_str+spacing+str(i)
        out_str = offset+out_str
        return out_str

    def get_shape(self, table):
        shape = False
        n = len(table)
        m = len(table[-1])
        for i in table[:-1]:            
            if(len(i) != m):
                err = self.__func_eprint__("[get_shape] Error: Table does not have a rectangular shape")
                return err
        shape = (n,m)
        return shape

    def coerce_array_rect(self, n):
        l = max(len(i) for i in n)    
        for i in n:
            if(len(i) < l):
                while(len(i) < l): 
                    i.append(None)
        return n
                
    ###################                           ################### 
    # table functions ############################# table functions #
    ###################                           ################### 

    # Table (pinax) functions 
    # These functions are the main function to be used on list arrays.

    # Format:
    #
    # The format for tables takes the following basic form: [[],[]]
    # 
    # Functions: 
    # 
    # table_trans  ([[1,2,3],[4,5,6]])  =>  [[1,4],[2,5],[3,6]]  

    
    def table_trans(self, n, coerce_rect=False, check_table=False):

        if(check_table):
            shape = self.get_shape(n)
            if(shape == False):
                err = self.__func_eprint__("[trans_table] Error: input is not a rectangular matrix")
                return err                

        nrow = len(n[0])
        new_matrix, new_row = [],[]
        
        if(coerce_rect):
            try:
                n = self.coerce_array_rect(n)
            except:
                err = self.__func_eprint__("[trans_table] Error: input could not be coerced into a rectangular matrix")
                return err
        
        try:           
            for k in range(nrow):
                for i in n:
                    new_row.append(i[k])
                new_matrix.append(new_row)
                new_row=[]
            return new_matrix
        except: 
            err = self.__func_eprint__("[trans_table] Error: input could not be cast into a translated matrix")
            return err           

    
    def table_numeric(self,line_list,sep=' ',header=False,sort=str):
        
        new_line_list = list(line_list)
        n = len(new_line_list)
        
        if(header):
            new_line_list = table_trans(new_line_list)
            new_line_list = new_line_list[1:-1]
            head = new_line_list[0]
            new_line_list = table_trans(new_line_list)
        
        for i in range(n):
            new_line_list[i] = new_line_list[i].split(sep)
            new_line_list[i] = filter(None,new_line_list[i])
            if(sort != str):
                for j in range(len(new_line_list[i])):
                    try:
                        if(sort == int or sort == long):
                            new_line_list[i][j] = sort(float(new_line_list[i][j]))
                        else:
                            new_line_list[i][j] = sort(new_line_list[i][j])
                    except:
                        success = False 
                        return success
        return new_line_list     
    
    
    def table_array_str(self, list_lines, split_str = '  ', row=True):
     
        lines = list(list_lines)
    
        for i in range(len(lines)):
            lines[i] = filter(None,lines[i].split(split_str))

        n = len(lines)
        for i in range(n):
            if(len(lines[i]) == 0):
                del lines[i]
                n=n-1
            if(len(lines[i]) == 1 and lines[i][0].isspace()):
                del lines[i]
                n=n-1     
           
        if(row):
            return lines 
        else:
            return self.table_trans(lines)
         
    
    
    
    
    
    
    


