import pytest

from services.currency_code import CurrenciesCode
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.tests.constants import CURRENCY_API_RESPONSE


@pytest.mark.asyncio
async def test_get_rate_ok(patched_currency_api_repository: CurrencyAPIRepository) -> None:
    """
        Check normal work of get_rate method

    :param patched_currency_api_repository: currency api repository with mocked method _send_request
    """
    char_code = CurrenciesCode(value='USD')
    rate = await patched_currency_api_repository.get_rate(char_code)

    assert isinstance(rate, float), f'return invalid type: {type(rate)}, expected float'
    assert rate == CURRENCY_API_RESPONSE['Valute']['USD']['Value'], 'return invalid rate'
