import json

from cache.cache_settings import LIVE_CACHE_SECONDS as TTL
from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.cache_settings import REDIS as redis
from services.repositories.api.api_schemas import CitySchema, CountrySchema


class Cache:

    @staticmethod
    async def get_country(coordinates: str) -> CountrySchema | None:
        """
        The function receives information about the country from the cache,
        if there is no entry in the cache, it returns None.

        :param coordinates

        :return: information about the country
        """
        country_data = await redis.get(f'{PREFIX_COUNTRY}{coordinates.replace(" ", "_")}')
        await redis.close()
        if country_data:
            return CountrySchema(**json.loads(country_data))
        return None

    @staticmethod
    async def get_city(coordinates: str) -> CitySchema | None:
        """
        The function receives information about the city from the cache,
        if there is no entry in the cache, it returns None.

        :param coordinates

        :return: information about the city
        """
        city_data = await redis.get(f'{PREFIX_CITY}{coordinates.replace(" ", "_")}')
        await redis.close()
        if city_data:
            return CitySchema(**json.loads(city_data))
        return None

    @staticmethod
    async def create_or_update_country(coordinates: str, country_data: CountrySchema) -> None:
        """
        Function creates or updates country cache

        :param coordinates:
        :param country_data

        :return: None
        """
        key_country = f'{PREFIX_COUNTRY}{coordinates.replace(" ", "_")}'
        await redis.set(key_country, json.dumps(dict(country_data)), TTL)
        await redis.close()

    @staticmethod
    async def create_or_update_city(city_data: CitySchema) -> None:
        """
        Function creates or updates city cache

        :param city_data

        :return: None
        """
        key_city = f'{PREFIX_CITY}{city_data.longitude}_{city_data.latitude}'
        await redis.set(key_city, json.dumps(dict(city_data)), TTL)
        await redis.close()
