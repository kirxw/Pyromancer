"""A file for handling game servers and their data"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pymongo import AsyncMongoClient

from classes.wrappedserver import WrappedServer
from config import CONFIG
from datamodels import (
    GameServer,
    ServerData,
)
from structuring import InboundMessage

if TYPE_CHECKING:
    from bot import Bot
    from classes.wrappedguild import WrappedGuild

MongoClient: AsyncMongoClient[ServerData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
ServerCollection = BotDatabase[CONFIG.SERVER_COLLECTION_NAME]


class ServerHandler:
    """Manages all roblox game servers"""

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
        bot.on_server_message.bind(self.on_server_message)

    # server data
    async def on_server_created(self, server: GameServer):
        """Creates an entry in the server database given server data, returns it. Won't make a new one if it already exists."""
        if server.JobId in self.servers:
            wserver = self.servers[server.JobId]
            await wserver.initialized_event.wait()
            return wserver

        wserver = WrappedServer(bot=self.bot, server=server)
        self.servers[server.JobId] = wserver

        server_data: ServerData | None = await ServerCollection.find_one(
            {"_id": server.JobId}
        )

        # wserver.apply_thread()
        return wserver

    async def on_server_closing(self, server: GameServer):
        """Removes a server from the database and closes the thread when the server shuts down"""

    async def on_server_message(self, server: GameServer, message: InboundMessage):
        """When a roblox server sends a message"""
        wserver: WrappedServer = await self.on_server_created(server)
