"""The data types used by Pyromancer"""

from typing import Any, TypedDict

import discord
from pydantic import BaseModel, ConfigDict


class BotConfig(BaseModel):
    """Pyromancer's configuration"""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    COGS_DIRECTORY: str
    PORT: int
    HOST: str
    INTENTS: discord.Intents
    STATUS_TYPE: discord.Status
    ACTIVITY_TYPE: discord.ActivityType
    ACTIVITY_NAME: str
    MONGO_URL: str
    MONGO_DB_NAME: str
    GUILD_COLLECTION_NAME: str
    SERVER_COLLECTION_NAME: str
    OAUTH_REQUIRED_PERMISSIONS: str
    OAUTH_REDIRECT_URL: str


class RobloxUser(BaseModel):
    """Representation of an ingame roblox user"""

    UserId: int
    Name: int
    DisplayName: int
    JoinTime: int


class Message(BaseModel):
    """The base of an inbound message"""

    # JobId: str
    # ServerType: Literal["Public", "Private", "Reserved", "Studio"]
    # PlaceId: int
    Timestamp: int
    SharedSecret: int


class UserMessage(Message):
    """A message sent by an ingame roblox user"""

    Author: RobloxUser
    Content: str


class UserCommand(Message):
    """A command issued by an ingame roblox user"""

    Author: RobloxUser
    CommandName: str
    CommandBody: str


class ServerMessage(Message):
    """A message to display sent by a roblox server"""

    Content: str
    Embeds: list[Any]


class Operation(Message):
    """An automated operation sent by a roblox server"""

    OperationName: str
    OperationBody: str


class NetworkBatch(BaseModel):
    """A batch of messages sent by a roblox server"""

    user_messages: list[UserMessage]
    user_commands: list[UserCommand]
    server_messages: list[ServerMessage]
    operations: list[Operation]


class GameServer(BaseModel):
    """An active roblox server"""

    PlaceId: int
    JobId: str
    StartupTime: int
    SharedSecret: int
    Players: list[RobloxUser]


class OauthCallbackParams(BaseModel):
    """The URL params recieved during oauth completion"""

    code: str
    state: str


class DiscordUser(BaseModel):
    UserId: str
    Name: str
    DisplayName: str


class RobloxConnection(TypedDict):
    """An oauth connection to a roblox account"""

    AccessToken: str
    RefreshToken: str
    ExpiresAt: int

    IssuedAt: int
    DiscordIssuerId: int

    RobloxIssuerId: int | None
    RobloxOwnerType: str | None

    ManagedUniverseIds: list[int]
    ResourcesInitialized: bool


class ManagedPlace(TypedDict):
    """A place managed through a connection"""

    UniverseId: int
    ConnectionUUID: str
    SharedSecret: str


class TokensFromCodeResponse(TypedDict):
    """The result returned by fetching oauth tokens"""

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str


class GuildData(TypedDict):
    """Saved data about a guild, this is not a guild object"""

    _id: int
    PermissionRoles: list[int]
    SharedSecret: str | None

    RobloxConnections: dict[str, RobloxConnection]  # UUID: RobloxConnection
    ManagedPlaces: dict[int, ManagedPlace]  # PlaceID: ManagedPlace


class ServerData(TypedDict):
    """Saved data about an active roblox server, this is not a server object"""

    _id: str
    ThreadId: int
    GuildId: int
    ConnectedUsers: dict[str, int]
    PlaceId: int
