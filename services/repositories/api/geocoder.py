import json

from aiohttp import ClientResponse

from services.repositories.api.api_settings import YANDEX_API_KEY
from services.repositories.api.api_urls import GEOCODER_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


class GeocoderAPIRepository(BaseAPIRepository):
    async def get_base_info(self, city_or_country_name: str) -> tuple[float, float, str]:
        """
        Returns country code and city coordinates.

        :param city_or_country_name: country or city name
        :type: str

        :return: Latitude and Longitude and country code
        :rtype: tuple[float, float, str]
        """
        url = GEOCODER_URL.format(yandex_api_key=YANDEX_API_KEY,
                                  city_or_country_name=city_or_country_name)
        response = await self._send_request(url=url)
        return await self._parse_response(response)

    async def _parse_response(self, response: ClientResponse) -> tuple[float, float, str]:
        """
        This function parse response.

        :param response: response from aiohttp
        :type: ClientResponse

        :return: parsed response
        :rtype: tuple[float, float, str]
        """
        data_yandex_geocoder = json.loads(await response.read())
        coordinates = data_yandex_geocoder['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        country_code = data_yandex_geocoder['response']['GeoObjectCollection']['featureMember'][
            0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['country_code']
        coordinates = coordinates.split()
        lons = float(coordinates[0])
        lats = float(coordinates[1])
        return (lons, lats, country_code)
