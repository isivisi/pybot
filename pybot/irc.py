# irc class to connect to irc servers
# written by isivisi

import json
import os
import random
import socket
import sys
import threading
import time
import urllib.request
import traceback
import pybot.globals as globals

from pybot.pybotextra import *

PWD = os.getcwd()

# class to encapsulate the logic for connecting and reading twitch user data
class chatters:
    def __init__(self, user, con, data):
        self.api = "http://tmi.twitch.tv/group/user/{user}/chatters"
        self.data = data
        self.user = user
        self.con = con
        self.check_time = 15
        self.chatterCount = 0
        self.mods = []
        self.viewers = []
        self.failures = 0						# count all the failed attempts at getting info
        self.failureMax = 10

        threading.Thread(target=self.loopChatter).start()
        #thread.start_new_thread(self.loopChatter, ())

    # Grab json info from api and return parsed json
    def getChatterInfo(self):
        url = self.api.replace("{user}", self.user)
        response = urllib.request.urlopen(url)
        data = json.loads((response.read()).decode("utf-8"))
        return data

    # Update loop to constantly check for changes
    def loopChatter(self):
        while 1:
            try:
                time.sleep(self.check_time)

                chatInfo = self.getChatterInfo()
                #printHTML("%s" % (chatInfo,))
                self.chatterCount = chatInfo["chatter_count"]
                self.mods = chatInfo["chatters"]["moderators"]
                self.viewers = chatInfo["chatters"]["viewers"]

                for user in self.mods:
                    self.con.addMode(user, "+o")

                self.failures = 0 # reset
            except:
                self.failures += 1
                if (self.failures >= self.failureMax):
                    pybotPrint("[pybot.chatters] Have not received any updates in a while.", "log")
                    self.failures = 0


# irc object
class irc:
    def __init__(self, hook):
        self.server = globals.settings.config['twitch']['HOST']
        self.port = int(globals.settings.config['twitch']['PORT'])
        self.channel = "#"+globals.settings.config['twitch']['channel']
        self.user = globals.settings.config['twitch']['channel']
        self.nick = globals.settings.config['bot']['NAME']
        self.hooks = [hook]
        self.connected = False
        self.socket = ""
        self.ping_timeout = 0
        self.ping_timeout_max = 300
        self.chat_timeout_max = 60 										# minutes
        self.chat_check_mods = 30										# seconds
        self.chat_time = 0												# auto incremented dont change
        self.password = globals.settings.config['bot']['AUTH']
        self.totalUsers = 0
        self.users = {}
        self.filterDb = {}  											# if filters need persistent data. list of all created dictionaries
        self.data = data
        #self.cmdc = cmdControl(self, db, self.channel)
        self.botIsMod = False
        self.closed = False
        self.chatters = chatters(self.user, self, self.data)
        self.linkgrabber = False
        self.parseSelf = False                                          # does pybot parse its own messages? for debugging
        self.conCount = 0

        self.filters = []
        for i in json.loads(globals.settings.config['filters']['activeFilters']):
            self.filters.append(i+".py")

        filterList = ""
        for f in self.filters:
            filterList += "%s " % f.upper()
        if (filterList != ""): pybotPrint("[pybot.irc] %s filters loaded" % filterList, "log")


        pybotPrint("[pybot.irc] IRC object initialized, starting ping check...", "log")
        threading.Thread(target=self.ping).start()
        #thread.start_new_thread(self.ping, ())
        threading.Thread(target=self.checkMod).start()
        #thread.start_new_thread(self.checkMod, ()) # waits to see if mod
        threading.Thread(target=self.chatTimeoutCheck).start()
        #thread.start_new_thread(self.chatTimeoutCheck, ())

    def addHook(self, hook):
        self.hooks.append(hook)

    def removeHook(self, hook):
        self.hooks.remove(hook)

    def chatTimeoutCheck(self):
        time.sleep(60)
        self.chat_time += 1
        if (self.chat_time == self.chat_timeout_max):
            self.msg("There has not been any activity for the past %s minutes, pybot is now disconnecting from your chat." % self.chat_timeout_max, "log")
            self.close()
        else:
            self.chatTimeoutCheck()

    def filter(self, user, data):
        for i in self.filters:
            threading.Thread(target=self._filterUser, args=(user, data, i)).start()
            #thread.start_new_thread(self._filterUser, (user, data, i))

    def _filterUser(self, user, data, filter):
        sys.argv = [user, data]
        exec(compile(open(PWD+"//filters//"+filter).read(), filter, 'exec'))

    def checkMod(self):
        time.sleep(120);
        pybotPrint("[pybot.irc] checking mod status...", "log")
        pybotPrint("%s" % self.botIsMod)
        if not (self.botIsMod):
            self.msg("Pybot is not a mod and will not function properly.", "log")

    def getCmdControl(self):
        return self.cmdController

    # so filters can access persistent data
    def accessFileDb(self, name):
        try:
            dataFile = open(PWD + "//db//%s" % name, "r")
        except:
            dataFile = open(PWD + "//db//%s" % name, "w")
            #dataFile.write("0\n")
            dataFile.close()
            dataFile = open(PWD + "//db//%s" % name, "r")

        return dataFile

    def accessDb(self, name):
        try:
            return self.filterDb[name]
        except:
            self.filterDb[name] = {}										# setup dictionary
            return self.filterDb[name]

    def kick(self, name):
        self.msg(".timeout %s" % name)
        pybotPrint("[pybot.irc] Kicked user %s" % name, "log")

    def ban(self, name):
        self.msg(".ban %s" % name)
        pybotPrint("[pybot.irc] Banned user %s" % name, "log")

    def send(self, msg):
        self.socket.send(msg.encode('utf-8'))

    def connect(self):
        if (self.conCount < 1):
            try:
                self.socket = ""
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server, self.port))
                pybotPrint("[pybot.irc] Sending user info...", "log")
                self.send("USER %s\r\n" % self.nick)
                self.send("PASS %s\r\n" % self.password)
                self.send("NICK %s\r\n" % self.nick)
                self.send("TWITCHCLIENT 3\r\n")
                #self.socket.send("CAP REQ :twitch.tv/membership") #request membership but disables chat for some reason

                if self.check_login_status(self.socket.recv(1024)):
                    pybotPrint("[pybot.irc] login success", "log")
                    self.msg("Pybot has connected to your chat.")
                else:
                    pybotPrint("[pybot.irc] login failed", "log")
                    self.retry()

                pybotPrint("[pybot.irc] Joining channel " + self.channel, "log")
                self.joinchannel(self.channel)

                self.connected = True
                self.ping_timeout = self.ping_timeout_max
                self.closed = False
                self.conCount += 1

                self.getLoop()
            except Exception as e:
                pybotPrint(e, "log")
                pybotPrint("[pybot.irc] connection failed, retrying...", "log")
                self.retry()

    def getMods(self):
        while 1:
            time.sleep(self.chat_check_mods)
        #self.msg("/mods", False)

    def joinchannel(self, channel):
        self.send("JOIN %s\r\n" % channel)
        self.send("WHOIS %s" % self.nick)

    def check_login_status(self, data):
        if re.match(b'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data):
            return False
        else:
            return True

    def retry(self):
        self.close(True)
        pybotPrint("Retrying connection in 15 seconds...", "log")
        time.sleep(15)
        self.connect()

    def msg(self, text, show=True, parse=False):
        if self.connected == True:
            self.send("PRIVMSG %s :%s\r\n" % (self.channel, text))
            if (show): pybotPrint(self.nick + " : " + text, "usermsg")
            #if (parse): self.parseSelf = ":%s!%s@%s.tmi.twitch.tv PRIVMSG %s" % (self.nick, self.nick, self.nick, text)

    def privmsg(self, user, text):
        if self.connected == True:
            self.send("PRIVMSG %s :%s\r\n" % (user, text))

    def rawmsg(self, text):
        if self.connected == True:
            self.send(text+"\r\n")

    def get(self):
        if (self.connected):
            try:
                msg = self.socket.recv(2048)
                msg = msg.decode("utf-8")
                msg = msg.strip("\n\r")
                return msg
            except ConnectionAbortedError:
                print("[pybot.irc.get] ConnectionAbortedError in get loop")
            #except Exception as e:
            #    pybotPrint("[pybot.irc.get] " + str(e), "log")
            except:
                return "ERROR"

    def getSetting(self, setting):
        value = self.mysql.query_r("SELECT %s FROM user WHERE userName = '%s'" % (setting, self.user))
        if (value[0][0] == "1"): return True
        else: return False

    def getLoop(self):
        try:
            while self.connected == True:
                messageFull = self.get()
                if messageFull != None:
                    messageList = messageFull.split('\r\n')

                #print messageFull
                #twitchnotify :  1 viewer resubscribed while you were away!

                for msg in messageList:
                    ev = ""

                    if msg == "ERROR":
                        ev = "server_lost"
                        self.close()

                    elif not "PRIVMSG" in msg:

                        if "Nickname is already in use" in msg:
                            ev = "nick_taken"

                        if "Cannot send to channel" in msg:
                            ev = "server_cantchannel"

                        if "QUIT" in msg:
                            ev = "user_quit"
                            name = self.getPrivMsgName(msg)
                            pybotPrint("%s has left the channel" % name, "irc")

                        if "JOIN" in msg:
                            if not self.nick in msg:
                                ev = "user_join"
                                name = self.getPrivMsgName(msg)
                                self.totalUsers += 1
                                pybotPrint("[IRC] %s has joined the channel (%s)" % (name, self.totalUsers), "irc")

                        if "PART" in msg:
                            if not self.nick in msg:
                                ev = "user_part"
                                name = self.getPrivMsgName(msg)
                                pybotPrint("[IRC] %s has left the channel" % name, "irc")
                                self.totalUsers -= 1

                        if "MODE" in msg:
                            ev = "user_mode"
                            name = msg.split(' ')[4].replace('\n\r', '')
                            mode = msg.split(' ')[3]
                            self.addMode(name, mode)

                        # when bot gets modded
                        #if (name == self.nick and mode == "+o"):
                        #	self.msg("Pybot has successfully joined your channel as a mod.")
                        #	self.botIsMod = True
                        #elif (name == self.nick and mode == "-o"):
                        #	self.botIsMod = False

                        if "PING" in msg:
                            ev = "server_ping"
                            self.rawmsg("PONG %s\r\n" % self.server) 		# make sure the bot doesnt time out!
                            self.ping_timeout = self.ping_timeout_max

                    else:
                        if ("jtv.tmi.twitch.tv PRIVMSG " + self.channel not in msg):
                            ev = "user_privmsg"
                            if (self.linkgrabber == True):
                                self.linkgrab(msg)

                            self.chat_time = 0 							  	# set timeout time to 0 so bot doesn't leave when there is activity
                        else:
                            ev = "jtv"
                            if ("SPECIALUSER" in msg):						# :jtv PRIVMSG pybot_beta :SPECIALUSER username subscriber
                                text = msg.split("PRIVMSG")[1].replace('%s :' % self.nick, '')
                                name = text.split(" ")[2]
                                type = text.split(" ")[3]

                                if (type not in self.getMode(name)):
                                    #printHTML(name + " is a "+type, "irc")
                                    self.addMode(name, "+"+type)
                                    pybotPrint(name + "is mode " + self.getMode(name))
                            elif ("The moderators of this room are:" in msg):
                                text = msg.split("PRIVMSG")[1].replace('%s :' % self.channel, '').replace("The moderators of this room are:", '')
                                names = text.split(',')
                                for i in names:
                                    self.addMode(i.strip(), "+o")

                    if self.connected == True and ev != "jtv":
                        for hook in self.hooks:
                            hook(self, msg, ev)
        except:
            traceback.print_exc()
            self.retry()

    def isLinkBanned(self, name):
        if name in globals.data.linkbanned:
            return True
        else:
            return False

    def linkBan(self, name):
        if name not in globals.data.linkbanned:
            globals.data.linkbanned.append(name)
            globals.data.save()
        else:
            globals.data.linkbanned.remove(name)
            globals.data.save()

    def addQuote(self, name, text):
        globals.data.quotes.append('"' + text + '" - ' + name)
        globals.data.save()

    def getRandomQuote(self):
        if (len(globals.data.quotes) > 0):
            return globals.data.quotes[random.randint(0, len(self.data.quotes)-1)]
        return False

    def linkgrab(self, msg):
        name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
        text = msg.split("PRIVMSG")[1].replace('%s :' % self.channel, '')

        # todo replace with REGEX!!!!!
        filters = ['http://', 'www.', '.com', '.ca', '.org', '.gov', '.on', '.tk']

        if self.isLinkBanned(name) == False:
            for filter in filters:
                if filter in text.lower():
                    #self.mysql.query("INSERT INTO link values (null, '%s', '%s', '%s')" % (self.channel, text, name))
                    if (globals.settings.config['linkgrabber']['filter'] in text):
                        globals.data.links[name] = text
                        globals.data.save()
                        self.msg(name + ", your link has been grabbed.")
                    break

    def getPrivMsgName(self, text):
        return text.replace(':', '').split('!')[0]

    def addMode(self, user, mode):

        if (user.strip() == self.nick and mode == "+o" and "o" not in self.getMode(user)):
            self.msg("Pybot has successfully joined your channel as a mod.", "log")
            self.botIsMod = True
        elif (user.strip() == self.nick and mode == "-o"):
            self.botIsMod = False

        try:
            if ("+" in mode):
                if mode.replace("+", "") not in self.users[user]:
                    try:
                        self.users[user] += mode.replace("+", "")+ ","
                    except:
                        self.users[user] = mode.replace("+", "")+ ","
            else:
                try:
                    self.users[user] = self.users[user].replace(mode.replace("-", "") + ",", "")
                except: None
        except:
            if ("+" in mode):
                self.users[user] = mode.replace("+", "")+ ","

    def getMode(self, name):
        try:
            return self.users[name]
        except:
            return ""
        return ""

    def isMod(self, name):
        if (name.lower() == self.channel.replace('#', '').lower()):			# if name is host its auto mod, comment this out if you want to test filters on your own channel
            return True
        else:
            try:
                if "o" in self.users[name]:
                    return True
            except:
                return False
        return False

    def getTotalUsers(self):
        return self.totalUsers

    def ping(self):
        while 1:
            if self.connected:
                self.ping_timeout = self.ping_timeout - 1
                if self.ping_timeout <= 0: # timed out!
                    pybotPrint("Bot has timed out!, reconnecting...", "log")
                    self.retry()
            time.sleep(1)

    def isClosed(self):
        try:
            return self.closed
        except:
            return True

    def close(self, reconn = False):
        if self.socket != "":
            try:
                self.send("disconnect")
                self.socket.close()
            except:
                self.socket.close()

        self.socket = ""
        self.connected = False
        self.conCount = 0
        if (reconn == False): self.closed = True

        print("[pybot.irc] Socket closed")