# using a python file instead of json to provide objects as config options...

import discord
from datamodels import BotConfig

CONFIG = BotConfig(
    COGS_DIRECTORY="cogs",
    PORT=8000,
    HOST="127.0.0.1",
    INTENTS=discord.Intents.all(),
    STATUS_TYPE=discord.Status.do_not_disturb,
    ACTIVITY_TYPE=discord.ActivityType.listening,
    ACTIVITY_NAME="across the abyss :3",

    MONGO_URL="mongodb://localhost:27017/",
    MONGO_DB_NAME="PYROMANCER_DATABASE",
    GUILD_COLLECTION_NAME="GUILDS",
)