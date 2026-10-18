# genuinely ridiculous that this needs to exist

from discord.ext import commands


class AsyncCog(commands.Cog):
    async def setup_hook(self):
        pass
