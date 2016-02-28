#simple profanity filter using google

import sys
import random
import urllib2
import urllib

name = sys.argv[0]
msg = sys.argv[1]

filterAPI 		= "http://www.wdyl.com/profanity?q="
KICK_MSGS 		= [", swearing is not allowed.", "please refrain from profanity."]

url_msg = urllib.quote(msg)
response = urllib2.urlopen("%s%s" % (filterAPI, url_msg))
html = response.read()
response.close()

if ("true" in html):
	printHTML("[FILTER][PROFANITY.PY] " + name, "filter")
	self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])
	self.kick(name)