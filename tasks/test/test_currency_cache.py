import pytest

from cache.cache_module import Cache
from tasks.test.fixtures import (
    ALL_BAD_VALUE_KEY,
    BAD_RESULT,
    GOOD_RECORD_KEY,
    ONE_BAD_VALUE_KEY,
    ONLY_ONE_BAD_KEY,
    ONLY_ONE_GOOD_KEY,
)


class TestCurrency:
    @pytest.mark.asyncio
    async def test_two_good_key(self):  # , _create_two_good_record):
        currencies = getattr(await Cache.get_country(GOOD_RECORD_KEY), 'currencies', {})
        assert True is currencies.get('BYN', BAD_RESULT).replace('.', '').isdigit()
        assert True is currencies.get('TMT', BAD_RESULT).replace('.', '').isdigit()

    @pytest.mark.asyncio
    async def test_one_bad_key(self):  # , _create_one_bad_value):
        currencies = getattr(await Cache.get_country(ONE_BAD_VALUE_KEY), 'currencies', {})
        assert True is currencies.get('BYN', BAD_RESULT).replace('.', '').isdigit()
        assert BAD_RESULT == currencies.get('QQQ')

    @pytest.mark.asyncio
    async def test_two_bad_key(self):  # , _create_two_bad_value):
        currencies = getattr(await Cache.get_country(ALL_BAD_VALUE_KEY), 'currencies', {})
        assert BAD_RESULT == currencies.get('QQQ')
        assert BAD_RESULT == currencies.get('NNN')

    @pytest.mark.asyncio
    async def test_only_one_bad_key(self):  # , _create_only_one_bad_value):
        currencies = getattr(await Cache.get_country(ONLY_ONE_BAD_KEY), 'currencies', {})
        assert BAD_RESULT == currencies.get('QQQ')

    @pytest.mark.asyncio
    async def test_only_one_good_key(self):  # , _create_only_one_good_value):
        currencies = getattr(await Cache.get_country(ONLY_ONE_GOOD_KEY), 'currencies', {})
        assert True is currencies.get('BYN', BAD_RESULT).replace('.', '').isdigit()
