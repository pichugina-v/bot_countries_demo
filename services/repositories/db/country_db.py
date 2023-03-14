from asgiref.sync import sync_to_async

from django_layer.countries_app.models import Capital, City, Country, Currency, Language
from services.repositories.api.country_detail import CountrySchema


class CountryDBRepository:
    """
    This is a class of a Country Database repository. Provides methods for working with the database for countries.
    Supported methods: create, update, get_by_iso_code, get_by_name, create_capital.
    """
    async def create(self, data: CountrySchema) -> Country:
        """
        Creates new country in database.

        :param data: :class:`CountrySchema` object

        :return: Country object
        """
        new_country = await Country.objects.acreate(
            iso_code=data.iso_code,
            name=data.name_en,
            area_size=data.area_size,
            population=data.population
        )
        await self._set_languages(data.languages, new_country)
        await self._set_currencies(data.currencies, new_country)
        return new_country

    async def update(self, iso_code: str, data: CountrySchema) -> Country:
        """
        Update existing country in database.

        :param iso_code: country iso code (example: "GB", "CA", "RU")
        :param data: :class:`CountrySchema` object

        :return: Country object
        """
        updated_country = await Country.objects.filter(pk=iso_code).aupdate(
            name=data.name_en,
            area_size=data.area_size,
            population=data.population
        )
        country = await self.get_by_iso_code(iso_code)
        if country:
            await self._update_languages(data.languages, country)
            await self._update_currencies(data.currencies, country)
        return updated_country

    async def get_by_iso_code(self, iso_code: str) -> Country | None:
        """
        Returns country by iso_code.

        :param iso_code: country iso code (example: "GB", "CA", "RU")

        :return: Country object or None
        """
        try:
            country = await Country.objects.aget(pk=iso_code)
            return country
        except Country.DoesNotExist:
            return None

    async def get_by_name(self, name: str) -> Country | None:
        """
        Return country by country name.

        :param iso_code: country iso code (example: "GB", "CA", "RU")

        :return: Country object or None
        """
        try:
            country = await Country.objects.aget(name=name)
            return country
        except Country.DoesNotExist:
            return None

    @staticmethod
    async def _set_languages(languages: list, country: Country) -> None:
        """
        Create new languages for concrete country in database.

        :param languages: list of languages (example: ["English", "French"])
        :param country: Country object

        :return: None
        """
        for language in languages:
            try:
                existing_language = await Language.objects.aget(name=language)
                await sync_to_async(country.languages.add)(existing_language)
            except Language.DoesNotExist:
                await country.languages.acreate(name=language)

    @staticmethod
    async def _set_currencies(currencies: dict, country: Country) -> None:
        """
        Create new currencies for concrete country in database.

        :param currencies: dict of currencies (example: {"CAN", "Canadian dollar"})
        :param country: Country object

        :return: None
        """
        for iso_code, currency_name in currencies.items():
            try:
                existing_currency = await Currency.objects.aget(iso_code=iso_code)
                await sync_to_async(country.currencies.add)(existing_currency)
            except Currency.DoesNotExist:
                await country.currencies.acreate(iso_code=iso_code, name=currency_name)

    @staticmethod
    async def _update_languages(languages: list, country: Country) -> None:
        """
        Update languages for concrete country in database.

        :param languages: list of languages (example: ["English", "French"])
        :param country: Country object

        :return: None
        """
        async for language in country.languages.filter(country=country.iso_code):
            await Language.objects.filter(name=language).adelete()
        await sync_to_async(country.languages.clear)()
        for language in languages:
            await country.languages.acreate(name=language)

    @staticmethod
    async def _update_currencies(currencies: dict, country: Country) -> None:
        """
        Update currencies for concrete country in database.

        :param currencies: dict of currencies (example: {"CAN", "Canadian dollar"})
        :param country: Country object

        :return: None
        """
        async for currency in country.currencies.filter(country=country.iso_code):
            await Currency.objects.filter(name=currency).adelete()
        await sync_to_async(country.currencies.clear)()
        for iso_code, currency_name in currencies.items():
            await country.currencies.acreate(iso_code=iso_code, name=currency_name)

    async def create_capital(self, country_pk, city_pk) -> Capital:
        """
        Create new catital in database.

        :param country_pk: country iso_code (primary key)
        :param city_pk: city id (primary key)

        :return: None
        """
        country = await Country.objects.aget(iso_code=country_pk)
        city = await City.objects.aget(id=city_pk)
        new_capital = await Capital.objects.acreate(country_id=country.pk, city_id=city.pk)
        return new_capital


def get_country_db_repository() -> CountryDBRepository:
    """
    Returns object of :class:`CountryDBRepository` class

    return: :class:`CountryDBRepository` object
    """
    return CountryDBRepository()
