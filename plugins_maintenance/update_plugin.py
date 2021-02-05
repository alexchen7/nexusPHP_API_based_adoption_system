# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:06:10 2020

@author: asus
"""

import csv
import hashlib
def hundred_md5(text):
    hash= text
    for i in range(100):
        hash = hashlib.md5(hash.encode()).hexdigest()
    return hash
hash_list = []
# with open("salary_report_2019_11.csv",'r',encoding='utf8') as f:
#     csv_reader = csv.reader(f)
#     header = next(csv_reader)
#     for line in csv_reader:
#         if len(line[3])>82:print(len(line[3]))
#         hash = hundred_md5(line[3])
#         if line[3]:
#             print(line[3])
#             print(hash)
#             hash_list.append(hash)
#     print(hash_list)
with open("keeper_report_2020_01",'r',encoding='utf8') as f:
    csv_reader = csv.reader(f)
    header = next(csv_reader)
    for line in csv_reader:
        hash = hundred_md5(line[2])
        if line[2]:
            # print(line[0],line[7])
            hash_list.append(hash)
    print(hash_list)
"""用户id,用户名,种子id,体积,做种时间,上传量,同伴数,认领人,认领名次,发布组,分类,发布时间,生存时间,合格体积,第一认领体积,合格数量,总做种时间,单种魔力,总魔力,达标,更新时间
"""