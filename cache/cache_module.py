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
        country_data = await redis.get(PREFIX_COUNTRY + coordinates)
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
        city_data = await redis.get(PREFIX_CITY + coordinates)
        await redis.close()
        if city_data:
            return CitySchema(**json.loads(city_data))
        return None

    @staticmethod
    async def create_or_update_country(country_data: CountrySchema) -> None:
        """
        Function creates or updates country cache

        :param country_data

        :return: None
        """
        longitude = str(country_data.capital_longitude)
        latitude = str(country_data.capital_latitude)
        key_country = PREFIX_COUNTRY + longitude + ' ' + latitude
        await redis.set(key_country, json.dumps(dict(country_data)), TTL)
        await redis.close()

    @staticmethod
    async def create_or_update_city(city_data: CitySchema) -> None:
        """
        Function creates or updates city cache

        :param city_data

        :return: None
        """
        longitude = str(city_data.longitude)
        latitude = str(city_data.latitude)
        key_city = PREFIX_CITY + longitude + ' ' + latitude
        await redis.set(key_city, json.dumps(dict(city_data)), TTL)
        await redis.close()
