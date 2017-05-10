# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:13:23 2016

@author: Andrew Skvortsov

"""
import smtplib


def SendMail(ServerMail, SendMailFrom, SendMailTo, message):
    connect = smtplib.SMTP(ServerMail)
    tolist = SendMailTo
    connect.sendmail(SendMailFrom, tolist, message) 
    connect.quit()