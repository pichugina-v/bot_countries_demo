import json

from cache.cache_settings import LIVE_CACHE_SECONDS as TTL
from cache.cache_settings import PREFIX_CITY, PREFIX_COUNTRY
from cache.cache_settings import REDIS as redis
from services.repositories.api.api_schemas import (
    CitySchema,
    CountrySchema,
    GeocoderSchema,
)


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

    @staticmethod
    async def get_city_by_name(city_name: str) -> GeocoderSchema | None:
        """
        Get geocoder data from cache

        :param city_name

        :return:
        """
        city_data = await redis.get(f'{PREFIX_CITY}{city_name}')
        await redis.close()
        if city_data:
            return GeocoderSchema(**json.loads(city_data))

        return None

    @staticmethod
    async def set_city_geocoder(city: GeocoderSchema) -> None:
        """
        Function creates or updates city geocoder cache

        :param city:
        :param key:

        :return: None
        """
        key = f'{PREFIX_CITY}{city.name}'
        await redis.set(key, json.dumps(city.dict()), TTL)
        await redis.close()

    @staticmethod
    async def get_country_by_name(country_name: str) -> GeocoderSchema | None:
        """
        Get geocoder data from cache

        :param city_name

        :return:
        """
        country_data = await redis.get(f'{PREFIX_CITY}{country_name}')
        await redis.close()
        if country_data:
            return GeocoderSchema(**json.loads(country_data))

        return None

    @staticmethod
    async def set_country_geocoder(country: GeocoderSchema) -> None:
        """
        Function creates or updates city geocoder cache

        :param city:
        :param key:

        :return: None
        """
        key = f'{PREFIX_CITY}{country.name}'
        await redis.set(key, json.dumps(country.dict()), TTL)
        await redis.close()
