from discord.ext import commands
from pymongo import AsyncMongoClient

from bot import Bot
from config import CONFIG
from datamodels import GuildData

MongoClient: AsyncMongoClient[GuildData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
GuildCollection = BotDatabase[CONFIG.GUILD_COLLECTION_NAME]

GuildCache = {}


class GuildHandler(commands.Cog):
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot


async def setup(bot: Bot):
    await bot.add_cog(GuildHandler(bot))
    print("Added GuildHandler cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("GuildHandler")
    print("Tore down GuildHandler cog.")
