from pybot.pybotextra import *
import pybot.globals as globals
from pybot.data import *

class Loopedads:
    def __init__(self):
        self.con = globals.con
        self.con.addHook(self.hook)

    def hook(self, con, msg, event):
        if event == "user_privmsg":
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split("PRIVMSG")[1].replace('%s :' % con.channel, '')

            if checkIfCommand(text, "!createad"):
                if con.isMod(name):
                    splitButNotQuotes(text)[1]
