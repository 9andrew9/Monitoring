#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri June 23 11:13:23 2017

@author: Andrew Skvortsov

"""
import re
import calendar
import datetime
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import string

import psycopg2

ServerMail = '172.24.3.81'
SendMailFrom = "report@europlan.ru"
SendMailTo = ['avs85@europlan.ru']  # , 'aao9@europlan.ru']
ServerExch = 'srv-exch13-01.enterprise.local'
DBH = '172.28.0.125'
DBPASS = 'trunk212'
DBPORT = '5434'
DBU = 'redmine_user'
DBN = 'sd'
User = "'aao9', 'pnd','rmb','san6','ivv4','avs85'"


def MonthDelta(self):
    days = calendar.monthrange(self.year, self.month)[1]
    print days
    return self - datetime.timedelta(days=days)


now = datetime.date.today()
mounth = MonthDelta(now).strftime("%Y-%m-%d")

users = "'aao9', 'pnd','rmb','san6','ivv4'"


#
def SendMail(ServerMail, SendMailFrom, SendMailTo, message):
    connect = smtplib.SMTP(ServerMail)
    tolist = SendMailTo
    connect.sendmail(SendMailFrom, tolist, message)
    connect.quit()


SqlQury = """with tt_cloased as
(
	select
		issueId,
		user_id "ClosedUserId",
		"UserName" "ClosedUserName",
		created_on "CloseTime",
		case when login in ({2}) then 1 else 0 end "ЗавершеноСотрудникамиИзСписка"
	from
	(
		select
			u.login,journalized_id as issueId, j.user_id, row_number () over (partition by journalized_id order by j.created_on desc ) rn, u.lastname || ' ' || u.firstname "UserName",j.created_on
		from
			journals as j
		inner join
			journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'status_id'
		join
			users u on
			(
				u.id = j.user_id

			)
		where
			jd.value::int in (14, 16)
			and
			j.created_on between '{0}' and '{1} 23:59:59.99'

	)tt
	where
		rn =1
		--and
		--issueId = 179498
), tt_issues as
(
	select 	distinct
		issueId,
		"ClosedUserId",
		"ClosedUserName",
		"CloseTime"
	from
		tt_cloased
	where
		"ЗавершеноСотрудникамиИзСписка" = 1
	union
	select distinct
		issueId,
		"ClosedUserId",

		(
			select  "UserName"
			from
			(
				select
					u.lastname || ' ' || u.firstname "UserName", row_number () over (partition by issueId order by j.created_on desc) rn
				from
					journals as j
				inner join
					journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'assigned_to_id'
				join
					users u on
					(
						u.id = jd.value::int
						and
						u.login in ('aao9', 'pnd','rmb','san6','ivv4')
					)
				where
					ttc.issueId = journalized_id
					and
					j.created_on <= ttc."CloseTime"
					and
					j.created_on between '{0}' and '{1} 23:59:59.99'
			)tt
			where
				rn =1
			limit (1)
		 )"ClosedUserName",
		"CloseTime"
	from
		tt_cloased ttc
	where
		exists (
				select
					journalized_id as issueId, u.lastname || ' ' || u.firstname "UserName", j.created_on, row_number () over (partition by issueId order by j.created_on desc)
				from
					journals as j
				inner join
					journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'assigned_to_id'
				join
					users u on
					(
						u.id = jd.value::int
						and
						u.login in ('aao9', 'pnd','rmb','san6','ivv4')
					)
				where
					ttc.issueId = journalized_id
					and
					j.created_on <= ttc."CloseTime"
					and
					j.created_on between '{0}' and '{1} 23:59:59.99'
		      )
),tt_issues2 as
(
	select tt1.*,
			(
				select
					max(j.created_on) "PrevStatDatetime"
				from
					journals as j
				inner join
					journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'status_id'
				where
					j.created_on < "CloseTime"
					and
					journalized_id = tt1.issueId
			)"PrevStatDatetime",
			tt2.created_on "NewDatetime"
	from
		tt_issues tt1
	join
		issues tt2 on
		(
			tt1.issueId = tt2.id
		)
)
select *, case when "ElapsedTimeHour"  < 24.0 then 'Быстрая' else 'Проектная' end "ПризнакЗадачи"
from
(
	select
		issueId,
		"ClosedUserName",
		"CloseTime","PrevStatDatetime", "NewDatetime",
		extract (epoch from ("CloseTime" - coalesce("PrevStatDatetime", "NewDatetime") ) ) / 3600  "ElapsedTimeHour"
	from
		tt_issues2
)tt""".format(mounth, now, users)

# print SqlQury
SqlQury2 = """with tt_cloased as
(
	select
		issueId,
		user_id "ClosedUserId",
		"UserName" "ClosedUserName",
		created_on "CloseTime",
		case when login in ('aao9', 'pnd','rmb','san6','ivv4') then 1 else 0 end "ЗавершеноСотрудникамиИзСписка"
	from
	(
		select
			u.login,journalized_id as issueId, j.user_id, row_number () over (partition by journalized_id order by j.created_on desc ) rn, u.lastname || ' ' || u.firstname "UserName",j.created_on
		from
			journals as j
		inner join
			journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'status_id'
		join
			users u on
			(
				u.id = j.user_id

			)
		where
			jd.value::int in (14, 16)
			and
			j.created_on between '2017-05-01' and '2017-05-31 23:59:59.99'

	)tt
	where
		rn =1
		--and
		--issueId = 179498
), tt_issues as
(
	select 	distinct
		issueId,
		"ClosedUserId",
		"ClosedUserName",
		"CloseTime"
	from
		tt_cloased
	where
		"ЗавершеноСотрудникамиИзСписка" = 1
	union
	select distinct
		issueId,
		"ClosedUserId",

		(
			select  "UserName"
			from
			(
				select
					u.lastname || ' ' || u.firstname "UserName", row_number () over (partition by issueId order by j.created_on desc) rn
				from
					journals as j
				inner join
					journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'assigned_to_id'
				join
					users u on
					(
						u.id = jd.value::int
						and
						u.login in ('aao9', 'pnd','rmb','san6','ivv4')
					)
				where
					ttc.issueId = journalized_id
					and
					j.created_on <= ttc."CloseTime"
					and
					j.created_on between '2017-05-01' and '2017-05-31 23:59:59.99'
			)tt
			where
				rn =1
			limit (1)
		 )"ClosedUserName",
		"CloseTime"
	from
		tt_cloased ttc
	where
		exists (
				select
					journalized_id as issueId, u.lastname || ' ' || u.firstname "UserName", j.created_on, row_number () over (partition by issueId order by j.created_on desc)
				from
					journals as j
				inner join
					journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'assigned_to_id'
				join
					users u on
					(
						u.id = jd.value::int
						and
						u.login in ('aao9', 'pnd','rmb','san6','ivv4')
					)
				where
					ttc.issueId = journalized_id
					and
					j.created_on <= ttc."CloseTime"
					and
					j.created_on between '2017-05-01' and '2017-05-31 23:59:59.99'
		      )
),tt_issues2 as
(
	select tt1.*,
			(
				select
					max(j.created_on) "PrevStatDatetime"
				from
					journals as j
				inner join
					journal_details as jd on j.id = jd.journal_id and jd.prop_key = 'status_id'
				where
					j.created_on < "CloseTime"
					and
					journalized_id = tt1.issueId
			)"PrevStatDatetime",
			tt2.created_on "NewDatetime"
	from
		tt_issues tt1
	join
		issues tt2 on
		(
			tt1.issueId = tt2.id
		)
)
select *, case when "ElapsedTimeHour"  < 24.0 then 'Быстрая' else 'Проектная' end "ПризнакЗадачи"
from
(
	select
		issueId,
		"ClosedUserName",
		"CloseTime","PrevStatDatetime", "NewDatetime",
		extract (epoch from ("CloseTime" - coalesce("PrevStatDatetime", "NewDatetime") ) ) / 3600  "ElapsedTimeHour"
	from
		tt_issues2
)tt
"""


def sqlsearch(DBN, DBU, DBPASS, DBH, DBPORT):
    print SqlQury
    conn = psycopg2.connect(database=DBN, user=DBU, password=DBPASS, host=DBH, port=DBPORT)
    if conn:
        print "Opened database successfully"
        cur = conn.cursor()
        cur.execute(SqlQury)
        rows = cur.fetchall()
        conn.close()
        return rows
    else:
        print "Error connect to databases"


mess = " "
# mess += "From:cc-qualit@europlan" + "\n" + "Subject:report" + "\n" + "\n"
mess += "Задачи" + ';' + "Работник" + ';' + "Время закрытия" + ';' + "Дата создания" + ';' + "Дата обновления" + ';' + "Затраченное время" + ';' + "Тип" + "\n"

sql = sqlsearch(DBN, DBU, DBPASS, DBH, DBPORT)
for row in sql:
    if row:
        # y = string.replace(row[5], ".", ",")
        convertfloat = str(row[5]).replace('.', ',')
        mess += ("%s;%s;%s;%s;%s;%s;%s\n" % (
            row[0], row[1], row[2], row[3], row[4], convertfloat, row[6]))

with open('Report.csv', 'w') as f:
    f.write(mess)

msg = MIMEMultipart()
part = MIMEBase('application', "octet-stream")
part.set_payload(open("Report.csv", "rb").read().decode('utf-8').encode('cp1251'))
part.add_header('Content-Disposition', 'attachment; filename="Report.csv"')
msg.attach(part)

# msg.attach(MIMEImage(file("image.png").read()))

send = SendMail(ServerMail, SendMailFrom, SendMailTo, msg.as_string())
print send
