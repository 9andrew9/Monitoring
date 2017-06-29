# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:13:23 2016

@author: Andrew Skvortsov

"""


import module_select_url as select
import module_insert     as insert 
import module_mail      as mail


checkurl = select.CheckUrlExch()
checkurl.initr() 
checkurl.getr()


#print  checkurl.getr()
'''
ServerMail = '172.24.3.81'
SendMailFrom = 'test@europlan.ru' 
SendMailTo = 'test@europlan.ru'
message = From:test@europlan.ru
Subject:test    

Alarm






if __name__ == "__main__":
    send = mail.SendMail(ServerMail, SendMailFrom, SendMailTo,  message)
    send






#RequestInsert = insert.Result
#print RequestInsert()

'''
