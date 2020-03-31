import sys
import os
import subprocess
import re

import ioparse as iop 
import strlist as strl 
import cmdline as cml 
import mathops as mops


class benv:

    def __init__(self, initialize = True, kernel = 'linux'):


        # File and folder names    
        self.PAR_FILE_NAME = 'par.don'
        self.VAL_FILE_NAME = 'nucleus.don'
             
        self.BINFILE = 'bin' 
        self.SRCFILE = 'src' 
        self.binpath = ''
              
        self.PARSFILE = 'parameters.don'
        self.parspath = ''

        self.SKVLFILE = 'skval.don'
        self.skvlpath = ''
           
        self.EOSDIR = 'eos' 
        self.eospath = '' 

        self.OPTPARS = 'opt_par.etr'
        self.SKINVAL = 'skin.srt'  

        # Regex codes 
        DIGIT    = "(\d+)"
        DIGITSPC = DIGIT+"\s+"
        FLOATER  = "(\d+.+\d*)\s*"

        self.INCLOOP = re.compile("\s*INCloop\s*:\s*([T,F]\D+)") 
        self.AZPAIRS = re.compile("\s*AZpairs\s*:\s*([T,F]\D+)")
        self.MIRRORS = re.compile("\s*Mirrors\s*:\s*([T,F]\D+)")
        self.NEWPARS = re.compile("\s*Newpars\s*:\s*([T,F]\D+)") 
           
        self.PAIRS = re.compile("\s*(\d+),(\d+)")
        self.LOOPS = re.compile("\s*(\d+)\s+(\d+)\s+(\d+)\s*")
        self.PARGP = re.compile("\s*"+9*DIGITSPC+FLOATER+DIGIT)     
 
        # debug 
        self.SUBPROCESS_PATH_CHECK = False
        self.SKVLFILE_PATH_ERROR = False
        self.EOSDIR_PATH_ERROR = False

        self.PAR_FORMAT_ERROR = False
        self.SKVAL_FORMAT_ERROR = False 
        self.SKVAL_CONTROL_ERROR = False

        self.EOS_SPLIT_FILE_ERROR = False
        self.EOS_FILE_FORMAT_ERROR = False 
        self.EOS_SPLIT_PARSE_ERROR = False
        self.EOS_PASS_ERROR = False

#        self.eos_table = []

        # internal shell command line
        self.cmv = cml.path_parse(kernel) 
        self.INITIAL_PATH = self.cmv.var_path
        self.run_time = 1 

        # initial data 
        self.initial_pars = ''
        self.initial_a = 0
        self.initial_z = 0           

        # skval functionality

        self.incloop = False  
        self.azpairs = False
        self.mirrors = False 
        self.newpars = False         

        success, self.CURRENT_PATH = self.cmv.cmd('pwd') 
            
        if(initialize):
          
            self.set_par_path()
            self.set_skvl_path() 
            self.set_eos_path()

            self.set_bin_dir()
         
            try:
                self.initial_pars, self.initial_vals = self.data_from_pars() 
                self.initial_pars = self.initial_pars[0]
            except:
                print("[benv] Error: failure to get data from 'parameters.don' file ")
                self.exit_function("while initializing 'benv' class instance")
                
            try: 
                self.initial_a, self.initial_z = strl.str_to_list(self.initial_vals[-1], filtre=True) 
                self.initial_a = int(float(strl.str_clean(self.initial_a)))
                self.initial_z = int(float(strl.str_clean(self.initial_z)))                
            except:
                print("[benv] Error: failure to parse isotope values A and Z to integers (the last parameter line)")
                self.exit_function("while initializing 'benv' class instance")

            self.set_eos_path()
         
          
    def exit_function(self, action_msg):
        print("Exit: failed "+action_msg)
        print("Failure occured on run number: "+str(self.run_time))
        sys.exit()
        
    ##############################################################
    # functions to set the internal pathway strings used in BENV #
    ############################################################## 

    def set_par_path(self):
        success, data = self.cmv.cmd("dir "+self.PARSFILE)
        if(not success):
            print("Error: failure to get path for file named '"+self.PARSFILE+"'")
            self.exit_function('when setting the parameter file path')
        self.parspath = data[0]
        return None       

    def set_skvl_path(self):
        success, data = self.cmv.cmd("dir "+self.SKVLFILE)
        if(not success):
            print("[set_eos_path] Warning: failure to get path for file named '"+self.SKVLFILE+"'")
            self.SKVLFILE_PATH_ERROR = True
        self.skvlpath = data[0]
        return None       

    def set_eos_path(self):
        success, data = self.cmv.cmd("dir "+self.EOSDIR)
        if(not success):
            print("[set_eos_path] Warning: failure to get path for file named '"+self.EOSDIR+"'")
            self.EOSDIR_PATH_ERROR = True
        else:    
            self.eospath = data[0]             
        return None

    def set_bin_dir(self):

        success, output = self.cmv.cmd("cd "+self.BINFILE)
        if(not success):
            print("[set_bin_dir] ExitError: failure to access "+self.BINFILE)
            self.exit_function("when entering the 'bin' directory")
        
        success, output = self.cmv.cmd("pwd")
        if(not success):
            print("[set_bin_dir] ExitError: failure to access "+self.BINFILE+" pathway")
            self.exit_function("when accessing 'bin' pathway")
        else:
            binpath = output 

        self.binpath = binpath  # the pathway for the bin directory is loaded      
        os.chdir(binpath)       # commands executed with subprocess will run in the bin directory
              
        success, output = self.cmv.cmd("cd ..")   
        if(not success):
            print("[set_bin_dir] ExitError: failure to access "+self.BINFILE)
            self.exit_function("when returning to initial directory")

        self.SUBPROCESS_PATH_CHECK = True
        return None


    ##################################################################################################
    # functions dealing with the 'parameters.don', 'par.don' and 'nucleus.don' (or equivalent) files #
    ##################################################################################################      
    
    def data_from_pars(self):        
        lines = iop.flat_file_grab(self.parspath)
        par = [lines[0]]
        val = lines[1:4]
        return (par, val)

    
    def format_pars_line(self, eos, 
                         density = 2
                         microscopic = True, 
                         e0_rho0 = True,
                         phenom_esym = False,
                         k0 = 220, 
                         rho0 = 0.16
                         fff = 65,
                         *lengths):

        if(isinstance(eos,str)):
            if(eos == '0' or eos.lower() == 'combined' or eos.lower() == 'com'):
                pos_3 = 0
            elif(eos == '1' or eos.lower() == 'seperate' or eos.lower() == 'sep'):
                pos_3 = 1
            elif(eos == '2' or eos.lower() == 'symmetric' or eos.lower() == 'sym'):
                pos_3 = 2
            else: 
                pos_3 = 0   
        elif(isinstance(eos,int)):      
            if(eos == 0):
                pos_3 = eos
            elif(eos == 1):
                pos_3 = eos
            elif(eos == 2):
                pos_3 = eos
            else: 
                pos_3 = 0      
        else: 
            pos_3 = 0

        
        if(isinstance(density,str)):
            options_list_2 = ['2pf', 'thomas-fermi', 'fermi', 'tf'] 
            options_list_3 = ['2py', 'folded-yukawa', 'yukawa', 'fy']
            options_list_4 = ['3pf', 'extended-thomas-fermi', 'extened-fermi','efermi', 'etf']
            if(density == '2' or density.lower() in options_list_2):
                pos_2 = 2
            elif(density == '3' or density.lower() in options_list_3):
                pos_2 = 3
            elif(density == '4' or density.lower() in options_list_4):
                pos_2 = 4
            else: 
                pos_2 = 2   
        elif(isinstance(density,int)):      
            if(eos == 2):
                pos_2 = eos
            elif(eos == 3):
                pos_2 = eos
            elif(eos == 4):
                pos_2 = eos
            else: 
                pos_2 = 2      
        else: 
            pos_2 = 2      
         
        if(microscopic):
            pos_6 = 1 
        else:
            pos_6 = 0           
         
        if(e0_rho0):
            pos_7 = 1 
        else:
            pos_7 = 0             

        if(phenom_esym):
            pos_8 = 1 
        else:
            pos_8 = 0   

        pos_9  = k0
        pos_10 = rho0
        pos_11 = fff

        lens = [n for n in lengths] 
        n = len(lens) 
        
        if(n == 0 and mic == 1):
            print("[format_pars_line] Error: if a microscopic eos is chosen, file length(s) must be defined")
            return False  
        if(mic == 1 and pos_3 == 0 and n < 1):
            print("[format_pars_line] Error: if a combined eos is chosen, the file length must be defined")
            return False         
        elif(mic == 1 and pos_3 == 1 and n < 2):
            print("[format_pars_line] Error: if a seperate eos is chosen, file lengths must be defined (e0 first then e1)")
            return False                  
        elif(mic == 1 and pos_3 == 2 and n < 1):
            print("[format_pars_line] Error: if a symmetric eos is chosen, the file length must be defined")
            return False     
        else:         
         
        if(mic == 1 and (pos_3 == 0 or pos_3 == 2)):
            pos_1 = lens[0]
            pos_4 = 0
            pos_5 = 0
        elif(mic == 1 and pos_3 == 1):
            pos_1 = 0
            pos_4 = lens[0]
            pos_5 = lens[0]
        else: 
            pos_1 = 0
            pos_4 = 0
            pos_5 = 0            
            
        outlist = [pos_1,pos_2,pos_3,pos_4,pos_5,pos_6,pos_7,pos_8,pos_9,pos_10,pos_11]
        outline = strl.array_to_str(outlist)
               
        return outline      
        

    def format_pars_data(self, parline, a, z, parform = 'str'):
        '''
        Takes a valid 'par.don' string and nucleus denoted by integers (A,Z)
        '''
        
        if(parform == 'array' or parform == 'list' or parform == 'tuple'):
            parline = array_to_str(parline, endline=True)
        else:
            if(isinstance(parline,str)):
                if('\n' in parline):
                    pass 
                else:
                    parline = parline + '\n'
            else:
                print("Error: 'parline' must either be a string or list of strings, set parform to 'list' in the latter case")
                self.exit_function("when attempting to create a list of valid 'parameters.don' lines")
         
        divs = "64 64 64\n"
        lims = "0.0 20.0\n" 
        az = str(a)+'  '+str(z)+'\n'
        return [parline, divs, lims, az] 

    def data_to_pars(self, dataline):        
        iop.flat_file_write(self.parspath, dataline)
        return None

    def get_inital_pars(self):
        return self.initial_pars

    def pass_pars(self, pars):
        '''
        Passes benv parameters to 'par.don' file located in 'bin'
        
        pars takes the form: [see read-me for details]

            n  nden nread n0 n1 mic isnm k0  rho0 fff
            11 2    0     19 19 0   1 0  220 0.16 65  

        '''
          
        #check on 'pars'
        if(isinstance(pars,(list,tuple))):
            parslist = pars
        elif(isinstance(pars,str)):
            parslist = [pars]
        else:
            print("[pass_pars] Error: 'pars' must be an array or string")
            self.exit_function("running checks on 'pars'")
                 
        par_file_path = self.cmv.pw_join(self.binpath,self.PAR_FILE_NAME)   
        success = iop.flat_file_write(par_file_path,parslist) 
        if(not success):
            print("[pass_pars] ExitError: failure when writing the string(s): \n")
            for i in parslist:
                print("    '"+str(i)+"'")
            print("to the path: ")
            print("    '"+str(par_file_path)+"'") 
            self.exit_function("writing parameters to 'par.don' file")
        return None
             

    def pass_vals(self, val_list): 
         
        #check on 'val_list'
        if(not isinstance(val_list,(list,tuple))):
            print("Error: 'val_list' must be an array")
            self.exit_function("running checks on 'val_list'")
         
        val_file_path = self.cmv.pw_join(self.binpath,self.VAL_FILE_NAME)  

        success = iop.flat_file_write(val_file_path,val_list) 
        if(not success):
            print("ExitError: failure when writing the string: \n")
            for i in val_list:
                print("    '"+str(i)+"'")
            print("to the path: ")
            print("    '"+str(val_file_path)+"'") 
            self.exit_function("writing parameters to 'nucleus.don' file")
        return None     
            
    #########################################
    # functions dealing with the skval loop #
    #########################################                               
              

    def get_skval_data(self):
        '''
        Gets skval data from the internal pathway (which must be set prior)
        
        Do not call this function unless the skval data file will be available in your script   
        '''     
        lines = iop.flat_file_grab(self.skvlpath, scrub = True)
        if(not lines):
            print("[get_skval_data] IOPError: failure to access the file '"+str(self.skvlpath)+"'")
            self.exit_function("when accessing the 'skval' parameters file") 
        
        return lines 
       
         
    def format_skval_data(self, lines):

        skval_lines = list(lines)          

        incloop, azpairs, mirrors, newpars = False, False, False, False
          
        n = len(skval_lines)
        incb, azpb, mirb, newb = True, True, True, True  
        npreamble = -1
         
        for i in xrange(n):
            if(incb):
                incloop = self.INCLOOP.findall(skval_lines[i])
                if(incloop != []):
                    self.incloop = (incloop[0].lower() == 'true')
                    incb = False             
            if(azpb):
                azpairs = self.AZPAIRS.findall(skval_lines[i])
                if(azpairs != []):
                    self.azpairs = (azpairs[0].lower() == 'true')
                    azpb = False                
            if(mirb):
                mirrors = self.MIRRORS.findall(skval_lines[i])  
                if(mirrors != []):
                    self.mirrors = (mirrors[0].lower() == 'true')
                    mirb = False 
            if(newb):
                newpars = self.NEWPARS.findall(skval_lines[i])  
                if(newpars != []):
                    self.newpars = (newpars[0].lower() == 'true')
                    newb = False 
                 
            if(i+1 == n and not all([not incb, not azpb, not mirb, not newb])):
                if(incb):
                    print("[format_skval_data] Warning: could not find parameter 'INCloop' in 'skval_lines'")  
                if(azpb):
                    print("[format_skval_data] Warning: could not find parameter 'AZpairs' in 'skval_lines'")
                if(mirb):
                    print("[format_skval_data] Warning: could not find parameter 'Mirrors' in 'skval_lines'")  
                if(newb):
                    print("[format_skval_data] Warning: could not find parameter 'Newpars' in 'skval_lines'")  
            elif(all([not incb, not azpb, not mirb, not newb])):
                npreamble = i    
                break    
            else:
                pass

        if(n > npreamble >= 0):
            skval_lines = skval_lines[npreamble:] 

        pars = []
        doubles = []
        loop = []
        output = []

        if(self.incloop and self.azpairs):
            print("[format_skval_data] Warning: both skval looping and nuclei pairs detected")
            print("    skval looping takes precedent over paring")
            self.SKVAL_CONTROL_ERROR = True
         
        if(self.incloop):
            for i in skval_lines:
                looplist = self.LOOPS.findall(i)
                if(len(looplist) > 0):
                    loop.append(looplist[0])
                if(self.newpars):
                    pgp = self.PARGP.findall(i)
                    if(len(pgp)>0): 
                        pars.append(pgp[0])  

            if(len(loop) > 0):
                if(len(pars) > 0):
                    if(len(loop) != len(pars)):
                        print("[format_skval_data] Warning: parameters detected with formatting error")
                        print("    Parameter will be ignored for this run group")
                        self.PAR_FORMAT_ERROR = True
                        output = (loop[0],"loop",False)
                        return output
                    else:
                        output = (map(lambda x,y: (x,y), loop,pars),"loop",True)
                        return output
                else:
                    if(len(loop) > 1):
                        print("[format_skval_data] Warning: skval loop detected with formatting error")
                        print("    Only the first skval loop will be executed for this run group")
                        self.SKVAL_FORMAT_ERROR = True
                    output = (loop[0],"loop",False)  
                    return output
            else:                    
                self.SKVAL_FORMAT_ERROR = True
              
        elif(self.azpairs):

            for i in skval_lines:
                double = self.PAIRS.findall(i)
                if(len(double)>0): 
                    var = double[0]
                    var = map(lambda x: float(strl.str_clean(x)), var)
                    doubles.append(var)
                if(self.newpars):
                    pgp = self.PARGP.findall(i)
                    if(len(pgp)>0): 
                        pars.append(pgp[0])

            if(len(doubles) > 0):
                if(len(pars) > 0):
                    if(len(doubles) != len(pars)):
                        print("[format_skval_data] Warning: parameters detected with formatting errors")
                        print("    Parameter will be ignored for this run group")
                        self.PAR_FORMAT_ERROR = True
                        output = (doubles,"pair",False)
                        return output
                    else:
                        output = (map(lambda x,y: (x,y), doubles,pars),"pair",True) 
                        return output 
                else:
                    output = (doubles,"pair",False)
                    return output
            else:                    
                self.SKVAL_FORMAT_ERROR = True
        else:
            output = [[],"",False] 

        print("No skval functionality detected...")                            
        return output  


    def skval_loop_line_parse(self, line):
        if(not isinstance(line,str)):      
            print("Error: input 'line' must be a string")                  
            self.exit_function("when parsing a skval loop instance")
          
        loop = strl.str_to_list(line, filtre=True)
        if(len(loop) != 6):
            print("[skval_loop_line_parse] Error: there should be exactly 6 entries in 'line'")
            self.exit_function("when parsing a skval loop instance")
            
        try:
            output_list = [int(loop[0]), int(loop[1]), int(loop[2]), bool(int(loop[3])), bool(int(loop[4])), bool(int(loop[5]))]
        except:
            print("[skval_loop_line_parse] Error: could not coerce 'loop' list into a skval-loop list")
            self.exit_function("when parsing a skval loop instance")

        return output_list


    ###################################################################################
    # functions dealing with the 'eoses.don', e[x,0,1]_nxlo.don (or equivalent) files #
    ################################################################################### 

    def collect_eos(self):
        '''
        Collects EoS from 'eos' directory 
        This function should only be called once per BENV run 
        
 
        ''' 

        eos_dir_path = self.cmv.pw_join(self.INITIAL_PATH,self.EOSDIR)
        eos_file_list = self.cmv.pw_contain(eos_dir_path)

        if(eos_file_list == None or eos_file_list == False):
            print("[collect_eos] Error: EoS files could not be found")
            self.EOS_COLLECT_ERROR = True
            return False
    
        exfiles = []
        e1files = []
        e0files = []
        egshock = []
        eoslist = []

            
        for i in eos_file_list:
            if('ex' in i.lower() and (('e0' not in i.lower()) and ('e1' not in i.lower()))):
                exfiles.append(i)
            elif('e1' in i.lower() and (('e0' not in i.lower()) and ('ex' not in i.lower()))):
                e1files.append(i) 
            elif('e0' in i.lower() and (('ex' not in i.lower()) and ('e1' not in i.lower()))):
                e0files.append(i)        
            else:
                egshock.append(i) 

        if(len(egshock) > 0):
            head = "The following files are not valid 'eos' files:"
            strl.format_fancy(egshock,header=head)                 
            
        for i in exfiles:
            file_path = self.cmv.pw_join(eos_dir_path,i)  
            file_inst = iop.flat_file_intable(i) 
            if(file_inst != False):
                if(len(file_inst) != 3):
                    print("[collect_eos] Error: the file '"+str(i)+"' did not have three equal data columns")
                    self.EOS_FILE_FORMAT_ERROR = True
                    continue 
                eoslist.append(file_inst)
            else:
                print("[collect_eos] Error: could not read the file '"+str(i)+"' as a table")
                continue                                     
              
        for i in e0files:
             
            e1pack = False
            
            if(len(i.split('e0')) == 2):
                e1add = 'e1'
                baselist = i.split('e0') 
            elif(len(i.split('E0')) == 2):
                e1add = 'E1'
                baselist = i.split('E0')                      
            else:         
                self.EOS_SPLIT_PARSE_ERROR = True 
                continue
            
            if(baselist[0] == ''):
                e1name = e1add+baselist[1] 
            else:
                e1name = baselist[0]+e1add+baselist[1]                                   
             
            e0_file_path = self.cmv.pw_join(eos_dir_path,i)  
    
            if(e1name in e1_files):
                e1pack = True
                e1_file_path = self.cmv.pw_join(eos_dir_path,e1name)     

            e0data = iop.flat_file_intable(e0_file_path)
            if(e1pack):
                e1data = iop.flat_file_intable(e1_file_path)

            if(not e0data):
                print("[collect_eos] Error: could not parse the file at path '"+str(e0_file_path)+"' into a table")
                self.EOS_SPLIT_PARSE_ERROR = True 
                continue 
            if(not e1data and e1pack):
                print("[collect_eos] Error: could not parse the file at path '"+str(e1_file_path)+"' into a table")
                self.EOS_SPLIT_PARSE_ERROR = True 
                continue

            if(e1pack)
                e10 = []
                try:
                    e10 = [e0data[0],e0data[1],e1data[0],e1data[1]]
                except:
                    print("[collect_eos] Error: could not parse '"+str(e0_file_path)+"' and '"+str(e1_file_path)+"' content into data")
                    self.EOS_SPLIT_PARSE_ERROR = True 
                    continue                                     
                eoslist.append(e10) 
            else:
                e0 = []
                try:
                    e0 = [e0data[0],e0data[1]]
                except:
                    print("[collect_eos] Error: could not parse '"+str(e0_file_path)+"' content into data")
                    self.EOS_SPLIT_PARSE_ERROR = True 
                    continue                                     
                eoslist.append(e0)
              
        return eoslist         
                    
         
            
    def format_eos_data(self, eoslist_entry, columns = True):
    
        output = ()
        exgp = [] 
        e0gp = [] 
        e1gp = []

        if(len(eoslist_entry) == 3):
            type = 0
            kf = eoslist_entry[0]
            e0 = eoslist_entry[1] 
            e1 = eoslist_entry[2]
            for i in xrange(len(eoslist_entry)):
                exgp.append(map(lambda x,y,z: strl.array_to_str([x,y,z],spc='  '),kf,e0,e1))
            output = (type, exgp)        
        elif(len(eoslist_entry) == 4):
            type = 1
            kf0 = eoslist_entry[0]
            e0  = eoslist_entry[1]
            kf1 = eoslist_entry[2]
            e1  = eoslist_entry[3]
            for i in xrange(len(eoslist_entry[0])):
                e0gp.append(map(lambda x,y,z: strl.array_to_str([x,y],spc='  '),kf0,e0))
            for i in xrange(len(eoslist_entry[0])):
                e1gp.append(map(lambda x,y,z: strl.array_to_str([x,y],spc='  '),kf0,e0))
            output = (type, e0gp, e1gp)                
        elif(len(eoslist_entry) == 2): 
            type = 2
            kf = eoslist_entry[0]
            e0 = eoslist_entry[1] 
            for i in xrange(len(eoslist_entry)):
                e0gp.append(map(lambda x,y: strl.array_to_str([x,y],spc='  '),kf,e0))
            output = (type, e0gp)   
        else:
            print("[format_eos_data] Error: 'eoslist_entry' must be either 3 or 4 numeric lists")
            output = False
                    
        return output         
           
         
    def pass_eos(self, formatted_eos):

        if(not isinstance(formatted_eos,(list,tuple))):
            print("[pass_eos] Error: 'formatted_eos' must be either a list or tuple")
            self.EOS_PASS_ERROR = True
            return False 
         
        type = formatted_eos[0]  
         
        if(type == 0):
            eos_path = self.cmv.pw_join(self.binpath,'ex_nxlo.don') 
            iop.flat_file_write(eos_path, formatted_eos[1])            
        elif(type == 1):
            e0_path = self.cmv.pw_join(self.binpath,'e0_nxlo.don') 
            iop.flat_file_write(e0_path, formatted_eos[1])
            e1_path = self.cmv.pw_join(self.binpath,'e1_nxlo.don') 
            iop.flat_file_write(e1_path, formatted_eos[2])      
        elif(type == 2):
            e0_path = self.cmv.pw_join(self.binpath,'e0_nxlo.don') 
            iop.flat_file_write(e0_path, formatted_eos[1])                  
        else:
            print("[pass_eos] Error: 'formatted_eos' is not properly formatted")
            return False

        return None


    #######################################
    # functions dealing with benv looping #
    #######################################


    def data_from_bin(self, file_name, firstline):
                      
        filepath = self.cmv.pw_join(self.binpath,file_name)
        lines = iop.flat_file_grab(filepath)
        if(lines == False):
            print("[data_from_bin] Error: Failure to get data from file: '"+str(file_name)+"'")
            print("    Attempted pathway: '"+str(filepath)+"'")
            return False
                    
        if(firstline):
            return lines[0] 
        else: 
            return lines   

  
    def run_benv(self, collect = True):

        if(not self.SUBPROCESS_PATH_CHECK):
            exit_function("because 'SUBPROCESS_PATH_CHECK' needs to be set before runing 'run_benv'")
          
        subprocess.call("./run.sh", shell=True)                   
                    
          
    def run_once(self):
           
        pars, vals = self.data_from_pars() 
        self.pass_pars(pars)
        self.pass_vals(vals)
        self.run_benv()
        
        optpars  = self.data_from_bin(self.OPTPARS,True)
        skinvals = self.data_from_bin(self.SKINVAL,True)
        
        subprocess.call("rm "+self.OPTPARS,shell = True)
        subprocess.call("rm "+self.SKINVAL,shell = True)

        self.run_time+=1
        return ((optpars,skinvals))
         

    def format_skval_benv_vals(self, benvals, split = False):
         
        if(split):
            parlines = [] 
            nuclines = []
            azs      = []
        else:
            outlines = []
                 
        for i in xrange(len(benvals)):
            parline = strl.str_to_list(str(benvals[i][0][0]).rstrip(), filtre=True)
            nucline = strl.str_to_list(str(benvals[i][0][1]).rstrip(), filtre=True)
        
            parline = strl.array_to_str([round(float(j),10) for j in parline], spc = '  ')
            nucline = strl.array_to_str([round(float(j),10) for j in nucline], spc = '  ')

            if(split):
                parlines.append(parline) 
                nuclines.append(nucline)
                azs.append((str(int(float(benvals[i][1][0]))), str(int(float(benvals[i][1][1])))))
            else:            
                isoline = '    '+str(int(float(benvals[i][1][0])))+'  '+str(int(float(benvals[i][1][1])))
                totline = parline+nucline+isoline+'\n'                
                outlines.append(totline)
        
        if(split): 
            return (parlines, nuclines, azs)
        else: 
            return outlines
            

    def clean_up(self):
        
        if(self.cmv.var_path_list[-1] != self.BINFILE):          
            success, output = self.cmv.cmd("cd "+self.BINFILE)
            if(not success):
                print("[clean_up] ExitError: failure to access "+self.BINFILE)
                self.exit_function("while changing directories")

        subprocess.call("rm CONSOLE.txt",shell = True)         
        return None
        
      
def benv_skval_loop(benv_instance, skval = True, reset = True):
    ''' 
    Notes: 

    'benv_instance' must be an initialized instance of the 'benv' class 

    It is strongly recommmended that your instance of the 'benv' class 
    keep the default 'initialize' option upon initialization 

    '''

    benvals = []

    initial_pars = benv_instance.get_inital_pars()
     
     
    if(skval):
        # Parsing data from the skval data file, default : 'skval.don' 
        skval_lines = benv_instance.get_skval_data()
        data, type, parincl = benv_instance.format_skval_data(skval_lines)
        
        # 'type' determines if BENV values are computed by a skval loop or individual nuclei   
        if(type == 'loop'):       
            if(parincl):
                for i in data:
                    skev, pars = i
                    skval_list = benv_instance.skval_loop_line_parse(skev)
                    if(skval_list[3]):
                        inv = -1 
                    else:
                        inv = 1                     
                    for i in xrange(skval_list[0]):
                        ax = self.initial_a+inv*skval_list[2]*(j+1)
                        for j in xrange(skval_list[1]): 
                            zx = self.initial_z+inv*(skval_list[2])*(j+1)                                    
                            parlines = benv_instance.format_pars_data(pars, ax, zx)       
                            benv_instance.data_to_pars(parlines)
                            results = benv_instance.run_once()
                            benvals.append(results,(ax,zx))                          
            else:
                skval_list = benv_instance.skval_loop_line_parse(data)   
                if(skval_list[3]):
                    inv = -1 
                else:
                    inv = 1
                for i in xrange(skval_list[0]):
                    ax = self.initial_a+inv*skval_list[2]*(j+1)
                    for j in xrange(skval_list[1]): 
                        zx = self.initial_z+inv*(skval_list[2])*(j+1)                                    
                        parlines = benv_instance.format_pars_data(initial_pars, ax, zx)
                        benv_instance.data_to_pars(parlines)
                        results = benv_instance.run_once()
                        benvals.append(results,(ax,zx))                         
                        
        elif(type == 'pair'): 
            if(parincl):   
                for i in data: 
                    pair, pars = i
                    parlines = benv_instance.format_pars_data(pars, pair[0], pairs[1])
                    benv_instance.data_to_pars(parlines)
                    results = benv_instance.run_once()
                    benvals.append((results,pair))                
            else:
                for i in data: 
                    parlines = benv_instance.format_pars_data(initial_pars, i[0], i[1])
                    benv_instance.data_to_pars(parlines)
                    results = benv_instance.run_once()
                    benvals.append((results,i))                
        else:
            print("Error: 'type' not reconignized")
            benv_instance.exit_function("when executing skval looping") 
         
        if(reset):
            benv_instance.data_to_pars(initial_pars)    

    else:
        results = benv_instance.run_once()
        benvals.append(results)
            
    return benvals
             

def benv_eos_loop(benv_instance):

    benvals_group = []

    initial_pars = benv_instance.get_inital_pars()

    eoslist = benv_instance.collect_eos()
    for entry in eoslist:
        eos_instance = benv_instance.format_eos_data(entry)
        benv_instance.pass_eos(eos_instance)
        benvals = benv_skval_loop(benv_instance)
        formatted_benvals = benv_instance.format_skval_benv_vals(benvals)
        benvals_group.append(formatted_benvals)

    return benvals_group 


 
