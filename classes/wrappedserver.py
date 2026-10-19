from bot import Bot
from datamodels import GameServer


class WrappedServer:
    bot: Bot
    data: GameServer

    def __init__(self, bot: Bot, data: GameServer):
        self.bot = bot
        self.data = data
