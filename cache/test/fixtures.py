import pytest_asyncio

from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.test.methods import clear_redis, create_test_data
from services.repositories.api.api_schemas import CitySchema, CountrySchema


COUNTRY_COORDINATES_KEY = '1234123 6623621'
COUNTRY_NAME = 'Россия'
LONG = 152342.323424
LAT = 643534.3423423
CITY_COORDINATES_KEY = f'{LONG}_{LAT}'
KEY_CITY = f'{PREFIX_CITY}{CITY_COORDINATES_KEY}'
KEY_COUNTRY = f'{PREFIX_COUNTRY}{COUNTRY_COORDINATES_KEY.replace(" ", "_")}'


@pytest_asyncio.fixture(autouse=False)
async def city_data() -> CitySchema:
    """
    Fixture returns schema for test data.
    """
    return CitySchema(
        name='Москва',
        country_code='RU',
        longitude=LONG,
        latitude=LAT,
        is_capital=True,
    )


@pytest_asyncio.fixture(autouse=False)
async def country_data() -> CountrySchema:
    """
    Fixture returns schema for test data.
    """
    return CountrySchema(
        iso_code='RU',
        name='Россия',
        capital='Москва',
        capital_longitude=LONG,
        capital_latitude=LAT,
        area_size=4545.1111,
        population=145000000,
        currencies=dict(key_1='value_1', key_2='value_2'),
        languages=['русский', 'английский'],
    )


@pytest_asyncio.fixture(autouse=False)
async def _clear_cache_city() -> None:
    """
    The fixture to call to clear the city cache.
    """
    await clear_redis([KEY_CITY])


@pytest_asyncio.fixture(autouse=False)
async def _clear_cache_country() -> None:
    """
    The fixture to call to clear the country cache.
    """
    await clear_redis(list(KEY_COUNTRY))


@pytest_asyncio.fixture(autouse=False)
async def _create_cache_country(country_data: pytest_asyncio.fixture) -> None:
    """
    The fixture creates a cache entry for the country.
    """
    await create_test_data(KEY_COUNTRY, country_data)


@pytest_asyncio.fixture(autouse=False)
async def _create_cache_city(city_data: pytest_asyncio.fixture) -> None:
    """
    The fixture creates a cache entry for the city.
    """
    await create_test_data(KEY_CITY, city_data)
