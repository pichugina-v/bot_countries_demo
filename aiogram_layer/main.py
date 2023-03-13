import logging
import os
import sys

from aiogram import executor

from aiogram_layer.src.app import dp

sys.path.append(os.path.join(os.getcwd()))
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
