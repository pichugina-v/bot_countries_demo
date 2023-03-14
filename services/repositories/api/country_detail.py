from dataclasses import dataclass
from http import HTTPStatus

from aiohttp import ClientResponse
from pydantic import BaseModel

from services.repositories.api.api_settings import REST_COUNTRY_API_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


class CountryData(BaseModel):
    iso_code: str
    name_en: str
    name_ru: str
    capital: str
    capital_longitude: float
    capital_latitude: float
    area_size: float
    population: int
    currencies: dict[str, str]
    languages: list[str]


@dataclass
class CountryDetailRepository(BaseAPIRepository):
    """
    This is a class of a RestCOuntries repository. Provides detailed information about countries
    by sending request to external API "Restcountries.com".
    Extends of the :class:`BaseAPIRepository` class.
    """
    api_url: str | None = REST_COUNTRY_API_URL

    async def get_country_detail(self, country_code: str) -> CountryData | None:
        """
        Return details about country by recieved country code.

        :param country_code: country iso code (example: "GB", "CA", "RU")

        :return: country details as :class:`CountryData` object or None
        """
        if self.api_url:
            response = await self._send_request(self.api_url.format(country_code=country_code))
        if response.status == HTTPStatus.OK:
            return await self._parse_response(response)
        else:
            return None

    async def _parse_response(self, response: ClientResponse) -> CountryData:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parsed response as :class:`CountryData` object
        """
        country_data = await response.json()
        iso_code = country_data[0]['cca2']
        name_en = country_data[0]['name']['common']
        name_ru = country_data[0]['translations']['rus']['common']
        capital = country_data[0]['capital'][0]
        capital_longitude = country_data[0]['capitalInfo']['latlng'][1]
        capital_latitude = country_data[0]['capitalInfo']['latlng'][0]
        area_size = country_data[0]['area']
        population = country_data[0]['population']
        currencies = {
            currency: country_data[0]['currencies'][currency]['name']
            for currency in country_data[0]['currencies']
        }
        languages = list(
            language for language in country_data[0]['languages'].values()
        )
        return CountryData(
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
