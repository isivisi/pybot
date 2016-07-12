import sys
import random

#######################################################
################        settings         ##############
#######################################################

MIN_MSG_LEN 	= 7														# Minimum message length to filter
KICK_MSGS 		= ["please dont yell", 
				   "i'll cut you if you keep yelling"]

###

name = sys.argv[0]
msg = sys.argv[1]

if (len(msg) >= MIN_MSG_LEN):
	
	if (msg.isupper()):
		pybotPrint("[FILTER][UPPERCASE.PY] " + name, "filter")
		self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])
		self.kick(name) 