import inspect
import intertools

import sys
import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def GetAttrs(object):
    return [getattr(object, name) for name in dir(object)]

def GetFuncs(object):
    return [member[0] for member in inspect.getmembers(object, predicate=inspect.ismethod)]

def RunFuncs(object, initialize, funcVals, ExcludeList = None):
    FuncList = GetFuncs(object)
    FuncList = FuncFilter(FuncList)
    object_inst = object(initialize)
    for func in FuncList:
        with stdoutIO() as output:
            exec("print(object_inst."+str(func)+"("+str(funcVals.get(func))+"))")
        print(func+" : "+str(output.getvalue()).strip())
    return None