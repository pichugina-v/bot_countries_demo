import pytest

from cache.cache_module import Cache
from cache.test.clear_test_data import clear_city, clear_country
from cache.test.data_for_test import (
    CITY_COORDINATES_KEY,
    CITY_DATA,
    COUNTRY_COORDINATES_KEY,
    COUNTRY_DATA,
)


class TestCache:
    @staticmethod
    @pytest.mark.asyncio()
    @pytest.mark.order(1)
    async def test_get_city_none():
        cache_response = await Cache.get_city(CITY_COORDINATES_KEY)
        assert cache_response is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(2)
    async def test_create_city():
        await Cache.create_or_update_city(CITY_DATA)

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(3)
    async def test_get_city():
        cache_response = await Cache.get_city(CITY_COORDINATES_KEY)
        assert cache_response == CITY_DATA
        await clear_city()

    @staticmethod
    @pytest.mark.asyncio()
    @pytest.mark.order(4)
    async def test_get_country_none():
        cache_response = await Cache.get_country(COUNTRY_COORDINATES_KEY)
        assert cache_response is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(5)
    async def test_create_country():
        await Cache.create_or_update_country(COUNTRY_DATA)

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(6)
    async def test_get_country():
        cache_response = await Cache.get_country(COUNTRY_COORDINATES_KEY)
        assert cache_response == COUNTRY_DATA
        await clear_country()
