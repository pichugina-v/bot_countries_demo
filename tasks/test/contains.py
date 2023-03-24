from services.repositories.api.api_schemas import CountrySchema

GOOD_RECORD_KEY = '123.123'
ONE_BAD_VALUE_KEY = '123.124'
ALL_BAD_VALUE_KEY = '123.125'
ONLY_ONE_GOOD_KEY = '123.126'
ONLY_ONE_BAD_KEY = '123.127'

SCHEMA_COUNTRY = CountrySchema(
    iso_code='RU',
    name='Россия',
    capital='Москва',
    capital_longitude=152342.323424,
    capital_latitude=643534.3423423,
    area_size=4545.1111,
    population=145000000,
    currencies=dict(keys_1='XXXXXXXXXX', keys_2='XXXXXXXXXX'),
    languages=['русский', 'английский'],
)
