import discord
from pymongo import AsyncMongoClient

from datamodels import GuildData
from config import CONFIG

MongoClient: AsyncMongoClient[GuildData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
GuildCollection = BotDatabase[CONFIG.GUILD_COLLECTION_NAME]

