import praw
import time
import json

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

def average(of_what, data):
    list_numbers = []
    for number in data:
        list_numbers.append(number[of_what])
    average = sum(list_numbers) / float(len(list_numbers))
    return average
        

r = praw.Reddit('Such Dogetipbot Delay (collecting stats about /u/dogetipbot) v0.1 by /u/MaximaxII')

tipbot = r.get_redditor('dogetipbot')

while True:
    comments = tipbot.get_comments(limit=limit)
    data = crawl(comments)

    short_data = [average('verification_created', data), average('verification_delay', data)] #x,y pair

    with open('dogetipdata.json') as f:
        json_data = json.load(f)
        
    json_data.append(short_data)

    with open('dogetipdata.json', 'wb') as f:
        json.dump(json_data, f)

    print 'Average delay for the last ' + str(limit) + ' verifications: ' + str(average('verification_delay', data))
    print 'Average time for the last' + str(limit) + ' verifications: ' + str(average('verification_created', data))
    time.sleep(885)
