import asyncio
from typing import Generator

import pytest
import pytest_asyncio

from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.cache_settings import REDIS as redis
from cache.test.contains import CITY_COORDINATES_KEY, COUNTRY_COORDINATES_KEY

key_city = PREFIX_CITY + CITY_COORDINATES_KEY
key_country = PREFIX_COUNTRY + COUNTRY_COORDINATES_KEY


@pytest.yield_fixture(scope='session')
def event_loop(*args, **kwargs) -> Generator:
    """
    Create event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def _clear_city() -> None:
    """
    Removes the cache entry for the city.
    """
    await redis.delete(key_city)
    await redis.close()


@pytest_asyncio.fixture()
async def _clear_country() -> None:
    """
    Removes the cache entry for the country.
    """
    await redis.delete(key_country)
    await redis.close()
