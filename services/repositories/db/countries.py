from asgiref.sync import sync_to_async

from django_layer.countries_app.models import Capital, City, Country, Currency, Language
from services.repositories.api.country_detail import CountrySchema


class CountryDBRepository:
    """
    This is a class of a Country Database repository. Provides CRUD operations for Country entity.
    Supported methods: create, update, get_by_iso_code, get_by_name, create_capital.
    """
    async def create(self, data: CountrySchema) -> Country:
        """
        Create a country record in Country table.

        :param data: new country attributed as :class:`CountrySchema` object.

        :return: created country record from Country table
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
        Update a country record in Country table.

        :param iso_code: country database identificator
        :param data: city attributes to update as :class:`CountrySchema` object

        :return: created country record from Country table
        """
        country = await Country.objects.filter(pk=iso_code).aupdate(
            name=data.name_en,
            area_size=data.area_size,
            population=data.population
        )
        country = await self.get_by_iso_code(iso_code)
        await self._update_languages(data.languages, country)
        await self._update_currencies(data.currencies, country)
        return country

    async def get_by_iso_code(self, iso_code: str) -> Country | None:
        """
        Looking for country record with requested iso_code.
        Returns a country record from Country table or None, if not found.

        :param iso_code: country database identificator

        :return: country record from Country table or None
        """
        try:
            country = await Country.objects.aget(pk=iso_code)
            return country
        except Country.DoesNotExist:
            return None

    async def get_by_name(self, name: str) -> Country | None:
        """
        Looking for country record with requested name.
        Returns a country record from Country table or None, if not found.

        :param name: country name (example: "GB", "CA", "RU")

        :return: country record from Country table or None
        """
        try:
            country = await Country.objects.aget(name=name)
            return country
        except Country.DoesNotExist:
            return None

    @staticmethod
    async def _set_languages(languages: list, country: Country) -> None:
        """
        Create new languages for concrete country in database or sets existing language for country.

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
        Create new currencies for concrete country in database or sets existing currencies for country.

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
        Create a capital record in Capital table.

        :param country_pk: country database identificator
        :param city_pk: city database identificator

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
