# -*- coding: utf-8 -*-
import csv
from datetime import datetime
def write_keeper_report(tordic, uid, uname, now, test=''):
    # takes a torrent dict of a keeeper and write in csv
    print ('开始写入保种员', uname, '用户id', uid, '的本月报告')
    
    yy_mm = now.strftime("%Y_%m")
    
    filename = 'keeper_report_' + yy_mm
    
    # change filename in case of test situation
    if test:
        filename += '_test'
    
    with open(filename, 'a', newline = '', encoding = 'utf-8') as f:
        
        fieldnames = ['用户id', '用户名', '种子id', '体积', '做种时间', \
                      '上传量', '同伴数', '认领人', '发布组', '分类', '发布时间', \
                      '更新时间']
        thewriter = csv.DictWriter(f, fieldnames = fieldnames)
        
        # detect if the file is empty, write header in blank file only
        if not (f.tell()):
            thewriter.writeheader()
        
        for tid in tordic:
            
            
            #多余了tname = tordic[tid]['name']
            size = tordic[tid]['size']
            seedtime = tordic[tid]['seedtime']
            uploads = tordic[tid]['upload']
            
            # fill 0 if blank in seedtime and uploads
            if not tordic[tid]['seedtime']:
                seedtime = 0
            if not tordic[tid]['upload']:
                uploads = 0
                
            seeders = tordic[tid]['seeders']
            adopted = tordic[tid]['adopted']
            
            """剔除认领人的NULL"""
            adopted = adopted.split("|")
            # build a new str of adopted for output
            adopted_fixed = list()
            
            for i in adopted:
                if i and i.isdigit():
                    adopted_fixed.append(i)
                else:
                    print ('有NULL!!!!!!!!!!!!!!!!!!! \n \n')
            
            adopted_fixed = '|'.join([str(elem) for elem in adopted_fixed])
            """剔除认领人NULL完毕"""        
            
            #多餘了reso = tordic[tid]['resolution']
            #要更改cate = tordic[tid]['official']
            addedtime = tordic[tid]['addedtime']
            
            # in case a torrent is not assigned to a group
            if 'team' not in tordic[tid].keys():
                print ('缺少了team')
            team = tordic[tid]['team']
            category = tordic[tid]['category']
            
            thewriter.writerow({'用户id': uid, '用户名': uname, \
                                '种子id': tid, \
            '体积': size, '做种时间': seedtime, '上传量': uploads, \
            '同伴数': seeders, '认领人': adopted_fixed, \
            '发布组': team, '分类': category, '发布时间': addedtime, \
            '更新时间': str(datetime.now())})
    