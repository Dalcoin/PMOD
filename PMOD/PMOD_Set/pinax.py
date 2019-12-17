#import tcheck #enable for tcheck functionality

class pinax:

    def __init__(self, table = None, eprint = False):
#        global check #enable for tcheck functionality
        self.table = table
        self.shape = (len(table),len(table[0]))
        self.eprint = oprint

#        check = tcheck.tcheck() #enable for tcheck functionality

    def func_eprint(self, msg):
        if(self.eprint):
            print(msg)
        return False

    def func_type_test(self,var,sort,err_msg):
        test = type_test(var,sort)
        if(not test):
            if(self.eprint):
                print(err_msg)
            return False
        else:
            return True

    def get_shape(self, table):
        shape = False
        n = len(table)
        m = len(table[-1])
        for i in table[:-1]:            
            if(len(i) != m):
                err = self.func_eprint("[get_shape] Error: Table does not have a rectangular shape")
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
                

    def trans_table(self, n, coerce_rect=False, check_table=False):

        if(check_table):
            shape = self.get_shape(n)
            if(shape == False):
                err = self.func_eprint("[trans_table] Error: input is not a rectangular matrix")
                return err                

        nrow = len(n[0])
        new_matrix, new_row = [],[]
        
        if(coerce_rect):
            try:
                n = self.coerce_array_rect(n)
            except:
                err = self.func_eprint("[trans_table] Error: input could not be coerced into a rectangular matrix")
                return err
        
        try:           
            for k in range(nrow):
                for i in n:
                    new_row.append(i[k])
                new_matrix.append(new_row)
                new_row=[]
            return new_matrix
        except: 
            err = self.func_eprint("[trans_table] Error: input could not be cast into a translated matrix")
            return err           

    
    def table_str_list(self,line_list,sep=' ',sort=str):
        
        new_line_list = list(line_list)
        n = len(new_line_list)
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
                        fail=True
        return new_line_list     
    
    
    
    
    
    
    
    
    
    


