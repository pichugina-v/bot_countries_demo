import json
from http import HTTPStatus

import pytest
import pytest_asyncio
from pytest import MonkeyPatch

from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.tests.mocks import MockClientResponse


@pytest_asyncio.fixture()
async def patched_currency_api_repository(monkeypatch: MonkeyPatch, currency_api_response: dict):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param currency_api_response: normal response from currency API

    :return: patched CurrencyAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(currency_api_response), HTTPStatus.OK)

    currency_api_repository = CurrencyAPIRepository()
    monkeypatch.setattr(currency_api_repository, '_send_request', return_mock)

    yield currency_api_repository


@pytest.fixture
def currency_api_response() -> dict:
    return {
        'Date': '2023-03-17T11:30:00+03:00',
                'PreviousDate': '2023-03-16T11:30:00+03:00',
                'PreviousURL': r'\/\/www.cbr-xml-daily.ru\/archive\/2023\/03\/16\/daily_json.js',
                'Timestamp': '2023-03-16T17:00:00+03:00',
                'Valute': {
                    'AUD': {
                        'ID': 'R01010',
                        'NumCode': '036',
                        'CharCode': 'AUD',
                        'Nominal': 1,
                        'Name': 'Австралийский доллар',
                        'Value': 50.713,
                        'Previous': 50.689
                    },
                    'USD': {
                        'ID': 'R01235',
                        'NumCode': '840',
                        'CharCode': 'USD',
                        'Nominal': 1,
                        'Name': 'Доллар США',
                        'Value': 76.4096,
                        'Previous': 75.7457
                    },
                }}
