# pybot raffle system
# implemented by isivisi

import threading
import time
import random
from pybotextra import *

class Raffle:
    def __init__(self, conn, data, timelimit=120):
        self.conn = conn
        self.data = data
        self.timelimit = timelimit
        self.users = []
        self.params = {"cost":0, "minpoints":0}
        conn.addHook(self.hook)

        conn.msg("Raffle has begun! to join say !joinraffle in chat")
        threading.Thread(target=self.wait, args=(self.timelimit,)).start()
        #thread.start_new_thread(self.wait, (self.timelimit,))

    def wait(self, timelimit):
        time.sleep(timelimit)
        self.chooseWinner()
        self.__del__()

    def chooseWinner(self):
        winner = self.users[random.randint(0, len(self.users)-1)]
        self.conn.msg("The winner is: " + winner)

    def setParam(self, param, value):
        self.params[param] = int(value)

    def hook(self, con, msg, event):
        if event == "user_privmsg":
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split("PRIVMSG")[1].replace('%s :' % con.channel, '')

            if checkIfCommand(text, "!joinraffle"):
                # do they meet the minimum user requirments?
                try:
                    userPoints = self.data.points[name]
                except:
                    userPoints = 0

                if userPoints >= self.params["minpoints"] and userPoints >= self.params["cost"] and name not in self.users:
                    self.users.append(name)
                    self.data.points[name] -= self.params["cost"]
                    self.data.save()
                    con.msg(name + " has entered the raffle!")

    def __del__(self):
        # remove hook because instance is being deleted
        self.conn.removeHook(self.hook)