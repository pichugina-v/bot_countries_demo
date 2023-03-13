from enum import Enum

from aiogram.types import InlineKeyboardButton

from aiogram_layer.src.callbacks import Callbacks as cb


class Buttons(Enum):
    country_search = InlineKeyboardButton('Поиск по стране', callback_data=cb.country.value)
    city_search = InlineKeyboardButton('Поиск по городу', callback_data=cb.city.value)
    about = InlineKeyboardButton('О проекте', callback_data=cb.about.value)
    to_main_menu = InlineKeyboardButton('К началу', callback_data=cb.to_main_menu.value)
    weather = InlineKeyboardButton('Погода', callback_data=cb.weather.value)
    country = InlineKeyboardButton('Подробнее о стране', callback_data=cb.country_info.value)
    currency = InlineKeyboardButton('Курс валюты', callback_data=cb.currency_rate.value)
