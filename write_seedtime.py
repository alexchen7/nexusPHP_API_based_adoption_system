# -*- coding: utf-8 -*-

import csv
from datetime import datetime
from tqdm import tqdm

def write_seedtime(salary_report, zero_salary, now, mod = 'write'):
    # take dict of salary_report
    
    #先看看在不在，不在的话加，在的话找最新的时间，以月份为标准，不在同月加，不同月才可相加
 
    
    filename = 'seeding_time'
    
    # for test mode
    if mod == 'test':
        filename = 'seeding_time_tmp'
    
    # get current month
    month = now.strftime("%Y-%m")
    
    # create a set for loaded records
    exsisting_seeding_info = set()
    
    # open the file first to load info so it's possible to avoid duplicate
    # updating of seeding time
    rf = csv.DictReader(open(filename))
    
    # iterate through the dict to load the saved info
    for i in rf:
        
        loaded_info = (i['种子id'], i['用户id'], i['更新时间'])
        
        # add each line to the loaded records
        exsisting_seeding_info.add(loaded_info)
    
    # openup the data base and prepare writing
    with open(filename, 'a', newline = '') as f:
        
        # 做种时间以天为单位
        fieldnames = ['种子id', '用户id', '做种时间', '更新时间']
        
        thewriter = csv.DictWriter(f, fieldnames = fieldnames)
        
        
        # iterate through the input dict
        for i in tqdm(salary_report):
            for j in salary_report[i]['做种情况']:
                tid = j
                uid = i
                # make the same tuple like loaded_info for duplication check (against 
                # exsisting_seeding_info)
                input_record = (tid, uid, month)
                
                # convert dur to days
                
                dur = round((salary_report[i]['做种情况'][j]['做种时间']),2)
                
                
                # write in if not exsisted in record and otherwise return funtion
                if input_record in exsisting_seeding_info:
                    print ('重复操作，本月已更新过做种时长记录。')
                else:
                    if uid in zero_salary:
                        dur = 0
                    thewriter.writerow({'种子id': tid, '用户id': uid, \
                    '做种时间': dur, '更新时间': month})
        
        
        
        
        
        