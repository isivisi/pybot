import pybot.features.quotes
import pybot.pybotextra
import pybot.tests

pybot.tests.startTest("QUOTES TESTS")

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
quotes = pybot.features.quotes.Quotes(irc)

pybot.globals.settings.config['features']['quotes'] = "True"
pybot.globals.data.quotes = []

print("Add quote test...")
msg = pybot.tests.createPrivMsg("notmod", "test", "!quote testquote0")
irc.hook(irc, msg, "user_privmsg")
assert ('"testquote0" - notmod' in pybot.globals.data.quotes), "Quote was not added"

msg = pybot.tests.createPrivMsg("notmod", "test", "!quote testquote1")
irc.hook(irc, msg, "user_privmsg")
assert ('"testquote1" - notmod' in pybot.globals.data.quotes), "Quote was not added"

print("Random quote test...")
msg = pybot.tests.createPrivMsg("notmod", "test", "!quote")
irc.hook(irc, msg, "user_privmsg")
assert ("testquote" in irc.lastMsg and "- notmod" in irc.lastMsg), "!quotes didnt print out correctly"
