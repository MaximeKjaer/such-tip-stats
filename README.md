such-tip-stats
==============

Stats for /u/dogetipbot.

I'm trying to do weekly releases on mondays. No promises, though - it may be earlier or later.

/!\ Prototype / proof of concept / Work in progress. /!\


![alt text](http://i.imgur.com/xv9Asp0.png "Screenshot")


dogetipdata.json in the frontend is just some data that I've collected over the course of a day and a half.

##Dependencies
 - Python 2.7
 - Praw module
 - (in order to test the frontend (index.html), you may need to store it on a local server such as Wamp, or the one that Brackets uses -- Javascript doesn't like fetching local files with XHR)

##To-do list
 - add ability to find biggest single tip
 - fix the "hour" field on hourly.json
 - better responsive design (I've started, but mobile still isn't working as well as it should)

##Done list (will be in the next release)
 -  Get dataCruncher.py integrated into suchDelay.py
 -  Make the frontend accept the new JSON format
 -  Give the real size of the unzipped JSON data, + make it downloadable
