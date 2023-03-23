import pytest

from services.repositories.api.api_schemas import WeatherSchema
from services.repositories.api.weather import WeatherAPIRepository


@pytest.mark.asyncio
async def test_get_weather(patched_weather_api_repository: WeatherAPIRepository, weather_api_response: dict) -> None:
    """
    Check normal work of get_weather method

    :param patched_weather_api_repository: weather api repository with mocked method _send_request
    :param weather_api_response: expected response from weather API
    """

    response = await patched_weather_api_repository.get_weather(latitude=11, longitude=22)

    assert isinstance(response, WeatherSchema), f'return invalid type: {type(response)}, expected WeatherSchema'
    assert response.current_weather_temp == weather_api_response['main']['temp']
    assert response.current_weather_temp_feels_like == weather_api_response['main']['feels_like']
