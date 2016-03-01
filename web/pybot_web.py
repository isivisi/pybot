# gui for pybot

import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = "Pybot web ui testing"
        info = "This is where information will go"
        self.render("templates/index.html", title=title, info=info)

class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Settings test")

# example
class exampleGetPost(tornado.web.RequestHandler):
    def get(self):
        self.write("whatever website bs")

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write(self.get_body_argument("nameofinputfromform"))


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

        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

# for testing directly
if __name__ == "__main__":
    pybot_web("","","")