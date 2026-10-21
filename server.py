import asyncio
import os
import secrets
import urllib.parse as urlparse
from contextlib import asynccontextmanager

import discord
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response
from itsdangerous import BadSignature, URLSafeTimedSerializer
from pydantic import ValidationError

from bot import Bot
from config import CONFIG
from datamodels import GameServer, NetworkBatch, OauthCallbackParams

load_dotenv()
BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
OAUTH2_CLIENT_ID: str | None = os.getenv("OAUTH2_CLIENT")
OAUTH_STATE_VALIDATION_KEY: str | None = os.getenv("OAUTH_STATE_VALIDATION_KEY")

assert isinstance(BOT_TOKEN, str), "Missing .env value 'BOT_TOKEN'"
assert isinstance(OAUTH2_CLIENT_ID, str), "Missing .env value 'OAUTH2_CLIENT_ID'"
assert isinstance(OAUTH_STATE_VALIDATION_KEY, str), (
    "Missing .env value 'OAUTH_STATE_VALIDATION_KEY'"
)

timed_state_serializer = URLSafeTimedSerializer(OAUTH_STATE_VALIDATION_KEY)
bot = Bot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    assert isinstance(BOT_TOKEN, str), "The bot token doesn't exist."
    asyncio.create_task(bot.start(token=BOT_TOKEN))
    yield
    await bot.close()


app = FastAPI(lifespan=lifespan)


@app.post("/network_batch/")
async def handle_network_batch(data: NetworkBatch):
    for message in data.operations:
        await bot.on_operation.invoke_blocking(message)
    for message in data.server_messages:
        await bot.on_server_message.invoke_blocking(message)
    for message in data.user_commands:
        await bot.on_user_command.invoke_blocking(message)
    for message in data.user_messages:
        await bot.on_user_message.invoke_blocking(message)


@app.post("/server_created/")
async def handle_server_created(data: GameServer):
    await bot.on_server_created.invoke_blocking(data)


@app.post("/server_closing/")
async def handle_server_closing(data: GameServer):
    await bot.on_server_closing.invoke_blocking(data)


def GenerateAuthUrl(guild_id: int | str, user_id: int | str):
    state = {
        "guild_id": str(guild_id),
        "user_id": str(user_id),
        "nonce": secrets.token_hex(16),
    }

    params = {
        "client_id": str(OAUTH2_CLIENT_ID),
        "redirect_uri": CONFIG.OAUTH_REDIRECT_URL,
        "scope": CONFIG.OAUTH_REQUIRED_PERMISSIONS,
        "response_type": "code",
        "state": timed_state_serializer.dumps(state),
    }
    return f"https://apis.roblox.com/oauth/v1/authorize?{urlparse.urlencode(params)}"


print(GenerateAuthUrl("[GUILDID]", "[USERID]"))


@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    query_params = dict(request.query_params)
    try:
        params = OauthCallbackParams.model_validate(query_params)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Malformed parameters.")

    try:
        state = timed_state_serializer.loads(params.state, max_age=300)
        guild_id = int(state["guild_id"])
        user_id = int(state["user_id"])
        # nonce = state["nonce"]
    except BadSignature as e:
        print(f"Failed handling oauth callback: BadSignature: {e}")
        raise HTTPException(
            status_code=400, detail="Request state expired. Please try again."
        )
    except KeyError as e:
        print(f"Failed handling oauth callback: KeyError: {e}")
        raise HTTPException(status_code=400, detail="Malformed request state.")
    except ValueError as e:
        print(f"Failed handling oauth callback: ValueError: {e}")
        raise HTTPException(status_code=400, detail="Malformed guild data.")
    # im highk too lazy to actually save and consume the nonce i'll do it later toootalllyyyy

    # TODO: save the data :3

    wguild = await bot.guild_handler.get_wrapped_guild_by_id(guild_id)
    if wguild is None:
        raise HTTPException(
            status_code=500, detail=f"Unable to fetch guild with id: {guild_id}"
        )
    member: discord.Member | None = wguild.guild.get_member(user_id)
    if member is None:
        try:
            member = await wguild.guild.fetch_member(user_id)
        except discord.NotFound:
            raise HTTPException(
                status_code=500, detail=f"Failed to fetch user with id: {user_id}"
            )

    if (not member.guild_permissions.administrator) and (
        member.id != wguild.guild.owner_id
    ):
        raise HTTPException(
            status_code=403, detail="User is not administrator in specified server."
        )

    return Response(content="Successfully linked.", status_code=200)
