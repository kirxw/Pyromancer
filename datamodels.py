from pydantic import BaseModel,ConfigDict
from typing import Literal

import discord

class BotConfig(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    COGS_DIRECTORY: str
    PORT: int
    HOST: str
    INTENTS: discord.Intents
    STATUS_TYPE: discord.Status
    ACTIVITY_TYPE: discord.ActivityType
    ACTIVITY_NAME: str

class Message(BaseModel):
    JobId: str
    ServerType: Literal["Public","Private","Reserved","Studio"]
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
    pass

class NetworkBatch(BaseModel):
    user_messages: list[UserMessage]
    user_commands = list[UserCommand]
    server_messages: list[ServerMessage]
    operations: list[Operation]