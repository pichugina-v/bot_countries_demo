from typing import NamedTuple

from cache.cache_settings import LIVE_CACHE_SECONDS as TTL
from cache.cache_settings import REDIS as redis


class CacheDTO(NamedTuple):
    data_bool: bool | None = None
    geo_info_data: dict | None = None


class Cache:

    @staticmethod
    async def exists(coordinates: str) -> CacheDTO:
        """
        The function checks for the presence of an entry in the cache.

        :param coordinates

        :return: True or False
        """
        data_bool = bool(await redis.exists(coordinates))
        await redis.close()
        return CacheDTO(data_bool=data_bool)

    @staticmethod
    async def get(coordinates: str) -> CacheDTO:
        """
        The function gets an entry from the cache.

        :param coordinates

        :return: information about the city or country
        """
        geo_info_data = await redis.hgetall(coordinates)
        await redis.close()
        return CacheDTO(geo_info_data=geo_info_data)

    @staticmethod
    async def create_or_update(coordinates: str, geo_info_data: dict) -> None:
        """
        Function creates or updates an existing cache entry

        :param coordinates

        :return: None
        """
        await redis.hmset(coordinates, geo_info_data)
        await redis.expire(coordinates, TTL)
        await redis.close()
