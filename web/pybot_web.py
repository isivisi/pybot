# gui for pybot

import tornado.ioloop
import tornado.web
import os
from src.data import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = "Pybot"
        self.render("templates/index.html", title=title)

class HubHandler(tornado.web.RequestHandler):
    def get(self, page):
        data = Data()
        settings = Settings()
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
    def __init__(self, con, settings, data):
        self.con = con
        self.settings = settings
        self.data = data

        print("[pybot.tornado.web] Web services starting on port " + str(settings.webport))

        app = make_app()
        app.listen(settings.webport)
        tornado.ioloop.IOLoop.current().start()

# for testing directly
#if __name__ == "__main__":
#    pybot_web("","","")