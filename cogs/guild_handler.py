import discord
from discord.ext import commands
from pymongo import AsyncMongoClient

from bot import Bot
from classes.asynccog import AsyncCog
from config import CONFIG
from datamodels import GuildData

MongoClient: AsyncMongoClient[GuildData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
GuildCollection = BotDatabase[CONFIG.GUILD_COLLECTION_NAME]

GuildCache = {}


class GuildHandler(AsyncCog):
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        pass


async def setup(bot: Bot):
    await bot.add_cog(GuildHandler(bot))
    print("Added GuildHandler cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("GuildHandler")
    print("Tore down GuildHandler cog.")
