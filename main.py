# -*- coding: utf-8 -*-
from get_keepers import get_keepers
#from seeding_stats import seeding_stats
import time
from datetime import datetime
import os.path
import os

from write_keeper_group import write_keeper_group
from load_keeper_report import load_keeper_report
from write_keeper_report import write_keeper_report

from adoption_api_test import adoption_api

from tqdm import tqdm

# change the current directory to file directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    """input of options can be take by class"""
    #create csv file
    
#    with open('output.csv', 'w', encoding = 'utf-8') as csv_file:
#    csvwriter = csv.writer(csv_file, delimiter='\t')
    
#    # load saved torrent info from local
#    loaded_torrent, loaded_torrent_info = load_torrent_info()
#    loaded_adoption, loaded_adoption_info = load_first_adoption()
#    loaded_
    
    # count time
    
    start = time.time()
    
    # create global variable for loaded_id
    loaded_id = set()
    
    # record current time
        
    now = datetime.now()
    
    # initialize test situation
    test = ''
    
    # all users or entered users
    inspect_keepers = input('按Enter扫描全部保种员，否则输入保种员uid空格id')
    
    # if it's for test single user is by default test only
    if not inspect_keepers:
        test = input('输入任意值后按enter启动测试扫描')
    else:
        test = 1
    
    # variables used for checking if current month's stats were generated    
    yr_mo = datetime.now().strftime("%Y_%m")
    yr_mo_dd = datetime.now().strftime("%Y_%m_%d")
    
    
    # in case not collecting data for this month
    select_time = str(input('若处理其他月份的数据请按照YYYY-XX-DD输入日期,\
                            按Enter键则默认处理本月数据'))
    # if there is output
    if select_time:
        select_time = datetime.strptime(select_time, "%Y-%m-%d")
        now = select_time
        yr_mo = select_time.strftime("%Y_%m")
        
    file_name_keeper_report = 'keeper_report_' + yr_mo
    
    
    
    # change the name of the file and delete previous test in a test situation
    if inspect_keepers or test:
        file_name_keeper_report += '_test'
        file_name_salary_report = 'salary_report_' + yr_mo + '_test'
        file_name_mini_salary_report = 'miniSR' + yr_mo + '_test'
        file_name_keeper_list = 'keeper_list_' + yr_mo_dd + '_test'
        
        # delete previous test files
        if os.path.exists(file_name_keeper_report):
            os.remove(file_name_keeper_report)
        if os.path.exists(file_name_salary_report):
            os.remove(file_name_salary_report)
        if os.path.exists(file_name_mini_salary_report):
            os.remove(file_name_mini_salary_report)
        if os.path.exists(file_name_keeper_list):
            os.remove(file_name_keeper_list)
            
            
    
    
    # get finished progress
    if os.path.exists(file_name_keeper_report):
        loaded_id = load_keeper_report(now)
        print ('上次进度已完成', len(loaded_id), '人')
    
    # get keepers list from website
    keepers_dict = get_keepers()
    
    # write keeper dict to csv file
    write_keeper_group(keepers_dict, now, test)
    print ('已生成最新保种组名单')
    
    # in case only checking one keeper
    if inspect_keepers:
        # re-build dictionary of name and id
        keepers_dict = {}
        keepers_dict[inspect_keepers.split()[0]] = inspect_keepers.split()[1]
    
    # num of user being processed
    to_be_done = len(keepers_dict) - len(loaded_id)
    print ('还剩', to_be_done, '人')
    
    current_user = 0
    
    for uid in tqdm(keepers_dict):
                
        if uid not in loaded_id:
            
            current_user += 1
            print ('正在处理当前第', current_user, '个用户')
            
            user_name = keepers_dict[uid]
            
            # pass uid to seeding stats
            torrent_dict = adoption_api(uid, now)
            
            write_keeper_report(torrent_dict, uid, user_name, now, test)
            
        print ('完成当前第', current_user, '个用户,还剩', to_be_done - current_user, '人')
        # num of torrent processing for current use
        

    end = time.time()

    print ('保种组信息拉取，用时'+str(round(end - start,3))+'秒')      
#        for torrent_id in torrent_dict:
#            # num of detail been recorded
#            current_record = 0
#            current_torrent += 1
#            for stat in torrent_dict[torrent_id]:
#                current_record += 1
#                
#                
#                #csvwriter.writerow([name, keepers_dict[name], torrent_id, stat, torrent_dict[torrent_id][stat]])
#                print('正在处理', name, '第', current_user, '个用户', '第', \
#                      current_torrent, '个种子', '的第', current_record, '条记录')
#    
    
if __name__ == "__main__":
    main()
    
from salary_calc import *

if __name__ == "__main__":
    salary_calc()