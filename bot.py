import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

from config import CONFIG

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=CONFIG["INTENTS"],
            status=CONFIG["STATUS_TYPE"],
            activity=discord.Activity(
                type=CONFIG["ACTIVITY_TYPE"],
                name=CONFIG["ACTIVITY_NAME"],
            ),
        )

    async def setup_hook(self):
        for filename in os.listdir(CONFIG["COGS_DIRECTORY"]):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                await self.load_extension(module_name)

    async def on_ready(self):
        print(f"Logged in as {self.user}")