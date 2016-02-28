# Settings class to load in settings
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

            config.add_section('print')
            config.set('print', 'HTML', 'false')

            with open('pybot.conf', 'wb') as configfile:
                config.write(configfile)

        def getConf(self):
            config = ConfigParser.RawConfigParser()
            config.read("pybot.conf")
            return config