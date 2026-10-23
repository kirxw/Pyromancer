from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import discord
from fastapi import HTTPException

from datamodels import GuildData, OauthCallbackParams
from modules.oauth2_networking import get_tokens_from_code

if TYPE_CHECKING:
    from bot import Bot


class WrappedGuild:
    bot: Bot
    guild: discord.Guild
    guild_data: GuildData
    initialized_event: asyncio.Event

    def __init__(self, bot: Bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild
        self.initialized_event = asyncio.Event()
        self.guild_handler = bot.guild_handler

    def apply_data(self, data: GuildData):
        self.data = data
        self.initialized_event.set()

    async def try_add_connection(self, user_id: int, params: OauthCallbackParams):
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
        await self.guild_handler.save_access_tokens(self, tokens, user_id)
