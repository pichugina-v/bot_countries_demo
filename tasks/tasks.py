import asyncio

from django_layer.celery import app
from services.repositories.api.geocoder import GeocoderAPIRepository

Geocoder = GeocoderAPIRepository()


async def my_coroutine():
    # do some async stuff and return a value

    result = await Geocoder.get_base_info('moscow')
    return result


@app.task()
def sample_task():
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(my_coroutine())
    # coro = my_coroutine()
    print(data)
