import discord
from discord import app_commands

from bot import Bot
from classes.asynccog import AsyncCog
from modules.oauth2_networking import generate_user_auth_url


class GuildCog(AsyncCog):
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(
        name="connect",
        description="Generate an Oauth2 URL to connect the bot to your account",
    )
    async def connect_account(self, interaction: discord.Interaction):
        member: discord.Member | discord.User = interaction.user
        guild: discord.Guild | None = interaction.guild
        if not isinstance(member, discord.Member) or not isinstance(
            guild, discord.Guild
        ):
            await interaction.response.send_message(
                "This command must be used in a guild!",
                ephemeral=True,
            )
            return

        if (not member.guild_permissions.administrator) and (
            interaction.user.id != guild.owner_id
        ):
            await interaction.response.send_message(
                "You cannot connect a game without being an administrator of this guild!",
                ephemeral=True,
            )
            return

        auth_url = generate_user_auth_url(guild.id, member.id)
        await interaction.response.send_message(
            f"Oauth2 URL generated! Navigate to {auth_url} and link the games you'd like to manage.",
            ephemeral=True,
        )
