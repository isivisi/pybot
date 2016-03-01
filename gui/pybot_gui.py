# gui for pybot

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Settings test")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/settings", SettingsHandler),
    ])

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