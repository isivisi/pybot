#simple profanity filter using google

import sys
import random
import urllib
import urllib.request

name = sys.argv[0]
msg = sys.argv[1]

filterAPI 		= "http://www.wdyl.com/profanity?"
KICK_MSGS 		= [", swearing is not allowed.", "please refrain from profanity."]

url_msg = urllib.parse.urlencode({'q':msg})

grabbed = False
times = 0
while (grabbed == False):
    if times > 10:
        pybotPrint("[pybot.filter.websites] api timeout")
        break
    try:
        response = urllib.request.urlopen("%s%s" % (filterAPI, url_msg))
        grabbed = True
    except Exception as e:
        print(e)
        grabbed = False
    times += 1

html = ""
if grabbed:
    html = response.read().decode('utf-8')
    response.close()

if ("true" in html):
	pybotPrint("[FILTER][PROFANITY.PY] " + name, "filter")
	self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])
	self.kick(name)