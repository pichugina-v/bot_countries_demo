import logging

from aiogram import Bot, Dispatcher, executor, types
from .settings import TG_API_TOKEN


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    bot = Bot(token=TG_API_TOKEN)
    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True)
