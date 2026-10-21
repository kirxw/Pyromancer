import asyncio
import os

import discord

# from discord import app_commands
from discord.ext import commands

from classes.asynccog import AsyncCog
from classes.event import Event
from config import CONFIG
from modules.guild_handler import GuildHandler
from modules.server_handler import ServerHandler


class Bot(commands.Bot):
    on_user_message: Event
    on_server_message: Event
    on_user_command: Event
    on_operation: Event
    on_server_created: Event
    on_server_closing: Event
    guild_handler: GuildHandler
    server_handler: ServerHandler

    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=CONFIG.INTENTS,
            status=CONFIG.STATUS_TYPE,
            activity=discord.Activity(
                type=CONFIG.ACTIVITY_TYPE, name=CONFIG.ACTIVITY_NAME
            ),
        )

        self.on_operation = Event()
        self.on_server_message = Event()
        self.on_user_command = Event()
        self.on_user_message = Event()
        self.on_server_created = Event()
        self.on_server_closing = Event()
        self.ON_SETUP_FINISHED = (
            asyncio.Event()
        )  # use asyncio's event because it can be set and stay set

        self.guild_handler = GuildHandler(self)
        self.server_handler = ServerHandler(self)

    async def setup_hook(self):
        for filename in os.listdir(CONFIG.COGS_DIRECTORY):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                await self.load_extension(f"{CONFIG.COGS_DIRECTORY}.{module_name}")

        for cog_name, cog in self.cogs.items():
            if isinstance(cog, AsyncCog):
                print(f"Blocking for setup hook in cog {cog_name}")
                await cog.setup_hook()

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        for cog_name, cog in self.cogs.items():
            if isinstance(cog, AsyncCog):
                print(f"Blocking for ready hook in cog {cog_name}")
                await cog.ready_hook()

        self.ON_SETUP_FINISHED.set()

        for cog_name, cog in self.cogs.items():
            if isinstance(cog, AsyncCog):
                print(f"Asynchronously running {cog_name}")
                asyncio.create_task(cog.on_running())
