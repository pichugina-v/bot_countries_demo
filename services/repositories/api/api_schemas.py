from pydantic import BaseModel, Field


class CurrencySchema(BaseModel):
    id: str = Field(..., alias='ID')
    num_code: str = Field(..., alias='NumCode')
    char_code: str = Field(..., alias='CharCode')
    nominal: int = Field(..., alias='Nominal')
    name: str = Field(..., alias='Name')
    value: float = Field(..., alias='Value')
    previous: float = Field(..., alias='Previous')


class CurrenciesSchema(BaseModel):
    currencies: list[CurrencySchema]


class CountrySchema(BaseModel):
    iso_code: str
    name_en: str
    name_ru: str
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
