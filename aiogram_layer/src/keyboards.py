from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BUTTONS = {
    'COUNTRY_SEARCH': InlineKeyboardButton(
        'Поиск по стране', callback_data='country'
    ),
    'CITY_SEARCH': InlineKeyboardButton(
        'Поиск по городу', callback_data='city'
    ),
    'ABOUT': InlineKeyboardButton(
        'О проекте', callback_data='about'
    ),
    'TO_MAIN_MENU': InlineKeyboardButton(
        'К началу', callback_data='to_main_menu'
    ),
    'WEATHER': InlineKeyboardButton(
        'Погода', callback_data='weather'
    ),
    'COUNTRY': InlineKeyboardButton(
        'Подробнее о стране', callback_data='country_info'
    ),
    'CURRENCY': InlineKeyboardButton(
        'Курс валюты', callback_data='currency_rate'
    )
}

MAIN_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [BUTTONS['COUNTRY_SEARCH']],
        [BUTTONS['CITY_SEARCH']],
        [BUTTONS['ABOUT']]
    ]
)
ALL_INFO = InlineKeyboardMarkup(
    inline_keyboard=[
        [BUTTONS['WEATHER']],
        [BUTTONS['COUNTRY']],
        [BUTTONS['CURRENCY']],
        [BUTTONS['TO_MAIN_MENU']]
    ]
)
WEATHER_DETAIL = InlineKeyboardMarkup(
    inline_keyboard=[
        [BUTTONS['COUNTRY']],
        [BUTTONS['CURRENCY']],
        [BUTTONS['TO_MAIN_MENU']]
    ]
)
COUNTRY_DETAIL = InlineKeyboardMarkup(
    inline_keyboard=[
        [BUTTONS['WEATHER']],
        [BUTTONS['CURRENCY']],
        [BUTTONS['TO_MAIN_MENU']]
    ]
)
CURRENCY_RATE_DETAIL = InlineKeyboardMarkup(
    inline_keyboard=[
        [BUTTONS['WEATHER']],
        [BUTTONS['COUNTRY']],
        [BUTTONS['TO_MAIN_MENU']]
    ]
)
