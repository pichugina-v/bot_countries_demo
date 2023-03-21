from typing import AsyncGenerator

import pytest_asyncio

from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.test.contains import (
    CITY_COORDINATES_KEY,
    CITY_DATA,
    COUNTRY_COORDINATES_KEY,
    COUNTRY_DATA,
)
from cache.test.methods import clear_redis, create_test_data
from services.repositories.api.api_schemas import CitySchema, CountrySchema

KEY_CITY = f'{PREFIX_CITY}{CITY_COORDINATES_KEY}'
KEY_COUNTRY = f'{PREFIX_COUNTRY}{COUNTRY_COORDINATES_KEY.replace(" ", "_")}'


@pytest_asyncio.fixture
async def city_data() -> CitySchema:
    return CitySchema(
        name='Москва',
        country_code='RU',
        longitude=152342.323424,
        latitude=643534.3423423,
        is_capital=True,
    )


@pytest_asyncio.fixture
async def _country_data() -> CountrySchema:
    return CountrySchema(
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


@pytest_asyncio.fixture
async def _clear_cache_city() -> None:
    """
    The fixture to call to clear the city cache.
    """
    await clear_redis(list(KEY_CITY))


@pytest_asyncio.fixture()
async def _clear_cache_country() -> None:
    """
    The fixture to call to clear the country cache.
    """
    await clear_redis(list(KEY_COUNTRY))


@pytest_asyncio.fixture()
async def _create_cache_country() -> None:
    """
    The fixture creates a cache entry for the country.
    """
    await create_test_data(KEY_COUNTRY, COUNTRY_DATA)


@pytest_asyncio.fixture()
async def _create_cache_city() -> None:
    """
    The fixture creates a cache entry for the city.
    """
    await create_test_data(KEY_CITY, CITY_DATA)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def auto_clear_cache_after_test() -> AsyncGenerator[None, None]:
    """
    The fixture clears records in the database after passing all the tests.
    """
    yield
    await clear_redis([KEY_COUNTRY, KEY_CITY])
