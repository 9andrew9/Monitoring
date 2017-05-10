#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:13:23 2016

@author: Andrew Skvortsov

"""


import re
import imaplib
import email
import time
import dateutil.parser
from dateutil.tz import tzoffset, tzlocal
import module_mail as mail



ServerMail = '172.24.3.81'
SendMailFrom = "suz@europlan.ru" 
SendMailTo = [ 'avs85@europlan.ru' ]
ServerExch = 'srv-exch13-01.enterprise.local'
PathToFile = 'rake_file.txt'

Mess = " "
Mess += "From:suz@europlan" + "\n" + "Subject:Problem to MailBox of SUZ" + "\n" + "\n"
LinesSerch = re.compile(r'username=([^\s]+)\s+password=([^\s]+)')
n = int(time.time())


with open(PathToFile, "r") as f:
    for i in f:
        StringResult = LinesSerch.search(i)
        if StringResult:
            Loggin = StringResult.group(1)
            Password = StringResult.group(2)
            try:
                im = imaplib.IMAP4_SSL(ServerExch)
                im.login(Loggin, Password)
                im.select()
                typ, data = im.search(None, 'SEEN')
                s = 0
                for num in data[0].split():
                    typ, data=im.fetch(num,'(RFC822)')
                    msg=email.message_from_string(data[0][1])
                    d=dateutil.parser.parse(msg['Date']).astimezone(tzlocal())
                    c=time.mktime(d.timetuple())
                    if n - c>7200:
                        s+=1         
                if s > 0:
                    Mess += "\n" + "Loggin = %s , CounntMail = %s , Password = %s" % (Loggin, s, Password) + "\n"
                    #im.close()
                    im.logout()

            except Exception, e:
                Mess += "\n" + "Loggin = %s , CountMail = %s , Password = %s" % (Loggin, e, Password) + "\n"
                #pass
#sys.stdout.flush()
Mess += "\n" + "Please view mailbox in https://mail.europlan.ru/owa"
#print mess
if Mess.count('Loggin') > 1:
    send = mail.SendMail(ServerMail, SendMailFrom, SendMailTo, Mess)
    send

