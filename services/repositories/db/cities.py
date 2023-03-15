from django_layer.countries_app.models import City, Country
from services.repositories.api.api_schemas import CitySchema


class CityBDRerpository:
    """
    This is a class of a CitiesRepository repository. Provides CRUD operations for City entity.
    """

    async def get_by_id(self, city_id: int) -> City | None:
        """
        Looking for city record with requested id.
        Returns a city record from City table.

        :param city_id: city identificator

        :return: city record from City tables
        """
        try:
            city = await City.objects.aget(id=city_id)
            return city
        except City.DoesNotExist:
            return None

    async def get_by_name(self, city_name: str) -> City | None:
        """
        Looking for city record with requested name.
        Returns a city record from City table.

        :param city_name: city database identificator

        :return: city record from City table.
        """
        try:
            city = await City.objects.aget(name=city_name)
            return city
        except City.DoesNotExist:
            return None

    async def create(self, data: CitySchema) -> City:
        """
        Create a city record in City table

        :param data: new city attributes

        :return: created city record from City table
        """
        new_city = await City.objects.acreate(
            name=data.name,
            longitude=data.longitude,
            latitude=data.latitude,
            country=await Country.objects.aget(iso_code=data.country_code)
        )
        return new_city

    async def update(self, city_id: int, new_name: str) -> City | None:
        """
        Update a city record in City table

        :param city_id: city database identificator
        :param new_name: new city name to update

        :return: updated city record from City table
        """
        await City.objects.filter(id=city_id).aupdate(name=new_name)
        updated_city = await self.get_by_id(city_id)
        return updated_city


def get_cities_repository() -> CityBDRerpository:
    """
    Returns object of :class:`CitiesRerpository` class

    return: :class:`CitiesRerpository` object
    """
    return CityBDRerpository()
