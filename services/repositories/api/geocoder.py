import json

from aiohttp import ClientResponse, ClientSession

from services.repositories.api.abstract_api_repository import AbstractAPIRepository
from services.repositories.api.api_schemas import GeocoderSchema
from services.repositories.api.api_settings import (
    CITY,
    COUNTRY,
    GEOCODER_URL,
    YANDEX_API_KEY,
)


class GeocoderAPIRepository(AbstractAPIRepository):

    async def get_city(self, city_name: str) -> GeocoderSchema | None:
        """
        Returns basic information about the city,
        if Yandex api confirms that the user entered the city.

        :param city_name: city name

        :return: Latitude and Longitude and country code
        """
        info_city = await self.get_base_info(city_name)
        if info_city and info_city.search_type == CITY:
            return info_city
        return None

    async def get_country(self, country_name: str) -> GeocoderSchema | None:
        """
        Returns basic information about the country,
        if Yandex api confirms that the user entered the country.

        :param country_name: country name

        :return: Latitude and Longitude and country code
        """
        info_country = await self.get_base_info(country_name)
        if info_country and info_country.search_type == COUNTRY:
            return info_country
        return None

    async def get_base_info(self, city_or_country_name: str) -> GeocoderSchema | None:
        """
        Returns country code and city coordinates and type search.

        :param city_or_country_name: country or city name

        :return: Latitude and Longitude and country code
        """
        url = f'{GEOCODER_URL}{YANDEX_API_KEY}&geocode={city_or_country_name}'
        response = await self._send_request(url=url)
        return await self._parse_response(response)

    async def _send_request(self, url: str, params=None, body=None) -> ClientResponse:
        """
        Send GET response
        :param url: API url address
        :param params: optional request's query params
        :param body: optional request's body
        :return: response from API
        """

        async with ClientSession() as session:
            resp = await session.get(url=url, params=params)
        return resp

    async def _parse_response(self, response: ClientResponse) -> GeocoderSchema | None:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parse response
        """
        data_yandex_geocoder = json.loads(await response.read())
        try:
            geo_obj = data_yandex_geocoder['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']
            geocoder_meta_data = geo_obj['metaDataProperty']['GeocoderMetaData']
            coordinates = geo_obj['Point']['pos']
            country_code = geocoder_meta_data['Address']['country_code']
            search_type = geocoder_meta_data['kind']
        except KeyError:
            return None
        return GeocoderSchema(coordinates=coordinates, country_code=country_code,
                              search_type=search_type)
