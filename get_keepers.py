def get_keepers():
    # return a dict of keepers with id as key and name as value 
    
    import requests
    import json
    from bs4 import BeautifulSoup
    import re
    
    # create an empty list of keepers
    keepers_stats = {}
    # set start point of keepers page initial to 0
    page_num = 0
    
    while 1:
        # generating pages
        url = 'https://torrent_site.me/users.php?class=keeper&page=' + str(page_num)
        # use your own cookies
        cookies = 
        r = requests.get(url, cookies = cookies)
        # pass page 'r' to soup
        soup = BeautifulSoup(r.text, features = 'lxml')
        # get <a> for keepers
        keepers = soup.findAll("a",{"class":"Keeper_Name"})
        if not keepers:
            # break while loop when over looped
            print ('页面拉取保种组人员名单完毕')
            return (keepers_stats)
        for keeper in keepers:
            user_id = re.sub("[^0-9]", "", keeper["href"])
            user_name = str(keeper.b)[3:-4]
            if user_name not in keepers_stats:
                keepers_stats[user_id] = user_name
        page_num += 1
        print ('已获取第', page_num, '页保种员信息。')
    #print ('已获取全部保种员名单,正在写入csv文件')
    #write_keeper_group(keepers_stats)
        
#    print ('页面拉取保种组人员名单完毕')
#    return (keepers_stats)