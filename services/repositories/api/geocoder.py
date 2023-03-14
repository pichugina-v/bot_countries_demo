import asyncio
import json
from typing import NamedTuple

from aiohttp import ClientResponse

from services.repositories.api.api_settings import GEOCODER_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


class GeocoderDTO(NamedTuple):

    latitude: float
    longitude: float
    country_code: str


class GeocoderAPIRepository(BaseAPIRepository):
    async def get_base_info(self, city_or_country_name: str) -> GeocoderDTO:
        """
        Returns country code and city coordinates.

        :param city_or_country_name: country or city name

        :return: Latitude and Longitude and country code
        """
        url = str(GEOCODER_URL).format(city_or_country_name=city_or_country_name)
        response = await self._send_request(url=url)
        return await self._parse_response(response)

    async def _parse_response(self, response: ClientResponse) -> GeocoderDTO:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parsed response
        """
        data_yandex_geocoder = json.loads(await response.read())
        coordinates = data_yandex_geocoder['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        country_code = data_yandex_geocoder['response']['GeoObjectCollection']['featureMember'][
            0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['country_code']
        coordinates = coordinates.split()
        lons = float(coordinates[0])
        lats = float(coordinates[1])
        return GeocoderDTO(latitude=lats, longitude=lons, country_code=country_code)


p = GeocoderAPIRepository()
loop = asyncio.get_event_loop()
data = loop.run_until_complete(p.get_base_info('москва'))
print(data)
