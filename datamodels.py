from typing import Literal, TypedDict

import discord
from pydantic import BaseModel, ConfigDict


class BotConfig(BaseModel):
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


class RobloxUser(BaseModel):
    UserId: int
    Name: int
    DisplayName: int
    JoinTime: int


class Message(BaseModel):
    JobId: str
    ServerType: Literal["Public", "Private", "Reserved", "Studio"]
    PlaceId: int
    Timestamp: int
    SharedSecret: int


class UserMessage(Message):
    Author: RobloxUser
    Content: str


class UserCommand(Message):
    Author: RobloxUser
    CommandName: str
    CommandBody: str


class ServerMessage(Message):
    Content: str


class Operation(Message):
    OperationName: str
    OperationBody: str


class NetworkBatch(BaseModel):
    user_messages: list[UserMessage]
    user_commands: list[UserCommand]
    server_messages: list[ServerMessage]
    operations: list[Operation]


class GameServer(BaseModel):
    PlaceId: int
    JobId: str
    StartupTime: int
    SharedSecret: int
    Players: list[RobloxUser]


class OauthCallbackParams(BaseModel):
    GuildId: int
    Code: str
    State: str


# SAVED GUILD DATA, NOT GUILD DATA OBJECT
class GuildData(TypedDict):
    _id: int
    ManagedPlaces: list[dict[int, str]]
    PermissionRoles: list[int]
    SharedSecret: str | None


# SAVED SERVER DATA, NOT SERVER DATA OBJECT
class ServerData(TypedDict):
    _id: str
    ThreadId: int
    GuildId: int
    ConnectedUsers: dict[str, int]
    PlaceId: int
