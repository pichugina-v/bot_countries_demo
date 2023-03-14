from django_layer.countries_app.models import Capital, City, Country
from services.repositories.api.country_detail import CountryData


class CountryDBRepository:
    async def create(self, data: CountryData) -> Country:
        new_country = await Country.objects.acreate(
            iso_code=data.iso_code,
            name=data.name_en,
            area_size=data.area_size,
            population=data.population
        )
        await self._set_languages(data.languages, new_country)
        await self._set_currencies(data.currencies, new_country)
        return new_country

    async def update(self, iso_code, data: CountryData):
        country = await Country.objects.filter(pk=iso_code).aupdate(
            iso_code=data.iso_code,
            name=data.name_en,
            area_size=data.area_size,
            population=data.population
        )
        # updated_country = await self.get_by_iso_code(iso_code)
        # await self._update_languages(data.languages, updated_country)
        # await self._update_currencies(data.currencies, updated_country)
        return country

    async def get_by_iso_code(self, iso_code):
        country = await Country.objects.aget(pk=iso_code)
        return country

    async def get_by_name(self, name):
        country = await Country.objects.aget(name=name)
        return country

    async def _set_languages(self, languages, country):
        for language in languages:
            await country.languages.acreate(name=language)

    async def _set_currencies(self, currencies, country):
        for iso_code, currency_name in currencies.items():
            await country.currencies.acreate(iso_code=iso_code, name=currency_name)

    # async def _update_currencies(self, currencies, country):
    #     for iso_code, currency_name in currencies.items():
    #         await country.currencies.aupdate(iso_code=iso_code, name=currency_name)

    # async def _update_languages(self, languages, country):
    #     for language in languages:
    #         await country.languages.aupdate(name=language)

    async def create_capital(self, country_pk, city_pk):
        country = await Country.objects.aget(iso_code=country_pk)
        city = await City.objects.aget(id=city_pk)
        new_capital = await Capital.objects.acreate(country_id=country.pk, city_id=city.pk)
        return new_capital


def get_country_db_repository() -> CountryDBRepository:
    return CountryDBRepository()
