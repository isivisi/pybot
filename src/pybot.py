#!python2.7
# pybot main process
# used to setup, run, and configure pybot

import os
import sys
import subprocess
from data import *
import pip

if ("\\pybot\\src" in os.getcwd()):
    mainLoc = os.getcwd()
else:
    mainLoc = os.path.join(os.getcwd(), "src")

pyLoc = sys.executable

dependencies = {"tornado":"tornado>=4.3", "requests":"requests>=2.9.1"}
get = { "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.min.js":"src\\web\\Chart.min.js",
        "https://raw.githubusercontent.com/dhg/Skeleton/master/css/normalize.css":"src\\web\\css\\normalize.css",
        "https://raw.githubusercontent.com/dhg/Skeleton/master/css/skeleton.css":"src\\web\\css\\skeleton.css" }

def main():

    if len(sys.argv) > 1:

        if sys.argv[1] == "-run":
            print ("Starting main pybot process...")
            subprocess.call([pyLoc, os.path.join(mainLoc, "pybot_main.py")], cwd=os.getcwd())

        elif sys.argv[1] == "-tests":
            subprocess.call([pyLoc, os.path.join(mainLoc, "tests.py")], cwd=os.getcwd())

        elif sys.argv[1] == "-setup":
            print("Pybot is setting up...")

            print("[Setup] Installing dependencies...")

            print("Installing pip modules...")
            for package in dependencies.keys():
                try:
                    __import__(package)
                    print("[Setup] " + package + " already installed")
                except:
                    pip.main(['install', dependencies[package]])
                    print("[Setup] " + package + " installed")

            print("Grabbing extra files...")
            import requests
            for file in get.keys():
                loc = get[file]
                if not os.path.isfile(loc):
                    print("Grabbing: " + file)
                    txt = requests.get(file)
                    if (loc != ""):
                        f = open(loc, 'w')
                        f.write(txt.text)
                        f.close()
                else:
                    print(loc + " Already exists.")

            # this create default config
            Settings()
            print("[Setup] Config created")

            Data()
            print("[Setup] Persistant data file created")

            if "win" in sys.platform:
                file = open("pybot.bat", 'w')
                file.write("@echo off\n" + \
                '"' + pyLoc + '"' +" src/pybot.py %*\n")
                file.close()
                file = open("pybot_run.bat", 'w')
                file.write("@echo off\n" + \
                '"' + pyLoc + '"' +" src/pybot.py -run\n")
                file.close()
                # sys.path.append(os.getcwd()+"\\pybot.bat")
                # os.environ["PATH"] += os.pathsep + os.getcwd()+"\\pybot.bat"
                print("[Setup] bat files created for windows")
            #TODO linux
            # print("[Setup] pybot added to system PATH")

            print("pybot setup complete")

        elif sys.argv[1] == "--config":
            if len(sys.argv) > 2:
                settings = Settings().getConf()
                args = sys.argv[2].split(".")
                settings.set(args[0], args[1], sys.argv[3])

                with open('pybot.conf', 'w') as configfile:
                    settings.write(configfile)
            else:
                print("Invalid use, type pybot -help")

        elif sys.argv[1] == "-help":
            help()
    else:
        print("Invalid usage, type pybot -help")

def help():
        print("Pybot Help\n" \
        "\t-run\tRuns pybot\n" \
        "\t-setup\tCreates config file\n" \
        "\t-help\tI really wonder...\n\n" \
        "\t--config\n" \
        "\t\tbot.name\n" \
        "\t\tbot.auth\n" \
        "\t\ttwitch.channel\n\t\tetc...")

if __name__ == "__main__":
    main()
