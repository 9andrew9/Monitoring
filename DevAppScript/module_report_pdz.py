#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:13:23 2017

@author: Andrew Skvortsov

"""

import psycopg2
import re
import requests


def connection_to_data_bases():
    try:
        conn = psycopg2.connect(database="devapp", user="root", password="trunk212", host="172.27.0.106", port="5432")
        print("Opened database successfully")
        cur = conn.cursor()
        # <editor-fold desc="Description">
        cur.execute("select msb,\
                     subdivisoin,\
                     outstanding_balance_contract,\
                     balance_delay_dfl,index_pdz\
                     from report_pdz;")
        # </editor-fold>
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("Opened database successfully")


def insert_to_flux_d_b(rows):
    if rows:
        for row in rows:
            a = row
            array = re.sub(r'\s+', '_', row[0]), re.sub(r'\s+', '_', row[1]), re.sub(r',', '.', row[4])
            proc = re.sub(r'%', '', array[2])
            column1 = array[0].encode('utf-8')
            column2 = array[1].encode('utf-8')
            column3 = a[2]
            column4 = a[3]
            column5 = proc
            xml = "division,name=%s,region=%s,obc=%s,ip=%s bdf=%s " % (column1, column2, column4, column5, column3)
            xml2 = "division_proc,name=%s,region=%s,obc=%s,ip=%s bdf=%s " % (column1, column2, column3, column4, column5)
            response = requests.post('http://172.27.0.106:8086/write?db=report_pdz', data=xml)
            response2 = requests.post('http://172.27.0.106:8086/write?db=report_pdz', data=xml2)
            # print response.url
            print(response.status_code, response2.status_code)
           # print(response2.status_code)

connect = connection_to_data_bases()
insert_to_flux_d_b(connect)
#print(insert)

# .decode('utf8').encode('cp866')

