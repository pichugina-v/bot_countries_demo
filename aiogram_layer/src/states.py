from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    """
    The Form for saving dialog states in the storage
    """
    country_search = State()
    city_search = State()
