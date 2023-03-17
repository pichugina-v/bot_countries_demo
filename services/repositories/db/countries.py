from asgiref.sync import sync_to_async
from pydantic import BaseModel

from django_layer.countries_app.models import City, Country, Currency, Language
from services.repositories.api.country_detail import CountrySchema
from services.repositories.db.base_db_repository import BaseDBRepository


class CurrencyDBSchema(BaseModel):
    currency_codes: list[str]


class LanguageDBSchema(BaseModel):
    languages: list[str]


class CountryDBRepository(BaseDBRepository):
    """
    This is a class of a Country Database repository. Provides CRUD operations for Country entity.
    Supported methods: create, update, get_by_pk, get_by_name, create_capital.
    Extends of the :class:`BaseDBRepository` class.
    """
    async def create(self, data: CountrySchema) -> Country:
        """
        Create a country record in Country table.

        :param data: new country attributed as :class:`CountrySchema` object

        :return: created country record from Country table
        """
        new_country = await Country.objects.acreate(
            iso_code=data.iso_code,
            name=data.name,
            area_size=data.area_size,
            population=data.population
        )
        await self._create_capital_city(data)
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
            name=data.name_ru,
            area_size=data.area_size,
            population=data.population
        )
        country = await self.get_by_pk(iso_code)
        await self._update_languages(data.languages, country)
        await self._update_currencies(data.currencies, country)
        return country

    async def get_by_pk(self, iso_code: str) -> Country | None:
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

        :param name: country name in russian

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

    @staticmethod
    async def _create_capital_city(data: CountrySchema):
        """
        Create a capital city record in City table

        :param data: new country attributed as :class:`CountrySchema` object

        :return: created city record from City table
        """
        new_city = await City.objects.acreate(
            name=data.capital,
            longitude=data.capital_longitude,
            latitude=data.capital_latitude,
            is_capital=True,
            country=await Country.objects.aget(iso_code=data.iso_code)
        )
        return new_city

    async def get_city_by_country_pk(self, country_pk) -> City | None:
        """
        Looking for city record with requested country pk.
        Returns a city record from City table or None, if not found.

        :param country_pk: country database identificator

        :return: city record from City table or None
        """
        try:
            city = await City.objects.filter(country_id=country_pk).aget(is_capital=True)
            return city
        except City.DoesNotExist:
            return None

    async def get_country_currency(self, country_pk: str) -> CurrencyDBSchema | None:
        """
        Looking for all currency records with requested country pk.
        Returns a list of currency names from Currency table or None, if not found.

        :param country_pk: country database identificator

        :return: list of currency names from Currency table or None
        """
        country = await self.get_by_pk(country_pk)
        currencies = []
        if country:
            async for currency in await sync_to_async(country.currencies.all)():
                currencies.append(currency.iso_code)
            return CurrencyDBSchema(currency_codes=currencies)
        return None

    async def get_country_language(self, country_pk: str) -> LanguageDBSchema | None:
        """
        Looking for all language records with requested country pk.
        Returns a list of languages names from Language table or None, if not found.

        :param country_pk: country database identificator

        :return: list of language names from Language table or None
        """
        country = await self.get_by_pk(country_pk)
        languages = []
        if country:
            async for language in await sync_to_async(country.languages.all)():
                languages.append(language.name)
            return LanguageDBSchema(languages=languages)
        return None


def get_country_db_repository() -> CountryDBRepository:
    """
    Returns object of :class:`CountryDBRepository` class

    return: :class:`CountryDBRepository` object
    """
    return CountryDBRepository()
