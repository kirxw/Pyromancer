from pydantic import BaseModel,ConfigDict

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

class UserMessage(BaseModel):
    UserId: int
    Name: str
    DisplayName: str

class UserCommand(BaseModel):
    pass

class ServerMessage(BaseModel):
    pass

class NetworkBatch(BaseModel):
    user_messages: list[UserMessage]
    user_commans = list[UserCommand]
    server_messages: list[ServerMessage]