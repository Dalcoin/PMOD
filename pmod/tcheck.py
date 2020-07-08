#!/usr/bin/env python
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

    imprimer:

        funcNameStr2list : converts 'funcName' object to list
        addFuncName : adds 'funcName' object to 'funcName'
        errPrint : prints error message
        arrayCheck : check if input object is python array (list or tuple), prints error message if not
        numCheck : check if input object is python numeric object (int, float or long), prints error message if not
        strCheck : check if input object is python string object, prints error message if not

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

    def __init__(self, space="    ", endline="\n", modName=None, failPrint=True):
        self.modName = modName

        if(isinstance(space, str)):
            self.space = space
            self.doubleSpace = space+space
        else:
            self.space = '    '
            self.doubleSpace = space+space

        if(isinstance(endline, str)):
            self.endline = endline
        else:
            self.endline = "\n"

        if(failPrint):
            self.failPrint = True
        else:
            self.failPrint = False

    def __kwarg__(self, kwarg):
        if(kwarg != None):
            return True
        else:
            return False

    def __funcName__(self, funcName):
        outString = ''
        if(isinstance(funcName,str)):
            outString = "["+funcName+"]"
        elif(isinstance(funcName,(list,tuple))):
            outString = ''
            for entry in funcName:
                outString = outString+"["+str(entry)+"]"
        else:
            return None
        outString = outString+" "
        if(isinstance(self.modName, str)):
            outString = "["+self.modName+"]"+outString
        return outString

    def update_funcName(self, function_name, **kwargs):

        if(not isinstance(function_name, str)):
            return kwargs

        if(kwargs.get("nonewFuncName")):
            if(kwargs.get('funcName') != None):
                kwargs["funcName"] = kwargs.get('funcName')
            else:
                kwargs["funcName"] = function_name
        else:
            newFuncName = printer.addFuncName(function_name, kwargs.get('funcName'))
            if(check.isArray(newFuncName)):
                kwargs["funcName"] = newFuncName
            else:
                kwargs["funcName"] = function_name

        if(kwargs.get("fullErrorPath")):
            kwargs["nonewFuncName"] = False
        else:
            kwargs["nonewFuncName"] = True
        return kwargs

    def setstop_funcName(self, inverse=False, **kwargs):

        if(not inverse):
            if(kwargs.get("nonewFuncName") == None):
                kwargs["nonewFuncName"] = True
        else:
            if(kwargs.get("nonewFuncName") == None):
                kwargs["nonewFuncName"] = False
        return kwargs


    def __stringParse__(self, msg, **kwargs):
        '''
        Description: Parses 'msg' input message(s) into string output

        kwarg list:

            failPrint : (bool)[True], determines if the output strings are printed (True) or not (False)

            space : (str)(bool)['    '], determines the string which appears at the beginning of the message,
                                         nothing is added for False

            endline : (bool)[False], determines if the endline character is added to the end of each string (True) or not (False)

            funcName : (str)(None)[None], determines the function id strings to be added to the beginning of each string (str),
                                          if None, or not a string then nothing is added

            heading : (str)(bool)[" Error"], determines the string to be added which identifies the message (str),
                                            if True, the string " 'Error'" is added, else if False, nothing is added

            varName : (str)(bool)[False], determines the string to be added which identifies a specific variable (str),
                                        if True, the string " 'variable'" is added, else if False, nothing is added

            lnum : (str)(int)(None)[None], determines the strings to be added for identifying the line for which the message
                                           applies (str)(int), if None then nothing is added

            blankLine : (bool)[True], determines if an extra blank line is to added between the heading and following lines
                                       if 'msg' input is an array of strings. The blank line is not added if False

            doubleSpace : (bool)[True], determines if an extra 'space' spacing string is to added to the beginning of each
                                        line if the 'msg' input is an array of strings. The spacing defaults to that which is
                                        determined by 'space' if False.

            finalSpace : (bool)[True],
        '''

        if(kwargs.get('failPrint') == None):
            failPrint = self.failPrint
        else:
            failPrint = kwargs.get('failPrint')

        newSpace = kwargs.get('space')
        if(isinstance(newSpace, str)):
            outString = newSpace
            doubleSpace = newSpace+newSpace 
        elif(newSpace == False):
            newSpace = ''
            outString = newSpace
            doubleSpace = newSpace+newSpace 
        else:
            newSpace = self.space
            outString = self.space
            doubleSpace = newSpace+newSpace 

        finalSpace = kwargs.get('finalSpace')
        if(finalSpace != False):
            finalSpace = True
        else:
            finalSpace = False

        endlineVal = ''
        if(isinstance(kwargs.get('endline'), str)):
            endlineAdd = True
            endlineVal = kwargs.get('endline')
        elif(kwargs.get('endline')):
            endlineAdd = True
            endlineVal = self.endline
        else:
            endlineAdd = False

        funcNameStr = self.__funcName__(kwargs.get('funcName'))
        if(isinstance(funcNameStr,str)):
            outString = outString+funcNameStr

        if(self.__kwarg__(kwargs.get('heading'))):
            if(isinstance(kwargs.get('heading'), str)):
                outString = outString+kwargs.get('heading')+":"
            elif(kwargs.get('heading') != False):
                outString = outString+"Error:"
            else:
                pass

        if(self.__kwarg__(kwargs.get('varName'))):
            if(isinstance(kwargs.get('varName'),str)):
                outString = outString+" '"+kwargs.get('varName')+"'"
            elif(kwargs.get('varName')):
                outString = outString+" 'variable'"
            else:
                pass

        lnum_kwarg = kwargs.get('lnum')
        if(isinstance(lnum_kwarg, int) or isinstance(lnum_kwarg, str)):
            outString = outString+" on line-num. "+str(kwargs.get('lnum'))+")"

        outStrings = []
        if(isinstance(msg, str)):
            outString = outString+" "+msg
            if(endlineAdd):
                outString = outString+endlineVal
        elif(isArray(msg)):

            if(len(msg) == 0):
                if(endlineAdd):
                    outString = outString+endlineVal
            elif(len(msg) == 1):
                if(endlineAdd):
                    outString = outString+" "+msg[0]+endlineVal
                else:
                    outString = outString+" "+msg[0]
            else:
                first = msg[0]
                rest = msg[1:]

                outString = outString+" "+first
                if(endlineAdd):
                    outString = outString+endlineVal
                outStrings.append(outString)

                if(kwargs.get('blankLine') != False):
                    if(endlineAdd):
                        outStrings.append(" "+endlineVal)
                    else:
                        outStrings.append(" ")

                if(kwargs.get('doubleSpace') != False):
                    startString = doubleSpace
                else:
                    startString = newSpace

                for entry in rest:
                    if(isinstance(entry, str)):
                        entryString = startString+entry
                    else:
                        continue

                    if(endlineAdd):
                        entryString = entryString+endlineVal
                    outStrings.append(entryString)
        else:
            return False

        if(failPrint):
            if(len(outStrings) > 0):
                for string in outStrings:
                    print(string)
                if(finalSpace):
                    print(" ")
                return outStrings
            else:
                print(outString)
                if(finalSpace):
                    print(" ")
                return outString
        else:
            if(outStrings > 0):
                return outStrings
            else:
                return outString

    def funcNameStr2list(self, funcNameStr):
        try:
            arr = [j[0] for j in filter(None, [filter(None,i.split('[')) for i in filter(None, funcNameStr.split(']'))])]
            return arr
        except:
            return False

    def addFuncName(self, newName, funcNameObj):
        if(isinstance(funcNameObj,str)):
            oldfn = self.funcNameStr2list(funcNameObj)
            if(oldfn == False):
                return False
        elif(isArray(funcNameObj)):
            oldfn = list(funcNameObj)
        else:
            return False

        if(isinstance(newName, str)):
            newfn = self.funcNameStr2list(newName)
            if(newfn == False):
                return False
        elif(isArray(newName)):
            newfn = newName
        else:
            return False

        for entry in newfn:
            oldfn.append(entry)
        return oldfn

    def errPrint(self, msg, **kwargs):
        if(not isinstance(kwargs.get('heading'), str)):
            kwargs['heading'] = "Error"
        outString = self.__stringParse__(msg, **kwargs)
        return outString


    def arrayCheck(self, var, **kwargs):
        isArray = isinstance(var,(list,tuple))

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = True

        if(isArray == False):
            printString = "should be an array (tuple or list), not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return isArray
        else:
            return isArray


    def numCheck(self, var, **kwargs):
        isNumeric = isinstance(var,(int,float,long))

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = True

        if(isNumeric == False):
            printString = "should be a numeric (int, float or long), not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return isNumeric
        else:
            return isNumeric


    def strCheck(self, var, **kwargs):
        isString = isinstance(var, str)

        if(not isinstance(kwargs.get('varName'), str)):
            kwargs['varName'] = True

        if(isString == False):
            printString = "should be a string, not: "+str(type(var))
            self.__stringParse__(printString, **kwargs)
            return isString
        else:
            return isString
