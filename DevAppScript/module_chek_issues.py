#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:13:23 2017

@author: Andrew Skvortsov

"""
import psycopg2
import datetime
import module_mail as mail

now = datetime.datetime.now()
DeltaTime = datetime.timedelta(hours=20)
pref = now - DeltaTime
n = pref.strftime('%Y-%m-%d %H')

ServerMail = '172.24.3.81'
SendMailFrom = "suz@europlan.ru"
SendMailTo = ['avs85@europlan.ru']
ServerExch = 'srv-exch13-01.enterprise.local'

conn = psycopg2.connect(database="sd", user="redmine_user", password="trunk212", host="172.28.0.26", port="5434")
print "Opened database successfully"

cur = conn.cursor()

cur.execute("select\
            i.id issue,\
            u.login,\
            i.start_date,\
            i.updated_on,\
            u.mail\
            from users u\
            left join issues i on u.id = i.assigned_to_id\
            where u.login in ('avs85', 'vsm9', 'sni1', 'ask', 'aim2', 'rmb')\
            and i.status_id in ('11', '12');")
rows = cur.fetchall()
conn.close()
for row in rows:
    if row:
        DateTime = row[3]
        if DateTime:
            DtL = DateTime + DeltaTime
            ToExpDay = DtL.strftime('%Y-%m-%d %H')
            NowDateTime = now.strftime('%Y-%m-%d %H')
            if ToExpDay == NowDateTime:
                mess = " "
                mess += "From:suz@europlan" + "\n" + "Subject:Deadline  the Expiration time issue" + "\n" + "\n"
                mess += (
                    '''Issue: %s Loggin: %s StartDate: %s LastUpdate: %s Email: %s \n http://sd.europlan.ru/issues/%s''' %
                    (row[0], row[1], row[2], row[3], row[4], row[0]))
                send = mail.SendMail(ServerMail, SendMailFrom, SendMailTo, mess)
                send
            else:
                print "%s != %s" % (ToExpDay, NowDateTime)
        else:
            print "Error item date"
