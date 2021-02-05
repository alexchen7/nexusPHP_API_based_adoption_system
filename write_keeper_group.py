import csv
from datetime import datetime
def write_keeper_group(keeper_dict, now, test=''):
    # takes a dict and wrtie to a csv file with keepers' id, name and time   
    
    # record current time
    update_time = str(now.date())
    # generate file name
    filename = 'keeper_list_' + str(now.date()).replace("-","_")
    
    # change the filename in case of a test
    if test:
        filename += '_test'
    
    # creates a file with name based on current date
    with open(filename,'w', newline = '') as f:
        fieldnames = ['保种员id', '用户名', '更新时间']
        thewriter = csv.DictWriter(f, fieldnames = fieldnames)
        thewriter.writeheader()
        
        # looping the input dict
        for keeper_id in keeper_dict:
            
            
            # record information
            thewriter.writerow({'保种员id':keeper_id, \
                                '用户名':keeper_dict[keeper_id], \
                                '更新时间':update_time})
    print ('完成记录本月全部保种员名单')