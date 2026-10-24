import datetime
import secrets

import discord
import httpx
from discord import app_commands

from bot import Bot
from classes.asynccog import AsyncCog
from datamodels import ManagedPlace
from modules.oauth2_networking import generate_user_auth_url


async def is_owner(interaction: discord.Interaction):
    member: discord.Member | discord.User = interaction.user
    guild: discord.Guild | None = interaction.guild
    if not isinstance(member, discord.Member) or not isinstance(guild, discord.Guild):
        await interaction.response.send_message(
            "This command must be used in a guild!",
            ephemeral=True,
        )
        return None, None

    if (not member.guild_permissions.administrator) and (
        interaction.user.id != guild.owner_id
    ):
        await interaction.response.send_message(
            "You cannot connect a game without being an administrator of this guild!",
            ephemeral=True,
        )
        return None, None

    return member, guild


class GuildCog(AsyncCog):
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(
        name="manage_place",
        description="Manage a place from any game that's already been connected via /connect",
    )
    async def manage_place(self, interaction: discord.Interaction, place_id: str | int):
        member, guild = await is_owner(interaction=interaction)
        if member == None or guild == None:
            return
        await interaction.response.defer(ephemeral=True)
        wguild = await self.bot.guild_handler.get_wrapped_guild(guild)

        try:
            place_id = int(place_id)
        except ValueError:
            await interaction.followup.send(
                f"place_id must be an integer, got {place_id}", ephemeral=True
            )
            return

        if place_id in wguild.data["ManagedPlaces"]:
            await interaction.followup.send(
                f"This guild already manages place with id {place_id}", ephemeral=True
            )
            return

        if place_id in self.bot.server_handler.managed_place_cache:
            await interaction.followup.send(
                f"The place with id {place_id} is already managed by a **different** guild.",
                ephemeral=True,
            )
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
            )
            response.raise_for_status()
            universe_id: int = response.json()["universeId"]

        connection_uuid: str | None = None
        for cuuid, connection in wguild.data["RobloxConnections"].items():
            if universe_id in connection["ManagedUniverseIds"]:
                connection_uuid = cuuid
                break
        if connection_uuid is None:
            await interaction.followup.send(
                f"This guild is not linked to universe {universe_id}", ephemeral=True
            )
            return

        secret_key = secrets.token_urlsafe(32)
        managed_place = ManagedPlace(
            SharedSecret=secret_key,
            UniverseId=universe_id,
            ConnectionUUID=connection_uuid,
        )

        await wguild.update(
            {
                "$set": {
                    f"ManagedPlaces.{place_id}": managed_place,
                }
            }
        )

        self.bot.server_handler.managed_place_cache[place_id] = managed_place

        await interaction.followup.send(
            f"Successfully linked place {place_id}.\nHere is that place's communication token. Save it somewhere, you won't be able to fetch it again:\n||{secret_key}||",
            ephemeral=True,
        )

    @app_commands.command(
        name="connect",
        description="Generate an Oauth2 URL to connect the bot to your account",
    )
    async def connect_account(self, interaction: discord.Interaction):
        member, guild = await is_owner(interaction=interaction)
        if member == None or guild == None:
            return

        timestamp = int(datetime.datetime.now(datetime.UTC).timestamp()) + 5 * 60
        auth_url = generate_user_auth_url(guild.id, member.id)
        await interaction.response.send_message(
            f"Oauth2 URL generated! Navigate to {auth_url} and link the games you'd like to manage.\nURL expires <t:{timestamp}:R>",
            ephemeral=True,
        )
