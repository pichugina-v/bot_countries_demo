import asyncio
import json
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.cache_settings import REDIS as redis
from cache.test.contains import (
    CITY_COORDINATES_KEY,
    CITY_DATA,
    COUNTRY_COORDINATES_KEY,
    COUNTRY_DATA,
)

KEY_CITY = PREFIX_CITY + CITY_COORDINATES_KEY
KEY_COUNTRY = PREFIX_COUNTRY + COUNTRY_COORDINATES_KEY


@pytest.fixture(scope='session')
def event_loop(*_, **__) -> Generator:
    """
    Create event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def _clear_cache_city() -> None:
    """
    The fixture to call to clear the city cache.
    """
    await redis.delete(KEY_CITY)
    await redis.close()


@pytest_asyncio.fixture()
async def _clear_cache_country() -> None:
    """
    The fixture to call to clear the country cache.
    """
    await redis.delete(KEY_COUNTRY)
    await redis.close()


@pytest_asyncio.fixture()
async def _create_cache_country() -> None:
    """
    The fixture creates a cache entry for the country.
    """
    await redis.set(KEY_COUNTRY, json.dumps(dict(COUNTRY_DATA)))
    await redis.close()


@pytest_asyncio.fixture()
async def _create_cache_city() -> None:
    """
    The fixture creates a cache entry for the city.
    """
    await redis.set(KEY_CITY, json.dumps(dict(CITY_DATA)))
    await redis.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def auto_clear_cache_after_test() -> AsyncGenerator[None, None]:
    """
    The fixture clears records in the database after passing all the tests.
    """
    yield
    await redis.delete(KEY_CITY, KEY_COUNTRY)
    await redis.close()
