"""
Copyright (C) 2014 TyA <tyler@faceyspacies.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
 subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import praw
import datetime
import time

# Configuration
username="username"
password="password"

subreddit_name="yourSubReddit"
defaultMode="any" # links and self are also valid options, however if self is the default, this bot doesn't make sense
selfOnlyDays=["Sunday", "Wednesday"]
ownersAccount="yourNameHere" #used to identify the bot owner in the useragent

timeBetweenChecks = 60 * 60 # 60 seconds == 1 minute * 60 == 1 hour
# END Configuration

r = praw.Reddit(ownersAccount + 's bot for r/' + subreddit_name + ' that manages SelfPost only days. Source: ')
r.login(username=username, password=password)
sub = r.get_subreddit(subreddit_name)


def isSelfOnlyDay():
   for item in selfOnlyDays:
      if(item == datetime.date.today().strftime("%A")):
         return True
		 
   return False
   
def isSelfOnly():
   return (r.get_settings(subreddit_name)["content_options"] == "self")
   
def goSelfOnly():
   r.update_settings(sub, content_options="self")
   
def backToDefault():
   r.update_settings(sub, content_options=defaultMode)

while(True):
    if(not r.is_logged_in()):
        r.login(username=username, password=password)
	
    isSelfDay = isSelfOnlyDay()
    isSelfOnlyMode = isSelfOnly()

    if (isSelfDay and isSelfOnlyMode):
        print "Subreddit in correct mode"
    elif (isSelfDay and not isSelfOnlyMode):
        goSelfOnly()
        print "Subreddit is now self only"
    elif (not isSelfDay and isSelfOnlyMode):
        backToDefault()
        print "Subreddit is no longer self only"
    else: #neither are true
        print "Subreddit is in correct mode"
		
    time.sleep(timeBetweenChecks)