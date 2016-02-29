# controller for pybot commands

import os
import thread
from pybotextra import *

PWD = "/var/www/html/pybot"

class Command:
    def __init__(self, trigger, args, message, permissions):
        self.trigger = trigger
        self.args = args
        self.message = message
        self.permissions = permissions

    def __cmp__(self, other):
        return (self.trigger == other)

    def __str__(self):
        return self.trigger + "," + self.args + "," + self.message + "," + self.permissions

    def getTrigger(self):
        return self.trigger

    def getMessage(self):
        return self.message

class Commands:
    def __init__(self, con):
        self.commands = []
        self.con = con
        self.data = con.data

        self.getCommands()
        con.addHook(self.hook)

    #def checkForCustomCommand

    def getCommands(self):
        commands = self.data.commands
        for command in commands:
            split = command.split(',')
            self.commands.append(Command(split[0], split[1], split[2], split[3]))
        pybotPrint("[CMDS] " + str(len(commands)) + " custom commands loaded.")

    def addCommand(self, trigger, args, message, permissions):
        cmd = Command(trigger, args, message, permissions)
        self.data.commands.append(str(cmd))
        self.commands.append(cmd)

    def hook(self, con, msg, event):
        if event == "user_privmsg":
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split("PRIVMSG")[1].replace('%s :' % con.channel, '')

            for command in self.commands:
                if checkIfCommand(text, command.trigger):
                    self.con.msg(command.message)
                    break
