from __future__ import annotations

from typing import TYPE_CHECKING

from pymongo import AsyncMongoClient

from classes.wrappedserver import WrappedServer
from config import CONFIG
from datamodels import (
    GameServer,
    ManagedPlace,
    Operation,
    RobloxConnection,
    ServerData,
    ServerMessage,
    UserCommand,
    UserMessage,
)

if TYPE_CHECKING:
    from bot import Bot

MongoClient: AsyncMongoClient[ServerData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
ServerCollection = BotDatabase[CONFIG.SERVER_COLLECTION_NAME]


class ServerHandler:
    bot: Bot
    servers: dict[str, WrappedServer]
    managed_place_cache: dict[int, ManagedPlace]
    roblox_connection_cache: dict[str, RobloxConnection]

    def __init__(self, bot: Bot):
        self.bot = bot

        self.servers = {}
        self.place_connection_map = {}

        bot.on_server_created.bind(self.on_server_created)
        bot.on_server_closing.bind(self.on_server_closing)

        bot.on_user_command.bind(self.on_user_command)
        bot.on_user_message.bind(self.on_user_message)
        bot.on_server_message.bind(self.on_server_message)
        bot.on_operation.bind(self.on_operation)

    # server data
    async def on_server_created(self, server: GameServer):
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

    async def get_wrapped_server(self, server: GameServer):
        return await self.on_server_created(server)
