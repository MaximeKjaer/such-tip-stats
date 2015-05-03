such-tip-stats
==============

Stats for /u/dogetipbot. Used to be live at [dogetips.info](http://www.dogetips.info).

I'm trying to do weekly releases on mondays. No promises, though - it may be earlier or later.


![alt text](http://i.imgur.com/NpWsnzc.png "Screenshot")


##Dependencies
 - Python 2.7
 - Praw module
 - The ```server``` folder is synced with my server's ```public_html``` folder through WebDAV.

##To-do list
 - add ability to find biggest single tip
 - Graph for average amount tipped
 - Button to convert all amounts to USD
 - Histogram with different amounts tipped
 - List of tips
 - Possibility for every user to go fetch their own tip data - biggest tip, average, median, total...
 - Automatic refresh (every minute?)
 - fix the "hour" field on hourly.json
 - Pull 500 comments every 2 seconds and scan for +/u/dogetipbot


##Done list
 -  Get dataCruncher.py integrated into suchDelay.py
 -  Make the frontend accept the new JSON format
 -  Give the real size of the unzipped JSON data, + make it downloadable

##Provided data
 - **frontpage.json:** data for the frontpage on default settings

 - **24h.json:** verification delay over the last 24 hours.
```[[UNIX timestamp, delay in seconds],[UNIX timestamp, delay in seconds]...]```

 - **hourly.json:** hour-for-hour data about distribution and amount of tips.

 - **records.json:** a list of records, plus the hourly data for the hour the record was broken

 - **dogetipdata2.json:** all the verification delays from day 1 (same syntax as 24h.json).

 - **dogecoin_tip_data.zip:** all the data in one ZIP file.
