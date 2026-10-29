"""Everything in here is pretty much useless, just did this for peace of mind"""

from typing import Literal

from pydantic import BaseModel

from datamodels import DiscordUser, RobloxUser

# inbound stuffs


class InboundMessage(BaseModel):
    Type: Literal["UserMessage", "UserCommand", "ServerMessage"]


class InboundUserMessage(InboundMessage):
    User: RobloxUser
    Message: str


class InboundUserCommand(InboundMessage):
    User: RobloxUser
    Command: str
    Body: str
    CommandUUID: str | None


class InboundServerMessage(InboundMessage):
    Body: str


class InboundPollBuffer(BaseModel):
    Buffers: dict[int, InboundUserCommand | InboundUserMessage | InboundServerMessage]
    RequestedBuffers: list[int]
    CurrentId: int


# outbound stuffs


class OutboundMessage(BaseModel):
    Type: Literal["UserMessage", "UserCommand"]


class OutboundUserMessage(OutboundMessage):
    User: DiscordUser
    Message: str


class OutboundUserCommand(BaseModel):
    User: DiscordUser
    Command: str
    Body: str


class OutboundPollBuffer(BaseModel):
    Buffers: dict[int, list[OutboundUserCommand | OutboundUserMessage]]
    RequestedBuffers: list[int]
    CurrentId: int
