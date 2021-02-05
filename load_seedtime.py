 # -*- coding: utf-8 -*-

import csv

def load_seedtime(mod = 'normal'):
    # take uid, tid and an option for current month
    # return a dict of seeding time info eg. {uid:{tid: 
    #'total_seedtime': 60.25}}
    
    # get current month
    #month = datetime.now().strftime("%Y-%m")
    
    # creat an dic for output
    loaded_seedtime = {}    
    
    filename = 'seeding_time'
    if mod == 'test':
        filename = 'seeding_time_tmp'
        
    f = csv.DictReader(open(filename))
    
    # iterate through dic line by line
    for i in f:
        tid = i['种子id']
        uid = i['用户id']
        seedtime = i['做种时间']
        
        
        
        # in case uid is recorded
        if uid in loaded_seedtime:
            
            # in case there is a record of this torrent under this user
            if tid in loaded_seedtime[uid]:
                
                current_seedtime = float(loaded_seedtime[uid][tid])
                current_seedtime += float(seedtime)
                loaded_seedtime[uid][tid] = current_seedtime
            
            # in case there is record of this user but not this torrent
            else:
                loaded_seedtime[uid][tid] = seedtime
                
        # in case there is no record about this user
        else:
            loaded_seedtime[uid] = {tid: seedtime}
            
    return loaded_seedtime