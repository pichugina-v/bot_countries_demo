from dataclasses import dataclass

from aiohttp import ClientResponse

from services.repositories.api.api_urls import COUNTRY_INFO
from services.repositories.api.base_api_repository import BaseAPIRepository


@dataclass
class CountryDetailRepository(BaseAPIRepository):
    """
    This is a class of a RestCOuntries repository. Provides detailed information about countries
    by sending request to external API "Restcountries.com".
    Extends of the :class:`BaseAPIRepository` class.
    """
    api_url: str = COUNTRY_INFO

    async def get_country_detail(self, country_code: str) -> dict | None:
        """
        Return details about country by recieved country code.

        :param country_code: country iso code (example: "GB", "CA", "RU")

        :return: country details or None
        """
        response = await self._send_request(self.api_url.format(country_code=country_code))
        if response.status == 200:
            country_data = await self._parse_response(response)
            return dict(
                name_en=country_data[0]['name']['common'],
                name_ru=country_data[0]['translations']['rus']['common'],
                capital=country_data[0]['capital'][0],
                area_size=country_data[0]['area'],
                population=country_data[0]['population'],
                currencies={currency: country_data[0]['currencies'][currency]['name']
                            for currency in country_data[0]['currencies']},
                languages=list(language for language in country_data[0]['languages'].values()),
            )
        else:
            return None

    async def _parse_response(self, response: ClientResponse):
        """
        This function parse response.

        :param response: response from aiohttp

        :return: response content as a json-object
        """
        country_data = await response.json()
        return country_data


def get_country_detail_repository():
    return CountryDetailRepository()
