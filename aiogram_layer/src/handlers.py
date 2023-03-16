from aiogram import types
from aiogram.dispatcher import FSMContext

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
    COUNTRY_INFO,
    COUNTRY_INFO_NAME,
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
from aiogram_layer.src.validators import is_user_input_valid
from services.country_service import CountryService


@dp.message_handler(commands=['start', 'help'])
async def start_page(message: types.Message):
    """
    This handler will be called when user sends /start or /help command

    :param message: message

    :return: None
    """
    await message.reply(
        text=START_MESSAGE,
        reply_markup=main_menu
    )


@dp.callback_query_handler(lambda c: c.data == cb.about.value)
async def show_about_page(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'О проекте' in main menu.
    Shows info about bot's features.

    :param callback: callback function

    :return: None
    """
    await callback.message.answer(
        text=ABOUT_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query_handler(lambda call: call.data == cb.city.value)
async def enter_city_name(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Поиск по городу' in main menu.

    :param callback: callback function

    :return: None
    """
    await Form.city_search.set()
    await callback.message.reply(
        text=ENTER_CITY
    )


@dp.message_handler(lambda message: not is_user_input_valid(message.text), state=Form.city_search)
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


@dp.message_handler(state=Form.city_search)
async def process_city_name(message: types.Message):
    """
    This handler will be called when user inputs city name.
    Continues the dialogue about the country where the city is located.

    :param message: message

    :return: None
    """
    await message.reply(
        text=COUNTRY_INFO.format(city=message.text),
        reply_markup=country_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == cb.weather.value,
    state=CountryCityForm
)
async def get_weather(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Погода' button.
    Continues the dialog about weather details.

    :param callback: callback function
    :param state: state

    :return: None
    """
    detail_text = WEATHER_DETAIL
    if (await state.get_state()) == 'CountryCityForm:country_search':
        async with state.proxy() as data:
            weather = await CountryService().get_capital_weather(
                data['capital_latitude'],
                data['capital_longitude']
            )
            capital = data['capital']
        detail_text = WEATHER_DETAIL_COUNTRY.format(
            capital=capital,
            current_temp=weather.current_weather_temp,
            feels_like_temp=weather.current_weather_temp_feels_like
        )
    await callback.message.reply(
        text=detail_text,
        reply_markup=weather_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == cb.country_info.value,
    state=CountryCityForm
)
async def get_country_info(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Подробнее о стране' button.
    Continues the dialog about country details.

    :param callback: callback function

    :return: None
    """
    await callback.message.reply(
        text=COUNTRY_INFO_NAME,
        reply_markup=country_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == cb.currency_rate.value,
    state=CountryCityForm
)
async def get_currency_rate(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Курс валюты' button.
    Continues the dialog about currency rate.

    :param callback: callback function

    :return: None
    """
    currency_details = ''
    async with state.proxy() as data:
        for currency in data['currencies']:
            currency_details += ' ' + str(currency.name) + '-' + str(currency.value)
            print(currency_details)
    await callback.message.reply(
        text=CURRENCY_RATE_DETAIL.format(currency_details=currency_details),
        reply_markup=currency_detail
    )


@dp.callback_query_handler(
    lambda call: call.data == cb.to_main_menu.value,
    state='*'
)
async def return_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'К началу' button.
    Resets all states, restarts dialog.

    :param callback: callback function
    :param state: state

    :return: None
    """
    await state.reset_state(with_data=True)
    await callback.message.reply(
        text=RESTART_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query_handler(lambda call: call.data == cb.country.value)
async def enter_country_name(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'Поиск по стране'.

    :param callback: arg1

    :return: None
    """
    await Form.country_search.set()
    await callback.message.reply(
        text=ENTER_COUNTRY
    )


@dp.message_handler(lambda message: not is_user_input_valid(message.text), state=Form.country_search)
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


@dp.message_handler(state=Form.country_search)
async def process_country_name(message: types.Message, state: FSMContext):
    """
    This handler will be called when user inputs country name.

    :param message: arg1

    :return: None
    """
    country_info = await CountryService().get_country(message.text)
    capital_info = await CountryService().get_capital_info(message.text)
    currencies = await CountryService().get_currency(message.text)
    languages = await CountryService().get_languages(message.text)
    async with state.proxy() as data:
        data['capital'] = capital_info[2]
        data['capital_longitude'] = capital_info[0]
        data['capital_latitude'] = capital_info[1]
        data['currencies'] = currencies
    await message.reply(
        text=COUNTRY_INFO_NAME.format(
            name=country_info.name,
            area_size=country_info.area_size,
            population=country_info.population,
            languages=', '.join(str(language) for language in languages.languages),
            currencies=', '.join(str(currency.name) for currency in currencies)
        ),
        reply_markup=country_detail
    )
