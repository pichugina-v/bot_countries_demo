import asyncio

import pytest


@pytest.yield_fixture(scope='session')
def event_loop(*args, **kwargs):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
