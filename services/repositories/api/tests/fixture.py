import json
from http import HTTPStatus

import pytest_asyncio
from pytest import MonkeyPatch

from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.tests.mocks import MockClientResponse
from services.repositories.api.weather import WeatherAPIRepository


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def currency_api_response() -> dict:
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


@pytest_asyncio.fixture
async def patched_weather_api_repository(monkeypatch: MonkeyPatch, weather_api_response: dict):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param weather_api_response: expected response from weather API

    :return: patched WeatherAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(weather_api_response), HTTPStatus.OK)

    weather_api_repository = WeatherAPIRepository()
    monkeypatch.setattr(weather_api_repository, '_send_request', return_mock)

    yield weather_api_repository


@pytest_asyncio.fixture
def weather_api_response() -> dict:
    return {
        'base': 'stations',
        'clouds': {'all': 100},
        'cod': 200,
        'coord': {'lat': 55.75, 'lon': 37.61},
        'dt': 1679039854,
        'id': 524901,
        'main': {'feels_like': -1.58,
                 'grnd_level': 1007,
                 'humidity': 94,
                 'pressure': 1025,
                 'sea_level': 1025,
                 'temp': 2.34,
                 'temp_max': 3.06,
                 'temp_min': 1.31},
        'name': 'Moscow',
        'sys': {'country': 'RU',
                'id': 2000314,
                'sunrise': 1679024464,
                'sunset': 1679067308,
                'type': 2},
        'timezone': 10800,
        'visibility': 10000,
        'weather': [{'description': 'overcast clouds',
                    'icon': '04d',
                     'id': 804,
                     'main': 'Clouds'}],
        'wind': {'deg': 12, 'gust': 10.4, 'speed': 4.28}
    }
