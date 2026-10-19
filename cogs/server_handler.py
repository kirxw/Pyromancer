from discord.ext import commands
from pymongo import AsyncMongoClient

from bot import Bot
from classes.wrappedserver import WrappedServer
from config import CONFIG
from datamodels import (
    GameServer,
    Operation,
    ServerData,
    ServerMessage,
    UserCommand,
    UserMessage,
)

MongoClient: AsyncMongoClient[ServerData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
ServerCollection = BotDatabase[CONFIG.SERVER_COLLECTION_NAME]


class ServerHandler(commands.Cog):
    bot: Bot
    servers: dict[int, WrappedServer]

    def __init__(self, bot: Bot):
        self.bot = bot

        bot.on_server_created.bind(self.on_server_created)
        bot.on_server_closing.bind(self.on_server_closing)

        bot.on_user_command.bind(self.on_user_command)
        bot.on_user_message.bind(self.on_user_message)
        bot.on_server_message.bind(self.on_server_message)
        bot.on_operation.bind(self.on_operation)

    # server data
    async def on_server_created(self, server: GameServer):
        pass

    async def on_server_closing(self, server: GameServer):
        pass

    # message types
    async def on_operation(self, operation: Operation):
        pass

    async def on_server_message(self, message: ServerMessage):
        pass

    async def on_user_command(self, command: UserCommand):
        pass

    async def on_user_message(self, message: UserMessage):
        pass


async def setup(bot: Bot):
    await bot.add_cog(ServerHandler(bot))
    print("Added ServerHandler cog.")


async def teardown(bot: Bot):
    await bot.remove_cog("ServerHandler")
    print("Tore down ServerHandler cog.")
