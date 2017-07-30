## k2a

[![MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/n303p4/Kitsuchan-NG/blob/master/LICENSE.txt)
[![Python](https://img.shields.io/badge/Python-3.6-brightgreen.svg)](https://python.org/)

**kitsuchan 2a** (or **k2a** for short) is a simple, modular Discord bot written in `discord.py`.
It's actually based on the Discord bot in **[k3](https://github.com/ClaraIO/kitsuchan)**, and is
thus not closely related to previous generations of Kitsuchan. The objective was to simplify
the bot's codebase.

## How to run k2a

k2a requires Python 3.6 or higher, as well as `discord.py` `rewrite`. This is a requirement, not
just a recommendation. If you get a syntax error, that's because you're running Python 3.5 or
older.

The bot should come with a sample configuration file called `config.example.json`. Rename it to
`config.json` and fill it out accordingly. Then in a terminal, run:

```bash
python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite
python3 kitsuchan.py
```

## License

See `LICENSE.txt` for details on that.
