from bot import Bot
from classes.asynccog import AsyncCog


class ServerCog(AsyncCog):
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot


async def setup(bot: Bot):
    await bot.add_cog(ServerCog(bot))
    print("Added ServerCog cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("ServerCog")
    print("Tore down ServerCog cog.")
