import pybot.globals as globals
import pybot.data as data
import re
import os

def pybotPrint(text, mode=""):
    settings = globals.settings
    if (data.toBool(settings.config["print"]["HTML"])):
        print("<div class='pybot-out-" + mode + "'>" + text + "</div>")
    else:
        print(text)
        globals.data.logs.append(text)

def checkIfCommand(text, *cmds_, addc=True):
    found = False
    cmds = list(cmds_)
    i = 0
    concat = ""
    app = globals.settings.config['compatibility']['append_to_commands']
    if app != '' and addc:
        cmds[0] = cmds[0][0] + app + cmds[0][1:]

    for cmd in cmds:
        regx = re.compile('^' + concat + '(' + cmd + ') *', re.IGNORECASE)
        if regx.search(text.strip()) and len(text.split(" ")[1 + i]) == len(cmd):
            found = True
            concat += text.split(" ")[1 + i] + " "
        else:
            found = False
            break
        i += 1

    return found

def splitButNotQuotes(text):
    text = text.strip()
    split = []
    pos = 0
    str = ""
    quote = False
    lent = len(text)
    while pos < len(text):
        if text[pos] == '"' :
            quote = not quote

        if (text[pos] == ' ' and quote == False) or pos == len(text)-1:
            split.append(str)
            str = ""
        else:
            str = str + text[pos]
        pos += 1
    return split

def allFilters():
    dir = 'filters/'
    return [f.replace('.py', '') for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]