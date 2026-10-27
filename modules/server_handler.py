""" A file for handling game servers and their data """

from __future__ import annotations

from typing import TYPE_CHECKING

from pymongo import AsyncMongoClient

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

if TYPE_CHECKING:
    from bot import Bot
    from classes.wrappedguild import WrappedGuild

MongoClient: AsyncMongoClient[ServerData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
ServerCollection = BotDatabase[CONFIG.SERVER_COLLECTION_NAME]


class ServerHandler:
    """ Manages all roblox game servers """

    bot: Bot
    servers: dict[str, WrappedServer]
    place_cache: dict[
        int, dict[str, WrappedGuild | str | int]
    ]  # i am so done right now okay if youre reading this feel free

    def __init__(self, bot: Bot):
        self.bot = bot

        self.servers = {}

        bot.on_server_created.bind(self.on_server_created)
        bot.on_server_closing.bind(self.on_server_closing)

        bot.on_user_command.bind(self.on_user_command)
        bot.on_user_message.bind(self.on_user_message)
        bot.on_server_message.bind(self.on_server_message)
        bot.on_operation.bind(self.on_operation)

    # server data
    async def on_server_created(self, server: GameServer):
        """ Creates an entry in the server database given server data, returns it. Won't make a new one if it already exists. """
        if server.JobId in self.servers:
            wserver = self.servers[server.JobId]
            await wserver.initialized_event.wait()
            return wserver

        wserver = WrappedServer(bot=self.bot, server=server)
        self.servers[server.JobId] = wserver

        # server_data: ServerData | None = await ServerCollection.find_one(
        #     {"_id": server.JobId}
        # )

        # wserver.apply_thread()
        return wserver

    async def on_server_closing(self, server: GameServer):
        """Remotes a server from the database and closes the thread when the server shuts down"""
        pass

    # message types
    async def on_operation(self, operation: Operation):
        """Runs when a game server requests an operation"""
        pass

    async def on_server_message(self, message: ServerMessage):
        """Runs when the game server requests sending a system message"""
        pass

    async def on_user_command(self, command: UserCommand):
        """Runs when a roblox user runs a command"""
        pass

    async def on_user_message(self, message: UserMessage):
        """Runs when a roblox user sends a message in the ingame chat"""
        pass

    async def get_wrapped_server(self, server: GameServer):
        """Returns a WrappedServer given server data, making a new entry if it doesn't exist"""
        return await self.on_server_created(server)
