"""Ridiculous that this needs to exist"""

from discord.ext import commands


class AsyncCog(commands.Cog):
    """A cog base that provides hooks for each startup step"""

    async def setup_hook(self):
        """Runs during the bot's setup_hook, after all cogs have been intialized"""

    async def ready_hook(self):
        """Runs during the bot's on_ready, before on_running"""

    async def on_running(self):
        """Runs after all ready hooks, still running in the body of bot's on_ready"""
