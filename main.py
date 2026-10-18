import os
from dotenv import load_dotenv
from bot import Bot

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

Bot(BOT_TOKEN)