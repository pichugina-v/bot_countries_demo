from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.cache_settings import REDIS as redis
from cache.test.data_for_test import CITY_COORDINATES_KEY, COUNTRY_COORDINATES_KEY

key_city = PREFIX_CITY + CITY_COORDINATES_KEY
key_country = PREFIX_COUNTRY + COUNTRY_COORDINATES_KEY


async def clear_city():
    await redis.delete(key_city)
    await redis.close()


async def clear_country():
    await redis.delete(key_country)
    await redis.close()
