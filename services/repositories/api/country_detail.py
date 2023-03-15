from dataclasses import dataclass
from http import HTTPStatus

from aiohttp import ClientResponse

from services.repositories.api.api_schemas import CountrySchema
from services.repositories.api.api_settings import COUNTRY_INFO_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


@dataclass
class CountryDetailRepository(BaseAPIRepository):
    """
    This is a class of a RestCOuntries repository. Provides detailed information about countries
    by sending request to external API "Restcountries.com".
    Extends of the :class:`BaseAPIRepository` class.
    """
    api_url: str | None = COUNTRY_INFO_URL

    async def get_country_detail(self, country_code: str) -> CountrySchema | None:
        """
        Return details about country by recieved country code.

        :param country_code: country iso code (example: "GB", "CA", "RU")

        :return: country details as :class:`CountrySchema` object or None
        """
        if self.api_url:
            response = await self._send_request(self.api_url.format(country_code=country_code))
        if response.status == HTTPStatus.OK:
            return await self._parse_response(response)
        else:
            return None

    async def _parse_response(self, response: ClientResponse) -> CountrySchema:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parsed response as :class:`CountrySchema` object
        """
        country_data = (await response.json())[0]
        iso_code = country_data['cca2']
        name_en = country_data['name']['common']
        name_ru = country_data['translations']['rus']['common']
        capital = country_data['capital'][0]
        capital_longitude = country_data['capitalInfo']['latlng'][1]
        capital_latitude = country_data['capitalInfo']['latlng'][0]
        area_size = country_data['area']
        population = country_data['population']
        currencies = {
            currency: country_data['currencies'][currency]['name']
            for currency in country_data['currencies']
        }
        languages = list(
            language for language in country_data['languages'].values()
        )
        return CountrySchema(
            iso_code=iso_code,
            name_en=name_en,
            name_ru=name_ru,
            capital=capital,
            capital_latitude=capital_latitude,
            capital_longitude=capital_longitude,
            area_size=area_size,
            population=population,
            currencies=currencies,
            languages=languages
        )


def get_country_detail_repository() -> CountryDetailRepository:
    """
    Returns object of :class:`CountryDetailRepository` class

    return: :class:`CountryDetailRepository` object
    """
    return CountryDetailRepository()
