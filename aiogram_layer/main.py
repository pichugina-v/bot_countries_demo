import logging
import os
import sys

from aiogram import executor

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd()))
    from aiogram_layer.src.app import dp
    executor.start_polling(dp, skip_updates=True)
