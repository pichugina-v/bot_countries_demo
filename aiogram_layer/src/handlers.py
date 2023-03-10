from aiogram import types
from aiogram.dispatcher import FSMContext

from .app import dp
from .messages import (
    ABOUT_MESSAGE,
    ENTER_CITY,
    COUNTRY_INFO,
    START_MESSAGE,
    RESTART_MESSAGE,
    WEATHER_DETAIL,
    COUNTRY_DETAIL,
    CURRENCY_RATE_DETAIL,
)
from .keyboards import (
    all_info,
    country_detail,
    currency_detail,
    main_menu,
    weather_detail,
)
from .messages import ABOUT_MESSAGE
from .states import CountryCityForm, Form


@dp.message_handler(commands=['start', 'help'])
async def start_page(message: types.Message):
    """
    This handler will be called when user sends /start or /help command
    """
    await message.reply(
        text=START_MESSAGE,
        reply_markup=main_menu
    )


@dp.callback_query_handler(lambda c: c.data == 'about')
async def show_about_page(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'О проекте' in main menu.
    Shows info about bot's features.
    """
    await callback.message.answer(
        text=ABOUT_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query_handler(lambda call: call.data == 'city')
async def enter_city_name(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Поиск по городу' in main menu.
    """
    await Form.city_search.set()
    await callback.message.reply(
        text=ENTER_CITY
    )


@dp.message_handler(state=Form.city_search)
async def process_city_name(message: types.Message):
    """
    This handler will be called when user inputs city name.
    Continues the dialogue about the country where the city is located.
    """
    await message.reply(
        text=COUNTRY_INFO.format(city=message.text),
        reply_markup=all_info
    )


@dp.callback_query_handler(
    lambda call: call.data == 'weather',
    state=CountryCityForm  # Было: state=Form.city_search
)
async def get_weather(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Погода' button.
    Continues the dialog about weather details.
    """
    await callback.message.reply(
        text=WEATHER_DETAIL,
        reply_markup=weather_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'country_info',
    state=CountryCityForm  # Было: state=Form.city_search
)
async def get_country_info(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Подробнее о стране' button.
    Continues the dialog about country details.
    """
    await callback.message.reply(
        text=COUNTRY_DETAIL,
        reply_markup=country_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'currency_rate',
    state=CountryCityForm  # Было: state=Form.city_search
)
async def get_currency_rate(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Курс валюты' button.
    Continues the dialog about currency rate.
    """
    await callback.message.reply(
        text=CURRENCY_RATE_DETAIL,
        reply_markup=currency_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'to_main_menu',
    state='*'
)
async def return_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'К началу' button.
    Resets all states, restarts dialog
    """
    await state.reset_state(with_data=True)
    await callback.message.reply(
        text=RESTART_MESSAGE,
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
