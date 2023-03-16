from cache.cache_module import Cache, CacheDTO
from django_layer.countries_app.models import City
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.db.city import CityBDRerpository


class CityService:
    """
    Class for get info about city from same repositories.
    """

    def __init__(self):
        self.geocoder = GeocoderAPIRepository()
        self.repository = CityBDRerpository()
        self.cache = Cache()

    async def get_city(self, name: str) -> CacheDTO | City | None:
        """
        Try to get info about city from same repositories.

        :param name: city name
        :return: information about city
        """
        city_info = await self.geocoder.get_base_info(name)
        if not city_info:
            return None
        cache_city = await self.cache.get(city_info.coordinates)
        if cache_city:
            return cache_city
        db_city = await self.repository.get_by_name(city_name=city_info.name)
        if db_city:
            return db_city
        return None
