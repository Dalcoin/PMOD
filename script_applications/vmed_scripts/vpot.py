import subprocess
import re

import pmod.strlist as strl
import pmod.ioparse as iop
import pmod.mathops as mops
import pmod.pinax   as px
from pmod.cmdutil import cmdUtil

'''

Partial Wave progression chart:

n    
0    1s0       NaN       3p0       NaN         NaN          NaN
1    1p1       3p1       3d1       3s1       3d1+3s1      3s1+3d1    
2    1d2       3d2       3f2       3p2       3p2+3f2      3f2+3p2    
3    1f3       3f3       3g3       3d3       3d3+3g3      3g3+3d3    
4    1g4       3g4       3h4       3f4       3f4+3h4      3h4+3f4    
5    1h5       3h5       3i5       3g5       3g5+3i5      3i5+3g5    
6    1i6       3i6       3k6       3h6       3h6+3k6      3k6+3h6    
7    1k7       3k7       3l7       3i7       3i7+3l7      3l7+3i7    
8    1l8       3l8       3m8       3k8       3k8+3m8      3m8+3k8    
9    1m9       3m9       3n9       3l9       3l9+3n9      3n9+3l9    
10   1n10      3n10      3o10      3m10     3m10+3o10    3o10+3m10   
11   1o11      3o11      3q11      3n11     3n11+3q11    3q11+3n11   
12   1q12      3q12      3r12      3o12     3o12+3r12    3r12+3o12   
13   1r13      3r13      3t13      3q13     3q13+3t13    3t13+3q13   
14   1t14      3t14      3u14      3r14     3r14+3u14    3u14+3r14   
15   1u15      3u15      3v15      3t15     3t15+3v15    3v15+3t15   


'''

vpotp = re.compile(r'\s+(\d+)\s+(\d+.\d+D[-,+]\d\d)\s+(\d+.\d+D[-,+]\d\d)')
vpotline = re.compile(r'\s*'+6*r'(-*\d+.\d+D[-,+]\d\d)\s*')

j_code_dict = {'singlet':0, 'triplet':1, 'V++':2, 'V--':3, 'V+-':4, 'V-+':5}

pwave_pair_dict = {'1s0':(0,'singlet'), 
                   '3p0':(0,'V++'), 
                   '1p1':(1,'singlet'),  
                   '3p1':(1,'triplet'),
                   '3d1':(1,'V++'),
                   '3s1':(1,'V--')}


p20_set = ['0.197327E+02',
           '0.394654E+02',
           '0.591981E+02',
           '0.789308E+02',
           '0.986635E+02',
           '0.118396E+03',
           '0.138129E+03',
           '0.157862E+03',
           '0.177594E+03',
           '0.197330E+03',
           '0.217060E+03',
           '0.236792E+03',
           '0.256525E+03',
           '0.276258E+03',
           '0.295991E+03',
           '0.315723E+03',
           '0.335456E+03',
           '0.355189E+03',
           '0.374921E+03',
           '0.394654E+03']

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


class vpot(cmdUtil):
      
    def __init__(self,
                 osFormat,
                 errorCheck=False,
                 newPath=None,
                 rename=False,
                 debug=True,
                 shellPrint=False,
                 colourPrint=True,
                 space='    ',
                 endline='\n',
                 moduleNameOverride="vpot",
                 **kwargs):

        super(vpot, self).__init__(osFormat,
                                   newPath,
                                   rename,
                                   debug,
                                   shellPrint,
                                   colourPrint,
                                   space,
                                   endline,
                                   moduleNameOverride,
                                   **kwargs)

        self.errorCheck = errorCheck


    def partial_wave_parse(self, lines, waves=[], float_convert=True, fm_unit_convert=False, errorCheck=None, **kwargs):
        '''
        Directions: 
    
            Input raw strings corrosponding to the lines from the 'pot.d' or 'pot.txt' file.
            
    
        lines : raw 'pot.d' string file lines
        '''

        kwargs = self.__update_funcNameHeader__("partial_wave_parse", **kwargs)

        forward = False
        plines = []

        if(errorCheck == None):
            errorCheck = self.errorCheck

        if(errorCheck):
            if(self.__not_strarr_print__(lines, varID='lines', firstError=True, **kwargs)):
                return False
            if(self.__not_arr_print__(waves, varID='waves', firstError=True, **kwargs)):
                return False

            if(self.__not_arr_print__(waves, style='list', **kwargs)):
                return False


        value_dict = {}
        j_dict = {}
        jvals = []

        try:
            if(len(waves) > 0):
                for wave in waves:
                    if(wave[0] not in jvals):
                        jvals.append(wave[0])
                        j_dict[wave[0]] = [wave[1]]
                    else:
                        j_dict[wave[0]].append(wave[1])
                    value_dict[wave] = []
                get_wave = True
            else:
                get_wave = False
        except:
            return self.__err_print__("should be composed of two-integer tuples", varID='waves', **kwargs)

        for i,line in enumerate(lines):
            if(len(vpotp.findall(line)) > 0 and not forward):
                temp = map(lambda x : x.replace('D','E'), vpotp.findall(line)[0])
                forward = True
            if(len(vpotline.findall(line)) > 0 and forward):
                temp_2 = map(lambda x : x.replace('D','E'), vpotline.findall(line)[0])
                if(get_wave):
                    try:
                        jval = int(temp[0])
                        if(jval in jvals):
                            for pos in j_dict[jval]:
                                is2float = False
                                v_val = temp_2[pos]
                                if(float_convert):
                                    try:
                                        v_val = float(v_val)
                                        is2float = True
                                    except:
                                        self.__err_print__("could not convert to float", varID='pot', heading='Warning', **kwargs)
                                    if(fm_unit_convert and is2float):
                                        v_val = v_val*vmhc
                                if(temp[1] == temp[2]):
                                    value_dict[(jval, pos)].append((temp[1], v_val))
                                else:
                                    value_dict[(jval, pos)].append(((temp[1],temp[2]), v_val))
                    except:
                        return self.__err_print__("could not determine partial wave line, "+str(i+1)+", of lines", **kwargs)
                else:
                    plines.append((temp, temp_2))
                forward = False

        if(get_wave):
            return value_dict
        else:
            return plines


    def parse_pot_data(self, files,
                             pwaves,
                             float_convert=True,
                             fm_unit_convert=False,
                             errorCheck=None,
                             **kwargs):

        kwargs = self.__update_funcNameHeader__("parse_pot_data", **kwargs)

        if(errorCheck == None):
            errorCheck = self.errorCheck

        if(errorCheck):
            if(isinstance(files, str)):
                files = [files]
            elif(self.strarrCheck(files, failPrint=False, firstError=True, **kwargs)):
                pass
            else:
                return self.__err_print__("should be an array of strings", varID='files', **kwargs)

            if(isinstance(pwaves, (tuple,list))):
                for i,pwave in enumerate(pwaves):
                    if(self.__not_arr_print__(pwave, varID='pwave : '+str(i+1), **kwargs)):
                        return False
                    else:
                        if(len(pwave) != 2):
                            return self.__err_print__("should be an array of length 2", varID='pwave', **kwargs)
                        else:
                            if(not isinstance(pwave[0], int) or not isinstance(pwave[1], int)):
                                msg = ["the both entries of pwaves should be 'int' :", 
                                       "("+str(type(pwave[0]))+","+str(type(pwave[1]))+")"]
                                return self.__err_print__(msg, **kwargs)
            else:
                return self.__err_print__("should be an array, not type : "+str(type(pwaves)), varID='pwaves', **kwargs)

        output_data = []

        for file in files:
            lines = iop.flat_file_read(file, **kwargs)
            if(lines == False):
                continue

            column_vals = self.partial_wave_parse(lines,
                                                  waves=pwaves,
                                                  float_convert=float_convert,
                                                  fm_unit_convert=fm_unit_convert,
                                                  errorCheck=errorCheck,
                                                  **kwargs)
            if(column_vals == False):
                self.__err_print__("could not parse lines from '"+str(file)+"'", **kwargs)
                continue

            output_data.append((file, column_vals))
        return output_data


    def tabulate_pot_data(self, pot_data, equiv_momenta=True, header_line=False, errorCheck=None, **kwargs):

        kwargs = self.__update_funcNameHeader__("tabulate_pot_data", **kwargs)

        def get_new_file_name(file_name):
            if(not isinstance(file_name, str)):
                return False
            new_file_list = file_name.split('.')
            if(len(new_file_list) != 2):
                return False
            new_file_list[0] = new_file_list[0]+"_pwaves"
            new_file_line = new_file_list[0]+'.'+new_file_list[1]
            return new_file_line

        if(errorCheck == None):
            errorCheck = self.errorCheck

        if(errorCheck):
            if(self.__not_arr_print__(pot_data, **kwargs)):
                return False

        header_list = []
        file_list = []

        for file_data in pot_data:
            momenta = []
            file_name, data_dict = file_data
            file_list.append(file_name)
            new_file_name = get_new_file_name(file_name)
            if(new_file_name == False):
                self.__err_print__("could not generate a new file name for '"+str(file_name)+"'", **kwargs)
                continue
            data_list = []
            for wave in sorted(list(data_dict)):
                wave_data = data_dict[wave]
                if(header_line):
                    header_list.append(file_name+"_"+str(wave))
                if(equiv_momenta):
                    if(len(momenta) == 0):
                        momenta = map(lambda lam: lam[0], wave_data)
                        data_list.append(momenta)
                    data_column = map(lambda lam: lam[1], wave_data)
                    data_list.append(data_column)
                else:
                    data_list.append(map(lambda lam: lam[0], wave_data))
                    data_list.append(map(lambda lam: lam[1], wave_data))
            data_list_trans = px.table_trans(data_list, **kwargs)
            data_lines = px.matrix_to_str_array(data_list_trans, endline=True, **kwargs)
            if(self.__not_strarr_print__(data_lines, varID='data_lines', **kwargs)):
                continue
            if(header_line):
                header_line_str = strl.array_to_str(header_list, **kwargs)
                data_lines = [header_line_str]+data_lines
            iop.flat_file_write(new_file_name, data_lines, **kwargs)
        return True