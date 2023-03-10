from aiogram import Bot, Dispatcher
from src.settings import TG_API_TOKEN


bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)
