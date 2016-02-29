from data import Settings
import re

def pybotPrint(text, mode=""):
    settings = Settings()
    if (settings.HTML):
        print "<div class='pybot-out-" + mode + "'>" + text + "</div>"
    else:
        print text

def checkIfCommand(text, cmd):
    regx = re.compile('^(' + cmd+ ') *', re.IGNORECASE)
    if regx.search(text.strip()) and len(text.split(" ", 2)[1]) == len(cmd):
        return True
    return False
