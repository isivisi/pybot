# controller for pybot commands

import os
import thread
from pybotextra import * 

PWD = "/var/www/html/pybot"

class command:
	def __init__(self, trigger, args, message, permissions):
		self.trigger = trigger
		self.args = args
		self.message = message
		self.permissions = permissions
		
	def __cmp__(self, other):
		return (self.trigger == other)
		
	def getTrigger(self):
		return self.trigger
		
	def getMessage(self):
		return self.message
		
class cmdControl:
	def __init__(self, connection, db, channel):
		self.commands = []
		self.con = connection
		self.db = db
		self.channel = channel
		
		thread.start_new_thread(self.getCommandsFromDatabase, ())
		
	#def checkForCustomCommand
		
	def getCommandsFromDatabase(self):		
		try:
			result = self.db.query_r("SELECT * FROM command WHERE userName = '%s' " % self.channel);
			found = False
			for cmd in result:
				self.commands.append(command(cmd[2], cmd[3], cmd[4], cmd[5]))
				found = True
				
			if (found): pybotPrint("[CMDC] Custom commands loaded")
		except:
			pybotPrint("[CMDC] No custom commands found")
		
	def addCommand(self, trigger, args, message, permissions):
		self.db.query("INSERT INTO command values ('%s', null, '%s', %s, '%s', '%s')" % (trigger, args, message, permissions))
		self.commands.append(command(trigger, args, message, permissions))
			