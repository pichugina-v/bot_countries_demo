import pytest
from aioredis import RedisError
from pytest_asyncio import fixture as async_fixture

from cache.cache_module import Cache
from cache.test.contains import (
    CITY_COORDINATES_KEY,
    CITY_DATA,
    COUNTRY_COORDINATES_KEY,
    COUNTRY_DATA,
)


class TestCacheCity:
    """
    Cache city repository test.
    All tests are atomic.
    """

    @pytest.mark.asyncio()
    async def test_get_city_none(
        self,
        _clear_cache_city: async_fixture
    ) -> None:
        """
        Trying to get a non-existent city cache.
        """
        cache_response = await Cache.get_city(CITY_COORDINATES_KEY)
        assert cache_response is None

    @pytest.mark.asyncio
    async def test_create_city(
        self,
        _clear_cache_city: async_fixture
    ) -> None:
        """
        Test for creating a city entry in the cache.
        """
        created = None
        try:
            await Cache.create_or_update_city(CITY_DATA)
            created = True
        except RedisError:
            created = False
        finally:
            assert created is True

    @pytest.mark.asyncio
    async def test_get_city(
        self,
        _clear_cache_city: async_fixture,
        _create_cache_city: async_fixture
    ) -> None:
        """
        Test for getting an existing city entry in the cache.
        """
        cache_response = await Cache.get_city(CITY_COORDINATES_KEY)
        assert cache_response == CITY_DATA


class TestCacheCountry:
    """
    Cache city repository test.
    All tests are atomic.
    """
    @pytest.mark.asyncio()
    async def test_get_country_none(
        self,
        _clear_cache_country: async_fixture
    ) -> None:
        """
        Trying to get a non-existent country cache.
        """
        cache_response = await Cache.get_country(COUNTRY_COORDINATES_KEY)
        assert cache_response is None

    @pytest.mark.asyncio
    async def test_create_country(
        self,
        _clear_cache_country: async_fixture
    ) -> None:
        """
        Test for creating a country entry in the cache.
        """

        created = None
        try:
            await Cache.create_or_update_country(COUNTRY_DATA)
            created = True
        except RedisError:
            created = False
        finally:
            assert created is True

    @pytest.mark.asyncio
    async def test_get_country(
        self,
        _clear_cache_country: async_fixture,
        _create_cache_country: async_fixture
    ) -> None:
        """
        Test for getting an existing country entry in the cache.
        """
        cache_response = await Cache.get_country(COUNTRY_COORDINATES_KEY)
        assert cache_response == COUNTRY_DATA
