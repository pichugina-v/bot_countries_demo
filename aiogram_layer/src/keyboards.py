from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

COUNTRY_SEARCH = InlineKeyboardButton(
    'Поиск по стране', callback_data='country')
CITY_SEARCH = InlineKeyboardButton('Поиск по городу', callback_data='city')
ABOUT = InlineKeyboardButton('О проекте', callback_data='about')
TO_MAIN_MENU = InlineKeyboardButton('К началу', callback_data='to_main_menu')


WEATHER = InlineKeyboardButton('Погода', callback_data='weather')
COUNTRY = InlineKeyboardButton(
    'Подробнее о стране', callback_data='country_info')
CURRENCY = InlineKeyboardButton('Курс валюты', callback_data='currency_rate')


MAIN_MENU = InlineKeyboardMarkup().add(COUNTRY_SEARCH).add(CITY_SEARCH).add(ABOUT)
ALL_INFO = InlineKeyboardMarkup().add(WEATHER).add(COUNTRY).add(CURRENCY).add(TO_MAIN_MENU)
WEATHER_DETAIL = InlineKeyboardMarkup().add(COUNTRY).add(CURRENCY).add(TO_MAIN_MENU)
COUNTRY_DETAIL = InlineKeyboardMarkup().add(WEATHER).add(CURRENCY).add(TO_MAIN_MENU)
CURRENCY_RATE_DETAIL = InlineKeyboardMarkup().add(WEATHER).add(COUNTRY).add(TO_MAIN_MENU)
