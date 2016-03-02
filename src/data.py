# for persistent data

import configparser
import os
import json
from Singleton import *

class Settings(Singleton):
        def __init__(self):
            if (os.path.isfile("pybot.conf")):
                config = self.getConf()
            else:
                self.createConf()
                config = self.getConf()
            self.setVars(config)

        def setVars(self, config):
            # name and auth for the user that the bot will speak from
            self.NAME = config.get("bot", "NAME")
            self.AUTH = config.get("bot", "AUTH")

            # twitch settings
            self.HOST = config.get("twitch", "HOST")
            self.PORT = config.getint("twitch", "PORT")
            self.channel = config.get("twitch", "channel")

            # filters
            self.filters = json.loads(config.get("filters", "activeFilters"))

            # features
            self.linkgrabber = config.getboolean("features", "linkgrabber")
            self.quotes = config.getboolean("features", "quotes")
            self.raffle = config.getboolean("features", "raffle")

            self.points = config.getboolean('points', 'enabled')
            self.pointsToAppend = config.getint('points', 'points_to_append')
            self.pointsInterval = config.getfloat('points', 'interval_in_minutes')

            self.web = config.getboolean("web", "enabled")
            self.webport = config.getint("web", "port")

            # printing settings
            self.HTML = config.getboolean("print", "HTML")

        def createConf(self):
            config = configparser.RawConfigParser()
            config.add_section('bot')
            config.set('bot', 'NAME', 'usernameforbot')
            config.set('bot', 'AUTH', 'autho:forbot')

            config.add_section('twitch')
            config.set('twitch', 'HOST', 'irc.twitch.tv')
            config.set('twitch', 'PORT', '6667')
            config.set('twitch', 'channel', 'channelName')

            config.add_section('filters')
            config.set('filters', 'activeFilters', '["length", "profanity", "repetition", "uppercase", "websites"]')

            config.add_section('features')
            config.set('features', 'linkgrabber', 'false')
            config.set('features', 'quotes', 'true')
            config.set('features', 'raffle', 'true')

            config.add_section('points')
            config.set('points', 'enabled', 'false')
            config.set('points', 'interval_in_minutes', '15.0')
            config.set('points', 'points_to_append', '1')

            config.add_section('web')
            config.set('web', 'enabled', 'true')
            config.set('web', 'port', '8888')

            config.add_section('print')
            config.set('print', 'HTML', 'false')

            with open('pybot.conf', 'wb') as configfile:
                config.write(configfile)

        def getConf(self):
            config = configparser.RawConfigParser()
            config.read("pybot.conf")
            return config

        def saveConf(self, conf):
            with open('pybot.conf', 'wb') as configfile:
                    conf.write(configfile)
            self.setVars(conf)

class Data(Singleton):
    def __init__(self):

        self.quotes = []
        self.linkbanned = []
        self.links = []

        self.points = {"name": 0}
        self.commands = []

        self.read()

    def read(self, set = True):
        if (os.path.isfile("persistent.data")):
            config = self.getConf()
        else:
            self.createConf()
            config = self.getConf()
        if set:
            self.quotes = json.loads(config.get("quotedata", "quotes"))
            self.linkbanned = json.loads(config.get("linkdata", "linkbanned"))
            self.links =json.loads(config.get("linkdata", "links"))
            self.points = json.loads(config.get("userdata", "points"))
            self.commands = json.loads(config.get("commands", "cmdlist"))

        return config

    def save(self):
        config = self.read(False)
        config.set("quotedata", "quotes", json.dumps(self.quotes))
        config.set("linkdata", "links", json.dumps(self.links))
        config.set("linkdata", "linkbanned", json.dumps(self.linkbanned))
        config.set('userdata', 'points', json.dumps(self.points))
        config.set('commands', 'cmdlist', json.dumps(self.commands))

        with open('persistent.data', 'wb') as configfile:
                config.write(configfile)

    def createConf(self):
            config = configparser.RawConfigParser()
            config.add_section('linkdata')
            config.set('linkdata', 'links', '[]')
            config.set('linkdata', 'linkbanned', '[]')

            config.add_section('quotedata')
            config.set('quotedata', 'quotes', '[]')

            config.add_section('userdata')
            config.set('userdata', 'points', json.dumps(self.points))

            config.add_section('commands')
            config.set('commands', 'cmdlist', '[]')

            with open('persistent.data', 'wb') as configfile:
                config.write(configfile)

    def getConf(self):
        config = configparser.RawConfigParser()
        config.read("persistent.data")
        return config

    def addPoints(self, user, points):
        try:
            self.points[user] = self.points[user] + points
        except:
            self.points[user] = 0