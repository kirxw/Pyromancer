import os
import asyncio

import discord
#from discord import app_commands
from discord.ext import commands

from config import CONFIG
from modules.event import Event
from datamodels import NetworkBatch

class Bot(commands.Bot):
    on_user_message: Event
    on_server_message: Event
    on_user_command: Event
    on_operation: Event

    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=CONFIG.INTENTS,
            status=CONFIG.STATUS_TYPE,
            activity=discord.Activity(
                type=CONFIG.ACTIVITY_TYPE,
                name=CONFIG.ACTIVITY_NAME
            ),
        )

        self.on_operation = Event()
        self.on_server_message = Event()
        self.on_user_command = Event()
        self.on_user_message = Event()
        self.ON_SETUP_FINISHED = asyncio.Event()

    async def handle_network_batch(self, data: NetworkBatch):
        for message in data.operations:
            await self.on_operation.invoke_blocking(message)
        for message in data.server_messages:
            await self.on_server_message.invoke_blocking(message)
        for message in data.user_commands:
            await self.on_user_command.invoke_blocking(message)
        for message in data.user_messages:
            await self.on_user_message.invoke_blocking(message)

    async def setup_hook(self):
        for filename in os.listdir(CONFIG.COGS_DIRECTORY):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                await self.load_extension(module_name)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.ON_SETUP_FINISHED.set()