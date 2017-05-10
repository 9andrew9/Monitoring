#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:13:23 2016

@author: root-avs

"""

import re
import paramiko
import json
import tempfile
f = tempfile.TemporaryFile()



host = ['172.27.0.50', '172.27.0.51']
host2 = ['172.26.52.220']
user = "root"
secret = "fhbcnjrhfn"
command_linux_cmd = "hostname;hpacucli ctrl all show config"
data = []
try:
    for i in host:
        status = []
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=i, username=user, password=secret)
        stdin, stdout, stderr = client.exec_command(command_linux_cmd)
        data += stdout.read() # + "\n" + stderr.read() + "\n"
        client.close()

except Exception, e:
    print e


#result = []
a = "".join([str(i) for i in data if i != "None"])
#print a
#Pattern = "physicaldrive(.*)"
#SearchRegexp = re.compile(Pattern)
SearchRegexp = re.compile(r'\s+physicaldrive\s+([\w:]+)\s+[^,]+,[^,]+,\s+([^,]+),\s+([^\)]+)\)')
s = SearchRegexp.findall(a)
varObj = []
for obj in s:
    varObj.append(obj)
    #print obj
    #varObj += obj
    #print varObj[1],varObj[2]
    #print [res for res in varObj]
for res in varObj:
    if res:
        print res #res[0], "\t", "\t", res[1], res[2]