# [Pybot](http://pybot.ca)

Pybot is an open source twitch chat bot.

### Dependencies
`python pybot.py -setup` will take care of any missing depencencies.

- Python 2.7
- [Tornado Web Framework](https://github.com/tornadoweb/tornado)
- [Skeleton](https://github.com/dhg/Skeleton)

## Features

- Web interface ([view [WIP] pull request](https://github.com/isivisi/pybot/pull/17))
- Moderator control
- Custom commands
- Chat Filters
- User points
- Custom raffles
- Quotes
- Link grabbing

## Installation

This version of pybot is in early stages, currently you just need to:
- pull repo
- Run `python pybot.py -setup`
- Configure your bot:
 - `pybot --config bot.name botusername`
 - `pybot --config bot.auth oauth:botauthentication`
 - `pybot --config twitch.channel channeltomoderate`
- You can view the full configure proccess [here](https://github.com/isivisi/pybot/wiki/Config)
- Now you can start pybot with `pybot -run`

## Usage

 - Commands
  - `!quotes`
  - `!ppermit`
  - `!plinkgrabber`     (allows links people say to be saved)
  - `!plinkban` 
  - `!pcommand [add|remove|update]`
  - `!praffle [cost:#|minpoints:#]`
  - `!pleave`

## Contributing

1. Fork it
2. Check the issues tab and start working on a bug / enhancement
3. Check the [wiki](https://github.com/isivisi/pybot/wiki) understand how pybot works if you're confused
5. Submit a pull request :D

## History

Pybot started out as more of a closed source project mostly because I was using some terrible coding practices like hardcoded passwords, etc. I've burned alot of that stuff so I could more eaisly add it to a public github repository so anyone could download, run, and modify the code. I will be modifying pybot to be able to run without any help from its web interface, making it easier for people to modify and test it.

## License

[GNU General public licence](https://github.com/isivisi/pybot/blob/master/LICENSE)
