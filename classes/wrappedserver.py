from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import discord

from datamodels import GameServer

if TYPE_CHECKING:
    from bot import Bot


class WrappedServer:
    bot: Bot
    server: GameServer
    initialized_event: asyncio.Event
    thread: discord.Thread

    def __init__(self, bot: Bot, server: GameServer):
        self.bot = bot
        self.server = server

        place_data = self.bot.server_handler.place_cache[server.PlaceId]
        assert place_data["SharedSecret"] == server.SharedSecret, (
            "Incorrect secret passed."
        )
        self.place_data = place_data

    def apply_thread(self, thread: discord.Thread):
        self.thread = thread
        self.initialized_event.set()
