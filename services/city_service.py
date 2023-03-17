from cache.cache_module import Cache
from services.repositories.api.geocoder import GeocoderAPIRepository, GeocoderDTO
from services.repositories.db.cities import CityBDRerpository


class CityService:
    """
    Class for get info about city from same repositories.
    """

    def __init__(self):
        self.geocoder = GeocoderAPIRepository()
        self.repository = CityBDRerpository()
        self.cache = Cache()

    # async def get_city(self, name: str) -> CacheDTO | City | None:
    async def get_city(self, name: str) -> GeocoderDTO | None:
        """
        Try to get info about city from same repositories.

        :param name: city name
        :return: information about city
        """
        city_info = await self.geocoder.get_base_info(name)
        print(city_info)
        return city_info
        # if city_info:
        #     return None
        # cache_city = await self.cache.get(city_info.coordinates)
        # if cache_city:
        #     return cache_city
        # db_city = await self.repository.get_by_name(city_name=city_info.name)
        # if db_city:
        #     return db_city
        # return None

    async def get_city_weather(self, city_name: str):
        pass

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
