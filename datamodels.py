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


class Message(BaseModel):
    JobId: str
    ServerType: Literal["Public", "Private", "Reserved", "Studio"]
    PlaceId: int
    Timestamp: int


class UserMessage(Message):
    UserId: int
    Name: str
    DisplayName: str
    Content: str


class UserCommand(Message):
    UserId: int
    Name: str
    DisplayName: str
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


class GuildData(TypedDict):
    _id: int
    ServerThreadChannel: int
    PermissionRoles: list[int]


class ServerData(TypedDict):
    _id: int
    ThreadId: int
    GuildId: int
    ConnectedUsers: dict[str, int]
