# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 12:11:43 2017

@author: Andrew Skvortsov

"""

import sys
import re
import requests

keys = {'key': 'f17b99d2b7e8ed6315b66389d1ebe8e4c81108bd'}
headers = {'Content-type': 'text/xml'}

with open('users_redmine', 'r') as f:
    lists = [ re.split('\s+', i) for i in f.readlines()]
    for list in lists:
        login = re.sub('@europlan.ru', '', list[3])
        name = list[1]#.decode('utf8').encode('cp866')
        raw1 = list[2]#.decode('utf8').encode('cp866')
        raw2 = list[0]#.decode('utf8').encode('cp866')
        lastname = (raw1 + " " + raw2) 
        password = ''
        mail = list[3]
        xml = """<user><login>%s</login>
             <firstname>%s</firstname>
             <lastname>%s</lastname>
             <password>%s</password>
             <mail>%s</mail></user>""" % (login, name, lastname, password, mail)
        print xml
        response = requests.post('http://misconduct.europlan.ru/users.xml?', params=keys, data=xml, headers=headers)
        var1 = response.text
        var2 = response.status_code
        var3 = response.url
        print var1, var2, var3
