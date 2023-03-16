from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from cache.cache_module import Cache, CacheDTO
from django_layer.countries_app.models import Country
from services.repositories.api.api_schemas import (
    CountrySchema,
    CurrencySchema,
    WeatherSchema,
)
from services.repositories.api.country_detail import CountryAPIRepository
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.countries import CountryDBRepository, LanguageDBSchema


class CurrencyServiceSchema(BaseModel):
    currencies: list[CurrencySchema]


@dataclass
class CountryService:
    """
    This is a class of a Country Service. Provides operations for retrieving information about countries.
    """
    cache: Cache = Cache()
    geocoder: GeocoderAPIRepository = GeocoderAPIRepository()
    countries_repo: CountryAPIRepository = CountryAPIRepository()
    weather_repo: WeatherAPIRepository = WeatherAPIRepository()
    currency_repo: CurrencyAPIRepository = CurrencyAPIRepository()
    crud: CountryDBRepository = CountryDBRepository()

    async def get_country(self, name: str) -> CacheDTO | Country | None:
        """
        Get info about country from cache, then db, then api repositories if exists.

        :param name: country name

        :return: information about country or None
        """
        country_info = await self.geocoder.get_base_info(name)
        if not country_info:
            return None
        cache_country = await self.cache.exists(country_info.coordinates)
        if cache_country.data_bool:
            return await self.cache.get(country_info.coordinates)
        db_country = await self.crud.get_by_name(name=country_info.name)
        if db_country is None:
            db_country = await self.crud.get_by_pk(country_info.country_code)
            if db_country is None:
                # country = await self.countries_repo.get_country_detail(country_info.country_code)
                country = CountrySchema(
                    iso_code='RU',
                    name_en='Russia',
                    name_ru='Россия',
                    capital='Moscow',
                    capital_longitude=37.61,
                    capital_latitude=55.75,
                    area_size=17098246.0,
                    population=1234567,
                    currencies={'EUR': 'Euro', 'USD': 'Dollar'},
                    languages=['Russian']
                )
                if country:
                    db_country = await self.crud.create(country)
        return db_country

    async def _get_db_country(self, name: str) -> Country | None:
        """
        Retrieves country object from database by name or requests iso_code from api
        and retrieves country object from database by iso_code.

        :param name: country name

        :return: information about country or None
        """
        db_country = await self.crud.get_by_name(name)
        if db_country is None:
            country_info = await self.geocoder.get_base_info(name)
            db_country = await self.crud.get_by_pk(country_info.country_code)
            if db_country is None:
                return None
        return db_country

    async def get_capital_info(self, name: str) -> tuple[Any, Any, Any] | None:
        """
        Retrieves city object from database by country name

        :param name: country name

        :return: name, longitude and latitude of a capital city
        """
        db_country = await self._get_db_country(name)
        if db_country is not None:
            city = await self.crud.get_city_by_country_pk(db_country.iso_code)
            if city:
                return city.longitude, city.latitude, city.name
        return None

    async def get_capital_weather(self, latitude: float, longitude: float) -> WeatherSchema | None:
        """
        Returns information about current weather in the country capital

        :param latutide: capital latitude
        :param longitude: capital longitude

        :return: information about current weather in the capital city
        """
        weather = await self.weather_repo.get_weather(latitude, longitude)
        return weather

    async def get_languages(self, name: str) -> LanguageDBSchema | None:
        """
        Retrieves language records from database by country name

        :param name: country name

        :return: language records
        """
        db_country = await self._get_db_country(name)
        if db_country is not None:
            languages = await self.crud.get_country_language(db_country.iso_code)
            return languages
        return None

    async def get_currency(self, name: str) -> CurrencyServiceSchema | None:
        """
        Returns information about currency of the country

        :param name: country name

        :return: information about currency
        """
        db_country = await self._get_db_country(name)
        if db_country is not None:
            currencies = await self.crud.get_country_currency(db_country.iso_code)
            if currencies is not None:
                currencies_info = []
                for currency_code in currencies.currency_codes:
                    currency = await self.currency_repo.get_rate(currency_code)
                    if currency is not None:
                        currencies_info.append(currency)
                return currencies_info
        return None
