# -*- coding: utf-8 -*-
import csv
from datetime import datetime
def load_keeper_report(now):
    # load keepers to a set and return to prevent repeated scanning
    uid_loaded = set()
    
    yy_mm = now.strftime("%Y_%m")
    
    filename = 'keeper_report_' + yy_mm    
    
    
    
    fieldnames = ['用户id', '用户名', '种子id', '种子名', '体积', '做种时间', \
                      '上传量', '同伴数', '第一认领人', '清晰度', '官方', \
                      '更新时间']
    
    f = csv.DictReader(open(filename, encoding="utf-8"))
    
#    thewriter = csv.DictReader(f, fieldnames = fieldnames)
    
    for i in f:
        # add to set
        uid_loaded.add(i['用户id'])
        
    return (uid_loaded)