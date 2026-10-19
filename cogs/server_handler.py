from discord.ext import commands
from pymongo import AsyncMongoClient

from bot import Bot
from config import CONFIG
from datamodels import GuildData

MongoClient: AsyncMongoClient[GuildData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
ServerCollection = BotDatabase[CONFIG.SERVER_COLLECTION_NAME]

GuildCache = {}


class ServerHandler(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


async def setup(bot: Bot):
    await bot.add_cog(ServerHandler(bot))
    print("Added ServerHandler cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("ServerHandler")
    print("Tore down ServerHandler cog.")
