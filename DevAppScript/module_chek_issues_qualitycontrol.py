#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri June 23 11:13:23 2017

@author: Andrew Skvortsov

"""
import psycopg2
import datetime
import module_mail as mail

now = datetime.datetime.now()

"""
Status and Time Expiration
Select to Data Base table:

"id","name"
1,"Новая"
2,"В работе"
3,"Решена"
4,"Обратная связь"
5,"Закрыта"
6,"Отклонена"
7,"Закрыта. Переоценен"
8,"Эскалация"

Example:
StatusNewJob = '1'
DeltaTimeInJobNewJob = datetime.timedelta(hours=2)

StatusOldJob = '2'
DeltaTimeInAssignedToOldJob = datetime.timedelta(hours=72)

Job status '1'(Новая) > 2 hours to send mail expiration dead line
Job status  '2' (В работе) > 72 hours to send mail expiration dead line

End create function
Example
SearchJopToMailSend(DeltaTimeInJobNewJob, StatusNewJob)
SearchJopToMailSend(DeltaTimeInAssignedToOldJob, StatusOldJob)
"""

StatusNewJob = '1'
DeltaTimeInJobNewJob = datetime.timedelta(hours=2)

StatusOldJob = '2'
DeltaTimeInAssignedToOldJob = datetime.timedelta(hours=72)

"""
Next block connect to data base

ServerMail = 'IP'
SendMailFrom = "NameMailFromSend"
SendMailTo = ['NameMailToSend', 'NameMailToSend2']
ServerExch = 'NameMailServer'
DBH = 'IpDataBase'
DBPASS = 'PassDataBase'
DBPORT = 'PortDatabase'
DBU = 'UserDataBase'
DBN = 'NameDataBase'
"""

ServerMail = '172.24.3.81'
SendMailFrom = "cc-quality@europlan.ru"
SendMailTo = ['avs85@europlan.ru']
ServerExch = 'srv-exch13-01.enterprise.local'
DBH = '172.28.0.125'
DBPASS = 'trunk212'
DBPORT = '5434'
DBU = 'redmine_user'
DBN = 'qualitycontrol'


def sqlsearch(DBN, DBU, DBPASS, DBH, DBPORT, ST):
    conn = psycopg2.connect(database=DBN, user=DBU, password=DBPASS, host=DBH, port=DBPORT)
    if conn:
        print "Opened database successfully"
        cur = conn.cursor()
        cur.execute("""select
			        i.id,
                    ist.id,
                    i.created_on,
                    i.updated_on,
                    ist.name,
                    u.firstname,
                    u.lastname,
                    u.mail
                    from issues as  i
                    left join issue_statuses ist on i.status_id = ist.id
                    left join users u on i.assigned_to_id = u.id
                    where i.status_id in (%s);""" % ST)
        rows = cur.fetchall()
        conn.close()
        return rows
    else:
        print "Error connect to databases"


def SearchJopToMailSend(DLT, ST):
    print DLT
    sql = sqlsearch(DBN, DBU, DBPASS, DBH, DBPORT, ST)
    for row in sql:
        if row:
            print row[0], row[1]
            DateTime = row[3]
            if DateTime:
                DtL = DateTime + DLT
                ToExpDay = DtL.strftime('%Y-%m-%d %H')
                NowDateTime = now.strftime('%Y-%m-%d %H')
                if ToExpDay == NowDateTime:
                    print (row[0], row[4], row[2], row[3], row[7], row[0])
                    mess = " "
                    mess += "From:cc-quality@europlan" + "\n" + "Subject:Deadline  the Expiration time issue" + "\n" + "\n"
                    mess += ("Задача: %s\nСтатус: %s больше %s часов.\n"
                             "Дата создания: %s.\n"
                             "Дата обновления: %s.\n"
                             "Email: %s\n"
                             "http://qualitycontrol.europlan.ru/issues/%s" % (row[0], row[4], DLT, row[2],
                                                                              row[3], row[7], row[0]))
                    send = mail.SendMail(ServerMail, SendMailFrom, SendMailTo, mess)
                    return send
                else:
                    print "%s != %s" % (ToExpDay, NowDateTime)
            else:
                print "Error item date"

SearchJopToMailSend(DeltaTimeInJobNewJob, StatusNewJob)
SearchJopToMailSend(DeltaTimeInAssignedToOldJob, StatusOldJob)

