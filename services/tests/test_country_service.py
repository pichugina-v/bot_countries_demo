import pytest

from cache.cache_module import Cache

# from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema
from cache.test.fixtures import COUNTRY_NAME
from services.country_service import CountryService


@pytest.mark.asyncio
async def test_get_country_info_from_api_and_create_in_cache(
        expected_geocoder_country_result, patched_geocoder_api_repository_for_country):
    country_info = await CountryService(
        geocoder=patched_geocoder_api_repository_for_country).get_country_info(COUNTRY_NAME)
    cached_country = await Cache().get_country_by_name(COUNTRY_NAME)

    assert country_info == expected_geocoder_country_result
    assert cached_country == expected_geocoder_country_result


@pytest.mark.asyncio
async def test_get_country_info_from_cache(
        expected_geocoder_country_result,
        _create_test_cache_country_by_name, patched_geocoder_api_repository_for_country):
    cached_country = await Cache().get_country_by_name(COUNTRY_NAME)
    country_info = await CountryService(
        geocoder=patched_geocoder_api_repository_for_country).get_country_info(COUNTRY_NAME)

    assert cached_country == country_info
    assert country_info == expected_geocoder_country_result

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_country_from_cache(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_country_from_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_country_from_api_and_create_in_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_languages_from_cache(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_languages_from_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_create_new_country_and_get_languages_from_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_currencies_from_cache(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_get_currencies_from_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_create_new_country_and_get_currencies_from_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_capital_info_from_cache(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_capital_info_from_db(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_currency_rates(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_capital_weather(test_country_data, _create_test_cache_country):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_capital_weather(test_country_data, _create_test_cache_country):
#     pass
