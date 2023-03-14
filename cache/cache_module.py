# from cache.cache_settings import REDIS as redis
import asyncio

from cache.cache_settings import LIVE_CACHE_SECONDS as ttl
from cache.cache_settings import REDIS as redis


class Cache:

    @staticmethod
    async def exists_(coordinates: str):
        data = await redis.exists(coordinates)
        await redis.close()
        return bool(data)

    @staticmethod
    async def get_(coordinates: str):
        geo_info_data = await redis.hgetall(coordinates)
        await redis.close()
        return geo_info_data

    @staticmethod
    async def set_or_update(coordinates: str, geo_info_data: dict):
        await redis.hmset(coordinates, geo_info_data)
        await redis.expire(coordinates, ttl)
        await redis.close()


data = {'k': 1, 's': 5}


async def main():
    # return await Cache.exists_('11123')
    return await asyncio.gather(Cache.set_('1112', data), Cache.get_('1112'))


if __name__ == '__main__':
    # data = {'k': 1, 's': 2}
    # print(data)
    # x = json.dumps(data)
    # print(x)
    x = asyncio.run(main())

    print(x)
    # print(json.loads(x.decode('utf-8')))
