from aiogram.dispatcher.filters.state import State, StatesGroup


class CountryCityForm(StatesGroup):
    country_search = State()
    city_search = State()


class Form(CountryCityForm):
    """
    The Form for saving dialog states in the storage
    """
    pass
