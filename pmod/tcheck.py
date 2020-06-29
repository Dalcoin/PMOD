
'''
'tcheck' module:

*Stand-Alone

Description: A selection of functions for aiding with error checking
             by searching for TypeError, each function returns either
             a None type or Bool type or Str type for error message.

function list:

    isNumeric(obj)
    isArray(obj)
    isArrayFlat(obj)
    isType(var,sort)
    isType_print(var, sort, var_name=None, func_name='', print_bool=True)

    internal:

        __fail_print__(success, var_name=None, correct_type="valid type", func_name='', print_bool = True)

class list:

    imprimer

'''

### Tester functions: test input against a given object type or object format
    
def isNumeric(obj):
    '''
    Description: A 'numeric' type is defined as an object which evaluates to a python number

    obj: input, any python object
    '''    
    return isinstance(obj, (int, float, long))


def isArray(obj):
    '''
    Description: An array is defined as a iterable and numerically indexed object: lists and tuples

    obj: input, any python object
    '''
    return isinstance(obj, (list, tuple))


def isArrayFlat(obj): 
    '''
    Description: Tests an array for flatness (each object within the array has a dimensionality of zero)

    obj: input, any python object    
    ''' 
    if(isArray(obj)):
        for i in obj:
            try:
                n = len(i)
                if(isinstance(i,str)):
                    continue
                else:
                    return False
            except:
                continue
        return True
    else:
        return False

# Printing Functions: Help with printing

def __fail_print__(success, var_name=None, correct_type="valid type", func_name='', print_bool = True):
    '''
    Dunder printing function for internal error correction and checking
    '''
    if(print_bool):
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
    else:
        return None   

### Main functions 

def isType(var, sort):
    '''
    Description: This function returns a boolean, 'var' is tested for equivalence to 
                 'sort', 'sort' may a 'type' object.  

    Inputs:
    
        var  : input object 
        sort : sort is either a type, class object or module object against which 'var' is tested
                
    '''

    if(sort == None):
        type_bool = (var == sort)
    elif(sort == 'num'):
        type_bool = isNumeric(var)  
    elif(sort == 'arr'):
        type_bool = isArray(var)
    elif(isinstance(sort, type) or type(sort) == "<type 'classobj'>" or type(sort) == "<type 'module'>"):        
        type_bool = isinstance(var, sort)
    else:
        type_bool = False
    return type_bool 


def isType_print(var, sort, var_name=None, func_name='', print_bool=True):
    '''
    Description: This function returns a boolean, 'var' is tested for equivalence to
                 'sort', 'sort' may a 'type', 'classobj' or 'module' object. The main
                 difference between this function and 'isType' is that this function
                 is optimized for printing out error functions

    Inputs:

        'var'  : python object, input object
        'sort' : sort is either a type, class object or module object against which 'var' is tested
        'var_name' : string, The name of variable 'var', to be used when printing error messages.
        'func_name' : string,  The name of a function, to be used when printing error messages.
        'print_bool' : boolean, printing option, useful when printing to the console would interfere with threading

    '''
    type_bool = isType(var, sort)
    if(print_bool):
        test = __fail_print__(type_bool, var_name, correct_type=sort, func_name=func_name)
        return test
    else:
        return type_bool



class imprimer(object):

    def __init__(self, space='    ', endline=True):
        self.space = space
        self.endline = endline

    def __funcName__(self, funcName):
        if(isinstance(funcName,str)):
            outString = "["+funcName+"]"
            return outString
        elif(isinstance(funcName,(list,tuple))):
            outString = ''
            for entry in funcName:
                outString = outString+"["+str(entry)+"]"
            return outString
        else:
            return None

    def __stringParse__(self, msg, funcName=None, varName=None, warning=False, lnum=None, failPrint=True):

        outString = self.space

        funcNameStr = self.__funcName__(funcName)
        if(isinstance(funcNameStr,str)):
            outString = outString+funcNameStr

        if(warning):
            outString = outString+" Warning: "
        else:
            outString = outString+" Error: "

        if(isinstance(varName,str)):
            outString = outString+"'"+varName+"' "
        elif(varName):
            outString = outString+"'variable' "
        else:
            pass

        if(isinstance(lnum,(str,int))):
            outString = outString+" on line-num. "+str(lnum)+", "
        outString = outString+msg+"\n"

        if(failPrint):
            print(outString)
        return outString


    def errPrint(self, printmsg, funcName=None, varName=None, warning=False, lnum=None, failPrint=True):
        if(isinstance(printmsg, str)):
            outString = self.__stringParse__(printmsg, funcName, varName, warning, lnum, failPrint)
            return outString
        else:
            outString = self.space+"Print Error: Error occured, message unresolved\n"
            if(failPrint):
                print(outString)
            return outString


    def arrayCheck(self, var, funcName=None, varName=True, warning=False, lnum=None, failPrint=True):
        isArray = isinstance(var,(list,tuple))
        if(isArray == False and failPrint):
            printString = "should be an array (tuple or list), not: "+str(type(var))
            self.__stringParse__(printString, funcName, varName, warning, lnum, failPrint)
            return isArray
        else:
            return isArray


    def numCheck(self, var, funcName=None, varName=True, warning=False, lnum=None, failPrint=True):
        isArray = isinstance(var,(int,float,long))
        if(isArray == False and failPrint):
            printString = "should be a numeric (int, float or long), not: "+str(type(var))
            self.__stringParse__(printString, funcName, varName, warning, lnum, failPrint)
            return isArray
        else:
            return isArray


    def strCheck(self, var, funcName=None, varName=True, warning=False, lnum=None, failPrint=True):
        isArray = isinstance(var,(str))
        if(isArray == False and failPrint):
            printString = "should be a string, not: "+str(type(var))
            self.__stringParse__(printString, funcName, varName, warning, lnum, failPrint)
            return isArray
        else:
            return isArray

