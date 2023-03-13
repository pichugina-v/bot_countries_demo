from dataclasses import dataclass

from aiohttp import ClientResponse

from services.repositories.api.api_settings import WEATHER_API_KEY
from services.repositories.api.api_urls import WEATHER_INFO_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


@dataclass
class WeatherAPIRepository(BaseAPIRepository):
    """
    This is a class of a WeatherAPI repository. Provides information about current weather
    by sending request to external API "Openweathermap.org".
    Extends of the :class:`BaseAPIRepository` class.

    :param api_key: api token for Openweathermap.org API connection
    :type api_key: str
    """
    api_key: str = WEATHER_API_KEY
    api_url: str = WEATHER_INFO_URL

    async def get_weather(self, latitude: float, longitude: float) -> tuple[str]:
        """
        Returns information about current weather temperature and current weather 'feels like' temperature.

        :param latitude: latitude coordinate of a place, which temperature is requested for
        :type latitude: float
        :param longitude: longitude coordinate of a place, which temperature is requested for
        :type longitude: float
        :return: a tuple of current weather temperature and current weather 'feels like' temperature in Celsius degrees
        :rtype: tuple
        """
        weather_api_url = self.api_url.format(lat=latitude, lon=longitude, api_key=self.api_key)
        response = await self._send_request(url=weather_api_url)
        if response.status == 200:
            data_weather = await self._parse_response(response)
            current_weather_temp = data_weather.get('main').get('temp')
            current_weather_temp_feels_like = data_weather.get('main').get('feels_like')
            return current_weather_temp, current_weather_temp_feels_like

    async def _parse_response(self, response: ClientResponse):
        """
        Converts :class:`ClientResponse` into json-object.

        :param response: response from API
        :type response: ClientResponse

        :return: response content as a json-object.
        :rtype: json
        """
        data_weather = await response.json()
        return data_weather


def get_weather_repository():
    return WeatherAPIRepository(WEATHER_API_KEY)
