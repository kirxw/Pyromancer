"""A collection of oauth2 functions"""

import os
import secrets
import urllib.parse as urlparse

import httpx
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

from config import CONFIG

load_dotenv()
OAUTH2_CLIENT_ID: str | None = os.getenv("OAUTH2_CLIENT")
OAUTH2_SECRET: str | None = os.getenv("OAUTH2_SECRET")
OAUTH_STATE_VALIDATION_KEY: str | None = os.getenv("OAUTH_STATE_VALIDATION_KEY")

assert isinstance(OAUTH2_CLIENT_ID, str), "Missing .env value 'OAUTH2_CLIENT_ID'"
assert isinstance(OAUTH2_SECRET, str), "Missing .env value 'OAUTH2_SECRET'"
assert isinstance(OAUTH_STATE_VALIDATION_KEY, str), (
    "Missing .env value 'OAUTH_STATE_VALIDATION_KEY'"
)

timed_state_serializer = URLSafeTimedSerializer(OAUTH_STATE_VALIDATION_KEY)


async def get_resources(access_token: str):
    """Fetch available resources"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://apis.roblox.com/oauth/v1/token/resources",
            data={
                "token": access_token,
                "client_id": OAUTH2_CLIENT_ID,
                "client_secret": OAUTH2_SECRET,
            },
        )
        response.raise_for_status()
        return response.json()


async def get_roblox_user(access_token: str):
    """Fetch the user associated with the oauth connectin"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://apis.roblox.com/oauth/v1/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        response.raise_for_status()
        return response.json()


async def get_tokens_from_refresh(refresh_token: str):
    """Update the auth token and refresh token given a refresh token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://apis.roblox.com/oauth/v1/token",
            data={
                "client_id": OAUTH2_CLIENT_ID,
                "client_secret": OAUTH2_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )
        response.raise_for_status()
        return response.json()


async def get_tokens_from_code(code: str):
    """Get the auth and refresh from the one time code after first auth"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://apis.roblox.com/oauth/v1/token",
            data={
                "client_id": OAUTH2_CLIENT_ID,
                "client_secret": OAUTH2_SECRET,
                "grant_type": "authorization_code",
                "code": code,
            },
        )
        response.raise_for_status()
        return response.json()


def generate_user_auth_url(guild_id: int | str, user_id: int | str):
    """Format the oauth url"""
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
