import tornado
from data import *

class Raffle(tornado.web.UIModule):
    def render(self):
        return self.render_string("templates/rafflemodule.html", data=Data.instance())

class UserPoints(tornado.web.UIModule):
    def render(self, top=0):
        return self.render_string("templates/userpointsmodule.html", data=Data.instance(), top=top)

class Logs(tornado.web.UIModule):
    def render(self):
        return self.render_string("templates/logmodule.html", data=Data.instance())
