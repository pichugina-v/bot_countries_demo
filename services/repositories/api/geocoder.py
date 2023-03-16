import json

from aiohttp import ClientResponse
from pydantic import BaseModel

from services.repositories.api.api_settings import GEOCODER_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


class GeocoderDTO(BaseModel):
    coordinates: str
    country_code: str
    search_type: str


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
        return GeocoderDTO(
            coordinates=data_yandex_geocoder['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['Point']['pos'],
            country_code=data_yandex_geocoder['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData'][
                'Address']['country_code'],
            search_type=data_yandex_geocoder['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind']
        )
