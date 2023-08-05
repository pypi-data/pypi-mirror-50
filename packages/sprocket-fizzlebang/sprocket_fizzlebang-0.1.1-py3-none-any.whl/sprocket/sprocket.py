from discord.ext import commands
import os

PREFIX = ("?", "!")
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
initial_extensions = ["cogs.base", "cogs.dice"]


def get_prefix(bot, message):
    prefixes = ["?", "!"]

    if not message.guild:
        return "?"

    return commands.when_mentioned_or(*prefixes)(bot, message)
