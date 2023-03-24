import pytest
import pytest_asyncio

from django_layer.countries_app.models import City, Country
from services.repositories.api.api_schemas import CitySchema


@pytest.fixture
def test_city_data() -> CitySchema:
    return CitySchema(
        name='Moscow',
        country_code='RU',
        longitude=37.61,
        latitude=55.75,
        is_capital=True,
    )


@pytest.fixture
def updated_test_city_data() -> CitySchema:
    return CitySchema(
        name='Saint Petersburg',
        country_code='RU',
        longitude=37.61,
        latitude=55.75,
        is_capital=False,
    )


@pytest_asyncio.fixture
async def country_fixture():
    country = await Country.objects.acreate(
        iso_code='RU',
        name='The Russian Federation',
        population=143000000,
        area_size=17100000,
    )
    return country


@pytest_asyncio.fixture
async def city_fixture(country_fixture, test_city_data):
    city = await City.objects.acreate(
        name=test_city_data.name,
        longitude=test_city_data.longitude,
        latitude=test_city_data.latitude,
        is_capital=test_city_data.is_capital,
        country=await Country.objects.aget(iso_code=test_city_data.country_code),
    )
    return city
