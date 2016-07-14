import pybot.features.linkgrabber
import pybot.pybotextra
import pybot.tests

pybot.tests.startTest("LINKGRABBER TESTS")


class hook():
    def __init__(self):
        self.hook = None
        self.channel = "#test"
        self.lastMsg = ""

    def addHook(self, h):
        self.hook = h

    def msg(self, msg):
        self.lastMsg = msg

    def isMod(self, name):
        return name == "mod"


print("Init test...")
irc = hook()
linkgrabber = pybot.features.linkgrabber.Linkgrabber(irc)

pybot.globals.settings.config['features']['linkgrabber'] = "True"
pybot.globals.settings.config['linkgrabber']['filter'] = ""

print("Enable / Disable test...")
msg = pybot.tests.createPrivMsg("mod", "test", "!linkgrabber")
irc.hook(irc, msg, "user_privmsg")
assert (linkgrabber.active == True), "Linkgrabber was not enabled when it should have been"

msg = pybot.tests.createPrivMsg("notmod", "test", "!linkgrabber")
irc.hook(irc, msg, "user_privmsg")
assert (linkgrabber.active == True), "Linkgrabber was disabled by a non mod"

print("Testing link grabbing...")
# testing grab
website = "http://mystupidwebsite.com/pleaselikemycontent"
msg = pybot.tests.createPrivMsg("notmod", "test", website)
irc.hook(irc, msg, "user_privmsg")
assert (pybot.globals.data.links["notmod"] == website), "website was not added to list properly"

print("Testing link banning...")
pybot.globals.data.linkbanned = []
pybot.globals.data.links.pop("azAZ09_", None)
linkgrabber.linkBan("azAZ09_")
msg = pybot.tests.createPrivMsg("azAZ09_", "test", website)
irc.hook(irc, msg, "user_privmsg")
assert ("azAZ09_" not in pybot.globals.data.links.keys()), "Link banned user was able to add a link"

pybot.globals.data.linkbanned = []
pybot.globals.data.links.pop("azAZ09_", None)
msg = pybot.tests.createPrivMsg("mod", "test", "!linkban azAZ09_")
irc.hook(irc, msg, "user_privmsg")
assert ("azAZ09_" in pybot.globals.data.linkbanned), "!linkban command not grabbing name correctly"

# testing if banned user could add link
msg = pybot.tests.createPrivMsg("azAZ09_", "test", website)
irc.hook(irc, msg, "user_privmsg")
assert ("azAZ09_" not in pybot.globals.data.links.keys()), "Link banned user was able to add a link"

# testing !linkban with no args
msg = pybot.tests.createPrivMsg("mod", "test", "!linkban")
irc.hook(irc, msg, "user_privmsg")
assert (irc.lastMsg == "mod, syntax: !plinkban <name>"), "!linkban with no args doesnt display snytax"
