from pydantic import BaseModel, Field


class CurrencySchema(BaseModel):
    """
    Pydantic schema for CurrencyAPIRepository. Using for parsing response from CurrencyAPI.
    """

    id: str = Field(..., alias='ID')
    num_code: str = Field(..., alias='NumCode')
    char_code: str = Field(..., alias='CharCode')
    nominal: int = Field(..., alias='Nominal')
    name: str = Field(..., alias='Name')
    value: float = Field(..., alias='Value')
    previous: float = Field(..., alias='Previous')


class CountrySchema(BaseModel):
    """
    Pydantic schema for CountryAPIRepository. Using for parsing response from CountryAPI.
    """
    iso_code: str
    name: str
    capital: str
    capital_longitude: float
    capital_latitude: float
    area_size: float
    population: int
    currencies: dict[str, str]
    languages: list[str]


class WeatherSchema(BaseModel):
    current_weather_temp: float
    current_weather_temp_feels_like: float


class CitySchema(BaseModel):
    name: str
    country_code: str
    longitude: float
    latitude: float
    is_capital: bool
