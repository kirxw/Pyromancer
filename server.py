import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI  # , HTTPException

# from config import CONFIG
from bot import Bot
from datamodels import GameServer, NetworkBatch

load_dotenv()
BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")

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
