# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:44:30 2019

@author: asus
"""
import requests
import json
from bs4 import BeautifulSoup
import re
import ast
from datetime import datetime


def adoption_api(uid, now):
    # create a dict in the format of {tor_id:{'size':b, ...}}to return
    keeper_dict = {}
    
    # convert date in text format
    yr_mo = now.strftime("%Y-%m")
    
    # POST information to aquire adoption information of a keeper
    data = {'mod': 'ADOPTIONSTATS', 'action': 'INFO_COLLETION', 'uid': uid, 'date': yr_mo}
    
    # use your own cookies
    cookies = 
    # POST to aquire adoption information of a keeper
    r = requests.post("https://torrent_site.me/adoptionapi.php",cookies = cookies, data = data)
    user_profile = BeautifulSoup(r.text, features = 'lxml')
    
    # convert html format to text format
    stats_str = user_profile.p.text
    
    """以下为错误的尝试，请无视"""
#    # convert to dictionary format
#    position_of_true = stats_str.find('true')
#    # in case failed to grab the correct information
#    if position_of_true == -1:
#        print ('Error aquiring the data')
#        return
#    # change the small t to cap T, so dict can be built
#    stats_str_formatted = stats_str[ : position_of_true] + 'T' + \
#                            stats_str[position_of_true + 1 :]
    
    # convert to dictionary format

    #stats_dict = ast.literal_eval(stats_str_formatted)
    """错误的尝试结束"""
    
    # convert to dict format
    stats_dict = json.loads(stats_str)
    
    # put information in desired format
    if stats_dict['success']:
        
        # in case the keeper adopt 0 torrent!
        if stats_dict['data']:
            for torrent in stats_dict['data']:
                keeper_dict[torrent['torrent']] = {'size' : torrent['size'], \
                           'seedtime' : torrent['seedtime'], 'upload' : \
                           torrent['uploaded'], 'seeders' : torrent['seeders'], \
                           'adopted' : torrent['keeper'], 'addedtime' : torrent['added'], \
                           'team' : torrent['team'], 'category' : torrent['category']}
        else:
            keeper_dict['-1'] = {'size' : '1', \
           'seedtime' : '0', 'upload' : \
           '0', 'seeders' : '0', \
           'adopted' : '0', 'addedtime' : '1970-01-01 00:00:00', \
           'team' : '0', 'category' : '0'}
            
    return keeper_dict

