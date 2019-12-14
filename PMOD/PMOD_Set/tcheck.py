class tcheck:
    '''
    tcheck:

       tcheck(var=None)

    Description: A class for aiding with error checking through type assertion functions.
                 Each function returns either a None type or Bool type. 

    '''

    def __init__(self,var=None):
        
        self.var = var 
        self.type = type(self.var)
        
    def set_var(self,var):
        self.var = var 
        self.type = type(var)

    def str_test(self,var):
        str_inst = isinstance(var,str)
        return str_inst

    def name_return(self,name):

        if(name != None):
            type = self.str_test(name)
            if(type):
                var_name = name
            else:
                var_name = None 
        else:
            var_name = None

        return var_name 
    

    def numeric_test(self,var,name=None):
        int_inst = isinstance(var, int)
        float_inst = isinstance(var, float)
        long_inst = isinstance(var, long)

        numeric_bool = int_inst or float_inst or long_inst
        
        var_name = self.name_return(name)
        
        result = (numeric_bool,var_name)
        return result 
         
         
    def type_test(self,var,sort,name=None):             
        type_bool = isinstance(var, sort) 
        var_name = self.name_return(name)    
        result = (type_bool,var_name)
        return result 

    
    def fail_print(self,print_bool,result,correct_type='valid type.',func_name=''):
        if(print_bool):
            if(self.str_test(correct_type)):
                correct_type = correct_type 
            else:
                try:
                    correct_type = str(correct_type)
                except:
                    correct_type = correct_type
            success = result[0]
            name = result[1]
            if(not success and name != None):
                print("["+func_name+"]"+" TypeError: the variable '"+name+"' is not a "+correct_type)
                return False
            if(not success and name == None):
                print("["+func_name+"]"+" TypeError: input variable is not a "+correct_type)
                return False 
            return True            

             
    def type_test_print(self,var,sort,name=None,func_name='',print_bool=True):
        result = self.type_test(var,sort,name)
        test = self.fail_print(print_bool,result,sort,func_name)
        return test