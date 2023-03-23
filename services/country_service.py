from dataclasses import dataclass

from cache.cache_module import Cache
from services.repositories.api.api_schemas import GeocoderSchema
from services.repositories.api.country_detail import CountryAPIRepository
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.countries import CountryDBRepository
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema
from services.service_schemas import CityCoordinatesSchema


@dataclass
class CountryService:
    """
    Class for get info about country from cache, database or api repositories.
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

    async def get_languages(self, country_info: GeocoderSchema):    # положить локализованные языки в кэш
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return LanguageNamesSchema(languages=cache_country.languages)
        languages = await self.crud.get_country_languages(country_info.country_code)
        if not languages:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            await self.crud.create(country)
            languages = await self.crud.get_country_languages(country_info.country_code)
        return languages

    async def get_currencies(self, country_info: GeocoderSchema):
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return CurrencyCodesSchema(currency_codes=[currency for currency in cache_country.currencies.keys()])
        currencies = await self.crud.get_country_currencies(country_info.country_code)
        if not currencies:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            await self.crud.create(country)
            currencies = await self.crud.get_country_currencies(country_info.country_code)
        return currencies

    async def get_currency_rates(self, currencies: CurrencyCodesSchema):
        return await self.currency_repo.get_rate(currencies.currency_codes)

    async def get_capital_weather(self, country_info: GeocoderSchema):
        city = await self.get_capital_info(country_info)
        return await self.weather_repo.get_weather(city.latitude, city.longitude)

    async def get_capital_info(self, country_info: GeocoderSchema):
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
