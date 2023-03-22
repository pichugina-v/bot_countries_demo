from dataclasses import dataclass
from http import HTTPStatus
from pprint import pprint

from aiohttp import ClientResponse, ClientSession

from services.repositories.api.abstract_api_repository import AbstractAPIRepository
from services.repositories.api.api_schemas import WeatherSchema
from services.repositories.api.api_settings import WEATHER_API_KEY, WEATHER_INFO_URL


@dataclass
class WeatherAPIRepository(AbstractAPIRepository):
    """
    This is a class of a WeatherAPI repository. Provides information about current weather
    by sending request to external API "Openweathermap.org".
    Extends of the :class:`BaseAPIRepository` class.
    """

    async def get_weather(self, latitude: float, longitude: float) -> WeatherSchema | None:
        """
        Returns information about current weather temperature and current weather 'feels like' temperature.

        :param latitude: latitude coordinate of a place, which temperature is requested for
        :param longitude: longitude coordinate of a place, which temperature is requested for

        :return: a tuple of current weather temperature and current weather 'feels like' temperature in Celsius degrees
        """
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
        }
        response = await self._send_request(url=WEATHER_INFO_URL, params=params)
        if response.status == HTTPStatus.OK:
            return await self._parse_response(response)
        return None

    async def _send_request(self, url: str, params=None, body=None) -> ClientResponse:
        """
        Send GET response

        :param url: API url address
        :param params: optional request's query params
        :param body: optional request's body

        :return: response from API
        """

        async with ClientSession() as session:
            resp = await session.get(url=url, params=params)
        return resp

    async def _parse_response(self, response: ClientResponse) -> WeatherSchema:
        """
        Converts :class:`ClientResponse` into json-object.

        :param response: response from API

        :return: parsed response as a :class:`WeatherData` object
        """
        data_weather = await response.json()
        return WeatherSchema(
            current_weather_temp=data_weather['main']['temp'],
            current_weather_temp_feels_like=data_weather['main']['feels_like'],
        )


def get_weather_repository() -> WeatherAPIRepository:
    """
    Returns object of :class:`WeatherAPIRepository` class

    return: :class:`WeatherAPIRepository` object
    """
    return WeatherAPIRepository()
