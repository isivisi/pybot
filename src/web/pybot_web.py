# gui for pybot

import tornado.ioloop
import tornado.web
import os
from data import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = "Pybot"
        self.render("templates/index.html", title=title)

class HubHandler(tornado.web.RequestHandler):
    def get(self, page):
        data = Data.instance()
        settings = Settings.instance()
        self.render("templates/hub.html", data=data, settings=settings, page=page)

    def post(self, page):
        data = Data.instance()
        settings = Settings.instance()
        if page == "settings":
            #TODO: modify settings to make this easier

            config = settings.getConf()

            for arg in self.request.arguments.keys():
                split = arg.split(".")
                config.set(split[0], split[1], self.request.arguments[arg][0])
                #print "[pybot.tornado.web] " + arg + " set to " + str(self.request.arguments[arg][0])
            settings.saveConf(config)

            self.render("templates/hub.html", data=data, settings=settings, page=page)

class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Settings test")

def make_app():

    settings = {
        "static_path": os.path.dirname(__file__)
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/settings", SettingsHandler), # cam do regex url(r"/story/([0-9]+)", StoryHandler, dict(db=db), name="story")
        (r"/hub/?(.*)", HubHandler)
        #(r"/static", tornado.web.StaticFileHander, dict(path=settings['static_path]'])),
    ], **settings)

class pybot_web():
    def __init__(self):
        settings = Settings.instance()
        print("[pybot.tornado.web] Web services starting on port " + str(settings.webport))

        app = make_app()
        app.listen(settings.webport)
        tornado.ioloop.IOLoop.current().start()

# for testing directly
#if __name__ == "__main__":
#    pybot_web()