# zzparse: Zeit-Zahl (Time and Number) parsing

import time
import datetime
import math as mt
import tcheck 

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
    '''
    class: clock
     
    Description:  
     
    '''

    def __init__(self, in_date = None, in_time = None):
        global check
        check = tcheck.tcheck()

        self.init_datetime = datetime.datetime.now()
        self.date = in_date
        self.time = in_time        

    def str_to_date_list(self,string,delim='-'):
        test = check.type_test_print(string,str,'string','str_to_date_list') 
        if(not test):
            return test 
        
        array = string.split(delim)
        date_list = [int(array[2]),int(array[0]),int(array[1])]
        return date_list 

    def date_list_to_str(self,array):
        test = check.type_test_print(array,list,'array','date_list_to_str') 
        if(not test):
            return test 
         
        string = array[1]+'-'+array[2]+'-'+array[0] 
        return string
        
    def date_list_to_ordate(self, array):
        test = check.type_test_print(array,list,'array','date_list_to_ordate') 
        if(not test):
            return test 
                
        try:
            dateobj = datetime.date(int(array[0]),int(array[1]),int(array[2]))
            ordate = dateobj.toordinal()
            return ordate
        except:
            print("[date_list_to_ordate] Error: input array could not be parsed as a date_list")
            return False

    def str_to_ordate(self, string):
        date_list = self.str_to_date_list(string)
        if(date_list == False):
            return False 
        
        ordate = self.date_list_to_ordate(date_list) 
        if(ordate == False):
            return False
        else:
            return ordate        
        
    def days_between_dates(self,early,later):
        tot = self.str_to_ordate(early)
        if(tot == False):
            return False 

        tard = self.str_to_ordate(later)
        if(tard == False):
            return False                     
              
        day_dif = int(tard) - int(tot) 
        if(day_dif < 0):
            day_dif = (-1)*day_dif
        
        return day_dif


    def weekday(self,string):
        test = check.type_test_print(string,str,'string','weekday') 
        if(not test):
            return test         

        date_list = self.str_to_date_list(string)
        if(date_list == False):
            return False

        year, month, day = date_list
        
        weekday_nums  = [i for i in range(7)]
        weekday_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Sunday'] 
        weekday_dict = dict(zip(weekday_nums,weekday_names))

        weekday_val = datetime.date(year, month, day).weekday()
        return weekday_dict[weekday_val]

            
    def get_datetime(self,value='datetime',form='str'):
          
        time_now = datetime.datetime.now()
                                                     
        datevals = ['DATE','Date','date']
        timevals = ['TIME','Time','time']
        datetimevals = ['DATETIME','Datetime','datetime']


        time_str = str(time_now).split(' ')[1]         
        time_list = time_str.split(':')
        time_int = [int(time_list[0]),int(time_list[1]),int(round(float(time_list[2]),0))]
        time_num = [int(time_list[0]),int(time_list[1]),float(time_list[2])]
                     
        if(value in timevals):
            if(form == 'int'):   
                return time_int
            elif(form == 'num'):
                return time_num
            elif(form == 'list'):                
                return time_list
            elif(form == 'str'):
                return time_str
            else:
                print("[get_datetime] Error: 'form' value, "+form+" not recognized")
                return False

        date_str = str(time_now).split(' ')[0]
        date_list = date_str.split('-')     
        date_str = self.date_list_to_str(date_list)    
        date_list = [date_list[1],date_list[2],date_list[0]]
        date_int = [int(date_list[0]),int(date_list[1]),int(date_list[2])]

        date_str = self.date_list_to_str(date_list)

        if(value in datevals):
            if(form == 'int' or form == 'num'):                
                return date_int
            elif(form == 'list'):
                return date_list
            elif(form == 'str'):
                return date_str
            else:
                print("[get_datetime] Error: 'form' value, "+form+" not recognized")
                return False       

        dt_int = (date_int,time_int)
        dt_num = (date_int,time_num)
        dt_list = (date_list,time_list)
        dt_str = (date_str,time_str)
     
        if(value in datetimevals):
            if(form == 'int'):                     
                return dt_int
            elif(form == 'num'):                
                return dt_num
            elif(form == 'list'):                
                return dt_list
            elif(form == 'str'):
                return dt_str
            else:
                print("[get_datetime] Error: 'form' value, "+form+" not recognized")
                return False

        else:
            print("[get_datetime] Error: 'value' "+value+" not recognized; no action taken")
            return False

       
    
    def get_clock(self,base = None, time_array = None):
        
        if(time_array != None):
            hour = time_array[0]
            minute = time_array[1]
            second = time_array[2]
        else:
            cdt = self.get_datetime('Time','list')
            hour = str(cdt[0])
            minute = str(cdt[1])
            second = int(round(float(cdt[2]),0))        
        
        if(base == None or base == '24'):
            if(second < 10):
                second = '0'+str(second)
            else:
                second = str(second)

        elif(base == '18'):
            time_sec = int(second)+60*int(minute)+60*60*int(hour)
            hour = time_sec/4800
            sec_rem = time_sec-hour*4800
            minute = sec_rem/120
            sec_rem = sec_rem-minute*120
            second = sec_rem
            if(second < 10):
                second = '00'+str(second)
            elif(second < 100):
                second = "0"+str(second)
            else:
                second = str(second)
            if(minute < 10):
                minute = '0'+str(minute)
            else:
                minute = str(minute)
            if(hour < 10):
                hour = '0'+str(hour)
            else:
                hour = str(hour)

        elif(base == '6'):

            #seconds through a day:
            #
            #1 min = 60 s
            #1 hr  = 60 min = 60*60 (= 3600) s 
            #1 day = 24 hr  = 24*3600 (= 86400 s)
            #
            #86400/4 = 21600 s
            #
            #86400/6 = 14400 s
            #
            #00:00:00 :     0 s   ->    2:00:00:00
            #06:00:00 : 21600 s   ->    3:00:00:00
            #12:00:00 : 43200 s   ->    4:00:00:00
            #18:00:00 : 64800 s   ->    1:00:00:00
            #
            #format:
            #
            #watch : hour : minute : second 


            sixsec = 21600
            newday = 64800 

            time_sec = int(second)+60*int(minute)+60*60*int(hour)

            if(time_sec >= newday):
                watch == 1
            else:
                watch = (time_sec/sixsec)+2  

            sec_left = time_sec%sixsec 
            hour = sec_left/3600
            sec_rem = sec_left-hour*3600
            minute = sec_rem/60
            sec_rem = sec_rem-minute*60
            second = sec_rem            
             
            if(second < 10):
                second = '0'+str(second)
            else:
                second = str(second)
            if(minute < 10):
                minute = '0'+str(minute)
            else:
                minute = str(minute)
            hour = str(hour)            


        time_str = str(hour)+':'+str(minute)+':'+str(second)
        return time_str
