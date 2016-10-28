import tornado
import pybot.globals as globals
from pybot.pybotextra import allFilters
import json


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
    def render(self, link=False):
        return self.render_string("templates/linksmodule.html", settings=globals.settings, data=globals.data, link=link)


class Filters(tornado.web.UIModule):
    def render(self):
        activeFilters = json.loads(globals.settings.config['filters']['activeFilters'])
        return self.render_string("templates/filtersmodule.html", data=globals.data, activeFilters=activeFilters,
                                  allfilters=allFilters())

class UserList(tornado.web.UIModule):
    def render(self):
        return self.render_string("templates/userlist.html", data=globals.data, chatters=globals.con.chatters)


# Values take in a list of dictionaries with values (value: #, color:"#F7464A", highlight: "#FF5A5E", label: "")
# settings is a dictionary with settings for the chart
class Chart(tornado.web.UIModule):
    def render(self, type, values=[], settings={}, datasets={}, datasetsInt={}, width=150, height=150):
        # test values
        #values.append({"value": "25", "color": "#F7464A", "highlight": "#FF5A5E", "label": "test1"})
        #values.append({"value": "75", "color": "#ffffff", "highlight": "#FF5A5E", "label": "test2"})

        return self.render_string("templates/chartmodule.html", datasets=datasets, datasetsInt=datasetsInt, type=type, values=values, settings=settings)
