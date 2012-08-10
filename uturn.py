#! /usr/bin/env python

# Imports
from simplemediawiki import MediaWiki, build_user_agent
import sys
from timestamper import *
import datetime
import time
import pprint

# Get wiki location
location = raw_input("Base URL to the wiki API (YOUR_WIKI_ROOT/api.php): ")
if (location[0:7].lower() != "http://"):
    location = "http://" + location
wiki = MediaWiki(location)
if wiki.normalize_api_url() is None:
    sys.exit("Invalid Wiki URL")

# Get login credetials
ua = build_user_agent("uturn", "0.1", "https://github.com/tomasreimers/wiki-uturn");
while True:
    username = raw_input("Username: ")
    password = raw_input("Password: ")
    if wiki.login(username, password) == True:
        break
    else:
        print "Invalid login"

# Get date to revert to
print "When would you like to revert to (IN UTC)?"
year = int(raw_input("Year: "))
month = int(raw_input("Month: "))
day = int(raw_input("Day: "))
hour = int(raw_input("Hour: "))
minute = int(raw_input("Minute: "))
second = int(raw_input("Second: "))
revertTime = datetime_to_timestamp(datetime.datetime(year, month, day, hour, minute, second))
if (revertTime > time.time()):
    sys.exit("This tool cannot go forward in time")

# Confirm
confirmation = raw_input("ARE YOU SURE YOU WANT TO RETURN THE WIKI TO THIS PERIOD OF TIME (Y/N): ")
if confirmation.lower() != "y":
    sys.exit("User aborted operation")

# Function to get all pages
def getAllResults(fromKey = ''):
    # No need to provide apnamespace b/c by default it only lists the main namespace
    results = wiki.call({'action': 'query', 'list': 'allpages', 'aplimit': '500', 'apfrom': fromKey})
    resultsPages = results['query']['allpages']
    # Continue as needed
    if ('query-continue' in results):
        resultsPages.extend(getAllResults(results['query-continue']['allpages']['apfrom']))
    return resultsPages

# Actually get all pages
allPages = getAllResults()

# Get an edit token, edit tokens are not unique to pages and we don't care about revision collision so no need to request multiple times
editTokenResult = wiki.call({'action': 'query', 'prop': 'info', 'intoken': 'edit', 'titles': allPages[0]['title']})
editToken = editTokenResult['query']['pages'][str(allPages[0]['pageid'])]['edittoken']

# deal with each page
for page in allPages:
    # get revisions until we are before date
    theRevision = None
    startAt = None
    while theRevision is None:
        callObj = {'action': 'query', 'prop': 'revisions', 'titles': page['title'], 'rvlimit': 500, 'rvprop': 'timestamp|user|content', 'rvdir': 'older'}
        if startAt != None:
            callObj['rvstartid'] = startAt
        results = wiki.call(callObj)
        revisions = results['query']['pages'][str(page['pageid'])]['revisions']
        for revision in revisions:
            # get time
            rvDatetime = datetime.datetime.strptime(revision['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            timestamp = datetime_to_timestamp(rvDatetime) 
            # check it
            if timestamp <= revertTime:
                theRevision = revision
                break
        # get next set of revisions
        if 'query-continue' in results:
            startAt = results['query-continue']['revisions']['rvstartid']
        # if no revision and nothing next, set as empty and end it
        elif theRevision is None:
            theRevision = {'delete': 'true'}
    # Create all the uTurn revision data
    if 'delete' in theRevision:
        content = ""
    else:
        content = theRevision['*']
    summary = "UTurn to " + str(revertTime)
    # Edit
    wiki.call({'action': 'edit', 'title': page['title'], 'summary': summary, 'text': content, 'token': editToken, 'bot': 'true'})
    # Inform User
    print "Done with '" + page['title'] + "'"  