# Introduction

So you want to contribute to Kitsuchan development. Great! Here's how you can help.

# Getting started

Make a fork of the repository. Then make whatever changes you wish to see, and open a pull
request. If the changes are judged to be acceptable, they'll be merged into the main tree.

# Style guide

* Commit messages should be descriptive enough. They don't need to be long, and there's no
  particular standard for them. But they should give some idea of what the commit is about.
* Kitsuchan mostly adheres to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for coding style.
  Please read up on it if you're unsure about formatting, or if the linter is complaining.
* Use `pylint` for your linting and do your best not to annoy it. Minor warnings are okay, though.
    * For example, global instance variables can be in lowercase. That's fine. Global constants
      should be uppercase, though.
* In regards to the above, it is **strongly** recommended that you use a text editor with support
  for linting. It will make your life much easier.
* Maximum line length is 100 characters.
* To handle HTTP requests and responses in your commands, use `ctx.bot.session`, which is an
  `aiohttp.ClientSession`. If you're unfamiliar, read up on
  [`aiohttp`](https://aiohttp.readthedocs.io/en/stable/) documentation. Usage of libraries such
  as `requests` is generally not okay, and pull requests that use these libraries will be rejected
  unless you have a good enough reason for it.
* Kitsuchan has a number of helper functions under the `k2.helpers` module. Use it when
  applicable, but try not to abuse it too heavily.
* If you're unsure of how to do something, look around at the code, or ask!
