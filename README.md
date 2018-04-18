![k2](logo.png)

[![MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/n303p4/Kitsuchan-NG/blob/master/LICENSE.txt)
[![Python](https://img.shields.io/badge/Python-3.6-brightgreen.svg)](https://python.org/)

**kitsuchan 2** (or **k2** for short) is a small, modular Discord bot written in `discord.py`,
with a focus on readable, portable, and easy to maintain code.

# How to run k2

k2 requires Python 3.6 or higher, as well as `discord.py` `rewrite`. If you're on Windows or
macOS, you should download and install Python from the [official website](http://python.org/).
If you're on Linux and your distribution ships Python 3.6 in the repositories, you should install
it from there instead. Some distributions still do not ship Python 3.6 (as of April 2018), so you
may have to compile it from source.

The bot should include a sample configuration file called `config.example.json`. Rename it to
`config.json` and fill it out accordingly. Then in a terminal, run:

```bash
python3 -m pip install --user -r requirements.txt
python3 kitsuchan.py
```

You may have to change the above commands slightly, depending on your operating system and the
location of your Python installation.

# Q&A

## Can I use Kitsuchan for my project?

Sure! Just read over [`LICENSE.txt`](LICENSE.txt) for details - it's very short, I promise! I
don't like long licenses, and you probably don't, either.

## Can I request a feature?

I don't take requests, but I do try and listen to feedback! Feel free to submit any suggestions
you have under the issue tracker. I'll be sure to ask you questions if I have any, and if I reject
your ideas, I'll try to explain my reasons as best as I can.

## Didn't you have another bot called Kitsuchan? What happened to that?

You might be talking about k3. The objective of that was to make a universal command framework,
but I realized that at best, it would either be severely limited, or unsustainably complex. I also
realized that with a good enough codebase, there's no need for such a framework, either, so I've
abandoned working on it.

## You're inconsistent with naming. Is there a particular way to spell this bot's name?

Nope. I'm terrible at that stuff, so use whatever you will. It's not like I can stop you anyway.
Kitsuchan 2, kitsuchan2, k2, K2, Kaytoo, etc.

## I want to help! How can I contribute?

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.
