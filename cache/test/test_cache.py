import pytest
import pytest_asyncio

from cache.cache_module import Cache
from cache.test.contains import (
    CITY_COORDINATES_KEY,
    CITY_DATA,
    COUNTRY_COORDINATES_KEY,
    COUNTRY_DATA,
)


class TestCache:
    """
    Repository test for cache
    """

    @pytest.mark.asyncio()
    @pytest.mark.order(1)
    async def test_get_city_none(self, _clear_city: pytest_asyncio.fixture) -> None:
        """
        Test get empty city cache.
        """
        cache_response = await Cache.get_city(CITY_COORDINATES_KEY)
        assert cache_response is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(2)
    async def test_create_city() -> None:
        """
        Test create city cache.
        """
        await Cache.create_or_update_city(CITY_DATA)

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(3)
    async def test_get_city() -> None:
        """
        Test get not empty city cache.
        """
        cache_response = await Cache.get_city(CITY_COORDINATES_KEY)
        assert cache_response == CITY_DATA

    @pytest.mark.asyncio()
    @pytest.mark.order(4)
    async def test_get_country_none(self, _clear_country: pytest_asyncio.fixture) -> None:
        """
        Test get empty country cache.
        """
        cache_response = await Cache.get_country(COUNTRY_COORDINATES_KEY)
        assert cache_response is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(5)
    async def test_create_country() -> None:
        """
        Test create country cache.
        """
        await Cache.create_or_update_country(COUNTRY_DATA)

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.order(6)
    async def test_get_country() -> None:
        """
        Test get not empty city cache.
        """
        cache_response = await Cache.get_country(COUNTRY_COORDINATES_KEY)
        assert cache_response == COUNTRY_DATA
