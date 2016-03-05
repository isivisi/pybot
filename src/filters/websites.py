import sys
import random
import re

def raw_string(s):
    if isinstance(s, str):
        s = s.encode('string-escape')
    elif isinstance(s, unicode):
        s = s.encode('unicode-escape')
    return s

name = sys.argv[0]
msg = sys.argv[1]

REGEX = re.compile('((ftp|http|https):\/\/)?([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+.*)', re.IGNORECASE)
KICK_MSGS 		= ["please dont post links without permission.", "please ask before posting a link."]
if REGEX.search(msg) is not None:
	pybotPrint("[FILTER][WEBSITES.PY] " + name, "filter")
	self.kick(name)
	self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])
