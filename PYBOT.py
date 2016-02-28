# Pybot twitch irc bot
# Designed and written by isivisi
# Pybot is designed to monitor and admin your twitch chat

import os
from pybotextra import * 
import time
import json
import thread
import sys
import base64
from sql import sql
import urllib
from irc import irc # yea its dumb naming
import colorama
from termcolor import colored # no longer in use
colorama.init()

import socket


# VERSION INFO
PYBOT_VERSION = {"status": "BETA", "version": 0, "build": 121}

PWD = "/var/pybot"			# if I make a different version of pybot I need to change this!
NAME = "pybot_beta"
oauth = "oauth:dre0xdlwc7kggs74j6zcuttdl1p148"

HOST = ''
PORT = 9091

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#while 1:
#	try :
#		s.bind((HOST, PORT))
#		print "bound to %s:%s" %(HOST, PORT)
#		break
#
#	except:
#		PORT += 1

#s.listen(10)
#print "Listening for requests..."

			
def main():
	printHTML("PYBOT %s VERSION %s BUILD %s"  % (PYBOT_VERSION["status"], PYBOT_VERSION["version"], PYBOT_VERSION["build"]), "usermsg")
	
	mysql = sql()

	channel = sys.argv[1]
	filters = []
	try:
		f = sys.argv[2]
		
		f = f.split(':');
		for i in f:
			if (i != ""):
				filters.append(i)
	except:
		printHTML("[PYBOT] Running with no filters")
	
	# create the irc connection and set the hook for the incoming feed
	con = None
	customBot = mysql.query_r("SELECT * FROM customBot WHERE userName = '%s'" % channel)
	
	if (customBot):
		con = irc("irc.twitch.tv", 6667, "#"+channel, customBot[0][1], customBot[0][2], feed, filters, mysql)
	else:
		con = irc("irc.twitch.tv", 6667, "#"+channel, NAME, oauth ,feed, filters, mysql) # secure to be 6697
		
	thread.start_new_thread(con.connect, ())
	
	while con.isClosed() == False:
		nothing = 0
			
	
	printHTML("[PYBOT] connection ended")
	exit()
		
# Once the irc connection is made it dumps the live feed here along with any events it finds
#TODO: create a feedHandler class to deal with specific feed events to clean stuff up
def feed(con, msg, event):
	#print msg
	if event == "server_cantchannel" or event == "server_lost": # couldn't connect to channel or lost connection, retry connection
		printHTML("Lost connection")
		con.retry()
		
	elif event == "nick_taken":
		printHTML("Nick has been taken!")
		con.retry()
		
	elif event == "user_join":
		name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
		if (name != con.nick):
			# fancy join counter
			joins = getUserData(name)
			#con.msg("%s has connected to this channel %s time/s" % (name, joins))
			
			# so it doesnt spam when there are alot of people
			#if (con.getTotalUsers() <= 2):
			#	con.msg("Welcome to the stream %s!" % name)
			setUserData(name, joins + 1)
		
	elif event == "user_privmsg":
	
		name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
		text = msg.split("PRIVMSG")[1].replace('%s :' % con.channel, '')
		
		#printHTML( text)
		
		if con.isMod(name) == False and name != "jtv":
			con.filter(name, text)
			
		
		if "!pleave" in text:
			if con.isMod(name):
				con.msg("Bye!");
				con.close()
			else: 
				con.msg('%s, you do not have access to this command.' % name)
		
		elif "!ppermit" in text:
			cmd_args = text.split(" ")
			if con.isMod(name):
				con.msg("%s can post a link" % cmd_args[2])
				con.addMode(cmd_args[2], "+permit")
			else: 
				con.msg('%s, you do not have access to this command.' % name)
				
		elif "!pcommand add" in text:
			if con.isMod(name): 
				trigger = msg.split(' ')[2]
				text = msg.split(' ')[3]
				permissions = msg.split(' ')[4].replace('\n\r', '')
				cmd = con.getCmdControl()
				cmd.addCommand(trigger, text, permissions)
			else:
				con.msg('%s, you do not have access to this command.' % name)
		elif "!plinkgrabber" in text:
			if con.isMod(name): 
				if (con.linkgrabber == True):
					con.linkgrabber = False
					con.msg("Link grabber has been disabled!")
				else:
					if con.getSetting("setting_linkgrabber"):
						con.linkgrabber = True
						con.msg("Link grabber has been enabled! post your links!")
			else:
				con.msg('%s, you do not have access to this command.' % name)
				
		elif "!quote" in text:
			if con.getSetting("feature_quotes"):
				quote = text.replace("!quote", "")
				if (quote.strip() != ""):
					con.addQuote(name, text.replace("!quote", ""))
					con.msg("Quote as been added.")
				else:
					if (con.getRandomQuote()):
						con.msg('"%s" - %s' % (con.getRandomQuote(), con.user))
				
		elif "!plinkban" in text:
			cmd_args = text.split(" ")
			if con.isMod(name):
				try:
					con.linkBan(cmd_args[2])
				except:
					con.msg("%s, syntax: !plinkban <name>" % name)
			else:
				con.msg("%s, you do not have access to this command." % name)
			
		# user message for console
		if (con.isMod(name)):
			printHTML("%s : %s" % (name, text), "usermsg-mod")
		else:
			printHTML("%s : %s" % (name, text), "usermsg")
		
	elif event == "user_mode":
		name = msg.split(' ')[4].replace('\n\r', '')
		printHTML("%s is mode %s" % (name, con.getMode(name)))
		
				
	
	#print msg

# set user data for joins, currently useless
def setUserData(user, data):
	return 0


# grab user data for joins, currently useless 
def getUserData(user):
	return 0



#while 1:
#	conn, addr = s.accept()
#	data = conn.recv(2048)
#	if data:
#		print data
#	conn.close()

if __name__ == "__main__": 
	main()

	# add whois channel support!