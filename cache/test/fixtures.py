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

KEY_CITY = f'{PREFIX_CITY}{CITY_COORDINATES_KEY}'
KEY_COUNTRY = f'{PREFIX_COUNTRY}{COUNTRY_COORDINATES_KEY.replace(" ", "_")}'


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
