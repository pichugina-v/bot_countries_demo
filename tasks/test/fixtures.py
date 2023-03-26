from typing import AsyncGenerator

import pytest_asyncio

from cache.cache_module import Cache
from services.repositories.api.api_schemas import CountrySchema
from tasks.tasks import update_currency_cache

GOOD_RECORD_KEY = '123.123'
ONE_BAD_VALUE_KEY = '123.124'
ALL_BAD_VALUE_KEY = '123.125'
ONLY_ONE_GOOD_KEY = '123.126'
ONLY_ONE_BAD_KEY = '123.127'
BAD_RESULT = 'this is a random string'


@pytest_asyncio.fixture(scope='session', autouse=False)
async def schema_country() -> CountrySchema:
    """
    Fixture returns schema for test data.
    """
    return CountrySchema(
        iso_code='RU',
        name='Россия',
        capital='Москва',
        capital_longitude=152342.323424,
        capital_latitude=643534.3423423,
        area_size=4545.1111,
        population=145000000,
        currencies=dict(keys_1=BAD_RESULT, keys_2=BAD_RESULT),
        languages=['русский', 'английский'],
    )


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_data(schema_country):
    """
    Fixture creates test records.
    """
    two_good_value = schema_country.copy(update=dict(currencies=dict(BYN=BAD_RESULT, TMT=BAD_RESULT)))
    await Cache.create_or_update_country(GOOD_RECORD_KEY, two_good_value)
    one_bad_value = schema_country.copy(update=dict(currencies=dict(BYN=BAD_RESULT, QQQ=BAD_RESULT)))
    await Cache.create_or_update_country(ONE_BAD_VALUE_KEY, one_bad_value)
    two_bad_value = schema_country.copy(update=dict(currencies=dict(NNN=BAD_RESULT, QQQ=BAD_RESULT)))
    await Cache.create_or_update_country(ALL_BAD_VALUE_KEY, two_bad_value)
    only_one_good_value = schema_country.copy(update=dict(currencies=dict(BYN=BAD_RESULT)))
    await Cache.create_or_update_country(ONLY_ONE_GOOD_KEY, only_one_good_value)
    only_one_bad_value = schema_country.copy(update=dict(currencies=dict(QQQ=BAD_RESULT)))
    await Cache.create_or_update_country(ONLY_ONE_BAD_KEY, only_one_bad_value)
    yield


@pytest_asyncio.fixture(scope='session', autouse=True)
async def update_currency_test_data() -> AsyncGenerator[None, None]:
    """
    The fixture starts updating the exchange rate in test records.
    """
    await update_currency_cache()
    yield
