
# Pybot twitch irc bot
# Pybot is designed to monitor and admin your twitch chat



import sys
import threading
import json

import os

os.chdir(os.path.dirname(__file__) or '.')

from pybot.data import *
from pybot.irc import irc # yea its dumb
from pybot.pybotextra import *
from pybot.features.raffle import Raffle
from pybot.features.commands import Commands
from pybot.features.points import Points
from pybot.features.linkgrabber import Linkgrabber
from pybot.features.quotes import Quotes
from pybot.web import pybot_web
import pybot.globals as globals

# VERSION INFO
PYBOT_VERSION = {"status": "BETA", "version": 0, "build": 121}

PWD = os.getcwd()

def main():
    settings = globals.settings
    pybotPrint("PYBOT %s VERSION %s BUILD %s" % (PYBOT_VERSION["status"], PYBOT_VERSION["version"], PYBOT_VERSION["build"]), "usermsg")

    if len(json.loads(settings.config['filters']['activeFilters'])) <= 0:
        pybotPrint("[pybot.main] Running with no filters", "log")

    # create the irc connection and set the hook for the incoming feed
    con = irc(feed)
    globals.con = con

    # connect separate features to the connection
    cmds = Commands(con)

    if (toBool(settings.config['points']['enabled'])):
        points = Points(con, con.chatters, settings, data)

    if (toBool(settings.config['features']['linkgrabber'])):
        linkgrabber = Linkgrabber(con)

    if (toBool(settings.config['features']['quotes'])):
        quotes = Quotes(con)

    # start connection in new thread
    #thread.start_new_thread(con.connect, ())
    threading.Thread(target=con.connect).start()

    # start web services
    if (toBool(settings.config['web']['enabled'])):
        web = pybot_web.pybot_web(con)
        threading.Thread(target=web.startWebService).start()
    while con.isClosed() == False:
        if (con.connected):
            inp = input("")
            if (inp):
                con.msg(inp)

    pybotPrint("[PYBOT] connection ended", "log")
    exit()

# Once the irc connection is made it dumps the live feed here along with any events it finds
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

        if checkIfCommand(text, "!raffle"):
            if toBool(globals.settings.config['features']['raffle']):
                texsplit = text.replace("!raffle", '').split(" ")
                raffle = Raffle(con, con.data, texsplit)
                globals.data.raffles.append(raffle)

        elif checkIfCommand(text, "!leave"):
            if con.isMod(name):
                con.msg("Bye!");
                con.close()
            else:
                con.msg('%s, you do not have access to this command.' % name)

        elif checkIfCommand(text, "!permit"):
            cmd_args = text.split(" ")
            if con.isMod(name):
                con.msg("%s can post a link" % cmd_args[2])
                con.addMode(cmd_args[2], "+permit")
            else:
                con.msg('%s, you do not have access to this command.' % name)

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