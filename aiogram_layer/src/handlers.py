from aiogram import types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from aiogram_layer.src.app import dp
from aiogram_layer.src.callbacks import Callbacks as cb
from aiogram_layer.src.keyboards import (
    country_detail,
    currency_detail,
    main_menu,
    to_main_menu,
    weather_detail,
)
from aiogram_layer.src.messages import (
    ABOUT_MESSAGE,
    CITY_INFO,
    COUNTRY_INFO,
    COUNTRY_NOT_FOUND,
    CURRENCY_RATE_DETAIL,
    ENTER_CITY,
    ENTER_COUNTRY,
    INVALID_CITY,
    INVALID_COUNTRY,
    RESTART_MESSAGE,
    START_MESSAGE,
    WEATHER_DETAIL,
    WEATHER_DETAIL_COUNTRY,
)
from aiogram_layer.src.states import CountryCityForm, Form
from aiogram_layer.src.validators import is_city_name_valid, is_country_name_valid
from services.country_service import CountryService


@dp.message(Command('start', 'help'))
async def start_page(message: types.Message):
    """
    This handler will be called when user sends /start or /help command

    :param message: message
    :type message: types.Message

    :return: None
    """
    await message.reply(
        text=START_MESSAGE,
        reply_markup=main_menu
    )


@dp.callback_query(Text(cb.about.value))
async def show_about_page(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'О проекте' in main menu.
    Shows info about bot's features.

    :param callback: callback function
    :type callback: types.CallbackQuery

    :return: None
    """
    await callback.message.answer(
        text=ABOUT_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query(Text(cb.city.value))
async def enter_city_name(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Поиск по городу' in main menu.

    :param callback: callback function
    :type callback: types.CallbackQuery

    :return: None
    """
    await state.set_state(Form.city_search)
    await callback.message.reply(
        text=ENTER_CITY
    )


@dp.message(lambda message: not is_city_name_valid(message.text), Form.city_search)
async def process_city_name_invalid(message: types.Message):
    """
    This handler will be called when user input invalid city name.

    :param message: message

    :return: None
    """
    await message.reply(
        text=INVALID_CITY,
        reply_markup=to_main_menu
    )


@dp.message(Form.city_search)
async def process_city_name(message: types.Message):
    """
    This handler will be called when user inputs city name.
    Continues the dialogue about the country where the city is located.

    :param message: message
    :type: types.Message

    :return: None
    """
    await message.reply(
        text=CITY_INFO.format(city=message.text),
        reply_markup=country_detail
    )


@dp.callback_query(
    Text(cb.weather.value),
    CountryCityForm()
)
async def get_weather(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Погода' button.
    Continues the dialog about weather details.

    :param callback: callback function
    :type callback: types.CallbackQuery
    :param state: state
    :type state: FSMContext

    :return: None
    """
    detail_text = WEATHER_DETAIL
    if (await state.get_state()) == 'CountryCityForm:country_search':
        data = await state.get_data()
        weather = await CountryService().get_capital_weather(data['country_info'])
        detail_text = WEATHER_DETAIL_COUNTRY.format(
            curr=weather.current_weather_temp,
            feels=weather.current_weather_temp_feels_like
        )
    await callback.message.reply(
        text=detail_text,
        reply_markup=weather_detail
    )


@dp.callback_query(
    Text(cb.country_info.value),
    CountryCityForm()
)
async def get_country_info(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Подробнее о стране' button.
    Continues the dialog about country details.

    :param callback: callback function
    :type callback: types.CallbackQuery

    :return: None
    """
    data = await state.get_data()
    await callback.message.reply(
        text=COUNTRY_INFO.format(
            country=data['country_detail'],
            languages=', '.join(str(language) for language in data['languages']),
            currencies=', '.join(str(currency.name) for currency in data['currencies'])
        ),
        reply_markup=country_detail
    )


@dp.callback_query(
    Text(cb.currency_rate.value),
    CountryCityForm()
)
async def get_currency_rate(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Курс валюты' button.
    Continues the dialog about currency rate.

    :param callback: callback function
    :type callback: types.CallbackQuery

    :return: None
    """
    currency_details = ''
    data = await state.get_data()
    for currency in data['currencies']:
        currency_details += ' ' + str(currency.name) + '-' + str(currency.value)
    await callback.message.reply(
        text=CURRENCY_RATE_DETAIL.format(currency_details=currency_details),
        reply_markup=currency_detail
    )


@dp.callback_query(
    Text(cb.to_main_menu.value)
)
async def return_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'К началу' button.
    Resets all states, restarts dialog.

    :param callback: callback function
    :type callback: types.CallbackQuery
    :param state: state
    :type state: FSMContext

    :return: None
    """
    await state.clear()
    await callback.message.reply(
        text=RESTART_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query(Text(cb.country.value))
async def enter_country_name(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Поиск по стране'.

    :param callback: arg1

    :return: None
    """
    await state.set_state(Form.country_search)
    await callback.message.reply(
        text=ENTER_COUNTRY
    )


@dp.message(lambda message: not is_country_name_valid(message.text), Form.country_search)
async def process_country_name_invalid(message: types.Message):
    """
    This handler will be called when user input invalid country name.

    :param message: message

    :return: None
    """
    await message.reply(
        text=INVALID_COUNTRY,
        reply_markup=to_main_menu
    )


@dp.message(Form.country_search)
async def process_country_name(message: types.Message, state: FSMContext):
    """
    This handler will be called when user inputs country name.

    :param message: arg1

    :return: None
    """
    info = await CountryService().get_country_info(message.text)
    if not info:
        return await message.answer(
            text=COUNTRY_NOT_FOUND,
            reply_markup=to_main_menu
        )
    detail = await CountryService().get_country(info)
    languages = await CountryService().get_languages(info)
    currencies = await CountryService().get_currencies(info)
    await message.answer(
        text=COUNTRY_INFO.format(
            country=detail,
            languages=', '.join(str(language) for language in languages.languages),
            currencies=', '.join(str(currency.name) for currency in currencies)
        ),
        reply_markup=country_detail
    )
    await state.update_data(
        country_info=info,
        country_detail=detail,
        languages=languages.languages,
        currencies=currencies
    )
