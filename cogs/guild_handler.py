import discord
from discord.ext import commands
from pymongo import AsyncMongoClient, ReturnDocument

from bot import Bot
from classes.asynccog import AsyncCog
from classes.wrappedguild import WrappedGuild
from config import CONFIG
from datamodels import GuildData

MongoClient: AsyncMongoClient[GuildData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
GuildCollection = BotDatabase[CONFIG.GUILD_COLLECTION_NAME]

GuildCache = {}


class GuildHandler(AsyncCog):
    bot: Bot
    guilds: dict[int, WrappedGuild]

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        await self.handle_guild(guild)

    async def ready_hook(self):
        for guild in self.bot.guilds:
            await self.handle_guild(guild)

    async def handle_guild(self, guild: discord.Guild):
        if guild.id in GuildCache:
            return

        default_data = GuildData(
            _id=guild.id,
            ManagedPlaces=[],
            PermissionRoles=[],
            SharedSecret=None,
        )

        guild_data: GuildData | None = await GuildCollection.find_one_and_update(
            filter={"_id": guild.id},
            update={"$setOnInsert": default_data},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        if guild_data is None:
            raise RuntimeError(
                "Guild document was nil after upsert. This should be impossible."
            )

        wguild = WrappedGuild(bot=self.bot, guild=guild, guild_data=guild_data)
        GuildCache[guild.id] = wguild

        return wguild

    async def get_wrapped_guild(self, guild: discord.Guild):
        return self.handle_guild(guild)


async def setup(bot: Bot):
    await bot.add_cog(GuildHandler(bot))
    print("Added GuildHandler cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("GuildHandler")
    print("Tore down GuildHandler cog.")
