# for persistent data

import ConfigParser
import os
import json

class Settings:
        def __init__(self):
            if (os.path.isfile("pybot.conf")):
                config = self.getConf()
            else:
                self.createConf()
                config = self.getConf()

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

            # printing settings
            self.HTML = config.getboolean("print", "HTML")

        def createConf(self):
            config = ConfigParser.RawConfigParser()
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
            config.set('features', 'quotes', 'false')

            config.add_section('print')
            config.set('print', 'HTML', 'false')

            with open('pybot.conf', 'wb') as configfile:
                config.write(configfile)

        def getConf(self):
            config = ConfigParser.RawConfigParser()
            config.read("pybot.conf")
            return config

class Data:
    def __init__(self):

        self.quotes = []
        self.linkbanned = []
        self.links = []

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

        return config

    def save(self):
        config = self.read(False)
        config.set("quotedata", "quotes", json.dumps(self.quotes))
        config.set("linkdata", "links", json.dumps(self.links))
        config.set("linkdata", "linkbanned", json.dumps(self.linkbanned))

        with open('persistent.data', 'wb') as configfile:
                config.write(configfile)

    def createConf(self):
            config = ConfigParser.RawConfigParser()
            config.add_section('linkdata')
            config.set('linkdata', 'links', '[]')
            config.set('linkdata', 'linkbanned', '[]')

            config.add_section('quotedata')
            config.set('quotedata', 'quotes', '[]')

            with open('persistent.data', 'wb') as configfile:
                config.write(configfile)

    def getConf(self):
        config = ConfigParser.RawConfigParser()
        config.read("persistent.data")
        return config