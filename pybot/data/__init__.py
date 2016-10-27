# for persistent data

import configparser
import os
import json


def toBool(s):
    return s == "True" or s == "true"


class Settings():
    def __init__(self):
        if (os.path.isfile("pybot.conf")):
            self.config = self.getConf()
        else:
            self.createConf()
            self.config = self.getConf()

    def addFilter(self, f):
        filters = json.loads(self.config['filters']['activeFilters'])
        filters.append(f)
        self.config['filters']['activeFilters'] = json.dumps(filters)
        self.saveConf()

    def removeFilter(self, filter):
        filters = json.loads(self.config['filters']['activeFilters'])
        filters.remove(filter)
        self.config['filters']['activeFilters'] = json.dumps(filters)
        self.saveConf()

    def createConf(self):
        config = configparser.ConfigParser()

        config['bot'] = {'NAME': 'usernameforbot', 'AUTH': 'oauth:botauthhere'}
        config['twitch'] = {'HOST': 'irc.twitch.tv', 'PORT': '6667', 'channel': 'channelName'}
        config['filters'] = {'activeFilters': '["length", "profanity", "repetition", "uppercase", "websites"]'}
        config['features'] = {'linkgrabber': 'False', 'quotes': 'True', 'raffle': 'True'}
        config['points'] = {'enabled': 'true', 'interval_in_minutes': '15.0', 'points_to_append': '1'}
        config['compatibility'] = {'append_to_commands': ''}
        config['web'] = {'enabled': 'True', 'port': '8888'}
        config['print'] = {'HTML': 'False'}
        config['linkgrabber'] = {'filter': ''}

        with open('pybot.conf', 'w') as configfile:
            config.write(configfile)

    def getConf(self):
        config = configparser.ConfigParser()
        config.read("pybot.conf")
        return config

    def saveConf(self, conf=None):
        if (conf == None):
            conf = self.config
        with open('pybot.conf', 'w') as configfile:
            conf.write(configfile)
        self.config = conf


class Data():
    def __init__(self):

        # live non saved data
        self.raffles = []
        self.logs = []

        # saved data
        self.quotes = []
        self.linkbanned = []
        self.links = {}

        self.commands = []

        # user data
        self.points = {"name": 0}
        self.activeUsersOverTime = {}       # dict {time: amount}

        self.read()

        # session data
        self.currentRandomLink = ""

    def getRaffle(self, name):
        raffle = False
        for r in Data.instance().raffles:
            if r.params["name"] == name:
                raffle = r
                break
        return raffle

    def read(self, doSet=True):
        if (os.path.isfile("persistent.data")):
            config = self.getConf()
        else:
            self.createConf()
            config = self.getConf()
        if doSet:
            self.quotes = json.loads(config.get("quotedata", "quotes"))
            self.linkbanned = json.loads(config.get("linkdata", "linkbanned"))
            self.links = json.loads(config.get("linkdata", "links"))
            self.points = json.loads(config.get("userdata", "points"))
            self.commands = json.loads(config.get("commands", "cmdlist"))
            self.activeUsersOverTime = json.loads(config.get("userData", "activeUsersOverTime"))

        return config

    def save(self):
        config = self.read(False)
        config.set("quotedata", "quotes", json.dumps(self.quotes))
        config.set("linkdata", "links", json.dumps(self.links))
        config.set("linkdata", "linkbanned", json.dumps(self.linkbanned))
        config.set('userdata', 'points', json.dumps(self.points))
        config.set('commands', 'cmdlist', json.dumps(self.commands))
        config.set("userData", "activeUsersOverTime", json.dumps(self.activeUsersOverTime))

        with open('persistent.data', 'w') as configfile:
            config.write(configfile)

    def createConf(self):
        config = configparser.ConfigParser()

        config['linkdata'] = {'links': json.dumps(self.links), 'linkbanned': '[]'}
        config['quotedata'] = {'quotes': '[]'}
        config['userdata'] = {'points': json.dumps(self.points)}
        config['commands'] = {'cmdlist': '[]'}
        config['userData'] = {'activeUsersOverTime': '{}'}

        with open('persistent.data', 'w') as configfile:
            config.write(configfile)

    def getConf(self):
        config = configparser.ConfigParser()
        config.read("persistent.data")
        return config

    def addPoints(self, user, points):
        try:
            self.points[user] = self.points[user] + points
        except:
            self.points[user] = 0
