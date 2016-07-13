# [Pybot](http://pybot.ca)
[![Build Status](https://travis-ci.org/isivisi/pybot.svg?branch=master)](https://travis-ci.org/isivisi/pybot)
[![Build status](https://ci.appveyor.com/api/projects/status/e4ibsuh5m2behfx5/branch/master?svg=true)](https://ci.appveyor.com/project/isivisi/pybot/branch/master)
[![Code Health](https://landscape.io/github/isivisi/pybot/master/landscape.svg?style=flat)](https://landscape.io/github/isivisi/pybot/master)
[![pip](https://img.shields.io/pypi/v/Twitch_Pybot.svg)](https://pypi.python.org/pypi/Twitch-Pybot)

Pybot is an open source twitch chat bot.

![image](http://i.imgur.com/KK87zjt.png "Pybot settings")

### Dependencies
`python pybot.py -setup` will take care of any missing depencencies.

- [Python 3.5](https://www.python.org/downloads/release/python-351/)
- [Tornado Web Framework](https://github.com/tornadoweb/tornado)
- [Requests](https://github.com/kennethreitz/requests)
- [Chart.js](https://github.com/nnnick/Chart.js/)
- [Skeleton](https://github.com/dhg/Skeleton)

## Features

- Web interface `mobile friendly`
- Moderator control
- Custom commands
- Chat Filters
- User points
- Custom raffles
- Quotes
- Link grabbing

## Installation
View full installation guide [here](https://github.com/isivisi/pybot/wiki/Installation-guide-(windows))

- Install via pip 
 - `pip install twitch-pybot`
- Or pull repo and run
 - `python setup.py build install` 
 - or for development `python setup.py develop`
- Configure your bot via the web interface:
 - `pybot -run`
 - then go to `127.0.0.1:8888` in your browser
- or use the command line:
 - `pybot --config bot.name botusername`
 - `pybot --config bot.auth oauth:botauthentication`
 - `pybot --config twitch.channel channeltomoderate`
- You can view the full configure proccess [here](https://github.com/isivisi/pybot/wiki/Config)
- Now you can start pybot with `pybot -run`

If you're running multiple bots you may want to set the compatibility setting to change all the command names. This adds a p to the beginning of every command so multiple bot commands dont clash. ex: `!quote` would now be `!pquote`
- `pybot --config compatibility.append_to_commands p` 

## Usage

 - Commands

|Command|Parameters|wiki link
|---------|-------------------|----------|
!quotes ||[Quotes](https://github.com/isivisi/pybot/wiki/quote)
!permit |
!linkgrabber |
!linkban |
!command | add remove
!raffle | cost:#  name:""  trigger:!raffle  minpoints:#
!leave |

## Contributing

1. Fork it
2. Check the issues tab and start working on a bug / enhancement
3. Check the [wiki](https://github.com/isivisi/pybot/wiki) to understand how pybot works if you're confused
5. Submit a pull request :D

## History

Pybot started out as more of a closed source project mostly because I was using some terrible coding practices like hardcoded passwords, etc. I've burned alot of that stuff so I could more eaisly add it to a public github repository so anyone could download, run, and modify the code. I will be modifying pybot to be able to run without any help from its web interface, making it easier for people to modify and test it.

## License

[GNU General public licence](https://github.com/isivisi/pybot/blob/master/LICENSE)
