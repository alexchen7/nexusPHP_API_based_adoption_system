# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 23:26:26 2020

@author: asus
"""
import requests
import json
from bs4 import BeautifulSoup
import re
import ast
from datetime import datetime

# use your own cookies
cookies = 

def PM(uid, title, body):
    
    data = {'receiver': str(uid), 'returnto': 'https://torrent_site.me/userdetails.php?id='+str(uid), \
            'subject': title, 'color': '0', 'font':'0','size':'0', \
            'body':body, 'save':'yes'}
    
    r = requests.post("https://torrent_site/takemessage.php",cookies = cookies, data = data)
    
    print ('已发送消息给id', uid)