# from typing import AsyncGenerator

# import pytest_asyncio

# from cache.cache_module import Cache
# from cache.test.methods import clear_redis
# from services.repositories.api.api_schemas import CountrySchema
# from tasks.tasks import update_currency_cache

# GOOD_RECORD_KEY = '123.123'
# ONE_BAD_VALUE_KEY = '123.124'
# ALL_BAD_VALUE_KEY = '123.125'
# ONLY_ONE_GOOD_KEY = '123.126'
# ONLY_ONE_BAD_KEY = '123.127'
# BAD_RESULT = 'this is a random string'


# @pytest_asyncio.fixture()
# async def schema_country():
#     return CountrySchema(
#         iso_code='RU',
#         name='Россия',
#         capital='Москва',
#         capital_longitude=152342.323424,
#         capital_latitude=643534.3423423,
#         area_size=4545.1111,
#         population=145000000,
#         currencies=dict(keys_1=BAD_RESULT, keys_2=BAD_RESULT),
#         languages=['русский', 'английский'],
#     )


# @pytest_asyncio.fixture(autouse=True)
# async def _create_two_good_record(schema_country: pytest_asyncio.fixture) -> None:
#     two_good_value = schema_country.copy(update=dict(currencies=dict(BYN=BAD_RESULT, TMT=BAD_RESULT)))
#     await Cache.create_or_update_country(GOOD_RECORD_KEY, two_good_value)


# @pytest_asyncio.fixture(autouse=True)
# async def _create_one_bad_value(schema_country: pytest_asyncio.fixture) -> None:
#     one_bad_value = schema_country.copy(update=dict(currencies=dict(BYN=BAD_RESULT, QQQ=BAD_RESULT)))
#     await Cache.create_or_update_country(ONE_BAD_VALUE_KEY, one_bad_value)


# @pytest_asyncio.fixture(autouse=True)
# async def _create_two_bad_value(schema_country: pytest_asyncio.fixture) -> None:
#     two_bad_value = schema_country.copy(update=dict(currencies=dict(NNN=BAD_RESULT, QQQ=BAD_RESULT)))
#     await Cache.create_or_update_country(ALL_BAD_VALUE_KEY, two_bad_value)


# @pytest_asyncio.fixture(autouse=True)
# async def _create_only_one_good_value(schema_country: pytest_asyncio.fixture) -> None:
#     only_one_good_value = schema_country.copy(update=dict(currencies=dict(BYN=BAD_RESULT)))
#     await Cache.create_or_update_country(ONLY_ONE_GOOD_KEY, only_one_good_value)


# @pytest_asyncio.fixture(autouse=True)
# async def _create_only_one_bad_value(schema_country: pytest_asyncio.fixture) -> None:
#     only_one_bad_value = schema_country.copy(update=dict(currencies=dict(QQQ=BAD_RESULT)))
#     await Cache.create_or_update_country(ONLY_ONE_BAD_KEY, only_one_bad_value)

# # @pytest_asyncio.fixture(autouse=False)
# # async def _start_update() -> None:


# @pytest_asyncio.fixture(autouse=True)
# async def prepare_and_clear_data() -> AsyncGenerator:
#     await update_currency_cache()
#     yield
#     data = [GOOD_RECORD_KEY, ONE_BAD_VALUE_KEY, ALL_BAD_VALUE_KEY,
#             ONLY_ONE_GOOD_KEY, ONLY_ONE_BAD_KEY]
#     for indx in range(len(data)):
#         data[indx] = f'country_{data[indx]}'
#     await clear_redis(data)

# # @pytest_asyncio.fixture(scope='package', autouse=False)
# # async def auto_clear_cache_after_test() -> AsyncGenerator[None, None]:
# #    """
# #    The fixture clears records in the database after passing all the tests.
# #    """

# #    yield
# #    data = [GOOD_RECORD_KEY, ONE_BAD_VALUE_KEY, ALL_BAD_VALUE_KEY,
# #            ONLY_ONE_GOOD_KEY, ONLY_ONE_BAD_KEY]
# #    for indx in range(len(data)):
# #        data[indx] = f'country_{data[indx]}'
# #    await clear_redis(data)
