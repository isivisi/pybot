from data import Settings
import re

def pybotPrint(text, mode=""):
    settings = Settings()
    if (settings.HTML):
        print "<div class='pybot-out-" + mode + "'>" + text + "</div>"
    else:
        print text

def checkIfCommand(text, *cmds):
    found = False
    i = 0
    concat = ""

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