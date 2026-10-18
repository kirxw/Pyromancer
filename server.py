import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI  # , HTTPException

# from config import CONFIG
from bot import Bot
from datamodels import NetworkBatch

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


@app.post("/post_network_batch/")
async def handle_api_invoke(data: NetworkBatch):
    await bot.handle_network_batch(data)
