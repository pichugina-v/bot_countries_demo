from cache.cache_module import Cache
from services.repositories.abstract_uow import AbstractUnitOfWork
from services.repositories.api.api_schemas import GeocoderSchema, WeatherSchema
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.cities import CityBDRepository


class CityService(AbstractUnitOfWork):
    """
    Class for get info about city from same repositories.
    """

    def __init__(self):
        self.geocoder = GeocoderAPIRepository()
        self.repository = CityBDRepository()
        self.cache = Cache()
        self.weather_repo: WeatherAPIRepository = WeatherAPIRepository()

    async def get_city(self, name: str) -> GeocoderSchema | None:
        """
        Try to get info about city from same repositories.

        :param name: city name
        :return: information about city
        """
        city_info = await self.geocoder.get_city(name)
        if city_info:
            return city_info
        # cache_city = await self.cache.get_city_by_name(name)
        # if cache_city:
        #     return cache_city
        # db_city = await self.repository.get_by_name(city_name=city_info.name)
        # if db_city:
        #     return db_city
        return None

    async def get_city_weather(self, latitude: float, longitude: float) -> WeatherSchema | None:
        weather = await self.weather_repo.get_weather(latitude, longitude)
        return weather

    # async def get_currency(self, name: str) -> float | None:
    #     """
    #     Returns information about currency rate of the city
    #
    #     :param name: city name
    #
    #     :return: currency rate
    #     """
    #     db_country = await self._get_db_country(name)
    #     if db_country is not None:
    #         currencies = await self.crud.get_country_currency(db_country.iso_code)
    #         if currencies is not None:
    #             currencies_info = []
    #             for currency_code in currencies.currency_codes:
    #                 currency = await self.currency_repo.get_rate(currency_code)
    #                 if currency is not None:
    #                     currencies_info.append(currency)
    #             return currencies_info
    #     return None
