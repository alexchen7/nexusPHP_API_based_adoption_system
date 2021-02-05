# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 23:55:44 2019

@author: asus
"""

import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
import csv
import math
import time
import os.path
import os
import shutil

from write_salary_report import write_salary_report
from write_seedtime import write_seedtime
from load_seedtime import load_seedtime

from tqdm import tqdm

"""工资自定义计算方程开始"""
# 认领名次合规数量的计算字典
def adoption_number_calc(adoption_rank, peers):
    return 2/(adoption_rank*(peers+1)**0.3)

adoption_number_ratio_function_dic = {'adoption_number_ratio_function': \
                                      adoption_number_calc}


def adoption_size_calc(adoption_rank, peers):
    return 2/(adoption_rank*(peers+1)**0.3)

adoption_size_ratio_function_dic = {'adoption_size_ratio_function': \
                                      adoption_size_calc}

def set_default_paras():
    global min_size_torrent, min_size_adopted, min_num_adopted, min_seedingtime, \
    adoption_number_ratio, adoption_number_ratio_function, \
    adoption_size_ratio, adoption_size_ratio_function, adoption_bonus_ratio, \
    code_official_group, code_invalid_category, salary_ratio, \
    size_for_salary_ratio, addedtime_for_salary_ratio, \
    seedingtime_for_salary_ratio, seeders_for_salary_ratio, \
    max_seeders_for_salary, min_size_first_adoption_ratio, \
    min_size_first_adoption
    # 单种体积下限(GB)
    min_size_torrent = 0.99
    
    # 一般保种员总合规种子体积下限(GB)
    min_size_adopted = 4096
    
    # 最低认领数量要求（个）
    min_num_adopted = 100
    
    # 最少做种时间(日)
    min_seedingtime = 12.5
    
    # 唯一认领，第一认领，第二认领···计为合规认领的0-1.00倍(个)
    adoption_number_ratio = [1, 1]
    
    # 唯一认领，第一认领，第二认领···合规认领数倍数使用的方程名字
    adoption_number_ratio_function = 'adoption_number_ratio_function'
    
    # 唯一认领，第一认领，第二认领···计入总合规标准种子体积的0-1.00倍
    adoption_size_ratio = [1, 1]
    
    #唯一认领，第一认领，第二认领···合规认领体积倍数使用的方程名字
    adoption_size_ratio_function = 'adoption_size_ratio_function'
    
    # 唯一认领，第一认领，第二认领···的工资记为种子标准魔力的0-1.00倍
    adoption_bonus_ratio = [1, 0.8, 0.6, 0.3]
    
    # 允许的官方发布小组代码
    code_official_group = ('1', '6', '9', '18', '22', '28', '31', '34', '35')
    
    # 不合规的分类，例如分集
    code_invalid_category = ('402')
    
    ### 工资系数
    salary_ratio = 1
    
    ### 工资体积系数0-1
    size_for_salary_ratio = 1
    
    ### 工资种子寿命系数0-1
    addedtime_for_salary_ratio = 1
    
    ### 工资做种时间系数0-1
    seedingtime_for_salary_ratio = 1
    
    ### 工资做种人数系数
    seeders_for_salary_ratio = 1
    
    ### 最多允许做种人数, 0为不限制
    max_seeders_for_salary = 0
    
    ### 最少第一认领体积
    min_size_first_adoption_ratio = 0.5
    
    min_size_first_adoption = min_size_adopted * min_size_first_adoption_ratio

"""工资自定义计算方程结束"""


def salary_calc():
    
    # aquire current time
    time_format = "%Y-%m-%d %H:%M:%S"
    
    # get current time
    now = datetime.now()
    
    # select which keeper_report to process
    select_time = str(input('若处理其他月份的数据请按照YYYY-XX-DD输入日期,\
                            按Enter键则默认处理本月数据'))
    
    """开始选择模式"""
    select_mod = str(input("请选择处理模式。若要更新做种时间请输入'yesyes'，否则 \
                           请输入enter"))
    select_standard = ''
    if select_mod != 'yesyes':
        # input time to ignore seeding time
        select_standard = input("输入time以启动无时间考核")
    """结束选择模式"""
    
    # update the time using if there is an input
    if select_time:
        select_time = datetime.strptime(select_time, "%Y-%m-%d")
        now = select_time
    
    # time the time takes to run the program
    start = time.time()
    
    # create a dict to store existed rules
    # with uid as the primary key
    existed_rule = dict()
    
    # name of the keeper rules' file
    keeper_rules_name = os.getcwd() + "\\Keepers_Rules\\rules"
    # load existed rules into a dict (keeper_rules_name)
    rf = csv.DictReader(open(keeper_rules_name, encoding = 'utf-8'))
    
    for i in rf:
        
        uid = i['用户id']
        min_size_torrent = float(i['最小单种体积'])
        min_size_adopted = float(i['最少总认领体积'])
        min_num_adopted = float(i['最少总认领数'])
        min_seedingtime = float(i['最少做种时间'])
        
        # convert str separated by space to list of intergers
        adoption_number_ratio = i['认领名次合格种子数比例']
        adoption_number_ratio = adoption_number_ratio.split(" ")
        # take out the last function in str
        adoption_number_ratio_function = adoption_number_ratio[-1]
        adoption_number_ratio = adoption_number_ratio[:-1]
        adoption_number_ratio = list(map(float, adoption_number_ratio))
        
        adoption_size_ratio = i['认领名次合格种子数体积比例']
        adoption_size_ratio = adoption_size_ratio.split(" ")
        # take out the last function in str
        adoption_size_ratio_function = adoption_size_ratio[-1]
        adoption_size_ratio = adoption_size_ratio[:-1]
        adoption_size_ratio = list(map(float, adoption_size_ratio))
        
        adoption_bonus_ratio = i['认领名次魔力比例']
        adoption_bonus_ratio = adoption_bonus_ratio.split(" ")
        adoption_bonus_ratio = list(map(float, adoption_bonus_ratio))
        
        # convert str separated by space to set of strs
        code_official_group = i['合格认领小组']
        code_official_group = code_official_group.split(" ")
        code_official_group = set(code_official_group)
        
        code_invalid_category = i['不合格认领分类']
        code_invalid_category = code_invalid_category.split(" ")
        code_invalid_category = set(code_invalid_category)
        
        salary_ratio = float(i['工资比例'])
        
        size_for_salary_ratio = float(i['工资体积系数'])
        addedtime_for_salary_ratio = float(i['工资种子寿命系数'])
        seedingtime_for_salary_ratio = float(i['工资做种时间系数'])
        seeders_for_salary_ratio = float(i['工资做种人数系数'])
        max_seeders_for_salary = int(i['最多允许同伴数'])
        min_size_first_adoption_ratio = float(i['最少第一认领占体积比'])
        
        
        existed_rule[uid] = {'min_size_torrent':min_size_torrent, \
                    'min_size_adopted':min_size_adopted, \
                    'min_num_adopted':min_num_adopted, \
                    'min_seedingtime':min_seedingtime, \
                    'adoption_number_ratio':adoption_number_ratio, \
                    'adoption_number_ratio_function':adoption_number_ratio_function, \
                    'adoption_size_ratio':adoption_size_ratio, \
                    'adoption_size_ratio_function':adoption_size_ratio_function, \
                    'adoption_bonus_ratio':adoption_bonus_ratio, \
                    'code_official_group':code_official_group, \
                    'code_invalid_category':code_invalid_category, \
                    'salary_ratio':salary_ratio, \
                    'size_for_salary_ratio':size_for_salary_ratio, \
                    'addedtime_for_salary_ratio':addedtime_for_salary_ratio, \
                    'seedingtime_for_salary_ratio':seedingtime_for_salary_ratio, \
                    'seeders_for_salary_ratio':seeders_for_salary_ratio, \
                    'max_seeders_for_salary':max_seeders_for_salary, \
                    'min_size_first_adoption_ratio':min_size_first_adoption_ratio}

    print ('加载订制规则完毕')
        
# open up keeper report and calc bonus points
    
    # make a blank keeper report dict
    keeper_report = {}
    
    # these keepers get 0 salary
    zero_salary = set()
    
    # make a set for all the keepers
    keeper_set = set()
    
    
    # the file name of keeper list
    keeper_list_filename = 'keeper_list_' + \
    str(now.date()).replace("-","_")
    # in case it's a test situation
    if select_mod != 'yesyes':
        keeper_list_filename += '_test'
    
    # load the set of keepers
    while not os.path.exists(keeper_list_filename):
        
        # in case the file is from another day
        keeper_list_filename = 'keeper_list_' + \
        str(input('当日保种组人员列表文件不存在，\
        请输入其他日期。以YYYY-MM-DD为标准'))
        
    with open(keeper_list_filename) as f:
        thereader = csv.reader(f.readlines())
        next(thereader)
        for i in thereader:
            keeper_set.add(i[0])
    
    # the file name of the keeper report to be read        
    yy_mm = now.strftime("%Y_%m")
    keeper_report_filename = 'keeper_report_' + yy_mm
    # in case of a test situation
    if select_mod != 'yesyes':
        keeper_report_filename += '_test'
    
    # openup the keeper report file
    f = csv.DictReader(open(keeper_report_filename, encoding="utf-8"))
    
    # open up keeper_report line by line
    print ('正在读取做种信息...')
    for i in f:
        
        user_id = i['用户id']
        user_name = i['用户名']
        torrent_id = i['种子id']
        #torrent_name = i['种子名']
        # size in GB, seedingtime in days and uploaded in GB
        size = round((int(i['体积'])) / (1024**3), 3)
        
        
        """请无视下面的"""
        # fix empty value from api
#        if not i['做种时间']:
#            seed_time = 0
#        else:
#            seed_time = round(float((int(i['做种时间'])) / (60*60*24)), 3)
            
        """停止无视"""
        # seedtime in days
        seed_time = round((int(i['做种时间'])) / (60*60*24), 3)

        # uploads in GB
        uploaded = round((int(i['上传量'])) / (1024**3), 3)
        peers = int(i['同伴数'])
        
        # prevent out range err
        if not (peers >= 1):
            peers = 1
        
        # set default keeper's adoption rank to 1
        adopted_rank = 1
        
        # process the '|' separated dict, generate a list with only adopted keepers
        adopted = i['认领人']
        adopted = adopted.split('|')
        adopted_keepers = []
        # if there is only one user adopted, it must be the keeper
        if len(adopted) == 1:
            adopted_keepers = adopted
            
        else:
            for j in adopted:
                if j in keeper_set:
                    adopted_keepers.append(j)
            # calculate adopted rank and update
            if len(adopted_keepers) != 1:                
                # fix api giving keepers not in the adoption list
                if user_id in adopted_keepers:
                    adopted_rank = adopted_keepers.index(user_id) + 1
                else:
                    print ('API Err')
                
        # update adopted users with only keepers and convert to str        
        adopted = ' '.join([str(elem) for elem in adopted_keepers])
                    
                    
        #resolution = i['清晰度']
        team = i['发布组']
        category = i['分类']
        addedtime = i['发布时间']
        date = i['更新时间']
        
        # in case this uid is in the dic
        if user_id in keeper_report:
            keeper_report[user_id]['做种情况'][torrent_id] = \
            {'体积': size, '做种时间': seed_time, \
             '上传量': uploaded, '同伴数': peers, '认领人': adopted, \
             '认领人表': adopted_keepers, '认领名次': adopted_rank, \
             '发布组': team, '分类': category, '发布时间': addedtime, \
             '更新时间': date, '合格': False, '单种备注':'', '合格体积': 0, \
             '合格数量': 0, '第一认领体积': 0}
            
        # in case this uid is not in the dic
        else:
            keeper_report[user_id] = {'用户名': user_name, '做种情况':{}}
            keeper_report[user_id]['做种情况'][torrent_id] = \
            {'体积': size, '做种时间': seed_time, \
             '上传量': uploaded, '同伴数': peers, '认领人': adopted, \
             '认领人表': adopted_keepers,'认领名次': adopted_rank, \
             '发布组': team, '分类': category, '发布时间': addedtime, \
             '更新时间': date, '合格': False, '单种备注':'', '合格体积': 0, \
             '合格数量': 0, '第一认领体积': 0}
            
    print ('信息读取完毕,正在判断未达标保种员')
    
   
            
    for i in tqdm(keeper_report):
        """default settings"""
        """此处为工资参数 PS.三个井号开头的系数一般不应修改！！"""
        set_default_paras()
        """默认工资参数截止 end of default settings"""
        
        """applying customized assessment parameters 应用订制考核参数"""
        if i in existed_rule.keys():
            min_size_torrent = existed_rule[i]['min_size_torrent']
            min_size_adopted = existed_rule[i]['min_size_adopted']
            min_num_adopted = existed_rule[i]['min_num_adopted']
            min_seedingtime = existed_rule[i]['min_seedingtime']
            adoption_number_ratio = existed_rule[i]['adoption_number_ratio']
            adoption_number_ratio_function = existed_rule[i]['adoption_number_ratio_function']
            
            adoption_size_ratio = existed_rule[i]['adoption_size_ratio']
            adoption_size_ratio_function = existed_rule[i]['adoption_size_ratio_function']
            
            adoption_bonus_ratio = existed_rule[i]['adoption_bonus_ratio']
            code_official_group = existed_rule[i]['code_official_group']
            code_invalid_category = existed_rule[i]['code_invalid_category']
            salary_ratio = existed_rule[i]['salary_ratio']
            size_for_salary_ratio = existed_rule[i]['size_for_salary_ratio']
            addedtime_for_salary_ratio = existed_rule[i]['addedtime_for_salary_ratio']
            seedingtime_for_salary_ratio = existed_rule[i]['seedingtime_for_salary_ratio']
            seeders_for_salary_ratio = existed_rule[i]['seeders_for_salary_ratio']
            max_seeders_for_salary = existed_rule[i]['max_seeders_for_salary']
            min_size_first_adoption_ratio = existed_rule[i]['min_size_first_adoption_ratio']
            min_size_first_adoption = min_size_adopted * min_size_first_adoption_ratio
        """finished applying customized assessment pars 完成应用订制化的考核参数"""
        
        
        
        # initialize number of torrents satisfied for bonus
        num_satisfied = 0
        # initialize size of torrents satisfied for bonus
        size_satisfied = 0
        # initialize size of torrents satisfied for first adoption
        size_first_adoption = 0
        # initialize num of torrents satisfied for first adoption
        num_first_adoption = 0
        # initialize number of torrents unsatisfied for seeding time
        num_seedingtime_unsatisfied = 0
        # initialize number of inofficial torrents
        num_unofficial = 0
        # initialize number of invalid category
        num_invalid_category = 0
        # initialize total size of valid non-first adoption
        size_non_first_adoption = 0
        # initialize total number of valid non-first adoption
        num_non_first_adoption = 0
        # initialize physical total size of valid non-first adoption
        size_physical_non_first_adoption = 0
        # initialize physcial total number of valid non-first adoption
        num_physical_non_first_adoption = 0
        
        # identifying keepers with zero salary
        if (len(keeper_report[i]['做种情况'])) < min_num_adopted:
            zero_salary.add(i)
            

        for j in keeper_report[i]['做种情况']:
            
            # initialize adoption number ratio and size ratio for this torrent
            this_adoption_number_ratio = 1
            this_adoption_size_ratio = 1
            
            """初始化该种参数"""
            # initialize customized assessment factors for this torrent
            # if the keeper is the first and only keeper adopted this torrent
            if (keeper_report[i]['做种情况'][j]['认领名次'] == 1) and \
            (len(keeper_report[i]['做种情况'][j]['认领人表']) == 1):
            
                this_adoption_number_ratio = adoption_number_ratio[0]
                this_adoption_size_ratio = adoption_size_ratio[0]
                
            else:
                
                # prevent out range err, in case the ranking is out of range
                # apply constant factor for qualified number and size calculation
                if (len(adoption_number_ratio) - 1) >= \
                keeper_report[i]['做种情况'][j]['认领名次']:
                    
                    this_adoption_number_ratio = \
                    adoption_number_ratio[keeper_report[i]['做种情况'][j]['认领名次']]
                    
                    this_adoption_size_ratio = \
                    adoption_number_ratio[keeper_report[i]['做种情况'][j]['认领名次']]
                # apply the function instide of the constant for undefined rankings
                else:
                    this_adoption_number_ratio = \
                    adoption_number_ratio_function_dic[adoption_number_ratio_function](keeper_report[i]['做种情况'][j]['认领名次'], \
                                                      keeper_report[i]['做种情况'][j]['同伴数'])
                    this_adoption_size_ratio = \
                    adoption_size_ratio_function_dic[adoption_size_ratio_function](keeper_report[i]['做种情况'][j]['认领名次'], \
                                                      keeper_report[i]['做种情况'][j]['同伴数'])
            """完成初始化该种参数"""
                
            """开始检测该种是否合规"""    
            
            # select torrents with seeding time shorter than 12.5 days
            if not keeper_report[i]['做种情况'][j]['做种时间'] >= min_seedingtime:
                # don't compare time when ignoring time AND has to be seeded
                # at least for some time
                if select_standard == 'time' and \
                keeper_report[i]['做种情况'][j]['做种时间'] != 0:
                    pass
                # in case it's not in "time ignored" mode or seeding time
                else:
                    keeper_report[i]['做种情况'][j]['单种备注'] += '做种时间不合格'
                num_seedingtime_unsatisfied += 1
#                print ('seeding time ok')
                
            # check if the torrent is official
            if not (keeper_report[i]['做种情况'][j]['发布组'] in \
            code_official_group):
                keeper_report[i]['做种情况'][j]['单种备注'] += '非官种 '
                num_unofficial += 1
                #print ('pass offcial check ok')
                
            # check if the torrent belongs to invalid group
            if keeper_report[i]['做种情况'][j]['分类'] in \
            code_invalid_category:
                keeper_report[i]['做种情况'][j]['单种备注'] += '分集 '
                num_invalid_category += 1
                #print ('first adption ok')
            
            # check if the torrent is larger than min_size_torrent
            if not (keeper_report[i]['做种情况'][j]['体积'] >= \
                             min_size_torrent):
                keeper_report[i]['做种情况'][j]['单种备注'] +=\
                '单种体积不合格 '
                #print ('size ok')
                            
            # max seeders allowed
            if (keeper_report[i]['做种情况'][j]['同伴数'] >= \
            max_seeders_for_salary) and \
            (max_seeders_for_salary != 0):
                keeper_report[i]['做种情况'][j]['单种备注'] +=\
                '做种人数超标 '
            
            """结束检测该种是否合规"""
            
            """准备该用户统计数据以填写备考"""
            
            if not keeper_report[i]['做种情况'][j]['单种备注']:
            
                # set torrent status to PASS
                keeper_report[i]['做种情况'][j]['合格'] = \
                True
                # add to num of satisfied torrents
                num_satisfied += 1 * this_adoption_number_ratio
                
                size_satisfied += \
                keeper_report[i]['做种情况'][j]['体积'] * \
                this_adoption_size_ratio
                
                keeper_report[i]['做种情况'][j]['合格体积'] = \
                keeper_report[i]['做种情况'][j]['体积'] * \
                this_adoption_size_ratio
                
                keeper_report[i]['做种情况'][j]['合格数量'] = \
                1 * this_adoption_number_ratio
                
                # add to the minimum FIRST adoption 
                if keeper_report[i]['做种情况'][j]['认领名次'] == 1:
                    keeper_report[i]['做种情况'][j]['第一认领体积'] = \
                    keeper_report[i]['做种情况'][j]['体积']
                    
                    size_first_adoption += \
                    keeper_report[i]['做种情况'][j]['体积']
                    num_first_adoption += 1
                elif keeper_report[i]['做种情况'][j]['认领名次'] > 1:
                    
                    size_non_first_adoption += \
                    keeper_report[i]['做种情况'][j]['合格体积']
                    num_non_first_adoption += \
                    keeper_report[i]['做种情况'][j]['合格数量']
                    
                    size_physical_non_first_adoption += \
                    keeper_report[i]['做种情况'][j]['体积']
                    num_physical_non_first_adoption += 1
                    
            """完成该用户用来填写备考的数据"""
        
        """开始生成备考"""
        # initialize comment                                        
        keeper_report[i]['备考'] = ''
        
        # lurking alart
        if len(keeper_report[i]['做种情况']) == 1 and ('-1' in \
        keeper_report[i]['做种情况'].keys()):
            keeper_report[i]['备考'] += '您就是超级大咸鱼了吧O.O'
        # add warning statement for seeding time ignoring mode
        if select_standard == 'time':
            keeper_report[i]['备考'] += '警告当前为虚拟考核。只要做种1分即通过 \
            结果仅供参考！'

        # generating user's comment
        keeper_report[i]['备考'] += '考核任务是合格种子数大于'+str(min_num_adopted) + \
        '个 合格种子体积大于'+str(min_size_adopted)+ 'GB。 已达标第一认领的体积' + \
        str(round(size_first_adoption, 3)) + 'GB。已达标第一认领数量：' + \
        str(round(num_first_adoption,3)) + '个。 已达标物理非第一认领体积' + \
        str(round(size_physical_non_first_adoption, 3)) + 'GB 折合后为' + \
        str(round(size_non_first_adoption, 3)) + 'GB。 已达标物理非第一认领数量为' + \
        str(round(num_physical_non_first_adoption, 3)) + '个 折合后为' + \
        str(round(num_non_first_adoption, 3)) + '个。 总合规体积为' + \
        str(round(size_satisfied, 3)) + 'GB 总合规数为' + \
        str(round(num_satisfied, 3)) + \
        '个。做种时间不达标的种子数'+ \
        str(num_seedingtime_unsatisfied)+'个 非官方种子数'+str(num_unofficial)+ \
        '个 分集种子数'+str(num_invalid_category)+'个 根据统计您当月考核'
        
        # in case the qualified number is unsatisfied
        if (num_satisfied < min_num_adopted):
            keeper_report[i]['备考'] += '种子数不合格 '
            zero_salary.add(i)
        # in case the qualified size is unsatisfied    
        if (size_satisfied < min_size_adopted):
            keeper_report[i]['备考'] += '种子体积不合格 '
            zero_salary.add(i)
            
        """REMOVED since 2020 JAN 15暂停考核第一认领数量和体积"""
#        if (size_first_adoption < min_size_first_adoption):
#            keeper_report[i]['备考'] += '第一认领体积不合格 '
#            zero_salary.add(i)
            
        if i not in zero_salary:
             keeper_report[i]['备考'] += '通过！获得魔力！'
        
        """备考生成完毕"""
        
    print ('未达标保种员分析完毕,准备更新做种时间')
    
    """开始更新总做种时间数据库"""
    # mode selection
    if select_mod == 'yesyes':
        
        # write seeding time to database
        write_seedtime(keeper_report, zero_salary, now)
        
        # load saved seedtime info
        loaded_seedtime = load_seedtime()
        
    else:
        # make a temporary copy of seeding_time file and remove later
        shutil.copyfile('seeding_time', 'seeding_time_tmp')
        write_seedtime(keeper_report, zero_salary, now, mod = 'test')
          
        # load saved seedtime info
        loaded_seedtime = load_seedtime(mod = 'test')
        # remove the tmp file
        os.remove("seeding_time_tmp")
    
    """完成更新总做种时间数据库"""
    
    """开始计算工资"""
    # calculating bonus
    for i in tqdm(keeper_report):
        
        """default settings"""
        """此处为工资参数 PS.三个井号开头的系数一般不应修改！！"""
        set_default_paras()
        """默认工资参数截止 end of default settings"""
        """applying customized assessment parameters 应用订制考核参数"""
        if i in existed_rule.keys():
            min_size_torrent = existed_rule[i]['min_size_torrent']
            min_size_adopted = existed_rule[i]['min_size_adopted']
            min_num_adopted = existed_rule[i]['min_num_adopted']
            min_seedingtime = existed_rule[i]['min_seedingtime']
            adoption_number_ratio = existed_rule[i]['adoption_number_ratio']
            adoption_number_ratio_function = existed_rule[i]['adoption_number_ratio_function']
            
            adoption_size_ratio = existed_rule[i]['adoption_size_ratio']
            adoption_size_ratio_function = existed_rule[i]['adoption_size_ratio_function']
            
            adoption_bonus_ratio = existed_rule[i]['adoption_bonus_ratio']
            code_official_group = existed_rule[i]['code_official_group']
            code_invalid_category = existed_rule[i]['code_invalid_category']
            salary_ratio = existed_rule[i]['salary_ratio']
            size_for_salary_ratio = existed_rule[i]['size_for_salary_ratio']
            addedtime_for_salary_ratio = existed_rule[i]['addedtime_for_salary_ratio']
            seedingtime_for_salary_ratio = existed_rule[i]['seedingtime_for_salary_ratio']
            seeders_for_salary_ratio = existed_rule[i]['seeders_for_salary_ratio']
            max_seeders_for_salary = existed_rule[i]['max_seeders_for_salary']
            min_size_first_adoption_ratio = existed_rule[i]['min_size_first_adoption_ratio']
            min_size_first_adoption = min_size_adopted * min_size_first_adoption_ratio
        """finished applying customized assessment pars 完成应用订制化的考核参数"""
        
        for j in keeper_report[i]['做种情况']:
            
            # initialize adoption bonus ratio
            this_adoption_bonus_ratio = 1
            
            """初始化该种参数"""
            # initialize customized assessment factors for this torrent
            # if the keeper is the first and only keeper adopted this torrent
            if (keeper_report[i]['做种情况'][j]['认领名次'] == 1) and \
            (len(keeper_report[i]['做种情况'][j]['认领人表']) == 1):
            
                this_adoption_bonus_ratio = adoption_bonus_ratio[0]
            else:
                
                # prevent out range err, in case it's invalid adoption
                if (len(adoption_bonus_ratio) - 1) >= \
                keeper_report[i]['做种情况'][j]['认领名次']:
                    
                    this_adoption_bonus_ratio = \
                    adoption_bonus_ratio[keeper_report[i]['做种情况'][j]['认领名次']]
                # set ratio to 0 for invalid adoption    
                else:
                    this_adoption_bonus_ratio = 0.3
            """完成初始化该种参数"""
            
            
            size = keeper_report[i]['做种情况'][j]['体积']
            
            # seedtime needs to pull up from database做种时间需要从数据库提取！！已经更改
            seedtime = float(loaded_seedtime[i][j])
            
            # calculate livetime
            livetime = now - \
            datetime.strptime(keeper_report[i]['做种情况'][j]['发布时间'], time_format)
            livetime = livetime.total_seconds()
            # convert livetime in seconds to months
            livetime = round(livetime / (60*60*24*30.5), 5)
            
            # write livetime for torrent
            keeper_report[i]['做种情况'][j]['生存时间'] = livetime
            
            # add total seedtime to the dic
            keeper_report[i]['做种情况'][j]['总做种时间'] = \
            float(loaded_seedtime[i][j])
            
            peers = int(keeper_report[i]['做种情况'][j]['同伴数'])

            uploads = keeper_report[i]['做种情况'][j]['上传量']
            
            # calculate salary for one torrent
            salary = round((100 * (size * size_for_salary_ratio) * \
                            (0.25 + 0.1 * math.log(1 + (livetime * 30.5 * \
                            addedtime_for_salary_ratio)/ 120) \
                             + (0.6 * math.log(1 + seedtime * \
                            seedingtime_for_salary_ratio) \
            / ((peers * seeders_for_salary_ratio)**0.6))) + 20 * uploads) * \
            this_adoption_bonus_ratio \
                                    * salary_ratio, 3)
            
            
#            # for test ONLY
#            if i in test.keys():
#                test[i][j] = {'size_for_salary_ratio' : size_for_salary_ratio\
#                    , 'addedtime_for_salary_ratio': addedtime_for_salary_ratio, \
#                   'seedingtime_for_salary_ratio':seedingtime_for_salary_ratio, \
#                   'seeders_for_salary_ratio' : seeders_for_salary_ratio, \
#                   'this_adoption_bonus_ratio':this_adoption_bonus_ratio, \
#                   'salary_ratio':salary_ratio, \
#                '名次': keeper_report[i]['做种情况'][j]['认领名次'], \
#                '认领人':keeper_report[i]['做种情况'][j]['认领人']}
#            else:
#                test[i] = {j:{'size_for_salary_ratio' : size_for_salary_ratio\
#                    , 'addedtime_for_salary_ratio': addedtime_for_salary_ratio, \
#                   'seedingtime_for_salary_ratio':seedingtime_for_salary_ratio, \
#                   'seeders_for_salary_ratio' : seeders_for_salary_ratio, \
#                   'this_adoption_bonus_ratio':this_adoption_bonus_ratio, \
#                   'salary_ratio':salary_ratio, \
#                   '名次': keeper_report[i]['做种情况'][j]['认领名次'], \
#                   '认领人':keeper_report[i]['做种情况'][j]['认领人']}}
#            # debug end!    
                
            """使用合格与否来判断"""
            # in case the torrent didn't satisfy the requirement, set salary=0
            if not keeper_report[i]['做种情况'][j]['合格']:
                salary = 0
                
            # record the reward for the torrent    
            keeper_report[i]['做种情况'][j]['单种魔力'] = salary
            
    """工资计算完毕"""

    # write the csv salary form for publication
    write_salary_report(keeper_report, zero_salary, now, select_standard, \
                        select_mod)
    
    end = time.time()
    
    print ('保种组工资计算完毕，用时'+str(round(end - start,3))+'秒')
    
    #return zero_salary, keeper_report
    return 'Done'
    
    #for i in keeper_report:
            
if __name__ == "__main__":
    continue_calc = input('是否继续进行其他考核？输入任意按enter进行其他考核。否按enter')
    if continue_calc:
        salary_calc()        
    
    # convert to csv
    from csv_to_excel import *
    
    