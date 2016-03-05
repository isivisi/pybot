# gui for pybot

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import os
import web.uimodules
import random
from data import *
import globals

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
            if act == "remove":
                globals.settings.removeFilter(filter)
                self.redirect("/hub/filters")

    def post(self, args):
            filter = tornado.escape.to_basestring(self.request.arguments['addfilter'][0])
            globals.settings.addFilter(filter)
            self.redirect("/hub/filters")

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

class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Settings test")

def make_app():

    settings = {
        "static_path": os.path.dirname(__file__),
        "ui_modules": web.uimodules
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/settings", SettingsHandler), # cam do regex url(r"/story/([0-9]+)", StoryHandler, dict(db=db), name="story")
        (r"/hub/?(.*)", HubHandler),
        (r"/bot/(.*)", BotHandler),
        (r"/websocket", SocketHandler),
        (r"/raffle/(.*)", RaffleHandler),
        (r"/filters/(.*)", FilterHandler)
        #(r"/static", tornado.web.StaticFileHander, dict(path=settings['static_path]'])),
    ], **settings)

class pybot_web():
    def __init__(self, con):
        self.settings = globals.settings

    def startWebService(self):
        print("[pybot.tornado.web] Web services starting on port " + str(self.settings.webport))

        app = make_app()
        app.listen(self.settings.webport)
        tornado.ioloop.IOLoop.current().start()

# for testing directly
#if __name__ == "__main__":
#    pybot_web()