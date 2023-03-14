# from cache.cache_settings import REDIS as redis
import asyncio
from typing import NamedTuple

from cache.cache_settings import LIVE_CACHE_SECONDS as ttl
from cache.cache_settings import REDIS as redis


class CacheDTO(NamedTuple):
    data_bool: bool = None
    geo_info_data: dict = None


class Cache:11

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
        await redis.expire(coordinates, ttl)
        await redis.close()


data = {'k': 1, 's': 5}


async def main():
    # return await Cache.exists_('11123')
    return await asyncio.gather(Cache.create_or_update('1112', data), Cache.get('1112'))


if __name__ == '__main__':
    x = asyncio.run(main())
    print(x)
