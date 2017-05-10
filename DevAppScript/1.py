# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 12:14:06 2017

@author: Andrew Skvortsov

"""

import requests

keys = {'key': 'f17b99d2b7e8ed6315b66389d1ebe8e4c81108bd'}
lim = {'limit': '1'}
headers = {'Content-type': 'text/xml'}
login = 'andrew1'
name = 'Андрей'
lastname = 'Валентинович Скворцов'
password = 'nhfkfkf123'
mail = 'test5@europlan.ru'
name2 = {'name': 'avs85'}




xml = """<user><login>%s</login>
         <firstname>%s</firstname>
         <lastname>%s</lastname>
         <password>%s</password>
         <mail>%s</mail></user>""" % (login, name, lastname, password, mail)
print xml
"""
response = requests.post('http://misconduct.europlan.ru/users.xml?', params=keys, data=xml, headers=headers)
var1 = response.text
var2 = response.status_code
var3 = response.url
print var1, var2, var3
"""



