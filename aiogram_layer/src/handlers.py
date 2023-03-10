from aiogram import types
from aiogram.dispatcher import FSMContext

from .app import dp
from .keyboards import (
    all_info,
    country_detail,
    currency_detail,
    main_menu,
    weather_detail,
)
from .messages import ABOUT_MESSAGE
from .states import CountryCityForm, Form


@dp.message_handler(commands='start')
async def start_page(message: types.Message):
    """
    This handler will be called when user sends /start or /help command
    """
    await message.reply(
        text='Привет! Выберите, что Вас интересует:',
        reply_markup=main_menu
    )


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


@dp.callback_query_handler(lambda call: call.data == 'city')
async def enter_city_name(callback: types.CallbackQuery):
    """
    This handler will be called when user clicks 'Поиск по городу' button
    """
    await Form.city_search.set()
    await callback.message.reply(
        text='Введите название городa'
    )


@dp.message_handler(state=Form.city_search)
async def process_city_name(message: types.Message):
    """
    This handler will be called when user enters city name
    """
    await message.reply(
        text=f'Информация о городе {message.text}',
        reply_markup=all_info
    )


@dp.callback_query_handler(
    lambda call: call.data == 'weather',
    state=CountryCityForm  # Было: state=Form.city_search
)
async def get_weather(callback: types.CallbackQuery):
    """
    This handler will be called when user clicks "Погода" button
    """
    await callback.message.reply(
        text='Погода',  # Было: text='Погода в выбранном городе'
        reply_markup=weather_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'country_info',
    state=CountryCityForm  # Было: state=Form.city_search
)
async def get_country_info(callback: types.CallbackQuery):
    """
    This handler will be called when user clicks "Подробнее о стране" button
    """
    await callback.message.reply(
        text='Подробнее о стране: ',
        reply_markup=country_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'currency_rate',
    state=CountryCityForm  # Было: state=Form.city_search
)
async def get_currency_rate(callback: types.CallbackQuery):
    """
    This handler will be called when user clicks "Курс валюты" button
    """
    await callback.message.reply(
        text='Подробнее о курсе валюты',
        reply_markup=currency_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'to_main_menu',
    state='*'
)
async def return_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user clicks "К началу" button
    Resets all states, restarts dialog
    """
    await state.reset_state(with_data=True)
    await callback.message.reply(
        text='Выберите, что Вас интересует:',
        reply_markup=main_menu,
    )


@dp.callback_query_handler(lambda call: call.data == 'country')
async def enter_country_name(callback: types.CallbackQuery):
    """
    This handler will be called when user clicks "Подробнее о стране" button
    """
    await Form.country_search.set()
    await callback.message.reply(
        text='Введите название страны'
    )


@dp.message_handler(state=Form.country_search)
async def process_country_name(message: types.Message):
    await message.reply(
        text=f'Информация о стране {message.text}',
        reply_markup=country_detail
    )
