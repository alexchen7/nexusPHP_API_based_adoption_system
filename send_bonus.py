# -*- coding: utf-8 -*-


import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime

def send_bonus(username, salary):
    # take 2 str of username and send bonus
    
    
    url = "https://torrent_site/amountbonus.php"
    # use your own cookies
    cookies = 
    
    data = {"username": username, "seedbonus": salary}
    
    r = requests.post(url, cookies = cookies, data = data)
	
    print ('给', username, '发了', salary, '魔力')