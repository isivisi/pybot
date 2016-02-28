import sys
import random

name = sys.argv[0]
msg = sys.argv[1]

filters 		= ['http://', 'www.', '.com', '.ca', '.org', '.gov', '.on', '.tk']
KICK_MSGS 		= ["please dont post links without permission.", "please ask before posting a link."]

for filter in filters:
	if filter in msg.lower() and "permit" not in self.getMode(name):
		
		pybotPrint("[FILTER][WEBSITES.PY] " + name, "filter")
		self.kick(name)
		self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])
		break