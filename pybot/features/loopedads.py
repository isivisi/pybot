import pybot.globals as globals
import threading
import time
from pybot.data import *
from pybot.pybotextra import *


class Loopedads:
    def __init__(self):
        self.con = globals.con
        self.con.addHook(self.hook)
        self.currentAdvert = 0
        self.loopTime = 60      # seconds
        self.adList = {}        # (adID: text)

        threading.Thread(target=self.displayAdvert).start()

    def displayAdvert(self):
        time.sleep(self.loopTime)
        adverts = self.adList.keys()
        if len(adverts) > 0:
            self.con.privmsg(adverts[self.currentAdvert])
            self.currentAdvert = self.currentAdvert + 1 if self.currentAdvert < len(adverts) else 0

    def hook(self, con, msg, event):
        if event == "user_privmsg":
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split("PRIVMSG")[1].replace('%s :' % con.channel, '')

            # usage: !createad "id" "advert"
            if checkIfCommand(text, "!createad"):
                if con.isMod(name):
                    args = splitButNotQuotes(text)
                    if len(args) >= 3:
                        advertId = args[1]
                        advert = args[2]
                        self.adList[advertId] = advert
