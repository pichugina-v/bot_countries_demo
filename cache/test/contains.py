from services.repositories.api.api_schemas import CitySchema, CountrySchema

CITY_DATA = CitySchema(
    name='Москва',
    country_code='RU',
    longitude=152342.323424,
    latitude=643534.3423423,
    is_capital=True,
)
COUNTRY_DATA = CountrySchema(
    iso_code='RU',
    name='Россия',
    capital='Москва',
    capital_longitude=152342.323424,
    capital_latitude=643534.3423423,
    area_size=4545.1111,
    population=145000000,
    currencies=dict(key_1='value_1', key_2='value_2'),
    languages=['русский', 'английский'],
)
CITY_COORDINATES_KEY = str(CITY_DATA.longitude) + ' ' + str(CITY_DATA.latitude)
COUNTRY_COORDINATES_KEY = (
    str(COUNTRY_DATA.capital_longitude) + ' ' + str(COUNTRY_DATA.capital_latitude)
)
