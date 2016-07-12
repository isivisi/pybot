# gui for pybot

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import os
import pybot.web.uimodules as uimodules
import random
from pybot.data import *
import pybot.globals as globals
import threading

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = "Pybot"
        self.render("templates/index.html", title=title)

class SocketHandler(tornado.websocket.WebSocketHandler):
    #def open(self):
    #    print("[pybot.tornado.websocket] Opened")

    def on_message(self, message):
        split = ""
        delim = "---!---"
        for msg in globals.data.logs:
           split += msg + delim;

        self.write_message(split)

    #def on_close(self):
    #    print("[pybot.tornado.websocket] Closed")

    def check_origin(self, origin):
        return True

class BotHandler(tornado.web.RequestHandler):
    def get(self, command):
        if command == "rejoin":
            threading.Thread(target=globals.con.retry).start()
        elif command == "leave":
            globals.con.close()
        self.redirect("/hub")

class RaffleHandler(tornado.web.RequestHandler):
    def get(self, action):
        split = action.split("/")
        data = globals.data
        if len(split) >= 2:
            act = split[0]
            raff = split[1]
            if (act == "select"):
                raffle = data.getRaffle(raff)
                if (raffle != False):
                    winner = raffle.users[random.randint(0, len(raffle.users)-1)]
                    self.render("templates/raffle.html", message="The winner is: " + winner)
                else:
                    self.render("templates/raffle.html", message="Raffle " + raff + " doesnt exist :(")
            elif (act == "cancel"):
                raffle = data.getRaffle(raff)
                if (raffle != False):
                    data.raffles.remove(raffle)
                    self.render("templates/raffle.html", message="Raffle " + raff + " removed")
                else:
                    self.render("templates/raffle.html", message="Raffle " + raff + " doesnt exist :(")

class FilterHandler(tornado.web.RequestHandler):
    def get(self, action):
        split = action.split("/")
        data = globals.data
        if len(split) >= 2:
            act = split[0]
            filter = split[1]
            if act == "disable":
                globals.settings.removeFilter(filter)
                self.redirect("/hub/filters")
            elif act == "enable":
                globals.settings.addFilter(filter)
                self.redirect("/hub/filters")

    def post(self, args):
            filter = tornado.escape.to_basestring(self.request.arguments['addfilter'][0])
            globals.settings.addFilter(filter)
            self.redirect("/hub/filters")

class LinkHandler(tornado.web.RequestHandler):
    def get(self, action):
        split = action.split("/")
        data = globals.data
        if len(split) >= 1:
            act = split[0]
            if act == "remove":
                user = split[1]
                del globals.data.links[user]
                self.redirect("/hub/links")
            elif act == "random":
                if len(data.links) > 0:
                    #self.render("templates/link.html", message=data.links[random.sample(list(data.links), 1)[0]])
                    globals.data.currentRandomLink = data.links[random.sample(list(data.links), 1)[0]]
                self.redirect("/hub/links")
            elif act == "removeall":
                data.links.clear()
                self.redirect("/hub/links")

class HubHandler(tornado.web.RequestHandler):
    def get(self, page):
        data = globals.data
        settings = globals.settings
        self.render("templates/hub.html", data=data, settings=settings, page=page)

    def post(self, page):
        data = globals.data
        settings = globals.settings
        if page == "settings":

            config = settings.getConf()

            for arg in self.request.arguments.keys():
                split = arg.split(".")
                config.set(split[0], split[1], tornado.escape.to_basestring(self.request.arguments[arg][0]))
                #print "[pybot.tornado.web] " + arg + " set to " + str(self.request.arguments[arg][0])
            settings.saveConf(config)

            self.render("templates/hub.html", data=data, settings=settings, page=page)

        if page == "links":
            inputFilter = self.get_argument('inputFilter', '')
            if inputFilter:
                settings.config['linkgrabber']['filter'] = inputFilter
                settings.saveConf()
            self.redirect('/hub/links')

class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Settings test")

def make_app():

    settings = {
        "static_path": os.path.dirname(__file__),
        "ui_modules": uimodules
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/settings", SettingsHandler), # cam do regex url(r"/story/([0-9]+)", StoryHandler, dict(db=db), name="story")
        (r"/hub/?(.*)", HubHandler),
        (r"/bot/(.*)", BotHandler),
        (r"/websocket", SocketHandler),
        (r"/raffle/(.*)", RaffleHandler),
        (r"/filters/(.*)", FilterHandler),
        (r"/links/(.*)", LinkHandler)
        #(r"/static", tornado.web.StaticFileHander, dict(path=settings['static_path]'])),
    ], **settings)

class pybot_web():
    def __init__(self, con):
        self.settings = globals.settings

    def startWebService(self):
        print("[pybot.tornado.web] Web services starting on port " + str(globals.settings.config['web']['port']))

        app = make_app()
        app.listen(int(globals.settings.config['web']['port']))
        tornado.ioloop.IOLoop.current().start()

# for testing directly
#if __name__ == "__main__":
#    pybot_web()