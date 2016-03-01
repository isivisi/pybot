#!python2.7
# pybot main process
# used to setup, run, and configure pybot

import os
import sys
import subprocess
from src import data
import pip

mainLoc = os.getcwd()+"//src//PYBOT.py"
pyLoc = sys.executable

dependencies = {"tornado":"tornado>=4.3"}

def main():

    if len(sys.argv) > 1:

        if sys.argv[1] == "-run":
            print ("Starting main pybot process...")
            subprocess.call([pyLoc, mainLoc])

        elif sys.argv[1] == "-setup":
            print("Pybot is setting up...")

            print("[Setup] Installing dependencies...")
            for package in dependencies.keys():
                try:
                    __import__(package)
                    print("[Setup] " + package + " already installed")
                except:
                    pip.main(['install', dependencies[package]])
                    print("[Setup] " + package + " installed")

            # this create default config
            data.Settings()
            print("[Setup] Config created")

            data.Data()
            print("[Setup] Persistant data file created")

            if "win" in sys.platform:
                file = open("pybot.bat", 'w')
                file.write("@echo off\n" + \
                pyLoc +" pybot.py %*")
                file.close()
                # sys.path.append(os.getcwd()+"\\pybot.bat")
                # os.environ["PATH"] += os.pathsep + os.getcwd()+"\\pybot.bat"
                print("[Setup] bat file created for windows")
            #TODO linux
            # print("[Setup] pybot added to system PATH")

            print("pybot setup complete")

        elif sys.argv[1] == "--config":
            if len(sys.argv) > 2:
                settings = data.Settings().getConf()
                args = sys.argv[2].split(".")
                settings.set(args[0], args[1], sys.argv[3])

                with open('pybot.conf', 'wb') as configfile:
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
