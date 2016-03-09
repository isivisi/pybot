import tornado
import globals
from pybotextra import allFilters

class Raffle(tornado.web.UIModule):
    def render(self):
        return self.render_string("templates/rafflemodule.html", data=globals.data)

class UserPoints(tornado.web.UIModule):
    def render(self, top=0):
        return self.render_string("templates/userpointsmodule.html", data=globals.data, top=top)

class Logs(tornado.web.UIModule):
    def render(self):
        return self.render_string("templates/logmodule.html", data=globals.data)

class Links(tornado.web.UIModule):
    def render(self, link = False):
        return self.render_string("templates/linksmodule.html", data=globals.data, link=link)

class Filters(tornado.web.UIModule):
    def render(self):
        return self.render_string("templates/filtersmodule.html", data=globals.data, settings=globals.settings, allfilters=allFilters())

