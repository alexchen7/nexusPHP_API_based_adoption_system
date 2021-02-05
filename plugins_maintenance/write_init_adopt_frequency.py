# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 01:20:06 2020

@author: asus
"""
from get_keepers import get_keepers

keeper_stats = get_keepers()

f = open("adopt_frequency","a")

for keeper in keeper_stats.keys():
    
    f.write("{} {}\n".format(keeper, '600'))
f.close()