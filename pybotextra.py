from data import Settings

def pybotPrint(text, mode=""):
    settings = Settings()
    if (settings.HTML):
        print "<div class='pybot-out-" + mode + "'>" + text + "</div>"
    else:
        print text
