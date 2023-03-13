from aiogram.types import InlineKeyboardMarkup

from aiogram_layer.src.buttons import Buttons

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.country_search.value],
        [Buttons.city_search.value],
        [Buttons.about.value],
    ]
)
all_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.weather.value],
        [Buttons.country.value],
        [Buttons.currency.value],
        [Buttons.to_main_menu.value],
    ]
)
weather_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.country.value],
        [Buttons.currency.value],
        [Buttons.to_main_menu.value],
    ]
)
country_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.weather.value],
        [Buttons.currency.value],
        [Buttons.to_main_menu.value],
    ]
)
currency_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.weather.value],
        [Buttons.country.value],
        [Buttons.to_main_menu.value],
    ]
)
