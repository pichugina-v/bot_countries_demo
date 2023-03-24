from dataclasses import dataclass

from cache.cache_module import Cache
from django_layer.countries_app.models import Country
from services.repositories.abstract_uow import AbstractUnitOfWork
from services.repositories.api.api_schemas import (
    CountrySchema,
    CurrencySchema,
    GeocoderSchema,
    WeatherSchema,
)
from services.repositories.api.country_detail import CountryAPIRepository
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.countries import CountryDBRepository
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema
from services.service_schemas import CityCoordinatesSchema


@dataclass
class CountryService(AbstractUnitOfWork):
    """
    Class for get info about country from cache, database or api repositories.
    """
    cache: Cache = Cache()
    geocoder: GeocoderAPIRepository = GeocoderAPIRepository()
    countries_repo: CountryAPIRepository = CountryAPIRepository()
    weather_repo: WeatherAPIRepository = WeatherAPIRepository()
    currency_repo: CurrencyAPIRepository = CurrencyAPIRepository()
    crud: CountryDBRepository = CountryDBRepository()

    async def get_country_info(self, country_name: str) -> GeocoderSchema | None:
        country_cache = await self.cache.get_country_by_name(country_name)
        if country_cache:
            return country_cache
        country_info = await self.geocoder.get_country(country_name)
        if country_info:
            await self.cache.set_country_geocoder(country_info)
            return country_info
        return None

    async def get_country(self, country_info: GeocoderSchema) -> CountrySchema | Country:
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return cache_country
        db_country = await self.crud.get_by_name(name=country_info.name)
        if not db_country:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            db_country = await self._create_db_and_cache_country(country, country_info.coordinates)
        return db_country

    async def get_languages(self, country_info: GeocoderSchema) -> LanguageNamesSchema | None:
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return LanguageNamesSchema(languages=cache_country.languages)
        languages = await self.crud.get_country_languages(country_info.country_code)
        if not languages:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            await self._create_db_and_cache_country(country, country_info.coordinates)
        return languages

    async def get_currencies(self, country_info: GeocoderSchema) -> CurrencyCodesSchema | None:
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return CurrencyCodesSchema(currency_codes=[currency for currency in cache_country.currencies.keys()])
        currencies = await self.crud.get_country_currencies(country_info.country_code)
        if not currencies:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            await self._create_db_and_cache_country(country, country_info.coordinates)
        return currencies

    async def get_currency_rates(self, currencies: CurrencyCodesSchema) -> list[CurrencySchema] | None:
        return await self.currency_repo.get_rate(currencies.currency_codes)

    async def get_capital_weather(self, country_info: GeocoderSchema) -> WeatherSchema | None:
        city = await self.get_capital_info(country_info)
        return await self.weather_repo.get_weather(city.latitude, city.longitude)

    async def get_capital_info(self, country_info: GeocoderSchema) -> CityCoordinatesSchema | None:
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return CityCoordinatesSchema(
                name=cache_country.capital,
                latitude=cache_country.capital_latitude,
                longitude=cache_country.capital_longitude,
            )
        city = await self.crud.get_capital(country_info.country_code)
        if city:
            return CityCoordinatesSchema(
                name=city.name,
                latitude=city.latitude,
                longitude=city.longitude,
            )
        return None

    async def _create_db_and_cache_country(self, country, coordinates) -> Country | None:
        db_country = await self.crud.get_by_pk(country.iso_code)
        if not db_country:
            db_country = await self.crud.create(country)
        updated_country = await self.crud.update_country_schema(country, db_country)
        await self.cache.create_or_update_country(coordinates, updated_country)
        return db_country
