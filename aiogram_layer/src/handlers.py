from aiogram import types

from .app import dp
from .keyboards import main_menu
from .messages import ABOUT_MESSAGE


@dp.message_handler(commands=['start', 'help'])
async def start_page(message: types.Message):
    """
    This handler will be called when user sends /start or /help command
    """
    await message.reply('Главное меню:', reply_markup=main_menu)


@dp.callback_query_handler(lambda c: c.data == 'about')
async def show_about_page(callback: types.CallbackQuery):
    """
    This handler will be called when user choose 'О проекте' in main menu.
    Shows info about bot's features.
    """
    await callback.message.answer(
        text=ABOUT_MESSAGE,
        reply_markup=main_menu,
    )
