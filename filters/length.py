import sys
import random

name = sys.argv[0]
msg = sys.argv[1]

MAX_CHAR_LEN = 250

KICK_MSGS 		= ["your message was too long, please split it up into multiple parts.", "please split your message into multiple parts."]

if (len(msg) > MAX_CHAR_LEN):
	pybotPrint("[FILTER][LENGTH.PY] " + name, "red")
	self.kick(name)
	self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])