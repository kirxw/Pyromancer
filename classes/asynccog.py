# genuinely ridiculous that this needs to exist

from discord.ext import commands


class AsyncCog(commands.Cog):
    async def setup_hook(self):
        pass

    async def ready_hook(self):
        pass

    async def on_running(self):
        pass
