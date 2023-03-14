from dataclasses import dataclass
from http import HTTPStatus

from aiohttp import ClientResponse
from pydantic import BaseModel

from services.repositories.api.api_settings import WEATHER_API_KEY, WEATHER_API_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


class WeatherData(BaseModel):
    current_weather_temp: float
    current_weather_temp_feels_like: float


@dataclass
class WeatherAPIRepository(BaseAPIRepository):
    """
    This is a class of a WeatherAPI repository. Provides information about current weather
    by sending request to external API "Openweathermap.org".
    Extends of the :class:`BaseAPIRepository` class.
    """
    api_key: str | None = WEATHER_API_KEY
    api_url: str | None = WEATHER_API_URL

    async def get_weather(self, latitude: float, longitude: float) -> WeatherData | None:
        """
        Returns information about current weather temperature and current weather 'feels like' temperature.

        :param latitude: latitude coordinate of a place, which temperature is requested for
        :param longitude: longitude coordinate of a place, which temperature is requested for

        :return: a tuple of current weather temperature and current weather 'feels like' temperature in Celsius degrees
        """
        if self.api_key and self.api_url:
            weather_api_url = self.api_url.format(lat=latitude, long=longitude, api_key=self.api_key)
        response = await self._send_request(url=weather_api_url)
        if response.status == HTTPStatus.OK:
            return await self._parse_response(response)
        return None

    async def _parse_response(self, response: ClientResponse) -> WeatherData:
        """
        Converts :class:`ClientResponse` into json-object.

        :param response: response from API

        :return: parsed response as a :class:`WeatherData` object
        """
        data_weather = await response.json()
        return WeatherData(
            current_weather_temp=data_weather['main']['temp'],
            current_weather_temp_feels_like=data_weather['main']['feels_like'],
        )


def get_weather_repository() -> WeatherAPIRepository:
    """
    Returns object of :class:`WeatherAPIRepository` class

    return: :class:`WeatherAPIRepository` object
    """
    return WeatherAPIRepository()
