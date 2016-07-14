# pybot tests

import py_compile
import os

os.chdir(os.path.dirname(__file__) or '.')
os.chdir('..') # move one back
src = os.getcwd()
print(src)


currentTest = 0
def startTest(msg):
    global currentTest
    currentTest += 1
    print("\n[TEST %s] %s" % (currentTest, msg,))

def createPrivMsg(user, channel, text):
    return ":%s!%s@%s.tmi.twitch.tv PRIVMSG #%s :%s" % (user, user, user, channel, text)

def getPyFilesFromDir(dir = ""):
    loc = os.path.join(src, dir)
    print("looking in " + loc)
    return [os.path.join(dir, f) for f in os.listdir(loc) if os.path.isfile(os.path.join(loc, f)) and ".py" in f and not ".pyc" in f and not "py." in f] # todo regex

def compileTest():
    startTest("SIMPLE SYNTAX TEST")
    print("Filding files...")
    subfolders = [s[0] for s in os.walk(src)]
    files = []
    files.extend(getPyFilesFromDir(src))
    for folder in subfolders:
        files.extend(getPyFilesFromDir(folder))
    print("compiling files...")
    for file in files:
        py_compile.compile(file, doraise=True)
        print(file + " compiled with no errors")

def setupTest():
    startTest("SETUP CHECK")
    print("Checking if setup was performed correctly...")

    print("importing tornado...")
    import tornado
    print("importing requests...")
    import requests

    print("looking for chart.min.js...")
    assert (os.path.isfile(os.path.join(src, "web", "Chart.min.js")) == True), "Chart.min.js not found!"
    print("looking for normalize.css...")
    assert (os.path.isfile(os.path.join(src, "web", "css",  "normalize.css")) == True), "normalize.css not found!"
    print("looking for skeleton.css...")
    assert (os.path.isfile(os.path.join(src, "web", "css", "skeleton.css")) == True), "skeleton.css not found!"


try:
    # Compile code to make sure its syntactically correct
    print("[PYBOT TESTS]\n")
    compileTest()
    setupTest()
except AssertionError as e:
    print("[TEST %s] ASSERTION FAILED: %s" % (currentTest, str(e),))
    exit(1)