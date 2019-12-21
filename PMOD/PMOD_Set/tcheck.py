class check_mod:
    '''
    check_mod:

       check_mod(print_bool=True,var=None)

    Description: A class for aiding with error checking through type assertion functions.
                 Each function returns either a None type or Bool type. 

    '''

    def __init__(self,print_bool=True,var=None):
        
        self.var = var 
        self.type = type(self.var)
        self.print_bool = print_bool

    # Acting getter/setter functions
        
    def pass_var(self,var):
        self.var = var 
        self.type = type(var)

    def pass_print(self,write):
        if(isinstance(write,bool)):
            self.print_bool = write 

    def get_var_type(self):
        return self.type 
 
    def get_type_test(self,inst):
        return isinstance(self.var,inst)


    ### Type test functions:
    
    def numeric_test(self,var):
        int_inst = isinstance(var, int)
        float_inst = isinstance(var, float)
        long_inst = isinstance(var, long)

        numeric_bool = int_inst or float_inst or long_inst
        return numeric_bool

                       
    def array_test(self,var):
        list_inst = isinstance(var, list)
        tuple_inst = isinstance(var, tuple)                  
        array_bool = list_inst or tuple_inst
        return array_bool 
             
                   
    def __fail_print__(self, success, var_name=None, correct_type='valid type.', func_name=''):
        if(self.print_bool):
            if(isinstance(correct_type,str)):
                correct_type = correct_type 
            else:
                try:
                    correct_type = str(correct_type)
                except:
                    print("[__fail_print__] Error: 'correct_type' must be a string or type object")
                    return False
            if(not success and var_name != None):
                if(func_name == ''): 
                    print("TypeError: the variable '"+var_name+"' is not a "+correct_type)
                else:
                    print("["+func_name+"]"+" TypeError: the variable '"+var_name+"' is not a "+correct_type)
                return False
            if(not success and var_name == None):
                if(func_name == ''):
                    print("TypeError: input variable is not a "+correct_type)
                else:
                    print("["+func_name+"]"+" TypeError: input variable is not a "+correct_type)
                return False 
            return True          
 
    # Main functions 

    def type_test(self,var,sort):
     
        if(sort == None):
            type_bool = (var == sort)
        elif(isinstance(sort,type) or isinstance(sort,object)):        
            type_bool = isinstance(var, sort)
        elif(sort == 'num'):
            type_bool = self.numeric_test(var)  
        elif(sort == 'arr'):
            type_bool = self.array_test(var)
        else:
            type_bool = False        
        return type_bool 

             
    def type_test_print(self,var,sort,var_name=None,func_name=''):
        type_bool = self.type_test(var,sort)
        test = self.__fail_print__(type_bool, var_name, correct_type=str(sort), func_name=func_name)
        return test