# using a python file instead of json to provide objects as config options...

import discord

CONFIG = {
    "COGS_DIRECTORY": "cogs",

    "INTENTS": discord.Intents.all(),
    "STATUS_TYPE": discord.Status.do_not_disturb,
    "ACTIVITY_TYPE": discord.ActivityType.listening,
    "ACTIVITY_NAME": "across the abyss :3",
}