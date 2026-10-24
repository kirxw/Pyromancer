import datetime

import discord
from discord import app_commands

from bot import Bot
from classes.asynccog import AsyncCog
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
    async def manage_place(self, interaction: discord.Interaction, place_id: str):
        member, guild = await is_owner(interaction=interaction)
        if member == None or guild == None:
            return

        try:
            place_int = int(place_id)
        except ValueError:
            await interaction.response.send_message(
                f"place_id must be an integer, got {place_id}", ephemeral=True
            )
            return

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
