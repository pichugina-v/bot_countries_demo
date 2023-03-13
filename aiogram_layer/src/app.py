from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_layer.src.settings import TG_API_TOKEN

bot = Bot(token=TG_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
