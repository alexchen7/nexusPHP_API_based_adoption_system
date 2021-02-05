# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:59:12 2020

@author: asus
"""
from datetime import timedelta
from datetime import datetime
import os.path
import os
from collections import OrderedDict
import csv
from tqdm import tqdm
import copy

# change the current directory to file directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def low_seed_checker():
    
    """ check if keeper discarded any low seed torrent"""
    
    # initialize a list of file names
    list_filenames = []
    
    # initialize a list of exist file names
    list_exist_filenames = []
    
    # nitialize a list of exist days
    list_exist_dates = []
    
    # initialize list of missing file names
    list_missing_filenames= []
    
    # initialize the adoption dictionary of {uid:{username:alex,adoption:{date:{torrent:peers, torrent1:peers,...}}}}
    adoption_dictionary = OrderedDict()
    
    # initialize off duty dict: {uid:{username: alex, adoption:{date:[]}}}
    off_duty_dictionary = {}
    
    # initialize looked up dictionary to record finished torrents
    # looked_up{uid:{tid:latest_time}}
    looked_up = {}
    
    """DATE AND FILE NAME GENERATION START"""
    while True:
        
        # take start time and end time
#        assessment_start = input("请输入起始考核日期,按照YYYY-MM格式,完成后按enter")
#        assessment_end = input("请输入考核截止日期,按照YYY-MM格式,不包含本月,完成后按enter")
        assessment_start = '2019-07'
        assessment_end = '2020-07'
        
        # take a list of strs and add prefix to it
        list_dates = month_interval(assessment_start, assessment_end)
        
        # confirm the time interval
        confirm_interval = input ('请确认考核区间是从{}开始,{}结束。确认按enter，\
                                  否则输入任意字符后按enter。'.format \
                                  (list_dates[0],list_dates[-1]))
        
        # break the input loop and continue assessment
        if not confirm_interval:
            break
    
    # add the file prefix to the list of dates
    for date in list_dates:
        date = 'salary_report_' + date
        list_filenames.append(date)
        
    """DATE AND FILE NAME GENERATION END"""
    
    """CHECK MISSING FILES START"""
    # check if there are any missing files and create a list of exist filenames
    # also create a list of exist dates
    for filename in list_filenames:
        
        if os.path.exists(filename):
            list_exist_filenames.append(filename)
            
            dates = filename[-7:]
            list_exist_dates.append(dates)
        else:
            list_missing_filenames.append(filename)
    
    # report missing files
    if list_missing_filenames:
        confirm_missing_filenames = input('以下文件缺失,中断请输入任意值,否则按 \
        enter继续 \n{}'.format(list_missing_filenames))
        if confirm_missing_filenames:
            return
    """CHECK MISSING FILES END"""
    
    """READ PAST FILES & BUILD ADOPTION DICT START"""
    
    # build the adoption dictionary by opening files in list_exist_filenames
    for filename in tqdm(list_exist_filenames):
        
        # get the date
        date =filename[-7: ]
        
        f = csv.DictReader(open(filename, encoding="utf-8"))
        
        for line in f:
            
            # make sure it's not a summary line
            if line['用户id'] and line['种子id']:
                uid, username, tid = line['用户id'], line['用户名'], line['种子id']
                
                # only take the torrents that got bonus point:
                if line['单种魔力']:
                    # delete '魔' for easier reading
                    bonus_single_torrent = line['单种魔力'].replace('魔','')
                    bonus_single_torrent = float(bonus_single_torrent)
                    
                    # make sure it's not 0 bonus
                    if bonus_single_torrent > 0:
                        
                        # get num of peers
                        peers = line['同伴数'].replace('人','')
                        peers = int(peers)
                        
                        # in case the UID is not yet in adoption_dictionary
                        if uid not in adoption_dictionary:
                            adoption_dictionary[uid] = {'username':username}
                            adoption_dictionary[uid]['adoption'] = OrderedDict()
                            
                            adoption_dictionary[uid]['adoption'][date] = \
                            {tid:{'peers': peers}}
                        
                        # in case the DATE is not already in adoption_dictionary
                        elif date not in adoption_dictionary[uid]['adoption']:
                            adoption_dictionary[uid]['adoption'][date] = \
                            {tid:{'peers':peers}}
                            
                        # in case the UID and DATE all in adoption_dictionary
                        else:
                            adoption_dictionary[uid]['adoption'][date][tid] = \
                            {'peers':peers}
    """READ PAST FILES & BUILD ADOPTION DICT END"""
    
    """CHECK IF A LOW-SEED TORRENT WAS ABONDONDED FOR CONSECTIVE 2 MONTHS START"""
    # last valid month to prevent out of range err
    last_month = list_exist_dates[-1]
    
    # check each user by uid
    for uid in tqdm(adoption_dictionary):
        
        # current username
        username = adoption_dictionary[uid]['username']
        
        adoption_info = adoption_dictionary[uid]['adoption']
        
        # create tuple of valid dates to prevent key error in the adoption_dictionary
        valid_dates = set()
        for i in adoption_info.keys():
            valid_dates.add(i)
            
        # checking low torrent following a chronological order
        for date in adoption_info:
            
            # check torrent in a month
            for tid in adoption_info[date]:
                
                str_month = copy.deepcopy(date)
                
                # select torrent with peers less than 5
                try:
                    if int(adoption_info[date][tid]['peers']) < 5:
#                        print('done with date:{}, uid:{}, name:{}, torrent:{}'.format( \
#                          date, uid, username, tid))
                        # convert the date format to calculatable time
                        this_month = datetime.strptime(date, "%Y_%m")
                        
                        # in case this torrent has been looked up before
                        if (uid in looked_up.keys()) and \
                        (tid in looked_up[uid]):
                            
                            # in case record of this torrent has been looked
                            date_looked = \
                            datetime.strptime(looked_up[uid][tid], "%Y_%m")
                            if date_looked >= this_month:
#                                print ('當前時間{}之前已查看{}的{}到{}'.format \
#                                       (date, uid, tid, date_looked))
                                continue
                            
                        # in case this torrent have not been looked
                        failed_adoption_count = 0
                        
                        # make sure +2 month from this month exists
                        # prevent dict out range err
                        while \
                        datetime.strptime(add_one_month(add_one_month(str_month)), \
                                          "%Y_%m") \
                        <=  datetime.strptime(last_month, "%Y_%m"):
                            
                            # plus 1 month
                            str_month = add_one_month(str_month)
                            
                            
                            # confirm this month was assessed (have record.csv) to prevent err
                            if (str_month in list_exist_dates):
                                
                            # in case the keeper have adoption and have that
                            # torrent on the next month
                                if (str_month in adoption_info) and \
                                (tid in adoption_info[str_month]):
                                    
                                    # in case it's no longer low seed torrent,
                                    # otherwise keep checking
                                    if int(adoption_info[str_month][tid]['peers']) \
                                    >= 5:
                                        """write in looked_up dict start"""
                                        # write in looked_up dict
                                        if uid not in looked_up:
                                            looked_up[uid] = \
                                            {'username': username, tid:str_month}
                                        else:
                                            looked_up[uid][tid] = str_month
                                        """write in looked_up dict end"""
                                        break
                                    
                                    # if the it's still low seed torrent    
                                    elif int(adoption_info[str_month][tid] \
                                             ['peers']) < 5:
                                        """write in looked_up dict start"""
                                         # write in looked_up dict
                                        if uid not in looked_up:
                                            looked_up[uid] = \
                                            {'username': username, tid:str_month}
                                        else:
                                            looked_up[uid][tid] = str_month
                                        """write in looked_up dict start"""
                                        continue
                                    
                                # in case it's abondoned
                                else:
                                    failed_adoption_count += 1
                            
                            # if low seed torrent was abondoned 2 in a row
                            if failed_adoption_count >= 2:
                                
                                # write in off_duty dict
                                # in case this user has no record
                                if uid not in off_duty_dictionary:
                                    off_duty_dictionary[uid] = {'username': \
                                    username, 'adoption':{tid: [str_month]}}
                                # in case this user didn't have this tid on record
                                elif tid not in off_duty_dictionary[uid] \
                                ['adoption']:
                                    off_duty_dictionary[uid]['adoption'][tid] \
                                    = [str_month]
                                # in case this user has lost this tid for 2 months
                                else:
                                    off_duty_dictionary[uid]['adoption'][tid] \
                                    .append(str_month)
                            
                                # write in looked_up dict
                                if uid not in looked_up:
                                    looked_up[uid] = \
                                    {'username': username, tid:str_month}
                                else:
                                    looked_up[uid][tid] = str_month
                except:
                    print('issue with date:{}, uid:{}, name:{}, torrent:{}'.format( \
                          date, uid, username, tid))
                    print(off_duty_dictionary)
                    return adoption_dictionary
                            
                                    
                                    
                                        
                                        
                                        
                                
                            
                            
                    
                    # check in the following months, stop when peers reached 5
                    
            
            
    
    return off_duty_dictionary
        
    
    
    
    

def subtract_one_month(dt0):
    dt0 = datetime.strptime(dt0, "%Y-%m")
    #dt1 = dt0.replace(days=1)
    dt2 = dt0 - timedelta(days=1)
    #dt3 = dt2.replace(days=1)
    dt3 = dt2.strftime("%Y-%m")
    return dt3

def add_one_month(dt0):
    # be aware the format is slightly different from subtract_one_month
    dt0 = datetime.strptime(dt0, "%Y_%m")
    #dt1 = dt0.replace(days=1)
    dt2 = dt0 + timedelta(days=32)
    #dt3 = dt2.replace(days=1)
    dt3 = dt2.strftime("%Y_%m")
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
    return list_of_month