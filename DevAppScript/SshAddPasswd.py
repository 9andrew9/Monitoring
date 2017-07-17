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

host = ['172.27.0.51']
user = "root"
secret = ",.h0rhfnbz"
command_linux_cmd = "hostname;hpacucli ctrl all show config"
data = []
try:
    for i in host:
        status = []
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=i, username=user, password=secret)
        stdin, stdout, stderr = client.exec_command(command_linux_cmd)
        data += stdout.read()  # + "\n" + stderr.read() + "\n"
        client.close()

except Exception as e:
    print(e)

# result = []
a = "".join([str(i) for i in data if i != "None"])
SearchRegexp = re.compile(r'\s+physicaldrive\s+([\w:]+)\s+[^,]+,[^,]+,\s+([^,]+),\s+([^\)]+)\)')
s = SearchRegexp.findall(a)
varObj = []
for obj in s:
    varObj.append(obj)
for res in varObj:
    if res:
        print(res)
        print("12")# res[0], "\t", "\t", res[1], res[2]
