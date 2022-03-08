# quizcord bot #

Get it? 'cause it's a pubquiz bot for discord 😎👉👉

## About ##

This little bot allows you to set up pubquizzes for discord, automatically posts
the questions for you, evaluates answers and keeps track of points. Quizzes are
created in YAML files and can be loaded via chat commands. The bot is also
controlled via chat commands, only accesible by previously defined admins.

## Setup ##

### Installation ###

To get started clone this repository:

```cmd
git clone https://github.com/sebastian-stubenvoll/quizcord-bot.git
```

Next either manually install the dependencies found in `Pipfile` or use `pipenv
install` to get set up automatically.

A small disclaimer: This bot was written
and tested in **python 3.9**, however any python version from 3.7 upwards should
work. This is because parts of the code rely on dictionaries preserving
insertion order.

Next set up an application and a bot user for it at the [Discord developer
portal](https://discord.com/developers/applications). This is where you obtain
your bot api token. Now create a `.env` file in the root directory of this
repository containing entries for `DISCORD_TOKEN` and `ADMINS`. For example:

```env
DISCORD_TOKEN="1234567890YOURTOKEN0987654321"
ADMINS="12345678987654321,000111000111000"
```

Note that `ADMINS` needs to contain a comma-separated list of Discord IDs. You
can easily obtain someone's Discord ID by right-clicking on their avatar and
selecting `copy ID`.

Now all there's left to do is creating your quiz (see next section).

### Create a quiz ###

Coming soon...
