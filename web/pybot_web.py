# gui for pybot

import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = "Pybot web ui testing"
        info = "This is where information will go"

        title2 = "status"
        info2 = ""
        self.render("templates/index.html", title=title, info=info, title2=title2, info2=info2)

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
        #(r"/static", tornado.web.StaticFileHander, dict(path=settings['static_path]'])),
    ], **settings)

class pybot_web():
    def __init__(self, con, settings, data):
        self.con = con
        self.settings = settings
        self.data = data

        print("[pybot.tornado.web] Web services starting")

        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

# for testing directly
#if __name__ == "__main__":
#    pybot_web("","","")