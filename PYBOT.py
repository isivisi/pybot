# pybot main process
# used to setup, run, and configure pybot

import os
import sys
import subprocess
from src import data

mainLoc = os.getcwd()+"//src//PYBOT.py"

def main():

    if len(sys.argv) > 1:

        if sys.argv[1] == "-run":
            print "Starting main pybot process..."
            subprocess.call(["python", mainLoc])

        elif sys.argv[1] == "-setup":
            print "Pybot is setting up..."
            # this create default config
            data.Settings()
            print "[Setup] Config created"
            data.Data()
            print "[Setup] Persistant data file created"
            sys.path.append(os.getcwd()+"pybot.py")
            print "[Setup] pybot added to system PATH"

            print "pybot setup complete"

        elif sys.argv[1] == "-help":
            help()
    else:
        print "Invalid usage, type pybot -help"

def help():
        print "Pybot Help\n" \
        "\t-run\tRuns pybot\n" \
        "\t-setup\tCreates config file\n" \
        "\t-help\tI really wonder...\n"

if __name__ == "__main__":
    main()