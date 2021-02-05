# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import re
import csv
from send_bonus import send_bonus
import os.path
from tqdm import tqdm
from datetime import datetime
from PM import PM
import time

##文件名全部没有通用性，已发列表需要改进添加更新日期到日期

#要使用检测文件是否存在功能来判断是否建库

#设置保种员额外奖励
"""!!! ONLY FOR CHN NEW YEAR!!!"""
extra_bonus = 0

now = datetime.now()

def send_salary():
    
    select_time = str(input('若发送其他月份的数据请按照YYYY-XX-DD输入日期,\
                            按Enter键则按照本月数据发放'))

    start = time.time()
    
    if select_time:
        select_time = datetime.strptime(select_time, "%Y-%m-%d")
        now = select_time
    

    
    # take a csv file and call send bonus to do action    
    yy_mm = now.strftime("%Y_%m")
    filename = 'salary_report_' + yy_mm

    # create global variable for progress in previous session
    loaded_sent_salary = set()
    
    # check the progress and record in loaded_sent_salary
    f = csv.DictReader(open('已发工资'))
    
    for i in f:
        loaded_sent_salary.add(i['uid'])
        
    
    loaded_report = {}
    
    g = csv.DictReader(open(filename, encoding="utf-8"))
    
    for i in g:
        
        if i['总魔力']:
            
            if i['用户id'] not in loaded_sent_salary:
                loaded_report[i['用户id']] = {'总魔力': i['总魔力']}
                loaded_report[i['用户id']]['备考'] = i['备考']
                loaded_report[i['用户id']]['用户名'] = i['用户名']
    

        
        
    # record users received salaries
    with open('已发工资', 'a', newline = '') as f:
        
        fieldnames = ['uid']
        
        
        thewriter = csv.DictWriter(f, fieldnames = fieldnames)
        
        thewriter.writeheader()
        
        for i in tqdm(loaded_report):
            
            # for passed keepers
            if float(loaded_report[i]['总魔力']) != 0:
                
                # bonus for passed keepers
                loaded_report[i]['总魔力'] = \
                str(float(loaded_report[i]['总魔力']) + extra_bonus)
                
                send_bonus(loaded_report[i]['用户名'], loaded_report[i]['总魔力'])
                thewriter.writerow({'uid': i})
                
            # for failed keepers
            else:
                PM(i, '温馨提示 本月保种员考核未通过', loaded_report[i]['备考'])
                thewriter.writerow({'uid': i})
                
    end = time.time()
    
    print ('保种组工资发放完毕，用时'+str(round(end - start,3))+'秒')
            
if __name__ == '__main__':
    send_salary()                
        
        