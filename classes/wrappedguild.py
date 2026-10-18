import discord

from bot import Bot
from datamodels import GuildData


class WrappedGuild:
    bot: Bot
    guild: discord.Guild
    guild_data: GuildData

    def __init__(self, bot: Bot, guild: discord.Guild, guild_data: GuildData):
        self.bot = bot
        self.guild = guild
        self.guild_data = guild_data
