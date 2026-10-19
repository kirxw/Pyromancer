import discord
from discord.ext import commands

from bot import Bot
from classes.asynccog import AsyncCog


class GuildCog(AsyncCog):
    bot: Bot

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        await self.bot.guild_handler.handle_guild(guild)

    async def ready_hook(self):
        for guild in self.bot.guilds:
            await self.bot.guild_handler.handle_guild(guild)


async def setup(bot: Bot):
    await bot.add_cog(GuildCog(bot))
    print("Added GuildCog cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("GuildCog")
    print("Tore down GuildCog cog.")
