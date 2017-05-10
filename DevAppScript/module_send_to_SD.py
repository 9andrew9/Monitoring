# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:40:38 2016

@author: root-avs
"""

import smtplib

connect = smtplib.SMTP('172.24.3.81')  # '172.24.3.81')
tolist = ['sd@europlan.ru']
message = '''�������, ������ ����.

����� ������� ��������� ������ �������� ������ ���������� sak24@europlan.ru 
<mailto:sak24@europlan.ru> (���)

� ���������,
������ ��������
��������� ���������� �������������� ��������������
��������
������, ������,
�������� �������, �. 16, ���. 1
������-����� "������������ �����"
���.: +7 (495) 786-80-80 ���. 50395
'''
connect.sendmail('kac2@europlan.ru', tolist, message)
connect.quit()
