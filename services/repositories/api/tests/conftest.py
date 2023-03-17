import asyncio
import json
import platform
from http import HTTPStatus
from typing import Generator

import pytest
import pytest_asyncio

from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.tests.constants import CURRENCY_API_RESPONSE
from services.repositories.api.tests.mocks import MockClientResponse


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """
        Create event loop for testing
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def patched_currency_api_repository(monkeypatch):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :return: patched CurrencyAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(CURRENCY_API_RESPONSE), HTTPStatus.OK)

    currency_api_repository = CurrencyAPIRepository()
    monkeypatch.setattr(currency_api_repository, '_send_request', return_mock)

    yield currency_api_repository
