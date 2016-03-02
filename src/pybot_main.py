
# Pybot twitch irc bot
# Pybot is designed to monitor and admin your twitch chat

import sys
import threading

import os
from data import *
from irc import irc # yea its dumb
from pybotextra import *
from features.raffle import Raffle
from features.commands import Commands
from features.points import Points
from web import pybot_web

# VERSION INFO
PYBOT_VERSION = {"status": "BETA", "version": 0, "build": 121}

PWD = os.getcwd()

def main():
    pybotPrint("PYBOT %s VERSION %s BUILD %s" % (PYBOT_VERSION["status"], PYBOT_VERSION["version"], PYBOT_VERSION["build"]), "usermsg")

    # global data
    settings = Settings.instance()
    data = Data.instance()

    if (len(settings.filters) <= 0):
        pybotPrint("[pybot.main] Running with no filters")

    # create the irc connection and set the hook for the incoming feed
    con = irc(settings, feed, data)

    # connect separate features to the connection
    cmds = Commands(con)
    points = Points(con, con.chatters, settings, data)

    # start connection in new thread
    #thread.start_new_thread(con.connect, ())
    threading.Thread(target=con.connect).start()

    # start web services
    if (settings.web):
        web = pybot_web.pybot_web()

    while con.isClosed() == False:
        if (con.connected):
            input = raw_input("")
            if (input):
                con.msg(input)


    pybotPrint("[PYBOT] connection ended")
    exit()

# Once the irc connection is made it dumps the live feed here along with any events it finds
#TODO: create a feedHandler class to deal with specific feed events to clean stuff up
def feed(con, msg, event):
    #print msg
    if event == "server_cantchannel" or event == "server_lost": # couldn't connect to channel or lost connection, retry connection
        pybotPrint("Lost connection")
        con.retry()

    elif event == "nick_taken":
        pybotPrint("Nick has been taken!")
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

        if checkIfCommand(text, "!praffle"):
            if con.settings.raffle:
                raffle = Raffle(con, con.data)
                texsplit = text.replace("!praffle", '').split(" ")

                for pair in texsplit:
                    try:
                        split = pair.split(":")
                        raffle.setParam(split[0], split[1])
                    except:
                        nothing = 0

        elif checkIfCommand(text, "!pleave"):
            if con.isMod(name):
                con.msg("Bye!");
                con.close()
            else:
                con.msg('%s, you do not have access to this command.' % name)

        elif checkIfCommand(text, "!ppermit"):
            cmd_args = text.split(" ")
            if con.isMod(name):
                con.msg("%s can post a link" % cmd_args[2])
                con.addMode(cmd_args[2], "+permit")
            else:
                con.msg('%s, you do not have access to this command.' % name)

        elif checkIfCommand(text, "!pcommand add"):
            if con.isMod(name):
                trigger = msg.split(' ')[2]
                text = msg.split(' ')[3]
                permissions = msg.split(' ')[4].replace('\n\r', '')
                cmd = con.getCmdControl()
                cmd.addCommand(trigger, text, permissions)
            else:
                con.msg('%s, you do not have access to this command.' % name)
        elif checkIfCommand(text, "!plinkgrabber"):
            if con.isMod(name):
                if (con.linkgrabber):
                    con.linkgrabber = False
                    con.msg("Link grabber has been disabled!")
                else:
                    if con.settings.linkgrabber:
                        con.linkgrabber = True
                        con.msg("Link grabber has been enabled! post your links!")
            else:
                con.msg('%s, you do not have access to this command.' % name)

        elif checkIfCommand(text, "!quote"):
            if con.settings.quotes:
                quote = text.replace("!quote", "")
                if (quote.strip() != ""):
                    con.addQuote(name, text.replace("!quote", ""))
                    con.msg("Quote as been added.")
                else:
                    if (con.getRandomQuote()):
                        con.msg(con.getRandomQuote())

        elif checkIfCommand(text, "!plinkban"):
            cmd_args = text.split(" ")
            if con.isMod(name):
                #try:
                con.linkBan(cmd_args[2])
                #except:
                #    con.msg("%s, syntax: !plinkban <name>" % name)
            else:
                con.msg("%s, you do not have access to this command." % name)

        # user message for console
        if (con.isMod(name)):
            pybotPrint("%s : %s" % (name, text), "usermsg-mod")
        else:
            pybotPrint("%s : %s" % (name, text), "usermsg")

    elif event == "user_mode":
        name = msg.split(' ')[4].replace('\n\r', '')
        pybotPrint("%s is mode %s" % (name, con.getMode(name)))



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