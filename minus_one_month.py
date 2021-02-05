# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 02:24:06 2020

@author: asus
"""

from datetime import timedelta
from datetime import datetime

def subtract_one_month(dt0):
    dt0 = datetime.strptime(dt0, "%Y-%m")
    #dt1 = dt0.replace(days=1)
    dt2 = dt0 - timedelta(days=1)
    #dt3 = dt2.replace(days=1)
    dt3 = dt2.strftime("%Y-%m")
    return dt3

def month_interval(start, end):
    start = datetime.strptime(start, "%Y-%m")
    end = datetime.strptime(end, "%Y-%m")
    list_of_month = []
    
    while start < end:
        end = end.strftime("%Y-%m")
        end = subtract_one_month(end)
        end = end.replace('-', '_')
        list_of_month.append(end)
        end = end.replace('_', '-')
        end = datetime.strptime(end, "%Y-%m")
        
    list_of_month = list_of_month[::-1]
    print (list_of_month)
    