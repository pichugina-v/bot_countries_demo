from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = {
    'country_search': InlineKeyboardButton(
        'Поиск по стране', callback_data='country'
    ),
    'city_search': InlineKeyboardButton(
        'Поиск по городу', callback_data='city'
    ),
    'about': InlineKeyboardButton(
        'О проекте', callback_data='about'
    ),
    'to_main_menu': InlineKeyboardButton(
        'К началу', callback_data='to_main_menu'
    ),
    'weather': InlineKeyboardButton(
        'Погода', callback_data='weather'
    ),
    'country': InlineKeyboardButton(
        'Подробнее о стране', callback_data='country_info'
    ),
    'currency': InlineKeyboardButton(
        'Курс валюты', callback_data='currency_rate'
    )
}

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons['country_search']],
        [buttons['city_search']],
        [buttons['about']]
    ]
)
all_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons['weather']],
        [buttons['country']],
        [buttons['currency']],
        [buttons['to_main_menu']]
    ]
)
weather_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons['country']],
        [buttons['currency']],
        [buttons['to_main_menu']]
    ]
)
country_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons['weather']],
        [buttons['currency']],
        [buttons['to_main_menu']]
    ]
)
currency_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons['weather']],
        [buttons['country']],
        [buttons['to_main_menu']]
    ]
)
