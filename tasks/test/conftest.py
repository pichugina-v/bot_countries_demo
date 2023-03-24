import asyncio
from typing import Generator

import pytest

pytest_plugins = [
    'cache.test.fixtures'
]


@pytest.fixture(scope='session')
def event_loop(*_, **__) -> Generator:
    """
    Create event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
