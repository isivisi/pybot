# controller for pybot commands

import os
from pybot.pybotextra import *
import pybot.globals as globals

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

        self.getCommands()
        con.addHook(self.hook)

    #def checkForCustomCommand

    def getCommands(self):
        commands = globals.data.commands
        for command in commands:
            split = command.split(',')
            self.commands.append(Command(split[0], split[1], split[2], split[3]))
        pybotPrint("[pybot.commands] " + str(len(commands)) + " custom commands loaded.")

    def addCommand(self, trigger, args, message, permissions):
        cmd = Command(trigger, args, message, permissions)
        globals.data.commands.append(str(cmd))
        globals.data.save()
        self.commands.append(cmd)

    def removeCommand(self, cmd):
        self.commands.remove(cmd)
        globals.data.commands.remove(str(cmd))
        globals.data.save()

    def commandExists(self, trigger):
        for cmd in self.commands:
            if cmd.trigger == trigger:
                return cmd
        return False

    def hook(self, con, msg, event):
        if event == "user_privmsg":
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split("PRIVMSG")[1].replace('%s :' % con.channel, '')

            for command in self.commands:
                if checkIfCommand(text, command.trigger, addc=False):
                    self.con.msg(command.message)
                    break

            if checkIfCommand(text, "!command", "add"):
                #split = re.split(ur'[^\s"\']+|"([^"]*)"|\'([^\']*)\'', text)
                if (self.con.isMod(name)):
                    split = splitButNotQuotes(text)
                    if len(split) >= 5:
                        self.addCommand(split[2], split[3], split[4].replace('"', ''), "")
                        self.con.msg("Command " + split[2] + " added")
                    else:
                        self.con.msg("Invalid syntax")

            if checkIfCommand(text, "!command", "remove"):
                if (self.con.isMod(name)):
                    split = text.strip().split()
                    if len(split) >= 3:
                        cmd = self.commandExists(split[2])
                        if cmd is not False:
                            self.removeCommand(cmd)
                            self.con.msg("Command " + split[2] + " removed")
                        else:
                            self.con.msg("Command not found")