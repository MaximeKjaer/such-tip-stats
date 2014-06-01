# -*- coding: cp1252 -*-
import praw
import time
import json
from collections import Counter
import os
import zipfile

data = []
limit = 5

########################
####### CRAWLERS #######
########################

def crawl(comments):
    i = 1
    data = []
    print "Getting an average delay time over the last 5 verifications."
    for comment in comments:
        #Print progress
        print i
        i = i+1
        #Crawl
        post_id = comment.id
        print post_id
        verification_created = comment.created_utc #
        parent = r.get_info(thing_id=comment.parent_id) # ONE API call --> 2 seconds.
        parent_created = parent.created_utc #
        verification_delay = verification_created - parent_created #
        data.append({'post_id': post_id,
                     'verification_created': int(verification_created),
                     'parent_created': int(parent_created),
                     'verification_delay': int(verification_delay)
                     })
    return data

def hourly_crawl(comments):
    i = 1
    data = []
    subreddits = []
    tipped = []
    for comment in comments:
        if i==1:
            newest = comment.created_utc
        if comment.created_utc < newest-3600:
            print "The latest hour's verifications have now been fetched"
            break
        else:
            subreddits.append(str(comment.subreddit))
            tipped.append(float(comment.body.encode('utf-8').split(' ^Dogecoins')[0].split('__^\xc3\x90')[-1]))
            last = comment.created_utc
        i = i+1
    print str(i) + " comments in an hour"
    data = {'amount_tipped': int(sum(tipped)),
             'many_comments': i-1,
             'hour': time.strftime('%H', time.gmtime(last)),
             'date': time.strftime('%d/%m/%y', time.gmtime(last)),
             'time': last,
             'subs': Counter(subreddits) }
    return data

########################
###### CRUNCHERS #######
########################

def daily_cruncher(days=1, save=False):
    """ Creates a file from dogetipdata2.json with the last day's worth of data. """
    day = []
    with open('server/JSON/dogetipdata2.json') as f:
        dogetipdata = json.load(f)
    for a in dogetipdata:
        if a[0] >= (dogetipdata[-1][0] - (86400*days)): # 86400 seconds in a day
            day.append([a[0],a[1]])
    if save == True and days == 1:
        with open('server/JSON/24h.json', 'wb') as f:
            json.dump(day, f)
    return day

def records_cruncher():
    """ Creates records.json with all-time records """
    with open('server/JSON/hourly.json') as f:
        hourly = json.load(f)
    #Greatest hourly tipping rate
    max_tips = greatest('amount_tipped', hourly)
    max_verifications = greatest('many_comments', hourly)
    records = {'tips': max_tips,
                'verifications': max_verifications}
    with open('server/JSON/records.json', 'wb') as f:
        json.dump(records, f)
    return records


def frontpage_data():
    """ Creates frontpagedata.json with all the data the front page needs """
    delay = daily_cruncher(2, False)
    records = records_cruncher()
    with open('server/JSON/hourly.json') as f:
        hourly_report = json.load(f)[-1]
    with open('server/JSON/frontpage.json', 'wb') as f:
        json.dump({'delay': delay,
                   'hourly': hourly_report,
                   'records': records}, f)

def zip_it_up():
    """ Creates a zip file with all the JSON, returns the unzipped size"""
    zf = zipfile.ZipFile("server/dogecoin_tip_data.zip", "w")
    folder_size = 0
    for dirname, subdirs, files in os.walk('server/JSON'):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
            folder_size += os.path.getsize(os.path.join(dirname, filename))
    zf.close()
    print "ZIP file created."
    data_size = str(folder_size/1024) + " KB"
    with open('server/JSON/frontpage.json') as f:
        almost_ready_data = json.load(f)
    almost_ready_data['data_size'] = data_size
    with open('server/JSON/frontpage.json', 'wb') as f:
        json.dump(almost_ready_data, f)




########################
###### COUNTERS ########
########################

def average(what, data):
    list_numbers = []
    for number in data:
        list_numbers.append(number[what])
    average = sum(list_numbers) / float(len(list_numbers))
    return average

def greatest(what, listed_object_data):
    b = {what: 0}
    for a in listed_object_data:
        if a[what] >= b[what]:
            b = a
    return b       

def mode(what, data): # TO DO!
    pass

########################
######## LOGIC #########
########################

r = praw.Reddit('Such Dogetipbot Delay (collecting stats about /u/dogetipbot) v0.1 by /u/MaximaxII')

tipbot = r.get_redditor('dogetipbot')
j = 4 #Depends on what time you launch it!
#0 for 15, 1 for 30, 2 for 45, 4 for 00
while True:
    j = j+1
    start = time.time()
    ## VERIFICATION DELAY ##
    comments = tipbot.get_comments(limit=limit)
    data = crawl(comments) # 10 seconds
    short_data = [average('verification_created', data), average('verification_delay', data)] #x,y pair
    
    with open('server/JSON/dogetipdata2.json') as f:
        json_data = json.load(f)
    json_data.append(short_data)
    with open('server/JSON/dogetipdata2.json', 'wb') as f:
        json.dump(json_data, f)
        
    print 'Average delay for the last ' + str(limit) + ' verifications: ' + str(average('verification_delay', data))
    print 'Average time for the last ' + str(limit) + ' verifications: ' + str(average('verification_created', data))
    json_data = []
    data = []
    ## HOURLY STATS ##
    if j == 4:
        #The maximum is supposed to be 300... but it sometimes exceeds that, somehow. So 500 it is.
        comments = tipbot.get_comments(limit=500) 
        data2 = hourly_crawl(comments)
        with open('server/JSON/hourly.json') as f:
            json_data = json.load(f)
        json_data.append(data2)
        with open('server/JSON/hourly.json', 'wb') as f:
            json.dump(json_data, f)
        print "HOURLY scan is now done"
        j = 0
        data2 = []
        json_data = []
        
    frontpage_data()
    daily_cruncher(1,True)
    zip_it_up()
    end = time.time()
    print "Going to sleep. Execution time was: " + str(end - start)
    time.sleep(900 - (end - start)) # exactly 15 minutes