# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from tqdm import tqdm

# translate team code to name
team_lib = {'1': 'HDS', '6': 'HDSky', '9': 'HDSTV', '18': 'HDSPad', \
            '22': 'HDSCD', '28': 'HDS3D', '31': 'HDSWEB', '34': 'HDSpecial', \
            '35': 'HDSWEB Episode', '36':'HDSAB'}

# translate category invalid code to category name
cate_invalid_lib = {'402':'分集'}

def write_salary_report(salary_report, zero_salary, now, select_standard = '', \
                        select_mod = ''):
    # takes dict of keeper report which contains uid as primary key, and
    # seeding stats as a secondary key.  teritary key is torrent id.
    # also takes a set of keeper ids with 0 salary
    
    # get time for file name
    yy_mm = now.strftime("%Y_%m")
    # concat time with file name header
    filename = 'salary_report_' + yy_mm
    mini_filename = 'miniSR' + yy_mm
    # change the filename in a test situation
    if select_mod != 'yesyes':
        filename += '_test'
        mini_filename += '_test'
    
    # if time is ignored
    if select_standard == 'time':
        filename += '_TimeIgnored'
    
    # initialize total salary per keeper
    total_salary = 0
    
    # initialize assesment value pass = 1 fail = 0
    assessment = 0
    
    # create a global variable for date
    date = ''
    
    # flag for write field name
    write_fieldname = True
    
    for i in tqdm(salary_report):
        
        
        user_name = salary_report[i]['用户名']
        observation = salary_report[i]['备考']
        
        with open(filename, 'a', newline = '', encoding = 'utf-8') as f:
            
            
            fieldnames = ['用户id', '用户名', '种子id', '体积', '做种时间', \
                          '上传量', '同伴数', '认领人', '认领名次', \
                          '发布组', '分类', '发布时间', '生存时间', '合格体积', \
                          '第一认领体积', '合格数量', \
                          '总做种时间', '单种魔力', '单种备注', '总魔力', '达标', \
                          '备考', '更新时间']
            
            thewriter = csv.DictWriter(f, fieldnames = fieldnames)
            
            # write filedname for the first time
            if write_fieldname:
                thewriter.writeheader()
                write_fieldname = False
                
            
            for j in salary_report[i]['做种情况']:
                
                uid = i
                tid = j
                
                # easier to read
                size = salary_report[i]['做种情况'][j]['体积']
                size = str(size) + 'GB'
                
                seedtime = salary_report[i]['做种情况'][j]['做种时间']
                seedtime = str(seedtime) + '日'
                
                
                # 待更改！！建库要更改！！！！！！！！已更改！
                total_seedtime = salary_report[i]['做种情况'][j]['总做种时间']
                total_seedtime = '共'+str(total_seedtime)+'日'
                
                uploads = salary_report[i]['做种情况'][j]['上传量']
                uploads = str(uploads) + 'GB上'
                
                seeders = salary_report[i]['做种情况'][j]['同伴数']
                seeders = str(seeders) + '人'
                
                adopted = salary_report[i]['做种情况'][j]['认领人']
                
                
                adoption_rank = salary_report[i]['做种情况'][j]['认领名次']
                adoption_rank = '第' + str(adoption_rank)
                
                # translate team code to name
                team = salary_report[i]['做种情况'][j]['发布组']
                if team in team_lib:
                    team = team_lib[team]
                else:
                    team = '非官方'
                
                # translate category invalid code to category name
                cate = salary_report[i]['做种情况'][j]['分类']
                if cate in cate_invalid_lib:
                    cate = cate_invalid_lib[cate]
                else:
                    cate = 'OK'
                    
                addedtime = salary_report[i]['做种情况'][j]['发布时间']
                
                live_time = salary_report[i]['做种情况'][j]['生存时间']
                live_time = str(live_time) + '个月'
                
                qualified_size = salary_report[i]['做种情况'][j]['合格体积']
                qualified_size = str(qualified_size) + 'GB符合'
                
                qualified_num = salary_report[i]['做种情况'][j]['合格数量']
                qualified_num = str(qualified_num) + '个符合'
                
                date = salary_report[i]['做种情况'][j]['更新时间']
                
                salary_per_tor = salary_report[i]['做种情况'][j]['单种魔力']
                salary_per_tor = str(salary_per_tor) + '魔'
                
                comment = salary_report[i]['做种情况'][j]['单种备注']
                
                first_adoption_size = salary_report[i]['做种情况'][j]['第一认领体积']
                first_adoption_size = str(first_adoption_size) + "GB第一"
                
                
                
                
                thewriter.writerow({'用户id': uid, '用户名':user_name, \
                                    '种子id': tid, \
                '体积': size, '做种时间': seedtime, '上传量': uploads, \
                '同伴数': seeders, '认领人': adopted, '认领名次': adoption_rank, \
                '发布组': team, '分类': cate, '发布时间': addedtime, \
                '生存时间': live_time, '总做种时间': total_seedtime, \
                '合格体积': qualified_size, '第一认领体积': first_adoption_size, \
                '合格数量': qualified_num, \
                '单种魔力': salary_per_tor, '单种备注': comment,'更新时间': date})
                
                # add to keeper's total salary
                total_salary += float(salary_per_tor[:-1])
            
            # set total salary 0 for keepers in zero salary
            if i in zero_salary:
                total_salary = 0
                assessment = 0
            else:
                assessment = 1
            
            # prepare uid, uname, date, to write
            uid = i
            # write the total salary for the keeper
            thewriter.writerow({'用户id': uid, '用户名': user_name, \
            '总魔力': total_salary, '达标': assessment, '备考':observation, \
            '更新时间': date})
    
            # write the summary file
            with open(mini_filename, 'a', newline = '', encoding = 'utf-8') as minif:
                fieldnames = ['用户id', '用户名', '总魔力', '达标', \
                          '备考', '更新时间']
                mini_writer = csv.DictWriter(minif, fieldnames = fieldnames)
                # only write filedname for the first time
                if not (minif.tell()):
                    mini_writer.writeheader()
                    
                mini_writer.writerow({'用户id': uid, '用户名':user_name, \
                                      '总魔力': total_salary, \
                                      '达标': assessment, '备考':observation, \
                                      '更新时间': date})

            # reset total salary
            total_salary = 0
            
    print ('工资表格写入完成')