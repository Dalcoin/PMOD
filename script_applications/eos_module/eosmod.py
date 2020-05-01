import ioparse as iop 
import strlist as strl
import pinax as px

# conversion functions

def kf2den(kf,gam):
    return gam*(kf*kf*kf)/(3.0*pi2)

def den2kf(den,gam):
    return pow((3.0*pi2*den/gam),1.0/3.0)


def convertFunc(value, convert, round_Value = None, debug = True, space = '    '):
    '''
    
    notes: possible convert option
            
        convert = 'sym2den'
        convert = 'asym2den'
        convert = 'den2sym'
        convert = 'den2asym'
        convert = 'sym2asym'
        convert = 'asym2sym'           

    '''
    
    listopt = False
    if(isinstance(convert,str)):
        convert = convert.lower()
    else:
        if(debug):
            print(space+"[convertFunc] Error: 'convert' must be a string")

    if(isinstance(value,(str,int,float,long))):
        try:
            value = float(value)
        except:
            if(debug):
                print(space+"[convertFunc] Error: input could not be coerced into a string\n")
            return False         
    elif(isinstance(value,(tuple,list))):
        try:
            value = [float(entry) for entry in value]
        except:
            if(debug):
                print(space+"[convertFunc] Error: input list could not be coerced into a list of floats\n")
            return False   
        listopt = True 
    else:
        if(debug):
            print(space+"[convertFunc] Error: input 'convert' not a recongnized conversion\n")    
        return False

    if(isinstance(round_Value,int)):
        rnd = True 
    else:
        rnd = False    
     
    if(convert == 'sym2den'):
        if(listopt):
            if(rnd):
                return [round(kf2den(entry,2.0),round_Value) for entry in value]
            else:
                return [kf2den(entry,2.0) for entry in value]        
        else:
            if(rnd):
                return round(kf2den(value,2.0),round_Value)
            else:
                return kf2den(value,2.0)

    elif(convert == 'asym2den'):
        if(listopt):
            if(rnd):
                return [round(kf2den(entry,1.0),round_Value) for entry in value]  
            else:
                return [kf2den(entry,1.0) for entry in value]
        else:
            if(rnd):
                return round(kf2den(value,1.0),round_Value)
            else:
                return kf2den(value,1.0)    

    elif(convert == 'den2sym'):
        if(listopt):
            if(rnd):
                return [round(den2kf(entry,2.0),round_Value) for entry in value]
            else:
                return [den2kf(entry,2.0) for entry in value]
        else:
            if(rnd):
                return round(den2kf(value,2.0),round_Value)
            else:
                return den2kf(value,2.0)

    elif(convert == 'den2asym'):
        if(listopt):
            if(rnd):
                return [round(den2kf(entry,1.0),round_Value) for entry in value]
            else:
                return [den2kf(entry,1.0) for entry in value]
        else:
            if(rnd):
                return round(den2kf(value,1.0),round_Value)
            else:
                return den2kf(value,1.0)  

    elif(convert == 'sym2asym'):
        if(listopt):
            if(rnd):
                return [round(pow(2,1.0/3.0)*entry,round_Value) for entry in value]
            else:
                return [pow(2,1.0/3.0)*entry for entry in value]
        else:
            if(rnd):
                return round(pow(2,1.0/3.0)*value)            
            else:
                return pow(2,1.0/3.0)*value

    elif(convert == 'asym2sym'):
        if(listopt):
            if(rnd):
                return [round(entry/pow(2,1.0/3.0),round_Value) for entry in value]
            else:
                return [entry/pow(2,1.0/3.0) for entry in value]  
        else:
            if(rnd):
                return round(value/pow(2,1.0/3.0),round_Value) 
            else:
                return value/pow(2,1.0/3.0) 

    else:
        if(debug):
            print(space+"[convertFunc] Error: 'convert' not a recongnized value")
        return False  


def file2Convert(fileName, style, header = False, newFile = None):
    '''

    notes: 

        fileName : the name of a eos file in the same directory as the script
        style    : see 'convert' function for possible options 
        header   : Set to True if there is a header, else keep as False 
        newFile  : if None, the original file will be overwritten with the EoS
                   if a string, a new file with a name equal to the string will be created and filled with the EoS
                   if True, a list of the strings corrosponding to the EoS will be returned. 
   '''

    lines = iop.flat_file_intable(fileName, header = header, entete=True)
    
    if(header): 
        modLines = convertFunc(lines[0][1:], convert = style, round_Value = 4)
        modLines.insert(0,lines[0][0])
    else:
        modLines = convertFunc(lines[0], convert = style, round_Value = 4) 
    
    lines[0] = modLines     
    newLines = px.table_trans(lines)      

    outLines = map(lambda x: strl.array_to_str(x,spc ='    ',endline=True), newLines)

    if(newFile == None):
        iop.flat_file_write(fileName,outLines)        
    elif(isinstance(newFile,str)):
        iop.flat_file_write(newFile,outLines)
    else:
        return outLines
    return True  
    
 
# Constants
     
pi = 3.141592653589793 # pi - 16 digits 
hc = 197.327           # hc - Standard Nuclear Conversion Constant
pi2 = pi*pi            # pi squared
                       
mnuc = 938.918         # Nucleon Mass-Energy 
mneu = 939.5656328     # Neutron Mass-Energy   
mprt = 938.2720881629  # Proton Mass-Energy  
melc = 0.51099895      # Electron Mass-Energy 
mmun = 105.658375523   # Muon Mass-Energy    
                       
vmhc = pi*hc*mnuc/2.0  # (pi/2) hc [MeV^-2] -> fm Conversion Constant      

kf_vals_20 = [i*0.1 for i in xrange(1,21)]  
qf_vals_20 = [hc*float(i) for i in kf_vals_20]
pf_vals_20 = [int(i) for i in qf_vals_20]

sm_vals_20 = [2.0*i*i*i/(3.0*pi2) for i in kf_vals_20]    
nm_vals_20 = [i*i*i/(3.0*pi2) for i in kf_vals_20]   