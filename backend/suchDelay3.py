# -*- coding: cp1252 -*-
import praw
import time
import json
from collections import Counter

data = []
limit = 5

def crawl(comments):
    i = 1
    data = []
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
            print "breaking"
            break
        else:
            subreddits.append(str(comment.subreddit))
            tipped.append(float(comment.body.split(' ^Dogecoin(s)')[0].split(' ')[-1][4:-1]))
            last = comment.created_utc
        i = i+1
    print str(i) + " comments in an hour"
    data = {'amount_tipped': int(sum(tipped)),
             'many_comments': i-1,
             'hour': time.strftime('%H', time.gmtime(last)),
             'date': time.strftime('%d/%m/%y', time.gmtime(last)),
             'subs': Counter(subreddits) }
    return data
        

def average(of_what, data):
    list_numbers = []
    for number in data:
        list_numbers.append(number[of_what])
    average = sum(list_numbers) / float(len(list_numbers))
    return average
        

r = praw.Reddit('Such Dogetipbot Delay (collecting stats about /u/dogetipbot) v0.1 by /u/MaximaxII')

tipbot = r.get_redditor('dogetipbot')
j = 3
while True:
    j = j+1
    start = time.time()
    ## VERIFICATION DELAY ##
    comments = tipbot.get_comments(limit=limit)
    data = crawl(comments) # 10 seconds
    short_data = [average('verification_created', data), average('verification_delay', data)] #x,y pair
    
    with open('dogetipdata2.json') as f:
        json_data = json.load(f)
    json_data.append(short_data)
    with open('dogetipdata2.json', 'wb') as f:
        json.dump(json_data, f)
        
    print 'Average delay for the last ' + str(limit) + ' verifications: ' + str(average('verification_delay', data))
    print 'Average time for the last' + str(limit) + ' verifications: ' + str(average('verification_created', data))
    json_data = []
    data = []
    ## HOURLY STATS ##
    if j == 4:
        comments = tipbot.get_comments(limit=300) #The absolute maximum in an hour.
        data2 = hourly_crawl(comments)

        with open('hourly.json') as f:
            json_data = json.load(f)
        json_data.append(data2)
        with open('hourly.json', 'wb') as f:
            json.dump(json_data, f)
            
        print "done"
        j = 0
        data2 = []
        json_data = []
    
    
    end = time.time()
    time.sleep(900 - (end - start)) # exactly 15 minutes

