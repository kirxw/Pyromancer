import asyncio

import discord

from bot import Bot
from datamodels import GuildData


class WrappedGuild:
    bot: Bot
    guild: discord.Guild
    guild_data: GuildData
    initialized_event: asyncio.Event

    def __init__(self, bot: Bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild
        self.initialized_event = asyncio.Event()

    def apply_data(self, data: GuildData):
        self.data = data
        self.initialized_event.set()
