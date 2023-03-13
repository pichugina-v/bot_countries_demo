import json
import os

from aiohttp import ClientResponse
from dotenv import load_dotenv

from services.repositories.api.api_urls import GEOCODER_URL
from services.repositories.api.base_api_repository import BaseAPIRepository

load_dotenv()

YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
URL = GEOCODER_URL.format(yandex_api_key=YANDEX_API_KEY)


class GeocoderAPIRepository(BaseAPIRepository):
    async def get_base_info(self, city_or_country_name: str) -> tuple[str, str]:
        """
        Returns country code and city coordinates.

        :param city_or_country_name: country or city name
        :type: str

        :return: coordinates and country_code
        :rtype: Union[str, str]
        """
        url = URL.format(city_or_country_name=city_or_country_name)
        response = await self._send_request(url=url)
        data_yandex_geocoder = await self._parse_response(response)
        coordinates = data_yandex_geocoder['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        country_code = data_yandex_geocoder['response']['GeoObjectCollection']['featureMember'][
            0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['country_code']
        return (coordinates, country_code)

    async def _parse_response(self, response: ClientResponse) -> dict:
        """
        This function parse response.

        :param response: response from aiohttp
        :type: ClientResponse

        :return: parsed response
        :rtype: dict
        """
        data_yandex_geocoder = json.loads(await response.read())
        return data_yandex_geocoder
