#-*- utf-8 -*-
import re

class Expected_value:

    def __init__(self, varname1=0, varname2=0):
        self.varname2 = 0 if not varname2 else varname2
        self.varname1 = 0 if not varname1 else varname1
        
class Opiration_File:
        
    def OpenAndSafeFile(self):
        tolist=[]
        with open("iprak6.txt") as f:
           for line in f.readlines():
               if line:
                   tolist.append(line)
        return tolist


    def Label(self, a, b):
        self.a = "INSERT INTO public.developapp_vlan2250_dmz_rkt(ip, des) VALUES"    
        self.b = "('none', 'none')"
        
    def LabelAnd(self):     
        print "('none', 'none')"
 
def Result():       
    OpenFiles = Opiration_File() 
    OpenFiles.Label(a=2, b=3)
    #o = OpenFiles.OpenAndSafeFile()
    for i in OpenFiles.OpenAndSafeFile():
        d = re.split('\s+', i)
        if len(d) > 1:
            exp =  Expected_value(d[0], d[1])
            print "('%s', '%s')," % (exp.varname1, exp.varname2)
        
    OpenFiles.LabelAnd()


res = Result()
print res