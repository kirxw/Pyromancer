"""File holding the WrappedGuild class"""

from __future__ import annotations

import asyncio
import datetime
from typing import TYPE_CHECKING, Any

import discord
from fastapi import HTTPException

from datamodels import GuildData, OauthCallbackParams
from modules.oauth2_networking import (
    get_resources,
    get_tokens_from_code,
    get_tokens_from_refresh,
)

if TYPE_CHECKING:
    from bot import Bot


class WrappedGuild:
    """
    An object containing a guild, data about the guild, and methods pertaining to the management of guild data
    Exposes WrappedGuild.initialized_event, which will be set after data has been applied
    """

    bot: Bot
    guild: discord.Guild
    data: GuildData
    initialized_event: asyncio.Event

    def __init__(self, bot: Bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild
        self.initialized_event = asyncio.Event()
        self.guild_handler = bot.guild_handler

    def apply_data(self, data: GuildData):
        """Sets the WrappedGuild's data and sets the initialized event"""

        self.data = data
        self.initialized_event.set()

    async def update(self, update: dict[str, Any]):
        """A wrapper to guild_handler.update(), runs a mongo query and updates the cached data too"""
        return await self.guild_handler.proper_update_guild_data(self, update)

    async def get_access_token(self, connection_uuid: str):
        """Gets the most recent access token, fetching a new one if it's expired"""
        roblox_connections = self.data["RobloxConnections"]
        if connection_uuid not in roblox_connections:
            raise KeyError(f"Unknown connection UUID {connection_uuid}")

        connection = roblox_connections[connection_uuid]
        now: float = datetime.datetime.now(datetime.UTC).timestamp()

        if connection["ExpiresAt"] < now:
            tokens = await get_tokens_from_refresh(connection["RefreshToken"])
            await self.guild_handler.update_access_tokens(self, connection_uuid, tokens)
            connection["AccessToken"] = tokens["access_token"]
            connection["RefreshToken"] = tokens["refresh_token"]

        return connection["AccessToken"]

    async def try_add_connection(self, user_id: int, params: OauthCallbackParams):
        """Attempts to add a RobloxConnection given an oauth callback"""
        member: discord.Member | None = self.guild.get_member(user_id)
        if member is None:
            try:
                member = await self.guild.fetch_member(user_id)
            except discord.NotFound:
                raise HTTPException(
                    status_code=500, detail=f"Failed to fetch user with id: {user_id}"
                )

        if (not member.guild_permissions.administrator) and (
            member.id != self.guild.owner_id
        ):
            raise HTTPException(
                status_code=403, detail="User is not administrator in specified server."
            )

        tokens = await get_tokens_from_code(params.code)
        UUID = await self.guild_handler.save_access_tokens(self, tokens, user_id)

        managed_universe_ids: list[int] = []
        resources = await get_resources(tokens["access_token"])
        for resource in resources["resource_infos"]:
            universe_ids = resource["resources"]["universe"]["ids"]
            managed_universe_ids.extend(universe_ids)

        print("NOW MANAGING ADDITIONAL IDS:", managed_universe_ids)

        await self.update(
            {
                "$set": {
                    # f"RobloxConnections.{UUID}.RobloxIssuerId": connection,
                    # f"RobloxConnections.{UUID}.RobloxOwnerType": connection,
                    f"RobloxConnections.{UUID}.ResourcesInitialized": True,
                    f"RobloxConnections.{UUID}.ManagedUniverseIds": managed_universe_ids,
                }
            }
        )
