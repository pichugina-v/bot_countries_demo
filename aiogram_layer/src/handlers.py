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
from .messages import (
    ABOUT_MESSAGE,
    COUNTRY_DETAIL,
    COUNTRY_INFO,
    COUNTRY_INFO_NAME,
    CURRENCY_RATE_DETAIL,
    ENTER_CITY,
    ENTER_COUNTRY,
    RESTART_MESSAGE,
    START_MESSAGE,
    WEATHER_DETAIL,
    WEATHER_DETAIL_COUNTRY,
)
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
    state=CountryCityForm
)
async def get_weather(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Погода' button.
    Continues the dialog about weather details.
    """
    detail_text = WEATHER_DETAIL
    if (await state.get_state()) == 'CountryCityForm:country_search':
        detail_text = WEATHER_DETAIL_COUNTRY
    await callback.message.reply(
        text=detail_text,
        reply_markup=weather_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == 'country_info',
    state=CountryCityForm
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
    state=CountryCityForm
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
    """This handler will be called when user chooses 'Поиск по стране'.

    :param callback: arg1
    :type callback: types.CallbackQuery

    :return: None
    """
    await Form.country_search.set()
    await callback.message.reply(
        text=ENTER_COUNTRY
    )


@dp.message_handler(state=Form.country_search)
async def process_country_name(message: types.Message):
    """This handler will be called when user inputs country name.

    :param message: arg1
    :type message: types.Message

    :return: None
    """
    await message.reply(
        text=COUNTRY_INFO_NAME.format(country=message.text),
        reply_markup=country_detail
    )
