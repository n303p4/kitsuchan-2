![k2](logo.png)

[![MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/n303p4/Kitsuchan-NG/blob/master/LICENSE.txt)
[![Python](https://img.shields.io/badge/Python-3.6-brightgreen.svg)](https://python.org/)
[![GPA](https://codeclimate.com/github/n303p4/kitsuchan-2/badges/gpa.svg)](https://codeclimate.com/github/n303p4/kitsuchan-2)

**kitsuchan 2** (or **k2** for short) is a small, modular Discord bot written in `discord.py`
with a focus on high quality code. This is a continuation and significant overhaul of the bot
called **Kitsuchan-NG**, built with the intent of sleekening the codebase.

## How to run k2

k2 requires Python 3.6 or higher, as well as `discord.py` `rewrite`. This is a requirement, not
just a recommendation. If you get a syntax error, that's because you're running Python 3.5 or
older. As of July 2017, many Linux distributions do not have Python 3.6 by default, so you might
have to install it specifically.

The bot should include a sample configuration file called `config.example.json`. Rename it to
`config.json` and fill it out accordingly. Then in a terminal, run:

```bash
python3 -m pip install --user -r requirements.txt
python3 kitsuchan.py
```

## Where are all the features? The old bot has way more stuff than this.

Well, first of all: For the purposes of simplifying maintenance and reducing feature creep,
this bot *won't* have everything that the old bot did. Many of Kitsuchan-NG's features never
really got used, anyway. Secondly, things are still in the process of being ported over and
cleaned up.

## What's the point? Isn't k3 going to replace k2 anyway?

k3 is meant for a different sort of bot - one that can easily be ported across different chat
protocols, but often at the expense of deeper integration. k2 is a Discord bot first and foremost,
and that gives it the ability to use many Discord-specific features that k3 cannot (at least
currently) take advantage of. This may change in the future as k3 matures, but it's not the case
yet. That being said, the development of this bot is closely tied with that of k3.

## You're inconsistent with naming. Is there a particular way to spell this bot's name?

Nope. I'm terrible at that stuff, so use whatever you will. It's not like I can stop you anyway.
Kitsuchan 2, kitsuchan2, k2, K2, Kaytoo, etc.

## License

See `LICENSE.txt` for details on that.
