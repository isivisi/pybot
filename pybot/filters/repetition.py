#repetition

import sys
import random

name = sys.argv[0]
msg = sys.argv[1]
db = self.accessDb("rep_db")

REP_AMMOUNT = 3

KICK_MSGS 		= ["please don't repeat yourself.", "don't repeat yourself"]

try:

	#database [user] = [last_message, count]
	if (msg.lower().strip() == db[name][0].lower().strip()):
		db[name][1] += 1
		
		if (db[name][1] >= REP_AMMOUNT):
			pybotPrint("[FILTER][REPETITION.PY] " + name, "filter")
			self.msg(name + " " + KICK_MSGS[random.randint(0, len(KICK_MSGS)-1)])
			self.kick(name)
			
	else:
		db[name][0] = msg
		db[name][1] = 1
			
except:
	db[name] = [msg, 1]				# create simple data structure
	
