import asyncio
import os
import platform
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from cache.test.fixtures import KEY_CITY, KEY_COUNTRY, COUNTRY_NAME
from cache.test.methods import clear_redis
from tasks.test.fixtures import (
    ALL_BAD_VALUE_KEY,
    GOOD_RECORD_KEY,
    ONE_BAD_VALUE_KEY,
    ONLY_ONE_BAD_KEY,
    ONLY_ONE_GOOD_KEY,
)
from tasks.test.methods import add_prefix

pytest_plugins = [
    'services.repositories.api.tests.fixture',
    'services.repositories.db.tests.fixture',
    'aiogram_layer.src.tests.fixtures',
    'cache.test.fixtures',
    'tasks.test.fixtures',
]

os.environ['WEATHER_API_KEY'] = 'fake_api_key'


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """
        Create event loop for testing
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope='session', autouse=True)
async def deleting_test_records() -> AsyncGenerator[None, None]:
    """
    Fixture removes test entries before and after tests.
    """
    keys_without_prefix = [GOOD_RECORD_KEY, ONE_BAD_VALUE_KEY, ALL_BAD_VALUE_KEY,
                           ONLY_ONE_GOOD_KEY, ONLY_ONE_BAD_KEY, COUNTRY_NAME]
    key_with_prefix = (add_prefix(keys_without_prefix)) + [KEY_CITY, KEY_COUNTRY]
    await clear_redis(key_with_prefix)
    yield
    await clear_redis(key_with_prefix)