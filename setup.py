from setuptools import setup
from distutils.command import build as build_module
from distutils.command import bdist as build_dist
import pip
import os

#os.chdir(os.path.dirname(__file__) or '.')

#scripts = ["pybot"] # bin/pybot"]
#if os.name == "nt":
#    scripts += ["bin/pybot.bat"]

get = {"https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.min.js": "pybot//web//Chart.min.js",
       "https://raw.githubusercontent.com/dhg/Skeleton/master/css/normalize.css": "pybot//web//css//normalize.css",
       "https://raw.githubusercontent.com/dhg/Skeleton/master/css/skeleton.css": "pybot//web//css//skeleton.css"}

def pysetup():
    print("Pybot is setting up...")
    try:
        __import__("requests")
    except:
        pip.main(['install', "requests", "--quiet"])

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
    print("Pybot ready to build")

# custom build
class build(build_module.build):
  def run(self):
    pysetup()
    build_module.build.run(self)

#class bdist(build_dist.bdist):
#    def run(self):
#        pysetup()
#        build_dist.bdist.run(self)

setup(
    name='Twitch-Pybot',
    description='A twitch bot with a web interface',
    author='John Iannandrea',
    author_email='jiannandrea@gmail.com',
    url='http://github.com/isivisi/pybot',
    install_requires=[
        'tornado',
        'requests'
    ],
    package_data = {
        "pybot" : ["web/Chart.min.js",
                         "web/css/*",
                         "web/images/*",
                         "web/templates/*"]
    },
    include_package_data=True,
    version='0.1.3',
    packages=['pybot', "pybot/web", "pybot/globals", "pybot/filters", "pybot/features", "pybot/data", "pybot/tests"],
    zip_safe=False,
    license='GNU',
    keywords='bot twitch web interface',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'pybot = pybot:main'
        ]
    },
    test_suite = 'pybot.tests',
    cmdclass={
        'build': build
        #'bdist': bdist
    }
)