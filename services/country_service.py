from dataclasses import dataclass

from pydantic import BaseModel

from cache.cache_module import Cache
from services.repositories.api.api_schemas import (
    CitySchema,
    CurrencySchema,
    GeocoderSchema,
)
from services.repositories.api.country_detail import CountryAPIRepository
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.countries import CountryDBRepository
from services.repositories.db.schemas import LanguageNamesSchema


class CurrencyServiceSchema(BaseModel):
    currencies: list[CurrencySchema]


@dataclass
class CountryService:
    """
    Class for get info about city from same repositories.
    """
    cache: Cache = Cache()
    geocoder: GeocoderAPIRepository = GeocoderAPIRepository()
    countries_repo: CountryAPIRepository = CountryAPIRepository()
    weather_repo: WeatherAPIRepository = WeatherAPIRepository()
    currency_repo: CurrencyAPIRepository = CurrencyAPIRepository()
    crud: CountryDBRepository = CountryDBRepository()

    async def get_country_info(self, country_name: str):
        country_info = await self.geocoder.get_country(country_name)
        if not country_info:
            return None
        return country_info

    async def get_country(self, country_info: GeocoderSchema):
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return cache_country
        db_country = await self.crud.get_by_name(name=country_info.name)
        if not db_country:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            db_country = await self.crud.create(country)
            await self.cache.create_or_update_country(country_info.coordinates, country)
        return db_country

    async def get_languages(self, country_info: GeocoderSchema):
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return LanguageNamesSchema(languages=cache_country.languages)
        return await self.crud.get_country_languages(country_info.country_code)

    async def get_currencies(self, country_info: GeocoderSchema):
        currencies = await self.crud.get_country_currencies(country_info.country_code)
        return await self.currency_repo.get_rate(currencies.currency_codes)

    async def get_capital_weather(self, country_info: GeocoderSchema):
        city = await self._get_capital_info(country_info)
        return await self.weather_repo.get_weather(city.latitude, city.longitude)

    async def _get_capital_info(self, country_info: GeocoderSchema):
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return CitySchema(
                name=cache_country.capital,
                latitude=cache_country.capital_latitude,
                longitude=cache_country.capital_longitude,
                country_code=cache_country.iso_code,
                is_capital=True
            )
        city = await self.crud.get_capital(country_info.country_code)
        if city:
            return CitySchema(
                name=city.name,
                latitude=city.latitude,
                longitude=city.longitude,
                country_code=country_info.country_code,
                is_capital=city.is_capital
            )
        return None
