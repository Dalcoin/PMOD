# zzparse: Zeit-Zahl (Time and Number) parsing

import time
import datetime
import math as mt

class zzparse:
    
    def __init__(self, num=None, time=None):
        
        self.num = num     
        self.time = time

    # Zeit Functions:

    def secs_counter(self,zeit,nbool=False,dplace = 3):
        if(nbool):
            return [zeit]
        else:
            if(zeit == 1.):
                return str(str(int(zeit))+' sec')
            else:
                zeit = self.round_decimal(zeit,dplace,True)
                return str(zeit+' secs')              
        
    def mins_counter(self,zeit,nbool=False):        
        mins = mt.floor(zeit/60.) 
        secs = zeit - mins*60.
        secs = self.secs_counter(secs,nbool)
        if(nbool):
            return [mins,secs[0]]        
        else:    
            if(mins == 1):
                return str(str(int(mins))+' min'+' & '+str(secs))
            else:
                return str(str(int(mins))+' mins'+' & '+str(secs))
    
    def hrs_counter(self,zeit,nbool=False):           
        hrs = mt.floor(zeit/(3600.))
        secs_left = zeit - hrs*3600.
        mins = self.mins_counter(secs_left,nbool)
        if(nbool):
            return [hrs,mins[0],mins[1]]
        else: 
            if(hrs == 1):
                return str(str(int(hrs))+' hr, ' + str(mins))
            else:
                return str(str(int(hrs))+' hrs, ' + str(mins))
                 
    def days_counter(self,zeit,nbool=False):
        days = mt.floor(zeit/86400.)
        secs_left = zeit - days*86400.
        hrs=self.hrs_counter(secs_left,nbool)
        if(nbool):
            return [days,hrs[0],hrs[1],hrs[2]] 
        else:
            if(days == 1):
                return str(str(int(days))+' day, ' + str(hrs))
            else:
                return str(str(int(days))+' days, ' + str(hrs)) 

    def yrs_counter(self,zeit,nbool=False):
        yrs = mt.floor(zeit/31536000.)
        secs_left = zeit - yrs*31536000.
        days=self.days_counter(secs_left,nbool)
        if(nbool):
            return [yrs,days[0],days[1],days[2],days[3]] 
        else:
            if(yrs == 1):
                return str(str(int(yrs))+' year, ' + str(days))
            else:
                return str(str(int(yrs))+' years, ' + str(days))

    def cent_counter(self,zeit,nbool=False):
        cent = mt.floor(zeit/3153600000.)
        secs_left = zeit - cent*3153600000.
        yrs=self.yrs_counter(secs_left,nbool)
        if(nbool):
            return [cent,yrs[0],yrs[1],yrs[2],yrs[3],yrs[4]] 
        else:
            if(cent == 1):
                return str(str(int(cent))+' century, ' + str(yrs))
            else:
                return str(str(int(cent))+' centries, ' + str(yrs))

    def mil_counter(self,zeit,nbool=False):
        mil = mt.floor(zeit/31536000000.)
        secs_left = zeit - mil*31536000000.
        cent=self.cent_counter(secs_left,nbool)
        if(nbool):
            return [mil,cent[0],cent[1],cent[2],cent[3],cent[4],cent[5]] 
        else:
            if(mil == 1):
                return str(str(int(mil))+' millennium , ' + str(cent))
            else:
                return str(str(int(mil))+' millennia , ' + str(cent))

    def cosmo_counter(self,zeit,nbool=False):
        cosmo = mt.floor(zeit/(31536000000.*230000.))
        secs_left = zeit - cosmo*31536000000.*230000.
        mil=self.mil_counter(secs_left,nbool)
        if(nbool):
            return [cosmo,mil[0],mil[1],mil[2],mil[3],mil[4],mil[5],mil[6]] 
        else:
            if(cosmo == 1):
                return str(str(int(cosmo))+' cosmo, ' + str(mil))
            else:
                return str(str(int(cosmo))+' cosmos, ' + str(mil))

    def aeon_counter(self,zeit,nbool=False):
        aeon = mt.floor(zeit/(31536000000.*1000000.))
        secs_left = zeit - aeon*31536000000.*1000000.
        cosmo=self.cosmo_counter(secs_left,nbool)
        if(nbool):
            return [aeon,cosmo[0],cosmo[1],cosmo[2],cosmo[3],cosmo[4],cosmo[5],cosmo[6],cosmo[7]] 
        else:
            if(aeon == 1):
                return str(str(int(aeon))+' aeon, ' + str(cosmo))
            else:
                return str(str(int(aeon))+' aeon, ' + str(cosmo))


    def time_parse_sec(self,zeit,nbool=False):
        
    #   convert_time(204235,True)    
    #   zeit = numeric type, number of seconds to be converted
    #   nbool: boolean type, controls if the output is a 
    #   string (when False), or a list of floats (when True)       
                    
        zeit = float(zeit)
        if(zeit < 0):
            zeit=-1.*zeit
    
        if (zeit < 1.):
            return self.secs_counter(zeit,nbool)
        elif (zeit< 60.):
            return self.secs_counter(zeit,nbool)
        elif (zeit < 3600.):
            return self.mins_counter(zeit,nbool)
        elif (zeit < 86400.):
            return self.hrs_counter(zeit,nbool)        
        elif (zeit < 31536000.):
            return self.days_counter(zeit,nbool) 
        elif (zeit < 3153600000.):
            return self.yrs_counter(zeit,nbool)
        elif (zeit < 31536000000.):
            return self.cent_counter(zeit,nbool)
        elif (zeit < 31536000000.*230000.):
            return self.mil_counter(zeit,nbool)
        elif (zeit < 31536000000.*1000000.):
            return self.cosmo_counter(zeit,nbool)
        else:
            return self.aeon_counter(zeit,nbool)


    def convert_time_unit(self,zeit,inunit,outunit='sec'):
        
        cosmo = 31536000000.*230000.
        aeon = 31536000000.*1000000.
        unit_list = ['sec','min','day','yr','cent','mil','cosmo','aeon'] 
        factor_list = [1.,60.,86400.,31536000.,3153600000.,31536000000.,cosmo,aeon]

        conv_dict = dict(zip(unit_list,factor_list))
        
        if(inunit not in unit_list):
            print("[convert_secs] Error: "+str(inunit)+" not a recognized abbreviated unit of time")  
            return False
        if(outunit not in unit_list):
            print("[convert_secs] Error: "+str(outunit)+" not a recognized abbreviated unit of time")  
            return False
        
        secs = zeit*conv_dict[inunit]

        if(outunit == 'sec'): 
            return secs
        else:
            heure = secs/conv_dict[outunit]
            return heure
        

    def time_parse(self,zeit,inunit,nbool)
        secs = self.convert_time_unit(zeit,inunit)
        ptime = self.time_parse_sec(secs,nbool)
        return ptime

    













class clock():

    def __init__(self, opt):
        self.init_time = datetime.datetime.now()
        
            
    def current_datetime(self,value='time',form='strlist'):
        time_now= datetime.datetime.now()
        date_str = str(time_now).split(' ')[0]
        time_str = str(time_now).split(' ')[1]
        
        time_list = time_str.split(':')
        time_list_numeric = [int(time_list[0]),int(time_list[1]),float(time_list[2])]
        time_list_int = [int(time_list[0]),int(time_list[1]),int(round(float(time_list[2]),0))]
        
        date_list = date_str.split('-')
        date_list_int = [int(date_list[0]),int(date_list[1]),int(date_list[2])]
        
        date = ['DATE','Date','date']
        time = ['TIME','Time','time']
        if(value in time):
            if(form == 'intlist'):
                return time_list_int
            elif(form == 'numlist'):
                return time_list_numeric
            elif(form == 'strlist'):
                return time_list
            else:
                return time_str
        elif(value in date):
            if(form == 'intlist' or form == 'numlist'):
                return date_list_int
            elif(form == 'strlist'):
                return date_list
            else:
                return date_str       
        else:
            return [date_str,time_str]
    
    
    def clock_outstr(self,base = None, time_array = None):
        
        if(time_array != None):
            hour = time_array[0]
            minute = time_array[1]
            second = time_array[2]
        else:
            cdt = self.current_datetime('Time','numlist')
            hour = str(cdt[0])
            minute = str(cdt[1])
            second = int(round(cdt[2],0))        
        
        if(base == None):
            if(second < 10):
                second = '0'+str(second)
            else:
                second = str(second)
            time_str = str(hour)+':'+str(minute)+':'+str(second)
            return time_str
        elif(base == '18hr'):
            time_sec = int(second)+60*int(minute)+60*60*int(hour)
            hr_18 = time_sec/4800
            sec_rem = time_sec-hr_18*4800
            min_18 = sec_rem/120
            sec_rem = sec_rem-min_18*120
            sec_18 = sec_rem
            if(sec_18 < 10):
                sec_18 = '00'+str(sec_18)
            elif(sec_18 < 100):
                sec_18 = "0"+str(sec_18)
            else:
                sec_18 = str(sec_18)
            if(min_18 < 10):
                min_18 = '0'+str(min_18)
            else:
                min_18 = str(min_18)
            if(hr_18 < 10):
                hr_18 = '0'+str(hr_18)
            else:
                hr_18 = str(hr_18)
            time_str = str(hr_18)+':'+str(min_18)+':'+str(sec_18)
            return time_str
