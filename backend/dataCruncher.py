import json

def greatest(what, listed_object_data):
    b = {what: 0}
    for a in listed_object_data:
        if a[what] >= b[what]:
            b = a
    return b


def daily_cruncher(days=1, save=False):
    """ Creates a file from dogetipdata2.json with the last day's worth of data. """
    day = []
    with open('dogetipdata2.json') as f:
        dogetipdata = json.load(f)
    for a in dogetipdata:
        if a[0] >= (dogetipdata[-1][0] - (86400*days)): # 86400 seconds in a day
            day.append([a[0],a[1]])
    if save == True and days == 1:
        with open('24h.json', 'wb') as f:
            json.dump(day, f)
    return day

def records_cruncher():
    """ Creates records.json with all-time records """
    with open('hourly.json') as f:
        hourly = json.load(f)
    #Greatest hourly tipping rate
    max_tips = greatest('amount_tipped', hourly)
    max_verifications = greatest('many_comments', hourly)
    records = {'tips': max_tips,
                'verifications': max_verifications}
    with open('records.json', 'wb') as f:
        json.dump(records, f)
    return records


def send_to_site():
    """ Creates frontpagedata.json with all the data the front page needs """
    delay = daily_cruncher(2, False)
    records = records_cruncher()
    with open('hourly.json') as f:
        hourly_report = json.load(f)[-1]
    with open('frontpage.json', 'wb') as f:
        json.dump({'delay': delay,
                   'hourly': hourly_report,
                   'records': records}, f)
    
    
    
