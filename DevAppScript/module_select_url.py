# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:13:23 2016

@author: Andrew Skvortsov

"""
import requests


class CheckUrlExch:   
    def initr(self):
        global urls 
        urls = ""
        urls = []
        tolist = [ 'Autodiscover', 'ecp', 'oab', 'ews', 'Microsoft-Server-ActiveSync', 'rpc', 'mapi', 'owa' ]
        for l in tolist: 
            for i in range(9):
                if i:
                    result = "https://srv-exch13-0%s.enterprise.local/%s/healthcheck.htm" % (i, l)
                    urls.append(result)
        return urls

    def getr(self):         
        for list in urls:
            response = requests.get(list, verify=False)
            print response.status_code
            if response.status_code != 200:
                print (response.url, response.status_code)

checkurl = CheckUrlExch()
print checkurl.initr()
print checkurl.getr()
