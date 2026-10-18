# using a python file instead of json to provide objects as config options...

import discord
from dataclasses import dataclass

@dataclass(frozen=True)
class BotConfig:
    COGS_DIRECTORY: str
    PORT: int
    HOST: str
    INTENTS: discord.Intents
    STATUS_TYPE: discord.Status
    ACTIVITY_TYPE: discord.ActivityType
    ACTIVITY_NAME: str

CONFIG = BotConfig(
    COGS_DIRECTORY="cogs",
    PORT=8000,
    HOST="127.0.0.1",
    INTENTS=discord.Intents.all(),
    STATUS_TYPE=discord.Status.do_not_disturb,
    ACTIVITY_TYPE=discord.ActivityType.listening,
    ACTIVITY_NAME="across the abyss :3",
)