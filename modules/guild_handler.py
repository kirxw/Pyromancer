from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

import discord
from pymongo import AsyncMongoClient, ReturnDocument

from classes.wrappedguild import WrappedGuild
from config import CONFIG
from datamodels import GuildData, RobloxConnection, TokensFromCodeResponse

if TYPE_CHECKING:
    from bot import Bot

MongoClient: AsyncMongoClient[GuildData] = AsyncMongoClient(CONFIG.MONGO_URL)
BotDatabase = MongoClient[CONFIG.MONGO_DB_NAME]
GuildCollection = BotDatabase[CONFIG.GUILD_COLLECTION_NAME]


class GuildHandler:
    bot: Bot
    guilds: dict[int, WrappedGuild]

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle_guild(self, guild: discord.Guild):
        if guild.id in self.guilds:
            wguild = self.guilds[guild.id]
            await wguild.initialized_event.wait()
            return wguild

        wguild = WrappedGuild(bot=self.bot, guild=guild)
        self.guilds[guild.id] = wguild

        default_data = GuildData(
            _id=guild.id,
            PermissionRoles=[],
            SharedSecret=None,
            RobloxConnections={},
            ManagedPlaces={},
        )

        guild_data: GuildData | None = await GuildCollection.find_one_and_update(
            filter={"_id": guild.id},
            update={"$setOnInsert": default_data},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        if guild_data is None:
            raise RuntimeError(
                "Guild document was nil after upsert. This should be impossible."
            )

        for place_id, managed_place in guild_data["ManagedPlaces"].items():
            self.bot.server_handler.place_cache[place_id] = {
                "ConnectionUUID": managed_place["ConnectionUUID"],
                "UniverseId": managed_place["UniverseId"],
                "WGuild": wguild,
                "SharedSecret": managed_place["SharedSecret"],
            }

        wguild.apply_data(guild_data)
        return wguild

    async def get_wrapped_guild(self, guild: discord.Guild):
        return await self.handle_guild(guild)

    async def get_wrapped_guild_by_id(self, id: int):
        guild: discord.Guild | None = self.bot.get_guild(id)
        if guild is None:
            try:
                guild = await self.bot.fetch_guild(id)
            except discord.NotFound as e:
                print(f"Failed to fetch guild: {e}")
                return None

        return await self.get_wrapped_guild(guild)

    async def get_and_save_resources(self, wguild: WrappedGuild, connection_uuid: str):
        pass

    async def save_access_tokens(
        self,
        wguild: WrappedGuild,
        tokens: TokensFromCodeResponse,
        user_id: int,
        connection_uuid: str | None = None,
    ):
        now: float = datetime.now().timestamp()
        time_remaining: float = tokens["expires_in"]
        expiration = int(now + time_remaining)
        connection: RobloxConnection = RobloxConnection(
            AccessToken=tokens["access_token"],
            RefreshToken=tokens["refresh_token"],
            ExpiresAt=expiration,
            IssuedAt=int(now),
            DiscordIssuerId=user_id,
            ResourcesInitialized=False,
            ManagedUniverseIds=[],
            RobloxIssuerId=None,
            RobloxOwnerType=None,
        )
        if connection_uuid is None:
            connection_uuid = str(uuid.uuid4())

        await wguild.update(
            {"$set": {f"RobloxConnections.{connection_uuid}": connection}}
        )

        return connection_uuid

    async def update_access_tokens(
        self, wguild: WrappedGuild, connection_uuid: str, tokens: TokensFromCodeResponse
    ):
        await wguild.update(
            {
                "$set": {
                    f"RobloxConnections.{connection_uuid}.AccessToken": tokens[
                        "access_token"
                    ],
                    f"RobloxConnections.{connection_uuid}.RefreshToken": tokens[
                        "refresh_token"
                    ],
                }
            }
        )

    async def proper_update_guild_data(
        self, wguild: WrappedGuild, update: dict[str, Any]
    ):
        guild_data: GuildData | None = await GuildCollection.find_one_and_update(
            filter={"_id": wguild.guild.id},
            update=update,
            return_document=ReturnDocument.AFTER,
        )
        if guild_data is None:
            raise RuntimeError(
                "Guild document was nil after upsert. This should be impossible."
            )
        wguild.data = guild_data
        return guild_data
